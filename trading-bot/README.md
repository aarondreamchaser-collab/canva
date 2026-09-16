# Trading Bot

Bot de trading modular en Python puro (sin dependencias para el núcleo), con
backtest realista, validación walk-forward, gestión de riesgo estricta y paper
trading. El modo con dinero real existe, pero está bloqueado por defecto.

## Antes de nada: la verdad sobre el "99 %" y el "100 € → 10.000 € en 30 días"

Este bot se pidió con dos objetivos. Ninguno es alcanzable y es importante que
lo sepas antes de arriesgar un euro:

| Objetivo pedido | Lo que exige en números | Realidad |
|---|---|---|
| 99 % de efectividad | 99 de cada 100 operaciones ganadoras | Los mejores sistemas del mundo rondan el 40-65 %. Un 99 % solo aparece en sistemas que ganan céntimos y pierden todo en la operación 100 (martingala, grid sin stop, venta de opciones sin cobertura). |
| 100 € → 10.000 € en 30 días | x100, es decir **16,6 % diario compuesto** durante 30 días seguidos | Los fondos cuantitativos más rentables hacen 30-70 % **al año**. Anualizado, tu objetivo es un 2·10²⁶ %. |

Compruébalo tú mismo con la calculadora incluida:

```bash
python -m tradingbot goal --start 100 --target 10000 --days 30
```

Salida:

```
Rendimiento diario necesario, compuesto: 16.59 % CADA día
Rendimiento mensual necesario:          9,900 %
Probabilidad de alcanzar el objetivo (estrategia muy buena, Monte Carlo): 0.00 %
Resultado MEDIANO tras 30 días con esa estrategia muy buena: ~212 €
```

Además, la **tasa de aciertos no mide la efectividad**. Un bot con 30 % de
aciertos que gana 3 € por cada 1 € que pierde es rentable. Uno con 95 % de
aciertos que pierde 30 € cada vez que falla te arruina. Lo que importa es:

- **Expectancy**: ganancia media por operación después de comisiones.
- **Profit factor**: ganancias brutas / pérdidas brutas (> 1.3 empieza a ser interesante).
- **Drawdown máximo**: la peor caída desde un máximo. Es lo que te hace abandonar.
- **Resultado fuera de muestra**: lo que hace la estrategia en datos que no vio al optimizarse.

Quien te prometa 99 % o x100 en un mes te está vendiendo un curso, una señal o
una estafa. Este bot está diseñado para que **no te engañes a ti mismo**.

## Qué hace de verdad este bot

```
datos (CSV / exchange / sintéticos)
   → indicadores (SMA, EMA, RSI, ATR, Bollinger)
   → estrategia (tendencia, reversión a la media, o cambio de régimen)
   → gestión de riesgo (tamaño por ATR, stop, take-profit, límite diario, kill switch)
   → broker (paper por defecto; live solo con confirmación explícita)
```

- **Backtest honesto**: comisiones por lado, slippage siempre en contra, stops
  evaluados dentro de la vela (si toca stop y take-profit en la misma vela, se
  asume el stop), ejecución al cierre sin mirar el futuro.
- **Walk-forward**: optimiza parámetros en una ventana y los valida en la
  siguiente, ventana a ventana. Si el resultado fuera de muestra es malo, la
  estrategia no sirve, por muy bonito que quede el backtest completo.
- **Riesgo**: nunca más del 1 % del capital por operación (configurable, máximo
  10 %), stop a 2 ATR, pérdida diaria máxima 5 % (pausa hasta el día siguiente),
  drawdown máximo 20 % (parada definitiva).
- **Paper trading**: datos reales del exchange, dinero simulado, estado
  persistente en JSON para sobrevivir reinicios.
- **Live**: bloqueado hasta exportar `TRADINGBOT_LIVE=I_UNDERSTAND_THE_RISK`.
  Solo largos en spot. Sin apalancamiento por defecto.

## Instalación

```bash
cd trading-bot
python -m pip install -e ".[dev]"     # tests
python -m pip install ccxt            # solo para datos reales / paper / live
python -m pytest                       # 25 tests
```

Requiere Python 3.10 o superior.

## Uso

```bash
# 1. Descarga velas reales (sin API key, solo lectura)
python -m tradingbot download --exchange kraken --symbol BTC/USD --timeframe 1h --limit 2000 --out data/btc.csv

# 2. Backtest de cada estrategia con tus 100 €
python -m tradingbot backtest --csv data/btc.csv --strategy trend   --equity 100
python -m tradingbot backtest --csv data/btc.csv --strategy meanrev --equity 100
python -m tradingbot backtest --csv data/btc.csv --strategy regime  --equity 100

# 3. Validación walk-forward (la prueba que de verdad importa)
python -m tradingbot walkforward --csv data/btc.csv --strategy meanrev --train 800 --test 200

# 4. Paper trading en vivo (Ctrl+C para parar; el estado se guarda en paper_state.json)
python -m tradingbot paper --exchange kraken --symbol BTC/USD --timeframe 1h --equity 100 --poll 60

# Ajusta el riesgo copiando config.example.json y pasando --config mi_config.json
```

Sin `--csv` ni `--exchange`, los comandos usan datos sintéticos con regímenes
alternos. Sirven para comprobar que la maquinaria funciona, **no** para estimar
rentabilidad: en datos aleatorios con comisiones las tres estrategias pierden
dinero, como debe ser.

## Verificar una estrategia en un solo comando

```bash
python -m tradingbot verify --csv data/btc.csv --strategy meanrev --equity 100
python -m tradingbot verify --csv data/btc.csv --rules strategies/cruce_emas.json --equity 100
```

Ejecuta backtest, Monte Carlo (bootstrap de operaciones) y walk-forward, y
comprueba ocho criterios mínimos: operaciones suficientes, profit factor,
expectancy, drawdown, percentil 95 de drawdown, percentil 5 de resultado,
ventanas fuera de muestra positivas y retorno fuera de muestra. Termina con
código de salida 0 solo si supera todos. Superarlos no garantiza nada. No
superarlos sí garantiza que no debes ponerle dinero.

## Estrategias por reglas (sin programar)

Puedes describir una estrategia en JSON y el bot la ejecuta, la optimiza y la
verifica. Es la forma de probar ideas que veas en internet sin fiarte de lo
que prometen. Ejemplos en `strategies/`:

| Archivo | Idea |
|---|---|
| `rsi_pullback.json` | RSI bajo con precio sobre la SMA 100: compra el retroceso en tendencia |
| `cruce_emas.json` | Cruce EMA 9/21 filtrado por SMA 200 |
| `bollinger_rebote.json` | Compra bajo la banda inferior, vende en la media |

Formato:

```json
{
  "name": "mi_idea",
  "indicators": {
    "rsi14": {"type": "rsi", "period": 14},
    "sma50": {"type": "sma", "period": 50},
    "bb":    {"type": "bbands", "period": 20, "mult": 2.0}
  },
  "long_entry":  [["rsi14", "<", 30], ["close", ">", "sma50"]],
  "long_exit":   [["rsi14", ">", 55]],
  "short_entry": [["rsi14", ">", 70], ["close", "<", "sma50"]],
  "short_exit":  [["rsi14", "<", 45]],
  "grid": {"rsi14.period": [10, 14, 20], "sma50.period": [30, 50, 100]}
}
```

Indicadores: `sma`, `ema`, `rsi`, `atr`, `bbands` (genera `nombre_mid`,
`nombre_up`, `nombre_lo`). Operadores: `<`, `>`, `<=`, `>=`, `crosses_above`,
`crosses_below`. Operandos: nombre de indicador, `open`/`high`/`low`/`close` o
un número. Todas las condiciones de una lista deben cumplirse. `grid` define
qué parámetros puede ajustar el walk-forward y la reoptimización.

Cualquier comando acepta `--rules archivo.json` en lugar de `--strategy`.

## Reoptimización automática ("aprender" sin engañarse)

```bash
python -m tradingbot paper --exchange kraken --symbol BTC/USD --equity 100 --reoptimize-every 168
```

Cada 168 velas (una semana en velas de 1 hora) el bot vuelve a elegir los
parámetros de la estrategia con las últimas 600 velas, usando la misma
puntuación robusta que el walk-forward (retorno penalizado por drawdown, mínimo
10 operaciones). Solo cambia parámetros, nunca la lógica, y solo con la
posición cerrada. Es la única forma de adaptación que no se convierte en
sobreajuste diario. Con 100 € y 20-40 operaciones al mes no hay datos para
nada más sofisticado: un modelo que "aprende" de 30 operaciones memoriza ruido.

## Antes de pasar a dinero real

```bash
export TRADINGBOT_API_KEY=...      # clave SIN permiso de retirada
export TRADINGBOT_API_SECRET=...
python -m tradingbot check --exchange kraken --symbol BTC/USD
```

Comprueba conexión, saldo, tamaño mínimo de orden y si tus posiciones con el
riesgo configurado superan ese mínimo. Con 100 € es frecuente que no lo hagan.
El modo real ajusta cantidades a la precisión del exchange, descarta órdenes
por debajo del mínimo e ignora señales cortas en spot. En paper, cada operación
cerrada se añade a `trades.csv` junto al fichero de estado.

## Estrategias incluidas

| Nombre | Idea | Perfil |
|---|---|---|
| `trend` | Cruce EMA 12/26 filtrado por SMA 100 | Pocos aciertos (30-40 %), ganancias grandes. Sufre en rango. |
| `meanrev` | Bollinger 20/2σ + RSI 14, sale en la media | Muchos aciertos (55-70 %), pérdidas ocasionales grandes. Sufre en tendencia fuerte. |
| `regime` | Efficiency Ratio de Kaufman decide cuál de las dos usar | Intenta lo mejor de ambas. Más parámetros = más riesgo de sobreajuste. |

Para añadir una estrategia: hereda de `Strategy` en `tradingbot/strategies.py`,
implementa `signals()` (1 largo, -1 corto, 0 plano), define `param_grid()` para
el walk-forward y regístrala en `REGISTRY`.

## Cómo saber si una estrategia sirve

1. Backtest completo con comisiones reales de tu exchange (`--fee`, `--slippage`).
2. Walk-forward con al menos 5 ventanas. Mira `oos_folds_positive` y
   `oos_return_compounded`. Si menos de la mitad de las ventanas son positivas,
   descártala.
3. Paper trading un mínimo de 4-8 semanas. Compara con el backtest del mismo
   periodo. Si diverge mucho, hay un error de ejecución o de datos.
4. Solo entonces, live con una cantidad que puedas perder entera sin que te
   afecte, y con el kill switch activo.

## Camino realista con 100 €

Con 100 € y comisiones del 0,1 % por lado, cada operación completa te cuesta
unos 0,20 € más slippage. Con un riesgo del 1 % por operación arriesgas 1 €.
Las comisiones se comen una parte enorme de tu edge. Lo honesto es:

- Usar 100 € para **aprender a operar un sistema sin perderlo todo**, no para
  hacerse rico.
- Un objetivo defendible con una estrategia buena y validada es un 2-5 %
  mensual con drawdowns del 10-15 %. Es lo que hacen los que sobreviven.
- Si el paper trading confirma un edge durante meses, el capital se escala
  poco a poco. La ventaja de un sistema es que se puede repetir; la de una
  apuesta, no.

## Estructura

```
trading-bot/
  tradingbot/
    data.py          velas, CSV, sintéticos, ccxt
    indicators.py    SMA, EMA, RSI, ATR, Bollinger
    strategies.py    trend, meanrev, regime + REGISTRY
    risk.py          RiskConfig, RiskManager (tamaño, stops, límites)
    backtest.py      motor + métricas
    walkforward.py   optimización con validación fuera de muestra
    goal.py          calculadora de objetivo + Monte Carlo
    rules.py         estrategias declarativas en JSON
    montecarlo.py    bootstrap de operaciones (dispersión de drawdown y resultado)
    broker.py        PaperBroker (con journal CSV), LiveBroker (bloqueado, con límites)
    bot.py           bucle en vivo con reoptimización periódica
    cli.py           comandos: backtest, walkforward, verify, goal, paper, check, download
  strategies/        ejemplos de estrategias por reglas
  tests/             25 tests
  config.example.json
```

## Aviso

Esto es software educativo. Operar con criptomonedas o cualquier activo
apalancado puede hacerte perder todo el capital. Nada aquí es consejo
financiero. El autor del bot no garantiza rentabilidad alguna, y desconfía de
quien lo haga.
