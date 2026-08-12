# architect-agent — design notes

## Purpose

The `architect-agent` is the second stage of the nurutech-company pipeline. It
converts a product requirements document (PRD) into a concrete system design. It
is the analogue of the Architect role in a software company and of the
`WriteDesign` action in MetaGPT.

## Position in the pipeline

```
PRD ──▶ architect-agent ──▶ system design ──▶ planner-agent ──▶ ...
```

The design produced here is the sole input to the `planner-agent`. Because of
that, the design must be self-contained: it cannot rely on the PRD being visible
alongside it or on anything said in the conversation that produced it.

## Input

- A complete PRD from the pm-agent, with its eight fixed sections.

When the PRD is silent on a design decision that must be made to proceed, the
agent chooses a reasonable default, records it under Design decisions, and
continues. This keeps the pipeline moving and makes every design assumption
visible for later validation.

## Output contract

A single Markdown document with eight fixed sections: Architecture overview,
Technology choices, Data structures, Interface contracts, File and module plan,
Cross-cutting concerns, Requirements traceability, and Design decisions and
risks. The headings are fixed because downstream agents parse the structure. A
missing section is written as "None" rather than removed.

This fixed, parseable structure mirrors the idea of a structured output contract
(an "ActionNode" in MetaGPT): the stage returns a predictable shape, not free
prose, so the next stage can consume it reliably.

## Design decisions

- **Requirements traceability is mandatory.** Every system requirement from the
  PRD must map to a component or file. This closes the gap between what the
  product must do and how the system delivers it, and gives the QA stage a map to
  check against later.
- **Technology choices must be justified against a requirement or constraint.**
  This keeps the design honest and prevents preference-driven complexity.
- **Interface contracts are precise about inputs and outputs.** Stating each
  contract exactly lets the planner and engineer build components independently
  against a shared boundary.
- **The agent stays in the design lane.** It does not schedule tasks or write
  code. Keeping stages single-purpose is what makes the roles composable and the
  handoffs clean.

## How to invoke

Within Claude Code, with this repository open as the workspace, after a PRD
exists:

```
> Use the architect-agent to turn this PRD into a system design: <paste the PRD>
```

The agent's final message is the design, ready to pass to the `planner-agent`.

## Mapping to MetaGPT

| nurutech-company | MetaGPT |
| --- | --- |
| `architect-agent` | `Architect` role |
| Design output contract | `WriteDesign` action and its structured output |
| Requirements traceability table | Design-to-requirement mapping |
| Fixed section headings | ActionNode structured output schema |
