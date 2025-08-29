from __future__ import annotations

"""
Algebraic utilities implemented with SymPy.

All functions are import-safe and contain robust exception handling.
"""

from typing import Dict

from sympy import SympifyError, simplify, sympify
from sympy.printing.latex import latex as sympy_latex


def _normalize(expr: str) -> str:
    """Normalize common user syntax to SymPy-friendly form."""
    # Caret is XOR in SymPy; convert to exponentiation.
    return expr.replace("^", "**")


def simplify_expr(expr: str) -> Dict[str, object]:
    """
    Parse `expr` via sympy.sympify, simplify with sympy.simplify, and return:
    { "status": "ok", "latex": "<latex of simplified>", "simplified_str": "<str(expr)>" }
    On SympifyError or any Exception, return { "status":"error", "message": str(e) }.
    """
    try:
        parsed = sympify(_normalize(expr))
        simplified = simplify(parsed)
        return {
            "status": "ok",
            "latex": sympy_latex(simplified),
            "simplified_str": str(simplified),
        }
    except (SympifyError, Exception) as exc:  # noqa: BLE001 - broad by design for tool safety
        return {"status": "error", "message": str(exc)}


