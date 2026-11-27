# Find Your Trajectory — Scholar Edition data contract, version 1

The Python validator is the executable contract; this document explains its semantics. All IDs are globally unique strings. All references resolve within the document. `bi` means an object with nonempty `en` and `zh` strings. This contract uses Chinese–English concept cards; adapt the schema explicitly for another language pair rather than filling a language field with untranslated text.

Required top-level fields:

| Field | Shape |
|---|---|
| `schema_version` | `1` |
| `synthetic` | Boolean; true means the entire example is fictional |
| `scholar` | `{id, name: bi}` |
| `coverage` | `{as_of: YYYY-MM-DD, scope, limitation, work_count, version_count}` |
| `sources` | List of source records |
| `evidence` | List of evidence records |
| `works` | List of intellectual works and versions |
| `theories` | List of explanatory modules |
| `terms` | List of bilingual term cards |
| `edges` | List of typed relationships |
| `contributions` | List of paper-level contribution claims |
| `related_scholars` | List; may be empty if outside scope or unverified |
| `impact_claims` | List; may be empty |

Source: `{id, kind, access, url, checked_at, licence}`. `kind` is `primary_publication`, `official_profile`, `official_project`, `secondary`, or `synthetic`. `access` is `fulltext`, `abstract`, `metadata`, `unavailable`, or `synthetic`. A real source requires an HTTP(S) URL; a fictional source requires `kind/access: synthetic` and `url: null`. `licence` may be null (unknown). An observed licence is not a grant of rights over all linked materials.

Evidence: `{id, source_id, locator, grade, scope, note}`. `grade` is `direct` or `inference`. `scope` is `bibliographic`, `citation`, `theoretical`, `biographical`, `activity`, `mentorship`, `collaboration`, `outcome`, or `interpretation`. The note describes exactly what the inspected source supports. Optional short `excerpt` text does not substitute for a locator. Fictional excerpts must only appear in synthetic datasets.

Work: `{id, title, author_names, year, evidence_refs, identity_status, versions}`. `identity_status` is `resolved` or `unresolved`. Each version is `{id, kind, date, doi, evidence_refs}`. `date` may be null or an ISO date; `doi` may be null or a DOI. Multiple versions require `identity_note` and `identity_evidence_refs`. Unresolved identity requires `identity_note`; explain its effect on totals in `coverage.limitation`. Version dates do not replace the work’s display year. Record pages/volume separately when verified; do not fabricate them to fill a template.

Theory: `{id, label: bi, discipline: bi, authors, year, proposition: bi, mechanism: bi, misreading: bi, evidence_refs}`. Authors is a list of names; year may be null when uncertain. A module can represent a later development, not necessarily an origin claim.

Term: `{id, theory_id, term: bi, definition: bi, example: bi, evidence_refs}`. Explanatory examples are illustrations, not additional empirical findings.

Edge: `{id, source, target, type, basis, label: bi, evidence_refs}`. Nodes may be theories, works, the focal scholar or related scholars. `type` is defined in evidence-rules; `basis` is `explicit` or `inferred`. `comparison` must be inferred and its label must say “comparison / 比较”. `mentorship` and `direct_citation` must be explicit. A direct-citation arrow points **from citing to cited**; other arrows follow their label. The UI must explain arrow semantics and must not relabel a comparison as influence.

Contribution: `{id, work_id, kind, status, claim: bi, evidence_refs}`. `kind` is `empirical_application`, `mechanism_extension`, `concept_proposal`, or `theoretical_innovation`; `status` is `evidenced` or `inference`. Innovation additionally requires `novelty_scope` and `attribution`. “Evidenced” means the claim has direct support, not that originality is universally accepted.

Related scholar: `{id, name: bi, affiliation, activity, activity_date, as_of, evidence_refs, relation: bi}`. Both dates use YYYY-MM-DD; the activity cannot postdate the observation. Require direct official evidence for current biographical information and dated activity. State the recency window in coverage; the validator checks dates but cannot decide what counts as recent for every discipline.

For an online-first article and issue assignment with the **same DOI**, use one version record with optional `online_date` and `issue_date` rather than repeating the DOI. The version count counts these consolidated records, not every bibliographic event. Separate manuscript and publisher versions may have different DOIs or no DOI; their identity still requires evidence.

Impact claim: `{id, label: bi, status, relation, evidence_refs}`. Allowed pairs:

- `evidenced` + `documented_collaboration` (direct collaboration evidence)
- `evidenced` + `reported_outcome` (direct outcome evidence)
- `inference` + `interpretation` (supporting references)
- `proposal` + `proposal` (`next_step` required; references optional)

For documented relations, include `parties` (at least two) or `period` and `attribution` for outcomes. Structural validation cannot detect a misleading paraphrase, an inaccessible source disguised as inspected, or a fabricated partnership hidden inside a proposal label. Human/source review remains necessary.
