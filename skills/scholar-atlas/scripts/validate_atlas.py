#!/usr/bin/env python3
"""Validate Find Your Trajectory — Scholar Edition atlas v1 without third-party dependencies or network access."""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


def normalize_doi(value):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("DOI must be a string or null")
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value.strip(), flags=re.I)
    if not re.fullmatch(r"10\.\d{4,9}/\S+", value, re.I):
        raise ValueError("invalid DOI syntax")
    return value.casefold()


def validate(data):
    errors = []

    def check(ok, where, message):
        if not ok:
            errors.append(f"{where}: {message}")
        return bool(ok)

    def text(obj, key, where):
        value = obj.get(key)
        return check(isinstance(value, str) and bool(value.strip()), where, f"{key} must be nonempty text")

    def bilingual(obj, key, where):
        value = obj.get(key)
        if check(isinstance(value, dict), where, f"{key} must have en and zh"):
            text(value, "en", where + "." + key)
            text(value, "zh", where + "." + key)

    def date(value, where, nullable=False):
        if nullable and value is None:
            return
        try:
            if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                raise ValueError()
            dt.date.fromisoformat(value)
        except (ValueError, TypeError):
            check(False, where, "must be an ISO calendar date YYYY-MM-DD")

    def strings(value, where, minimum=1):
        return check(isinstance(value, list) and len(value) >= minimum and all(isinstance(x, str) and x.strip() for x in value), where, f"must be a list of at least {minimum} nonempty strings")

    if not isinstance(data, dict):
        return ["root: expected an object"]
    check(data.get("schema_version") == 1, "root", "schema_version must be 1")
    check(type(data.get("synthetic")) is bool, "root", "synthetic must be boolean")
    synthetic = data.get("synthetic") is True
    groups = {}
    ids = set()

    def register(obj, where):
        ident = obj.get("id")
        if check(isinstance(ident, str) and bool(ident.strip()), where, "id must be nonempty text"):
            check(ident not in ids, where, f"duplicate global ID {ident}")
            ids.add(ident)

    names = ("sources", "evidence", "works", "theories", "terms", "edges", "contributions", "related_scholars", "impact_claims")
    for name in names:
        items = data.get(name)
        if not check(isinstance(items, list), name, "must be a list"):
            items = []
        valid = []
        for i, obj in enumerate(items):
            if check(isinstance(obj, dict), f"{name}[{i}]", "must be an object"):
                register(obj, f"{name}[{i}]")
                valid.append(obj)
        groups[name] = valid
    maps = {k: {x["id"]: x for x in v if isinstance(x.get("id"), str)} for k, v in groups.items()}
    scholar = data.get("scholar")
    if not check(isinstance(scholar, dict), "scholar", "must be an object"):
        scholar = {}
    register(scholar, "scholar")
    bilingual(scholar, "name", "scholar")
    people = set(maps["related_scholars"])
    if isinstance(scholar.get("id"), str):
        people.add(scholar["id"])
    nodes = people | set(maps["theories"]) | set(maps["works"])

    def refs(obj, where, field="evidence_refs", required=True):
        values = obj.get(field)
        if not strings(values, where + "." + field, 1 if required else 0):
            return []
        check(len(values) == len(set(values)), where, f"duplicate {field}")
        found = []
        for ident in values:
            if check(ident in maps["evidence"], where, f"unknown evidence ID {ident}"):
                found.append(maps["evidence"][ident])
        return found

    def direct(items, scope):
        return any(e.get("grade") == "direct" and e.get("scope") == scope for e in items)

    for s in groups["sources"]:
        w = str(s.get("id"))
        check(s.get("kind") in {"primary_publication", "official_profile", "official_project", "secondary", "synthetic"}, w, "invalid source kind")
        check(s.get("access") in {"fulltext", "abstract", "metadata", "unavailable", "synthetic"}, w, "invalid access level")
        date(s.get("checked_at"), w + ".checked_at")
        check("licence" in s and (s["licence"] is None or isinstance(s["licence"], str)), w, "licence must be text or explicit null")
        if synthetic:
            check(s.get("kind") == "synthetic" and s.get("access") == "synthetic" and s.get("url") is None, w, "synthetic sources must be labelled synthetic with null URL")
        else:
            check(s.get("kind") != "synthetic" and s.get("access") != "synthetic", w, "synthetic evidence cannot appear in a real atlas")
            u = urlparse(s.get("url") if isinstance(s.get("url"), str) else "")
            check(u.scheme in {"http", "https"} and bool(u.netloc), w, "real source requires HTTP(S) URL")
    scopes = {"bibliographic", "citation", "theoretical", "biographical", "activity", "mentorship", "collaboration", "outcome", "interpretation"}
    for e in groups["evidence"]:
        w = str(e.get("id"))
        text(e, "locator", w)
        text(e, "note", w)
        check(e.get("grade") in {"direct", "inference"}, w, "invalid evidence grade")
        check(e.get("scope") in scopes, w, "invalid evidence scope")
        sid = e.get("source_id")
        source = maps["sources"].get(sid) if isinstance(sid, str) else None
        if check(source is not None, w, "unknown source_id"):
            check(source.get("access") != "unavailable", w, "unavailable source cannot support inspected evidence")
            if source.get("access") == "metadata":
                check(e.get("scope") == "bibliographic", w, "metadata access only supports bibliographic evidence")

    dois = {}
    version_count = 0
    for work in groups["works"]:
        w = str(work.get("id"))
        text(work, "title", w)
        strings(work.get("author_names"), w + ".author_names")
        check(type(work.get("year")) is int, w, "year must be an integer")
        refs(work, w)
        check(work.get("identity_status") in {"resolved", "unresolved"}, w, "invalid identity_status")
        versions = work.get("versions")
        if not check(isinstance(versions, list) and bool(versions), w, "versions must be a nonempty list"):
            continue
        if len(versions) > 1 or work.get("identity_status") == "unresolved":
            text(work, "identity_note", w)
        if len(versions) > 1:
            identity = refs(work, w, "identity_evidence_refs")
            check(direct(identity, "bibliographic"), w, "multiple versions need direct bibliographic identity evidence")
        for i, version in enumerate(versions):
            vwhere = f"{w}.versions[{i}]"
            version_count += 1
            if not check(isinstance(version, dict), vwhere, "must be an object"):
                continue
            register(version, vwhere)
            text(version, "kind", vwhere)
            check("date" in version and "doi" in version, vwhere, "date and doi must be explicit, or null")
            date(version.get("date"), vwhere + ".date", True)
            for field in ("online_date", "issue_date"):
                if field in version:
                    date(version[field], vwhere + "." + field, True)
            refs(version, vwhere)
            try:
                doi = normalize_doi(version.get("doi"))
                if doi:
                    check(doi not in dois, vwhere, f"duplicate DOI {doi}; first at {dois.get(doi)}; consolidate a repeated DOI into one version with multiple date fields")
                    dois[doi] = vwhere
            except ValueError as exc:
                check(False, vwhere, str(exc))
    coverage = data.get("coverage")
    if check(isinstance(coverage, dict), "coverage", "must be an object"):
        date(coverage.get("as_of"), "coverage.as_of")
        for key in ("scope", "limitation"):
            text(coverage, key, "coverage")
        check(type(coverage.get("work_count")) is int and coverage["work_count"] == len(groups["works"]), "coverage", "work_count mismatch")
        check(type(coverage.get("version_count")) is int and coverage["version_count"] == version_count, "coverage", "version_count mismatch")

    for theory in groups["theories"]:
        w = str(theory.get("id"))
        for key in ("label", "discipline", "proposition", "mechanism", "misreading"):
            bilingual(theory, key, w)
        strings(theory.get("authors"), w + ".authors")
        check("year" in theory and (theory["year"] is None or type(theory["year"]) is int), w, "year must be an integer or null")
        refs(theory, w)
    for term in groups["terms"]:
        w = str(term.get("id"))
        for key in ("term", "definition", "example"):
            bilingual(term, key, w)
        check(isinstance(term.get("theory_id"), str) and term["theory_id"] in maps["theories"], w, "unknown theory_id")
        refs(term, w)
    for edge in groups["edges"]:
        w = str(edge.get("id"))
        bilingual(edge, "label", w)
        ev = refs(edge, w)
        for key in ("source", "target"):
            check(isinstance(edge.get(key), str) and edge[key] in nodes, w, f"unknown {key} node")
        kind, basis = edge.get("type"), edge.get("basis")
        check(kind in {"direct_citation", "conceptual_development", "application", "comparison", "mentorship"}, w, "invalid edge type")
        check(basis in {"explicit", "inferred"}, w, "invalid edge basis")
        if kind in {"direct_citation", "mentorship"}:
            check(basis == "explicit", w, f"{kind} cannot be inferred")
            check(direct(ev, "citation" if kind == "direct_citation" else "mentorship"), w, f"{kind} needs matching direct evidence")
        if kind == "mentorship":
            check(edge.get("source") in people and edge.get("target") in people, w, "mentorship connects people only")
        if kind in {"conceptual_development", "application"} and basis == "explicit":
            check(direct(ev, "theoretical"), w, "explicit theoretical edge needs direct theoretical evidence")
        if kind == "comparison":
            check(basis == "inferred", w, "comparison must be labelled inferred")
            label = edge.get("label") if isinstance(edge.get("label"), dict) else {}
            check("comparison" in str(label.get("en", "")).lower() and "比较" in str(label.get("zh", "")), w, "comparison label must say comparison / 比较")
            check(len(ev) >= 2, w, "comparison needs evidence for both sides")
    for c in groups["contributions"]:
        w = str(c.get("id"))
        bilingual(c, "claim", w)
        ev = refs(c, w)
        check(isinstance(c.get("work_id"), str) and c["work_id"] in maps["works"], w, "unknown work_id")
        check(c.get("kind") in {"empirical_application", "mechanism_extension", "concept_proposal", "theoretical_innovation"}, w, "invalid contribution kind")
        check(c.get("status") in {"evidenced", "inference"}, w, "invalid contribution status")
        if c.get("status") == "evidenced":
            check(direct(ev, "theoretical"), w, "evidenced contribution needs direct theoretical evidence")
        if c.get("kind") == "theoretical_innovation":
            text(c, "novelty_scope", w)
            text(c, "attribution", w)
    for person in groups["related_scholars"]:
        w = str(person.get("id"))
        for key in ("name", "relation"):
            bilingual(person, key, w)
        for key in ("affiliation", "activity"):
            text(person, key, w)
        date(person.get("as_of"), w + ".as_of")
        date(person.get("activity_date"), w + ".activity_date")
        if isinstance(person.get("activity_date"), str) and isinstance(person.get("as_of"), str):
            check(person["activity_date"] <= person["as_of"], w, "activity_date cannot be after the observation date")
        ev = refs(person, w)
        for scope in ("biographical", "activity"):
            official = [e for e in ev if maps["sources"].get(e.get("source_id"), {}).get("kind") in ({"synthetic"} if synthetic else {"official_profile", "official_project", "primary_publication"})]
            check(direct(official, scope), w, f"related scholar needs direct official {scope} evidence")
    pairs = {("evidenced", "documented_collaboration"), ("evidenced", "reported_outcome"), ("inference", "interpretation"), ("proposal", "proposal")}
    for claim in groups["impact_claims"]:
        w = str(claim.get("id"))
        bilingual(claim, "label", w)
        status, relation = claim.get("status"), claim.get("relation")
        check((status, relation) in pairs, w, "invalid impact status/relation pair; proposals are not documented partnerships")
        ev = refs(claim, w, required=status != "proposal")
        if relation == "documented_collaboration":
            check(direct(ev, "collaboration"), w, "collaboration needs direct collaboration evidence")
            strings(claim.get("parties"), w + ".parties", 2)
        if relation == "reported_outcome":
            check(direct(ev, "outcome"), w, "outcome needs direct outcome evidence")
            text(claim, "period", w)
            text(claim, "attribution", w)
        if status == "proposal":
            text(claim, "next_step", w)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("atlas", type=Path)
    args = parser.parse_args()
    try:
        with args.atlas.open(encoding="utf-8") as stream:
            data = json.load(stream)
        errors = validate(data)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"FAIL: cannot validate input: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print("ERROR " + error, file=sys.stderr)
        print(f"FAIL: {len(errors)} issue(s)", file=sys.stderr)
        return 1
    print(f"PASS: {len(data['works'])} works, {data['coverage']['version_count']} versions; synthetic={data['synthetic']}")
    print("Structure passed. Source truth and scholarly interpretation still require review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
