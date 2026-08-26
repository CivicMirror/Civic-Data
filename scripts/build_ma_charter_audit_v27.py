#!/usr/bin/env python3
import csv, json, uuid, zipfile
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

ROOT=Path(__file__).resolve().parent; DATE="2026-08-21"; OLD="2026-08-21_v26"; NEW="2026-08-21_v27"
NS=uuid.UUID("7d06d8b8-5ee6-5a43-b10a-b8fe3ccf801f")
BATCH=["New Marlborough","New Salem","Newbury","Newburyport","Newton"]

def oid(kind,key): return f"ocd-{kind}/{uuid.uuid5(NS,kind+'|'+key)}"
def slug(s): return s.lower().replace(" ","-")
def office(m,s,r,t,n,structure,years,staggered,legal,election,results,notes=""):
    return {"municipality":m,"office_id":f"{slug(m)}-ma/{s}","role":r,"elected":True,"seats":n,
      "seat_structure":structure,"term_years":years,"staggered_terms":staggered,"partisan":False,
      "legal_source_url":legal,"election_source_url":election,"results_source_url":results,
      "verification_status":"schema-ready" if n else "elected-seat-count-unresolved","notes":notes,"local_title":t}
def hs(m,oid_,seats,names,source,note="",vacancy=0):
    out=[]
    for seat,name in names: out.append({"municipality":m,"office_id":oid_,"seat":seat,"person_name":name,"current_status":"verified-current","source_url":source,"retrieved_on":DATE,"notes":note})
    for i in range(vacancy): out.append({"municipality":m,"office_id":oid_,"seat":f"seat {len(names)+i+1:03d}","person_name":"","current_status":"vacant","source_url":source,"retrieved_on":DATE,"notes":note})
    if seats:
      for i in range(max(0,seats-len(names)-vacancy)): out.append({"municipality":m,"office_id":oid_,"seat":f"seat {len(names)+vacancy+i+1:03d}","person_name":"","current_status":"unresolved","source_url":source,"retrieved_on":DATE,"notes":note or "Current holder not safely reconciled from official sources."})
    return out
off=[]; cur=[]; exclusions=[]
def add(o,names=(),source=None,note="",vacancy=0): off.append(o); cur.extend(hs(o["municipality"],o["office_id"],o["seats"],names,source or o["results_source_url"],note,vacancy))

# New Marlborough — later current official board pages supersede stale FY25 roster material.
m="New Marlborough"; legal="https://www.newmarlboroughma.gov/1336/Town-By-Laws"; election="https://www.newmarlboroughma.gov/DocumentCenter/View/3625"; results="https://www.newmarlboroughma.gov/DocumentCenter/View/3645/OFFICIAL-RESULTS-OF-ANNUAL-TOWN-ELECTION-51126"
nm=[
 ("moderator","Moderator","Moderator",1,"at-large",1,False,["Barry Shapiro"],results),
 ("select-board-member","Select Board Member","Select Board Member",3,"at-large",3,True,["Tara B. White","William West","Maggie Arian"],"https://www.newmarlboroughma.gov/1225/Select-Board"),
 ("assessor","Assessor","Board of Assessors Member",3,"at-large",3,True,["Michael Britton","Wendy W Miller","Freddy Friedman"],"https://www.newmarlboroughma.gov/1244/Board-of-Assessors"),
 ("board-of-health-member","Board of Health Member","Board of Health Member",3,"at-large",3,True,["Larry Davis","Jordan Chretien","John Miller"],"https://www.newmarlboroughma.gov/1243/Board-of-Health"),
 ("cemetery-commissioner","Cemetery Commissioner","Cemetery Commissioner",3,"at-large",3,True,["Tammi Palmer","Robert Palmer","Tara B. White"],"https://www.newmarlboroughma.gov/1239/Cemetery-Commission"),
 ("constable","Constable","Constable",1,"at-large",None,False,["William West"],"https://www.newmarlboroughma.gov/1215/Constable"),
 ("finance-committee-member","Finance Committee Member","Finance Committee Member",7,"at-large",3,True,["I. Douglas Newman","John Pshenishny","Jane Fuccillo","Timothy Fitzgerald","Anne Riney","Sharon Fleck"],"https://www.newmarlboroughma.gov/1234/Finance-Committee"),
 ("library-trustee","Library Trustee","Library Trustee",3,"at-large",3,True,["Thomas Masters","Robin Tost","Sarah North Reynolds"],"https://www.newmarlboroughma.gov/1229/Library-Trustees"),
 ("planning-board-member","Planning Board Member","Planning Board Member",5,"at-large",5,True,["Robert W Hartt","Jonathan James","Jordan Archey","Christian Stovall","Becky Wilkinson"],"https://www.newmarlboroughma.gov/1228/Planning-Board"),
 ("regional-school-committee-member","Regional School Committee Member","Southern Berkshire Regional School Committee Member",2,"district",4,True,["Nanci Worthington","Miguel Mir"],"https://www.newmarlboroughma.gov/1226/School-Committee"),
 ("town-clerk","Town Clerk","Town Clerk",1,"at-large",3,False,["Katherine Chretien"],"https://newmarlboroughma.gov/1208/Town-Clerk"),
 ("tree-warden","Tree Warden","Tree Warden",1,"at-large",1,False,["Matthew Wright"],"https://www.newmarlboroughma.gov/1204/Tree-Warden")]
for s,r,t,n,st,y,sg,names,src in nm:
    note=""
    vac=1 if s=="finance-committee-member" else 0
    if s=="finance-committee-member": note="Bylaws establish seven elected staggered seats; official current page explicitly marks one vacancy through May 2027."
    if s=="regional-school-committee-member": note="Regional agreement §2 allocates two of ten district seats to New Marlborough; elected at biennial state elections."
    if s=="constable": note="Current holder and May 2027 endpoint verified; regular term length unresolved."
    add(office(m,s,r,t,n,st,y,sg,legal,election,results,note),[("",x) for x in names],src,note,vac)
for x,u,n in [("Board of Registrars","https://www.newmarlboroughma.gov/DocumentCenter/View/3627/Annual-Report-FY25","Listed under appointed officers."),("Treasurer","https://www.newmarlboroughma.gov/DocumentCenter/View/3627/Annual-Report-FY25","Listed under appointed officers."),("Tax Collector","https://www.newmarlboroughma.gov/DocumentCenter/View/3627/Annual-Report-FY25","Listed under appointed officers."),("Capital Planning Committee",legal,"Bylaws §8A.1: appointed by Select Board."),("Council on Aging",legal,"Bylaws §12.1: appointed by Select Board."),("Conservation Commission","https://www.newmarlboroughma.gov/DocumentCenter/View/3627/Annual-Report-FY25","Appointed by Select Board.")]: exclusions.append((m,x,"appointed",u,n))

# New Salem — preserve only positively established totals as schema-ready.
m="New Salem"; legal="https://www.newsalemma.org/1495/2023-Annual-Town-Meeting-Warrant"; election="https://www.newsalemma.org/1455/Town-Clerk"; results="https://www.newsalemma.org/1455/Town-Clerk"
ns=[("selectboard-member","Select Board Member","Selectboard Member",3,[],legal),("town-clerk","Town Clerk","Town Clerk",1,[],legal),("assessor","Assessor","Assessor",3,["Pat Renville","Sarah Childs","Leanne Rist"],"https://www.newsalemma.org/1410/Assessors"),("school-committee-member","School Committee Member","New Salem/Wendell School Committee Member",None,[],"https://www.newsalemma.org/1443/Erving-School-Union-28"),("constable","Constable","Constable",1,[],legal),("moderator","Moderator","Moderator",1,[],legal),("board-of-health-member","Board of Health Member","Board of Health Member",None,["Jenny Potee","Patrick Temple"],"https://www.newsalemma.org/1354/Board-of-Health"),("municipal-light-plant-member","Municipal Light Plant Member","Municipal Light Plant Member",None,[],legal)]
for s,r,t,n,names,src in ns: add(office(m,s,r,t,n,"at-large",None,n not in (None,1),legal,election,results,"Elected status verified; unresolved terms or composition retained conservatively."),[("",x) for x in names],src)
for x in ["Conservation Commission","Council on Aging","Ballot Clerk"]: exclusions.append((m,x,"appointed-supported",legal,"Appears in official Selectboard annual appointments material."))

# Newbury — Acts of 2008 c.460 §§13-14 controls the sharply limited elected universe.
m="Newbury"; legal="https://malegislature.gov/Laws/SessionLaws/Acts/2008/Chapter460"; election="https://www.newburyma.gov/DocumentCenter/View/3342/ATM-2026-Electoral-Openings"; results="https://www.newburyma.gov/AgendaCenter/ViewFile/Agenda/_05122026-1041"
nb=[("town-clerk","Town Clerk","Town Clerk",1,None,False,["Gretchen Girard"],"https://www.newburyma.gov/837/Elected-Officials"),("select-board-member","Select Board Member","Select Board Member",None,3,True,["William F. DiMaio","Leslie D. Matthews"],results),("moderator","Moderator","Moderator",1,3,False,["F.N. Budd Kelley III"],results),("assessor","Assessor","Board of Assessors Member",None,3,True,["Sanford Wechsler"],results),("board-of-health-member","Board of Health Member","Board of Health Member",None,3,True,["Steven H. Fram"],results),("constable","Constable","Constable",None,4,True,["Charles A. Colby Jr."],results),("fish-commissioner","Fish Commissioner","Fish Commissioner",None,3,True,["Paul A. Thistlewood"],results),("planning-board-member","Planning Board Member","Planning Board Member",5,5,True,["Peter C. Paicos Jr."],"https://www.newburyma.gov/830/Planning-Board-Member"),("library-trustee","Library Trustee","Library Trustee",5,3,True,["Patricia A. Olson","Richard J. Passeri","Melissa Mashburn","Terry Litterst","Alex Burke"],"https://www.newburyma.gov/AgendaCenter/ViewFile/Minutes/_06242026-1075"),("tree-warden","Tree Warden","Tree Warden",1,3,False,["Keith J. Stromski"],results),("triton-regional-school-committee-member","Regional School Committee Member","Triton Regional School Committee Member",3,3,True,["Paul Goldner","Matthew Landers","Brett M. Alger"],"https://www.newburyma.gov/745/Schools"),("first-settlers-burial-ground-trustee","Cemetery Trustee","Trustee of First Settlers' Burial Ground",None,3,True,["Anthony John Matthews Jr."],results)]
for s,r,t,n,y,sg,names,src in nb: add(office(m,s,r,t,n,"district" if s.startswith("triton") else "at-large",y,sg,legal,election,results,"Acts of 2008 c.460 §14 preserves this office; unresolved total composition remains research-only."),[("",x) for x in names],src)
for x,status,u,n in [("Open Town Meeting voters","not-elected-office","https://www.newburyma.gov/761/What-is-Town-Meeting","Open Town Meeting voters are not elected representatives."),("Treasurer and Tax Collector","appointed",legal,"Acts 2008 c.460 §13."),("Planning Board Associate Member","appointed","https://www.newburyma.gov/830/Planning-Board-Member","One associate excluded from five elected members."),("Finance Committee","appointed","https://www.newburyma.gov/761/What-is-Town-Meeting","Seven members appointed by Select Board."),("Whittier Regional Vocational Technical School Committee representative","appointed","https://www.newburyma.gov/AgendaCenter/ViewFile/Minutes/_02242026-953","Select Board sought a volunteer for this role.")]: exclusions.append((m,x,status,u,n))

# Newburyport
m="Newburyport"; legal="https://www.cityofnewburyport.com/charter-review-committee/pages/charter-related-laws"; election="https://www.cityofnewburyport.com/city-clerk/files/november-4-2025-election-warrant"; results="https://www.cityofnewburyport.com/city-clerk/files/municipal-election-11-4-25-results"
add(office(m,"mayor","Mayor","Mayor",1,"at-large",4,False,legal,election,results),[("","Sean Reardon")],"https://www.cityofnewburyport.com/mayors-office")
c=[("Ward 1","Sharif I. Zeid"),("Ward 2","Stephanie Niketic"),("Ward 3","Brian Callahan"),("Ward 4","Beth Trach"),("Ward 5","Lisa Medina Smith"),("Ward 6","Mary C. DeLai"),("At-Large","Heather Shand"),("At-Large","Ed Cameron"),("At-Large","Afroz K. Khan"),("At-Large","Sarah Hall"),("At-Large","Ben Harman")]
add(office(m,"city-councillor","City Council Member","City Councillor",11,"mixed",2,False,legal,election,results,"Five at-large and six ward councillors. Current roster controls over Heather Shand's stale individual profile."),c,"https://www.cityofnewburyport.com/city-council")
add(office(m,"school-committee-member","School Committee Member","School Committee Member",6,"at-large",4,True,legal,election,results,"Mayor is ex officio and excluded from six elected seats."),[("","Pamela A. Leblanc"),("","Jennifer Moore")],"https://www.cityofnewburyport.com/school-committee")

# Newton — four neighborhood area councils are charter-created elected bodies.
m="Newton"; legal="https://www.newtonma.gov/home/showpublisheddocument/29895/637268617822670000"; election="https://www.newtonma.gov/government/elections/running-for-office"; results="https://www.newtonma.gov/home/showpublisheddocument/137615/638979188998130000"
add(office(m,"mayor","Mayor","Mayor",1,"at-large",4,False,legal,election,results),[("","Marc Laredo")],"https://www.newtonma.gov/government/mayor")
at=[]
for w,names in {1:["John Oliver","Alison Leary"],2:["Susan Albright","Tarik Lucas"],3:["Andrea W. Kelley","Pamela A. Wright"],4:["Cyrus Dahmubed","Joshua Krintzman"],5:["Rena Getz Escudero","Brittany Hume Charm"],6:["Martha Bixby","Lisa Gordon"],7:["R. Lisle Baker","Brian Golden"],8:["David A. Kalis","Stephen Farrell"]}.items(): at += [(f"Ward {w} At-Large",x) for x in names]
add(office(m,"city-councilor-at-large","City Council Member","City Councilor-at-Large",16,"mixed",2,False,legal,election,results,"Two at-large councilors associated with each of eight wards."),at,"https://www.newtonma.gov/government/city-clerk/city-council")
ward=[(f"Ward {i}",n) for i,n in enumerate(["Maria Scibelli Greenberg","David Micley","Julia Malakie","Randy Block","Julie Irish","Sean Roche","Rebecca Walker Grossman","Jacob Silber"],1)]
add(office(m,"ward-councilor","City Council Member","Ward Councilor",8,"ward",2,False,legal,election,results),ward,"https://www.newtonma.gov/government/city-clerk/city-council")
school=[(f"Ward {i}",n) for i,n in enumerate(["Arrianna Proia","Linda Swain","Jason Bhardwaj","Tamika Olszewski","Ben Schlesinger","Jonathan Greene","Alicia Piedalue","Victor Lee"],1)]
add(office(m,"school-committee-member","School Committee Member","School Committee Member",8,"ward",2,False,legal,election,results,"Mayor serves ex officio and is excluded from eight elected seats."),school,"https://www.newton.k12.ma.us/Page/225")
high=[("","Allen Ciccone"),("","Beverly Daniel"),("","Matthew M. Miller"),("","Julia Malakie"),("","Paul Levy"),("","Timon Singh"),("","Cassandra Dorman")]
add(office(m,"newton-highlands-neighborhood-area-council-member","Neighborhood Area Council Member","Newton Highlands Neighborhood Area Councilor",9,"district",2,False,"https://www.newtonma.gov/government/neighborhood-area-councils/newton-highlands",election,election,"Seven current members verified; two seats unresolved, not inferred vacant."),high,"https://www.newtonma.gov/government/neighborhood-area-councils/newton-highlands")
add(office(m,"newtonville-area-council-member","Neighborhood Area Council Member","Newtonville Area Councilor",9,"district",2,False,"https://www.newtonma.gov/government/neighborhood-area-councils/newtonville",election,election,"Current roster unresolved."),[],"https://www.newtonma.gov/government/neighborhood-area-councils/newtonville")
add(office(m,"newton-upper-falls-neighborhood-area-council-member","Neighborhood Area Council Member","Newton Upper Falls Neighborhood Area Councilor",None,"district",None,None,"https://www.newtonma.gov/government/neighborhood-area-councils/newton-upper-falls",election,election,"Charter-created elected body; total seats and current roster unresolved."))
add(office(m,"waban-area-council-member","Neighborhood Area Council Member","Waban Area Councilor",None,"district",None,None,"https://www.newtonma.gov/government/neighborhood-area-councils/waban",election,election,"Charter-created elected body; total seats and current roster unresolved."))
exclusions += [(m,"City Clerk","elected-by-council-not-voters",legal,"Charter §2-7."),(m,"Comptroller of Accounts","elected-by-council-not-voters",legal,"Charter §2-7."),(m,"Boards and commissions generally","appointed","https://www.newtonma.gov/government/boards-commissions","Appointments made by Mayor, City Council, or School Committee.")]

def load(stem): return json.loads((ROOT/f"{stem}_{OLD}.json").read_text())
def writej(stem,data): (ROOT/f"{stem}_{NEW}.json").write_text(json.dumps(data,indent=2)+"\n")
def csvwrite(path,rows,fields):
  with path.open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(({k:r.get(k) for k in fields} for r in rows))

inv=load("ma_charter_elected_office_inventory_rolling"); inv["records"].extend(off); inv.update(generated_on=DATE,municipalities_with_local_findings=200,office_rows=len(inv["records"]),schema_ready_post_rows=sum(x["seats"] is not None for x in inv["records"])); inv["scope_note"]="Rolling Massachusetts municipal charter/elected-office audit through Newton; structure and officeholder coverage tracked separately."; writej("ma_charter_elected_office_inventory_rolling",inv)
current=load("ma_current_officeholders_rolling"); current.extend(cur); writej("ma_current_officeholders_rolling",current)
posts=load("ma_schema_ready_posts_rolling"); orgs=load("ma_schema_ready_organizations_rolling"); persons=load("ma_schema_ready_persons_rolling"); memberships=load("ma_schema_ready_memberships_rolling")
post_by_id={x["id"]:x for x in posts}; org_by_post={x["id"]:x["organization_id"] for x in posts}; person_by_name={x["name"].casefold():x for x in persons}
for o in off:
  if o["seats"] is None: continue
  orgid=oid("organization",o["office_id"]); src={"url":o["legal_source_url"],"retrieved":DATE}
  orgs.append({"id":orgid,"name":o["local_title"],"jurisdiction_id":f"ocd-jurisdiction/country:us/state:ma/place:{slug(o['municipality'])}/government","identifiers":[{"scheme":"civicmirror-office","identifier":o["office_id"]}],"status":"active","sources":[src]})
  p={"id":o["office_id"],"organization_id":orgid,"title":o["local_title"],"seats":o["seats"],"sources":[src]}; posts.append(p); post_by_id[p["id"]]=p; org_by_post[p["id"]]=orgid
for h in cur:
  if h["current_status"]!="verified-current" or h["office_id"] not in post_by_id: continue
  key=h["person_name"].casefold(); p=person_by_name.get(key)
  if not p:
    p={"id":oid("person",h["municipality"]+"|"+h["person_name"]),"name":h["person_name"],"candidacies":[],"verification":{"status":"machine-extracted","reviewed_on":DATE,"pipeline":"MA Municipality Research"},"sources":[{"url":h["source_url"],"retrieved":DATE}]}; persons.append(p); person_by_name[key]=p
  mm={"id":oid("membership",p["id"]+"|"+h["office_id"]+"|"+h["seat"]),"person_id":p["id"],"organization_id":org_by_post[h["office_id"]],"post_id":h["office_id"],"role":post_by_id[h["office_id"]]["title"],"sources":[{"url":h["source_url"],"retrieved":DATE}]}
  if h["seat"]: mm["seat"]=h["seat"]
  memberships.append(mm)
for stem,data in [("ma_schema_ready_posts_rolling",posts),("ma_schema_ready_organizations_rolling",orgs),("ma_schema_ready_persons_rolling",persons),("ma_schema_ready_memberships_rolling",memberships)]: writej(stem,data)
csvwrite(ROOT/f"ma_charter_elected_office_inventory_rolling_{NEW}.csv",inv["records"],list(inv["records"][0])); csvwrite(ROOT/f"ma_current_officeholders_rolling_{NEW}.csv",current,list(current[0]))
oldex=list(csv.DictReader((ROOT/f"ma_charter_appointed_exclusions_rolling_{OLD}.csv").open())); fields=list(oldex[0])
for m,x,s,u,n in exclusions: oldex.append({fields[0]:m,fields[1]:x,fields[2]:s,fields[3]:u,fields[4]:n})
csvwrite(ROOT/f"ma_charter_appointed_exclusions_rolling_{NEW}.csv",oldex,fields)
audit=load("ma_charter_source_audit_rolling")
web={"New Marlborough":"https://www.newmarlboroughma.gov/","New Salem":"https://www.newsalemma.org/","Newbury":"https://www.newburyma.gov/","Newburyport":"https://www.cityofnewburyport.com/","Newton":"https://www.newtonma.gov/"}
for m in BATCH:
  oo=[x for x in off if x["municipality"]==m]; hh=[x for x in cur if x["municipality"]==m]
  audit.append({"municipality":m,"official_website_url":web[m],"office_rows":len(oo),"schema_ready_rows":sum(x["seats"] is not None for x in oo),"unresolved_rows":sum(x["seats"] is None for x in oo),"legal_source_urls":" | ".join(dict.fromkeys(x["legal_source_url"] for x in oo)),"election_source_urls":" | ".join(dict.fromkeys(x["election_source_url"] for x in oo)),"results_source_urls":" | ".join(dict.fromkeys(x["results_source_url"] for x in oo)),"current_officeholder_verified_rows":sum(x["current_status"]=="verified-current" for x in hh),"known_vacancies":sum(x["current_status"]=="vacant" for x in hh),"officeholder_unresolved_markers":sum(x["current_status"]=="unresolved" for x in hh),"person_validation_status":"schema-valid-for-serialized-persons","conflicts_notes":"See inventory notes; unresolved totals, stale rosters, and source conflicts are preserved conservatively.","status":"locally-researched-substantial-with-officeholder-backfill"})
writej("ma_charter_source_audit_rolling",audit); csvwrite(ROOT/f"ma_charter_source_audit_rolling_{NEW}.csv",audit,list(audit[0]))
schemas={k:json.loads((ROOT/f"{k}.schema.json").read_text()) for k in ["organization","post","person","membership"]}; errors={}
for k,data in [("organization",orgs),("post",posts),("person",persons),("membership",memberships)]:
  resolver=RefResolver((ROOT/f"{k}.schema.json").as_uri(),schemas[k],store={(ROOT/f"{n}.schema.json").as_uri():s for n,s in schemas.items()}); errors[k]=sum(1 for row in data for _ in Draft202012Validator(schemas[k],resolver=resolver).iter_errors(row))
orgids={x["id"] for x in orgs}; personids={x["id"] for x in persons}; pids={x["id"] for x in posts}; ref=sum(x["organization_id"] not in orgids for x in posts)+sum(x["organization_id"] not in orgids or x["person_id"] not in personids or x["post_id"] not in pids for x in memberships)
batch=[x for x in cur if x["municipality"] in BATCH]
report={"generated_on":DATE,"schema_model":"Organization / Post / Person / Membership","schema_migration_note":"Existing v26 IDs preserved. New v27 IDs use the explicit namespace recorded since v26.","coverage_ledger_reconciled_from_inventory":True,"municipalities_with_local_findings":200,"municipalities_remaining_without_preserved_local_office_research":151,"total_office_research_rows":len(inv["records"]),"explicit_schema_ready_inventory_rows":sum(x["seats"] is not None for x in inv["records"]),"schema_ready_organization_records":len(orgs),"schema_ready_post_records":len(posts),"total_current_officeholder_research_rows":len(current),"schema_ready_person_records":len(persons),"schema_ready_membership_records":len(memberships),"organization_schema_errors":errors["organization"],"post_schema_errors":errors["post"],"person_schema_errors":errors["person"],"membership_schema_errors":errors["membership"],"referential_integrity_errors":ref,"latest_structure_batch":BATCH,"latest_officeholder_batch":BATCH,"verified_current_officeholder_rows_latest_batch":sum(x["current_status"]=="verified-current" for x in batch),"known_vacancies_latest_batch":sum(x["current_status"]=="vacant" for x in batch),"unresolved_officeholder_markers_latest_batch":sum(x["current_status"]=="unresolved" for x in batch),"remaining_officeholder_backfill_municipalities_without_any_holder_rows":None,"notes":["The all-351 coverage ledger remains absent and was not fabricated.","Unresolved seat counts remain research-only and do not generate Posts.","Newburyport official pages were partially Cloudflare-challenged; exact official URLs and conflicts are preserved."]}; writej("ma_charter_validation_report_rolling",report)
readme=f"""# Massachusetts Municipal Charter / Elected-Office Audit — Rolling Preservation\n\nGenerated: {DATE}\nVersion: v27\n\n- Municipalities with local elected-office findings: **200 / 351**\n- Elected-office research rows: **{len(inv['records'])}**\n- Explicitly schema-ready inventory rows: **{report['explicit_schema_ready_inventory_rows']}**\n- Schema-ready Organizations / Posts: **{len(orgs)} / {len(posts)}**\n- Schema-ready Persons / Memberships: **{len(persons)} / {len(memberships)}**\n- Schema and referential-integrity errors: **{sum(errors.values())+ref}**\n- Municipalities remaining without preserved local office research: **151**\n- Latest batch verified current officeholders: **{report['verified_current_officeholder_rows_latest_batch']}**\n- Latest batch explicit vacancies: **{report['known_vacancies_latest_batch']}**\n- Latest batch unresolved officeholder markers: **{report['unresolved_officeholder_markers_latest_batch']}**\n\nLatest batch: **New Marlborough, New Salem, Newbury, Newburyport, Newton**.\n\n## Important limitations\n\n- New Salem and Newbury retain research-only offices where elected status is verified but total seat count is unresolved.\n- Newbury's 2008 special act controls and converts non-preserved elective offices to appointed or terminated status.\n- Newburyport's official site was partially Cloudflare-challenged; the official URLs and roster conflict are preserved.\n- Newton Upper Falls and Waban Area Council totals remain unresolved; Newtonville's nine seats remain holder-unresolved.\n- The all-351 coverage JSON remains absent and was not fabricated.\n"""; (ROOT/f"MA_CHARTER_AUDIT_ROLLING_README_{NEW}.md").write_text(readme)
zp=ROOT/f"ma_charter_audit_rolling_{NEW}.zip"
with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
  for p in ROOT.glob(f"*{NEW}*"):
    if p!=zp: z.write(p,p.name)
  for p in ROOT.glob("*.schema.json"): z.write(p,p.name)
print(json.dumps(report,indent=2))
