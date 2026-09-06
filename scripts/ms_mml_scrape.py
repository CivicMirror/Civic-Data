#!/usr/bin/env python3
"""
mml_scrape.py  —  CivicMirror / MS municipal audit
Populate the "City Website" column (Municipalities!G) from the Mississippi
Municipal League per-city pages.

WHY THIS SOURCE: each MML member page exposes the city's *official* website
(the "Web" link under "Connect with us"), so MML is used only to LOCATE the
official site — the value stored is the city's own URL. It also carries phone,
population, next election date, and the elected officials roster (bonus columns
for later officeholder backfill).

COVERAGE: ~290 of 299 municipalities are MML members. Non-members / pages with
no Web link are written with website="" and status="NOT FOUND" for manual review.

RUN LOCALLY (MML returns 503 to datacenter IPs; a normal machine is fine):
    pip install requests openpyxl beautifulsoup4
    python mml_scrape.py --xlsx MS_Municipalities.xlsx --out ms_city_websites.csv
    # optional: also write the URLs straight into column G of a copy:
    python mml_scrape.py --xlsx MS_Municipalities.xlsx --write-xlsx MS_Municipalities_websites.xlsx

Then send me ms_city_websites.csv and I'll merge + push, or use --write-xlsx.
"""
import argparse, csv, re, sys, time
import requests
from bs4 import BeautifulSoup

BASE = "https://www.mmlonline.com/members/municipalities/{slug}/"
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def slugs_for(name: str):
    """MML slugs are the display name with spaces -> hyphens. Yield a few
    variants to cover apostrophes and punctuation quirks (D'Iberville, D'Lo,
    Bay St Louis, etc.)."""
    n = name.strip()
    base = n.replace(" ", "-")
    variants = [
        base,                                  # Bay-St-Louis, D'Iberville
        base.replace("'", ""),                 # DIberville, DLo
        base.replace("'", "-"),                # D-Iberville
        re.sub(r"[^A-Za-z0-9-]", "", base),    # strip stray punctuation
        n.replace(" ", ""),                    # BaySaintLouis fallback
    ]
    seen, out = set(), []
    for v in variants:
        if v and v not in seen:
            seen.add(v); out.append(v)
    return out

def fetch(slug, tries=3):
    url = BASE.format(slug=slug)
    for i in range(tries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200 and "Government Contacts" in r.text:
                return r.text
            if r.status_code == 404:
                return None
        except requests.RequestException:
            pass
        time.sleep(1.5 * (i + 1))
    return None

def parse(html):
    """Extract official website + bonus fields from an MML city page."""
    soup = BeautifulSoup(html, "html.parser")
    out = {"website": "", "phone": "", "population": "", "next_election": "", "officials": ""}

    # Official website: anchor whose <img> src is the Internet_Icon, or the
    # link immediately labeled "Web".
    for a in soup.find_all("a", href=True):
        img = a.find("img")
        if img and "Internet_Icon" in (img.get("src") or ""):
            out["website"] = a["href"].strip(); break
    if not out["website"]:
        for a in soup.find_all("a", href=True):
            if a.get_text(strip=True).lower() == "web":
                out["website"] = a["href"].strip(); break

    text = soup.get_text("\n")
    def after(label):
        m = re.search(re.escape(label) + r"\s*[:\n]\s*([^\n]+)", text)
        return m.group(1).strip() if m else ""
    out["phone"]         = after("Phone")
    out["population"]    = after("Population")
    out["next_election"] = after("Next Election Date")

    # Officials from the Government Contacts table
    roster = []
    for tbl in soup.find_all("table"):
        for row in tbl.find_all("tr"):
            cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
            cells = [c for c in cells if c]
            if len(cells) >= 2:
                roster.append(f"{cells[0]}: {cells[1]}")
    out["officials"] = " | ".join(roster)
    return out

def city_names(xlsx):
    from openpyxl import load_workbook
    wb = load_workbook(xlsx, read_only=True)
    ws = wb["Municipalities"]
    names = []
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:  # header
            continue
        if row and row[0]:
            names.append(str(row[0]).strip())
    return names

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True, help="MS_Municipalities.xlsx (reads Municipalities!A)")
    ap.add_argument("--out", default="ms_city_websites.csv")
    ap.add_argument("--write-xlsx", default="", help="also write websites into column G of this copy")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests (be polite)")
    args = ap.parse_args()

    names = city_names(args.xlsx)
    print(f"{len(names)} municipalities to look up", file=sys.stderr)

    results = {}
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["City", "Website", "Status", "MML_Slug", "Phone",
                    "Population", "NextElection", "Officials"])
        for idx, name in enumerate(names, 1):
            html, used = None, ""
            for slug in slugs_for(name):
                html = fetch(slug)
                if html:
                    used = slug; break
            if not html:
                w.writerow([name, "", "NOT FOUND (non-member?)", "", "", "", "", ""])
                results[name] = ""
                print(f"[{idx}/{len(names)}] {name}: not found", file=sys.stderr)
            else:
                d = parse(html)
                status = "OK" if d["website"] else "PAGE FOUND, NO WEB LINK"
                w.writerow([name, d["website"], status, used, d["phone"],
                            d["population"], d["next_election"], d["officials"]])
                results[name] = d["website"]
                print(f"[{idx}/{len(names)}] {name}: {d['website'] or status}", file=sys.stderr)
            time.sleep(args.delay)

    found = sum(1 for v in results.values() if v)
    print(f"\nDone. {found}/{len(names)} official websites found. CSV -> {args.out}", file=sys.stderr)

    if args.write_xlsx:
        from openpyxl import load_workbook
        wb = load_workbook(args.xlsx)
        ws = wb["Municipalities"]
        header = [c.value for c in ws[1]]
        gcol = header.index("City Website") + 1
        for row in ws.iter_rows(min_row=2):
            nm = str(row[0].value).strip() if row[0].value else ""
            url = results.get(nm, "")
            if url:
                ws.cell(row=row[0].row, column=gcol, value=url)
        wb.save(args.write_xlsx)
        print(f"Wrote websites into column G -> {args.write_xlsx}", file=sys.stderr)

if __name__ == "__main__":
    main()
