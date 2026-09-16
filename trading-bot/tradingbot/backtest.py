"""Motor de backtest con comisiones, slippage, stops intrabar y métricas honestas."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence

from .data import Candle
from .indicators import atr
from .risk import RiskConfig, RiskManager
from .strategies import Strategy

DAY_MS = 86_400_000


@dataclass
class Trade:
    side: int
    entry_ts: int
    entry: float
    exit_ts: int
    exit: float
    units: float
    pnl: float
    reason: str  # "signal" | "stop" | "tp" | "end" | "killswitch" | "dailylimit"

    @property
    def ret(self) -> float:
        return self.pnl / (self.entry * self.units) if self.units else 0.0


@dataclass
class Metrics:
    trades: int
    win_rate: float
    expectancy: float        # ganancia media por operación en dinero
    profit_factor: float
    total_return: float
    max_drawdown: float
    sharpe: float
    final_equity: float
    halted: bool

    def as_dict(self) -> dict:
        return {
            "trades": self.trades,
            "win_rate": round(self.win_rate, 4),
            "expectancy": round(self.expectancy, 4),
            "profit_factor": round(self.profit_factor, 3),
            "total_return": round(self.total_return, 4),
            "max_drawdown": round(self.max_drawdown, 4),
            "sharpe": round(self.sharpe, 3),
            "final_equity": round(self.final_equity, 2),
            "halted": self.halted,
        }


@dataclass
class BacktestResult:
    trades: List[Trade]
    equity_curve: List[float]
    metrics: Metrics


@dataclass
class Backtester:
    strategy: Strategy
    risk: RiskConfig = field(default_factory=RiskConfig)
    fee: float = 0.001         # 0.1 % por lado (típico en cripto spot)
    slippage: float = 0.0005   # 0.05 % adverso en cada ejecución
    initial_equity: float = 1000.0
    atr_period: int = 14

    def run(self, candles: Sequence[Candle]) -> BacktestResult:
        rm = RiskManager(self.risk)
        sig = self.strategy.signals(candles)
        a = atr(candles, self.atr_period)

        equity = self.initial_equity
        peak = equity
        day_start_equity = equity
        current_day = candles[0].ts // DAY_MS if candles else 0
        curve: List[float] = []
        trades: List[Trade] = []
        halted = False
        paused_day: Optional[int] = None

        pos = 0
        units = 0.0
        entry = 0.0
        entry_ts = 0
        stop: Optional[float] = None
        tp: Optional[float] = None

        def fill(price: float, side: int) -> float:
            # slippage siempre en contra
            return price * (1 + self.slippage * side)

        def close_position(price: float, ts: int, reason: str) -> None:
            nonlocal equity, pos, units, entry, stop, tp
            exit_price = fill(price, -pos)
            gross = (exit_price - entry) * units * pos
            fees = (entry + exit_price) * units * self.fee
            pnl = gross - fees
            equity += pnl
            trades.append(Trade(pos, entry_ts, entry, ts, exit_price, units, pnl, reason))
            pos, units, entry, stop, tp = 0, 0.0, 0.0, None, None

        for i, c in enumerate(candles):
            day = c.ts // DAY_MS
            if day != current_day:
                current_day = day
                day_start_equity = equity

            # 1) stops / take-profit intrabar sobre la posición abierta
            if pos != 0:
                hit_stop = stop is not None and (c.low <= stop if pos == 1 else c.high >= stop)
                hit_tp = tp is not None and (c.high >= tp if pos == 1 else c.low <= tp)
                if hit_stop:  # pesimista: si toca ambos en la misma vela, asumimos stop
                    close_position(stop, c.ts, "stop")
                elif hit_tp:
                    close_position(tp, c.ts, "tp")

            # 2) kill switch definitivo (drawdown) y pausa diaria (pérdida del día)
            if not halted and rm.drawdown_breached(equity, peak):
                if pos != 0:
                    close_position(c.close, c.ts, "killswitch")
                halted = True
            if paused_day != day and rm.daily_loss_breached(equity, day_start_equity):
                if pos != 0:
                    close_position(c.close, c.ts, "dailylimit")
                paused_day = day

            # 3) señal al cierre de vela (ejecuta al cierre; sin mirar el futuro)
            if not halted and paused_day != day and a[i] is not None:
                s = sig[i]
                if pos != 0 and s != pos:
                    close_position(c.close, c.ts, "signal")
                if pos == 0 and s != 0:
                    u = rm.position_size(equity, c.close, a[i])
                    if u > 0:
                        pos = s
                        units = u
                        entry = fill(c.close, s)
                        entry_ts = c.ts
                        stop = rm.stop_price(entry, s, a[i])
                        tp = rm.take_profit_price(entry, s, a[i])

            # 4) equity mark-to-market
            mtm = equity + ((c.close - entry) * units * pos if pos != 0 else 0.0)
            peak = max(peak, mtm)
            curve.append(mtm)

        if pos != 0 and candles:
            close_position(candles[-1].close, candles[-1].ts, "end")
            curve[-1] = equity

        return BacktestResult(trades, curve, compute_metrics(trades, curve, self.initial_equity, halted))


def compute_metrics(trades: List[Trade], curve: List[float], initial: float, halted: bool) -> Metrics:
    n = len(trades)
    wins = [t.pnl for t in trades if t.pnl > 0]
    losses = [-t.pnl for t in trades if t.pnl <= 0]
    win_rate = len(wins) / n if n else 0.0
    expectancy = sum(t.pnl for t in trades) / n if n else 0.0
    gross_loss = sum(losses)
    profit_factor = (sum(wins) / gross_loss) if gross_loss > 0 else (math.inf if wins else 0.0)

    final = curve[-1] if curve else initial
    total_return = final / initial - 1 if initial else 0.0

    peak, mdd = -math.inf, 0.0
    for v in curve:
        peak = max(peak, v)
        if peak > 0:
            mdd = max(mdd, (peak - v) / peak)

    rets = [curve[i] / curve[i - 1] - 1 for i in range(1, len(curve)) if curve[i - 1] > 0]
    if len(rets) > 1:
        mean = sum(rets) / len(rets)
        var = sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)
        sd = var ** 0.5
        # anualización asumiendo velas horarias (24*365); ajusta si usas otro timeframe
        sharpe = (mean / sd) * math.sqrt(24 * 365) if sd > 0 else 0.0
    else:
        sharpe = 0.0

    return Metrics(n, win_rate, expectancy, profit_factor, total_return, mdd, sharpe, final, halted)
