"""Shared contest->post mapping for the NC county pass (issue #172)."""
import re, unicodedata

ROMAN = {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8",
         "I": "1", "II": "2", "III": "3", "IV": "4", "V": "5", "VI": "6", "VII": "7", "VIII": "8",
         "01": "1", "02": "2", "03": "3", "04": "4", "05": "5", "06": "6", "07": "7", "08": "8"}

def norm_name(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"[^a-z ]", "", s.lower())
    t = [x for x in s.split() if x not in ("jr", "sr", "ii", "iii", "iv")]
    if len(t) > 2 and len(t[1]) == 1:
        t = [t[0]] + t[2:]
    return " ".join(t)

def cslug(county):
    return county.lower().replace(" ", "-")

def contest_suffix(contest):
    m = re.search(r"(BOARD OF COMMISSIONERS|COUNTY COMMISSIONERS)(.*)$", contest.upper())
    return m.group(2).strip() if m else ""

def map_commissioner_post(posts_for_county, contest):
    """posts_for_county: list of post ids for the county. Returns post id or None."""
    suf = contest_suffix(contest)
    unexpired = "(UNEXPIRED)" in suf
    suf = suf.replace("(UNEXPIRED)", "").strip()
    tails = {p.split("/", 1)[1]: p for p in posts_for_county}
    def hit(tok):
        return tails.get(tok)
    if suf in ("", "AT-LARGE", "COUNTY-WIDE"):
        return hit("commissioner-at-large") or (posts_for_county[0] if len(posts_for_county) == 1 else None)
    if suf == "MEMBERS":
        return hit("commissioner-members")
    if suf == "CHAIRMAN":
        return hit("commissioner-chairman")
    m = re.match(r"(?:DISTRICT|DIST) ([0-9IVX]+)$", suf)
    if m:
        raw = m.group(1)
        n = ROMAN.get(raw)
        cands = [f"commissioner-district-{n}", f"commissioner-district-{raw.lower()}",
                 f"commissioner-district-{int(n):02d}"]
        for c in cands:
            if hit(c):
                return hit(c)
        return None
    m = re.match(r"DISTRICT ([A-C])$", suf)
    if m:
        return hit(f"commissioner-district-{m.group(1).lower()}")
    m = re.match(r"DISTRICT ([0-9]+) SEAT ([0-9]+)$", suf)
    if m:
        return hit(f"commissioner-district-{int(m.group(1)):02d}-seat-{int(m.group(2)):02d}")
    m = re.match(r"AT-LARGE SEAT ([0-9]+)$", suf)
    if m:
        return hit(f"commissioner-at-large-seat-{int(m.group(1)):02d}")
    if suf.endswith(" TWP") or suf.endswith(" TOWNSHIP"):
        base = re.sub(r" (TWP|TOWNSHIP)$", "", suf).lower().replace(" ", "-")
        return hit(f"commissioner-{base}-twp") or hit(f"commissioner-{base}-township")
    if suf.endswith(" DISTRICT"):
        base = suf[: -len(" DISTRICT")].lower().replace(" ", "-")
        return hit(f"commissioner-{base}-district")
    base = suf.lower().replace(" ", "-")
    return hit(f"commissioner-{base}")
