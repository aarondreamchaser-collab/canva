from tradingbot.bot import Bot
from tradingbot.broker import PaperBroker
from tradingbot.data import synthetic
from tradingbot.risk import RiskConfig
from tradingbot.strategies import MeanReversion


def test_bot_loop_trades_and_persists(tmp_path):
    candles = synthetic(900, seed=3)
    state = tmp_path / "state.json"
    broker = PaperBroker(100.0, state_path=state)
    bot = Bot(MeanReversion(), broker, RiskConfig(), fetch=lambda: [], poll_seconds=0)
    for i in range(200, len(candles)):
        bot.step(candles[: i + 1])
    assert state.exists() and (tmp_path / "trades.csv").exists()
    lines = (tmp_path / "trades.csv").read_text().strip().splitlines()
    assert len(lines) >= 2  # cabecera + al menos una operación
    assert abs(PaperBroker(0.0, state_path=state).equity - broker.equity) < 1e-9


def test_bot_reoptimizes_periodically(tmp_path):
    candles = synthetic(900, seed=5)
    broker = PaperBroker(100.0, state_path=tmp_path / "s.json")
    bot = Bot(MeanReversion(), broker, RiskConfig(), fetch=lambda: [], poll_seconds=0,
              reoptimize_every=100, reoptimize_window=300)
    seen = set()
    for i in range(300, len(candles)):
        bot.step(candles[: i + 1])
        seen.add((bot.strategy.period, bot.strategy.mult, bot.strategy.rsi_low))
    assert bot.bars_since_reopt < 100  # se ha reoptimizado al menos una vez
    assert isinstance(bot.strategy, MeanReversion)


def test_bot_ignores_repeated_candle():
    candles = synthetic(300)
    broker = PaperBroker(100.0)
    bot = Bot(MeanReversion(), broker, RiskConfig(), fetch=lambda: [], poll_seconds=0)
    bot.step(candles)
    before = len(broker.log)
    bot.step(candles)
    assert len(broker.log) == before
