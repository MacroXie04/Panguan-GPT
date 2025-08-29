from __future__ import annotations

"""LaTeX rendering helpers."""

from typing import Dict, List, Union

from sympy import SympifyError, sympify
from sympy.printing.latex import latex as sympy_latex


def pretty(expr_or_steps: Union[str, List[str]]) -> Dict[str, object]:
    """
    If list, join steps into a LaTeX aligned environment; else latex(expr).
    Return: status, latex_block.
    """
    try:
        if isinstance(expr_or_steps, list):
            # Assume each step is a line of LaTeX content already
            lines = [str(s) for s in expr_or_steps]
            block = "\\begin{aligned}\n" + " \\\n".join(lines) + "\n\\end{aligned}"
            return {"status": "ok", "latex_block": block}
        # Single expression: attempt to sympify and latex it
        parsed = sympify(str(expr_or_steps))
        return {"status": "ok", "latex_block": sympy_latex(parsed)}
    except (SympifyError, Exception) as exc:  # noqa: BLE001
        # If it is a raw string that cannot be parsed, fall back to raw
        try:
            return {"status": "ok", "latex_block": str(expr_or_steps)}
        except Exception:  # noqa: BLE001
            return {"status": "error", "message": str(exc)}


