# ZioNet-HW-2: Job Application Triage Workflow

## Task Definition

Build a triage workflow for job applications using LangGraph:
preprocess → classify → route.

Specifically:

1. Preprocess raw application data (plain function node)
2. Classify applications using an LLM (agent node)
3. Route to shortlist, reject, or escalate (conditional edges)
4. Stream events while the pipeline runs (no silent black box)
5. Pause for human approval before rejection (bonus HITL)

---

## Description

This project implements a **job application triage pipeline** that automatically sorts incoming applications into three categories using an LLM classifier.

Key components:

- **`TriageNodes` class** - Bundles all pipeline node methods with shared LLM client and logger via dependency injection.
- **`ApplicationClassification`** - Pydantic model for structured LLM output (category, urgency, missing_info, reasoning, score).
- **`ApplicationState`** - TypedDict defining the shared state passed between nodes.
- **`GroqClient`** - Lightweight LLM client for single-turn completions.
- **`AppLogger`** - Colored structured logger with `NodeLogger` for pipeline-specific prefixes.

Project structure:

```
./
│
├── src/
│   ├── agent.py              # Entry point for streaming pipeline
│   ├── graph.py              # LangGraph StateGraph builder
│   ├── prompts.py            # LLM classifier system prompt
│   ├── llm/
│   │   └── groq_client.py    # Groq LLM client
│   ├── nodes/
│   │   └── triage_nodes.py   # All pipeline nodes in one class
│   ├── types/
│   │   ├── classification.py # ApplicationClassification (Pydantic)
│   │   └── state.py          # ApplicationState (TypedDict)
│   └── logger/
│       ├── app_logger.py     # AppLogger
│       └── subloggers/       # ColoredFormatter, Logger, NodeLogger
├── data/
│   └── samples.py            # Sample applications for testing
└── main.py                   # Entry point
```

---

## Purpose

1. **Triage workflow** - preprocess → classify → route in a clean LangGraph pipeline.
2. **Structured output** - LLM response validated against Pydantic schema.
3. **Conditional routing** - 3 paths: shortlist, reject, escalate.
4. **Streamed events** - each node completion logged in real time.
5. **Human-in-the-loop** - rejection requires human confirmation.

---

## How It Works

1. **Preprocess** - Cleans and normalizes raw application data (strips whitespace, normalizes casing, parses types).
2. **Classify** - Sends cleaned data to LLM with structured output prompt. Parses response into `ApplicationClassification`.
3. **Router** - Reads `classification.category` and returns routing key.
4. **Shortlist** - Logs interview scheduling.
5. **Reject** - Pauses for human confirmation before sending rejection.
6. **Escalate** - Flags application for human review.

---

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

Create `.env`:

```
GROQ_API_KEY=your_groq_key
MODEL_NAME=llama-3.3-70b-versatile
```

---

## Run

```bash
python main.py
```

---

## Output Example

```
[21:05:12] [INFO] ============================================================
[21:05:12] [INFO] [MAIN] Starting: Strong candidate - John Doe
[21:05:12] [INFO] ============================================================
[21:05:12] [INFO] [PREPROCESS] Starting: Cleaning application data
[21:05:12] [INFO] [PREPROCESS] Done: John Doe → Senior Python Developer
[21:05:12] [INFO] [MAIN] Node 'preprocess' completed
[21:05:12] [INFO] [CLASSIFY] Starting: Analyzing application with LLM
[21:05:12] [INFO] [CLASSIFY] Done: shortlist (score=90)
[21:05:12] [INFO] [ROUTER] Routing to: SHORTLIST
[21:05:12] [INFO] [MAIN] Node 'classify' completed
[21:05:12] [INFO] [SHORTLIST] Starting: Scheduling interview for: John Doe
[21:05:12] [INFO] [SHORTLIST] Score: 90/100 | Urgency: high
[21:05:12] [INFO] [SHORTLIST] Done: Strong match for the role.
[21:05:12] [INFO] [MAIN] Node 'shortlist' completed
[21:05:12] [INFO] [MAIN] Done: Strong candidate - John Doe
```

---

## Dependencies

- Python 3.11+
- `langgraph` - Graph-based workflow orchestration
- `langchain-groq` - Groq integration
- `groq` - Groq API client
- `pydantic` - Structured output validation
- `python-dotenv` - Environment variable loading

---

## Project Status

**Status:** ✅ Completed

- Triage workflow with 3 executors implemented
- Structured JSON output validated via Pydantic
- Conditional routing with 3 paths
- Streamed events for every node
- Human-in-the-loop approval before rejection
- Clean OOP architecture with DI throughout

---

Made with ❤️ and Python by **Sam Malikin** 🎓
