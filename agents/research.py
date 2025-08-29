from __future__ import annotations

"""ResearchAgent: lightweight research assistant.

Default tool: google_search when available. Optionally uses Tavily or Serper
if API keys are present; degrades silently otherwise.

Output key: "research_output" with keys: citations, summary, key_expressions.
"""

import os
from typing import Dict, List, Optional

from tools import web_search as web_tools


class ResearchAgent:
    model: str = "gemini-2.0-flash"

    def __init__(self) -> None:
        self.tools = []
        if getattr(web_tools, "SEARCH_TOOL", None) is not None:
            self.tools.append(web_tools.SEARCH_TOOL)
        # Optional adapters: placeholders (not executed here to avoid runtime deps)
        if os.getenv("TAVILY_API_KEY"):
            # In a full ADK context, wrap Tavily into FunctionTool
            pass
        if os.getenv("SERPER_API_KEY"):
            # In a full ADK context, wrap Serper into FunctionTool
            pass

    def run(self, text: str, state: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        state = {} if state is None else dict(state)
        # Offline-safe: return an empty stub. Real implementation would call tools.
        research_output = {
            "citations": [],
            "summary": "",
            "key_expressions": [],
        }
        state["research_output"] = research_output
        return state


