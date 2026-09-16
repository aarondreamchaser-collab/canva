"""Calculadora de objetivo: qué hace falta, en números, para pasar de A a B en N días."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass


@dataclass
class GoalReport:
    start: float
    target: float
    days: int
    multiple: float
    daily_return_needed: float
    monthly_return_needed: float
    annualized: float
    prob_success: float
    prob_ruin: float
    median_final: float

    def render(self) -> str:
        lines = [
            f"Objetivo: {self.start:.2f} -> {self.target:.2f} en {self.days} días (x{self.multiple:.0f})",
            f"  Rendimiento diario necesario, compuesto: {self.daily_return_needed*100:.2f} % CADA día",
            f"  Rendimiento mensual necesario:          {self.monthly_return_needed*100:,.0f} %",
            f"  Equivalente anualizado:                 {self.annualized:.2e} % (no es una errata)",
            "",
            "Simulación Monte Carlo con una estrategia MUY buena (más optimista que la realidad):",
            "(55 % de aciertos, ratio 1.5:1, 5 operaciones/día, riesgo 2 % por operación, sin rachas)",
            f"  Probabilidad de alcanzar el objetivo: {self.prob_success*100:.2f} %",
            f"  Probabilidad de perder más de la mitad: {self.prob_ruin*100:.1f} %",
            f"  Resultado MEDIANO tras {self.days} días:       {self.median_final:.2f} (desde {self.start:.2f})",
            "",
            "Referencias: los mejores fondos cuantitativos del mundo rondan el 30-70 % ANUAL.",
            "Nadie sostiene un 16 % diario. Quien lo prometa te está vendiendo algo.",
        ]
        return "\n".join(lines)


def monte_carlo(
    start: float,
    target: float,
    days: int,
    win_rate: float = 0.55,
    reward_risk: float = 1.5,
    trades_per_day: int = 5,
    risk_per_trade: float = 0.02,
    fee: float = 0.001,
    runs: int = 5000,
    seed: int = 7,
) -> tuple[float, float, float]:
    rng = random.Random(seed)
    success = ruin = 0
    finals = []
    n = days * trades_per_day
    for _ in range(runs):
        eq = start
        hit = False
        for _ in range(n):
            r = risk_per_trade * eq
            eq += (r * reward_risk if rng.random() < win_rate else -r) - 2 * fee * eq
            if eq >= target:
                hit = True
                break
            if eq <= 0:
                break
        success += hit
        ruin += eq < start * 0.5
        finals.append(eq)
    finals.sort()
    return success / runs, ruin / runs, finals[len(finals) // 2]


def analyze(start: float, target: float, days: int) -> GoalReport:
    if start <= 0 or target <= 0 or days <= 0:
        raise ValueError("start, target y days deben ser positivos")
    mult = target / start
    daily = mult ** (1 / days) - 1
    monthly = (1 + daily) ** 30 - 1
    annual = ((1 + daily) ** 365 - 1) * 100
    ps, pr, med = monte_carlo(start, target, days)
    return GoalReport(start, target, days, mult, daily, monthly, annual, ps, pr, med)
