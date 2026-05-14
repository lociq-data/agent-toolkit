# LOCIQ Agent Toolkit

Build AI agents that answer questions about U.S. property data — ownership, businesses, parcels, and the relationships between them.

This toolkit is for developers and AI engineers using [LOCIQ](https://lociq.ai) as a data source for their agents. It ships:

- **A system prompt** that teaches an agent how to think about LOCIQ data — confidence tiers, evidence model, the cluster graph, and how to compose tools into workflows
- **A Python reference implementation** that connects an agent to LOCIQ's MCP server in roughly 150 lines, heavily annotated as a teaching artifact
- **A cookbook** of complete, runnable workflows — investor research, market intelligence, evaluation harnesses — that your agent can read and execute

You bring your own LLM (Claude, GPT, Gemini, whatever). You bring your own agent framework or write the loop yourself. LOCIQ provides the data, the tools, and the workflows. Your agent does the rest.

## Status (2026-05-13)

This repo is being built in the open. **Today there's scaffolding and the documents you're reading.** SYSTEM_PROMPT.md and the Python reference implementation are landing in coming days; cookbook entries follow. Star the repo to track. File an issue if you want a specific workflow in the cookbook.

## What's in here

    agent-toolkit/
    ├── prompts/           SYSTEM_PROMPT.md — the conceptual document teaching agents how to think about LOCIQ data
    ├── reference/         agent.py — minimum-viable Python agent connecting to LOCIQ's MCP server
    └── cookbook/          Workflow recipes: problem statement + complete code + expected output + gotchas

## Quickstart (coming soon)

The quickstart below describes the target shape. It does not run today.

    git clone https://github.com/lociq-data/agent-toolkit.git
    cd agent-toolkit
    pip install -r reference/requirements.txt
    export LOCIQ_API_KEY=your_key
    export ANTHROPIC_API_KEY=your_key
    python reference/agent.py "Find every property owned by Big Sky Properties LLC and its related entities"

The reference implementation is intentionally small. Read it, understand it, then build the agent you actually need.

## Why this exists

LOCIQ's relationship graph — portfolios, LLC clusters, business chains, build-to-rent nexuses — is the moat. The graph is queryable through standard API endpoints, but agents trip over the shape: which tool to call first, how to compose tools, what the confidence tiers mean, when "I don't know" is the right answer.

This toolkit is the answer to that. The system prompt teaches the shape. The reference implementation shows the integration. The cookbook ships proven workflows so your agent doesn't have to discover them.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and pull requests welcome; LOCIQ does not accept custom-development requests — read CONTRIBUTING.md before filing a feature request.

## License

MIT — see [LICENSE](LICENSE).
