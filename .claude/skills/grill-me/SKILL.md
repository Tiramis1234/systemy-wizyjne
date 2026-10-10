---
name: grill-me
description: Grill the user with many questions about a plan, task or design before any code is written. Use when the user says "grill me", "/grill-me", or wants a plan or stage brief stress-tested.
---

# Grill me

Ask the user a lot of questions to remove every ambiguity before implementation. Do not write code and do not propose solutions until the grilling is done.

## How to grill

1. Read the plan, stage brief or idea the user gave (and relevant code / `CLAUDE.md` if needed).
2. Ask questions in rounds of 3–5, grouped by topic. Wait for answers before the next round.
3. Dig deeper on vague answers ("it depends", "something like", "maybe") — ask for concrete values or examples.
4. Keep going until there are no open questions left, then summarise the decisions as a short list and ask the user to confirm.

## What to ask about

- **Scope:** what exactly is the required minimum, what are extras, what is out of scope.
- **Inputs:** image sources, formats, sizes, lighting, sample data.
- **Methods and parameters:** which algorithm, why it and not an alternative, parameter values and how they will be justified in the report.
- **Expected results:** what counts as correct, how it will be shown and explained in the UI.
- **Tests:** which cases (normal, edge, failure) prove the feature works — TDD starts from these.
- **Configuration:** what must be saved and loaded.
- **Integration:** impact on earlier stages, API endpoints, frontend changes.
- **Report:** what goes into the stage report in `docs/`, which illustrations are needed.
- **Risks:** what could go wrong, what is the fallback.

## Rules

- Questions must be short and concrete — one thing per question.
- Prefer questions with options when there are obvious choices.
- Never assume an answer; if the user skips a question, ask it again later.
- Point out contradictions between answers.
