# Panguan-GPT

Panguan-GPT is a multi-agent math/academic solver built on the Google ADK (Agent Development Kit). It emphasizes symbolic-first reasoning (SymPy), numeric validation, grounded web search, and explainable derivations.

## Quickstart

- **Python**: 3.9+
- **Install deps**:
  ```bash
  pip install -r requirements.txt
  ```
- **Environment**: put keys in `.env` at project root:
  ```
  GOOGLE_API_KEY=""
  GOOGLE_GENAI_USE_VERTEXAI=FALSE
  # If using Vertex later:
  # GOOGLE_GENAI_USE_VERTEXAI=TRUE
  # GOOGLE_CLOUD_PROJECT=""
  # GOOGLE_CLOUD_LOCATION="us-central1"
  ```
- **Run (ADK)** from project root:
  ```bash
  adk run .
  adk api_server
  ```
  The first command runs the root pipeline. The second starts a FastAPI server.

## Architecture

```
Planner ──▶ Parallel( Solver, Research ) ──▶ Verifier ──▶ Explainer
```

- **Planner**: decomposes the question into steps/tools.
- **Solver**: SymPy-first derivation, optional code execution for numeric checks.
- **Research**: brief citations/snippets via search.
- **Verifier**: unit checks, plug-back evaluation, boundary cases, cross-check with research.
- **Explainer**: clean Markdown + LaTeX write-up with boxed final result.

## How to run

- **ADK CLI** (root = pipeline SequentialAgent):
  ```bash
  adk run .
  ```

- **ADK API Server**:
  ```bash
  adk api_server
  ```
  Example request:
  ```bash
  curl -X POST http://localhost:8000/run \
    -H 'Content-Type: application/json' \
    -d '{"input": "Compute \\int_0^1 x^2 \\mathrm{d}x"}'
  ```

- **Python CLI** (this repo):
  ```bash
  python app.py --once "Compute ∫_0^1 x^2 dx"
  # or run a file of prompts (one per line)
  python app.py --file ./prompts.txt
  # demos
  python app.py --demo
  ```

## Config matrix (AI Studio vs Vertex)

- **AI Studio**: set `GOOGLE_API_KEY` and keep `GOOGLE_GENAI_USE_VERTEXAI=FALSE`.
- **Vertex**: set `GOOGLE_GENAI_USE_VERTEXAI=TRUE`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`.

## Grounded search UI

When `google_search` returns suggestions/citations, display them with title, source, date, and URL. Use these for brief, high-signal citations in the write-up.

## Determinism knobs

- Deterministic rounding in explanations: 4 decimal places.
- Seed values (if executing Python sampling) should be fixed for repeatability.

## Tests

Run tests with:
```bash
pytest -q
```

# Panguan-GPT