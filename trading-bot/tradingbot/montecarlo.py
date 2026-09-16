"""Monte Carlo sobre las operaciones de un backtest: cuánto puede doler la misma estrategia con otra suerte."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Sequence

from .backtest import Trade


@dataclass
class MCResult:
    runs: int
    final_p5: float
    final_p50: float
    final_p95: float
    drawdown_p50: float
    drawdown_p95: float
    prob_hit_max_drawdown: float

    def as_dict(self) -> dict:
        return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in self.__dict__.items()}


def shuffle_trades(trades: Sequence[Trade], initial_equity: float, max_drawdown: float = 0.2, runs: int = 2000, seed: int = 1) -> MCResult:
    """Bootstrap: remuestrea las operaciones con reemplazo y mide la dispersión de resultados.

    Simula "otra tirada" de la misma estrategia: mismas operaciones posibles, distinta suerte.
    Si el percentil 95 del drawdown supera tu kill switch, la estrategia te va a parar
    tarde o temprano. Si el percentil 5 del resultado final está por debajo del capital
    inicial, una racha normal te deja en pérdidas.
    """
    rets = [t.ret for t in trades]
    if not rets:
        return MCResult(0, initial_equity, initial_equity, initial_equity, 0.0, 0.0, 0.0)
    rng = random.Random(seed)
    finals: List[float] = []
    dds: List[float] = []
    hits = 0
    n = len(rets)
    for _ in range(runs):
        sample = [rets[rng.randrange(n)] for _ in range(n)]
        eq, peak, dd = initial_equity, initial_equity, 0.0
        for r in sample:
            eq *= 1 + r
            peak = max(peak, eq)
            dd = max(dd, (peak - eq) / peak)
        finals.append(eq)
        dds.append(dd)
        hits += dd >= max_drawdown
    finals.sort()
    dds.sort()

    def p(xs: List[float], q: float) -> float:
        return xs[min(len(xs) - 1, int(q * len(xs)))]

    return MCResult(runs, p(finals, 0.05), p(finals, 0.5), p(finals, 0.95), p(dds, 0.5), p(dds, 0.95), hits / runs)
