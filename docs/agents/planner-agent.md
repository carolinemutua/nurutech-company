# planner-agent — design notes

## Purpose

The `planner-agent` is the third stage of the nurutech-company pipeline. It
converts a system design into an actionable build plan. It is the analogue of the
Project Manager role in a software company and of the `WriteTasks` (project
management) action in MetaGPT.

## Position in the pipeline

```
system design ──▶ planner-agent ──▶ build plan ──▶ engineer-agent ──▶ ...
```

The plan produced here is the sole input to the `engineer-agent`. Because of that,
the plan must be self-contained: it cannot rely on the design being visible
alongside it or on anything said in the conversation that produced it.

## Input

- A complete system design from the architect-agent, with its file list, class
  diagram, and program call flow.

When the design is silent on a planning detail that must be settled to proceed,
the agent chooses a reasonable default, records it under "Anything unclear", and
continues. This keeps the pipeline moving and makes every planning assumption
visible for later validation.

## Output contract

A single Markdown document with seven fixed sections: Required packages, Required
other language third-party packages, Logic Analysis, Task list, Full API spec,
Shared Knowledge, and Anything unclear. This section set is taken directly from
MetaGPT's project-management action node. The headings are fixed because the
engineer-agent parses the structure. A missing section is written as "None" rather
than removed.

This fixed, parseable structure is the "ActionNode" idea from MetaGPT: the stage
returns a predictable shape, not free prose, so the next stage can consume it
reliably.

## Grounding in MetaGPT

The output contract is a faithful adaptation of MetaGPT's project-management
action, not an invented format. The mapping below records the correspondence field
by field.

| This agent's section | MetaGPT `PM_NODE` field | MetaGPT instruction, in brief |
| --- | --- | --- |
| Required packages | Required packages | Third-party packages with pinned versions |
| Required other language third-party packages | Required Other language third-party packages | Packages for non-primary languages |
| Logic Analysis | Logic Analysis | Files with classes, methods, functions, dependencies, imports; must match the design file list |
| Task list | Task list | Filenames ordered by dependency |
| Full API spec | Full API spec | All APIs in OpenAPI 3.0, or blank if no client-server split |
| Shared Knowledge | Shared Knowledge | Common utilities and configuration relied on across files |
| Anything unclear | Anything UNCLEAR | State unclear planning aspects and try to clarify them |

The Project Manager role's goal ("break down tasks according to PRD/technical
design, generate a task list, and analyze task dependencies to start with the
prerequisite modules") and constraint ("use same language as user requirement")
are carried over into the Role and Constraint text of the agent file.

## Design decisions

- **The output mirrors MetaGPT's project-management fields exactly.** Using the
  real field set keeps the "based on MetaGPT" claim literal and keeps the plan
  build-ready.
- **The task list is dependency-ordered.** MetaGPT's Project Manager exists to
  sequence prerequisite modules first, and this agent preserves that as its
  central job.
- **Logic analysis must match the design file list.** Tying the plan back to the
  design's files prevents drift between the two stages.
- **The agent stays in the planning lane.** It does not write code. Keeping stages
  single-purpose is what makes the roles composable and the handoffs clean.

## How to invoke

Within Claude Code, with this repository open as the workspace, after a design
exists:

```
> Use the planner-agent to turn this design into a build plan: <paste the design>
```

The agent's final message is the plan, ready to pass to the `engineer-agent`.

## Mapping to MetaGPT

| nurutech-company | MetaGPT |
| --- | --- |
| `planner-agent` | `ProjectManager` role |
| Plan output contract | `WriteTasks` action, project-management node |
| Dependency-ordered task list | Task list field |
| Fixed section headings | ActionNode structured output schema |
