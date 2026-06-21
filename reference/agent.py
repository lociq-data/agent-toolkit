"""
LOCIQ MCP reference agent -- a minimal, provider-neutral example.

This is a teaching artifact, not a framework, SDK, or production agent. It
demonstrates the four-part pattern for connecting any LLM to LOCIQ's MCP
tools:

    1. Connect to the LOCIQ MCP server (streamable-http transport)
    2. Translate MCP tool schemas to the LLM's tool-calling format
    3. Run the agent loop (query -> tool calls -> results -> repeat)
    4. Return the final answer

LOCIQ requires only a LOCIQ API key. This script additionally needs an LLM
key because it IS an agent -- it brings its own LLM. That key is yours and
your provider's, never LOCIQ's.

This example drives the agent with one LLM provider for illustration only.
LOCIQ is provider-neutral (section 22); the LLM is entirely your choice. To
use a different provider, replace call_llm() -- see README.

Usage:

    export LOCIQ_API_KEY=your_lociq_key   # the ONLY key LOCIQ requires
    export LLM_API_KEY=your_llm_key       # your own provider key (this script only)
    python reference/agent.py "Find every property owned by Big Sky Properties LLC"

LOCIQ_API_KEY is the ONLY key LOCIQ requires -- the MCP server is tools behind
bearer auth; LOCIQ never sees or needs an LLM key. LLM_API_KEY is your own
provider's key, needed ONLY to run THIS example script. A customer who points
an existing MCP client at LOCIQ needs no LLM key for LOCIQ at all.
"""

import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# --- Configuration -----------------------------------------------------------

LOCIQ_MCP_URL = "https://mcp.lociq.ai/mcp"

# Safety bound on the tool-call loop. Prevents runaway loops from a model
# that never stops requesting tools.
MAX_TOOL_TURNS = 10

# The conceptual document teaching the LLM how to interpret LOCIQ data
# (confidence, evidence, tiers, the cluster graph, when to say "I don't know").
SYSTEM_PROMPT_PATH = (
    Path(__file__).resolve().parent.parent / "prompts" / "SYSTEM_PROMPT.md"
)

# --- Helpers -----------------------------------------------------------------


def load_system_prompt() -> str:
    """Load the LOCIQ system prompt from prompts/SYSTEM_PROMPT.md.

    This is the epistemic-honesty mechanism: LOCIQ's conventions (confidence
    tiers, tier-gating behavior, evidence model, and the honesty principle)
    are stated once in prose and inherited by whatever model is used. The
    prompt teaches what the data means -- it does not prescribe agent
    behavior or name any LLM provider."""
    try:
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return (
            "LOCIQ is a property intelligence graph. Interpret responses "
            "honestly: surface confidence tiers, acknowledge coverage gaps, "
            "and do not claim more than the data supports."
        )


def require_env(name: str) -> str:
    """Return an environment variable or exit with a clear message."""
    value = os.environ.get(name, "")
    if not value:
        sys.exit(f"Missing environment variable: {name}")
    return value


def to_llm_tools(mcp_tools: list) -> list[dict]:
    """Translate MCP tool schemas to the LLM's tool-calling format.

    This is the glue between the MCP tool surface and the LLM. The format
    below matches the example provider (Anthropic). If your provider's
    tool-schema shape differs, adapt this function alongside call_llm()."""
    return [
        {
            "name": tool.name,
            "description": tool.description or "",
            "input_schema": tool.inputSchema,
        }
        for tool in mcp_tools
    ]


# =============================================================================
# PROVIDER SWAP POINT -- the ONLY provider-specific code in this file.
#
# This example uses Anthropic's Claude for illustration only. LOCIQ is
# provider-neutral and prefers no provider (DECISIONS.md section 22). To use
# OpenAI, Gemini, a local model, or any other provider: replace the body of
# call_llm() below (and adjust to_llm_tools() if the tool-schema shape
# differs). Everything else in this file is provider-neutral.
# See README for provider parity notes.
# =============================================================================

import anthropic  # noqa: E402 -- provider-specific; lives here, not at top

LLM_MODEL = "claude-sonnet-4-6"


def call_llm(
    system_prompt: str, messages: list[dict], tools: list[dict]
):
    """Send a request to the LLM and return the raw response.

    All provider-specific logic is isolated here. The rest of the agent loop
    interacts with the response through .content blocks (.type, .text for
    text; .id, .name, .input for tool_use) and .stop_reason."""
    client = anthropic.Anthropic(api_key=require_env("LLM_API_KEY"))
    return client.messages.create(
        model=LLM_MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=messages,
        tools=tools,
    )


# --- Agent loop --------------------------------------------------------------


async def run_agent(query: str) -> str:
    """Connect to LOCIQ's MCP server and run the agent loop.

    The loop is the heart of an MCP agent: send the user query to the LLM
    with the available tools, execute any tool calls the LLM requests, feed
    results back, and repeat until the LLM produces a final text answer.

    Tier-gate markers (requires_upgrade) and confidence/data_quality fields
    pass through to the model unmodified -- they are not hidden or filtered,
    so the model can reason about limits and evidence honestly."""

    headers = {"Authorization": f"Bearer {require_env('LOCIQ_API_KEY')}"}
    system_prompt = load_system_prompt()

    async with streamablehttp_client(LOCIQ_MCP_URL, headers=headers) as (
        read,
        write,
        _,
    ):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tool_list = (await session.list_tools()).tools
            tools = to_llm_tools(tool_list)

            messages = [{"role": "user", "content": query}]

            for _turn in range(MAX_TOOL_TURNS):
                response = call_llm(system_prompt, messages, tools)

                # Append the assistant's full response as a conversation turn.
                messages.append(
                    {"role": "assistant", "content": response.content}
                )

                # If the model produced a final answer (no tool calls),
                # collect text blocks and return.
                if response.stop_reason != "tool_use":
                    return "\n".join(
                        block.text
                        for block in response.content
                        if block.type == "text"
                    )

                # Execute each tool call the model requested.
                tool_results = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue
                    result = await session.call_tool(
                        block.name, block.input or {}
                    )
                    text = "\n".join(
                        part.text
                        for part in result.content
                        if hasattr(part, "text")
                    )
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": text,
                        }
                    )

                # Feed all tool results back as a single user turn.
                messages.append({"role": "user", "content": tool_results})

    return "Reached tool-turn limit without a final answer."


# --- Entry point -------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: python reference/agent.py "your question"')
    print(asyncio.run(run_agent(sys.argv[1])))
