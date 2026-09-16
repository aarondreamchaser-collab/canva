"""Estrategias. Cada una devuelve una señal por vela: 1 (largo), -1 (corto), 0 (plano/cerrar)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence

from .data import Candle
from .indicators import bollinger, closes, ema, rsi, sma


class Strategy:
    name = "base"
    params: Dict[str, float]

    def signals(self, candles: Sequence[Candle]) -> List[int]:
        raise NotImplementedError

    @classmethod
    def param_grid(cls) -> Dict[str, List[float]]:
        """Rejilla de parámetros para la optimización walk-forward."""
        return {}


@dataclass
class TrendFollowing(Strategy):
    """Cruce de EMAs con filtro de tendencia largo plazo. Pocos aciertos, ganancias grandes."""

    fast: int = 12
    slow: int = 26
    trend: int = 100
    name: str = field(default="trend", init=False)

    def signals(self, candles: Sequence[Candle]) -> List[int]:
        c = closes(candles)
        f, s, t = ema(c, self.fast), ema(c, self.slow), sma(c, self.trend)
        out = [0] * len(c)
        for i in range(len(c)):
            if f[i] is None or s[i] is None or t[i] is None:
                continue
            if f[i] > s[i] and c[i] > t[i]:
                out[i] = 1
            elif f[i] < s[i] and c[i] < t[i]:
                out[i] = -1
            else:
                out[i] = 0
        return out

    @classmethod
    def param_grid(cls):
        return {"fast": [8, 12, 20], "slow": [26, 40, 60], "trend": [100, 150, 200]}


@dataclass
class MeanReversion(Strategy):
    """Bandas de Bollinger + RSI. Muchos aciertos pequeños, pérdidas ocasionales grandes."""

    period: int = 20
    mult: float = 2.0
    rsi_period: int = 14
    rsi_low: float = 30.0
    rsi_high: float = 70.0
    name: str = field(default="meanrev", init=False)

    def signals(self, candles: Sequence[Candle]) -> List[int]:
        c = closes(candles)
        mid, up, lo = bollinger(c, self.period, self.mult)
        r = rsi(c, self.rsi_period)
        out = [0] * len(c)
        pos = 0
        for i in range(len(c)):
            if mid[i] is None or r[i] is None:
                continue
            if pos == 0:
                if c[i] < lo[i] and r[i] < self.rsi_low:
                    pos = 1
                elif c[i] > up[i] and r[i] > self.rsi_high:
                    pos = -1
            elif pos == 1 and c[i] >= mid[i]:
                pos = 0
            elif pos == -1 and c[i] <= mid[i]:
                pos = 0
            out[i] = pos
        return out

    @classmethod
    def param_grid(cls):
        return {"period": [14, 20, 30], "mult": [1.5, 2.0, 2.5], "rsi_low": [25, 30, 35]}


@dataclass
class RegimeSwitch(Strategy):
    """Usa tendencia cuando el mercado se mueve y reversión cuando está en rango.

    Régimen medido con el Efficiency Ratio de Kaufman: desplazamiento neto / camino recorrido.
    Cerca de 1 = tendencia limpia; cerca de 0 = rango ruidoso.
    """

    er_period: int = 20
    er_threshold: float = 0.3
    trend_period: int = 100
    name: str = field(default="regime", init=False)

    def signals(self, candles: Sequence[Candle]) -> List[int]:
        c = closes(candles)
        tf = TrendFollowing(trend=self.trend_period).signals(candles)
        mr = MeanReversion().signals(candles)
        out = [0] * len(c)
        n = self.er_period
        for i in range(n, len(c)):
            path = sum(abs(c[j] - c[j - 1]) for j in range(i - n + 1, i + 1))
            er = abs(c[i] - c[i - n]) / path if path > 0 else 0.0
            out[i] = tf[i] if er > self.er_threshold else mr[i]
        return out

    @classmethod
    def param_grid(cls):
        return {"er_period": [10, 20, 30], "er_threshold": [0.2, 0.3, 0.45]}


REGISTRY = {"trend": TrendFollowing, "meanrev": MeanReversion, "regime": RegimeSwitch}


def make(name: str, **params) -> Strategy:
    if name not in REGISTRY:
        raise KeyError(f"Estrategia desconocida: {name}. Opciones: {list(REGISTRY)}")
    return REGISTRY[name](**params)
