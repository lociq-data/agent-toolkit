# Connecting an MCP Client to LOCIQ

LOCIQ exposes its property-intelligence tools through a Model Context Protocol
(MCP) server. Any MCP-compatible client can connect to it — you bring your own
client and your own language model; LOCIQ provides the tools and the data.

This document describes **LOCIQ's MCP surface**: the endpoint, how authentication
works, and what the server exposes. It does not describe how to configure any
particular client — consult your MCP client's own documentation for how to add a
remote MCP server. (A general starting point for MCP clients is
<https://modelcontextprotocol.io>.)

## What you need

- An MCP-compatible client (you supply this).
- A LOCIQ API key, for any tool beyond the open discovery tier. Get one at
  <https://lociq.ai/pricing>.

You do **not** need an LLM API key to *use LOCIQ's tools* — your client brings its
own model. LOCIQ only ever needs a LOCIQ key.

## Endpoint

```
https://mcp.lociq.ai/mcp
```

The server speaks MCP over streamable HTTP (POST). Requests need these headers:

```
Content-Type: application/json
Accept: application/json, text/event-stream
```

Responses are returned as Server-Sent Events — each response arrives as an
`event: message` line followed by a `data:` line carrying the JSON-RPC payload.

## Authentication

Authentication is a bearer token — your LOCIQ API key:

```
Authorization: Bearer YOUR_LOCIQ_API_KEY
```

**Discovery is open.** Listing the available tools (`tools/list`) works without a
key, so a client can connect and see the full tool catalog and schemas before
authenticating. This lets an agent discover and plan against LOCIQ's capabilities
before a key is supplied.

**Tool calls are tier-gated.** Calling a tool that requires a paid tier without a
sufficient key returns a structured upgrade signal rather than a generic error
(see "Tier gating" below).

## Rate limits and quota

Authenticated responses include headers that report your current limits and usage:

```
X-RateLimit-Limit       requests per minute allowed
X-RateLimit-Remaining   requests remaining in the current minute
X-Monthly-Quota         your monthly request allowance
X-Monthly-Used          requests used this month
```

A client can read these to pace its own usage.

## The tools

LOCIQ's MCP server exposes 13 tools:

| Tool | What it does |
|------|--------------|
| `find_property` | Look up a property by address or identifier |
| `get_property_details` | Full detail for a known property |
| `find_properties_in_area` | Properties within a geographic area |
| `find_businesses_nearby` | Businesses near a location |
| `get_area_stats` | Summary statistics for an area |
| `get_area_aggregate` | Aggregated metrics across an area |
| `get_owner_portfolio` | Properties held by a given owner |
| `find_related_properties` | Properties linked to a given one |
| `get_cluster` | An ownership cluster (related owners/properties) |
| `find_llc_properties` | Properties held under LLC ownership |
| `find_vacant_commercial` | Vacant commercial properties |
| `detect_changes` | Recent changes in an area or property set |
| `find_activity_signals` | Permit / activity signals |

Each tool's full input schema is available from `tools/list` — that is the
authoritative, always-current source for arguments. Treat the list above as
orientation; read the live schemas for exact parameters.

## Tier gating

Some tools require a paid tier. When a call is made without sufficient
authorization, the server returns a structured signal rather than failing
opaquely:

```json
{
  "error": "requires_upgrade",
  "current_tier": "anonymous",
  "tier_needed": "starter",
  "upgrade_url": "https://lociq.ai/pricing",
  "message": "This tool requires the starter tier or above. Upgrade to access."
}
```

A client encountering this knows exactly which tier is needed and where to
upgrade, and can surface that to the user rather than treating it as a hard error.

## Data honesty

LOCIQ is built to be explicit about the limits of its data rather than to imply
false completeness.

- **`get_cluster` returns a `data_quality` field** on each result. A healthy
  cluster reports `{"complete": true}`. A cluster whose membership could not be
  fully populated reports `{"complete": false, ...}` with the reason and the
  counts involved — so a client can tell a fully-resolved cluster from a partial
  one rather than treating an incomplete result as complete. This field is
  specific to `get_cluster`; it is not present on other tools.
- Numeric values such as assessed values may be returned as JSON strings; parse
  defensively.
- Coverage is currently nine U.S. states (see the LOCIQ documentation for the
  current list); a query against an area outside coverage returns empty rather
  than erroring.

## In short

Point your MCP client at `https://mcp.lociq.ai/mcp`, send the two required
headers, add `Authorization: Bearer YOUR_LOCIQ_API_KEY` for gated tools, and read
the live `tools/list` for exact schemas. Your client and your model are yours to
choose; LOCIQ supplies the tools.
