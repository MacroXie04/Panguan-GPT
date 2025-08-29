from __future__ import annotations

"""Web search tools exposed from Google ADK.

Gemini 2-only; returns grounded results/citations when available.
"""

try:
    # Import guarded for import safety
    from google.adk.tools import google_search as _google_search
except Exception:  # noqa: BLE001
    _google_search = None


# Keep a module-level variable for consumers
SEARCH_TOOL = _google_search


