#!/usr/bin/env python3
"""Batch 5 of the VT #163 municipal fan-out (alphabetical positions
41-50): Calais, Cambridge (town), Cambridge (village), Canaan,
Castleton, Cavendish, Charleston, Charlotte, Chelsea, Chester.
Emits one JSON spec per municipality for build_vt_municipality.py.
Research: vt_muni_batch5_research.md.
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
                  f"(VT municipal batch 5); issue #163 "
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
                  f"# municipal fan-out batch 5; issue #163 "
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
# Calais (charter ch. 108C: treasurer and auditor appointed by the
# selectboard; 2026 official ballot + signed warning + town report)
# ------------------------------------------------------------------
CAL_BALLOT = {
    "url": "https://www.calaisvermont.gov/vertical/sites/%7B226D684E-C864-4AFA-B4A5-59BE32741B77%7D/uploads/Calais_Town_Meeting_Sample_Ballot(1).pdf",
    "note": "PLACEHOLDER",
}
CAL_WARNING = {
    "url": "https://calaisvermont.govoffice.com/vertical/Sites/%7B226D684E-C864-4AFA-B4A5-59BE32741B77%7D/uploads/Town_Meeting_Warning_2026_SIGNED.pdf",
    "note": "PLACEHOLDER",
}
CAL_CH = {
    "url": "https://legislature.vermont.gov/statutes/fullchapter/24APPENDIX/108C",
    "note": "PLACEHOLDER",
}
CAL_SITE = {
    "url": "https://www.calaisvermont.gov",
    "note": "PLACEHOLDER",
}
CAL_MINUTES_2024 = {
    "url": "https://www.calaisvermont.gov/vertical/sites/%7B226D684E-C864-4AFA-B4A5-59BE32741B77%7D/uploads/2024_Town_Meeting_Minutes_Approved_and_Signed(1).pdf",
    "note": "PLACEHOLDER",
}
CAL_SB_MIN_2026 = {
    "url": "https://www.calaisvermont.gov/uploads/dm/79490/SELECTBOARD_MINUTES_51826.pdf",
    "note": "PLACEHOLDER",
}


def cal_ch(what):
    return S(CAL_CH, "Town of Calais charter, Title 24 Appendix "
             f"V.S.A. chapter 108C (2017, No. M-11): {what}")


SPECS.append(spec("calais", "Town of Calais", [
    office("selectboard", "Selectboard Member", "Calais Selectboard", 5,
           [sb_dir("lists five Calais Selectboard members: William "
                   "Davis; Jordan Keyes (Chair); Barbara Mcandrew "
                   "[directory casing]; Christy Mihaly; and Jamie "
                   "Moorby (Vice Chair)."),
            S(CAL_BALLOT, "Town of Calais official ballot, Town "
              "Meeting March 3, 2026: Jordan Keyes was the candidate "
              "for the three-year Selectboard term and William Davis "
              "for the two-year term; both were elected.")],
           [holder("Jordan Keyes", "jordan-keyes"),
            holder("Barbara McAndrew", "barbara-mcandrew"),
            holder("William Davis", "william-davis"),
            holder("Christy Mihaly", "christy-mihaly"),
            holder("Jamie Moorby", "jamie-moorby")]),
    office("town-clerk", "Town Clerk", "Calais Town Clerk", 1,
           [guide("lists Teegan Dykeman-Brown as Town Clerk of "
                  "Calais."),
            S(CAL_BALLOT, "Town of Calais official ballot, Town "
              "Meeting March 3, 2026: Teegan Dykeman-Brown was the "
              "candidate for Town Clerk, three-year term ending "
              "March 2029; she was elected.")],
           [holder("Teegan Dykeman-Brown", "teegan-dykeman-brown")]),
    office("town-treasurer", "Town Treasurer", "Calais Town Treasurer", 1,
           [cal_ch("section 3 provides that the Selectboard shall "
                   "annually appoint a Town Treasurer, who is also "
                   "collector of current taxes."),
            guide("lists Kari Bradley as Treasurer of Calais.")],
           [holder("Kari Bradley", "kari-bradley",
                   how_seated="appointed")]),
    office("auditor", "Town Auditor", "Calais Town Auditor", 1,
           [cal_ch("section 4 provides that the Selectboard shall "
                   "annually appoint a Town Auditor, and shall "
                   "contract a certified public accountant audit at "
                   "least every three years."),
            S(CAL_SITE, "Town of Calais official website: the "
              "Selectboard's appointed auditor is the New England "
              "Municipal Resource Center, an accounting firm, not "
              "an individual; a firm cannot hold a person record, "
              "so the post is recorded with no membership.")]),
    office("moderator", "Moderator", "Calais Town Moderator", 1,
           [S(CAL_MINUTES_2024, "Town of Calais, approved minutes of "
              "the Annual Town Meeting, March 5, 2024: Gus Seelig "
              "was elected Moderator for the ensuing year."),
            S(CAL_SITE, "Town of Calais official website: the town's "
              "2026 Certificate of Votes records Gus Seelig "
              "re-elected Moderator at the Annual Town Meeting of "
              "March 3, 2026.")],
           [holder("Gus Seelig", "gus-seelig")]),
    office("lister", "Lister", "Calais Listers", 3,
           [S(CAL_SITE, "Town of Calais official website: the 2025 "
              "Town Report's town officers table lists three "
              "listers: Wilson Hughes, John McCullough, and Toby "
              "Talbot."),
            S(CAL_BALLOT, "Town of Calais official ballot, Town "
              "Meeting March 3, 2026: Toby Talbot was the candidate "
              "for Lister, three-year term ending March 2029; he "
              "was elected.")],
           [holder("Wilson Hughes", "wilson-hughes"),
            holder("John McCullough", "john-mccullough"),
            holder("Toby Talbot", "toby-talbot")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Calais Trustees of Public Funds", 3,
           [S(CAL_WARNING, "Town of Calais, Warning for the Annual "
              "Meeting of March 3, 2026 (signed): Article 3 elects "
              "a Trustee of Public Funds for a three-year term "
              "expiring 2029."),
            S(CAL_SITE, "Town of Calais official website: the 2025 "
              "Town Report lists three Trustees of Public Funds: "
              "Rodney A. Buck, Scott G. Grzankowski, and Steve "
              "Killoran; the town's 2026 Certificate of Votes "
              "records Buck (as 'Rod Buck') re-elected.")],
           [holder("Rodney A. Buck", "rodney-a-buck"),
            holder("Scott G. Grzankowski", "scott-g-grzankowski"),
            holder("Steve Killoran", "steve-killoran")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Calais Cemetery Commissioners", 5,
           [S(CAL_WARNING, "Town of Calais, Warning for the Annual "
              "Meeting of March 3, 2026 (signed): Article 3 elects "
              "a Cemetery Commissioner for a five-year term "
              "expiring 2031."),
            S(CAL_SITE, "Town of Calais official website: the 2025 "
              "Town Report lists five Cemetery Commissioners: "
              "Michael Fullerton, Juanita Nunn, Laura Dailey, Shari "
              "Fitch, and Sage Kennedy; Dailey was re-elected in "
              "2026.")],
           [holder("Michael Fullerton", "michael-fullerton"),
            holder("Juanita Nunn", "juanita-nunn"),
            holder("Laura Dailey", "laura-dailey"),
            holder("Shari Fitch", "shari-fitch"),
            holder("Sage Kennedy", "sage-kennedy")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Calais Collector of Delinquent Taxes", 1,
           [S(CAL_SB_MIN_2026, "Town of Calais, Selectboard meeting "
              "minutes, May 18, 2026: the Selectboard's annual "
              "appointments list includes 'Sandra Ferver: "
              "Delinquent Tax Collector.' The office is filled "
              "separately from the treasurer (17 V.S.A. section "
              "2651d); Ferver, the town's former elected treasurer, "
              "is recorded as the appointed holder.")],
           [holder("Sandra Ferver", "sandra-ferver",
                   how_seated="appointed")]),
    office("constable", "Constable", "Calais Constable", 1,
           [S(CAL_SITE, "Town of Calais official website: the 2025 "
              "Town Report's town officers roster prints the "
              "Constable office as VACANT. Structure only: the "
              "seat stands vacant and no holder is recorded.")]),
    office("grand-juror", "Grand Juror", "Calais Grand Juror", 1,
           [statute2646_structure("a grand juror")]),
    office("town-agent", "Town Agent", "Calais Town Agent", 1,
           [statute2646_structure("a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Calais Justices of the Peace", 7,
           [jp_src("lists seven Calais justices of the peace: Janet "
                   "Ancel, W. Scott Bassage, Charlotte Hanna "
                   "Bassage, Kristina Bielenberg, Barbara Butler, "
                   "Dillon Burns, and Michael Loignon.")],
           [holder("Janet Ancel", "janet-ancel"),
            holder("W. Scott Bassage", "w-scott-bassage"),
            holder("Charlotte Hanna Bassage",
                   "charlotte-hanna-bassage"),
            holder("Kristina Bielenberg", "kristina-bielenberg"),
            holder("Barbara Butler", "barbara-butler"),
            holder("Dillon Burns", "dillon-burns"),
            holder("Michael Loignon", "michael-loignon")]),
], jp=jp_election("calais-vt", "Town of Calais", 7,
                  "lists seven Calais justices of the peace for the "
                  "2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Cambridge TOWN (general law; Certificate of Votes, March 3, 2026,
# attested by the Town Clerk, is the roster of record)
# ------------------------------------------------------------------
CAM_CERT = {
    "url": "https://www.cambridge.vermont.gov/document_center/Clerk%20Office/Certificate%20of%20Votes%20March%203%202026.pdf?t=202603041351320",
    "note": "PLACEHOLDER",
}
CAM_LISTERS = {
    "url": "http://cms7.revize.com/revize/cambridgevt/directory/town_department/lister_s_office.php",
    "note": "PLACEHOLDER",
}


def cam_cert(what):
    return S(CAM_CERT, "Town of Cambridge, Certificate of Votes "
             "for the Annual Town Meeting, March 3, 2026 (attested "
             f"by Dana Warren, Town Clerk): {what}")


SPECS.append(spec("cambridge-11500", "Town of Cambridge", [
    office("selectboard", "Selectboard Member",
           "Cambridge Selectboard", 5,
           [sb_dir("lists five Cambridge Selectboard members: Toni "
                   "Bryce, Brooke Chouinard, Cody Marsh, Angela "
                   "Pratt, and Dan St Cyr."),
            cam_cert("Toni Bryce was elected to a three-year "
                     "Selectboard term and Brooke Chouinard to a "
                     "two-year term at the 2026 annual meeting.")],
           [holder("Toni Bryce", "toni-bryce"),
            holder("Brooke Chouinard", "brooke-chouinard"),
            holder("Cody Marsh", "cody-marsh"),
            holder("Angela Pratt", "angela-pratt"),
            holder("Dan St Cyr", "dan-st-cyr")]),
    office("town-clerk", "Town Clerk", "Cambridge Town Clerk", 1,
           [guide("lists Dana Warren as Town Clerk of Cambridge and "
                  "as Town Treasurer of Cambridge.")],
           [holder("Dana Warren", "dana-warren")]),
    office("town-treasurer", "Town Treasurer",
           "Cambridge Town Treasurer", 1,
           [guide("lists Dana Warren as Town Clerk of Cambridge and "
                  "as Town Treasurer of Cambridge.")],
           [holder("Dana Warren", "dana-warren")]),
    office("moderator", "Moderator", "Cambridge Town Moderator", 1,
           [cam_cert("Joel Page was elected Town Moderator for a "
                     "one-year term.")],
           [holder("Joel Page", "joel-page")]),
    office("auditor", "Auditor", "Cambridge Auditors", 3,
           [cam_cert("Donna Hutchins was elected Auditor for a "
                     "three-year term. The holders of the board's "
                     "other two seats are not published in any "
                     "official source read; they are left unfilled "
                     "rather than guessed.")],
           [holder("Donna Hutchins", "donna-hutchins")]),
    office("lister", "Lister", "Cambridge Listers", 3,
           [S(CAM_LISTERS, "Town of Cambridge official website, "
              "Listers' Office page: 'Listers: Cora Conly, Dale "
              "Copping, Suzanne Girouard.'"),
            cam_cert("Suzanne Girouard was re-elected Lister for a "
                     "three-year term.")],
           [holder("Cora Conly", "cora-conly"),
            holder("Dale Copping", "dale-copping"),
            holder("Suzanne Girouard", "suzanne-girouard")]),
    office("constable", "Constable", "Cambridge Constable", 1,
           [cam_cert("David Jones was elected Constable for a "
                     "one-year term.")],
           [holder("David Jones", "david-jones")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Cambridge Collector of Delinquent Taxes", 1,
           [cam_cert("Dana Warren was elected Delinquent Tax "
                     "Collector for a one-year term; the office is "
                     "filled separately (17 V.S.A. section "
                     "2651d).")],
           [holder("Dana Warren", "dana-warren")]),
    office("library-trustee", "Library Trustee",
           "Cambridge Library Trustees", 5,
           [cam_cert("Carol Plante was elected Library Trustee for "
                     "a five-year term and Cory Meier for a "
                     "two-year term. The holders of the board's "
                     "remaining seats are not published in any "
                     "current official source read; they are left "
                     "unfilled rather than guessed.")],
           [holder("Carol Plante", "carol-plante"),
            holder("Cory Meier", "cory-meier")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Cambridge Trustee of Public Funds", 1,
           [cam_cert("April Tuck was elected Trustee Public Funds "
                     "for a three-year term. Cambridge elects a "
                     "single trustee of public funds to successive "
                     "three-year terms (Elise Raymond was elected "
                     "in 2023); the post is recorded with one "
                     "seat.")],
           [holder("April Tuck", "april-tuck")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Cambridge Cemetery Commissioners", 5,
           [cam_cert("the Cemetery Commissioner five-year seat "
                     "drew 'No nominations' at the 2026 annual "
                     "meeting. Structure only: no official source "
                     "publishes the board's current holders.")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Cambridge Justices of the Peace", 9,
           [jp_src("lists nine Cambridge justices of the peace: "
                   "Cora Conly, Rosemary D'Elia, Linda Davis, Adam "
                   "Howard, Justin Marsh, Mark Nash, Jan Sander, "
                   "Mark Schilling, and Denise Webster. Justin "
                   "Marsh is a distinct person from Selectboard "
                   "member Cody Marsh.")],
           [holder("Cora Conly", "cora-conly"),
            holder("Rosemary D'Elia", "rosemary-delia"),
            holder("Linda Davis", "linda-davis"),
            holder("Adam Howard", "adam-howard"),
            holder("Justin Marsh", "justin-marsh"),
            holder("Mark Nash", "mark-nash"),
            holder("Jan Sander", "jan-sander"),
            holder("Mark Schilling", "mark-schilling"),
            holder("Denise Webster", "denise-webster")]),
], jp=jp_election("cambridge-11500-vt", "Town of Cambridge", 9,
                  "lists nine Cambridge justices of the peace for "
                  "the 2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Cambridge VILLAGE (charter ch. 213, section 21 fixes the officer
# set; the village publishes no official roster anywhere found --
# structure only, holders not guessed)
# ------------------------------------------------------------------
CAMV_CH = {
    "url": "https://legislature.vermont.gov/statutes/section/24APPENDIX/213/00021",
    "note": "PLACEHOLDER",
}


def camv_ch(what):
    return S(CAMV_CH, "Village of Cambridge charter, Title 24 "
             "Appendix V.S.A. chapter 213, section 21 (official "
             f"text, Vermont General Assembly): {what} Structure "
             "only: the village publishes no official roster on "
             "any website found, so no holder is recorded rather "
             "than guessed from an unofficial lead.")


SPECS.append(spec("cambridge", "Village of Cambridge", [
    office("trustee", "Village Trustee",
           "Cambridge Village Trustees", 3,
           [camv_ch("three Trustees are chosen by ballot at the "
                    "village's annual meeting, for one-year "
                    "terms.")]),
    office("village-clerk", "Village Clerk",
           "Cambridge Village Clerk", 1,
           [camv_ch("a Clerk is chosen by ballot at the annual "
                    "meeting.")]),
    office("village-treasurer", "Village Treasurer",
           "Cambridge Village Treasurer", 1,
           [camv_ch("a Treasurer is chosen by ballot at the "
                    "annual meeting.")]),
    office("collector-of-taxes", "Collector of Taxes",
           "Cambridge Village Collector of Taxes", 1,
           [camv_ch("a Collector of Taxes is chosen by ballot at "
                    "the annual meeting; under section 28 the "
                    "Collector is ex officio Chief of Police.")]),
    office("auditor", "Village Auditor",
           "Cambridge Village Auditor", 1,
           [camv_ch("one Auditor is chosen by ballot at the "
                    "annual meeting.")]),
    office("fire-marshal", "Fire Marshal",
           "Cambridge Village Fire Marshal", 1,
           [camv_ch("a Fire Marshal is chosen by ballot at the "
                    "annual meeting.")]),
]))

# ------------------------------------------------------------------
# Canaan (general law; the town's official "2026 Elected and
# Appointed Town Officials" PDF is the roster of record -- its
# first list is current; the same file also reproduces the 2024
# Annual Report's superseded list, which is not used)
# ------------------------------------------------------------------
CAN_PDF = {
    "url": "https://canaan-vt.org/images/Town_officials_2026.pdf",
    "note": "PLACEHOLDER",
}


def can_pdf(what):
    return S(CAN_PDF, "Town of Canaan official document, '2026 "
             f"Elected and Appointed Town Officials': {what}")


SPECS.append(spec("canaan", "Town of Canaan", [
    office("selectboard", "Selectboard Member", "Canaan Selectboard", 3,
           [sb_dir("lists three Canaan Selectboard members: Dillon "
                   "Begin (Chair), Alfred Buckley, and Alan Leigh "
                   "(board Clerk)."),
            can_pdf("Selectboard: Dillon G. Begin (Chair), Alfred "
                    "Buckley (Vice Chair), Alan B. Leigh.")],
           [holder("Dillon Begin", "dillon-begin"),
            holder("Alfred Buckley", "alfred-buckley"),
            holder("Alan Leigh", "alan-leigh")]),
    office("moderator", "Moderator", "Canaan Town Moderator", 1,
           [can_pdf("Moderator: Ashley Morgan Wade.")],
           [holder("Ashley Morgan Wade", "ashley-morgan-wade")]),
    office("town-clerk", "Town Clerk", "Canaan Town Clerk", 1,
           [guide("lists Zachary Brown as Town Clerk of Canaan and "
                  "as Town Treasurer of Canaan."),
            can_pdf("Town Clerk and Treasurer: Zachary William "
                    "Brown (the fuller form the town prints).")],
           [holder("Zachary Brown", "zachary-brown")]),
    office("town-treasurer", "Town Treasurer", "Canaan Town Treasurer", 1,
           [guide("lists Zachary Brown as Town Clerk of Canaan and "
                  "as Town Treasurer of Canaan."),
            can_pdf("Town Clerk and Treasurer: Zachary William "
                    "Brown (the fuller form the town prints).")],
           [holder("Zachary Brown", "zachary-brown")]),
    office("lister", "Lister", "Canaan Listers", 3,
           [can_pdf("Listers: Noreen J. Labrecque, Gordon (Tom) "
                    "Trammell, Tana Trammell. The nickname form is "
                    "the town's; the record carries the plain "
                    "name.")],
           [holder("Noreen Labrecque", "noreen-labrecque"),
            holder("Gordon Trammell", "gordon-trammell"),
            holder("Tana Trammell", "tana-trammell")]),
    office("auditor", "Auditor", "Canaan Auditors", 3,
           [can_pdf("Auditors: Fern Owen-Brown, Ursula Johnson, "
                    "Ginette Ladd.")],
           [holder("Fern Owen-Brown", "fern-owen-brown"),
            holder("Ursula Johnson", "ursula-johnson"),
            holder("Ginette Ladd", "ginette-ladd")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Canaan Collector of Delinquent Taxes", 1,
           [can_pdf("the Delinquent Tax Collector, Dencie "
                    "Cunningham, is listed in the document's "
                    "appointed-officers section; she is recorded "
                    "as an appointed holder of the separately "
                    "filled office (17 V.S.A. section 2651d).")],
           [holder("Dencie Cunningham", "dencie-cunningham",
                   how_seated="appointed")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Canaan Trustees of Public Funds", 3,
           [can_pdf("Trustees of Public Funds: Dencie Cunningham, "
                    "Zachary W. Brown, and one position printed "
                    "VACANT; the vacant seat is left unfilled.")],
           [holder("Dencie Cunningham", "dencie-cunningham"),
            holder("Zachary Brown", "zachary-brown")]),
    office("library-trustee", "Library Trustee",
           "Canaan Library Trustees", 5,
           [can_pdf("Library Trustees (elected board of five): "
                    "Sharon H. Belleville, Shellie Bresnahan, "
                    "Georgiana Carr, Nancy Petro, Kathy Smith.")],
           [holder("Sharon Belleville", "sharon-belleville"),
            holder("Shellie Bresnahan", "shellie-bresnahan"),
            holder("Georgiana Carr", "georgiana-carr"),
            holder("Nancy Petro", "nancy-petro"),
            holder("Kathy Smith", "kathy-smith")]),
    office("grand-juror", "Grand Juror", "Canaan Grand Juror", 1,
           [can_pdf("the Grand Juror, Fern Owen-Brown, is listed "
                    "in the document's appointed-officers section; "
                    "she is recorded as an appointed holder.")],
           [holder("Fern Owen-Brown", "fern-owen-brown",
                   how_seated="appointed")]),
    office("town-agent", "Town Agent", "Canaan Town Agent", 1,
           [can_pdf("the Town Agent, Ryan D. Porter, is listed in "
                    "the document's appointed-officers section; "
                    "he is recorded as an appointed holder.")],
           [holder("Ryan D. Porter", "ryan-d-porter",
                   how_seated="appointed")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Canaan Justices of the Peace", 5,
           [jp_src("lists five Canaan justices of the peace: Fern "
                   "Owen-Brown, Renee Marchesseault, Judith "
                   "Masson, Frank Sawicki Jr., and Katie Sawicki."),
            can_pdf("the town's officials list prints the same "
                    "five justices of the peace.")],
           [holder("Fern Owen-Brown", "fern-owen-brown"),
            holder("Renee Marchesseault", "renee-marchesseault"),
            holder("Judith Masson", "judith-masson"),
            holder("Frank Sawicki Jr.", "frank-sawicki-jr"),
            holder("Katie Sawicki", "katie-sawicki")]),
], jp=jp_election("canaan-vt", "Town of Canaan", 5,
                  "lists five Canaan justices of the peace for the "
                  "2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Castleton (general law; 2026 warning Art. 1 is the office set;
# clerk and treasurer in transition -- posts with no membership)
# ------------------------------------------------------------------
CAS_SB = {
    "url": "https://www.castletonvermont.org/select-board",
    "note": "PLACEHOLDER",
}
CAS_WARN = {
    "url": "https://www.castletonvermont.org/home/news/town-meeting-informational-meeting-take-note-changes",
    "note": "PLACEHOLDER",
}
CAS_SITE = {
    "url": "https://www.castletonvermont.org",
    "note": "PLACEHOLDER",
}


def cas_warn(what):
    return S(CAS_WARN, "Town of Castleton, Warning for the "
             f"Annual Town Meeting of March 3, 2026: {what}")


SPECS.append(spec("castleton", "Town of Castleton", [
    office("selectboard", "Selectboard Member",
           "Castleton Selectboard", 5,
           [sb_dir("lists five Castleton Selectboard members: Mark "
                   "Brown (Parlimentarian [sic]), Richard Combs "
                   "(Chairman), Mary Harris (Clerk), Robert "
                   "Spaulding (Vice Chairman), and Rob Steele."),
            S(CAS_SB, "Town of Castleton official website, "
              "Selectboard page: seats Richard Combs (Chairman), "
              "Robert Spaulding, Rob Steele (Vice Chairman), Mark "
              "Brown (Parlimentarian), and Mary Lee Harris (Board "
              "Clerk). The town's fuller form, Mary Lee Harris, "
              "is recorded; the Secretary of State directory "
              "prints Mary Harris.")],
           [holder("Mark Brown", "mark-brown"),
            holder("Richard Combs", "richard-combs"),
            holder("Mary Lee Harris", "mary-lee-harris"),
            holder("Robert Spaulding", "robert-spaulding"),
            holder("Rob Steele", "rob-steele")]),
    office("moderator", "Moderator", "Castleton Town Moderator", 1,
           [cas_warn("Article 1 elects a Moderator for a one-year "
                     "term. No official source publishes the 2026 "
                     "winner; the seat is left unfilled rather "
                     "than guessed. Structure only.")]),
    office("town-clerk", "Town Clerk", "Castleton Town Clerk", 1,
           [cas_warn("Article 1 elects a Town Clerk for a "
                     "three-year term, and Article 55 asked the "
                     "voters to authorize the Selectboard to "
                     "appoint the Town Clerk under 17 V.S.A. "
                     "section 2651e and eliminate the election."),
            guide("lists Janice Buxton as Castleton's Interim Town "
                  "Clerk."),
            S(CAS_SITE, "Town of Castleton official website: the "
              "elected Town Clerk, Nedra Boutwell, resigned "
              "effective December 19, 2025; the Selectboard "
              "called an April 16, 2026 special meeting to "
              "appoint a Town Clerk and Treasurer; job postings "
              "of July and September 2026 describe the office "
              "as Selectboard-appointed, and the October 12, "
              "2026 Selectboard agenda still lists the Town "
              "Clerk under 'Job vacancies update.' No current "
              "holder is verifiably published, so no membership "
              "is recorded.")]),
    office("town-treasurer", "Town Treasurer",
           "Castleton Town Treasurer", 1,
           [cas_warn("Article 56 asked the voters to authorize "
                     "the Selectboard to appoint the Town "
                     "Treasurer under 17 V.S.A. section 2651f and "
                     "eliminate the election."),
            guide("lists Abby Cohen as Treasurer of Castleton."),
            S(CAS_SITE, "Town of Castleton official website: the "
              "town's Treasurer page named Abbey Cohen, but the "
              "Selectboard's April 16, 2026 special meeting was "
              "called to appoint a Town Clerk and Treasurer, "
              "2026 job postings describe the office as "
              "Selectboard-appointed, and the October 12, 2026 "
              "agenda still lists the Treasurer under 'Job "
              "vacancies update.' No current holder is "
              "verifiably published, so no membership is "
              "recorded.")]),
    office("library-trustee", "Library Trustee",
           "Castleton Library Trustees", 5,
           [cas_warn("Article 1 elects Library Trustees to "
                     "five-year staggered terms (in 2026, one "
                     "five-year seat and one seat for the year "
                     "remaining of a five-year term). The board "
                     "is recorded with five seats; its current "
                     "holders are not published in any official "
                     "source read, so no memberships are "
                     "recorded.")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Castleton Justices of the Peace", 12,
           [jp_src("lists twelve Castleton justices of the peace: "
                   "Patricia Albin-Diercksen, Gerard Ashton, "
                   "Michael Bethel, Yvonne DeLance, Robert Grace, "
                   "Mary Beth Hadeka, Jennifer Jones, Toni "
                   "Lobdell, Deborah Rosmus, Laura Sargent, "
                   "Patricia Schroeder, and Lilian Sheren.")],
           [holder("Patricia Albin-Diercksen",
                   "patricia-albin-diercksen"),
            holder("Gerard Ashton", "gerard-ashton"),
            holder("Michael Bethel", "michael-bethel"),
            holder("Yvonne DeLance", "yvonne-delance"),
            holder("Robert Grace", "robert-grace"),
            holder("Mary Beth Hadeka", "mary-beth-hadeka"),
            holder("Jennifer Jones", "jennifer-jones"),
            holder("Toni Lobdell", "toni-lobdell"),
            holder("Deborah Rosmus", "deborah-rosmus"),
            holder("Laura Sargent", "laura-sargent"),
            holder("Patricia Schroeder", "patricia-schroeder"),
            holder("Lilian Sheren", "lilian-sheren")]),
], jp=jp_election("castleton-vt", "Town of Castleton", 12,
                  "lists twelve Castleton justices of the peace "
                  "for the 2025-2026 term; they are the winners of "
                  "the November 5, 2024 election for the office. "
                  "The listing publishes no vote totals and no "
                  "party designations for justices of the peace.")))

# ------------------------------------------------------------------
# Cavendish (general law under the ch. 109 Proctorsville merger
# charter; lister office eliminated -- absent from the town's own
# current elected-officials tables; most non-core seats stood for
# election in March 2026 with no published outcome)
# ------------------------------------------------------------------
CAV_BOARDS = {
    "url": "https://www.cavendishvt.com/boards-and-committees",
    "note": "PLACEHOLDER",
}
CAV_OFFICE = {
    "url": "https://www.cavendishvt.com/town-office",
    "note": "PLACEHOLDER",
}
CAV_REPORT22 = {
    "url": "https://static1.squarespace.com/static/5967f43a893fc01de256c378/t/63f7b487c4de2c3029cced69/1677177995917/2022+Town+Report.pdf",
    "note": "PLACEHOLDER",
}


def cav_structure(office_phrase, extra):
    return S(CAV_REPORT22, "Town of Cavendish, 2022 Town Report, "
             "Elected Officials table: the town's elected "
             f"offices include {office_phrase}. {extra} Structure "
             "only: the seat stood for election in March 2026 "
             "and no official source publishes the outcome.")


SPECS.append(spec("cavendish", "Town of Cavendish", [
    office("selectboard", "Selectboard Member",
           "Cavendish Selectboard", 5,
           [sb_dir("lists five Cavendish Selectboard members: "
                   "Shannon Devereux, Robert Glidden (Chairman), "
                   "David Norton, Michael Ripley, and Sandra "
                   "Russo."),
            S(CAV_BOARDS, "Town of Cavendish official website, "
              "Boards and Committees page: lists the same five "
              "Selectboard members (the site prints 'Robert W. "
              "Glidden' and 'Mike Ripley'). The page also states "
              "the Water Commissioners are appointed by the "
              "Selectboard and that the Selectboard sits as the "
              "Board of Sewer Commissioners, so no separate "
              "utility posts are created.")],
           [holder("Robert Glidden", "robert-glidden"),
            holder("Shannon Devereux", "shannon-devereux"),
            holder("David Norton", "david-norton"),
            holder("Michael Ripley", "michael-ripley"),
            holder("Sandra Russo", "sandra-russo")]),
    office("town-clerk", "Town Clerk", "Cavendish Town Clerk", 1,
           [S(CAV_OFFICE, "Town of Cavendish official website, "
              "Town Office page: 'Michael Murphy, Town Clerk and "
              "Treasurer.'"),
            guide("lists Diane McNamara as Town Clerk of "
                  "Cavendish and as Town Treasurer of Cavendish; "
                  "she did not stand for re-election in 2026, and "
                  "the town's current page governs.")],
           [holder("Michael Murphy", "michael-murphy")]),
    office("town-treasurer", "Town Treasurer",
           "Cavendish Town Treasurer", 1,
           [S(CAV_OFFICE, "Town of Cavendish official website, "
              "Town Office page: 'Michael Murphy, Town Clerk and "
              "Treasurer.'"),
            guide("lists Diane McNamara as Town Clerk of "
                  "Cavendish and as Town Treasurer of Cavendish; "
                  "she did not stand for re-election in 2026, and "
                  "the town's current page governs.")],
           [holder("Michael Murphy", "michael-murphy")]),
    office("moderator", "Moderator", "Cavendish Town Moderator", 1,
           [cav_structure("the Town Moderator",
                          "Michael Ripley was the incumbent "
                          "going into the 2026 election.")]),
    office("town-agent", "Town Agent", "Cavendish Town Agent", 1,
           [cav_structure("the Town Agent",
                          "The office was reported vacant going "
                          "into the 2026 election.")]),
    office("auditor", "Auditor", "Cavendish Auditors", 3,
           [cav_structure("the Auditors (three seats)",
                          "Andrew Amatutz held the one-year seat "
                          "going into the 2026 election; the "
                          "two-year and three-year seats were "
                          "reported vacant.")]),
    office("grand-juror", "Grand Juror", "Cavendish Grand Juror", 1,
           [cav_structure("the Town Grand Juror",
                          "Theresa McNamara was the incumbent "
                          "going into the 2026 election.")]),
    office("library-trustee", "Library Trustee",
           "Cavendish Library Trustees", 5,
           [cav_structure("the Library Trustees (five seats)",
                          "Christopher Saylor's five-year seat "
                          "stood for election in 2026.")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Cavendish Trustees of Public Funds", 3,
           [cav_structure("the Trustees of Public Funds",
                          "The seat warned in 2026 was reported "
                          "vacant.")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Cavendish Justices of the Peace", 5,
           [jp_src("lists five Cavendish justices of the peace: "
                   "Doris Jameson Eddy, Maureen Savage, "
                   "Christopher Saylor, John Smart, and Rolf van "
                   "Schaik. John Smart is the listing's form; the "
                   "town's older tables print Jack Smart.")],
           [holder("Doris Jameson Eddy", "doris-jameson-eddy"),
            holder("Maureen Savage", "maureen-savage"),
            holder("Christopher Saylor", "christopher-saylor"),
            holder("John Smart", "john-smart"),
            holder("Rolf van Schaik", "rolf-van-schaik")]),
], jp=jp_election("cavendish-vt", "Town of Cavendish", 5,
                  "lists five Cavendish justices of the peace for "
                  "the 2025-2026 term; they are the winners of the "
                  "November 5, 2024 election for the office. The "
                  "listing publishes no vote totals and no party "
                  "designations for justices of the peace.")))

# ------------------------------------------------------------------
# Charleston (general law; 2025 Annual Report officers table +
# official results of the March 3, 2026 annual meeting)
# CORRECTION (2026-10-18): the first transcription of the town's
# 2026 results sheet was erroneous and has been superseded by a
# verbatim transcription verified against the site's full-page
# preview image of the same PDF; it agrees with the Annual
# Report's term-expiry column seat for seat. The spec below
# follows the verified transcription. See issue #163.
# ------------------------------------------------------------------
CHA_REPORT = {
    "url": "https://charlestonvt.org/wp-content/uploads/2026/02/WEB_Charleston.pdf",
    "note": "PLACEHOLDER",
}
CHA_RESULTS = {
    "url": "https://charlestonvt.org/wp-content/uploads/2026/03/2026-Town-of-Charleston-Town-and-School-Results.pdf",
    "note": "PLACEHOLDER",
}
CHA_MINUTES_2025 = {
    "url": "https://charlestonvt.org/wp-content/uploads/2025/03/SBMinutes20250313.pdf",
    "note": "PLACEHOLDER",
}
CHA_HOME = {
    "url": "https://charlestonvt.org",
    "note": "PLACEHOLDER",
}


def cha_report(what):
    return S(CHA_REPORT, "Town of Charleston, 2025 Annual Report "
             f"(published February 2026), Town Officers table: "
             f"{what}")


def cha_results(what):
    return S(CHA_RESULTS, "Town of Charleston, official 'Results "
             "of 2026 Annual Town & School Meeting' (March 3, "
             f"2026): {what}")


SPECS.append(spec("charleston", "Town of Charleston", [
    office("selectboard", "Selectboard Member",
           "Charleston Selectboard", 3,
           [sb_dir("lists three Charleston Selectboard members: "
                   "Patrick Austin, Tim Jenness, and Terry "
                   "Rollins."),
            cha_report("Selectboard: Patrick Austin (expires "
                       "2028), Timothy Jenness (2026), Terry "
                       "Rollins (2027)."),
            cha_results("Timothy Jenness was elected Selectboard "
                        "member for a three-year term at the "
                        "2026 meeting, re-elected to the seat "
                        "his term expired on."),
            S(CHA_HOME, "Town of Charleston official website: the "
              "site's Select Board header names the board as "
              "Larry Allen, Patrick Austin, and Timothy Jenness "
              "(the board also serves as Road Commissioners). "
              "Allen is recorded as an appointed member, the "
              "statutory vacancy path (24 V.S.A. section 963), "
              "for the seat Rollins held to 2027 -- no election "
              "record names Allen, the June 2026 directory still "
              "prints Rollins, and Rollins is not recorded as a "
              "current member.")],
           [holder("Patrick Austin", "patrick-austin"),
            holder("Timothy Jenness", "timothy-jenness"),
            holder("Larry Allen", "larry-allen",
                   how_seated="appointed")]),
    office("town-clerk", "Town Clerk", "Charleston Town Clerk", 1,
           [guide("lists Teri Gray as Town Clerk of Charleston "
                  "and as Town Treasurer of Charleston."),
            cha_report("Town Clerk & Treasurer: Teri Gray, "
                       "three-year term expiring 2028.")],
           [holder("Teri Gray", "teri-gray")]),
    office("town-treasurer", "Town Treasurer",
           "Charleston Town Treasurer", 1,
           [guide("lists Teri Gray as Town Clerk of Charleston "
                  "and as Town Treasurer of Charleston."),
            cha_report("Town Clerk & Treasurer: Teri Gray, "
                       "three-year term expiring 2028.")],
           [holder("Teri Gray", "teri-gray")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Charleston Collector of Delinquent Taxes", 1,
           [cha_report("the officers tables place the Delinquent "
                       "Tax Collector, Teri Gray, among the "
                       "town's appointed officers."),
            S(CHA_MINUTES_2025, "Town of Charleston, Selectboard "
              "minutes, March 13, 2025: the minutes record that "
              "the voters approved appointing rather than "
              "electing a Delinquent Tax Collector, and that the "
              "Selectboard appointed Teri Gray to the office. "
              "The 2026 meeting's results record no election "
              "for the office.")],
           [holder("Teri Gray", "teri-gray",
                   how_seated="appointed")]),
    office("moderator", "Moderator", "Charleston Town Moderator", 1,
           [cha_report("Moderator: John Kellogg, one-year term "
                       "expiring 2026."),
            cha_results("Jean Wilson was elected School & Town "
                        "Moderator for a one-year term at the "
                        "2026 meeting; Kellogg, whose term "
                        "expired at that meeting, is not "
                        "recorded as the current moderator.")],
           [holder("Jean Wilson", "jean-wilson")]),
    office("lister", "Lister", "Charleston Listers", 3,
           [cha_report("Listers: Jean Wilson (2027), Steve Wilson "
                       "(2028), Robert Wilson (2026)."),
            S(CHA_MINUTES_2025, "Town of Charleston, Selectboard "
              "minutes, March 13, 2025: with none elected at Town "
              "Meeting to fill the remaining years of a "
              "three-year lister term, the Selectboard appointed "
              "Bob Wilson to the office until Town Meeting."),
            cha_results("Robert Wilson was elected Lister for a "
                        "three-year term at the 2026 meeting, "
                        "succeeding his appointment.")],
           [holder("Jean Wilson", "jean-wilson"),
            holder("Steve Wilson", "steve-wilson"),
            holder("Robert Wilson", "robert-wilson")]),
    office("auditor", "Auditor", "Charleston Auditors", 3,
           [cha_report("Town Auditors: Michael Morelli (2027), "
                       "Diana Marckwardt (2028), Janice Bowen "
                       "(2026)."),
            cha_results("Janice Bowen was re-elected Auditor for "
                        "a three-year term at the 2026 meeting.")],
           [holder("Michael Morelli", "michael-morelli"),
            holder("Diana Marckwardt", "diana-marckwardt"),
            holder("Janice Bowen", "janice-bowen")]),
    office("first-constable", "First Constable",
           "Charleston First Constable", 1,
           [cha_report("First Constable: Michael Tynio, "
                       "two-year term expiring 2027."),
            cha_results("the 2026 meeting's results record no "
                        "election for First Constable; Tynio's "
                        "two-year term runs to 2027.")],
           [holder("Michael Tynio", "michael-tynio")]),
    office("second-constable", "Second Constable",
           "Charleston Second Constable", 1,
           [cha_report("Second Constable: Natasha 'Anya' Tynio, "
                       "term expiring 2026. The town's results "
                       "sheet prints her name as Natasha Anya "
                       "Tynio, the form recorded here."),
            cha_results("Natasha Anya Tynio was elected Second "
                        "Constable for a one-year term at the "
                        "2026 meeting.")],
           [holder("Natasha Anya Tynio", "natasha-anya-tynio")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Charleston Cemetery Commissioners", 5,
           [cha_report("Cemetery Commissioners: Darald Moulton "
                       "(2026), Martin Davis (2027), Grace "
                       "Frizzell (2029), Janice Bowen (2028), "
                       "Sherman Allen, Jr. (2030)."),
            cha_results("Darald Moulton was re-elected Cemetery "
                        "Commissioner for a five-year term at "
                        "the 2026 meeting. The report table "
                        "accounts for all five seats of the "
                        "commission as so continued.")],
           [holder("Darald Moulton", "darald-moulton"),
            holder("Martin Davis", "martin-davis"),
            holder("Grace Frizzell", "grace-frizzell"),
            holder("Janice Bowen", "janice-bowen"),
            holder("Sherman Allen Jr.", "sherman-allen-jr")]),
    office("grand-juror", "Grand Juror", "Charleston Grand Juror", 1,
           [statute2646_structure("a grand juror")]),
    office("town-agent", "Town Agent", "Charleston Town Agent", 1,
           [statute2646_structure("a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Charleston Justices of the Peace", 5,
           [jp_src("lists five Charleston justices of the peace: "
                   "Benjamin Applegate, Carolyn Hannan, Samantha "
                   "Stevens, Amy Wagner, and Jean Wilson."),
            cha_report("the Justices of the Peace list (terms to "
                       "January 31, 2027) prints the same five "
                       "names.")],
           [holder("Benjamin Applegate", "benjamin-applegate"),
            holder("Carolyn Hannan", "carolyn-hannan"),
            holder("Samantha Stevens", "samantha-stevens"),
            holder("Amy Wagner", "amy-wagner"),
            holder("Jean Wilson", "jean-wilson")]),
], jp=jp_election("charleston-vt", "Town of Charleston", 5,
                  "lists five Charleston justices of the peace "
                  "for the 2025-2026 term; they are the winners of "
                  "the November 5, 2024 election for the office. "
                  "The listing publishes no vote totals and no "
                  "party designations for justices of the peace.")))

# ------------------------------------------------------------------
# Charlotte (general law -- the ch. 110 charter was repealed in
# 2015; Selectboard settled by the town's March 9, 2026 minutes;
# several holders rest on the town newspaper's 2026 results
# reporting, disclosed in the notes and on issue #163)
# ------------------------------------------------------------------
CHO_MINUTES = {
    "url": "https://charlottevt.org/vertical/sites/%7B797C5C63-8973-48DF-A5F9-82DC6FAE7EDF%7D/uploads/3-March_9_2026_DRAFT_SELECTBOARD__MEETING_MINUTES_.pdf",
    "note": "PLACEHOLDER",
}
CHO_REPORT22 = {
    "url": "https://charlottevt.org/vertical/sites/%7B5618C1B5-BAB5-4588-B4CF-330F32AA3E59%7D/uploads/Final_Report_2022.pdf",
    "note": "PLACEHOLDER",
}
CHO_NEWS_APR = {
    "url": "https://www.charlottenewsvt.org/2026/04/16/selectboard-buys-signs-appoints-auditor-talks-budget/",
    "note": "PLACEHOLDER",
}


def cho_report22(what):
    return S(CHO_REPORT22, "Town of Charlotte, 2022 Annual Town "
             f"Report, Elected Town Officers table: {what}")


SPECS.append(spec("charlotte", "Town of Charlotte", [
    office("selectboard", "Selectboard Member",
           "Charlotte Selectboard", 5,
           [S(CHO_MINUTES, "Town of Charlotte, Selectboard "
              "meeting minutes, March 9, 2026: 'Lee Krohn "
              "welcomed Troy Krahl as a new member of the "
              "Selectboard, elected for a three-year term'; the "
              "organizational votes elected Natalie Kanner "
              "Chair and Frank Tenney Vice Chair. The board is "
              "Kanner, Tenney, Krahl, Krohn, and J.D. Herlihy. "
              "The Selectboard directory's Charlotte entry was "
              "cut off at a page turn in extraction, but it "
              "lists Troy Krahl with a three-year term, "
              "agreeing. (The signature block of the town's "
              "August 2026 Committee Handbook still names the "
              "pre-election board with Krohn as Chair; it "
              "reproduces the 2024-2025 signature page verbatim "
              "and is a template carryover, not the current "
              "roster.)")],
           [holder("Natalie Kanner", "natalie-kanner"),
            holder("Frank Tenney", "frank-tenney"),
            holder("Troy Krahl", "troy-krahl"),
            holder("Lee Krohn", "lee-krohn"),
            holder("J.D. Herlihy", "jd-herlihy")]),
    office("town-clerk", "Town Clerk", "Charlotte Town Clerk", 1,
           [guide("lists Mary Mead as Town Clerk of Charlotte "
                  "and as Town Treasurer of Charlotte.")],
           [holder("Mary Mead", "mary-mead")]),
    office("town-treasurer", "Town Treasurer",
           "Charlotte Town Treasurer", 1,
           [guide("lists Mary Mead as Town Clerk of Charlotte "
                  "and as Town Treasurer of Charlotte.")],
           [holder("Mary Mead", "mary-mead")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Charlotte Collector of Delinquent Taxes", 1,
           [cho_report22("Delinquent Tax Collector: Mary A. Mead "
                         "(one-year term)."),
            S(CHO_NEWS_APR, "The Charlotte News, April 16, 2026, "
              "reporting a Selectboard meeting: Mead reported on "
              "the town's delinquent taxes in her capacity as "
              "collector. The News' March 2026 town-meeting "
              "results report her re-elected Delinquent Tax "
              "Collector; the town publishes no results document "
              "of its own that could be found, and the "
              "newspaper reporting is uncontradicted.")],
           [holder("Mary Mead", "mary-mead")]),
    office("moderator", "Moderator", "Charlotte Town Moderator", 1,
           [cho_report22("Moderator (Town): Charlie Russell "
                         "(one-year term)."),
            S(CHO_NEWS_APR, "The Charlotte News' March 2026 "
              "town-meeting results report Charlie Russell "
              "re-elected Moderator; Russell was also styled "
              "the town moderator in the News' January 2026 "
              "reporting. The town publishes no results document "
              "of its own that could be found.")],
           [holder("Charlie Russell", "charlie-russell")]),
    office("road-commissioner", "Road Commissioner",
           "Charlotte Road Commissioner", 1,
           [cho_report22("the town's posted election results "
                         "list 'Road Commissioner (1 Year): Hugh "
                         "Lewis Jr.'"),
            S(CHO_NEWS_APR, "The Charlotte News' March 2026 "
              "town-meeting results report Hugh Lewis Jr. "
              "re-elected Road Commissioner. The town publishes "
              "no results document of its own that could be "
              "found.")],
           [holder("Hugh Lewis Jr.", "hugh-lewis-jr")]),
    office("auditor", "Auditor", "Charlotte Auditors", 3,
           [S(CHO_NEWS_APR, "The Charlotte News, April 16, 2026: "
              "'Patrice Machavern will continue as a town "
              "auditor until an election in March 2027,' "
              "appointed by the Selectboard to a vacancy after "
              "the March 2026 auditor contest drew no elected "
              "winner. The town's Board of Auditors is a live "
              "elected body (the town posted notice of its "
              "January 22, 2026 annual meeting). The holders of "
              "the board's other two seats are not published "
              "in any current source read.")],
           [holder("Patrice Machavern", "patrice-machavern",
                   how_seated="appointed")]),
    office("library-trustee", "Library Trustee",
           "Charlotte Library Trustees", 5,
           [cho_report22("Charlotte Library Trustees serve "
                         "five-year staggered terms (the table "
                         "lists one term expiring each year)."),
            S(CHO_NEWS_APR, "The Charlotte News' March 2026 "
              "town-meeting results report Cecelia Wu elected "
              "Library Trustee to a five-year term. Janice "
              "Heilmann's term, per the town report table, "
              "expires in 2027, so she remains seated; the "
              "holders of the board's remaining seats are not "
              "published in any current source read.")],
           [holder("Cecelia Wu", "cecelia-wu"),
            holder("Janice Heilmann", "janice-heilmann")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Charlotte Cemetery Commissioners", 3,
           [cho_report22("Cemetery Commissioners serve "
                         "three-year staggered terms."),
            S(CHO_NEWS_APR, "The Charlotte News' March 2026 "
              "results report the Cemetery Commissioner "
              "three-year contest as 'Write-in vacant.' "
              "Structure only: no current holder is verifiably "
              "published.")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Charlotte Trustees of Public Funds", 3,
           [S(CHO_NEWS_APR, "The Charlotte News' March 2026 "
              "results report the Trustee of Public Funds "
              "three-year contest as 'Write-in vacant'; the "
              "town's report table shows the board's three "
              "staggered seats. Structure only: no current "
              "holder is verifiably published.")]),
    office("grand-juror", "Grand Juror", "Charlotte Grand Juror", 1,
           [statute2646_structure("a grand juror")]),
    office("town-agent", "Town Agent", "Charlotte Town Agent", 1,
           [statute2646_structure("a town agent")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Charlotte Justices of the Peace", 12,
           [jp_src("lists twelve Charlotte justices of the "
                   "peace: Jill Abilock, Greg Cluff, Lorna "
                   "Jimerson, Chea Waters Evans, Michael "
                   "Krasnow, Elizabeth Langfeldt, Robin Reid, "
                   "Heather Roberts, Peggy Sharpe, Carrie Spear, "
                   "Mike Yantachka, and Seth Zimmerman. Chea "
                   "Waters Evans is the sitting State "
                   "Representative for the Chittenden-5 district "
                   "(Charlotte); her existing person record is "
                   "reused.")],
           [holder("Jill Abilock", "jill-abilock"),
            holder("Greg Cluff", "greg-cluff"),
            holder("Lorna Jimerson", "lorna-jimerson"),
            holder("Chea Waters Evans", "chea-waters-evans",
                   existing_person_id="ocd-person/8ad2ba30-c495-53bc-998e-a4b0f902ca31",
                   ballot_name="Chea Waters Evans"),
            holder("Michael Krasnow", "michael-krasnow"),
            holder("Elizabeth Langfeldt", "elizabeth-langfeldt"),
            holder("Robin Reid", "robin-reid"),
            holder("Heather Roberts", "heather-roberts"),
            holder("Peggy Sharpe", "peggy-sharpe"),
            holder("Carrie Spear", "carrie-spear"),
            holder("Mike Yantachka", "mike-yantachka"),
            holder("Seth Zimmerman", "seth-zimmerman")]),
], jp=jp_election("charlotte-vt", "Town of Charlotte", 12,
                  "lists twelve Charlotte justices of the peace "
                  "for the 2025-2026 term; they are the winners "
                  "of the November 5, 2024 election for the "
                  "office. The listing publishes no vote totals "
                  "and no party designations for justices of the "
                  "peace.")))

# ------------------------------------------------------------------
# Chelsea (general law; the town website, chelseavt.us, fails DNS
# resolution in both fetchers -- the Brunswick treatment: SOS
# sources only)
# ------------------------------------------------------------------
# Chelsea (general law; the town's official website is
# chelseavt.org -- the chelseavt.us domain does not resolve.
# CORRECTION (2026-10-18): Chelsea was first built SOS-only on
# the mistaken belief that the town had no reachable website;
# its site in fact publishes its elective offices and current
# holders, and the spec follows it. The town's own "2026
# Election Results" PDF could not be fetched, so seats that
# stood in March 2026 rest on the town's current pages for
# currency, as noted. See issue #163.)
# ------------------------------------------------------------------
CHE_VOTE = {
    "url": "https://www.chelseavt.org/voting-elections/",
    "note": "PLACEHOLDER",
}
CHE_CONTACTS = {
    "url": "https://www.chelseavt.org/contacts/",
    "note": "PLACEHOLDER",
}
CHE_SB_PAGE = {
    "url": "https://www.chelseavt.org/board-committee/selectboard/",
    "note": "PLACEHOLDER",
}
CHE_CEM = {
    "url": "https://www.chelseavt.org/board-committee/cemetery-commission/",
    "note": "PLACEHOLDER",
}
CHE_NEWS25 = {
    "url": "https://www.chelseavt.org/category/news/page/11/",
    "note": "PLACEHOLDER",
}


def che_vote(what):
    return S(CHE_VOTE, "Town of Chelsea official website, Voting "
             f"& Elections page, 'Town Offices up for Election' "
             f"table for 2026: {what}")


def che_2025(what):
    return S(CHE_NEWS25, "Town of Chelsea official website, town "
             "news post 'Congratulations to Chelsea's 2025 "
             f"elected officials!' (March 2025): {what}")


SPECS.append(spec("chelsea", "Town of Chelsea", [
    office("selectboard", "Selectboard Member",
           "Chelsea Selectboard", 5,
           [sb_dir("lists five Chelsea Selectboard members: "
                   "Carrie Caouette-De Lallo, Curtis Chase (Vice "
                   "Chair), Gregg Herrin (Chair), Paul Libby, "
                   "and Charles Peel."),
            S(CHE_CONTACTS, "Town of Chelsea official website, "
              "Contacts page: lists the same five Selectboard "
              "members with the same roles (Herrin Chair, Chase "
              "Vice Chair)."),
            S(CHE_SB_PAGE, "Town of Chelsea official website, "
              "Selectboard page: its liaison assignments and "
              "member contacts name the same five members.")],
           [holder("Carrie Caouette-De Lallo",
                   "carrie-caouette-de-lallo"),
            holder("Curtis Chase", "curtis-chase"),
            holder("Gregg Herrin", "gregg-herrin"),
            holder("Paul Libby", "paul-libby"),
            holder("Charles Peel", "charles-peel")]),
    office("town-clerk", "Town Clerk", "Chelsea Town Clerk", 1,
           [guide("lists Jennifer Chase as Town Clerk of "
                  "Chelsea."),
            S(CHE_CONTACTS, "Town of Chelsea official website, "
              "Contacts page: 'Town Clerk: Jennifer Chase.'")],
           [holder("Jennifer Chase", "jennifer-chase")]),
    office("town-treasurer", "Town Treasurer",
           "Chelsea Town Treasurer", 1,
           [guide("lists Gayle Durkee as Treasurer of "
                  "Chelsea."),
            S(CHE_CONTACTS, "Town of Chelsea official website, "
              "Contacts page: 'Treasurer & Delinquent Tax "
              "Collector: Gayle Durkee.'")],
           [holder("Gayle Durkee", "gayle-durkee")]),
    office("collector-of-delinquent-taxes",
           "Collector of Delinquent Taxes",
           "Chelsea Collector of Delinquent Taxes", 1,
           [che_2025("the town's 2025 elected officials include "
                     "'Treasurer and Delinquent Tax Collector: "
                     "Gayle Durkee' -- the office is elective in "
                     "Chelsea and separately filled (17 V.S.A. "
                     "section 2651d)."),
            che_vote("lists the Delinquent Tax Collector among "
                     "the offices up for election in 2026 "
                     "(one-year term), incumbent Gayle Durkee."),
            S(CHE_CONTACTS, "Town of Chelsea official website, "
              "Contacts page: 'Treasurer & Delinquent Tax "
              "Collector: Gayle Durkee' (current). The town's "
              "own 2026 results document could not be fetched; "
              "her currency rests on the town's live contacts "
              "page.")],
           [holder("Gayle Durkee", "gayle-durkee")]),
    office("moderator", "Moderator", "Chelsea Town Moderator", 1,
           [che_2025("the town's 2025 elected officials include "
                     "Moderator Emily Marshia (one-year term)."),
            che_vote("lists the Moderator among the offices up "
                     "for election in 2026 (one-year term), "
                     "incumbent Emily Marshia. Her term expired "
                     "at the March 2026 meeting and no source "
                     "read publishes the outcome, so the seat is "
                     "left unfilled rather than guessed. "
                     "Structure only.")]),
    office("lister", "Lister", "Chelsea Listers", 3,
           [che_2025("the town's 2025 elected officials include "
                     "Lister Phyllis Hayward; listers serve "
                     "three-year staggered terms, and her seat "
                     "was not among those up in 2026."),
            che_vote("lists two lister seats up in 2026: a "
                     "three-year seat, incumbent Susan Elder, "
                     "and a one-year remainder seat, vacant. The "
                     "remainder seat's outcome is not published "
                     "in any source read and is left unfilled."),
            S(CHE_CONTACTS, "Town of Chelsea official website, "
              "Contacts page (current): 'Listers: Phyllis "
              "Hayward, Susan Elder.'")],
           [holder("Phyllis Hayward", "phyllis-hayward"),
            holder("Susan Elder", "susan-elder")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Chelsea Trustees of Public Funds", 3,
           [che_2025("the town's 2025 elected officials include "
                     "'Trustee of the Public Money: David "
                     "Bradshaw.' One trustee is elected each "
                     "year to a three-year term (the 2026 table "
                     "shows one three-year seat up), so the "
                     "board is recorded with three seats."),
            che_vote("lists a Trustee of Public Funds seat "
                     "(three-year term) up in 2026, incumbent "
                     "Edwin Coburn. His seat's outcome is not "
                     "published in any source read, so he is not "
                     "recorded; Bradshaw, elected in 2025 to a "
                     "term running to 2028, is.")],
           [holder("David Bradshaw", "david-bradshaw")]),
    office("cemetery-commissioner", "Cemetery Commissioner",
           "Chelsea Cemetery Commissioners", 5,
           [che_2025("the town's 2025 elected officials list "
                     "includes the Cemetery Commissioner among "
                     "the elective offices ('Cemetery "
                     "Commissioner: None (not enough votes)' in "
                     "2025). One commissioner is elected each "
                     "year to a five-year term (the 2026 table "
                     "shows one five-year seat up), so the "
                     "commission is recorded with five seats; "
                     "the seat that drew no election in 2025 is "
                     "left unfilled."),
            che_vote("lists a Cemetery Commissioner seat "
                     "(five-year term) up in 2026, incumbent "
                     "Steve Knudsen."),
            S(CHE_CEM, "Town of Chelsea official website, "
              "Cemetery Commission page: its current personnel "
              "are Frank Keene, Shannon Doyle, Steven Knudsen, "
              "and Terry Carty. The election table prints "
              "'Steve Knudsen'; the commission's own page "
              "prints Steven Knudsen, the form recorded "
              "here.")],
           [holder("Frank Keene", "frank-keene"),
            holder("Shannon Doyle", "shannon-doyle"),
            holder("Steven Knudsen", "steven-knudsen"),
            holder("Terry Carty", "terry-carty")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Chelsea Justices of the Peace", 5,
           [jp_src("lists five Chelsea justices of the peace: "
                   "David Bradshaw, Susan A. Kay, Tracy S. "
                   "Simon, Joseph L. Spinella, and Emily "
                   "Marshia.")],
           [holder("David Bradshaw", "david-bradshaw"),
            holder("Susan A. Kay", "susan-a-kay"),
            holder("Tracy S. Simon", "tracy-s-simon"),
            holder("Joseph L. Spinella", "joseph-l-spinella"),
            holder("Emily Marshia", "emily-marshia")]),
], jp=jp_election("chelsea-vt", "Town of Chelsea", 5,
                  "lists five Chelsea justices of the peace for "
                  "the 2025-2026 term; they are the winners of "
                  "the November 5, 2024 election for the office. "
                  "The listing publishes no vote totals and no "
                  "party designations for justices of the peace.")))


# ------------------------------------------------------------------
# Chester (general law under the ch. 111 merger charter; the
# town's own elective-offices post fixes the office set)
# ------------------------------------------------------------------
CHE_SB = {
    "url": "https://www.chestervt.gov/select-board.html",
    "note": "PLACEHOLDER",
}
CHE_POST = {
    "url": "https://www.chestervt.gov/latest-news/previous/7",
    "note": "PLACEHOLDER",
}


def che_structure(office_phrase):
    return S(CHE_POST, "Town of Chester official website, "
             "'Elective Offices' post: the town's elective "
             f"offices include {office_phrase}. Structure only: "
             "no official source publishes the current holder; "
             "the seat is left unfilled rather than guessed.")


SPECS.append(spec("chester", "Town of Chester", [
    office("selectboard", "Selectboard Member",
           "Chester Selectboard", 5,
           [sb_dir("lists five Chester Selectboard members: "
                   "Lauren Fierman, A Lee Gustafson (Chair), "
                   "Peter Hudkins, Arne Jonynas, and Timothy "
                   "Roper."),
            S(CHE_SB, "Town of Chester official website, Select "
              "Board page: lists Lee Gustafson (Chair), Arunas "
              "'Arne' Jonynas (Vice Chair), Tim Roper, Peter "
              "Hudkins, and Lauren Fierman. The directory forms "
              "recorded here are A Lee Gustafson, Arne Jonynas, "
              "and Timothy Roper.")],
           [holder("A Lee Gustafson", "a-lee-gustafson"),
            holder("Arne Jonynas", "arne-jonynas"),
            holder("Timothy Roper", "timothy-roper"),
            holder("Peter Hudkins", "peter-hudkins"),
            holder("Lauren Fierman", "lauren-fierman")]),
    office("town-clerk", "Town Clerk", "Chester Town Clerk", 1,
           [guide("lists Amie Record as Town Clerk of Chester "
                  "and as Town Treasurer of Chester.")],
           [holder("Amie Record", "amie-record")]),
    office("town-treasurer", "Town Treasurer",
           "Chester Town Treasurer", 1,
           [guide("lists Amie Record as Town Clerk of Chester "
                  "and as Town Treasurer of Chester.")],
           [holder("Amie Record", "amie-record")]),
    office("moderator", "Moderator", "Chester Town Moderator", 1,
           [che_structure("a Town Moderator, one-year term")]),
    office("grand-juror", "Grand Juror", "Chester Grand Juror", 1,
           [che_structure("a Town Grand Juror, one-year term")]),
    office("town-agent", "Town Agent (Agent to Defend Suits)",
           "Chester Town Agent", 1,
           [che_structure("an Agent to Defend Suits, one-year "
                          "term -- the town agent under the "
                          "styling Chester's elective-offices "
                          "post uses")]),
    office("trustee-of-public-funds", "Trustee of Public Funds",
           "Chester Trustees of Public Funds", 3,
           [che_structure("Trustees of Public Funds, one "
                          "three-year seat elected each year")]),
    office("justice-of-the-peace", "Justice of the Peace",
           "Chester Justices of the Peace", 12,
           [jp_src("lists twelve Chester justices of the peace: "
                   "Kenneth D. Barrett, Patricia Budnick, "
                   "Heather Chase, Lisa Duncan, Gerald Gleason, "
                   "Edward Grossman, Jessica Krust, Cheryl "
                   "LeClair, Marilyn Mahusky, Russell Monier, "
                   "Larry Semones, and Sarah Vail. Heather Chase "
                   "is a distinct person from Chelsea Town Clerk "
                   "Jennifer Chase and Chelsea Selectboard "
                   "member Curtis Chase.")],
           [holder("Kenneth D. Barrett", "kenneth-d-barrett"),
            holder("Patricia Budnick", "patricia-budnick"),
            holder("Heather Chase", "heather-chase"),
            holder("Lisa Duncan", "lisa-duncan"),
            holder("Gerald Gleason", "gerald-gleason"),
            holder("Edward Grossman", "edward-grossman"),
            holder("Jessica Krust", "jessica-krust"),
            holder("Cheryl LeClair", "cheryl-leclair"),
            holder("Marilyn Mahusky", "marilyn-mahusky"),
            holder("Russell Monier", "russell-monier"),
            holder("Larry Semones", "larry-semones"),
            holder("Sarah Vail", "sarah-vail")]),
], jp=jp_election("chester-vt", "Town of Chester", 12,
                  "lists twelve Chester justices of the peace "
                  "for the 2025-2026 term; they are the winners "
                  "of the November 5, 2024 election for the "
                  "office. The listing publishes no vote totals "
                  "and no party designations for justices of the "
                  "peace.")))

for s in SPECS:
    path = OUT / f"{s['place_slug']}.json"
    path.write_text(json.dumps(s, indent=1, ensure_ascii=False))
    print("wrote", path)
print(f"{len(SPECS)} specs")
