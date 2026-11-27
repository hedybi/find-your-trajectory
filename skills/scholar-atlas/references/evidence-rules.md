# Evidence rules

## Record what was actually inspected

Each source records its origin, URL, observation date and access level. Each evidence item points to a source and a precise locator (section, page, abstract, profile heading or timestamp), with a short note explaining the supported proposition. Quote only short necessary fragments; paraphrase the remainder. Public readability does not imply permission to redistribute a PDF. Store access URLs and licence statements separately; do not infer a licence.

Evidence grades apply to individual claims, not to a scholar or source as a whole:

| Grade | Meaning | Permitted presentation |
|---|---|---|
| `direct` | Inspected passage explicitly supports this proposition | Attribute the claim and retain its limits |
| `inference` | Analyst connects inspected facts; no source states the whole connection | Mark as interpretation, not author intent |
| Missing | No adequate accessible evidence | Leave unknown, omit the edge, or state a proposal |

A publisher metadata page can establish a title or DOI, not a detailed theoretical mechanism. An abstract supports only what it says. A bibliography proves citation, not acceptance, development or mentorship. Secondary histories can orient a search; prefer the theorist’s own text for a proposition and preserve disagreement among accounts.

## Edges and contribution claims

| Edge type | Minimum support |
|---|---|
| `direct_citation` | Citing text or reference list identifying the cited work |
| `conceptual_development` | Passage explaining the change; if reconstructed by the atlas, label inference |
| `application` | Focal work demonstrates how a concept is operationalized |
| `comparison` | Sources for both sides and an explicit analyst-comparison label |
| `mentorship` | Explicit biographical evidence of supervision/mentorship; never inferred from citation |

Avoid connecting every theory to a single famous founder. The history of a term, mechanism and discipline may differ. Separate the author’s novelty claim from the atlas’s assessment and from a field-wide consensus. `theoretical_innovation` requires a comparison scope and attribution; the validator cannot decide whether that assessment is intellectually convincing.

## Work/version identity

Normalize DOI prefixes (`doi:`, `https://doi.org/`, `http://dx.doi.org/`), whitespace and case. Never delete meaningful DOI punctuation. Repeated records with the same normalized DOI are duplicates for review. Group preprint, accepted manuscript, online-first, issue and revised chapter versions only with identity evidence. A translation, new edition or substantially revised article may need a separate work plus an explicit relationship. DOI absence is normal and is not a reason to fabricate one.

Report both distinct-work and version counts. If identity is unresolved, retain separate work records with an explicit unresolved relationship and do not silently present a settled unique-work total. The schema’s declared counts are checked structurally; the coverage note must explain the unresolved count.

## Research-to-practice claims

`documented_collaboration` requires explicit evidence of the parties and activity. `reported_outcome` requires an outcome-specific source, attribution and time period; distinguish self-report from independent assessment. A project proposal, grant, pilot or policy citation does not prove realized impact. Label causal claims carefully: temporal sequence and adoption do not establish causation.

An `interpretation` can link research to a practical problem but cannot assert a partnership. A `proposal` is a possible next step; include the verification or action still needed. Missing evidence must never be repaired by switching the label to “documented”.

## Stop conditions and handoff

Stop a branch when it explains the target mechanism sufficiently for the user’s question, further retrieval is inaccessible, or a material claim requires evidence unavailable within scope. State the unresolved issue and specific next source needed. Do not repeatedly retry blocked access or seek private accounts without authorization. Export only permitted material; remove private paths, credentials, account identifiers and unrelated documents from shareable artifacts.
