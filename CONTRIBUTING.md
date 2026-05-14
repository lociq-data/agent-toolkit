# Contributing to the LOCIQ Agent Toolkit

This document explains how to contribute to this toolkit and what's in scope. Read before filing issues or pull requests.

## What this repo is

The LOCIQ agent toolkit ships three artifacts:

1. `prompts/SYSTEM_PROMPT.md` — the conceptual document teaching an agent how to think about LOCIQ data.
2. `reference/agent.py` — a minimum-viable Python reference implementation connecting an agent to LOCIQ's MCP server.
3. `cookbook/` — complete workflow recipes an agent can read and execute.

The repo is not a Python SDK, an agent framework, or a hosted service. The reference implementation is intentionally small (approximately 150 lines, heavily annotated) and is meant to be read, understood, and adapted. The cookbook entries are not casual examples — they are the proven workflows that LOCIQ supports.

## How to contribute

### Reporting issues

File issues for:

- Bugs in the reference implementation or cookbook entries
- Documentation errors in SYSTEM_PROMPT.md or cookbook entries
- Missing workflows you would like to see added to the cookbook
- Edge cases or failure modes you encountered that the gotchas section of a cookbook entry should warn about

Include enough detail to reproduce the issue. For workflow requests, describe the agent's task in concrete terms: what is the user asking, what is the expected output, what data does the agent need to access.

### Pull requests

Pull requests are welcome for:

- Fixes to bugs in the reference implementation or cookbook entries
- Improvements to documentation clarity
- Additional language reference implementations are not in scope at v1 (TypeScript reference deferred per design plan)
- New cookbook entries should be discussed in an issue first to confirm scope and tier alignment before code is written

Pull requests must follow the voice conventions:

- README and cookbook entry intros use marketing-aware first-person voice
- SYSTEM_PROMPT.md, setup guides, reference implementation comments, and cookbook code/steps use reference-doc neutral voice

Cookbook entries follow a fixed four-section structure: problem statement, complete code (no placeholders; runnable as written), expected output, gotchas (data gaps, tier requirements, common failure modes).

## What LOCIQ does and does not do

LOCIQ provides structured property data and standardized tools accessible via API and MCP. Customization — composing tools into workflows specific to a customer's domain — is the customer's agent's job.

**LOCIQ does not accept custom-development requests.** If your use case is not covered by the standard product plus your own agent, the resolution is one of:

1. A cookbook entry exists for it (or should exist; file an issue requesting one)
2. The standard product has a gap that should be fixed for everyone (file an issue describing the gap)
3. The use case is out of scope for LOCIQ

There is no fourth option. LOCIQ does not provide consulting, managed agent configurations, or paid integration work. This is a deliberate choice: the cookbook is the substitute for custom development, and keeping LOCIQ focused on data and tools (rather than services) is how the product compounds value across all customers.

If you are unsure whether your need fits the cookbook model, file an issue describing the workflow and we will respond with one of the three resolutions above.

## License

Contributions to this repository are licensed under the MIT License (see LICENSE).
