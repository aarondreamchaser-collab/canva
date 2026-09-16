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
from .montecarlo import shuffle_trades
from .risk import RiskConfig
from .rules import load_rules
from .strategies import REGISTRY, make
from .walkforward import summarize, walk_forward


def _load_candles(args) -> list:
    if args.csv:
        return D.load_csv(args.csv)
    if args.exchange:
        return D.fetch_ccxt(args.exchange, args.symbol, args.timeframe, args.limit)
    return D.synthetic(n=args.limit)


def _strategy_cls(args):
    return load_rules(args.rules) if getattr(args, "rules", None) else REGISTRY[args.strategy]


def _risk(args) -> RiskConfig:
    if args.config:
        cfg = json.loads(Path(args.config).read_text()).get("risk", {})
        return RiskConfig(**cfg)
    return RiskConfig()


def cmd_backtest(args) -> int:
    candles = _load_candles(args)
    risk = _risk(args)
    bt = Backtester(_strategy_cls(args)(), risk, args.fee, args.slippage, args.equity)
    res = bt.run(candles)
    print(json.dumps(res.metrics.as_dict(), indent=2))
    reasons = {}
    for t in res.trades:
        reasons[t.reason] = reasons.get(t.reason, 0) + 1
    print("Cierres por motivo:", reasons)
    if args.montecarlo:
        mc = shuffle_trades(res.trades, args.equity, risk.max_drawdown)
        print("Monte Carlo (mismas operaciones, otro orden):")
        print(json.dumps(mc.as_dict(), indent=2))
    return 0


def cmd_walkforward(args) -> int:
    candles = _load_candles(args)
    folds = walk_forward(_strategy_cls(args), candles, args.train, args.test, _risk(args), args.fee, args.slippage, args.equity)
    for f in folds:
        print(f"fold {f.train_start}-{f.train_end}-{f.test_end} params={f.best_params} "
              f"train_ret={f.train.total_return:+.3f} TEST_ret={f.test.total_return:+.3f} "
              f"test_wr={f.test.win_rate:.2f} test_dd={f.test.max_drawdown:.3f} trades={f.test.trades}")
    print(json.dumps(summarize(folds), indent=2))
    return 0


def cmd_goal(args) -> int:
    print(analyze(args.start, args.target, args.days).render())
    return 0


def cmd_verify(args) -> int:
    """Veredicto completo sobre una estrategia: backtest + walk-forward + Monte Carlo."""
    candles = _load_candles(args)
    risk = _risk(args)
    cls = _strategy_cls(args)
    res = Backtester(cls(), risk, args.fee, args.slippage, args.equity).run(candles)
    m = res.metrics
    mc = shuffle_trades(res.trades, args.equity, risk.max_drawdown)
    folds = walk_forward(cls, candles, args.train, args.test, risk, args.fee, args.slippage, args.equity)
    wf = summarize(folds)

    checks = [
        ("Suficientes operaciones (>= 30)", m.trades >= 30, f"{m.trades}"),
        ("Profit factor > 1.2 tras comisiones", m.profit_factor > 1.2, f"{m.profit_factor:.2f}"),
        ("Expectancy positiva", m.expectancy > 0, f"{m.expectancy:.4f}"),
        ("Drawdown máximo < límite del kill switch", m.max_drawdown < risk.max_drawdown, f"{m.max_drawdown:.1%}"),
        ("Monte Carlo: p95 de drawdown < kill switch", mc.drawdown_p95 < risk.max_drawdown, f"{mc.drawdown_p95:.1%}"),
        ("Monte Carlo: p5 de equity final >= inicial", mc.final_p5 >= args.equity, f"{mc.final_p5:.2f}"),
        ("Walk-forward: mayoría de ventanas positivas", bool(wf) and wf["oos_folds_positive"] * 2 > wf["folds"], f"{wf.get('oos_folds_positive', 0)}/{wf.get('folds', 0)}"),
        ("Walk-forward: retorno fuera de muestra > 0", bool(wf) and wf["oos_return_compounded"] > 0, f"{wf.get('oos_return_compounded', 0):+.2%}"),
    ]
    print(f"\nVERIFICACIÓN de '{cls().name}' sobre {len(candles)} velas\n")
    passed = 0
    for label, ok, val in checks:
        passed += ok
        print(f"  [{'OK ' if ok else 'NO '}] {label:<48} {val}")
    print(f"\n  {passed}/{len(checks)} criterios superados.")
    if passed == len(checks):
        print("  Veredicto: candidata a paper trading. No es garantía de nada; es el mínimo exigible.")
    elif passed >= len(checks) - 2:
        print("  Veredicto: prometedora pero frágil. Revisa lo que falla antes de seguir.")
    else:
        print("  Veredicto: descártala o replantéala. Con dinero real perderías.")
    print(
        "\nBacktest:", json.dumps(m.as_dict()),
        "\nMonte Carlo:", json.dumps(mc.as_dict()),
        "\nWalk-forward:", json.dumps(wf),
    )
    return 0 if passed == len(checks) else 1


def cmd_check(args) -> int:
    """Comprueba conexión, saldo y mínimos de orden con claves de solo lectura. No opera."""
    import os

    try:
        import ccxt  # type: ignore
    except ImportError:
        print("pip install ccxt", file=sys.stderr)
        return 2
    key, secret = os.environ.get("TRADINGBOT_API_KEY"), os.environ.get("TRADINGBOT_API_SECRET")
    if not key or not secret:
        print("Exporta TRADINGBOT_API_KEY y TRADINGBOT_API_SECRET (clave SIN permiso de retirada)", file=sys.stderr)
        return 2
    ex = getattr(ccxt, args.exchange)({"apiKey": key, "secret": secret, "enableRateLimit": True})
    ex.load_markets()
    if args.symbol not in ex.markets:
        print(f"{args.symbol} no existe en {args.exchange}. Ejemplos: {list(ex.markets)[:5]}")
        return 1
    mk = ex.markets[args.symbol]
    limits = mk.get("limits", {}) or {}
    bal = ex.fetch_balance()
    quote = args.symbol.split("/")[1]
    free = float((bal.get("free") or {}).get(quote) or 0)
    price = float(ex.fetch_ticker(args.symbol)["last"])
    min_amt = (limits.get("amount") or {}).get("min") or 0
    min_cost = (limits.get("cost") or {}).get("min") or 0
    print(f"Exchange: {args.exchange} | Par: {args.symbol} | Precio: {price}")
    print(f"Saldo disponible en {quote}: {free:.2f}")
    print(f"Orden mínima: {min_amt} {mk['base']} / {min_cost} {quote} (~{max(min_amt * price, min_cost or 0):.2f} {quote})")
    rc = RiskConfig()
    typical = free * rc.risk_per_trade / (rc.stop_atr_mult * 0.01)  # ATR ~1 % del precio como aproximación
    print(f"Tamaño típico de posición con riesgo {rc.risk_per_trade:.0%} y ATR ~1 %: ~{typical:.2f} {quote}")
    if typical < max(min_amt * price, min_cost or 0):
        print("AVISO: tus posiciones quedarían por debajo del mínimo del exchange. Sube capital o riesgo por operación.")
    return 0


def cmd_paper(args) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if not args.exchange:
        print("paper necesita --exchange y --symbol para datos en vivo (pip install ccxt)", file=sys.stderr)
        return 2
    broker = PaperBroker(args.equity, args.fee, args.slippage, Path(args.state))
    bot = Bot(
        _strategy_cls(args)(),
        broker,
        _risk(args),
        fetch=lambda: D.fetch_ccxt(args.exchange, args.symbol, args.timeframe, args.limit),
        poll_seconds=args.poll,
        reoptimize_every=args.reoptimize_every,
        fee=args.fee,
        slippage=args.slippage,
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
        sp.add_argument("--rules", help="JSON de reglas (ver strategies/*.json); sustituye a --strategy")
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
    common(s)
    s.add_argument("--montecarlo", action="store_true", help="baraja las operaciones para ver la dispersión")
    s.set_defaults(fn=cmd_backtest)

    s = sub.add_parser("walkforward", help="optimiza en ventana y valida fuera de muestra")
    common(s)
    s.add_argument("--train", type=int, default=600)
    s.add_argument("--test", type=int, default=200)
    s.set_defaults(fn=cmd_walkforward)

    s = sub.add_parser("verify", help="veredicto completo: backtest + Monte Carlo + walk-forward")
    common(s)
    s.add_argument("--train", type=int, default=600)
    s.add_argument("--test", type=int, default=200)
    s.set_defaults(fn=cmd_verify)

    s = sub.add_parser("check", help="comprueba conexión, saldo y mínimos del exchange (solo lectura)")
    s.add_argument("--exchange", required=True)
    s.add_argument("--symbol", default="BTC/USD")
    s.set_defaults(fn=cmd_check)

    s = sub.add_parser("goal", help="qué hace falta para pasar de A a B en N días")
    s.add_argument("--start", type=float, default=100.0)
    s.add_argument("--target", type=float, default=10000.0)
    s.add_argument("--days", type=int, default=30)
    s.set_defaults(fn=cmd_goal)

    s = sub.add_parser("paper", help="paper trading en vivo con datos reales, dinero simulado")
    common(s)
    s.add_argument("--poll", type=int, default=60)
    s.add_argument("--state", default="paper_state.json")
    s.add_argument("--reoptimize-every", type=int, default=0, help="velas entre reoptimizaciones (p. ej. 168 = semanal en 1h)")
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
