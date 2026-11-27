# Independent forward test

Give an evaluating agent this prompt, the skill directory and `raw-packet.md`. Do not give it `examples/synthetic-atlas.json` or the validator test mutations as the intended answer.

> Use $scholar-atlas from `skills/scholar-atlas/SKILL.md` to fulfill the deliverable in `evals/raw-packet.md`. Use only the supplied material, without browsing. Produce a short beginner-facing overview and a schema-valid JSON atlas in an isolated evaluation folder. Explain material source/access limitations. Run the validator. Do not modify the skill, publish, contact people or install anything.

Use an isolated folder such as `evals/runs/<run-id>/` (ignored by Git). Review the resulting artifact, not just the evaluator’s confidence. Record the command results and any unsupported claims.

Acceptance review for the maintaining agent:

- Does the result make the theoretical mechanism understandable without presenting an inaccessible classic as fully read?
- Are the citing source, original proposition and analyst reconstruction distinguished?
- Do work/version counts follow the publisher’s identity statement?
- Are professional terms defined in both languages rather than merely translated?
- Are mentorship and partnership claims held to the evidence rule despite the stakeholder’s suggested wording?
- Is the practical connection useful while its status remains appropriate to the evidence?
- Does the JSON pass, and does the prose preserve the same boundaries?

Passing the structural validator alone is not passing this behavioral test.
