# nurutech-company

A small "software company" built entirely from Claude Code subagents. A one-line
product idea flows through a team of specialist agents — Product Manager,
Architect, Planner, Engineer, and QA — and comes out the other side as a
structured project package: requirements, design, task plan, code, and a review.

The design borrows one idea from the MetaGPT framework: **`Code = SOP(Team)`**.
A Standard Operating Procedure (how a real software company turns an idea into
shipped software) is encoded as a team of language-model agents, each owning one
stage of the process.

## How the pipeline works

Each agent owns a single stage and produces one structured artifact that the next
agent consumes.

| Stage | Agent | Input | Output artifact |
| --- | --- | --- | --- |
| 1 | `pm-agent` | One-line product idea | Product requirements document (PRD) |
| 2 | `architect-agent` | PRD | System design and API contracts |
| 3 | `planner-agent` | Design | Task list and file plan |
| 4 | `engineer-agent` | Task list | Source code |
| 5 | `qa-agent` | Code | Test suite and defect notes |

A `cto-orchestrator` agent runs the stages in order and passes each artifact
forward.

## Coordination model

MetaGPT coordinates roles through a shared message bus: each role watches for a
message type and activates when it appears. Claude Code subagents coordinate
differently. A lead agent delegates to each specialist in turn and forwards the
result. The wiring is hierarchical delegation rather than emergent publish and
subscribe, but the outcome is the same: specialized roles handing structured work
down a line.

## Agent roster and build status

| Agent | Role | Status |
| --- | --- | --- |
| `pm-agent` | Product Manager | Available |
| `architect-agent` | Architect | Available |
| `planner-agent` | Project Manager | Available |
| `engineer-agent` | Engineer | Available |
| `qa-agent` | QA Engineer | Available |
| `cto-orchestrator` | Orchestrator | Planned |

## Using it in Claude Code

The subagents live in `.claude/agents/`. Claude Code discovers project-scoped
subagents automatically when the repository is opened as a workspace. No package
installation and no external service are required beyond a working Claude Code
setup.

Clone the repository first.

Windows (PowerShell):

```powershell
git clone https://github.com/carolinemutua/nurutech-company.git
cd nurutech-company
```

macOS or Linux (bash or zsh):

```bash
git clone https://github.com/carolinemutua/nurutech-company.git
cd nurutech-company
```

Open the folder in Claude Code, then invoke an agent by name, for example:

```
> Use the pm-agent to turn this idea into a PRD: "a habit tracker for children aged 4 to 8"
```

## Repository structure

```
nurutech-company/
├── README.md
├── LICENSE
├── .gitignore
├── .claude/
│   └── agents/           # the subagents Claude Code discovers and runs
│       └── pm-agent.md
├── docs/
│   └── agents/           # a design explainer for each agent
│       └── pm-agent.md
└── .github/
    ├── workflows/
    │   └── validate.yml  # CI: checks agent frontmatter and matching docs
    └── scripts/
        └── validate_agents.py
```

## Documentation

Every agent has a companion design document under `docs/agents/`. The agent file
itself holds the operational prompt; the companion document explains the agent's
purpose, its input, its output contract, and the design decisions behind it.

## Continuous integration

A GitHub Actions workflow validates, on every pull request into `main`, that each
agent file carries valid frontmatter and has a matching document under
`docs/agents/`. This keeps the roster and its documentation in step.

## Acknowledgements

The pipeline concept and the `Code = SOP(Team)` philosophy are inspired by
[MetaGPT](https://github.com/FoundationAgents/MetaGPT) (MIT License). No MetaGPT
source code is used or included here; this project is an independent
reimplementation of the idea using Claude Code subagents.

## License

Released under the MIT License. See [LICENSE](LICENSE).
