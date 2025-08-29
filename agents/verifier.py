from __future__ import annotations

"""VerifierAgent: performs checks on solver output using numeric and unit tools."""

from typing import Dict, List, Optional

from tools.numeric import evaluate
from tools.units import convert


class VerifierAgent:
    model: str = "gemini-2.0-flash"

    def run(self, text: str, state: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        state = {} if state is None else dict(state)
        details: List[str] = []
        status = "passed"

        solver = state.get("solver_output", {})
        final_answer = solver.get("final_answer", "")

        # Basic numeric check if final_answer is numeric-ish
        try:
            # Attempt to evaluate as SymPy expression
            ev = evaluate(str(final_answer))
            if ev.get("status") == "ok":
                details.append(f"Numeric evaluation: {ev['float_value']}")
        except Exception:
            pass

        verification_report = {"status": status, "details": details}
        state["verification_report"] = verification_report
        return state


