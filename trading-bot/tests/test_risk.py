import pytest

from tradingbot.risk import RiskConfig, RiskManager


def test_position_size_respects_risk():
    rm = RiskManager(RiskConfig(risk_per_trade=0.01, stop_atr_mult=2.0))
    units = rm.position_size(equity=1000, price=50, atr_value=1.0)
    # stop a 2 unidades de precio -> pérdida = 2 * units = 10 (1 % de 1000)
    assert abs(units * 2.0 - 10.0) < 1e-9


def test_position_size_capped_by_leverage():
    rm = RiskManager(RiskConfig(risk_per_trade=0.05, stop_atr_mult=0.1, max_leverage=1.0))
    units = rm.position_size(equity=1000, price=100, atr_value=0.01)
    assert units <= 10.0 + 1e-9  # nunca más de 1000/100 unidades


def test_rejects_absurd_risk():
    with pytest.raises(ValueError):
        RiskManager(RiskConfig(risk_per_trade=0.5))


def test_kill_switch():
    rm = RiskManager(RiskConfig(max_drawdown=0.2, max_daily_loss=0.05))
    assert rm.drawdown_breached(79, 100)
    assert not rm.drawdown_breached(81, 100)
    assert rm.daily_loss_breached(94, 100)


def test_stop_and_tp_sides():
    rm = RiskManager(RiskConfig(stop_atr_mult=2, take_profit_atr_mult=4))
    assert rm.stop_price(100, 1, 1.0) == 98 and rm.take_profit_price(100, 1, 1.0) == 104
    assert rm.stop_price(100, -1, 1.0) == 102 and rm.take_profit_price(100, -1, 1.0) == 96
