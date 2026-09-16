import json

import pytest

from tradingbot.backtest import Backtester
from tradingbot.data import synthetic
from tradingbot.montecarlo import shuffle_trades
from tradingbot.rules import RuleStrategy, load_rules, validate
from tradingbot.walkforward import best_params, walk_forward


def test_load_and_run_examples():
    c = synthetic(1200)
    for name in ("rsi_pullback", "cruce_emas", "bollinger_rebote"):
        cls = load_rules(f"strategies/{name}.json")
        assert issubclass(cls, RuleStrategy)
        sig = cls().signals(c)
        assert len(sig) == len(c) and set(sig) <= {-1, 0, 1}
        assert any(s != 0 for s in sig), f"{name} no genera señales"


def test_param_override_and_grid():
    cls = load_rules("strategies/rsi_pullback.json")
    s = cls(rsi14__period=21)
    assert s.spec["indicators"]["rsi14"]["period"] == 21
    assert cls.spec["indicators"]["rsi14"]["period"] == 14  # la clase no se modifica
    assert "rsi14__period" in cls.param_grid()
    with pytest.raises(KeyError):
        cls(noexiste__period=3)


def test_crosses():
    spec = {
        "name": "x",
        "indicators": {"f": {"type": "ema", "period": 3}, "s": {"type": "ema", "period": 10}},
        "long_entry": [["f", "crosses_above", "s"]],
        "long_exit": [["f", "crosses_below", "s"]],
    }
    cls = type("R", (RuleStrategy,), {"spec": spec})
    c = synthetic(500, seed=1)
    sig = cls().signals(c)
    assert 1 in sig and -1 not in sig


def test_validate_rejects_bad_specs():
    with pytest.raises(ValueError):
        validate({"indicators": {}})
    with pytest.raises(ValueError):
        validate({"long_entry": [["rsi9", "<", 30]], "indicators": {}})
    with pytest.raises(ValueError):
        validate({"long_entry": [["close", "??", 30]], "indicators": {}})


def test_walkforward_and_best_params_on_rules():
    cls = load_rules("strategies/bollinger_rebote.json")
    c = synthetic(1500)
    bp = best_params(cls, c[:800], initial_equity=100)
    assert set(bp) == {"bb__period", "bb__mult"}
    folds = walk_forward(cls, c, 800, 300, initial_equity=100)
    assert len(folds) == 2


def test_montecarlo_percentiles_ordered():
    c = synthetic(2000)
    res = Backtester(load_rules("strategies/bollinger_rebote.json")(), initial_equity=100).run(c)
    mc = shuffle_trades(res.trades, 100, 0.2, runs=300)
    assert mc.final_p5 <= mc.final_p50 <= mc.final_p95
    assert 0 <= mc.drawdown_p50 <= mc.drawdown_p95 <= 1
    assert 0 <= mc.prob_hit_max_drawdown <= 1
