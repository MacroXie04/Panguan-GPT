from __future__ import annotations

"""Equation solving utilities."""

from typing import Dict, List

from sympy import Symbol, SympifyError, solve, sympify
from sympy.printing.latex import latex as sympy_latex


def _normalize(expr: str) -> str:
    return expr.replace("^", "**")


def solve_equation(expr: str, var: str) -> Dict[str, object]:
    """Solve expr == 0 for `var`. Return: status, solutions_latex, solutions (JSON-serializable list)."""
    try:
        parsed = sympify(_normalize(expr))
        symbol = Symbol(var)
        sols: List[object] = solve(parsed, symbol)
        sols_latex = [sympy_latex(s) for s in sols]
        return {
            "status": "ok",
            "solutions_latex": sols_latex,
            "solutions": [str(s) for s in sols],
        }
    except (SympifyError, Exception) as exc:  # noqa: BLE001
        return {"status": "error", "message": str(exc)}


