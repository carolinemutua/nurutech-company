# architect-agent — design notes

## Purpose

The `architect-agent` is the second stage of the nurutech-company pipeline. It
converts a product requirements document (PRD) into a concise, complete system
design. It is the analogue of the Architect role in a software company and of the
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
agent chooses a reasonable default, records it under "Anything unclear", and
continues. This keeps the pipeline moving and makes every design assumption
visible for later validation.

## Output contract

A single Markdown document with five fixed sections: Implementation approach, File
list, Data structures and interfaces, Program call flow, and Anything unclear.
This section set is taken directly from MetaGPT's `DesignAPI` action node, whose
fields are Implementation approach, File list, Data structures and interfaces,
Program call flow, and Anything UNCLEAR. The headings are fixed because downstream
agents parse the structure. A missing section is written as "None" rather than
removed.

This fixed, parseable structure is the "ActionNode" idea from MetaGPT: the stage
returns a predictable shape, not free prose, so the next stage can consume it
reliably.

## Grounding in MetaGPT

The output contract is a faithful adaptation of MetaGPT's design action, not an
invented format. The mapping below records the correspondence field by field.

| This agent's section | MetaGPT `DesignAPI` node field | MetaGPT instruction, in brief |
| --- | --- | --- |
| Implementation approach | Implementation approach | Analyze the difficult points and select an open-source framework |
| File list | File list | Relative paths only, with a correct entry file for the language |
| Data structures and interfaces | Data structures and interfaces | A mermaid classDiagram with methods and type annotations, marked relationships, PEP8 |
| Program call flow | Program call flow | A mermaid sequenceDiagram covering init and CRUD of each object |
| Anything unclear | Anything UNCLEAR | State unclear aspects and try to clarify them |

The Architect role's goal ("design a concise, usable, complete software system")
and constraints ("keep the architecture simple enough and use appropriate
open-source libraries") are carried over into the Role and Constraints text of the
agent file.

## Design decisions

- **The output mirrors MetaGPT's DesignAPI fields exactly.** Using the real field
  set, rather than a reinvented one, keeps the "based on MetaGPT" claim literal
  and makes the design diagram-first, as MetaGPT intends.
- **Diagrams are expressed in mermaid.** The class diagram and the sequence
  diagram are the core of the design, matching MetaGPT's use of mermaid for the
  data-structures view and the program call flow.
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
| Design output contract | `WriteDesign` action, `DesignAPI` node |
| Class diagram + sequence diagram | Data structures and interfaces, Program call flow |
| Fixed section headings | ActionNode structured output schema |
