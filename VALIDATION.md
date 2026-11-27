# Find Your Trajectory — Scholar Edition: validation record

Prepared on 2026-11-27. The 18 tests and both synthetic atlases were rerun successfully after the project rename. No network access, publishing, installation or external account actions were used for these checks.

| Check | Result |
|---|---|
| `python3 skills/scholar-atlas/scripts/validate_atlas.py examples/synthetic-atlas.json` | Passed: 2 works, 3 consolidated versions, synthetic=true |
| `python3 tests/test_validator.py` | 18 tests pass, including negative evidence/identity cases |
| Independent forward test using `evals/raw-packet.md` | Produced an overview and valid JSON: 1 work, 2 versions |
| Skill Creator `quick_validate.py skills/scholar-atlas` | Attempted; blocked by environment dependency: `ModuleNotFoundError: No module named 'yaml'` |

The official Skill Creator validator requires PyYAML. This repository’s atlas validator and tests use only the standard library. No replacement parser was substituted to claim that the official check passed. To repeat that check, run the Skill Creator validator from an existing environment with PyYAML.

The independent evaluator received the skill and a different fictional source packet, without the demonstration atlas or test mutations. Its output explicitly distinguished citation from mentorship, kept a possible industry connection as a proposal, documented the unavailable foundational text, and did not claim to have read a complete corpus. The maintaining agent inspected its prose and reran its JSON validation. Evaluation artifacts are local under the Git-ignored `evals/runs/independent-01/` folder.

These checks establish selected structural and behavioral properties. They do not establish that future source passages are true, translations are accurate, or a claimed theory is novel across a whole field.

## Source visibility update — 2026-11-28

The final-output instructions now require a reader-facing source overview and claim-level references with purpose, inspected scope, access limits, dates and passage locations. The v1 schema, validator and 18 existing tests are unchanged; no tests that merely match instruction wording were added.

- Reran all 18 existing tests: passed.
- Reran the demonstration atlas validator: passed, 2 works / 3 versions.
- An independent agent used the expanded fictional packet without seeing the demonstration or earlier evaluation results. Its final Markdown overview contained 7 visible source cards and 16 local citation markers; all markers resolved to those cards. The maintaining agent read the report and checked its references independently.
- The report distinguished article excerpts, official-profile material, index-only metadata, an unsuccessful book-access attempt and a restricted private document. It did not present Scholar as original theoretical evidence, the inaccessible book as read, or private material as publicly accessible. It retained the limited-corpus statement and rejected unsupported mentorship and partnership claims.
- The new evaluation JSON passed a separate rerun: 1 work / 2 versions. Its local artifacts are Git-ignored under `evals/runs/independent-sources-02/`.
- Reran Skill Creator `quick_validate.py`: still blocked by the environment’s missing PyYAML module. No substitute parser or dependency installation was used.

This was a Markdown-output acceptance check, not a browser or PDF-export test. The final-visibility requirement must also be checked in the actual website or other format when one is produced. No remote state was changed for this update.
