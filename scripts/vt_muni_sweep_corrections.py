#!/usr/bin/env python3
"""VT #163 straggler sweep -- hand corrections the builder cannot express.
Run from ~/workspace/civic-data-vt163. Prints every action; asserts shapes
before editing."""
import textwrap
from pathlib import Path

R = Path("data/us/vt")
M = R / "memberships/municipal"
RETR = "2026-10-21"


def note_block(url, note, retrieved=RETR):
    esc = note.replace("'", "''")
    wrapped = textwrap.fill(esc, width=76,
                            initial_indent="  note: '",
                            subsequent_indent="    ")
    return f"- url: {url}\n{wrapped}'\n  retrieved: '{retrieved}'\n"


def append_source(path, url, note):
    t = path.read_text()
    assert t.endswith("\n")
    path.write_text(t + note_block(url, note))
    print("APPEND-SRC", path.name)


def end_membership(path, url, note):
    t = path.read_text()
    assert "\nend:" not in t, path
    lines = t.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("how_seated:"):
            lines.insert(i + 1, "end: '2026'")
            break
    else:
        raise AssertionError(f"no how_seated in {path}")
    path.write_text("\n".join(lines))
    append_source(path, url, note)
    print("ENDED", path.name)


# ---------- 1. deletions ----------
DELETES = [
    R / "posts/municipal/barnard-vt-town-agent.yaml",
    R / "organizations/municipal/barnard-vt-town-agent.yaml",
    R / "posts/municipal/bridgewater-vt-lister.yaml",
    R / "organizations/municipal/bridgewater-vt-lister.yaml",
    M / "bridgewater-vt-lister-kaleb-mcintire.yaml",
    R / "posts/municipal/wilmington-vt-trustee-of-cc-haynes-fund.yaml",
    R / "organizations/municipal/wilmington-vt-trustee-of-cc-haynes-fund.yaml",
    M / "danville-vt-auditor-andrew-grout.yaml",
    M / "danville-vt-constable-matt-choate.yaml",
    M / "danville-vt-moderator-eric-bach.yaml",
    M / "danville-vt-lister-ellen-woodward.yaml",
    M / "danville-vt-lister-sharon-langford.yaml",
    R / "people/municipal/ellen-woodward.yaml",
    R / "people/municipal/sharon-langford.yaml",
    R / "people/municipal/andrew-grout.yaml",
]
for p in DELETES:
    assert p.exists(), p
    p.unlink()
    print("DELETE", p)

# ---------- 2. seat corrections ----------
for post, old, new in [
    (R / "posts/municipal/danville-vt-lister.yaml", "seats: 2", "seats: 3"),
    (R / "posts/municipal/plainfield-vt-cemetery-commissioner.yaml",
     "seats: 3", "seats: 5"),
]:
    t = post.read_text()
    assert f"\n{old}\n" in t, post
    post.write_text(t.replace(f"\n{old}\n", f"\n{new}\n", 1))
    print("SEATS", post.name, old, "->", new)

# ---------- 3. membership endings ----------
READING_MIN = ("https://readingvt.govoffice.com/vertical/sites/"
               "%7B29D76170-2CBD-4DB0-A089-6F91F5BED766%7D/uploads/"
               "20260407131936802.pdf")
end_membership(
    M / "reading-vt-library-trustee-vanessa-maxham.yaml", READING_MIN,
    "Town of Reading, 2026 election-of-officers and appointments table "
    "(Selectboard minutes packet, April 7, 2026): Vanessa Maxham "
    "resigned as Library Trustee and Rich Grogan was appointed to the "
    "seat. The exact resignation date is not published; this "
    "membership is ended in 2026.")
end_membership(
    M / "reading-vt-library-trustee-janet-malcolm.yaml", READING_MIN,
    "Town of Reading, 2026 election-of-officers and appointments table "
    "(Selectboard minutes packet, April 7, 2026): Janet Malcolm "
    "resigned as Library Trustee and Kristen Hurd was appointed to "
    "the seat. The exact resignation date is not published; this "
    "membership is ended in 2026.")
end_membership(
    M / "shoreham-vt-auditor-maureen-gour.yaml", "https://shorehamvt.us",
    "Town of Shoreham, Auditors page (live): the sitting auditors are "
    "Tamra Hawley-House, Karen Jarboe-Singletary and Michelle "
    "Treadway; Maureen Gour no longer sits. Her departure date and "
    "mechanism are not published; this membership is ended in 2026 "
    "on the town's current page.")
end_membership(
    M / "worcester-vt-cemetery-commissioner-heather-pagel.yaml",
    "https://worcestervt.org/wp/public_html/wp/wp-content/uploads/"
    "2026/09/Cemetery-Minutes-9.9.26.pdf",
    "Town of Worcester, Cemetery Commission minutes, September 9, "
    "2026, and the town directory: John Meninger sits as Cemetery "
    "Commissioner (appointed) and Heather Pagel no longer does. Her "
    "departure date is not published; this membership (cemetery "
    "commissioner only -- her town treasurer record is separate and "
    "stands) is ended in 2026.")
end_membership(
    M / "johnson-vt-village-treasurer-rosemary-audibert.yaml",
    "https://villageofjohnson.com/wp-content/uploads/2026/05/"
    "Johnson-Village-Trustee-Board-Minutes-5-11-26.pdf",
    "Village of Johnson, Board of Trustees minutes, May 11, 2026: on "
    "Rosemary Audibert's retirement as Village Treasurer the board "
    "voted to offer the position to Ashley Isabell, who holds it "
    "(see her membership). Audibert continues as Village Clerk.")
end_membership(
    M / "westford-vt-library-trustee-kelsi-cross.yaml",
    "https://westfordvt.us/wp-content/uploads/2026/03/"
    "Official-Return-of-Votes-2026.pdf",
    "Town of Westford, Official Return of Votes, March 3, 2026: "
    "Charles Cavanaugh was elected to the library trustee seat (the "
    "5-year seat with one year remaining) that Kelsi Cross held by "
    "interim appointment. Her appointment ended with that election.")

# ---------- 4. richford hancock how_seated ----------
p = M / "richford-vt-lister-jon-hancock.yaml"
t = p.read_text()
assert "\nhow_seated: elected\n" in t
p.write_text(t.replace("\nhow_seated: elected\n",
                       "\nhow_seated: appointed\n", 1))
append_source(
    p, "https://www.richfordvt.org",
    "Town of Richford, Selectboard minutes, March 16, 2026: 'motion "
    "to appoint Jon as lister... passed unanimously' -- Hancock was "
    "appointed to the lister seat, not elected. This corrects the "
    "batch-11 record, which carried him as elected.")
print("HOW_SEATED richford hancock -> appointed")

# ---------- 5. danville selectboard phantom-source replacement -------
CORRECTION = ("This source replaces the batch-6 citation to a "
              "clerk-signed 'Results of Officers Elected' document "
              "that does not exist; the holder is verified by the "
              "town report and minutes cited here.")
SB = {
    "alison-low": (
        "Selectboard member, term to 2028",
        "Articles 2-3 of the same minutes filled the seats whose "
        "terms expired in 2026; Alison Low's term (to 2028) was not "
        "before the meeting."),
    "eric-bach": (
        "Selectboard member, term to 2027",
        "Articles 2-3 of the same minutes filled the seats whose "
        "terms expired in 2026; Eric Bach's term (to 2027) was not "
        "before the meeting."),
    "matt-choate": (
        "Selectboard member, term to 2026",
        "Article 2: Matt Choate was elected Selectperson for a "
        "3-year term."),
    "janice-ouellette": (
        "Selectboard member, term to 2026",
        "Article 3: Janice Ouellette was elected Selectperson for "
        "a 1-year term."),
    "kristen-calkins": (
        "Kristen Calkins does not appear in the 2025 report's "
        "officers table (the five listed are Low, Bach, Herrin, "
        "Choate and Ouellette)",
        "Article 3: Kristen Calkins was elected Selectperson for a "
        "1-year term, succeeding Glenn Herrin, whose report term "
        "ran to 2026 and who was not re-elected."),
}
for slug, (report_fact, minutes_fact) in SB.items():
    p = M / f"danville-vt-selectboard-{slug}.yaml"
    t = p.read_text()
    marker = "- url: https://danvillevt.gov\n"
    assert t.count("- url:") == 2 and marker in t, p
    head = t[:t.index(marker)]
    new = head
    new += note_block(
        "https://danvillevt.gov",
        "Town of Danville, 2025 Annual Town Report, elected "
        f"officers tables (pp. 10-12): {report_fact}. {CORRECTION}")
    new += note_block(
        "https://danvillevt.gov",
        "Town of Danville, DRAFT Annual Town Meeting minutes, "
        f"March 3, 2026: {minutes_fact}")
    p.write_text(new)
    print("SB-SRC", p.name)
print("DONE")
