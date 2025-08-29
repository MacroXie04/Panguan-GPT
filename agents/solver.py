from __future__ import annotations

"""
MathSolverAgent: symbolic-first solver using tools and SymPy with safe fallbacks.

Input: natural language math problem
Output state key: "solver_output" (dict with derivation_steps, final_answer)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import re

from sympy import Eq, Symbol, oo, limit as sympy_limit
from sympy import sympify
from sympy import integrate as sympy_integrate
from sympy import solve as sympy_solve
from sympy.printing.latex import latex as sympy_latex

from tools.algebra import simplify_expr
from tools.calculus import differentiate, integrate
from tools.equation import solve_equation
from tools.numeric import evaluate
from tools.latex import pretty as latex_pretty


def _norm(s: str) -> str:
    return s.replace("^", "**")


@dataclass
class MathSolverAgent:
    """
    Lightweight, import-safe stand-in for an ADK LlmAgent configured to prefer
    tool calls (SymPy tools) and execute Python for numeric checks.

    When ADK is available, this agent can be adapted to inherit from
    google.adk.agents.LlmAgent and register tools. For tests and offline use,
    this class exposes a simple run(text: str, state: dict) method.
    """

    model: str = "gemini-2.0-flash"

    def run(self, text: str, state: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        state = {} if state is None else dict(state)
        derivation_steps: List[str] = []
        final_answer: str = ""

        # Heuristic routing
        routed = False
        t = text.strip()

        # 1) Definite integral like ∫_0^1 x^2 dx
        m = re.search(r"∫_\s*([^\{^\s]+)\^\s*([^\s]+)\s+([^d]+)d([a-zA-Z])", t)
        if m:
            a_str, b_str, f_str, var = m.groups()
            a = sympify(_norm(a_str))
            b = sympify(_norm(b_str))
            expr = _norm(f_str.strip())
            tool_res = integrate(expr, var, (var, a, b))
            if tool_res.get("status") == "ok":
                derivation_steps.append(r"\\int_{%s}^{%s} %s \, d%s = %s" % (
                    sympy_latex(a), sympy_latex(b), sympy_latex(sympify(expr)), var, tool_res["latex"]
                ))
                final_answer = tool_res["result_str"]
                routed = True

        # 2) Explicit integrate(...) form
        if not routed and t.lower().startswith("integrate("):
            # Expect integrate("x**2", "x", ("x",0,1)) minimal parsing
            try:
                # Unsafe to eval; parse minimally
                inner = t[len("integrate(") : -1]
                parts = [p.strip() for p in inner.split(",")]
                expr = parts[0].strip().strip("'\"")
                var = parts[1].strip().strip("'\"")
                if len(parts) >= 3:
                    lim = parts[2:5]
                    lim_var = lim[0].strip().strip("() '")
                    a = sympify(lim[1])
                    b = sympify(lim[2].rstrip(")"))
                    tool_res = integrate(expr, var, (lim_var, a, b))
                else:
                    tool_res = integrate(expr, var, None)
                if tool_res.get("status") == "ok":
                    derivation_steps.append(tool_res["latex"])  # already LaTeX of result
                    final_answer = tool_res.get("result_str", "")
                    routed = True
            except Exception:
                pass

        # 3) Solve equation like: Solve x^2 - 5x + 6 = 0 -> {2,3}
        if not routed and ("=" in t or t.lower().startswith("solve ")):
            try:
                # Strip leading 'solve' and optional trailing 'for <var>'
                q = re.sub(r"^(?i)\s*solve\s*", "", text.strip())
                q = re.sub(r"\s+for\s+[A-Za-z][A-Za-z0-9_]*.*$", "", q, flags=re.IGNORECASE)
                eq_match = re.search(r"(.+?)=\s*(.+)", q)
                if eq_match:
                    lhs_raw, rhs_raw = eq_match.groups()
                    lhs = sympify(_norm(lhs_raw))
                    rhs = sympify(_norm(rhs_raw))
                    expr = lhs - rhs
                else:
                    expr = sympify(_norm(q))
                symbols = sorted(expr.free_symbols, key=lambda s: s.name)
                var_symbol = symbols[0] if symbols else Symbol("x")
                tool_res = solve_equation(str(expr), var_symbol.name)
                if tool_res.get("status") == "ok":
                    sols = tool_res["solutions"]
                    sols_set = "{" + ", ".join(sols) + "}"
                    derivation_steps.append(r"Solve\\; %s = 0 \\;\\text{for}\\; %s" % (sympy_latex(expr), var_symbol.name))
                    final_answer = sols_set
                    routed = True
            except Exception:
                pass

        # 4) limit((1+1/n)**n, n, oo)
        if not routed and t.lower().startswith("limit("):
            try:
                # naive parse: limit(expr, var, point)
                inner = t[len("limit(") : -1]
                parts = [p.strip() for p in inner.split(",")]
                expr = sympify(_norm(parts[0]))
                var = Symbol(parts[1])
                point = sympify(parts[2])
                res = sympy_limit(expr, var, point)
                derivation_steps.append(r"\\lim_{%s \\to %s} %s = %s" % (
                    sympy_latex(var), sympy_latex(point), sympy_latex(expr), sympy_latex(res)
                ))
                final_answer = str(res)
                routed = True
            except Exception:
                pass

        # Fallback: try simplifying the entire text as an expression
        if not routed:
            simp = simplify_expr(t)
            if simp.get("status") == "ok":
                derivation_steps.append(simp["latex"])
                final_answer = simp["simplified_str"]
                routed = True

        if not routed:
            derivation_steps.append(r"\text{Unable to parse problem}")
            final_answer = ""

        state["solver_output"] = {
            "derivation_steps": derivation_steps,
            "final_answer": final_answer,
        }
        return state


