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
records a clarification under "Anything unclear" rather than halting. This keeps
the pipeline moving and makes every open question visible for later validation.

## Output contract

A single Markdown document with twelve fixed sections: Language, Programming
Language, Original Requirements, Project Name, Product Goals, User Stories,
Competitive Analysis, Competitive Quadrant Chart, Requirement Analysis,
Requirement Pool, UI Design draft, and Anything unclear. This section set is taken
directly from MetaGPT's `WritePRD` action node. The headings are fixed because
downstream agents parse the structure. A missing section is written as "None"
rather than removed.

This fixed, parseable structure is the "ActionNode" idea from MetaGPT: the stage
returns a predictable shape, not free prose, so the next stage can consume it
reliably.

## Grounding in MetaGPT

The output contract is a faithful adaptation of MetaGPT's PRD action, not an
invented format. The mapping below records the correspondence field by field.

| This agent's section | MetaGPT `WritePRD` node field | MetaGPT instruction, in brief |
| --- | --- | --- |
| Language | Language | The project language, matching the requirement language |
| Programming Language | Programming Language | Mainstream stack; default Vite, React, MUI, Tailwind CSS |
| Original Requirements | Original Requirements | The original user requirement, restated |
| Project Name | Project Name | A snake_case name derived from the requirement |
| Product Goals | Product Goals | Up to three clear, orthogonal goals |
| User Stories | User Stories | Three to five scenario-based stories |
| Competitive Analysis | Competitive Analysis | Five to seven competitive products |
| Competitive Quadrant Chart | Competitive Quadrant Chart | A mermaid quadrantChart, scores between 0 and 1 |
| Requirement Analysis | Requirement Analysis | A detailed analysis of the requirements |
| Requirement Pool | Requirement Pool | Top-five requirements tagged P0, P1, or P2 |
| UI Design draft | UI Design draft | A simple description of UI elements and layout |
| Anything unclear | Anything UNCLEAR | State unclear aspects and try to clarify them |

## Design decisions

- **The output mirrors MetaGPT's WritePRD fields exactly.** Using the real field
  set, rather than a reinvented one, keeps the "based on MetaGPT" claim literal.
  This is a deliberate change from an earlier version of this agent, which used a
  bespoke PRD format (acceptance criteria on every story, "shall" requirements).
  That earlier format was a general product-management convention, not MetaGPT's,
  so it was replaced with the grounded contract.
- **Prioritisation lives in the requirement pool.** MetaGPT expresses priority
  through the P0/P1/P2 pool rather than through per-story acceptance criteria, and
  this agent follows that model.
- **The agent stays in the product lane.** It does not select an architecture or
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
| PRD output contract | `WritePRD` action, `WritePRD` node |
| Competitive quadrant chart | Competitive Quadrant Chart (mermaid quadrantChart) |
| Fixed section headings | ActionNode structured output schema |
