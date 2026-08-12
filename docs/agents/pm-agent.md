# pm-agent — design notes

## Purpose

The `pm-agent` is the first stage of the nurutech-company pipeline. It converts a
one-line product idea into a structured product requirements document (PRD). It is
the analogue of the Product Manager role in a software company and of the
`WritePRD` action in MetaGPT.

## Position in the pipeline

```
one-line idea ──▶ pm-agent ──▶ PRD ──▶ architect-agent ──▶ ...
```

The PRD produced here is the sole input to the `architect-agent`. Because of that,
the PRD must be self-contained: it cannot rely on anything said in the
conversation that produced it.

## Input

- A single line describing the product idea.
- Optionally, a short amount of context such as target audience, platform, or a
  hard constraint.

When the idea is ambiguous on a point that changes the requirements, the agent
records an explicit assumption rather than halting. This keeps the pipeline moving
and makes every assumption visible for later validation.

## Output contract

A single Markdown document with eight fixed sections: Overview, Goals, Target
users, User stories, System requirements, Success metrics, Out of scope, and
Assumptions and risks. The headings are fixed because downstream agents parse the
structure. A missing section is written as "None" rather than removed.

This fixed, parseable structure mirrors the idea of a structured output contract
(an "ActionNode" in MetaGPT): the stage returns a predictable shape, not free
prose, so the next stage can consume it reliably.

## Design decisions

- **Acceptance criteria are mandatory on every user story.** A story in the
  "As a role, I want goal, so that benefit" form but without testable acceptance
  criteria is treated as incomplete and excluded. This forces the PRD to be
  verifiable rather than aspirational.
- **System requirements use "shall" and must be testable.** This separates real
  requirements from goals and from vague quality wishes, and gives the QA stage
  concrete conditions to check against later.
- **The agent stays in the product lane.** It does not select technologies or
  propose a design. Keeping stages single-purpose is what makes the roles
  composable and the handoffs clean.

## How to invoke

Within Claude Code, with this repository open as the workspace:

```
> Use the pm-agent to turn this idea into a PRD: "a habit tracker for children aged 4 to 8"
```

The agent's final message is the PRD, ready to pass to the `architect-agent`.

## Mapping to MetaGPT

| nurutech-company | MetaGPT |
| --- | --- |
| `pm-agent` | `ProductManager` role |
| PRD output contract | `WritePRD` action and its structured output |
| Fixed section headings | ActionNode structured output schema |
