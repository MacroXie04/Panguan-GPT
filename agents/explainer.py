from __future__ import annotations

"""ExplainerAgent: Produces Markdown + LaTeX explanation from pipeline state.

Output key: "final_writeup" (string)
"""

from typing import Dict, Optional


class ExplainerAgent:
    model: str = "gemini-2.0-flash"

    def run(self, text: str, state: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        state = {} if state is None else dict(state)
        plan = state.get("plan_json", {})
        solver = state.get("solver_output", {})
        research = state.get("research_output", {})
        verify = state.get("verification_report", {})

        steps = solver.get("derivation_steps", [])
        steps_md = "\n".join([f"- {s}" for s in steps])
        final_box = solver.get("final_answer", "")

        writeup = (
            "### Plan\n"
            + f"{plan}\n\n"
            + "### Derivation Steps\n"
            + steps_md
            + "\n\n### Research Notes\n"
            + f"{research}\n\n"
            + "### Verification\n"
            + f"{verify}\n\n"
            + "### Final Answer\n"
            + f"\\boxed{{{final_box}}}"
        )

        state["final_writeup"] = writeup
        return state


