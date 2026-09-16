"""CLI: python -m tradingbot <comando>."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from . import data as D
from .backtest import Backtester
from .bot import Bot
from .broker import PaperBroker
from .goal import analyze
from .risk import RiskConfig
from .strategies import REGISTRY, make
from .walkforward import summarize, walk_forward


def _load_candles(args) -> list:
    if args.csv:
        return D.load_csv(args.csv)
    if args.exchange:
        return D.fetch_ccxt(args.exchange, args.symbol, args.timeframe, args.limit)
    return D.synthetic(n=args.limit)


def _risk(args) -> RiskConfig:
    if args.config:
        cfg = json.loads(Path(args.config).read_text()).get("risk", {})
        return RiskConfig(**cfg)
    return RiskConfig()


def cmd_backtest(args) -> int:
    candles = _load_candles(args)
    bt = Backtester(make(args.strategy), _risk(args), args.fee, args.slippage, args.equity)
    res = bt.run(candles)
    print(json.dumps(res.metrics.as_dict(), indent=2))
    reasons = {}
    for t in res.trades:
        reasons[t.reason] = reasons.get(t.reason, 0) + 1
    print("Cierres por motivo:", reasons)
    return 0


def cmd_walkforward(args) -> int:
    candles = _load_candles(args)
    folds = walk_forward(REGISTRY[args.strategy], candles, args.train, args.test, _risk(args), args.fee, args.slippage, args.equity)
    for f in folds:
        print(f"fold {f.train_start}-{f.train_end}-{f.test_end} params={f.best_params} "
              f"train_ret={f.train.total_return:+.3f} TEST_ret={f.test.total_return:+.3f} "
              f"test_wr={f.test.win_rate:.2f} test_dd={f.test.max_drawdown:.3f} trades={f.test.trades}")
    print(json.dumps(summarize(folds), indent=2))
    return 0


def cmd_goal(args) -> int:
    print(analyze(args.start, args.target, args.days).render())
    return 0


def cmd_paper(args) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if not args.exchange:
        print("paper necesita --exchange y --symbol para datos en vivo (pip install ccxt)", file=sys.stderr)
        return 2
    broker = PaperBroker(args.equity, args.fee, args.slippage, Path(args.state))
    bot = Bot(
        make(args.strategy),
        broker,
        _risk(args),
        fetch=lambda: D.fetch_ccxt(args.exchange, args.symbol, args.timeframe, args.limit),
        poll_seconds=args.poll,
    )
    bot.run_forever()
    return 0


def cmd_download(args) -> int:
    candles = D.fetch_ccxt(args.exchange, args.symbol, args.timeframe, args.limit)
    D.save_csv(args.out, candles)
    print(f"{len(candles)} velas guardadas en {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tradingbot", description="Bot de trading con backtest, walk-forward y paper trading")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp):
        sp.add_argument("--strategy", default="regime", choices=list(REGISTRY))
        sp.add_argument("--csv", help="CSV ts,open,high,low,close,volume")
        sp.add_argument("--exchange", help="id de ccxt, p. ej. binance, kraken")
        sp.add_argument("--symbol", default="BTC/USDT")
        sp.add_argument("--timeframe", default="1h")
        sp.add_argument("--limit", type=int, default=2000)
        sp.add_argument("--equity", type=float, default=100.0)
        sp.add_argument("--fee", type=float, default=0.001)
        sp.add_argument("--slippage", type=float, default=0.0005)
        sp.add_argument("--config", help="JSON con sección 'risk'")

    s = sub.add_parser("backtest", help="backtest sobre CSV, exchange o datos sintéticos")
    common(s); s.set_defaults(fn=cmd_backtest)

    s = sub.add_parser("walkforward", help="optimiza en ventana y valida fuera de muestra")
    common(s)
    s.add_argument("--train", type=int, default=600)
    s.add_argument("--test", type=int, default=200)
    s.set_defaults(fn=cmd_walkforward)

    s = sub.add_parser("goal", help="qué hace falta para pasar de A a B en N días")
    s.add_argument("--start", type=float, default=100.0)
    s.add_argument("--target", type=float, default=10000.0)
    s.add_argument("--days", type=int, default=30)
    s.set_defaults(fn=cmd_goal)

    s = sub.add_parser("paper", help="paper trading en vivo con datos reales, dinero simulado")
    common(s)
    s.add_argument("--poll", type=int, default=60)
    s.add_argument("--state", default="paper_state.json")
    s.set_defaults(fn=cmd_paper)

    s = sub.add_parser("download", help="descarga velas a CSV")
    s.add_argument("--exchange", required=True)
    s.add_argument("--symbol", default="BTC/USDT")
    s.add_argument("--timeframe", default="1h")
    s.add_argument("--limit", type=int, default=1000)
    s.add_argument("--out", default="data/candles.csv")
    s.set_defaults(fn=cmd_download)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
