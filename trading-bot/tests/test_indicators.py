from tradingbot.indicators import atr, bollinger, ema, rsi, sma
from tradingbot.data import synthetic


def test_sma_basic():
    assert sma([1, 2, 3, 4, 5], 3) == [None, None, 2.0, 3.0, 4.0]


def test_ema_seed_equals_sma():
    v = [1, 2, 3, 4, 5, 6]
    e = ema(v, 3)
    assert e[:2] == [None, None]
    assert abs(e[2] - 2.0) < 1e-9
    assert e[-1] is not None and e[-1] > e[2]


def test_rsi_bounds_and_monotone_series():
    up = list(range(1, 40))
    r = rsi(up, 14)
    assert r[13] is None and r[14] == 100.0
    down = list(range(40, 1, -1))
    assert rsi(down, 14)[-1] == 0.0


def test_atr_positive():
    c = synthetic(100)
    a = atr(c, 14)
    assert a[13] is None and a[14] is not None and all(x > 0 for x in a[14:])


def test_bollinger_order():
    v = [float(i % 7) for i in range(50)]
    mid, up, lo = bollinger(v, 20)
    for i in range(19, 50):
        assert lo[i] <= mid[i] <= up[i]
