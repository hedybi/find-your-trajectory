---
name: scholar-atlas
description: Build evidence-linked guides to a scholar’s theoretical development, foundations, bilingual concepts, related active scholars, and research-to-practice connections. Use for a scholarly overview or theory map, not routine citation formatting.
---

# Find Your Trajectory — Scholar Edition

This is the first, scholar-focused edition of Find Your Trajectory. The portable skill identifier remains `scholar-atlas`; personal trajectory planning is a possible future extension, not a current capability.

Turn a bounded publication corpus into an understandable, inspectable account of how a scholar thinks. The central artifact is a network of **claims with evidence**, not a chronological list of names. A theory tree is a reading interface; intellectual history may have parallel roots, loops, and disputed connections.

## Establish the corpus

Start with the scholar’s official profile, publication list and stable identifiers. Resolve namesakes using affiliation, subject and coauthors. Record the requested scope and actual coverage: identified works, checked versions, full texts read, abstracts only, inaccessible items and search date. Never promise an exhaustive web search or claim to have read inaccessible references.

Maintain one work record per intellectual work and separate publication versions. Online-first and issue dates usually describe versions of one work; different DOIs alone do not establish different works. Compare titles, author order, abstract/content and publisher version statements before grouping. Preserve uncertain identity as unresolved, with reasons. Read [schema.md](references/schema.md) when creating the machine-readable atlas.

## Build the explanatory map

Read [evidence-rules.md](references/evidence-rules.md) before making ancestry, novelty or impact claims. For each central paper, identify its problem, cited mechanism, empirical operation and claimed contribution. Read the relevant passages of foundational sources, not every item in every reference list. Follow another citation layer when it resolves a disputed mechanism or explains a major conceptual shift; otherwise record the boundary and stop.

Build routes with as many **supported** steps as exist:

> Discipline and classic problem → later author’s actual development → focal scholar’s use → contribution and limits.

Do not invent an intermediate theorist to make a tidy route. Distinguish direct citation, documented conceptual development, application, interpretive comparison and actual mentorship. Citation is not endorsement or intellectual descent. Date order is not a causal connection. An interpretive route must visibly say “interpretive comparison / 解读性比较”.

Explain each major module in three depths:

1. A one-sentence everyday explanation and a small navigable overview.
2. A bilingual concept card: original term, Chinese equivalent, definition, mechanism, example and common misreading. Keep competing translations visible when they change meaning.
3. An expandable evidence trail: source passage location, what it supports, access limitation, and the focal scholar’s empirical application, mechanism extension, concept proposal or theoretical innovation. Strong novelty claims need a stated comparison scope; otherwise identify them as the author’s claim or the atlas’s interpretation.

Follow the user’s desired depth and format; do not force a website or fixed number of modules. Preserve paper-level details in an expandable view or companion file so the overview remains legible.

## Connect the field and practice

Select related active scholars because of a documented citation, coauthorship, shared research question or a labelled comparison—not a ranking. Verify current affiliation and at least one dated recent research activity from official sources. State the observation date; “active” is bounded by the chosen recency window. An official profile without recent work is insufficient evidence of current activity.

For industry, policy and research connections, separate **documented collaboration**, **reported outcome**, **interpretation**, and **proposal**. A topic match, employer logo, grant or interview does not by itself prove adoption, partnership or causal impact. Keep future collaboration ideas labelled as proposals even if the user asks for persuasive language. Do not contact people, publish, or create a remote repository unless the user authorizes that action.

## Produce and check

Use portable Markdown, JSON, SVG or HTML as appropriate. If the user requests a website and a Sites skill is available, read and use that skill for implementation/publication; this skill has no proprietary plugin dependency. Keep content usable without hosting.

Validate structured output with:

```bash
python3 scripts/validate_atlas.py /path/to/atlas.json
```

Resolve validation failures, then inspect the actual claims and visual labels: the validator checks structure and evidence categories, not the truth of cited passages. Compare displayed counts against distinct works and versions. Report missing coverage and material uncertainty alongside the result, without implying universal completeness.

For a self-contained example see the repository’s `examples/synthetic-atlas.json`; all people and excerpts there are fictional. For independent behavioral acceptance, use `evals/forward-test.md` with its separate raw source packet. Do not use synthetic examples as real scholarly evidence.
