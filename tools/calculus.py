from __future__ import annotations

"""
Calculus utilities implemented with SymPy.
"""

from typing import Dict, Optional, Tuple

from sympy import Integral, Symbol, SympifyError, diff, sympify
from sympy import integrate as sympy_integrate
from sympy.printing.latex import latex as sympy_latex


def _normalize(expr: str) -> str:
    return expr.replace("^", "**")


def differentiate(expr: str, var: str) -> Dict[str, object]:
    """Return derivative wrt `var` with keys: status, latex, derivative_str."""
    try:
        parsed = sympify(_normalize(expr))
        symbol = Symbol(var)
        deriv = diff(parsed, symbol)
        return {"status": "ok", "latex": sympy_latex(deriv), "derivative_str": str(deriv)}
    except (SympifyError, Exception) as exc:  # noqa: BLE001
        return {"status": "error", "message": str(exc)}


def integrate(
    expr: str,
    var: str,
    limits: Optional[Tuple[object, object, object]] = None,
) -> Dict[str, object]:
    """
    If limits is provided like ("x", 0, 1) or (var, a, b), perform definite integral,
    else indefinite. Return: status, latex, result_str, constant_note ("+C" or "").
    """
    try:
        parsed = sympify(_normalize(expr))
        symbol = Symbol(var)
        constant_note = ""
        if limits is not None:
            lim_var, a, b = limits
            lim_symbol = Symbol(str(lim_var))
            result = sympy_integrate(parsed, (lim_symbol, sympify(a), sympify(b)))
        else:
            result = sympy_integrate(parsed, symbol)
            constant_note = "+C"
        return {
            "status": "ok",
            "latex": sympy_latex(result),
            "result_str": str(result),
            "constant_note": constant_note,
        }
    except (SympifyError, Exception) as exc:  # noqa: BLE001
        return {"status": "error", "message": str(exc)}


