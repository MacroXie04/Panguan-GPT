from __future__ import annotations

"""PlannerAgent: decomposes a question into steps and verification items.

Output key: "plan_json"
"""

from typing import Dict, List, Optional


class PlannerAgent:
    model: str = "gemini-2.0-flash"

    def run(self, text: str, state: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        state = {} if state is None else dict(state)
        # Minimal heuristic plan
        steps: List[Dict[str, object]] = []
        expected_theorems: List[str] = []
        verification_items: List[str] = []

        t = text.lower()
        if "integral" in t or "∫" in t or t.startswith("integrate("):
            steps.append({"step": "Compute integral", "tool": "calculus.integrate"})
            expected_theorems.append("Fundamental Theorem of Calculus")
            verification_items.append("Differentiate result to recover integrand")
        if "solve" in t or "=" in t:
            steps.append({"step": "Solve equation", "tool": "equation.solve_equation"})
            expected_theorems.append("Quadratic formula (if polynomial)")
            verification_items.append("Plug solutions back into equation")
        if "limit(" in t:
            steps.append({"step": "Compute limit", "tool": "sympy.limit"})
            expected_theorems.append("Definition of e via (1+1/n)^n")
            verification_items.append("Numeric approach check")

        plan_json = {
            "steps": steps,
            "expected_theorems": expected_theorems,
            "verification_items": verification_items,
        }
        state["plan_json"] = plan_json
        return state


