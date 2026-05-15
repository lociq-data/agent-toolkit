# SYSTEM_PROMPT.md Changelog

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
