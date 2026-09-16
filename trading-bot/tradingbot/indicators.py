"""Indicadores técnicos en Python puro. Devuelven listas alineadas con la entrada (None hasta tener datos)."""
from __future__ import annotations

from typing import List, Optional, Sequence

from .data import Candle

Series = List[Optional[float]]


def sma(values: Sequence[float], period: int) -> Series:
    out: Series = [None] * len(values)
    if period <= 0:
        raise ValueError("period debe ser > 0")
    acc = 0.0
    for i, v in enumerate(values):
        acc += v
        if i >= period:
            acc -= values[i - period]
        if i >= period - 1:
            out[i] = acc / period
    return out


def ema(values: Sequence[float], period: int) -> Series:
    out: Series = [None] * len(values)
    if period <= 0:
        raise ValueError("period debe ser > 0")
    k = 2.0 / (period + 1)
    prev: Optional[float] = None
    for i, v in enumerate(values):
        if prev is None:
            if i == period - 1:
                prev = sum(values[:period]) / period
                out[i] = prev
            continue
        prev = v * k + prev * (1 - k)
        out[i] = prev
    return out


def rsi(values: Sequence[float], period: int = 14) -> Series:
    out: Series = [None] * len(values)
    if len(values) <= period:
        return out
    gains = losses = 0.0
    for i in range(1, period + 1):
        d = values[i] - values[i - 1]
        gains += max(d, 0)
        losses += max(-d, 0)
    avg_g, avg_l = gains / period, losses / period
    out[period] = 100.0 if avg_l == 0 else 100 - 100 / (1 + avg_g / avg_l)
    for i in range(period + 1, len(values)):
        d = values[i] - values[i - 1]
        avg_g = (avg_g * (period - 1) + max(d, 0)) / period
        avg_l = (avg_l * (period - 1) + max(-d, 0)) / period
        out[i] = 100.0 if avg_l == 0 else 100 - 100 / (1 + avg_g / avg_l)
    return out


def atr(candles: Sequence[Candle], period: int = 14) -> Series:
    """Average True Range (Wilder)."""
    out: Series = [None] * len(candles)
    if len(candles) <= period:
        return out
    trs: List[float] = []
    for i, c in enumerate(candles):
        if i == 0:
            trs.append(c.high - c.low)
        else:
            pc = candles[i - 1].close
            trs.append(max(c.high - c.low, abs(c.high - pc), abs(c.low - pc)))
    val = sum(trs[1 : period + 1]) / period
    out[period] = val
    for i in range(period + 1, len(candles)):
        val = (val * (period - 1) + trs[i]) / period
        out[i] = val
    return out


def bollinger(values: Sequence[float], period: int = 20, mult: float = 2.0):
    """Devuelve (media, banda_superior, banda_inferior)."""
    mid = sma(values, period)
    up: Series = [None] * len(values)
    lo: Series = [None] * len(values)
    for i in range(period - 1, len(values)):
        window = values[i - period + 1 : i + 1]
        m = mid[i]
        assert m is not None
        var = sum((x - m) ** 2 for x in window) / period
        sd = var ** 0.5
        up[i] = m + mult * sd
        lo[i] = m - mult * sd
    return mid, up, lo


def closes(candles: Sequence[Candle]) -> List[float]:
    return [c.close for c in candles]
