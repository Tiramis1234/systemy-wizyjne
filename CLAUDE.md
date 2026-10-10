# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Working with Claude

- **Always start in plan mode.** Explore and propose a plan first; write code only after the plan is approved.
- **Don't guess — ask.** If anything is unclear or ambiguous (requirements, parameters, naming, scope), ask the user before acting. Use `/grill-me` to stress-test a plan with many questions.
- **Explain while building.** When writing code, briefly explain non-obvious parts so the understanding check at the end of the stage is not a surprise.

## Project

Course project for **Machine Vision Systems** (winter semester 2026/27). We build **one** Python + OpenCV application that:

- lets the user experiment with image processing methods (preview, tunable parameters, comparing results),
- performs a complete inspection of a chosen product/process (inspection subject: **TBD** — initial project charter).

Stack: **FastAPI** backend (all image processing in Python) + simple **Vue** frontend, run together with **Docker Compose**.

Individual project — the author must understand every piece of code and be able to justify every parameter choice. Keep code readable and document why parameter values were chosen; no magic numbers.

## Course rules (mandatory)

1. **One application evolved through all stages P01–P12.** Each stage extends it, never replaces it.
2. **Keep previous features** — nothing from earlier stages may be removed or broken. All earlier tests must keep passing.
3. **Separate UI from algorithms** — processing modules never import FastAPI or anything web-related.
4. **Persist configuration** — method/pipeline parameters can be saved and loaded (JSON).
5. **Explain results** — the app shows not only the outcome but why (intermediate images, values, metrics, OK/NOK decision with reasoning).

## Architecture

```
app/                 # Python backend (FastAPI)
  core/              # OpenCV algorithms — pure functions: (image, params) -> result
  pipeline/          # composing steps into an inspection pipeline
  api/               # FastAPI routers + Pydantic schemas, no processing logic
  config/            # saving/loading configuration
tests/               # pytest, mirrors app/ structure
frontend/            # Vue 3 + Vite, talks to the API only
data/samples/        # small sample images for tests and demos
docs/                # per-stage TXT reports, written during each task
```

- `core/` works on `numpy.ndarray`; it knows nothing about HTTP, uploads or sessions.
- Method parameters are Pydantic models (validation + config serialization in one place).
- Endpoints are thin: decode image → call `core`/`pipeline` → encode result.
- Keep the frontend simple: parameter controls, image previews, result explanations. No business logic in Vue.

## Tooling

- Python dependencies and environment: **uv** (`uv add`, `uv run`). Never use bare `pip`.
- Run backend: `uv run fastapi dev app/main.py`
- Tests: `uv run pytest`
- Lint/format: `uv run ruff check .` and `uv run ruff format .`
- Frontend: `npm` inside `frontend/` (`npm run dev`, `npm run build`).
- Whole app: `docker compose up --build` (services: `backend`, `frontend`). Local `uv`/`npm` commands stay usable without Docker.

## Development process: TDD

Every feature follows red → green → refactor:

1. Write a failing test describing the expected behaviour (`uv run pytest` must show it failing).
2. Write the minimal code to make it pass.
3. Refactor with tests green.

- Algorithms in `core/` are tested on small synthetic images (e.g. `np.zeros` + drawn shapes) with known expected results.
- API endpoints are tested with FastAPI `TestClient`.
- No feature is committed without its tests.

## Git workflow

- `main` always contains a working application.
- **One branch per task (stage):** `feature/<short-description>`, e.g. `feature/p01-image-loading`. Branch off the current `main`.
- **One commit per feature:** a commit = one complete feature (tests + code). No mixed or WIP commits.
- **Cycle:** commit feature → update stage report in `docs/` → commit report → push branch → tests pass → understanding check passed → merge into `main` → delete branch.
- **Report is written during the task**, not at the end: after each feature commit, add its section to `docs/Lenarczyk_Marek_Inf_ProjektXX.txt` and commit it separately as `docs(reports): ...`.
- **Conventional Commits:** `type(scope): description`, lowercase, imperative, English.
  - Types: `feat`, `fix`, `test`, `refactor`, `docs`, `chore`, `style`, `perf`.
  - Scope = location in the codebase: `core`, `pipeline`, `api`, `config`, `frontend`, `tests`, `docs`, …
  - Examples: `feat(core): add otsu thresholding`, `feat(frontend): add histogram preview`, `docs(reports): add p01 report`.
- **Keep commit and PR messages short and plain.** Say what changed, not a lecture on why or how. A commit is usually just the subject line; a PR description is a few bullet points at most.
- **Do not add `Co-Authored-By` lines or any Claude/AI attribution to commits or PR descriptions.**
- Never commit or push without the user's explicit instruction.

## Understanding check (stage gate)

Passing the course requires 100% knowledge of the code; the instructor verifies it, e.g. by asking the author to change part of it. **A stage is not finished — no merge into `main` — until the user understands all of its code** (backend, frontend, tests, config).

Before merging a stage, Claude runs the check:

1. **Questions** about the stage's code: what each module/function does, why each parameter value was chosen, how data flows from the API to `core/` and back, what the tests verify.
2. **At least one "change X" task**, e.g. change a parameter's range, add an option to a method, alter an OK/NOK rule. The user writes the change themselves — Claude does not write or hint the code, only reviews it afterwards; tests must pass.

- If gaps show up, Claude explains the fragment and then checks it again.
- Merge only after the user explicitly confirms they understand everything **and** the check is passed.
- The practice change is not committed unless the user decides to keep it.

## Stage deliverables

After each stage P01–P12 two files with the same base name are submitted:

- `Lenarczyk_Marek_Inf_ProjektXX.txt` — report in `docs/`, **UTF-8**, `XX` = 01–12,
- `Lenarczyk_Marek_Inf_ProjektXX.zip` — current source code.

The report covers: implemented features, progress since the previous stage, methods and parameters (with justification), test conditions, results and illustrations, problems, limitations, next steps. **Clearly separate the required minimum from extras.** The P12 report additionally includes a full validation of the application.

ZIP excludes: `.venv`, `__pycache__`, `node_modules`, `frontend/dist`, `.git`, large data and temporary files.

## Schedule

The stage timeline is in `README.md`. Stage briefs P01–P12 arrive as the course progresses — before starting a stage, ask for its brief and grading criteria (minimum vs. extensions).

## Grading

Each stage: minimum = 3, maximum = 5. The TXT report and ZIP are part of the minimum. Extras raise the grade — always finish the minimum first, then extensions.

## Code conventions

- **Readability over cleverness.** Prefer straightforward, explicit code over clever one-liners, tricks or premature abstractions. If it needs explaining at the defense, it should be obvious from reading it.
- Everything in English: code, comments, docs, commits.
- Python with type hints; `ruff` for lint and formatting.
- Default parameter values live in one place, each with a short comment explaining where it comes from.
- OpenCV uses BGR. Images reach the frontend as PNG/JPG encoded with `cv2.imencode`, which expects BGR, so encoding is the BGR→RGB boundary — no manual channel swap in `core/`.
