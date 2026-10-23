#!/usr/bin/env python3
"""Batch 4 of the VT #163 municipal fan-out (alphabetical positions
31-40): Bridport, Brighton, Bristol, Brookfield, Brookline,
Brownington, Brunswick, Burke, Burlington (city), Cabot.
Emits one JSON spec per municipality for build_vt_municipality.py.
Research: vt_muni_batch4_research.md.
"""
import json
from pathlib import Path

OUT = Path(__file__).parent / "vt_muni_data"
OUT.mkdir(exist_ok=True)

SB_DIR = {
    "url": "https://outside.vermont.gov/dept/sos/Elections_Division/election_info_resources/town_meeting_local_elections/selectboardinformation.pdf",
    "note": "PLACEHOLDER",
}
JP_PDF = {
    "url": "https://outside.vermont.gov/dept/sos/Elections_Division/election_info_resources/candidates/local_office_descriptions/vermont_justices_of_the_peace.pdf",
    "note": "PLACEHOLDER",
}
GUIDE = {
    "url": "https://outside.vermont.gov/dept/sos/Elections_Division/voters/guide_vermonts_town_clerks_treasurers_county.pdf",
    "note": "PLACEHOLDER",
}
STATUTE_2646 = {
    "url": "https://legislature.vermont.gov/statutes/section/17/055/02646",
    "note": "PLACEHOLDER",
}


def S(src, note):
    d = dict(src)
    d["note"] = note
    return d


def sb_dir(roster_note):
    return S(SB_DIR, "Vermont Secretary of State, Elections Division, "
             "'Vermont Selectboard Members' directory (updated "
             f"June 5, 2026): {roster_note}")


def sb_dir_none(town):
    return S(SB_DIR, "Vermont Secretary of State, Elections Division, "
             "'Vermont Selectboard Members' directory (updated "
             f"June 5, 2026): publishes no {town} roster ('Contact "
             "the Town Clerk'); the roster recorded here is from the "
             "town's official website.")


def jp_src(count_note):
    return S(JP_PDF, "Vermont Secretary of State, Elections Division, "
             "'2025-2026 Vermont Justices of the Peace' listing "
             f"(updated December 4, 2025): {count_note}")


def guide(what):
    return S(GUIDE, "Vermont Secretary of State, Elections Division, "
             "'Guide to Vermont's Town Clerks, Treasurers, & County "
             f"Clerks' (January 2026): {what}")


def statute2646(office_phrase):
    return S(STATUTE_2646, "17 V.S.A. section 2646 (official text, "
             "Vermont General Assembly) provides for the election of "
             f"{office_phrase} at annual town meeting.")


def statute2646_structure(office_phrase):
    return S(STATUTE_2646, "17 V.S.A. section 2646 (official text, "
             "Vermont General Assembly) provides for the election of "
             f"{office_phrase} at annual town meeting. Structure only: "
             "no official source publishes the current holder; the "
             "seat is left unfilled rather than guessed.")


def jp_election(prefix, label, vote_for, winners_note, extra_sources=()):
    return {
        "election_id": f"{prefix}/2024-11-05/general",
        "contest_id": f"{prefix}/2024-11-05/justice-of-the-peace",
        "name": f"{label} Justice of the Peace Election 2024-11-05",
        "filename": f"{prefix}--2024-11-05--justice-of-the-peace.yaml",
        "vote_for": vote_for,
        "sources": [jp_src(winners_note)] + list(extra_sources),
        "header": f"# {label} -- justice of the peace election "
                  f"(VT municipal batch 4); issue #163 "
                  f"(VT master tracking).",
    }


def holder(name, slug, **kw):
    d = {"name": name, "slug": slug}
    d.update(kw)
    return d


def spec(place_slug, label, offices, jp=None):
    d = {
        "label": label,
        "place_slug": place_slug,
        "jurisdiction_id": f"ocd-jurisdiction/country:us/state:vt/place:{place_slug}/government",
        "header": f"# {label} municipal roster backfill -- Vermont\n"
                  f"# municipal fan-out batch 4; issue #163 "
                  f"(VT master tracking).\n",
        "offices": offices,
    }
    if jp:
        d["jp_election"] = jp
    return d


def office(slug, title, org_name, seats, sources, holders=(), **kw):
    d = {
        "slug": slug,
        "title": title,
        "org_name": org_name,
        "seats": seats,
        "sources": sources,
    }
    if holders:
        d["holders"] = list(holders)
    d.update(kw)
    return d


SPECS = []

# ------------------------------------------------------------------
# Bridport (general law + charter ch. 107A: clerk & treasurer
# appointed by the selectboard)
# ------------------------------------------------------------------
BRID_CONTACTS = {
    "url": "https://bridportvt.org/contacts",
    "note": "PLACEHOLDER",
}
BRID_CH = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/107A",
    "note": "PLACEHOLDER",
}
BRID_SITE = {
    "url": "https://bridportvt.org",
    "note": "PLACEHOLDER",
}


def brid_ch(what):
    return S(BRID_CH, "Town of Bridport charter, Title 24 Appendix "
             f"V.S.A. chapter 107A (2015 No. M-16): {what}")


SPECS.append(spec("bridport", "Town of Bridport", [
    office("selectboard", "Selectboard Member", "Bridport Selectboard", 5,
           [S(BRID_CONTACTS, "Town of Bridport official website, "
              "Contacts page: lists five Selectboard members: Tim "
              "Howlett (Chair), Drexel Wheeler, Stephanie Pope, "
              "Robert Sunderland, and David Bronson."),
            sb_dir_none("Bridport")],
           [holder("Tim Howlett", "tim-howlett"),
            holder("Drexel Wheeler", "drexel-wheeler"),
            holder("Stephanie Pope", "stephanie-pope"),
            holder("Robert Sunderland", "robert-sunderland"),
            holder("David Bronson", "david-bronson")]),
    office("town-clerk", "Town Clerk", "Bridport Town Clerk", 1,
           [brid_ch("section 3 provides that the Town Clerk is "
                    "appointed by the Selectboard."),
            S(BRID_CONTACTS, "Town of Bridport official website, "
              "Contacts page: names Julie Howlett as Town Clerk.")],
           [holder("Julie Howlett", "julie-howlett",
                   how_seated="appointed")]),
    office("town-treasurer", "Town Treasurer", "Bridport Town Treasurer", 1,
           [brid_ch("section 3 provides that the Town Treasurer is "
                    "appointed by the Selectboard."),
            S(BRID_CONTACTS, "Town of Bridport official website, "
              "Contacts page: names Luella Gipson as Town Treasurer. "
              "The Secretary of State's January 2026 Guide still "
              "names Kathleen Shimel; the town's current page "
              "governs, and the change is an appointment change "
              "under the charter."),
            guide("lists Kathleen Shimel as Treasurer of Bridport "
                  "(superseded by the town's current Contacts page).")],
           [holder("Luella Gipson", "luella-gipson",
                   how_seated="appointed")]),
    office("moderator", "Moderator", "Bridport Town Moderator", 1,
           [S(BRID_SITE, "Town of Bridport official website: the 2026 "
              "Town Meeting Warning warned election of a Moderator "
              "(one-year term), and the town's draft minutes of the "
              "March 2026 annual meeting record Tim Howlett elected "
              "Moderator. The minutes are posted in draft form; the "
              "election is recorded from them with that disclosure.")],
           [holder("Tim Howlett", "tim-howlett")]),
    office("lister", "Lister", "Bridport Listers", 3,
           [S(BRID_SITE, "Town of Bridport official website: the "
              "town's draft minutes of the March 2026 annual meeting "
              "record Vicki Major elected Lister (three-year term); "
              "the minutes are posted in draft form. The holders of "
              "the other two lister seats are published in no "
              "official source and are left unfilled.")],
           [holder("Vicki Major", "vicki-major")]),
    office("auditor", "Auditor", "Bridport Auditors", 3,
           [S(BRID_SITE, "Town of Bridport official website: the "
              "2026 Town Meeting Warning warned election of three "
              "Auditors (three-, two-, and one-year terms), and the "
              "town's draft minutes of the March 2026 annual meeting "
              "record 'No one was elected' for all three seats. The "
              "post is created structure only; all three seats are "
              "vacant.")]),
    office("first-constable", "First Constable", "Bridport First Constable", 1,
           [S(BRID_SITE, "Town of Bridport official website: the "
              "town's draft minutes of the March 2026 annual meeting "
              "record Richard Shimel elected First Constable "
              "(one-year term); the minutes are posted in draft "
              "form. He is a distinct person from former Town "
              "Treasurer Kathleen Shimel.")],
           [holder("Richard Shimel", "richard-shimel")]),
    office("second-constable", "Second Constable", "Bridport Second Constable", 1,
           [S(BRID_SITE, "Town of Bridport official website: the "
              "town's draft minutes of the March 2026 annual meeting "
              "record Dusty Huestis elected Second Constable "
              "(one-year term); the minutes are posted in draft "
              "form.")],
           [holder("Dusty Huestis", "dusty-huestis")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Bridport Cemetery Commission", 5,
           [{"url": "https://bridportvt.org/cemetery-commission-info-minutes",
             "note": "Town of Bridport official website, Cemetery "
                     "Commission page: the commission is composed of "
                     "five members."},
            S(BRID_SITE, "Town of Bridport official website: the "
              "town's draft minutes of the March 2026 annual meeting "
              "record David Basque elected Cemetery Commissioner "
              "(five-year term); the minutes are posted in draft "
              "form. The holders of the other four seats are "
              "published in no official source and are left "
              "unfilled.")],
           [holder("David Basque", "david-basque")]),
    office("grand-juror", "Grand Juror", "Bridport Grand Juror", 1,
           [statute2646_structure("a grand juror")]),
    office("town-agent", "Town Agent", "Bridport Town Agent", 1,
           [statute2646_structure("a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Bridport Justices of the Peace", 7,
           [jp_src("lists seven Bridport justices of the peace: "
                   "Michael Bordeleau, Joan Huestis, Judd Markowski, "
                   "Chris Goodrich, Philip Wagner, Steve Huestis, and "
                   "Heather Hodsden.")],
           [holder("Michael Bordeleau", "michael-bordeleau"),
            holder("Joan Huestis", "joan-huestis"),
            holder("Judd Markowski", "judd-markowski"),
            holder("Chris Goodrich", "chris-goodrich"),
            holder("Philip Wagner", "philip-wagner"),
            holder("Steve Huestis", "steve-huestis"),
            holder("Heather Hodsden", "heather-hodsden")]),
], jp=jp_election("bridport-vt", "Town of Bridport", 7,
                  "lists seven Bridport justices of the peace for the "
                  "2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Brighton (general law)
# ------------------------------------------------------------------
BRIGHTON_DEPT = {
    "url": "https://brightonvt.org/town-departments/",
    "note": "PLACEHOLDER",
}

SPECS.append(spec("brighton", "Town of Brighton", [
    office("selectboard", "Selectboard Member", "Brighton Selectboard", 3,
           [S(BRIGHTON_DEPT, "Town of Brighton official website, Town "
              "Departments page: lists three Selectboard members: "
              "Michael Testut (Chair), Heather McElroy, and William "
              "Hawkins."),
            sb_dir_none("Brighton")],
           [holder("Michael Testut", "michael-testut"),
            holder("Heather McElroy", "heather-mcelroy"),
            holder("William Hawkins", "william-hawkins")]),
    office("town-clerk", "Town Clerk", "Brighton Town Clerk", 1,
           [guide("lists Teresa DeBonville as Town Clerk of "
                  "Brighton and as Town Treasurer of Brighton."),
            S(BRIGHTON_DEPT, "Town of Brighton official website, Town "
              "Departments page: names Teresa DeBonville as Town "
              "Clerk and Town Treasurer.")],
           [holder("Teresa DeBonville", "teresa-debonville")]),
    office("town-treasurer", "Town Treasurer", "Brighton Town Treasurer", 1,
           [guide("lists Teresa DeBonville as Town Clerk of "
                  "Brighton and as Town Treasurer of Brighton."),
            S(BRIGHTON_DEPT, "Town of Brighton official website, Town "
              "Departments page: names Teresa DeBonville as Town "
              "Clerk and Town Treasurer.")],
           [holder("Teresa DeBonville", "teresa-debonville")]),
    office("moderator", "Moderator", "Brighton Town Moderator", 1,
           [statute2646_structure("a moderator")]),
    office("lister", "Lister", "Brighton Listers", 3,
           [S(BRIGHTON_DEPT, "Town of Brighton official website, Town "
              "Departments page: names Tara Martin as a Lister and "
              "prints '(two lister positions vacant)'. The two "
              "vacant seats are left unfilled.")],
           [holder("Tara Martin", "tara-martin")]),
    office("auditor", "Auditor", "Brighton Auditors", 3,
           [S(BRIGHTON_DEPT, "Town of Brighton official website, Town "
              "Departments page: names Jocelyn Gervais and Judy "
              "Castonguay as Auditors. The holder of the third seat "
              "is published in no official source and is left "
              "unfilled.")],
           [holder("Jocelyn Gervais", "jocelyn-gervais"),
            holder("Judy Castonguay", "judy-castonguay")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Brighton Cemetery Commission", 3,
           [S(BRIGHTON_DEPT, "Town of Brighton official website, Town "
              "Departments page: names John Manning, Julie Lamere, "
              "and Reg Lamere as Cemetery Commissioners.")],
           [holder("John Manning", "john-manning"),
            holder("Julie Lamere", "julie-lamere"),
            holder("Reg Lamere", "reg-lamere")]),
    office("grand-juror", "Grand Juror", "Brighton Grand Juror", 1,
           [statute2646_structure("a grand juror")]),
    office("town-agent", "Town Agent", "Brighton Town Agent", 1,
           [statute2646_structure("a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Brighton Justices of the Peace", 7,
           [jp_src("lists seven Brighton justices of the peace: "
                   "David Robbins, Dolores Robbins, Peder Pederson, "
                   "Susan Pederson, Janet Osborne, Kystyna Kurzej "
                   "(spelled as printed in the listing), and "
                   "Stephanie Nagle.")],
           [holder("David Robbins", "david-robbins"),
            holder("Dolores Robbins", "dolores-robbins"),
            holder("Peder Pederson", "peder-pederson"),
            holder("Susan Pederson", "susan-pederson"),
            holder("Janet Osborne", "janet-osborne"),
            holder("Kystyna Kurzej", "kystyna-kurzej"),
            holder("Stephanie Nagle", "stephanie-nagle")]),
], jp=jp_election("brighton-vt", "Town of Brighton", 7,
                  "lists seven Brighton justices of the peace for "
                  "the 2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Bristol (merger charter ch. 108; general-law officers, Selectboard
# fixed at five)
# ------------------------------------------------------------------
BRISTOL_SB = {
    "url": "https://bristolvt.org/boards-commissions-committees/selectboard/",
    "note": "PLACEHOLDER",
}
BRISTOL_REPORT = {
    "url": "http://bristolvt.org/wp-content/uploads/2026/02/Town_of_Bristol_FY2025_Annual_Report_web.pdf",
    "note": "PLACEHOLDER",
}
BRISTOL_WARNING = {
    "url": "https://bristolvt.org/wp-content/uploads/2026/02/Town_of_Bristol_2026_Annual-Meeting-Warning_2026-01-28_approved.pdf",
    "note": "PLACEHOLDER",
}
BRISTOL_SITE = {
    "url": "https://bristolvt.org",
    "note": "PLACEHOLDER",
}
BRISTOL_CH = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/108",
    "note": "PLACEHOLDER",
}

SPECS.append(spec("bristol", "Town of Bristol", [
    office("selectboard", "Selectboard Member", "Bristol Selectboard", 5,
           [sb_dir("lists five Bristol Selectboard members: Ian "
                   "Albinson (Chair), Joel Bouvier, John Heffernan, "
                   "Michelle Perlee, and Jessica Teets (Vice-Chair)."),
            S(BRISTOL_SB, "Town of Bristol official website, "
              "Selectboard page: lists Ian Albinson (Chair; term to "
              "2028), Jessica Teets (Vice-Chair; term to 2028), Joel "
              "Bouvier (term to 2027), John Heffernan (term to "
              "2027), and Michelle Perlee (term to 2029)."),
            S(BRISTOL_CH, "Town of Bristol merger charter, Title 24 "
              "Appendix V.S.A. chapter 108, section 301: town "
              "officers are as provided by general law and the "
              "Selectboard is fixed at five members.")],
           [holder("Ian Albinson", "ian-albinson"),
            holder("Joel Bouvier", "joel-bouvier"),
            holder("John Heffernan", "john-heffernan"),
            holder("Michelle Perlee", "michelle-perlee"),
            holder("Jessica Teets", "jessica-teets")]),
    office("town-clerk", "Town Clerk", "Bristol Town Clerk", 1,
           [guide("lists Sharon Lucia as Town Clerk of Bristol and "
                  "as Town Treasurer of Bristol."),
            S(BRISTOL_WARNING, "Town of Bristol, 2026 Annual Meeting "
              "Warning (approved January 28, 2026): attested by "
              "'Sharon A. Lucia, Town Clerk'.")],
           [holder("Sharon Lucia", "sharon-lucia")]),
    office("town-treasurer", "Town Treasurer", "Bristol Town Treasurer", 1,
           [guide("lists Sharon Lucia as Town Clerk of Bristol and "
                  "as Town Treasurer of Bristol."),
            S(BRISTOL_REPORT, "Town of Bristol, FY2025 Annual Report, "
              "Town Employees page: lists Sharon Lucia as Town Clerk "
              "and Town Treasurer.")],
           [holder("Sharon Lucia", "sharon-lucia")]),
    office("moderator", "Moderator", "Bristol Town Moderator", 1,
           [S(BRISTOL_SITE, "Town of Bristol official website: the "
              "town's official ballot results for the March 3, 2026 "
              "annual meeting record Jennifer L. Wagner elected "
              "Moderator (549 votes, one-year term)."),
            S(BRISTOL_REPORT, "Town of Bristol, FY2025 Annual Report, "
              "Elected Town Officials page: lists Jennifer Wagner as "
              "Moderator (term expiring 2026, the seat filled at the "
              "2026 annual meeting).")],
           [holder("Jennifer Wagner", "jennifer-wagner")]),
    office("lister", "Lister", "Bristol Listers", 3,
           [S(BRISTOL_SITE, "Town of Bristol official website, town "
              "directory: lists Patricia King, Douglas Corkins, and "
              "Mark Bouvier as the town's Listers."),
            S(BRISTOL_REPORT, "Town of Bristol, FY2025 Annual Report, "
              "Elected Town Officials page: lists Patricia L. King "
              "(term expiring 2026), Douglas Corkins (term expiring "
              "2027), and Mark Bouvier (term expiring 2028) as "
              "Listers. The lister seat filled in March 2026 was "
              "contested by write-in only and the town published no "
              "tally; the town directory continues to list King, "
              "and she is recorded from it.")],
           [holder("Patricia King", "patricia-king"),
            holder("Douglas Corkins", "douglas-corkins"),
            holder("Mark Bouvier", "mark-bouvier")]),
    office("delinquent-tax-collector", "Collector of Delinquent Taxes",
           "Bristol Collector of Delinquent Taxes", 1,
           [S(BRISTOL_SITE, "Town of Bristol official website, town "
              "directory: styles Sharon Lucia 'Town "
              "Clerk/Treasurer/Delinquent Tax Collector'; the town "
              "fills the office separately from the treasurer's "
              "general duties, so the post is created under "
              "17 V.S.A. section 2651d.")],
           [holder("Sharon Lucia", "sharon-lucia")]),
    office("first-constable", "First Constable", "Bristol First Constable", 1,
           [S(BRISTOL_REPORT, "Town of Bristol, FY2025 Annual Report, "
              "Elected Town Officials page: lists Bruce Nason as 1st "
              "Constable with a term expiring in 2026. The 2026 "
              "contest was contested by write-in only and the town "
              "published no winner, so the seat is left unfilled "
              "rather than carried over. Structure only.")]),
    office("second-constable", "Second Constable", "Bristol Second Constable", 1,
           [S(BRISTOL_REPORT, "Town of Bristol, FY2025 Annual Report, "
              "Elected Town Officials page: the 2nd Constable seat "
              "(term expiring 2026) is printed with no name (vacant). "
              "Structure only.")]),
    office("library-trustee", "Library Trustee",
           "Bristol Lawrence Memorial Library Trustees", 7,
           [S(BRISTOL_REPORT, "Town of Bristol, FY2025 Annual Report, "
              "Elected Town Officials page: lists seven Lawrence "
              "Memorial Library Trustees: Scott Kluever (term "
              "expiring 2026), Daniella Hall Sutherland (term "
              "expiring 2026), Peter Hewitt (2027), Elizabeth "
              "Guilbeault (2027), Ken Johnson (2028), Darren "
              "Kleinfelter (2028), and Vicki Coyle (2028)."),
            S(BRISTOL_SITE, "Town of Bristol official website: the "
              "town's official ballot results for the March 3, 2026 "
              "annual meeting record Scott Kluever (469) and Sophie "
              "Bristol Pickens (520) elected Library Trustees "
              "(three-year terms). Sutherland's term expired in "
              "2026 and she was not re-elected; she is not "
              "recorded.")],
           [holder("Scott Kluever", "scott-kluever"),
            holder("Sophie Bristol Pickens", "sophie-bristol-pickens"),
            holder("Peter Hewitt", "peter-hewitt"),
            holder("Elizabeth Guilbeault", "elizabeth-guilbeault"),
            holder("Ken Johnson", "ken-johnson"),
            holder("Darren Kleinfelter", "darren-kleinfelter"),
            holder("Vicki Coyle", "vicki-coyle")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Bristol Justices of the Peace", 12,
           [jp_src("lists twelve Bristol justices of the peace: "
                   "Nathan Bouvier, Sharon Compagna, Dayna Epstein, "
                   "Mark Gibson, Patricia King, Daniel Lyons, Dave "
                   "Sharpe, Ben Skolozdra, Alicia Standridge, Don "
                   "Stratton, Anne Wallace, and Helen Young. Nathan "
                   "Bouvier is a distinct person from Selectboard "
                   "member Joel Bouvier and Lister Mark Bouvier.")],
           [holder("Nathan Bouvier", "nathan-bouvier"),
            holder("Sharon Compagna", "sharon-compagna"),
            holder("Dayna Epstein", "dayna-epstein"),
            holder("Mark Gibson", "mark-gibson"),
            holder("Patricia King", "patricia-king"),
            holder("Daniel Lyons", "daniel-lyons"),
            holder("Dave Sharpe", "dave-sharpe"),
            holder("Ben Skolozdra", "ben-skolozdra"),
            holder("Alicia Standridge", "alicia-standridge"),
            holder("Don Stratton", "don-stratton"),
            holder("Anne Wallace", "anne-wallace"),
            holder("Helen Young", "helen-young")]),
], jp=jp_election("bristol-vt", "Town of Bristol", 12,
                  "lists twelve Bristol justices of the peace for "
                  "the 2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Brookfield (general law; treasurer appointed by the selectboard
# per the town's officers table)
# ------------------------------------------------------------------
BF_SB = {
    "url": "https://www.brookfieldvt.org/board-committee/selectboard/",
    "note": "PLACEHOLDER",
}
BF_REPORT = {
    "url": "https://www.brookfieldvt.org/wp/wp-content/uploads/2026/02/Brookfield-Report-2025_2-1.pdf",
    "note": "PLACEHOLDER",
}
BF_MINUTES = {
    "url": "https://www.brookfieldvt.org/wp/wp-content/uploads/2026/03/Brookfield-Annual-Meeting-2026-Minutes.pdf",
    "note": "PLACEHOLDER",
}
BF_AGENDA = {
    "url": "https://www.brookfieldvt.org/wp/wp-content/uploads/2026/03/SB-Agenda-Mch-232026.pdf",
    "note": "PLACEHOLDER",
}


def bf_report(what):
    return S(BF_REPORT, "Town of Brookfield, 2025 Annual Town "
             f"Report, 'Town of Brookfield Officers 2025' table: {what}")


SPECS.append(spec("brookfield", "Town of Brookfield", [
    office("selectboard", "Selectboard Member", "Brookfield Selectboard", 5,
           [S(BF_SB, "Town of Brookfield official website, Selectboard "
              "page: lists John Benson (Chair), Curtis Koren, Keith "
              "Sprague, Laura Rochat, and Stuart Edson as Selectboard "
              "members."),
            bf_report("lists the Selectboard as J. Keith Sprague III, "
                      "John Benson, Stuart Edson, C. Curtis Koren, and "
                      "Laura Rochat."),
            sb_dir_none("Brookfield")],
           [holder("John Benson", "john-benson",
                   existing_person_id="ocd-person/af620c1b-f9f0-5af0-bbaa-a11ab9be74c2"),
            holder("Curtis Koren", "curtis-koren"),
            holder("Keith Sprague", "keith-sprague"),
            holder("Laura Rochat", "laura-rochat"),
            holder("Stuart Edson", "stuart-edson")]),
    office("town-clerk", "Town Clerk", "Brookfield Town Clerk", 1,
           [guide("lists Carol Monness as Town Clerk of Brookfield."),
            bf_report("lists Town Clerk Carol J. Monness (three-year "
                      "term, printed end March 2026)."),
            S(BF_MINUTES, "Town of Brookfield, minutes of the March 3, "
              "2026 annual meeting: Carol J. Monness served as Town "
              "Clerk at the meeting; the minutes record no Australian "
              "ballot results."),
            S(BF_AGENDA, "Town of Brookfield, Selectboard agenda for "
              "March 23, 2026: lists 'Town Auditors and Town "
              "Moderator -- Carol and Kristi' (Clerk Carol Monness "
              "and Treasurer Kristi Ehlers) as the officers "
              "reporting, three weeks after the annual meeting; no "
              "official source names any other person as Town Clerk, "
              "and she is recorded as holding the office on that "
              "post-election evidence.")],
           [holder("Carol Monness", "carol-monness")]),
    office("town-treasurer", "Town Treasurer", "Brookfield Town Treasurer", 1,
           [bf_report("lists the Treasurer as 'appt.' -- Kristi "
                      "Ehlers, appointed by the Selectboard."),
            guide("lists Kristi Ehlers as Treasurer of Brookfield.")],
           [holder("Kristi Ehlers", "kristi-ehlers",
                   how_seated="appointed")]),
    office("moderator", "Moderator", "Brookfield Town Moderator", 1,
           [bf_report("lists Town Moderator Greg Wight (term ended "
                      "March 5, 2026)."),
            S(BF_MINUTES, "Town of Brookfield, minutes of the March 3, "
              "2026 annual meeting: note that 2026 was Greg Wight's "
              "last year as Moderator; the minutes record no "
              "Australian ballot results."),
            S(BF_AGENDA, "Town of Brookfield, Selectboard agenda for "
              "March 23, 2026: lists a Town Moderator 'decline' "
              "letter as an item of business. The 2026 outcome and "
              "any successor are published in no official source, "
              "so the seat is left unfilled. Structure only.")]),
    office("lister", "Lister", "Brookfield Listers", 3,
           [bf_report("lists Listers Kristi Ehlers (term to 2028), "
                      "Tom Garbitelli (term to 2027), and Carol J. "
                      "Monness (term ended March 5, 2026). Monness's "
                      "seat stood for election in March 2026 and no "
                      "official source publishes the outcome; that "
                      "seat is left unfilled.")],
           [holder("Kristi Ehlers", "kristi-ehlers"),
            holder("Tom Garbitelli", "tom-garbitelli")]),
    office("auditor", "Auditor", "Brookfield Auditors", 3,
           [bf_report("prints 'Vacant' for the Auditor office (all "
                      "three seats). Structure only; the seats are "
                      "vacant.")]),
    office("delinquent-tax-collector", "Collector of Delinquent Taxes",
           "Brookfield Collector of Delinquent Taxes", 1,
           [bf_report("lists Delinquent Tax Collector Kristi Ehlers "
                      "(term ended March 5, 2026); the town fills "
                      "the office separately, so the post is created "
                      "under 17 V.S.A. section 2651d. No official "
                      "source publishes the outcome of the March 2026 "
                      "election for the seat, so it is left unfilled. "
                      "Structure only.")]),
    office("first-constable", "First Constable", "Brookfield First Constable", 1,
           [bf_report("lists 1st Constable Dan Mason (term ended "
                      "March 5, 2026). No official source publishes "
                      "the outcome of the March 2026 election for "
                      "the seat, so it is left unfilled. Structure "
                      "only.")]),
    office("second-constable", "Second Constable", "Brookfield Second Constable", 1,
           [bf_report("lists 2nd Constable Ed Neas (term ended "
                      "March 5, 2026). No official source publishes "
                      "the outcome of the March 2026 election for "
                      "the seat, so it is left unfilled. Structure "
                      "only.")]),
    office("library-trustee", "Library Trustee",
           "Brookfield Library Trustees", 5,
           [bf_report("lists five Library Trustees (three-year "
                      "terms): Emily Noyes (term ended March 7, "
                      "2026), Susan O'Brien (term ended March 7, "
                      "2026), Amy Borgman (term to 2028), Dan Childs "
                      "(term to 2027), and Starr Strong (term to "
                      "2027). The seats whose terms ended in March "
                      "2026 are left unfilled; no official source "
                      "publishes their outcomes.")],
           [holder("Amy Borgman", "amy-borgman"),
            holder("Dan Childs", "dan-childs"),
            holder("Starr Strong", "starr-strong")]),
    office("grand-juror", "Grand Juror", "Brookfield Grand Juror", 1,
           [statute2646_structure("a grand juror")]),
    office("town-agent", "Town Agent", "Brookfield Town Agent", 1,
           [bf_report("prints the headings 'Agent to Deed Land' and "
                      "'Agent to Defend Suits' with no names. "
                      "Structure only: no official source publishes "
                      "the current holder."),
            statute2646("a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Brookfield Justices of the Peace", 7,
           [jp_src("lists seven Brookfield justices of the peace: "
                   "Elizabeth \"Beth\" DeForge, Billi Gosh, C. Curtis "
                   "Koren, Linda Runnion, Perry Kacik, Kym Anderson, "
                   "and Starr Strong."),
            bf_report("lists the same seven justices of the peace, "
                      "terms ending February 1, 2027.")],
           [holder("Elizabeth DeForge", "elizabeth-deforge",
                   ballot_name='Elizabeth "Beth" DeForge'),
            holder("Billi Gosh", "billi-gosh"),
            holder("Curtis Koren", "curtis-koren",
                   ballot_name="C. Curtis Koren"),
            holder("Linda Runnion", "linda-runnion"),
            holder("Perry Kacik", "perry-kacik"),
            holder("Kym Anderson", "kym-anderson"),
            holder("Starr Strong", "starr-strong")]),
], jp=jp_election("brookfield-vt", "Town of Brookfield", 7,
                  "lists seven Brookfield justices of the peace for "
                  "the 2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Brookline (general law; treasurer and delinquent tax collector
# appointed per the town's officers pages)
# ------------------------------------------------------------------
BL_ELECTED = {
    "url": "https://brooklinevt.com/elected-town-officers/",
    "note": "PLACEHOLDER",
}
BL_APPT = {
    "url": "https://brooklinevt.com/appointed-town-officers/",
    "note": "PLACEHOLDER",
}


def bl_elected(what):
    return S(BL_ELECTED, "Town of Brookline official website, "
             f"Elected Town Officers page: {what}")


SPECS.append(spec("brookline", "Town of Brookline", [
    office("selectboard", "Selectboard Member", "Brookline Selectboard", 5,
           [sb_dir("lists five Brookline Selectboard members: Emily "
                   "Beer, E. Mark Bills, Michael Desocio (Chair), "
                   "Bruce Mello, and Douglas Wellman."),
            bl_elected("lists the Selectboard as Michael Desocio "
                       "(Chair; term to 2028), Doug Wellman (Vice "
                       "Chair; term to 2027), Bruce Mello (term to "
                       "2029), Emily Beer (term to 2027), and E. Mark "
                       "Bills (term to 2028).")],
           [holder("Michael Desocio", "michael-desocio"),
            holder("Doug Wellman", "doug-wellman"),
            holder("Bruce Mello", "bruce-mello"),
            holder("Emily Beer", "emily-beer"),
            holder("E. Mark Bills", "e-mark-bills")]),
    office("town-clerk", "Town Clerk", "Brookline Town Clerk", 1,
           [bl_elected("lists Marjorie Ray as Town Clerk, elected, "
                       "one-year term expiring 2027."),
            guide("lists Marjorie Ray as Town Clerk of Brookline.")],
           [holder("Marjorie Ray", "marjorie-ray")]),
    office("town-treasurer", "Town Treasurer", "Brookline Town Treasurer", 1,
           [bl_elected("lists Melissa Brown as Treasurer, appointed, "
                       "term expiring 2027."),
            guide("lists Melissa Brown as Treasurer of Brookline.")],
           [holder("Melissa Brown", "melissa-brown",
                   how_seated="appointed")]),
    office("moderator", "Moderator", "Brookline Town Moderator", 1,
           [bl_elected("lists David Y. Parker, Jr. as Moderator, "
                       "elected, one-year term expiring 2027.")],
           [holder("David Y. Parker, Jr.", "david-y-parker-jr")]),
    office("lister", "Lister", "Brookline Listers", 3,
           [bl_elected("lists the Lister office with one seat "
                       "'Vacant' (term expiring 2029) and Helen Holt, "
                       "appointed, term expiring 2027. The third seat "
                       "is accounted for in no official source and is "
                       "left unfilled.")],
           [holder("Helen Holt", "helen-holt",
                   how_seated="appointed")]),
    office("auditor", "Auditor", "Brookline Auditors", 3,
           [bl_elected("lists three Auditors, all elected: Heidi "
                       "Nystrom (Chair; term to 2027), Kendra Brooks "
                       "(term to 2029), and Frank Rucker (term to "
                       "2027).")],
           [holder("Heidi Nystrom", "heidi-nystrom"),
            holder("Kendra Brooks", "kendra-brooks"),
            holder("Frank Rucker", "frank-rucker")]),
    office("delinquent-tax-collector", "Collector of Delinquent Taxes",
           "Brookline Collector of Delinquent Taxes", 1,
           [bl_elected("lists Melissa Brown as Delinquent Tax "
                       "Collector, appointed, one-year term expiring "
                       "2027; the town fills the office separately, "
                       "so the post is created under 17 V.S.A. "
                       "section 2651d.")],
           [holder("Melissa Brown", "melissa-brown",
                   how_seated="appointed")]),
    office("first-constable", "First Constable", "Brookline First Constable", 1,
           [bl_elected("lists the First Constable officeholder as "
                       "'Selectboard' (the board itself), term "
                       "printed 2026. No individual holder is named, "
                       "so no membership is recorded. Structure "
                       "only.")]),
    office("second-constable", "Second Constable", "Brookline Second Constable", 1,
           [bl_elected("lists the Second Constable officeholder as "
                       "'Selectboard' (the board itself), term "
                       "printed 2026. No individual holder is named, "
                       "so no membership is recorded. Structure "
                       "only.")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Brookline Cemetery Commission", 5,
           [bl_elected("lists five Cemetery Commissioner seats "
                       "(five-year terms, all elected): Dorothy Maggio "
                       "(term to 2030), Howard Osgood (term to 2031), "
                       "one seat 'Vacant' (term to 2028), Michael W. "
                       "Winot (term to 2027), and Doug Wellman (term "
                       "to 2029). The vacant seat is left unfilled.")],
           [holder("Dorothy Maggio", "dorothy-maggio"),
            holder("Howard Osgood", "howard-osgood"),
            holder("Michael W. Winot", "michael-w-winot"),
            holder("Doug Wellman", "doug-wellman")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Brookline Trustees of Public Funds", 1,
           [bl_elected("lists a single Trustee of Public Funds "
                       "position, marked appointed, with the name "
                       "cell blank (24 V.S.A. section 2431 permits a "
                       "town to elect one or more trustees). No "
                       "holder is named, so no membership is "
                       "recorded. Structure only.")]),
    office("grand-juror", "Grand Juror", "Brookline Grand Juror", 1,
           [statute2646_structure("a grand juror")]),
    office("town-agent", "Town Agent", "Brookline Town Agent", 1,
           [statute2646_structure("a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Brookline Justices of the Peace", 2,
           [jp_src("lists two Brookline justices of the peace: "
                   "Laurie J. Nau-Martocci and Dorothy Maggio.")],
           [holder("Laurie Nau-Martocci", "laurie-nau-martocci",
                   ballot_name="Laurie J. Nau-Martocci"),
            holder("Dorothy Maggio", "dorothy-maggio")]),
], jp=jp_election("brookline-vt", "Town of Brookline", 2,
                  "lists two Brookline justices of the peace for the "
                  "2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing names only two justices for Brookline; "
                  "any remaining seat is a possible vacancy the "
                  "listing does not explain. The listing publishes "
                  "no vote totals and no party designations for "
                  "justices of the peace.")))

# ------------------------------------------------------------------
# Brownington (general law)
# ------------------------------------------------------------------
BROWNING_SB = {
    "url": "https://www.browningtonvt.com/town-officials/select-board",
    "note": "PLACEHOLDER",
}
BROWNING_SITE = {
    "url": "https://www.browningtonvt.com",
    "note": "PLACEHOLDER",
}

SPECS.append(spec("brownington", "Town of Brownington", [
    office("selectboard", "Selectboard Member", "Brownington Selectboard", 3,
           [sb_dir("lists three Brownington Selectboard members: "
                   "Byron Burdick, Mike Glodgett, and Marilyn "
                   "Martinez (Chair)."),
            S(BROWNING_SB, "Town of Brownington official website, "
              "Select Board page: lists Mike Glodgett (term expires "
              "2027), Marilyn Martinez, Chairman (term expires "
              "2028), and Byron Burdick (term expires 2029).")],
           [holder("Michael Glodgett", "mike-glodgett"),
            holder("Byron Burdick", "byron-burdick"),
            holder("Marilyn Martinez", "marilyn-martinez")]),
    office("town-clerk", "Town Clerk", "Brownington Town Clerk", 1,
           [guide("lists Cheryl Galipeau as Town Clerk of "
                  "Brownington and as Town Treasurer of "
                  "Brownington. The town's website contact page "
                  "names only the office; no official source names "
                  "any other holder.")],
           [holder("Cheryl Galipeau", "cheryl-galipeau")]),
    office("town-treasurer", "Town Treasurer", "Brownington Town Treasurer", 1,
           [guide("lists Cheryl Galipeau as Town Clerk of "
                  "Brownington and as Town Treasurer of "
                  "Brownington.")],
           [holder("Cheryl Galipeau", "cheryl-galipeau")]),
    office("moderator", "Moderator", "Brownington Town Moderator", 1,
           [{"url": "https://docs.google.com/document/d/1Th-fJtyflbxt7gIkyGJGC8L5DIx36q7t/edit",
             "note": "Town of Brownington, 2026 Annual Town Meeting "
                     "Warning (published on the town website): warns "
                     "election of a Moderator. No official source "
                     "publishes the holder's name, so the seat is "
                     "left unfilled. Structure only."}]),
    office("lister", "Lister", "Brownington Listers", 3,
           [S(BROWNING_SITE, "Town of Brownington official website, "
              "Listers page: lists Larry Chase (term expires 2027), "
              "Roger Patenaude (term expires 2028), and Larry Faust "
              "(term expires 2029) as Listers.")],
           [holder("Larry Chase", "larry-chase"),
            holder("Roger Patenaude", "roger-patenaude"),
            holder("Larry Faust", "larry-faust")]),
    office("auditor", "Auditor", "Brownington Auditors", 3,
           [S(BROWNING_SITE, "Town of Brownington official website, "
              "Auditors page: lists Barbara Thompson (term expires "
              "2027), Kim Hastings (term expires 2028), and Beth "
              "Martin (term expires 2029) as Auditors.")],
           [holder("Barbara Thompson", "barbara-thompson"),
            holder("Kim Hastings", "kim-hastings"),
            holder("Beth Martin", "beth-martin")]),
    office("first-constable", "First Constable", "Brownington First Constable", 1,
           [S(BROWNING_SITE, "Town of Brownington official website, "
              "Constables page: lists Cameron Falconer as Town "
              "First Constable (term expires 2028).")],
           [holder("Cameron Falconer", "cameron-falconer")]),
    office("second-constable", "Second Constable", "Brownington Second Constable", 1,
           [S(BROWNING_SITE, "Town of Brownington official website, "
              "Constables page: lists Renee Falconer as Town Second "
              "Constable (term expires 2028).")],
           [holder("Renee Falconer", "renee-falconer")]),
    office("grand-juror", "Grand Juror", "Brownington Grand Juror", 1,
           [statute2646_structure("a grand juror")]),
    office("town-agent", "Town Agent", "Brownington Town Agent", 1,
           [statute2646_structure("a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Brownington Justices of the Peace", 5,
           [jp_src("lists five Brownington justices of the peace: "
                   "Armand Brunelle, Larry Chase, Larry Faust, "
                   "Andrew Swett, and Michael Glodgett."),
            S(BROWNING_SITE, "Town of Brownington official website, "
              "Justices of the Peace page: names the same five "
              "justices of the peace.")],
           [holder("Armand Brunelle", "armand-brunelle"),
            holder("Larry Chase", "larry-chase"),
            holder("Larry Faust", "larry-faust"),
            holder("Andrew Swett", "andrew-swett"),
            holder("Michael Glodgett", "mike-glodgett")]),
], jp=jp_election("brownington-vt", "Town of Brownington", 5,
                  "lists five Brownington justices of the peace for "
                  "the 2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Brunswick (general law; no official town website exists -- the
# Bloomfield treatment: SOS sources only)
# ------------------------------------------------------------------
SPECS.append(spec("brunswick", "Town of Brunswick", [
    office("selectboard", "Selectboard Member", "Brunswick Selectboard", 3,
           [sb_dir("lists three Brunswick Selectboard members: David "
                   "Caron, Robert Hook, and Darcy Smart. Brunswick "
                   "has no official town website; the directory is "
                   "the official roster of record.")],
           [holder("David Caron", "david-caron"),
            holder("Robert Hook", "robert-hook"),
            holder("Darcy Smart", "darcy-smart")]),
    office("town-clerk", "Town Clerk", "Brunswick Town Clerk", 1,
           [guide("lists Sharon Graham as Town Clerk of Brunswick "
                  "and as Town Treasurer of Brunswick.")],
           [holder("Sharon Graham", "sharon-graham")]),
    office("town-treasurer", "Town Treasurer", "Brunswick Town Treasurer", 1,
           [guide("lists Sharon Graham as Town Clerk of Brunswick "
                  "and as Town Treasurer of Brunswick.")],
           [holder("Sharon Graham", "sharon-graham")]),
    office("moderator", "Moderator", "Brunswick Town Moderator", 1,
           [statute2646_structure("a moderator")]),
    office("lister", "Lister", "Brunswick Listers", 3,
           [statute2646_structure("listers")]),
    office("auditor", "Auditor", "Brunswick Auditors", 3,
           [statute2646_structure("auditors")]),
    office("grand-juror", "Grand Juror", "Brunswick Grand Juror", 1,
           [statute2646_structure("a grand juror")]),
    office("town-agent", "Town Agent", "Brunswick Town Agent", 1,
           [statute2646_structure("a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Brunswick Justices of the Peace", 5,
           [jp_src("lists five Brunswick justices of the peace: "
                   "Claudette Hook, Laurence Hook, Jr., Sharon "
                   "Graham, Crystal Meunier, and Deborah Tetreault. "
                   "Claudette Hook and Laurence Hook, Jr. are "
                   "distinct persons from Selectboard member Robert "
                   "Hook.")],
           [holder("Claudette Hook", "claudette-hook"),
            holder("Laurence Hook, Jr.", "laurence-hook-jr"),
            holder("Sharon Graham", "sharon-graham"),
            holder("Crystal Meunier", "crystal-meunier"),
            holder("Deborah Tetreault", "deborah-tetreault")]),
], jp=jp_election("brunswick-vt", "Town of Brunswick", 5,
                  "lists five Brunswick justices of the peace for "
                  "the 2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Burke (general law; lister office eliminated by town vote in
# 2016; the 2026 warning elects Moderator, Selectperson, Constable,
# and Agent to Convey Real Estate only)
# ------------------------------------------------------------------
BURKE_OFFICES = {
    "url": "https://www.burkevermont.org/offices-and-departments",
    "note": "PLACEHOLDER",
}
BURKE_BOARDS = {
    "url": "https://www.burkevermont.org/boards-and-commissions",
    "note": "PLACEHOLDER",
}
BURKE_WARNING = {
    "url": "https://irp.cdn-website.com/9e15e12e/files/uploaded/2026+Burke+Warning.pdf",
    "note": "PLACEHOLDER",
}


def burke_warning(what):
    return S(BURKE_WARNING, "Town of Burke, 2026 Town Meeting "
             f"Warning: {what}")


SPECS.append(spec("burke", "Town of Burke", [
    office("selectboard", "Selectboard Member", "Burke Selectboard", 3,
           [sb_dir("lists three Burke Selectboard members: Joseph "
                   "Allard, Gerald Booth, and Mark Daigle (Chair)."),
            S(BURKE_BOARDS, "Town of Burke official website, Boards & "
              "Commissions page (Selectboard tab): lists Mark Daigle "
              "(Chair), Jerry Booth, and Joe Allard.")],
           [holder("Mark Daigle", "mark-daigle"),
            holder("Gerald Booth", "gerald-booth"),
            holder("Joseph Allard", "joseph-allard")]),
    office("town-clerk", "Town Clerk", "Burke Town Clerk", 1,
           [S(BURKE_OFFICES, "Town of Burke official website, Offices "
              "& Departments page: names Linda Hackett-Corey as Town "
              "Clerk."),
            guide("lists Linda Hackett-Corey as Town Clerk of "
                  "Burke.")],
           [holder("Linda Hackett-Corey", "linda-hackett-corey")]),
    office("town-treasurer", "Town Treasurer", "Burke Town Treasurer", 1,
           [guide("lists Kathleen Feeley as Treasurer of Burke."),
            S(BURKE_OFFICES, "Town of Burke official website, Offices "
              "& Departments page: names the Town Treasurer as "
              "'Cathi Feeley'; the town's Justices of the Peace page "
              "and the Secretary of State's sources print Kathleen "
              "Feeley, the form recorded here.")],
           [holder("Kathleen Feeley", "kathleen-feeley")]),
    office("moderator", "Moderator", "Burke Town Moderator", 1,
           [burke_warning("Article 4 warns election of a Town "
                          "Moderator (Australian ballot). The town's "
                          "official results publish no names, and "
                          "the name printed on the sample ballot is "
                          "a candidacy, not a certified result, so "
                          "the seat is left unfilled. Structure "
                          "only.")]),
    office("constable", "Constable", "Burke Constable", 1,
           [burke_warning("Article 4 warns election of one Constable "
                          "(Australian ballot). The town's official "
                          "results publish no names, and the name "
                          "printed on the sample ballot is a "
                          "candidacy, not a certified result, so the "
                          "seat is left unfilled. Structure only.")]),
    office("agent-to-convey-real-estate", "Agent to Convey Real Estate",
           "Burke Agent to Convey Real Estate", 1,
           [burke_warning("Article 4 warns election of an Agent to "
                          "Convey Real Estate (Australian ballot); "
                          "the 2026 ballot offered the office by "
                          "write-in only. No official source names a "
                          "holder, so the seat is left unfilled. "
                          "Structure only.")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Burke Justices of the Peace", 7,
           [jp_src("lists seven Burke justices of the peace: Wendy "
                   "Bean, Susan Carr, Anthony (Tony) DeMasi, Kathleen "
                   "Feeley, Joel Gilbert, Joan Harlowe, and John "
                   "Kascenska. The town website's justices page names "
                   "a different set of six (including a Daniel Tanner "
                   "and omitting Harlowe); the Secretary of State "
                   "listing governs the election record.")],
           [holder("Wendy Bean", "wendy-bean"),
            holder("Susan Carr", "susan-carr"),
            holder("Anthony DeMasi", "anthony-demasi",
                   ballot_name="Anthony (Tony) DeMasi"),
            holder("Kathleen Feeley", "kathleen-feeley"),
            holder("Joel Gilbert", "joel-gilbert"),
            holder("Joan Harlowe", "joan-harlowe"),
            holder("John Kascenska", "john-kascenska")]),
], jp=jp_election("burke-vt", "Town of Burke", 7,
                  "lists seven Burke justices of the peace for the "
                  "2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Burlington (city charter ch. 003)
# ------------------------------------------------------------------
BURL_CH = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/003",
    "note": "PLACEHOLDER",
}
BURL_DECL = {
    "url": "https://www.burlingtonvt.gov/DocumentCenter/View/11781/Declaration-of-Election-Results---Candidates-Official-PDF",
    "note": "PLACEHOLDER",
}
BURL_DIR_PAGE = {
    "url": "https://www.burlingtonvt.gov/m/directory/employee?eid=6",
    "note": "PLACEHOLDER",
}


def burl_ch(what):
    return S(BURL_CH, "City of Burlington charter, Title 24 Appendix "
             f"V.S.A. chapter 003: {what}")


def burl_decl(what):
    return S(BURL_DECL, "City of Burlington, 'Declaration of "
             "Election Results - Candidates (Official)' for the "
             f"March 3, 2026 Annual City Election: {what}")


def councilor(name, slug, seat_desc):
    return holder(name, slug, sources=[
        sb_dir(f"lists {name} as City Councilor for the {seat_desc} "
               "of Burlington, and Emma Mulvaney-Stanak as Mayor."),
    ])


SPECS.append(spec("burlington", "City of Burlington", [
    office("mayor", "Mayor", "Burlington Mayor", 1,
           [sb_dir("lists Emma Mulvaney-Stanak as Mayor of "
                   "Burlington."),
            burl_ch("sections 3(a) and 125(a) provide for election "
                    "of a Mayor for a three-year term.")],
           [holder("Emma Mulvaney-Stanak", "emma-mulvaney-stanak")]),
    office("city-councilor", "City Councilor", "Burlington City Council", 12,
           [sb_dir("lists twelve Burlington City Councilors: Mark "
                   "Barlow (North District), Eugene Bergman (Ward 2), "
                   "Marek Broderick (Ward 8), Sarah Carpenter "
                   "(Ward 4), Melo Grant (Central District), Evan "
                   "Litwin (Ward 7), Becca McKnight (Ward 6), Carter "
                   "Neubieser (Ward 1), Laura Sanchez-Parkinson "
                   "(Ward 3), Allie Schachter (East District), "
                   "Ranjot \"Buddy\" Singh (South District), and Ben "
                   "Traverse (Ward 5; Council President)."),
            burl_ch("sections 3(b) and 125(b) provide for election "
                    "of four district councilors and eight ward "
                    "councilors, all for two-year terms."),
            burl_decl("declares the eight ward councilors elected "
                      "March 3, 2026: Carter Neubieser (Ward 1), "
                      "Gene Bergman (Ward 2), Laura Sanchez-Parkinson "
                      "(Ward 3), Sarah Carpenter (Ward 4), Ben "
                      "Traverse (Ward 5), Becca Brown McKnight "
                      "(Ward 6), Evan Litwin (Ward 7), and Marek "
                      "Broderick (Ward 8). The four district "
                      "councilors were elected in 2025 and stand from "
                      "the Secretary of State directory.")],
           [councilor("Mark Barlow", "mark-barlow", "North District"),
            councilor("Gene Bergman", "gene-bergman", "Ward 2"),
            councilor("Marek Broderick", "marek-broderick", "Ward 8"),
            councilor("Sarah Carpenter", "sarah-carpenter", "Ward 4"),
            councilor("Melo Grant", "melo-grant", "Central District"),
            councilor("Evan Litwin", "evan-litwin", "Ward 7"),
            councilor("Becca Brown McKnight", "becca-brown-mcknight",
                      "Ward 6"),
            councilor("Carter Neubieser", "carter-neubieser", "Ward 1"),
            councilor("Laura Sanchez-Parkinson",
                      "laura-sanchez-parkinson", "Ward 3"),
            councilor("Allie Schachter", "allie-schachter",
                      "East District"),
            councilor("Buddy Singh", "buddy-singh", "South District"),
            councilor("Ben Traverse", "ben-traverse", "Ward 5")],
           org_key="burlington-vt/city-council"),
    office("chief-administrative-officer", "Chief Administrative Officer",
           "Burlington Chief Administrative Officer", 1,
           [burl_ch("section 122(a) provides that the Mayor appoints "
                    "a Chief Administrative Officer with the approval "
                    "of the City Council, and section 138 assigns the "
                    "officer the functions of the former City Clerk "
                    "and City Treasurer; the charter has no elected "
                    "clerk or treasurer."),
            S(BURL_DIR_PAGE, "City of Burlington official website, "
              "Staff Directory: styles Katherine Schad 'Chief "
              "Administrative Officer', Clerk / Treasurer's Office.")],
           [holder("Katherine Schad", "katherine-schad",
                   how_seated="appointed")]),
    office("city-grand-juror", "City Grand Juror", "Burlington City Grand Juror", 1,
           [burl_ch("sections 122(a) and 151 provide for a City "
                    "Grand Juror appointed by the Mayor with the "
                    "approval of the City Council. The city publishes "
                    "no current holder by name, so the post is "
                    "created structure only.")]),
    office("city-constable", "City Constable", "Burlington City Constable", 1,
           [burl_ch("sections 122(a) and 152 provide for a City "
                    "Constable appointed by the Mayor with the "
                    "approval of the City Council. The city publishes "
                    "no current holder by name, so the post is "
                    "created structure only.")]),
    office("ward-clerk", "Ward Clerk", "Burlington Ward Clerks", 8,
           [burl_ch("section 10 provides for election of one Ward "
                    "Clerk in each of the city's eight wards, for a "
                    "two-year term."),
            {"url": "https://www.burlingtonvt.gov/185/Election-Workers-Ward-Clerks-Inspectors-",
             "note": "City of Burlington official website, "
                     "'Election Workers - Ward Clerks & Inspectors "
                     "of Election' page: describes the ward clerk "
                     "office but publishes no names by ward."},
            burl_decl("shows a Ward Clerk line only for Ward 3, "
                      "marked 'No candidate elected'. No current "
                      "ward clerk roster is published, so all eight "
                      "seats are left unfilled. Structure only.")]),
    office("inspector-of-election", "Inspector of Election",
           "Burlington Inspectors of Election", 24,
           [burl_ch("section 10 provides for election of three "
                    "Inspectors of Election in each of the city's "
                    "eight wards, for staggered three-year terms."),
            burl_decl("declares the Inspectors of Election elected "
                      "March 3, 2026: Linda A. Sheehey (Ward 1), "
                      "Julia DiPietro (Ward 2), Deborah Krugipudi "
                      "(Ward 3, two-year term), Wendy Rice (Ward 4), "
                      "Rachel Fisher (Ward 5), Leslyn Hall (Ward 6), "
                      "and Thomas L. Fleury (Ward 7); the Ward 3 "
                      "three-year seat and both Ward 8 seats are "
                      "marked 'No candidate elected'. Inspectors "
                      "elected in the 2024 and 2025 cycles are "
                      "published in no current roster; those seats "
                      "are left unfilled rather than reconstructed "
                      "from past declarations.")],
           [holder("Linda A. Sheehey", "linda-a-sheehey"),
            holder("Julia DiPietro", "julia-dipietro"),
            holder("Deborah Krugipudi", "deborah-krugipudi"),
            holder("Wendy Rice", "wendy-rice"),
            holder("Rachel Fisher", "rachel-fisher"),
            holder("Leslyn Hall", "leslyn-hall"),
            holder("Thomas L. Fleury", "thomas-l-fleury")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Burlington Justices of the Peace", 15,
           [jp_src("lists fifteen Burlington justices of the peace: "
                   "Sue Alenick, Carmen George, Dawn Ellis, Andrew D. "
                   "Champagne, Mary-Katherine Stone, Robert \"Bob\" "
                   "Bolyard, Erin Kranichfeld, Theresa Lefebvre, "
                   "Amanda Janoo, Helaine \"Lainey\" Rappaport, "
                   "Robert Hooper, Owen Doherty, Ryan Nick, Zoraya "
                   "Hightower, and Gene Bergman.")],
           [holder("Sue Alenick", "sue-alenick"),
            holder("Carmen George", "carmen-george"),
            holder("Dawn Ellis", "dawn-ellis"),
            holder("Andrew D. Champagne", "andrew-d-champagne"),
            holder("Mary-Katherine Stone", "mary-katherine-stone"),
            holder("Robert Bolyard", "robert-bolyard",
                   ballot_name='Robert "Bob" Bolyard'),
            holder("Erin Kranichfeld", "erin-kranichfeld"),
            holder("Theresa Lefebvre", "theresa-lefebvre"),
            holder("Amanda Janoo", "amanda-janoo"),
            holder("Helaine Rappaport", "helaine-rappaport",
                   ballot_name='Helaine "Lainey" Rappaport'),
            holder("Robert Hooper", "robert-hooper",
                   existing_person_id="ocd-person/279486d1-303c-55f2-bc18-c2cfcb6c8ac3",
                   ballot_name="Robert Hooper"),
            holder("Owen Doherty", "owen-doherty"),
            holder("Ryan Nick", "ryan-nick"),
            holder("Zoraya Hightower", "zoraya-hightower"),
            holder("Gene Bergman", "gene-bergman")]),
], jp=jp_election("burlington-vt", "City of Burlington", 15,
                  "lists fifteen Burlington justices of the peace for "
                  "the 2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Cabot (general law)
# ------------------------------------------------------------------
CABOT_OFFICERS = {
    "url": "https://cabotvt.us/town-officiers/",
    "note": "PLACEHOLDER",
}
CABOT_SB = {
    "url": "https://cabotvt.us/selectboard/",
    "note": "PLACEHOLDER",
}
CABOT_MIN_JUL = {
    "url": "https://cabotvt.us/wp-content/uploads/2026/07/SELECTBOARD-MEETING-minutesdraft7.7.2026.pdf",
    "note": "PLACEHOLDER",
}
CABOT_MIN_JUN = {
    "url": "https://cabotvt.us/wp-content/uploads/2026/06/6.4.2026minutesdraft.pdf",
    "note": "PLACEHOLDER",
}
CABOT_MIN_MAR = {
    "url": "https://cabotvt.us/wp-content/uploads/2026/03/postedSB-Minutes-3.10.26.pdf",
    "note": "PLACEHOLDER",
}


def cabot_officers(what):
    return S(CABOT_OFFICERS, "Town of Cabot official website, Town "
             f"Officers page: {what}")


SPECS.append(spec("cabot", "Town of Cabot", [
    office("selectboard", "Selectboard Member", "Cabot Selectboard", 5,
           [sb_dir("lists five Cabot Selectboard members: Walter "
                   "(Skip) Bothfeld, Frederick Ducharme, Michael "
                   "Hogan (Vice Chair), Peggy Miller, and Jennifer "
                   "Miner (Chair)."),
            S(CABOT_SB, "Town of Cabot official website, Selectboard "
              "page: lists Jennifer Miner (Chair), Michael Hogan "
              "(Vice Chair), Peggy Miller, Fred Ducharme, and Walter "
              "(Skip) Bothfeld, Jr.")],
           [holder("Jennifer Miner", "jennifer-miner"),
            holder("Michael Hogan", "michael-hogan"),
            holder("Peggy Miller", "peggy-miller"),
            holder("Fred Ducharme", "fred-ducharme"),
            holder("Walter Bothfeld", "walter-bothfeld")]),
    office("town-clerk", "Town Clerk", "Cabot Town Clerk", 1,
           [cabot_officers("lists Town Clerk Brittany Butler, term "
                           "expires 2029."),
            S(CABOT_MIN_JUN, "Town of Cabot, Selectboard meeting "
              "minutes (June 4, 2026): signed 'Respectfully "
              "Submitted, Brittany Butler, Town Clerk'."),
            S(CABOT_MIN_JUL, "Town of Cabot, Selectboard meeting "
              "minutes (July 7, 2026): signed by Brittany Butler as "
              "Town Clerk."),
            guide("lists Betty Ritter as Town Clerk of Cabot; "
                  "Ritter signed the town's minutes through late "
                  "2025 and Butler signs them from spring 2026 -- "
                  "the January 2026 Guide is superseded by the "
                  "town's current records.")],
           [holder("Brittany Butler", "brittany-butler")]),
    office("town-treasurer", "Town Treasurer", "Cabot Town Treasurer", 1,
           [S(CABOT_MIN_JUL, "Town of Cabot, Selectboard meeting "
              "minutes (July 7, 2026): record the Selectboard Chair "
              "signing a three-year contract for Town Treasurer Amy "
              "Monahan -- the treasurer serves under contract with "
              "the Selectboard, not by election."),
            cabot_officers("lists Town Treasurer Amy Monahan with "
                           "term 'Non-Term'."),
            guide("lists Amy Monahan as Treasurer of Cabot.")],
           [holder("Amy Monahan", "amy-monahan",
                   how_seated="appointed")]),
    office("moderator", "Moderator", "Cabot Town Moderator", 1,
           [cabot_officers("lists Moderator Jeanne Johnson with a "
                           "printed term expiration of 2024. No "
                           "official source publishes the outcome of "
                           "a later election for the seat, so it is "
                           "left unfilled. Structure only.")]),
    office("lister", "Lister", "Cabot Listers", 3,
           [cabot_officers("lists Listers Brittany Butler (printed "
                           "term 2026), Jeanne Johnson (no term "
                           "printed), and Jacqueline Lumbra (printed "
                           "term 2026). The printed terms have run "
                           "out and no official source publishes the "
                           "current holders, so the seats are left "
                           "unfilled. Structure only.")]),
    office("delinquent-tax-collector", "Collector of Delinquent Taxes",
           "Cabot Collector of Delinquent Taxes", 1,
           [cabot_officers("lists Delinquent Tax Collector Susan "
                           "Carpenter with a printed term expiration "
                           "of 2025; the town fills the office "
                           "separately, so the post is created under "
                           "17 V.S.A. section 2651d. No official "
                           "source publishes the current holder, so "
                           "the seat is left unfilled. Structure "
                           "only.")]),
    office("grand-juror", "Grand Juror", "Cabot Grand Juror", 1,
           [cabot_officers("lists Grand Juror Dave Pike with a "
                           "printed term expiration of 2025. No "
                           "official source publishes the current "
                           "holder, so the seat is left unfilled."),
            statute2646("a grand juror")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Cabot Cemetery Commission", 5,
           [cabot_officers("lists five Cemetery Commissioners -- Deb "
                           "Bothfeld, Ruth Goodrich, Angela Ward, "
                           "Melvin Churchill (Chair), and Cedric "
                           "Alexander -- with printed term "
                           "expirations of 2025 and 2026. All of the "
                           "printed terms have run out and no "
                           "official source publishes the current "
                           "holders, so the seats are left unfilled. "
                           "Structure only.")]),
    office("first-constable", "First Constable", "Cabot First Constable", 1,
           [S(CABOT_MIN_MAR, "Town of Cabot, Selectboard meeting "
              "minutes (March 10, 2026): the Selectboard's annual "
              "appointments table appoints Stephen Hogan as 1st "
              "Constable (three-year term to 2029). He is a "
              "distinct person from Selectboard member Michael "
              "Hogan.")],
           [holder("Stephen Hogan", "stephen-hogan",
                   how_seated="appointed")]),
    office("second-constable", "Second Constable", "Cabot Second Constable", 1,
           [S(CABOT_MIN_MAR, "Town of Cabot, Selectboard meeting "
              "minutes (March 10, 2026): the Selectboard's annual "
              "appointments table appoints Nell McQuenney as 2nd "
              "Constable (three-year term to 2029).")],
           [holder("Nell McQuenney", "nell-mcquenney",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Cabot Justices of the Peace", 7,
           [jp_src("lists seven Cabot justices of the peace: Susan "
                   "Carpenter, Fred Ducharme, Cedric Alexander, "
                   "Caleb Pitkin, Carla Payne, Roman Kokodyniak, and "
                   "Judy Pransky."),
            {"url": "https://cabotvt.us",
             "note": "Town of Cabot official website, Justice of the "
                     "Peace page: names the same seven justices of "
                     "the peace."}],
           [holder("Susan Carpenter", "susan-carpenter"),
            holder("Fred Ducharme", "fred-ducharme"),
            holder("Cedric Alexander", "cedric-alexander"),
            holder("Caleb Pitkin", "caleb-pitkin"),
            holder("Carla Payne", "carla-payne"),
            holder("Roman Kokodyniak", "roman-kokodyniak"),
            holder("Judy Pransky", "judy-pransky")]),
], jp=jp_election("cabot-vt", "Town of Cabot", 7,
                  "lists seven Cabot justices of the peace for the "
                  "2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

for s in SPECS:
    path = OUT / f"{s['place_slug']}.json"
    path.write_text(json.dumps(s, indent=1, ensure_ascii=False))
    print("wrote", path)
print(f"{len(SPECS)} specs")
