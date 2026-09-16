"""Walk-forward: optimiza en una ventana, valida en la siguiente. Evita engañarte con sobreajuste."""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Dict, List, Sequence, Type

from .backtest import Backtester, Metrics
from .data import Candle
from .risk import RiskConfig
from .strategies import Strategy


@dataclass
class Fold:
    train_start: int
    train_end: int
    test_end: int
    best_params: Dict[str, float]
    train: Metrics
    test: Metrics


def _grid(strategy_cls: Type[Strategy]) -> List[Dict[str, float]]:
    grid = strategy_cls.param_grid()
    if not grid:
        return [{}]
    keys = list(grid)
    return [dict(zip(keys, combo)) for combo in itertools.product(*(grid[k] for k in keys))]


def score(m: Metrics) -> float:
    """Puntuación robusta: penaliza drawdown y pocas operaciones, no solo mira retorno."""
    if m.trades < 10 or m.halted:
        return -1e9
    return m.total_return - 2 * m.max_drawdown


def walk_forward(
    strategy_cls: Type[Strategy],
    candles: Sequence[Candle],
    train_size: int,
    test_size: int,
    risk: RiskConfig | None = None,
    fee: float = 0.001,
    slippage: float = 0.0005,
    initial_equity: float = 1000.0,
) -> List[Fold]:
    risk = risk or RiskConfig()
    folds: List[Fold] = []
    start = 0
    while start + train_size + test_size <= len(candles):
        train = candles[start : start + train_size]
        test = candles[start : start + train_size + test_size]  # incluye historial para indicadores
        best, best_m, best_s = None, None, -1e18
        for params in _grid(strategy_cls):
            m = Backtester(strategy_cls(**params), risk, fee, slippage, initial_equity).run(train).metrics
            s = score(m)
            if s > best_s:
                best, best_m, best_s = params, m, s
        assert best is not None and best_m is not None
        # Evaluación out-of-sample: solo cuentan las operaciones abiertas dentro de la ventana de test
        res = Backtester(strategy_cls(**best), risk, fee, slippage, initial_equity).run(test)
        test_start_ts = candles[start + train_size].ts
        oos_trades = [t for t in res.trades if t.entry_ts >= test_start_ts]
        oos_curve = res.equity_curve[train_size:]
        from .backtest import compute_metrics

        base = res.equity_curve[train_size - 1] if train_size > 0 else initial_equity
        test_m = compute_metrics(oos_trades, oos_curve, base, res.metrics.halted)
        folds.append(Fold(start, start + train_size, start + train_size + test_size, best, best_m, test_m))
        start += test_size
    return folds


def summarize(folds: List[Fold]) -> Dict[str, float]:
    if not folds:
        return {}
    oos = [f.test for f in folds]
    compounded = 1.0
    for m in oos:
        compounded *= 1 + m.total_return
    return {
        "folds": len(folds),
        "oos_return_compounded": round(compounded - 1, 4),
        "oos_avg_win_rate": round(sum(m.win_rate for m in oos) / len(oos), 4),
        "oos_worst_drawdown": round(max(m.max_drawdown for m in oos), 4),
        "oos_folds_positive": sum(1 for m in oos if m.total_return > 0),
        "oos_total_trades": sum(m.trades for m in oos),
    }
