# qa-agent — design notes

## Purpose

The `qa-agent` is the fifth and final stage of the nurutech-company pipeline. It
converts source code into a comprehensive test suite. It is the analogue of the QA
Engineer role in a software company and of the `WriteTest` action in MetaGPT.

## Position in the pipeline

```
source code ──▶ qa-agent ──▶ test suite and defect notes
```

The qa-agent closes the pipeline. Its test suite and notes are the quality record
for the project and stand on their own.

## Input

- The source code from the engineer-agent.
- The system design the code implements, whose data structures and interfaces the
  tests must respect.

## Output contract

A sequence of `## Test: tests/test_<file>` sections, one per source file, each
containing a complete test module, followed by a `## Test notes` section listing
edge cases and observed defects. This mirrors MetaGPT's WriteTest output, which
writes one `unittest` test file per source file under a `##`-split section. The
headings are fixed because downstream tooling parses them.

## Grounding in MetaGPT

The output format and standards are a faithful adaptation of MetaGPT's WriteTest
action, not an invented format. The correspondence is recorded below.

| This agent | MetaGPT `WriteTest` |
| --- | --- |
| One `## Test: tests/test_<file>` per source file | The action writes one test file per code file under review |
| Standard framework, PEP8, maintainable | Attention on PEP8-compliant, well-structured tests for the unit-testing framework |
| Comprehensive, reusable coverage | The requirement for a complete, robust, reusable suite |
| `##` section headings before each test | Attention 1 (use `##` to split sections) |
| Defaults, strong types, explicit variables | Attention 2 |
| Follow data structures and interfaces, do not change design | Attention 3 |
| `## Test notes` on edge cases and failures | "Think before writing: what edge cases could exist, what might fail" |
| Completeness check | "Carefully check you don't miss any necessary test cases" |

The QA Engineer role's goal ("write comprehensive and robust tests to ensure codes
will work as expected without bugs") and constraints ("conform to a standard like
PEP8, be modular, easy to read and maintain; use same language as user
requirement") are carried over into the Role and Constraints text of the agent
file.

## Design decisions

- **One test file per source file.** Matching MetaGPT's per-file test format keeps
  coverage traceable to the code and keeps each test module complete.
- **The design is authoritative for the tests too.** Tests validate the code
  against the design's interfaces rather than inventing new behaviour, which keeps
  the whole pipeline internally consistent.
- **A defect-notes section is included.** MetaGPT's QA loop also runs and debugs
  the code (RunCode, DebugError). In a prompt-only Claude Code agent there is no
  execution sandbox, so the "think about what might fail" step is captured as
  written test notes rather than an execution log.

## How to invoke

Within Claude Code, with this repository open as the workspace, after code exists:

```
> Use the qa-agent to write tests for this code: <paste the code and design>
```

The agent's final message is the test suite and defect notes.

## Mapping to MetaGPT

| nurutech-company | MetaGPT |
| --- | --- |
| `qa-agent` | `QaEngineer` role |
| Test output format | `WriteTest` action, per-file `unittest` modules |
| Seven standards | The WriteTest prompt attentions |
| Test notes | The QA loop's run-and-debug intent (RunCode, DebugError) |
