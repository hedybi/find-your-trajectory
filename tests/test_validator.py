"""Behavioral invariants using fictional data; no live DOI resolution or network."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT / "skills/scholar-atlas/scripts/validate_atlas.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
EXAMPLE = json.loads((ROOT / "examples/synthetic-atlas.json").read_text(encoding="utf-8"))


class EvidenceInvariants(unittest.TestCase):
    def setUp(self):
        self.atlas = copy.deepcopy(EXAMPLE)

    def errors(self):
        return "\n".join(validator.validate(self.atlas))

    def test_valid_demo(self):
        self.assertEqual(validator.validate(self.atlas), [])

    def test_missing_reference(self):
        self.atlas["theories"][0]["evidence_refs"] = ["missing"]
        self.assertIn("unknown evidence ID", self.errors())

    def test_duplicate_doi_across_works(self):
        self.atlas["works"][0]["versions"][0]["doi"] = "https://doi.org/10.5555/SYNTHETIC"
        self.atlas["works"][1]["versions"][0]["doi"] = " doi:10.5555/synthetic "
        self.assertIn("duplicate DOI", self.errors())

    def test_doi_punctuation_not_silently_removed(self):
        self.assertEqual(validator.normalize_doi("https://doi.org/10.5555/test(1)"), "10.5555/test(1)")

    def test_missing_version_identity_evidence(self):
        self.atlas["works"][1]["identity_evidence_refs"] = ["e-mechanism"]
        self.assertIn("identity evidence", self.errors())

    def test_distinct_work_count(self):
        self.atlas["coverage"]["work_count"] = 3
        self.assertIn("work_count mismatch", self.errors())

    def test_version_count(self):
        self.atlas["coverage"]["version_count"] = 2
        self.assertIn("version_count mismatch", self.errors())

    def test_bilingual_definition(self):
        del self.atlas["terms"][0]["definition"]["zh"]
        self.assertIn("zh must be nonempty", self.errors())

    def test_citation_is_not_mentorship(self):
        edge = self.atlas["edges"][0]
        edge.update(type="mentorship", source="person-rook", target="person-reed")
        self.assertIn("mentorship needs matching direct evidence", self.errors())

    def test_comparison_cannot_be_explicit_descent(self):
        self.atlas["edges"][2]["basis"] = "explicit"
        self.assertIn("comparison must be labelled inferred", self.errors())

    def test_proposal_cannot_be_documented_partnership(self):
        self.atlas["impact_claims"][0]["relation"] = "documented_collaboration"
        self.assertIn("invalid impact status/relation pair", self.errors())

    def test_relabelling_both_fields_does_not_prove_collaboration(self):
        self.atlas["impact_claims"][0].update(status="evidenced", relation="documented_collaboration", parties=["Fictional researcher", "Fictional company"])
        self.assertIn("collaboration needs direct collaboration evidence", self.errors())

    def test_unavailable_source_cannot_support_evidence(self):
        self.atlas["sources"][0]["access"] = "unavailable"
        self.assertIn("unavailable source cannot support", self.errors())

    def test_synthetic_sources_cannot_be_passed_as_real(self):
        self.atlas["synthetic"] = False
        self.assertIn("synthetic evidence cannot appear in a real atlas", self.errors())

    def test_invalid_calendar_date(self):
        self.atlas["coverage"]["as_of"] = "2026-02-30"
        self.assertIn("ISO calendar date", self.errors())

    def test_future_activity_is_not_observed_activity(self):
        self.atlas["related_scholars"][0]["activity_date"] = "2027-01-01"
        self.assertIn("activity_date cannot be after", self.errors())

    def test_optional_publication_dates_are_checked(self):
        self.atlas["works"][0]["versions"][0]["issue_date"] = "2026-13-01"
        self.assertIn("ISO calendar date", self.errors())

    def test_malformed_input_returns_errors(self):
        self.assertTrue(validator.validate([]))
        self.atlas["edges"] = [None]
        self.assertIn("must be an object", self.errors())


if __name__ == "__main__":
    unittest.main(verbosity=2)
