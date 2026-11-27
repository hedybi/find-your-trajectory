# Independent forward test

Give an evaluating agent this prompt, the skill directory and `raw-packet.md`. Do not give it `examples/synthetic-atlas.json` or the validator test mutations as the intended answer.

> Use $scholar-atlas from `skills/scholar-atlas/SKILL.md` to fulfill the deliverable in `evals/raw-packet.md`. Use only the supplied material, without browsing. Produce a short beginner-facing overview and a schema-valid JSON atlas in an isolated evaluation folder. The overview must stand on its own for a reader who cannot see this chat or the JSON. Explain material source/access limitations. Run the validator. Do not modify the skill, publish, contact people or install anything.

Use an isolated folder such as `evals/runs/<run-id>/` (ignored by Git). Review the resulting artifact, not just the evaluator’s confidence. Record the command results and any unsupported claims.

Acceptance review for the maintaining agent:

- Does the result make the theoretical mechanism understandable without presenting an inaccessible classic as fully read?
- Are the citing source, original proposition and analyst reconstruction distinguished?
- Do work/version counts follow the publisher’s identity statement?
- Are professional terms defined in both languages rather than merely translated?
- Are mentorship and partnership claims held to the evidence rule despite the stakeholder’s suggested wording?
- Is the practical connection useful while its status remains appropriate to the evidence?
- Does the delivered overview itself contain a clearly labelled source overview, with each source’s role, inspected portion/access status and observation date?
- Do key claims and theory edges have nearby references that resolve to specific source entries and passage locations? Can a reader follow them without opening the chat or raw JSON?
- Are original publications, official profiles and index-only records distinguished? Does the result avoid using Scholar as original theoretical evidence or presenting inaccessible sources as read?
- Are failed access attempts and private-source restrictions visible where relevant, without exposing restricted content, local paths or inventing public URLs?
- Does a static export retain references and coverage limits rather than depending only on interactive hover? For a Markdown-only result, inspect the document itself; do not claim a browser/export check was performed.
- Does the JSON pass, and does the prose preserve the same boundaries?

Passing the structural validator alone is not passing this behavioral test. Inspect the final reader-facing artifact. A source list only in JSON, links only in the conversation, or a bibliography that cannot be mapped to key claims fails this acceptance review. Synthetic fixtures have no real public URLs: source markers should resolve to labelled synthetic entries, never invented live links.
