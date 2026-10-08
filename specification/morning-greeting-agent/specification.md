# Specification: morning-greeting-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` at the solution root for full context
- [x] Bootstrap agent code in `assets/morning-greeting-agent/` using the `sap-agent-bootstrap` skill instructions (invoke from inside `assets/morning-greeting-agent/`, use copy commands — do NOT create files manually)
- [x] Install dependencies; validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

No complex multi-step workflow or domain-specific reference material is required for a greeting agent. The greeting generation logic is simple enough for the system prompt. Skip runtime skill creation.

---

## Project-Specific Tasks

## Scheduler Setup

- [x] Add `apscheduler` to `requirements.txt` as a dependency for the daily 8:00 AM trigger
- [x] In `assets/morning-greeting-agent/app/`, create `scheduler.py` that:
  - Imports `AsyncIOScheduler` from `apscheduler.schedulers.asyncio`
  - Defines a `start_scheduler(agent_invoke_fn)` function that schedules a daily job at 08:00 (configurable timezone, default UTC)
  - The scheduled job calls the agent's `invoke` (or equivalent) function with a fixed message: `"Good morning! Please send a greeting to the user."`
  - Logs `M1.achieved: morning greeting scheduler initialized, next trigger at 08:00` on successful setup
  - Logs `M1.missed: scheduler initialization failed, agent will not trigger` on error
- [x] Wire `start_scheduler` into `main.py` so the scheduler starts when the application starts (after `app = server.build()` and `bootstrap(app)`)

## Greeting Generation (System Prompt)

- [x] Open `assets/morning-greeting-agent/app/agent.py` and update the `@prompt_section` body (`get_system_prompt`) to include all required instructions
- [x] No MCP tools are required for greeting generation — the LLM generates the greeting directly from the system prompt.

## Greeting Delivery & Confirmation

- [x] In `scheduler.py`, after the agent produces the greeting text, log M2/M3/M4 milestones
- [x] Implement a fallback static greeting: `"Good morning! Wishing you a productive and wonderful day ahead."`
- [x] All milestone logs (M2, M3, M4) implemented in both `agent.py` and `scheduler.py`

---

## Business Instrumentation

- [x] Implement business step instrumentation for all four milestones from the PRD (M1–M4)
- [x] Add OpenTelemetry custom spans in `_run_greeting()` helper (not in async generators)
- [x] Extract business logic from `stream()` into `_run_greeting()` async helper — instrumented with OTel spans
- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## MCP Tool Integration

No SAP API integration is required for this agent. The agent uses the LLM directly to generate the greeting. Skip MCP translation file creation, MCP server asset setup, and mock generation.

---

## Testing

- [x] Install test dependencies: `pip install -r requirements-test.txt` from `assets/morning-greeting-agent/`
- [x] Write unit tests in `assets/morning-greeting-agent/tests/` (test_scheduler.py, test_agent.py)
- [x] Write one integration test in `assets/morning-greeting-agent/tests/test_integration.py`
- [x] Run `pytest` from `assets/morning-greeting-agent/` (no args)
- [x] Verify `assets/morning-greeting-agent/app/agent.py` has exactly 9 decorated functions — confirmed: 9
- [x] Run `pytest` again (no args) to generate final `test_report.json`
- [x] Verify `test_report.json` exists in `assets/morning-greeting-agent/` — confirmed ✓
