from swimlane import Map
m=Map("Part 8 — Operate and Maintain",
      "Level-1 cross-functional map · as specified · handover, turnover and the maintenance chain · gates 21, 30 and 34 · 8 September 2026",
      [("ext","External: Client"),("exec","Executive"),("om","Operations and Maintenance"),("proj","Projects"),("fin","Finance"),("platform","The Platform")])
s=m.step
# --- hand over ---
s("8.1","proj","Commissioning and snagging complete",rec="project_blocks 8 and 9",col=0,dev="completion is computed from site activities; the project stage still cannot move — it is stuck in design")
s("8.2","ext","The client accepts the system",kind="external",col=1,dev="there is no acceptance record, no certificate, nothing to sign")
s("8.3","exec","Record the turnover date",rec="projects",state="turnoverDate",gate=("21","Director","COO",None),col=2,dev="G21 has no code anywhere; recordTurnoverDate is ungated and anyone can call it")
s("8.4","platform","Retention release and warranty expiry derived",kind="auto",rec="projects",col=3,dev="both dates are derived from the contract in the same transaction — correct, and one of the cleanest pieces of code in the product")
s("8.5","fin","Raise the retention invoice at the release date",col=4,dev="G12 has no record — see Part 6. The date is derived and then nothing uses it")
# --- maintain ---
s("8.6","om","Create the maintenance schedule",rec="om_schedules",col=0,dev="frequency in calendar days; a next visit date is set once")
s("8.7","om","Create a visit",rec="om_visits",state="draft",col=1,dev="refused after warranty expiry, with a readable message. The schema calls this hard block 5 — a fourth meaning of that number")
s("8.8","om","Work the visit — nine activity types",rec="om_visits",state="in_progress → completed",col=2,dev="three outcomes per activity: satisfactory, requires attention, not applicable")
s("8.9","om","Record readings",rec="om_readings",col=3,dev="reading type and unit are free text — energy, irradiation and performance ratio are not a fixed list")
s("8.10","om","Raise a defect",rec="om_defects",state="open → acknowledged → in_repair → resolved | escalated",col=4,dev="four severities and five states, and no gate on escalation")
s("8.11","om","Submit the visit for sign-off",rec="approval_requests",state="pending",col=5,dev="a real approval request, built from the gate row with the approver role copied onto it — the right pattern")
s("8.12","exec","Approve the sign-off",rec="om_visits",state="signed_off",gate=("34","O&M Lead",None,None),col=6,dev="approved by its own patch: no R6 self-approval refusal and no role check. The field is gate30ApprovalId, the request says gate 34, and the specification calls neither a service report sign-off")
s("8.13","platform","The next visit date advances",kind="auto",rec="om_schedules",col=7,dev="never happens — the schema says it is updated after each visit and no code does it. Nothing ever falls due")
# --- warranty ---
s("8.14","om","Submit a warranty claim",gate=("34","O&M Lead",None,None),col=8,dev="there is no warranty claim record anywhere; warranty_claim exists only as a document category")
s("8.15","platform","The gate engine",kind="auto",rec="foundation/gates.ts",col=9,dev="a complete correct engine: R6 self-approval refusal in the specification's own words, primary and alternate role checks, no-alternate respected. Twelve approval points in six modules take a string instead and never call it")
for a,b in [("8.1","8.2"),("8.2","8.3"),("8.3","8.4"),("8.4","8.5"),
            ("8.6","8.7"),("8.7","8.8"),("8.8","8.9"),("8.9","8.10"),("8.10","8.11"),("8.11","8.12"),("8.12","8.13"),("8.13","8.14"),("8.14","8.15")]: m.edge(a,b)
m.edge("8.10","8.7","a defect brings the next visit forward",kind="return")
m.edge("8.12","8.8","rejected: the visit goes back to completed",kind="return")
m.banner="The platform has a complete and correct approval engine — R6 self-approval refusal, primary and alternate role checks — and twelve approval points across six modules take an approval reference as a plain string instead of calling it · gate 21 turnover has no code · gate 34 is consumed by the visit sign-off and the warranty claim it names has no record · the maintenance schedule never rolls forward"
info=m.render("part8.svg"); print(info)
import re
svg=open("part8.svg").read()
open("part8.min.svg","w").write(re.sub(r'>\n\s*<','><',svg))
w,h=re.search(r'width="(\d+)" height="(\d+)"',svg).groups()
open("part8.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:A3 landscape;margin:5mm}} html,body{{margin:0;background:#fff}} svg{{width:{w}px;height:{h}px;display:block}}</style></head><body>'+svg+'</body></html>')
print("canvas",w,"x",h)
