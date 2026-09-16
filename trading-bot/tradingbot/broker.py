"""Brokers: paper (simulado, por defecto) y live (ccxt, requiere confirmación explícita)."""
from __future__ import annotations

import csv
import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

log = logging.getLogger("tradingbot.broker")


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
        self._journal(p, px, pnl, reason)
        self.position = Position()
        self._save()
        return pnl

    def _journal(self, p: Position, exit_px: float, pnl: float, reason: str) -> None:
        """Añade la operación cerrada a trades.csv junto al fichero de estado."""
        if not self.state_path:
            return
        path = Path(self.state_path).with_name("trades.csv")
        new = not path.exists()
        with open(path, "a", newline="") as fh:
            w = csv.writer(fh)
            if new:
                w.writerow(["closed_at", "side", "units", "entry", "exit", "pnl", "reason", "equity_after"])
            w.writerow([int(time.time()), p.side, p.units, p.entry, exit_px, round(pnl, 6), reason, round(self.equity, 6)])

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
        self.ex.load_markets()
        if symbol not in self.ex.markets:
            raise ValueError(f"{symbol} no existe en {exchange_id}")
        self.market = self.ex.markets[symbol]
        self.symbol = symbol
        self.fee = fee
        self.position = Position()

    def _normalize(self, units: float, price: float) -> float:
        """Ajusta la cantidad a la precisión del exchange y comprueba mínimos. 0 si no es válida."""
        limits = self.market.get("limits", {}) or {}
        min_amt = (limits.get("amount") or {}).get("min") or 0
        min_cost = (limits.get("cost") or {}).get("min") or 0
        amt = float(self.ex.amount_to_precision(self.symbol, units))
        if amt < min_amt or amt * price < min_cost:
            log.warning("Orden por debajo del mínimo del exchange (%.8f uds, %.2f de coste). No se envía.", amt, amt * price)
            return 0.0
        return amt

    @property
    def equity(self) -> float:
        bal = self.ex.fetch_balance()
        quote = self.symbol.split("/")[1]
        return float(bal["total"].get(quote, 0.0))

    def open(self, side: int, units: float, price: float, stop, tp) -> None:
        if side < 0:
            log.info("Señal corta ignorada: cortos en spot no soportados en live")
            return
        amt = self._normalize(units, price)
        if amt <= 0:
            return
        order = self.ex.create_market_buy_order(self.symbol, amt)
        filled = float(order.get("filled") or amt)
        self.position = Position(side, filled, float(order.get("average") or price), stop, tp)

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
