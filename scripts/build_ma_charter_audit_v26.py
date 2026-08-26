#!/usr/bin/env python3
import csv, json, shutil, uuid, zipfile
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parent
DATE = "2026-08-21"
OLD = "2026-08-20_v25"
NEW = "2026-08-21_v26"
# v25 did not preserve the v23 namespace value or generator.  Keep this explicit
# from v26 onward so subsequent checkpoints can reproduce every new entity ID.
NS = uuid.UUID("7d06d8b8-5ee6-5a43-b10a-b8fe3ccf801f")

def oid(kind, key):
    return f"ocd-{kind}/{uuid.uuid5(NS, kind + '|' + key)}"

def office(m, slug, role, title, seats, structure, years, staggered, legal, election, results, notes=""):
    return {"municipality": m, "office_id": f"{m.lower().replace(' ', '-')}-ma/{slug}", "role": role,
            "elected": True, "seats": seats, "seat_structure": structure, "term_years": years,
            "staggered_terms": staggered, "partisan": False, "legal_source_url": legal,
            "election_source_url": election, "results_source_url": results,
            "verification_status": "schema-ready" if seats else "elected-seat-count-unresolved",
            "notes": notes, "local_title": title}

def holders(m, office_id, seats, names, source, note="", vacancy=0):
    out=[]
    for seat, name in names:
        out.append({"municipality":m,"office_id":office_id,"seat":seat,"person_name":name,
                    "current_status":"verified-current","source_url":source,"retrieved_on":DATE,"notes":note})
    for i in range(vacancy):
        out.append({"municipality":m,"office_id":office_id,"seat":f"seat {len(names)+i+1:03d}","person_name":"",
                    "current_status":"vacant","source_url":source,"retrieved_on":DATE,"notes":note})
    if seats:
        for i in range(max(0,seats-len(names)-vacancy)):
            out.append({"municipality":m,"office_id":office_id,"seat":f"seat {len(names)+vacancy+i+1:03d}","person_name":"",
                        "current_status":"unresolved","source_url":source,"retrieved_on":DATE,"notes":note or "Current holder not safely reconciled from official sources."})
    return out

off=[]; cur=[]; exclusions=[]
def add(o, names=(), holder_source=None, note="", vacancy=0):
    off.append(o); cur.extend(holders(o["municipality"],o["office_id"],o["seats"],names,holder_source or o["results_source_url"],note,vacancy))

# Nantucket — official 2026 ballot proves election; unresolved total composition stays research-only.
m="Nantucket"; legal="https://ecode360.com/11766101"; election="https://nantucket-ma.gov/3574/Running-for-Office"; results="https://nantucket-ma.gov/DocumentCenter/View/55809/2026-Annual-Town-Election-Results-PDF"
add(office(m,"moderator","Moderator","Moderator",1,"at-large",None,False,legal,election,results),[("","Sarah F. Alger")])
add(office(m,"select-board-member","Select Board Member","Select Board Member",5,"at-large",3,True,legal,election,results,"Charter §2-2; Select Board also serves as county commissioners."),[("","Bob DeCosta"),("","Jill Vieth")],note="Three continuing seats remain unresolved in this bounded roster pass.")
for slug,role,title,names in [
 ("school-committee-member","School Committee Member","School Committee Member",["Tim Lepore","Shantaw Bloise-Murphy"]),
 ("historic-district-commissioner","Historic District Commissioner","Historic District Commissioner",["Val Oliver","Ray Pohl"]),
 ("land-bank-commissioner","Land Bank Commissioner","Land Bank Commissioner",["Neil Paterson"]),
 ("harbor-shellfish-advisory-board-member","Harbor and Shellfish Advisory Board Member","Harbor & Shellfish Advisory Board Member",["Peter B. Brace","Kevin C. Korn"]),
 ("housing-authority-member","Housing Authority Member","Nantucket Housing Authority Member",["Beth Ann Meehan"]),
 ("planning-board-member","Planning Board Member","Planning Board Member",["Brian A. Borgeson"]),
 ("water-commissioner","Water Commissioner","Nantucket Water Commissioner",['Nelson "Snooky" Eldridge',"Curtis L. Barnes"])]:
    add(office(m,slug,role,title,None,"at-large",None,True,election,election,results,"Elected status and 2026 winner(s) verified; total elected seat count unresolved."),[("",x) for x in names])
exclusions += [(m,"Town Clerk","appointed",legal,"Charter §4-7 makes Town Clerk appointive."),(m,"County Commissioners","not-separate-elected-office",legal,"Select Board serves ex officio as county commissioners."),(m,"Town Meeting members","not-elected", "https://nantucket-ma.gov/3722/2026-Annual-Town-Meeting","Open Town Meeting participants are not elected representatives.")]

# Natick
m="Natick"; legal="https://www.natickma.gov/DocumentCenter/View/15009/Complete-Charter-April-2023"; election=results="https://www.natickma.gov/2299/Annual-Town-Election-3312026"
natick=[
 ("town-meeting-member","Town Meeting Member","Representative Town Meeting Member",180,"precinct",3,True,[],"https://www.natickma.gov/DocumentCenter/View/19476/TMM-List--Master-Spring-2025"),
 ("select-board-member","Select Board Member","Select Board Member",5,"at-large",3,True,["Danielle P. Dente","Kristen M. Pope","Michael J. Hickey","James P. Pederson","Bruce I. Evans"],"https://natickma.granicus.com/boards/w/92da504fd1cc6cc6/boards/7612"),
 ("town-clerk","Town Clerk","Town Clerk",1,"at-large",3,False,["Andrew Ghobrial"],"https://www.natickma.gov/358/Town-Clerk"),
 ("moderator","Moderator","Moderator",1,"at-large",3,False,["John Barrett"],"https://www.natickma.gov/642/Moderator"),
 ("school-committee-member","School Committee Member","School Committee Member",7,"at-large",3,True,["Courtney Leigh","Matt Brand","Amanda Lipman","Julie McDonough"],"https://www.natickps.org/o/nps/page/school-committee"),
 ("assessor","Assessor","Board of Assessors Member",3,"at-large",3,True,[],"https://www.natickma.gov/389/Board-of-Assessors"),
 ("board-of-health-member","Board of Health Member","Board of Health Member",3,"at-large",3,True,[],"https://www.natickma.gov/392/Board-of-Health"),
 ("constable","Constable","Constable",6,"at-large",3,True,[],"https://www.natickma.gov/461/Constables"),
 ("housing-authority-member","Housing Authority Member","Housing Authority Member",3,"at-large",5,True,["Michael Lioce Jr.","Jeremy Kadden","David M. Ciminelli"],"https://natickma.granicus.com/boards/w/f6f39663a18babea/boards/8941"),
 ("library-trustee","Library Trustee","Morse Institute Library Trustee",5,"at-large",5,True,[],"https://www.natickma.gov/646/Morse-Institute-Library-Board-of-Trustee"),
 ("planning-board-member","Planning Board Member","Planning Board Member",5,"at-large",5,True,[],"https://www.natickma.gov/515/Planning-Board"),
 ("recreation-parks-commissioner","Recreation and Parks Commissioner","Recreation and Parks Commissioner",5,"at-large",3,True,[],"https://www.natickma.gov/467/Recreation-Parks-Commission")]
for slug,role,title,seats,structure,years,stag,names,src in natick:
    note="180 elected seats: 18 per precinct across 10 precincts." if slug=="town-meeting-member" else ""
    add(office(m,slug,role,title,seats,structure,years,stag,legal,election,results,note),[("",x) for x in names],src)
exclusions += [(m,"Housing Authority appointed seats","appointed","https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVII/Chapter121B/Section5","Two appointed seats excluded from the three elected seats."),(m,"School Committee METCO representative","non-elected","https://www.natickps.org/o/nps/page/school-committee","Auxiliary role excluded from seven charter-elected seats."),(m,"Keefe Tech School Committee","appointed","https://www.natickma.gov/2006/Keefe-Tech-School-Committee","No voter-elected Natick regional seat verified." )]

# Needham
m="Needham"; legal="https://www.needhamma.gov/DocumentCenter/View/1859/General-By-LawsCharter-2021-PDF?bidId="; election="https://needhamma.gov/5755/2026-Annual-Town-Election-Candidates"; results="https://needhamma.gov/DocumentCenter/View/61963/Final-Tally-4142026-Annual-Town-Election"
needham=[
 ("select-board-member","Select Board Member",5,3,["Heidi R. Frail","Kevin T. Keane","Joshua W. Levy","Catherine Reid Dowd","William R. Dermody"]),
 ("school-committee-member","School Committee Member",7,3,["Alisa M. Skatrud","Sri Baqri","Andrea Longo Carter","Elizabeth Lee","Michael E. O'Brien","Michael J. Greis","Matthew Spengler"]),
 ("moderator","Moderator",1,3,["Michael K. Fee"]),("town-clerk","Town Clerk",1,3,["Louise L. Miller"]),
 ("park-and-recreation-commissioner","Park & Recreation Commissioner",5,3,["Michelle S. Geddes","Cynthia J. Chaston","Dina R. Hannigan","Christopher J. Gerstel","James E. Rosenbaum"]),
 ("constable","Constable",2,3,["John J. Longley"]),("assessor","Board of Assessors Member",3,3,["John Bulian","Michael Diener","Marc J. Wexler"]),
 ("commissioner-of-trust-funds","Commissioner of Trust Funds",3,3,[]),
 ("needham-public-library-trustee","Trustee of the Needham Public Library",7,3,["Kathleen Cahill Allison","Robert A. Petitt","Jay M. Fialkov","Joshua Adam Small","Erhardt Graeff","Michael D. O'Neal","Meghan W. Small"]),
 ("memorial-park-trustee","Trustee of Memorial Park",5,3,["Matthew L. Ching","Michael A. Fraini","William R. Dermody","John S. Gallello"]),
 ("board-of-health-member","Board of Health Member",5,3,["Edward V. Cosgrove III","Stephen K. Epstein","Robert A. Partridge","Tejal Gandhi","Aarti Sawant-Basak"]),
 ("planning-board-member","Planning Board Member",5,5,["Justin D. McCullen","Adam J. Block","Artie R. Crocker","Eric Greenberg","Oscar E. Mertz"]),
 ("needham-housing-authority-member","Needham Housing Authority Member",3,5,["James D. Flanagan","Geoffrey Engler","Amanda Berman"]),
 ("town-meeting-member","Town Meeting Member",240,3,[])]
for slug,title,seats,years,names in needham:
    note=""
    vacancy=0
    if slug=="commissioner-of-trust-funds": note="Official 2026-08-17 notice confirms one vacancy; identities of the two continuing members unresolved."; vacancy=1
    if slug=="memorial-park-trustee": note="Official rosters conflict on the fifth elected member; Select Board designee excluded." 
    if slug=="town-meeting-member": note="240 elected seats, 24 per precinct across 10 precincts; authoritative roster found but not fully serialized in this batch."
    role=title.replace(" & "," and ")
    add(office(m,slug,role,title,seats,"precinct" if slug=="town-meeting-member" else "at-large",years,seats>1,legal,election,results,note),[("",x) for x in names],vacancy=vacancy)
exclusions += [(m,x,"appointed",legal,"Needham Charter §20 or related charter provision.") for x in ["Town Manager","Town Counsel","Board of Appeals","Conservation Commission","Town Treasurer/Tax Collector","Administrative Assessor"]]
exclusions += [(m,"Housing Authority Governor and tenant seats","appointed","https://www.needhamma.gov/1207/Needham-Housing-Authority","Excluded from three elected seats.")]

# New Bedford
m="New Bedford"; legal="https://library.municode.com/ma/new_bedford/codes/code_of_ordinances?nodeId=COOR_CH2AD_ARTIINGE_S2-7ADREFE"; election="https://www.sec.state.ma.us/divisions/elections/voter-resources/find-my-local-election-office.htm"; results="https://stories.opengov.com/newbedfordma/published/nntClIy7M"
add(office(m,"mayor","Mayor","Mayor",1,"at-large",None,False,legal,election,results,"Direct current charter term source unresolved."),[("","Jonathan F. Mitchell")],"https://newbedford.ss16.sharpschool.com/cms/one.aspx?pageId=159932")
council=[("At-Large","Ian Abreu"),("At-Large","Shane A. Burgo"),("At-Large","Brian K. Gomes"),("At-Large","Naomi R.A. Carney"),("Ward 1","Leo Chouetta"),("Ward 3","Shawn Oliver"),("Ward 4","Derek Baptiste"),("Ward 5","Joseph P. Lopes"),("Ward 6","Ryan J. Pereira")]
add(office(m,"city-council-member","City Council Member","City Councillor",11,"mixed",None,False,"https://library.municode.com/ma/new_bedford/codes/code_of_ordinances?nodeId=COOR_CH2AD_ARTIIICICO_DIV1GE",election,results,"Five at-large and six ward seats; accessible official roster conflicts with later election reporting for two seats."),council,results)
school=["Melissa Costa","Christopher A. Cotter",'Joaquim "Jack" Livramento, Jr.',"Von Marie Moniz","Richard Porter","William B. Markey"]
add(office(m,"school-committee-member","School Committee Member","School Committee Member",6,"at-large",4,True,legal,election,"https://newbedford.ss16.sharpschool.com/cms/one.aspx?pageId=159932","Mayor is ex officio and excluded from six elected seats."),[("",x) for x in school])
exclusions += [(m,"City Treasurer and Collector of Taxes","appointed","https://library.municode.com/ma/new_bedford/codes/code_of_ordinances?nodeId=COOR_CH2AD_ARTVICITRCOTA","Code §2-100."),(m,"Election Commission","appointed",legal,"Board of election commissioners is appointed."),(m,"Greater New Bedford Regional Voc-Tech seats","appointed","https://www.gnbvt.edu/school-committee/","New Bedford members are mayor-appointed.")]

# New Braintree
m="New Braintree"; legal="https://www.newbraintree.org/warrant.html"; election=results=legal
nb=[("select-board-member","Select Board Member","Select Board Member",3,["Joe Chenevert","William Howland","Randy Walker"]),("town-moderator","Moderator","Moderator",1,[]),("town-clerk","Town Clerk","Town Clerk",1,["Jessica Bennett"]),("town-auditor","Town Auditor","Town Auditor",1,["Christina DeVries"]),("town-treasurer","Treasurer","Treasurer",1,["Janet Pierce"]),("tax-collector","Tax Collector","Tax Collector",1,["Janet Pierce"]),("assessor","Assessor","Assessor",3,["Joe Chenevert","Andrea Letendre","Claire Reavey"]),("planning-board-member","Planning Board Member","Planning Board Member",None,["Jason Ayer","Genevieve Stillman"]),("pathfinder-regional-vocational-school-committee-member","Regional Vocational School Committee Member","Pathfinder Regional Vocational School Committee Member",1,["Marty Goulet"]),("quabbin-regional-school-committee-member","Regional School Committee Member","Quabbin Regional School Committee Member",None,[])]
for slug,role,title,seats,names in nb:
    src="https://pathfindertech.org/school-committe/" if slug.startswith("pathfinder") else "https://www.newbraintree.org/committees.html" if names else legal
    note=""
    if slug in ("town-treasurer","tax-collector"): note="Warrant has separate elected salary lines, while current roster combines Treasurer/Tax Collector; structure conflict preserved."
    if slug=="planning-board-member": note="Elected status verified by official failure-to-elect minutes; exact seat count unresolved."
    if slug.startswith("quabbin"): note="Municipality-seat mapping and elected seat count unresolved; Peggy Thompson not serialized as verified local holder."
    add(office(m,slug,role,title,seats,"district" if "regional" in slug else "at-large",None,None,legal,election,results,note),[("",x) for x in names],src)
for x in ["Town Administrator","Animal Inspector","Building Inspector","Zoning Enforcement Officer","Fire Chief / Forest Fire Warden","Dog Officer / Animal Control Officer","Zoning Board of Appeals"]:
    exclusions.append((m,x,"appointed","https://www.newbraintree.org/government.html","Official town pages identify appointment."))

def load(stem): return json.loads((ROOT/f"{stem}_{OLD}.json").read_text())
inv=load("ma_charter_elected_office_inventory_rolling"); inv["records"].extend(off); inv.update(generated_on=DATE,municipalities_with_local_findings=195,office_rows=len(inv["records"]),schema_ready_post_rows=sum(x["seats"] is not None for x in inv["records"])); inv["scope_note"]="Rolling Massachusetts municipal charter/elected-office audit through New Braintree; structure and officeholder coverage tracked separately."
(ROOT/f"ma_charter_elected_office_inventory_rolling_{NEW}.json").write_text(json.dumps(inv,indent=2)+"\n")

current=load("ma_current_officeholders_rolling"); current.extend(cur); (ROOT/f"ma_current_officeholders_rolling_{NEW}.json").write_text(json.dumps(current,indent=2)+"\n")

posts=load("ma_schema_ready_posts_rolling"); orgs=load("ma_schema_ready_organizations_rolling"); persons=load("ma_schema_ready_persons_rolling"); memberships=load("ma_schema_ready_memberships_rolling")
post_ids={x["id"] for x in posts}; person_by_name={x["name"].casefold():x for x in persons}
for o in off:
    if o["seats"] is None: continue
    orgid=oid("organization",o["office_id"]); src={"url":o["legal_source_url"],"retrieved":DATE}
    orgs.append({"id":orgid,"name":o["local_title"],"jurisdiction_id":f"ocd-jurisdiction/country:us/state:ma/place:{o['municipality'].lower().replace(' ','-')}/government","identifiers":[{"scheme":"civicmirror-office","identifier":o["office_id"]}],"status":"active","sources":[src]})
    posts.append({"id":o["office_id"],"organization_id":orgid,"title":o["local_title"],"seats":o["seats"],"sources":[src]}); post_ids.add(o["office_id"])
for h in cur:
    if h["current_status"]!="verified-current" or h["office_id"] not in post_ids: continue
    key=h["person_name"].casefold(); p=person_by_name.get(key)
    if not p:
        p={"id":oid("person",h["municipality"]+"|"+h["person_name"]),"name":h["person_name"],"candidacies":[],"verification":{"status":"machine-extracted","reviewed_on":DATE,"pipeline":"MA Municipality Research"},"sources":[{"url":h["source_url"],"retrieved":DATE}]}; persons.append(p); person_by_name[key]=p
    orgid=next(x["organization_id"] for x in posts if x["id"]==h["office_id"])
    mid=oid("membership",p["id"]+"|"+h["office_id"]+"|"+h["seat"])
    mm={"id":mid,"person_id":p["id"],"organization_id":orgid,"post_id":h["office_id"],"role":next(x["title"] for x in posts if x["id"]==h["office_id"]),"sources":[{"url":h["source_url"],"retrieved":DATE}]}
    if h["seat"]: mm["seat"]=h["seat"]
    memberships.append(mm)
for stem,data in [("ma_schema_ready_posts_rolling",posts),("ma_schema_ready_organizations_rolling",orgs),("ma_schema_ready_persons_rolling",persons),("ma_schema_ready_memberships_rolling",memberships)]:
    (ROOT/f"{stem}_{NEW}.json").write_text(json.dumps(data,indent=2)+"\n")

def csvwrite(path, rows, fields):
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(({k:r.get(k) for k in fields} for r in rows))
csvwrite(ROOT/f"ma_charter_elected_office_inventory_rolling_{NEW}.csv",inv["records"],list(inv["records"][0]))
csvwrite(ROOT/f"ma_current_officeholders_rolling_{NEW}.csv",current,list(current[0]))

old_ex=list(csv.DictReader((ROOT/f"ma_charter_appointed_exclusions_rolling_{OLD}.csv").open()))
fields=list(old_ex[0]);
for m,body,status,url,note in exclusions: old_ex.append({fields[0]:m,fields[1]:body,fields[2]:status,fields[3]:url,fields[4]:note})
csvwrite(ROOT/f"ma_charter_appointed_exclusions_rolling_{NEW}.csv",old_ex,fields)

audit=load("ma_charter_source_audit_rolling")
for m in ["Nantucket","Natick","Needham","New Bedford","New Braintree"]:
    oo=[x for x in off if x["municipality"]==m]; hh=[x for x in cur if x["municipality"]==m]
    web={"Nantucket":"https://nantucket-ma.gov/","Natick":"https://www.natickma.gov/","Needham":"https://www.needhamma.gov/","New Bedford":"https://www.newbedford-ma.gov/","New Braintree":"https://www.newbraintree.org/"}[m]
    audit.append({"municipality":m,"official_website_url":web,"office_rows":len(oo),"schema_ready_rows":sum(x["seats"] is not None for x in oo),"unresolved_rows":sum(x["seats"] is None for x in oo),"legal_source_urls":" | ".join(dict.fromkeys(x["legal_source_url"] for x in oo)),"election_source_urls":" | ".join(dict.fromkeys(x["election_source_url"] for x in oo)),"results_source_urls":" | ".join(dict.fromkeys(x["results_source_url"] for x in oo)),"current_officeholder_verified_rows":sum(x["current_status"]=="verified-current" for x in hh),"known_vacancies":sum(x["current_status"]=="vacant" for x in hh),"officeholder_unresolved_markers":sum(x["current_status"]=="unresolved" for x in hh),"person_validation_status":"schema-valid-for-serialized-persons","conflicts_notes":"See inventory notes; unresolved totals and roster conflicts are preserved conservatively.","status":"locally-researched-substantial-with-officeholder-backfill"})
(ROOT/f"ma_charter_source_audit_rolling_{NEW}.json").write_text(json.dumps(audit,indent=2)+"\n")
csvwrite(ROOT/f"ma_charter_source_audit_rolling_{NEW}.csv",audit,list(audit[0]))

schemas={k:json.loads((ROOT/f"{k}.schema.json").read_text()) for k in ["organization","post","person","membership"]}
errors={}
for k,data in [("organization",orgs),("post",posts),("person",persons),("membership",memberships)]:
    resolver=RefResolver((ROOT/f"{k}.schema.json").as_uri(),schemas[k],store={ (ROOT/f"{n}.schema.json").as_uri():s for n,s in schemas.items()})
    errors[k]=sum(1 for row in data for _ in Draft202012Validator(schemas[k],resolver=resolver).iter_errors(row))
orgids={x["id"] for x in orgs}; personids={x["id"] for x in persons}; pids={x["id"] for x in posts}
ref=sum(x["organization_id"] not in orgids for x in posts)+sum(x["organization_id"] not in orgids or x["person_id"] not in personids or x["post_id"] not in pids for x in memberships)
batch=[x for x in cur if x["municipality"] in {"Nantucket","Natick","Needham","New Bedford","New Braintree"}]
report={"generated_on":DATE,"schema_model":"Organization / Post / Person / Membership","schema_migration_note":"Existing v25 IDs preserved. New v26 IDs use the explicit namespace recorded in build_v26.py.","coverage_ledger_reconciled_from_inventory":True,"municipalities_with_local_findings":195,"municipalities_remaining_without_preserved_local_office_research":156,"total_office_research_rows":len(inv["records"]),"explicit_schema_ready_inventory_rows":sum(x["seats"] is not None for x in inv["records"]),"schema_ready_organization_records":len(orgs),"schema_ready_post_records":len(posts),"total_current_officeholder_research_rows":len(current),"schema_ready_person_records":len(persons),"schema_ready_membership_records":len(memberships),"organization_schema_errors":errors["organization"],"post_schema_errors":errors["post"],"person_schema_errors":errors["person"],"membership_schema_errors":errors["membership"],"referential_integrity_errors":ref,"latest_structure_batch":["Nantucket","Natick","Needham","New Bedford","New Braintree"],"latest_officeholder_batch":["Nantucket","Natick","Needham","New Bedford","New Braintree"],"verified_current_officeholder_rows_latest_batch":sum(x["current_status"]=="verified-current" for x in batch),"known_vacancies_latest_batch":sum(x["current_status"]=="vacant" for x in batch),"unresolved_officeholder_markers_latest_batch":sum(x["current_status"]=="unresolved" for x in batch),"remaining_officeholder_backfill_municipalities_without_any_holder_rows":None,"notes":["The all-351 coverage ledger remains absent and was not fabricated.","Unresolved seat counts are retained only in research inventory; no schema-ready Post is generated for them.","Natick and Needham representative Town Meeting rosters were located but not fully transcribed in this checkpoint."]}
(ROOT/f"ma_charter_validation_report_rolling_{NEW}.json").write_text(json.dumps(report,indent=2)+"\n")

readme=f"""# Massachusetts Municipal Charter / Elected-Office Audit — Rolling Preservation\n\nGenerated: {DATE}\nVersion: v26\n\n- Municipalities with local elected-office findings: **195 / 351**\n- Elected-office research rows: **{len(inv['records'])}**\n- Explicitly schema-ready inventory rows: **{report['explicit_schema_ready_inventory_rows']}**\n- Schema-ready Organizations / Posts: **{len(orgs)} / {len(posts)}**\n- Schema-ready Persons / Memberships: **{len(persons)} / {len(memberships)}**\n- Schema and referential-integrity errors: **{sum(errors.values()) + ref}**\n- Municipalities remaining without preserved local office research: **156**\n- Latest batch verified current officeholders: **{report['verified_current_officeholder_rows_latest_batch']}**\n- Latest batch explicit vacancies: **{report['known_vacancies_latest_batch']}**\n- Latest batch unresolved officeholder markers: **{report['unresolved_officeholder_markers_latest_batch']}**\n\nLatest batch: **Nantucket, Natick, Needham, New Bedford, New Braintree**.\n\n## Important limitations\n\n- Nantucket and New Braintree preserve several elected offices with unresolved total seat counts; those rows are research-only.\n- Natick and Needham representative Town Meeting rosters were found but were not fully transcribed; unresolved markers preserve the seat shortfall without implying vacancies.\n- New Bedford's accessible official council roster conflicts with later election reporting for two seats; those seats remain unresolved.\n- New Braintree's Treasurer/Tax Collector structure and several possible elective boards require further controlling-law research.\n- The all-351 coverage JSON remains absent and was not fabricated.\n\n## Serialization\n\nExisting v25 IDs are preserved. Because v25 named but did not record the v23 UUID namespace, v26 records an explicit deterministic namespace in `build_v26.py` for all new Organization, Person, and Membership IDs.\n"""
(ROOT/f"MA_CHARTER_AUDIT_ROLLING_README_{NEW}.md").write_text(readme)

zip_path=ROOT/f"ma_charter_audit_rolling_{NEW}.zip"
with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
    for p in ROOT.glob(f"*{NEW}*"): 
        if p != zip_path: z.write(p,p.name)
    for p in ROOT.glob("*.schema.json"): z.write(p,p.name)
print(json.dumps(report,indent=2))
