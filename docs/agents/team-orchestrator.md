# team-orchestrator — design notes

## Purpose

The `team-orchestrator` is the lead of the nurutech-company pipeline. It runs a
one-line product idea through the whole team end to end and returns a single
project package. It is the analogue of the team lead in a software company and of
MetaGPT's `Team` running an `Environment` of hired roles.

## Position in the pipeline

```
idea ──▶ team-orchestrator ──▶ [ pm ▶ architect ▶ planner ▶ engineer ▶ qa ] ──▶ project package
```

Unlike the five specialist agents, the orchestrator does not own a single stage. It
owns the sequence: it hands each stage's artifact to the next stage and gathers the
results.

## Input

- A one-line product idea (the requirement for the run).
- Optionally, an investment budget and a round limit that bound the run.

## Output contract

One project package with five fixed sections in order: `## Requirements`, `##
Design`, `## Plan`, `## Code`, `## Quality`. Each section holds the corresponding
specialist's artifact verbatim. The headings are fixed so the package can be split
downstream.

## Why this agent exists

MetaGPT coordinates roles through a shared message bus. A `Team` hires roles into an
`Environment`; `Team.run_project` publishes the human idea as one message; each role
watches for a message type and activates when it appears; `Team.run(n_round)` loops
the environment until it is idle or the budget runs out, then archives the result.
The pipeline order is emergent: it falls out of which action output each role
subscribes to.

Claude Code has no message bus. Subagents do not publish and subscribe; a lead
delegates to each specialist in turn and forwards the result. The
`team-orchestrator` is that lead. It flattens MetaGPT's publish-and-subscribe wiring
into an explicit, fixed sequence of delegations, which produces the same order the
`_watch` subscriptions would have produced.

MetaGPT has no CTO role. This agent is not a reimplementation of a role at all; it
is the Claude Code equivalent of the `Team` and `Environment` run machinery. It is
named `team-orchestrator` for that reason, rather than after a job title.

## Grounding in MetaGPT

The operating procedure is a faithful adaptation of `Team.run()` and the
`Environment` run loop, not an invented flow. The correspondence is recorded below.

| This agent | MetaGPT `Team` / `Environment` |
| --- | --- |
| Fixed set of specialist agents driven in turn | `Team.hire` adds roles to the `Environment` |
| Start from one published idea | `Team.run_project` publishes one human requirement `Message` |
| Each stage's artifact is the next stage's input | Each role `_watch`es the previous role's action output and activates on it |
| Run bounded by a round limit and budget; stop when idle | `Team.run(n_round)` loops `env.run()` until idle or `_check_balance` fails |
| Assemble the five artifacts into one package | The archive step that closes a run (`env.archive`) |

## Design decisions

- **Sequencing is explicit, not emergent.** With no message bus, the safest way to
  reproduce MetaGPT's order is to hard-code the stage sequence and the handoffs.
  This removes any dependence on subscription wiring that Claude Code does not have.
- **Artifacts are forwarded verbatim.** Each specialist is grounded in a specific
  MetaGPT action contract. Passing the previous artifact through unchanged is what
  lets the next specialist's contract line up with its real input.
- **The run is bounded.** A round limit and budget are carried over so a run has a
  defined stopping point, matching `Team.run(n_round)` and the budget check rather
  than looping indefinitely.
- **Not framed as a CTO.** MetaGPT has no CTO role. Presenting this agent as the
  `Team`/`Environment` runner keeps the grounding honest.

## How to invoke

Within Claude Code, with this repository open as the workspace:

```
> Use the team-orchestrator to build this idea: "a habit tracker for children aged 4 to 8"
```

The agent's final message is the assembled project package.

## Mapping to MetaGPT

| nurutech-company | MetaGPT |
| --- | --- |
| `team-orchestrator` | `Team` plus `Environment` run loop (no role equivalent) |
| One published idea | `Team.run_project` |
| Ordered stage delegation | The `_watch` subscription chain across roles |
| Round and budget bound | `Team.run(n_round)` and `_check_balance` |
| Assembled project package | `env.archive` at the end of a run |
