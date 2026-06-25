# SYSTEM_PROMPT.md Changelog

## 2026-06-25 — coverage update + honesty markers

Three drift fixes against the served MCP surface:

1. Coverage corrected: eight → nine states. The prompt understated coverage; served reality is nine (AZ, CO, FL, ID, IN, MT, NC, NE, WA). Whether a state was newly added or simply miscounted in the prior draft is not asserted.
2. `data_quality` field documented (Section 6). `get_cluster` results carry `data_quality: {complete: true/false}` — the first per-result honesty field, landed in §154 (cr_app). Agents should treat incomplete clusters as partial, not empty.
3. `requires_upgrade` response shape documented (Section 10). The structured tier-gate signal (`error`, `current_tier`, `tier_needed`, `upgrade_url`) is now described with a concrete example so agents can handle tier gating programmatically rather than treating it as an opaque error.

Classification of change: additive. No existing fields renamed or removed. Agents that did not previously handle `data_quality` or `requires_upgrade` will now have documentation for signals they were already receiving.

## 2026-05-14 — initial draft

First public draft of the LOCIQ agent system prompt. Twelve sections, narrative structure, approximately 3,200 words.

Section structure:

1. What LOCIQ is and what this prompt covers
2. Tool categories
3. The shape of a property
4. Confidence and evidence
5. primary_label
6. Owners, ownership, and the cluster graph
7. Businesses and how they attach to places
8. Activity signals
9. Coverage
10. Tier gating
11. The map and deep linking
12. When to say "I don't know"

Design source: docs/agent-toolkit-plan.md Q6-Q11 (locked 2026-05-13) and DECISIONS.md §46 Q46-8 (locked 2026-05-14).

Voice: declarative, descriptive with focused prescriptive interjections at the epistemic gates, no second-person address, always inline code formatting for field names and identifiers. Teaches what LOCIQ data means and what claims it does and does not support. Does not prescribe agent behavior — communication, tone, and presentation are the customer's agent's territory.

Reflects the M:M cluster membership shape per DECISIONS.md §44 (clusters array on owner/business endpoints, via_clusters array on properties from cluster-traversal queries).

Pre-commit verification pass against cr_app codebase preceded this draft. Six factual claims were revised to match implementation reality: activity signal field names (issued_date, activity_type, valuation rather than date, type, value), confidence thresholds (0.80 rather than 0.85 at the confirmed/probable boundary), cluster type descriptions (LLC, business chain, B2R nexus revised to match build-clusters.js logic), tier boundaries (revised to match auth-middleware.js implementation), and coverage endpoint reference (softened to not name a specific endpoint that does not yet exist). Section 11's URL parameter shapes remain as design intent per DECISIONS.md §46 Q46-2; URL handling lands with the map UI build-out.

## 2026-05-15 — cluster rename: b2r_nexus → mixed_property_owner

The fourth cluster type renames from `b2r_nexus` to `mixed_property_owner`, with cluster ID prefix changing from `B2R_` to `MIXED_`. Per DECISIONS.md §47 (cr_app, 2026-05-14): the original name "B2R" (build-to-rent) carried industry-specific meaning (institutional single-family rental operators) that the cluster's actual detection — an address-pattern signal between owner mailing address and residential property addresses — did not deliver. The new name describes what the code actually detects.

Sections updated:
- Section 6 (Owners, ownership, and the cluster graph): fourth cluster type description, opening paragraph cluster-type list, ASPEN PARTNERS LLC JSON example (cluster_id and cluster_type), closing-paragraph cluster footprint reference.

Code cascade landed in cr_app commit 690b070 (2026-05-14): `build-clusters.js` writes the new cluster_type and ID prefix; OpenAPI spec enum updated; CLI flag renamed to `--type mixed_property_owner`; tests pass.

Compatibility note: Existing rows in `relationship_clusters` with `cluster_type = 'b2r_nexus'` are not migrated. The CASCADE pattern from DECISIONS.md §44 handles cleanup at the next per-state rebuild. Agents querying LOCIQ during the transition window may see both old and new cluster_type values; the new value is canonical from this commit forward.

Classification of change: potentially breaking. Agents that hardcoded the old `cluster_type` value or `B2R_` prefix in their parsing logic will need to update.
