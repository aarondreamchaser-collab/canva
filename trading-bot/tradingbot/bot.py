"""Bucle de ejecución: cada vela nueva -> señal -> riesgo -> broker."""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Callable, List, Optional

from .data import Candle
from .indicators import atr
from .risk import RiskConfig, RiskManager
from .strategies import Strategy

log = logging.getLogger("tradingbot")


@dataclass
class Bot:
    strategy: Strategy
    broker: object                 # PaperBroker o LiveBroker
    risk: RiskConfig
    fetch: Callable[[], List[Candle]]   # devuelve el historial reciente de velas
    poll_seconds: int = 60
    atr_period: int = 14

    def __post_init__(self) -> None:
        self.rm = RiskManager(self.risk)
        self.peak = float(self.broker.equity)
        self.halted = False
        self.last_ts: Optional[int] = None
        self.day: Optional[int] = None
        self.day_start_equity = self.peak
        self.paused_day: Optional[int] = None

    def step(self, candles: List[Candle]) -> None:
        if len(candles) < self.atr_period + 2:
            return
        c = candles[-1]
        if self.last_ts == c.ts:
            return
        self.last_ts = c.ts
        sig = self.strategy.signals(candles)[-1]
        a = atr(candles, self.atr_period)[-1]
        p = self.broker.position

        if p.side != 0:
            if p.stop is not None and (c.low <= p.stop if p.side == 1 else c.high >= p.stop):
                log.info("STOP tocado a %.4f", p.stop)
                self.broker.close(p.stop, "stop")
            elif p.tp is not None and (c.high >= p.tp if p.side == 1 else c.low <= p.tp):
                log.info("TAKE PROFIT tocado a %.4f", p.tp)
                self.broker.close(p.tp, "tp")

        day = c.ts // 86_400_000
        if day != self.day:
            self.day = day
            self.day_start_equity = float(self.broker.equity)
        eq = self.broker.mark(c.close)
        self.peak = max(self.peak, eq)
        if self.paused_day != day and self.rm.daily_loss_breached(eq, self.day_start_equity):
            log.warning("Límite de pérdida diaria alcanzado. Sin operar hasta mañana.")
            if self.broker.position.side:
                self.broker.close(c.close, "dailylimit")
            self.paused_day = day
        if self.paused_day == day:
            return
        if self.rm.drawdown_breached(eq, self.peak):
            if not self.halted:
                log.error("KILL SWITCH: drawdown %.1f%% supera el límite. Bot parado.", (1 - eq / self.peak) * 100)
                if self.broker.position.side:
                    self.broker.close(c.close, "killswitch")
            self.halted = True
            return

        p = self.broker.position
        if a is None:
            return
        if p.side != 0 and sig != p.side:
            self.broker.close(c.close, "signal")
            log.info("Cierre por señal a %.4f | equity %.2f", c.close, self.broker.equity)
        if self.broker.position.side == 0 and sig != 0:
            units = self.rm.position_size(float(self.broker.equity), c.close, a)
            if units > 0:
                stop = self.rm.stop_price(c.close, sig, a)
                tp = self.rm.take_profit_price(c.close, sig, a)
                self.broker.open(sig, units, c.close, stop, tp)
                log.info("Abre %s %.6f uds a %.4f | stop %.4f | tp %s", "LARGO" if sig == 1 else "CORTO", units, c.close, stop, tp)

    def run_forever(self) -> None:
        log.info("Bot en marcha. Estrategia=%s equity=%.2f", self.strategy.name, float(self.broker.equity))
        while not self.halted:
            try:
                self.step(self.fetch())
            except Exception:  # noqa: BLE001
                log.exception("Error en el ciclo; reintento en %ss", self.poll_seconds)
            time.sleep(self.poll_seconds)
