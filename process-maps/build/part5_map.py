from swimlane import Map
m=Map("Part 5 — Build Safely",
      "Level-1 cross-functional map · as specified · mobilisation, the daily site loop and the safety chain · gates 19, 28, 29, 30 · hard blocks 1, 2, 3 and 4 · 8 September 2026",
      [("ext","External Authorities"),("exec","Executive"),("safety","Safety"),("proj","Projects"),("site","Site Execution"),("hr","Human Resource and Manpower"),("platform","The Platform")])
s=m.step
# --- get on site, then the daily loop ---
s("5.1","hr","Raise a resource request",rec="resource_requests",state="open",col=0)
s("5.2","hr","Create the deployment",rec="deployments",state="planned",col=1,dev="the workforce person is marked deployed; nothing checks they are at this project's site")
s("5.3","hr","Mobilise the deployment",rec="deployments",state="mobilised",col=2,hb=("HB1","insurance certificate — and HB4 prerequisite permit — belong here; neither has any code"))
s("5.4","site","Assign equipment to the project",rec="equipment_deployments",col=3,dev="assign and return only — no condition, no calibration, no operator")
s("5.5","platform","The project stage should become construction",kind="auto",rec="projects",col=4,dev="the only stage mutation in the platform is setup to design — a project can never leave design")
s("5.6","site","Open the site report for the day",rec="site_reports",state="draft",col=5,dev="one per project per day, correctly refused on a duplicate; a future date is accepted")
s("5.7","site","Record the toolbox meeting and who attended",rec="toolbox_meetings",col=6,dev="photographRef is in the schema and no screen uses it")
s("5.8","site","Add the day's activities against blocks",rec="site_report_activities",col=7,dev="every activity must name a block; cumulative percent is never checked against the previous entry")
s("5.9","site","Submit the report",rec="site_reports",state="submitted",col=8,dev="refused without a toolbox meeting — the one enforced safety precondition in this part")
s("5.10","proj","Approve the report",rec="site_reports",state="approved",col=9,dev="no role check and no same-person check — the person who submitted can approve")
s("5.11","platform","Block completion computed on read",kind="auto",rec="project_blocks",col=10,dev="correct — never stored (L5)")
s("5.12","platform","Days worked derived from toolbox attendance",kind="auto",rec="payroll",col=11,dev="the toolbox meeting attendance list is what pays people")
# --- the safety chain ---
s("5.13","ext","Department of Labor and Employment approves the Safety and Health Program",kind="external",col=0,hb=("HB2","construction start — no code checks it, and the programme has no record in the platform"))
s("5.14","safety","Create a permit to work — six types",rec="permits_to_work",state="draft",col=1,dev="the issuer is supplied by the caller, not the actor; the same-day rule the schema promises is not enforced and expired is unreachable")
s("5.15","safety","Issue the permit",rec="permits_to_work",state="issued",gate=("28","Safety Officer",None,None),col=2,dev="no Safety Officer check — anyone can issue a hot-work permit; no competency list exists")
s("5.16","site","Any person raises a safety stop",rec="safety_stops",state="active",col=4,dev="correct — the actor is recorded and any person may raise it")
s("5.17","safety","Lift the safety stop",rec="safety_stops",state="cleared",gate=("29","Safety Officer",None,None),col=5,dev="no Safety Officer check and no same-person check — the person who raised it can lift it")
s("5.18","safety","Record an incident — eighteen fields",rec="incidents",state="open",col=6,dev="the statutory deadline is typed by hand, never derived from type or severity")
s("5.19","safety","Report a near miss",rec="near_misses",state="open",col=7,dev="genuinely anonymous — no reporter field exists on the record. Correct")
s("5.20","safety","Safety inspection — three types",rec="safety_inspections",state="open",col=8)
s("5.21","safety","Corrective action — hierarchy of controls",rec="corrective_actions",state="open",col=9,dev="must link to an incident or an inspection — enforced")
s("5.22","site","Raise a non-conformance report",rec="non_conformance_reports",state="open",col=10)
s("5.23","proj","Review the report",rec="non_conformance_reports",state="pending_closure_approval",col=11)
s("5.24","exec","Close the report",rec="non_conformance_reports",state="closed",gate=("19","Project Manager","Director","3d"),col=12,dev="the approval reference is a string the caller supplies — the same pattern as gate 4")
s("5.25","platform","No project reaches commissioning with an open report",kind="auto",col=13,hb=("HB3","the mutation the schema names does not exist, and there is no block B0 — the spine starts at Mobilization"))
for a,b in [("5.1","5.2"),("5.2","5.3"),("5.3","5.4"),("5.4","5.5"),("5.5","5.6"),("5.6","5.7"),("5.7","5.8"),("5.8","5.9"),("5.9","5.10"),("5.10","5.11"),("5.11","5.12"),
            ("5.13","5.14"),("5.14","5.15"),("5.15","5.16"),("5.16","5.17"),("5.17","5.18"),("5.18","5.19"),("5.19","5.20"),("5.20","5.21"),("5.21","5.22"),("5.22","5.23"),("5.23","5.24"),("5.24","5.25")]: m.edge(a,b)
m.edge("5.21","5.20","verified at the next inspection",kind="return")
m.edge("5.24","5.22","rejected: the report goes back to open",kind="return")
m.banner="Gates 28 and 29 have no Safety Officer check — anyone can issue a permit to work or lift a safety stop · hard blocks 1, 2, 3 and 4 have no code anywhere · a project can never leave design, so mobilisation and construction start are not events the platform has · gate 30, incident investigation closure, is claimed by two other modules and enforced by none"
info=m.render("part5.svg"); print(info)
import re
svg=open("part5.svg").read()
open("part5.min.svg","w").write(re.sub(r'>\n\s*<','><',svg))
w,h=re.search(r'width="(\d+)" height="(\d+)"',svg).groups()
open("part5.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:A3 landscape;margin:5mm}} html,body{{margin:0;background:#fff}} svg{{width:{w}px;height:{h}px;display:block}}</style></head><body>'+svg+'</body></html>')
print("canvas",w,"x",h)
