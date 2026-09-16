"""Brokers: paper (simulado, por defecto) y live (ccxt, requiere confirmación explícita)."""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Position:
    side: int = 0
    units: float = 0.0
    entry: float = 0.0
    stop: Optional[float] = None
    tp: Optional[float] = None


@dataclass
class PaperBroker:
    """Simula ejecuciones y persiste el estado en JSON para sobrevivir reinicios."""

    equity: float
    fee: float = 0.001
    slippage: float = 0.0005
    state_path: Optional[Path] = None
    position: Position = field(default_factory=Position)
    log: list = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.state_path and Path(self.state_path).exists():
            data = json.loads(Path(self.state_path).read_text())
            self.equity = data["equity"]
            self.position = Position(**data["position"])
            self.log = data.get("log", [])

    def _save(self) -> None:
        if self.state_path:
            Path(self.state_path).write_text(
                json.dumps({"equity": self.equity, "position": self.position.__dict__, "log": self.log[-500:]}, indent=2)
            )

    def open(self, side: int, units: float, price: float, stop, tp) -> None:
        px = price * (1 + self.slippage * side)
        self.equity -= px * units * self.fee
        self.position = Position(side, units, px, stop, tp)
        self.log.append({"t": time.time(), "action": "open", "side": side, "units": units, "price": px})
        self._save()

    def close(self, price: float, reason: str) -> float:
        p = self.position
        if p.side == 0:
            return 0.0
        px = price * (1 - self.slippage * p.side)
        pnl = (px - p.entry) * p.units * p.side - px * p.units * self.fee
        self.equity += pnl
        self.log.append({"t": time.time(), "action": "close", "price": px, "pnl": pnl, "reason": reason})
        self.position = Position()
        self._save()
        return pnl

    def mark(self, price: float) -> float:
        p = self.position
        return self.equity + ((price - p.entry) * p.units * p.side if p.side else 0.0)


class LiveBroker:
    """Envía órdenes reales por ccxt. Desactivado salvo que TRADINGBOT_LIVE=I_UNDERSTAND_THE_RISK."""

    def __init__(self, exchange_id: str, symbol: str, api_key: str, secret: str, fee: float = 0.001):
        if os.environ.get("TRADINGBOT_LIVE") != "I_UNDERSTAND_THE_RISK":
            raise RuntimeError(
                "Modo live bloqueado. Ejecuta primero semanas de paper trading y, si aun así quieres, "
                "exporta TRADINGBOT_LIVE=I_UNDERSTAND_THE_RISK"
            )
        import ccxt  # type: ignore

        self.ex = getattr(ccxt, exchange_id)({"apiKey": api_key, "secret": secret, "enableRateLimit": True})
        self.symbol = symbol
        self.fee = fee
        self.position = Position()

    @property
    def equity(self) -> float:
        bal = self.ex.fetch_balance()
        quote = self.symbol.split("/")[1]
        return float(bal["total"].get(quote, 0.0))

    def open(self, side: int, units: float, price: float, stop, tp) -> None:
        if side < 0:
            raise RuntimeError("Cortos en spot no soportados; usa solo señales largas en live")
        order = self.ex.create_market_buy_order(self.symbol, units)
        self.position = Position(side, units, float(order.get("average") or price), stop, tp)

    def close(self, price: float, reason: str) -> float:
        if self.position.side == 0:
            return 0.0
        order = self.ex.create_market_sell_order(self.symbol, self.position.units)
        px = float(order.get("average") or price)
        pnl = (px - self.position.entry) * self.position.units
        self.position = Position()
        return pnl

    def mark(self, price: float) -> float:
        return self.equity
