"""Estrategias declarativas: reglas en JSON para probar ideas sin escribir código.

Formato:
{
  "name": "rsi_rebote",
  "indicators": {
    "rsi14": {"type": "rsi", "period": 14},
    "sma50": {"type": "sma", "period": 50},
    "bb":    {"type": "bbands", "period": 20, "mult": 2.0}     -> bb_mid, bb_up, bb_lo
  },
  "long_entry":  [["rsi14", "<", 30], ["close", ">", "sma50"]],
  "long_exit":   [["rsi14", ">", 55]],
  "short_entry": [["rsi14", ">", 70], ["close", "<", "sma50"]],
  "short_exit":  [["rsi14", "<", 45]],
  "grid": {"rsi14.period": [10, 14, 20], "sma50.period": [30, 50, 100]}
}

Operadores: <, >, <=, >=, crosses_above, crosses_below.
Operandos: nombre de indicador, open/high/low/close, o un número.
Todas las condiciones de una lista deben cumplirse (AND).
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Type

from .data import Candle
from .indicators import atr, bollinger, closes, ema, rsi, sma
from .strategies import Strategy

OPS = {"<", ">", "<=", ">=", "crosses_above", "crosses_below"}
PRICE_FIELDS = {"open", "high", "low", "close"}


def _compute_indicators(spec: Dict[str, Any], candles: Sequence[Candle]) -> Dict[str, List[Optional[float]]]:
    c = closes(candles)
    out: Dict[str, List[Optional[float]]] = {
        "open": [x.open for x in candles],
        "high": [x.high for x in candles],
        "low": [x.low for x in candles],
        "close": c,
    }
    for name, ind in spec.get("indicators", {}).items():
        t = ind["type"]
        if t == "sma":
            out[name] = sma(c, int(ind["period"]))
        elif t == "ema":
            out[name] = ema(c, int(ind["period"]))
        elif t == "rsi":
            out[name] = rsi(c, int(ind.get("period", 14)))
        elif t == "atr":
            out[name] = atr(candles, int(ind.get("period", 14)))
        elif t == "bbands":
            mid, up, lo = bollinger(c, int(ind.get("period", 20)), float(ind.get("mult", 2.0)))
            out[f"{name}_mid"], out[f"{name}_up"], out[f"{name}_lo"] = mid, up, lo
        else:
            raise ValueError(f"Indicador desconocido: {t}")
    return out


def _operand(series: Dict[str, List[Optional[float]]], x: Any, i: int) -> Optional[float]:
    if isinstance(x, (int, float)):
        return float(x)
    if x not in series:
        raise KeyError(f"Operando desconocido en reglas: {x}")
    return series[x][i]


def _cond(series, cond, i: int) -> bool:
    left, op, right = cond
    if op not in OPS:
        raise ValueError(f"Operador desconocido: {op}")
    a, b = _operand(series, left, i), _operand(series, right, i)
    if a is None or b is None:
        return False
    if op == "<":
        return a < b
    if op == ">":
        return a > b
    if op == "<=":
        return a <= b
    if op == ">=":
        return a >= b
    if i == 0:
        return False
    pa, pb = _operand(series, left, i - 1), _operand(series, right, i - 1)
    if pa is None or pb is None:
        return False
    if op == "crosses_above":
        return pa <= pb and a > b
    return pa >= pb and a < b  # crosses_below


def _all(series, conds, i: int) -> bool:
    return bool(conds) and all(_cond(series, c, i) for c in conds)


class RuleStrategy(Strategy):
    spec: Dict[str, Any] = {}

    def __init__(self, **overrides: float) -> None:
        self.spec = copy.deepcopy(type(self).spec)
        self.name = self.spec.get("name", "rules")
        for key, value in overrides.items():
            ind, _, field = key.partition("__")
            if ind not in self.spec.get("indicators", {}):
                raise KeyError(f"Parámetro desconocido: {key}")
            self.spec["indicators"][ind][field] = value
        self.params = dict(overrides)

    def signals(self, candles: Sequence[Candle]) -> List[int]:
        s = _compute_indicators(self.spec, candles)
        le, lx = self.spec.get("long_entry", []), self.spec.get("long_exit", [])
        se, sx = self.spec.get("short_entry", []), self.spec.get("short_exit", [])
        out = [0] * len(candles)
        pos = 0
        for i in range(len(candles)):
            if pos == 1 and _all(s, lx, i):
                pos = 0
            elif pos == -1 and _all(s, sx, i):
                pos = 0
            if pos == 0:
                if _all(s, le, i):
                    pos = 1
                elif _all(s, se, i):
                    pos = -1
            out[i] = pos
        return out

    @classmethod
    def param_grid(cls) -> Dict[str, List[float]]:
        return {k.replace(".", "__"): v for k, v in cls.spec.get("grid", {}).items()}


def load_rules(path: str | Path) -> Type[RuleStrategy]:
    """Crea una clase de estrategia a partir de un JSON de reglas."""
    spec = json.loads(Path(path).read_text())
    validate(spec)
    return type(f"Rules_{spec.get('name', 'custom')}", (RuleStrategy,), {"spec": spec})


def validate(spec: Dict[str, Any]) -> None:
    if not any(spec.get(k) for k in ("long_entry", "short_entry")):
        raise ValueError("Las reglas necesitan al menos long_entry o short_entry")
    names = set(PRICE_FIELDS)
    for n, ind in spec.get("indicators", {}).items():
        if ind.get("type") == "bbands":
            names |= {f"{n}_mid", f"{n}_up", f"{n}_lo"}
        else:
            names.add(n)
    for key in ("long_entry", "long_exit", "short_entry", "short_exit"):
        for cond in spec.get(key, []):
            if len(cond) != 3 or cond[1] not in OPS:
                raise ValueError(f"Condición inválida en {key}: {cond}")
            for x in (cond[0], cond[2]):
                if not isinstance(x, (int, float)) and x not in names:
                    raise ValueError(f"Operando desconocido en {key}: {x}")
