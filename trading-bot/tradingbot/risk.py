"""Gestión de riesgo: lo único que de verdad separa un bot que sobrevive de uno que no."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskConfig:
    risk_per_trade: float = 0.01       # fracción del capital arriesgada por operación (1 %)
    stop_atr_mult: float = 2.0         # stop-loss a N ATR de la entrada
    take_profit_atr_mult: float = 4.0  # take-profit a N ATR (0 = sin TP, cierra por señal)
    max_leverage: float = 1.0          # 1.0 = sin apalancamiento
    max_drawdown: float = 0.20         # kill switch: si el drawdown supera 20 %, el bot se para
    max_daily_loss: float = 0.05       # pérdida máxima diaria antes de parar el día
    max_position_pct: float = 1.0      # nunca más del 100 % del capital en una posición

    def validate(self) -> None:
        if not 0 < self.risk_per_trade <= 0.1:
            raise ValueError("risk_per_trade debe estar entre 0 y 0.1 (10 %). Más es suicida.")
        if self.max_leverage < 1:
            raise ValueError("max_leverage mínimo 1")
        if self.stop_atr_mult <= 0:
            raise ValueError("stop_atr_mult debe ser > 0")


@dataclass
class RiskManager:
    cfg: RiskConfig

    def __post_init__(self) -> None:
        self.cfg.validate()

    def position_size(self, equity: float, price: float, atr_value: float) -> float:
        """Unidades a comprar para que, si salta el stop, se pierda risk_per_trade * equity."""
        if price <= 0 or atr_value <= 0 or equity <= 0:
            return 0.0
        stop_distance = atr_value * self.cfg.stop_atr_mult
        units = (equity * self.cfg.risk_per_trade) / stop_distance
        max_units = (equity * self.cfg.max_leverage * self.cfg.max_position_pct) / price
        return min(units, max_units)

    def stop_price(self, entry: float, side: int, atr_value: float) -> float:
        return entry - side * atr_value * self.cfg.stop_atr_mult

    def take_profit_price(self, entry: float, side: int, atr_value: float):
        if self.cfg.take_profit_atr_mult <= 0:
            return None
        return entry + side * atr_value * self.cfg.take_profit_atr_mult

    def drawdown_breached(self, equity: float, peak_equity: float) -> bool:
        if peak_equity <= 0:
            return False
        return (peak_equity - equity) / peak_equity >= self.cfg.max_drawdown

    def daily_loss_breached(self, equity: float, day_start_equity: float) -> bool:
        if day_start_equity <= 0:
            return False
        return (day_start_equity - equity) / day_start_equity >= self.cfg.max_daily_loss
