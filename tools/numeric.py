from __future__ import annotations

"""Numeric evaluation utilities."""

from typing import Dict, Optional

from sympy import N, SympifyError, sympify


def _normalize(expr: str) -> str:
    return expr.replace("^", "**")


def evaluate(expr: str, subs: Optional[dict] = None) -> Dict[str, object]:
    """
    Evaluate numerically with sympy.N. If subs provided, substitute first.
    Return: status, float_value (Python float), precision_note.
    """
    try:
        parsed = sympify(_normalize(expr))
        if subs:
            # Convert keys to strings/symbols safely
            safe_subs = {}
            for k, v in subs.items():
                safe_subs[sympify(str(k))] = sympify(v)
            parsed = parsed.subs(safe_subs)
        numeric = N(parsed)
        return {"status": "ok", "float_value": float(numeric), "precision_note": "evalf"}
    except (SympifyError, Exception) as exc:  # noqa: BLE001
        return {"status": "error", "message": str(exc)}


