from __future__ import annotations

"""Minimal executable app for both CLI and ADK server run.

Import-safe: Only builds/executes when invoked as a script.
"""

import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from orchestrations.pipeline import build_root_agent


console = Console()


def create_session(user_id: str):  # Session type omitted for import safety
    """Factory for a simple in-memory session placeholder.

    In full ADK, use InMemorySessionService. Here we emulate a session_id.
    """
    return {"user_id": user_id, "session_id": f"sess-{user_id}"}


def run_query(session_id: str, text: str) -> Dict[str, object]:
    load_dotenv()
    root = build_root_agent()
    console.rule("Panguan-GPT Run")
    console.print(Panel.fit(text, title="Prompt"))
    state = root.run(text, state={"session_id": session_id})
    final_writeup = state.get("final_writeup", "")
    verification_report = state.get("verification_report", {})
    console.print(Panel(final_writeup, title="Final Writeup"))
    console.print(Panel(str(verification_report), title="Verification"))
    return {"final_writeup": final_writeup, "verification_report": verification_report}


def _run_file(session_id: str, path: str) -> None:
    p = Path(path)
    lines = [line.strip() for line in p.read_text().splitlines() if line.strip()]
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    reports_dir = Path("./reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_path = reports_dir / f"report-{ts}.md"
    out_lines = ["# Panguan-GPT Report", ""]
    for q in lines:
        res = run_query(session_id, q)
        out_lines.append("## Problem\n" + q)
        out_lines.append("\n### Final Writeup\n" + res["final_writeup"])  # type: ignore[index]
        out_lines.append("\n### Verification\n" + str(res["verification_report"]))  # type: ignore[index]
        out_lines.append("")
    out_path.write_text("\n".join(out_lines))
    console.print(f"Saved report to {out_path}")


def _run_demos(session_id: str) -> None:
    run_query(session_id, "Compute ∫_0^1 x^2 dx")
    run_query(session_id, "Find the general solution to y'' - y = 0 and verify initial conditions y(0)=1, y'(0)=0")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default=None)
    parser.add_argument("--once", type=str, default=None)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    sess = create_session("cli-user")
    session_id = sess["session_id"]

    if args.file:
        _run_file(session_id, args.file)
    elif args.once:
        run_query(session_id, args.once)
    elif args.demo:
        _run_demos(session_id)
    else:
        console.print("Provide --once, --file, or --demo")


