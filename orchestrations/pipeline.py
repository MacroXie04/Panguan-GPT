from __future__ import annotations

"""Pipeline orchestration: Planner → Parallel(Solver, Research) → Verifier → Explainer."""

from typing import Dict

from agents.planner import PlannerAgent
from agents.solver import MathSolverAgent
from agents.research import ResearchAgent
from agents.verifier import VerifierAgent
from agents.explainer import ExplainerAgent


class SequentialAgent:
    def __init__(self, steps):
        self.steps = steps

    def run(self, text: str, state: Dict[str, object] | None = None) -> Dict[str, object]:
        state = {} if state is None else dict(state)
        for step in self.steps:
            state = step.run(text, state)
        return state


class ParallelAgent:
    def __init__(self, agents):
        self.agents = agents

    def run(self, text: str, state: Dict[str, object] | None = None) -> Dict[str, object]:
        state = {} if state is None else dict(state)
        # Run sequentially here to avoid threading; merge outputs
        for agent in self.agents:
            state = agent.run(text, state)
        return state


def build_root_agent() -> SequentialAgent:
    planner = PlannerAgent()
    solver = MathSolverAgent()
    research = ResearchAgent()
    verifier = VerifierAgent()
    explainer = ExplainerAgent()

    root = SequentialAgent([
        planner,
        ParallelAgent([solver, research]),
        verifier,
        explainer,
    ])
    return root


