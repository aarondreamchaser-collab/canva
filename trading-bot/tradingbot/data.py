"""Carga y generación de velas OHLCV."""
from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class Candle:
    ts: int        # timestamp en milisegundos
    open: float
    high: float
    low: float
    close: float
    volume: float


def load_csv(path: str | Path) -> List[Candle]:
    """Lee un CSV con cabecera: ts,open,high,low,close,volume."""
    out: List[Candle] = []
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            out.append(
                Candle(
                    ts=int(float(row["ts"])),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row.get("volume", 0) or 0),
                )
            )
    out.sort(key=lambda c: c.ts)
    return out


def save_csv(path: str | Path, candles: Iterable[Candle]) -> None:
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["ts", "open", "high", "low", "close", "volume"])
        for c in candles:
            w.writerow([c.ts, c.open, c.high, c.low, c.close, c.volume])


def synthetic(
    n: int = 2000,
    start_price: float = 100.0,
    seed: Optional[int] = 42,
    drift: float = 0.0002,
    vol: float = 0.01,
    regime_switch_every: int = 400,
    step_ms: int = 3_600_000,
) -> List[Candle]:
    """Serie sintética con regímenes alternos (tendencia / rango).

    Sirve para probar la maquinaria, NO para estimar rentabilidad real.
    """
    rng = random.Random(seed)
    price = start_price
    ts = 1_600_000_000_000
    out: List[Candle] = []
    trending = True
    for i in range(n):
        if i % regime_switch_every == 0:
            trending = not trending
        d = drift if trending else 0.0
        v = vol if trending else vol * 0.6
        r = rng.gauss(d, v)
        if not trending:
            # reversión a la media suave dentro del régimen de rango
            r -= 0.05 * math.log(price / start_price) if price > 0 else 0
        o = price
        c = price * math.exp(r)
        hi = max(o, c) * (1 + abs(rng.gauss(0, v / 3)))
        lo = min(o, c) * (1 - abs(rng.gauss(0, v / 3)))
        out.append(Candle(ts, o, hi, lo, c, abs(rng.gauss(1000, 300))))
        price = c
        ts += step_ms
    return out


def fetch_ccxt(
    exchange_id: str,
    symbol: str,
    timeframe: str = "1h",
    limit: int = 1000,
    since: Optional[int] = None,
) -> List[Candle]:
    """Descarga velas reales vía ccxt (pip install ccxt). Solo lectura, sin API key."""
    try:
        import ccxt  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Instala ccxt para descargar datos: pip install ccxt") from exc
    ex = getattr(ccxt, exchange_id)({"enableRateLimit": True})
    raw = ex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
    return [Candle(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5] or 0)) for r in raw]
