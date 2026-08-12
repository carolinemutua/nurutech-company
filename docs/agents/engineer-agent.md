# engineer-agent — design notes

## Purpose

The `engineer-agent` is the fourth stage of the nurutech-company pipeline. It
converts a build plan and its system design into complete source code. It is the
analogue of the Engineer role in a software company and of the `WriteCode` action
in MetaGPT.

## Position in the pipeline

```
build plan ──▶ engineer-agent ──▶ source code ──▶ qa-agent ──▶ ...
```

The code produced here is the sole input to the `qa-agent`. Because of that, the
code must stand on its own: it cannot rely on the plan or design being visible
alongside it or on anything said in the conversation that produced it.

## Input

- A build plan from the planner-agent, whose task list sets the file order.
- The system design the plan was derived from, whose class diagram and interfaces
  the code must follow exactly.

## Output contract

A sequence of `## Code: <path>` sections, one per file in the task list, each
containing the complete contents of that file in a fenced code block. This mirrors
MetaGPT's WriteCode output format, which emits one file per code block under a
`## Code: <filename>` heading. The headings are fixed because downstream tooling
parses them. No prose is added between sections.

## Grounding in MetaGPT

The output format and the standards are a faithful adaptation of MetaGPT's
WriteCode action, not an invented format. The correspondence is recorded below.

| This agent | MetaGPT `WriteCode` |
| --- | --- |
| `## Code: <path>` sections, one per file | The action's "Format example": one code block per file under `## Code: <filename>` |
| One file at a time, complete, no TODO | Attentions 1, 2, and 7 of the WriteCode prompt |
| Defaults, strong types, no circular imports | Attention 3 |
| Follow the design's data structures and interfaces | Attention 4 |
| Completeness check for every class and function | Attention 5 |
| Import before use | Attention 6 |
| Google-style, modular, maintainable | The Engineer role's goal and constraints |

The Engineer role's goal ("write elegant, readable, extensible, efficient code")
and constraints ("the code should conform to standards like google-style and be
modular and maintainable; use same language as user requirement") are carried over
into the Role and Constraints text of the agent file.

## Design decisions

- **The output is one code block per file, in task order.** Matching MetaGPT's
  per-file format keeps the handoff parseable and keeps each file complete rather
  than sketched.
- **The design is authoritative.** The engineer follows the class diagram and
  interfaces without changing them, which is what keeps the earlier design and the
  final code in agreement.
- **The agent stays in the implementation lane.** It does not redesign or re-plan.
  Keeping stages single-purpose is what makes the roles composable and the
  handoffs clean.

## How to invoke

Within Claude Code, with this repository open as the workspace, after a plan and
design exist:

```
> Use the engineer-agent to implement this plan and design: <paste the plan and design>
```

The agent's final message is the source code, ready to pass to the `qa-agent`.

## Continuous integration note

The engineer-agent is the stage that produces runnable source code. The `lint` and
`run-tests` CI gates were deferred earlier for exactly this reason: they become
meaningful once generated code lands in the repository. The agent file itself is
Markdown, so the existing `validate-agents` and `gitleaks` checks continue to
apply to this change.

## Mapping to MetaGPT

| nurutech-company | MetaGPT |
| --- | --- |
| `engineer-agent` | `Engineer` role |
| Code output format | `WriteCode` action, per-file code blocks |
| Seven standards | The WriteCode prompt attentions |
| Follow data structures and interfaces | Attention 4 of WriteCode |
