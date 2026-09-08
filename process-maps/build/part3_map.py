from swimlane import Map
m=Map("Part 3 — Design and Permit",
      "Level-1 cross-functional map · as specified · design package to issued for construction, and the permit chain · gate 18 · gate 20 · 8 September 2026",
      [("client","External Authorities"),("exec","Executive"),("eng","Engineering"),("admin","Administration and Permits"),("proj","Projects and Site"),("platform","The Platform")])
s=m.step
# --- design chain ---
s("3.1","eng","Create design package",rec="design_packages",state="draft")
s("3.2","eng","Work the package",rec="design_packages",state="in_progress")
s("3.3","eng","Add deliverables — nine types",rec="design_deliverables",state="draft")
s("3.4","eng","Record professional seal",rec="professional_seals",dev="recorded, then never displayed back; a second seal can be added on top (2-13)")
s("3.5","eng","Issue for review",rec="design_packages",state="issued_for_review")
s("3.6","eng","Deliverable review",rec="design_deliverables",state="in_review → approved",dev="draft can go straight to approved; no reviewer is named (2-06)")
s("3.7","eng","Issue for approval",rec="design_packages",state="issued_for_approval")
s("3.8","eng","Submit design freeze",rec="approval_requests",state="pending",col=8)
s("3.9","exec","Approve design freeze",rec="approval_requests",state="approved",gate=("18","Design Engineer",None,None),dev="RC-A raiser can approve own request")
s("3.10","platform","Package released",kind="auto",rec="design_packages",state="issued_for_construction",dev="refuses release without G18 — the one gate fully enforced in the product")
s("3.11","eng","Bill of materials — seven categories",rec="bill_of_materials_lines",dev="item code is free text, not a catalogue picker; nothing checks it against stock (2-02)")
# --- permit chain ---
s("3.12","admin","Maintain permit type library",rec="permit_types",col=1,dev="negative default duration accepted (1-17); library ships empty (2-28)")
s("3.13","admin","Raise project permit",rec="project_permits",state="draft",col=2)
s("3.14","admin","Set requirements from the library",rec="project_permit_requirements",state="open",col=3)
s("3.15","platform","Requirement observed — library accumulates",kind="auto",rec="permit_requirements.timesObserved",col=4,dev="raw field name shown to the user (1-18)")
s("3.16","admin","Requirements ready",rec="project_permits",state="requirements_set",col=5)
s("3.17","exec","Engage permit consultant",gate=("20","COO","Director",None),col=6,dev="G20 specified; no code raises it anywhere")
s("3.18","admin","Submit permit",rec="project_permits",state="submitted",col=7)
s("3.19","client","Authority decides",kind="external",rec="project_permits",state="approved | rejected",col=8)
s("3.20","admin","Record decision",rec="project_permits",state="approved | rejected",col=9)
s("3.21","admin","Close permit",rec="project_permits",state="closed",col=10,dev="only an approved permit can be closed")
s("3.22","proj","Approved permit is the precondition mobilisation checks",rec="project_permits [approved]",col=11,hb=("HB4","prerequisite permit — fires at mobilisation in Part 5"))
for a,b in [("3.1","3.2"),("3.2","3.3"),("3.3","3.4"),("3.4","3.5"),("3.5","3.6"),("3.6","3.7"),("3.7","3.8"),("3.8","3.9"),("3.9","3.10"),("3.10","3.11"),
            ("3.12","3.13"),("3.13","3.14"),("3.14","3.15"),("3.15","3.16"),("3.16","3.17"),("3.17","3.18"),("3.18","3.19"),("3.19","3.20"),("3.20","3.21"),("3.21","3.22")]: m.edge(a,b)
m.edge("3.9","3.7","rejected: back to issued for approval",kind="return")
m.edge("3.20","3.14","rejected: rework the requirements",kind="return")
m.banner="G18 design freeze is genuinely enforced — the package cannot reach issued for construction without it · G20 permit consultant is specified but no code raises it · a deliverable can go draft to approved with no named reviewer · the seal is recorded and never shown back"
info=m.render("part3.svg"); print(info)
svg=open("part3.svg").read()
import re; w,h=re.search(r'width="(\d+)" height="(\d+)"',svg).groups()
open("part3.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:A3 landscape;margin:5mm}} html,body{{margin:0;background:#fff}} svg{{width:{w}px;height:{h}px;display:block}}</style></head><body>'+svg+'</body></html>')
print("canvas",w,"x",h)
