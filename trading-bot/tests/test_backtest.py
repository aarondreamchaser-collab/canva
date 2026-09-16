from tradingbot.backtest import Backtester
from tradingbot.data import Candle, synthetic
from tradingbot.goal import analyze
from tradingbot.risk import RiskConfig
from tradingbot.strategies import MeanReversion, RegimeSwitch, Strategy, TrendFollowing
from tradingbot.walkforward import summarize, walk_forward


class AlwaysLong(Strategy):
    name = "always_long"

    def signals(self, candles):
        return [1] * len(candles)


def flat_candles(n=60, price=100.0):
    return [Candle(1_600_000_000_000 + i * 3_600_000, price, price, price, price, 1.0) for i in range(n)]


def test_fees_and_slippage_lose_money_on_flat_market():
    # Con precio constante el ATR es 0 -> no abre. Usamos velas con rango mínimo.
    c = [Candle(1_600_000_000_000 + i * 3_600_000, 100, 100.5, 99.5, 100, 1.0) for i in range(60)]
    res = Backtester(AlwaysLong(), RiskConfig(), fee=0.001, slippage=0.0005, initial_equity=1000).run(c)
    assert res.metrics.trades == 1
    assert res.metrics.final_equity < 1000  # comisiones + slippage cuestan dinero


def test_stop_loss_limits_loss():
    # Sube tranquila y luego se desploma: el stop debe cortar la pérdida cerca del 1 %
    up = [Candle(1_600_000_000_000 + i * 3_600_000, 100 + i, 100.6 + i, 99.4 + i, 100 + i, 1.0) for i in range(30)]
    crash = [Candle(up[-1].ts + (i + 1) * 3_600_000, 60, 61, 55, 56, 1.0) for i in range(5)]
    res = Backtester(AlwaysLong(), RiskConfig(risk_per_trade=0.01), initial_equity=1000).run(up + crash)
    stops = [t for t in res.trades if t.reason == "stop"]
    assert stops, "debería haber saltado el stop"
    assert res.metrics.max_drawdown < 0.03


def test_kill_switch_halts_backtest():
    up = [Candle(1_600_000_000_000 + i * 3_600_000, 100 + i, 100.6 + i, 99.4 + i, 100 + i, 1.0) for i in range(30)]
    # cada vela cae 30 % respecto a la anterior: reabre y vuelve a perder hasta que salta el kill switch
    p = 130.0
    crash = []
    for i in range(20):
        lo = p * 0.7
        crash.append(Candle(up[-1].ts + (i + 1) * 3_600_000, p, p, lo, lo, 1.0))
        p = lo
    res = Backtester(AlwaysLong(), RiskConfig(max_drawdown=0.05, max_daily_loss=0.99), initial_equity=1000).run(up + crash)
    assert res.metrics.halted


def test_all_strategies_run_on_synthetic():
    c = synthetic(1500)
    for s in (TrendFollowing(), MeanReversion(), RegimeSwitch()):
        res = Backtester(s, initial_equity=100).run(c)
        assert len(res.equity_curve) == len(c)
        assert 0 <= res.metrics.win_rate <= 1
        assert res.metrics.max_drawdown <= RiskConfig().max_drawdown + 0.05


def test_walkforward_produces_folds():
    c = synthetic(1600)
    folds = walk_forward(MeanReversion, c, train_size=800, test_size=300, initial_equity=100)
    assert len(folds) == 2
    s = summarize(folds)
    assert s["folds"] == 2 and "oos_return_compounded" in s


def test_goal_math():
    g = analyze(100, 10000, 30)
    assert abs(g.multiple - 100) < 1e-9
    assert 0.16 < g.daily_return_needed < 0.17
    assert g.prob_success < 0.01
