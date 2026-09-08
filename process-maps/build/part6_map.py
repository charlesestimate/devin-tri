from swimlane import Map
m=Map("Part 6 — Get Paid",
      "Level-1 cross-functional map · as specified · billing the client, drawing cash, writing off · gates 1, 2, 3, 8, 11, 12, 23 · hard block 6 · 8 September 2026",
      [("ext","External: Client"),("exec","Executive"),("bill","Finance: Billing"),("treas","Finance: Treasury"),("proj","Projects and Site"),("platform","The Platform")])
s=m.step
# --- bill the client ---
s("6.1","bill","Create a billing milestone on the contract",rec="billing_milestones",state="pending",col=0)
s("6.2","bill","Raise a progress claim",rec="progress_claims",state="draft",col=1,dev="percent complete is derived from block activities and never typed — correct; the claimed amount is not checked against the contract, the milestone or the percent complete")
s("6.3","bill","Submit the claim to the client",rec="progress_claims",state="submitted",gate=("11","Head of Finance","Director",None),col=2,dev="the code raises G25a, an inventory transfer gate; the reference is an unchecked string")
s("6.4","ext","The client reviews and certifies",kind="external",rec="progress_claims",state="certified | disputed",col=3)
s("6.5","bill","Record the certification",rec="progress_claims",state="certified",gate=("11","Head of Finance","Director",None),col=4,dev="the code raises G25b; certified is correctly a separate field from claimed, and is not checked against it")
s("6.6","bill","Mark the milestone paid",rec="billing_milestones",state="paid",col=5,dev="paid amount is not checked against certified")
s("6.7","bill","Raise the retention invoice at the release date",col=6,dev="G12 retention invoice has no code and no record; retention is stored on the contract and never billed")
# --- draw cash ---
s("6.8","treas","Raise a fund request",rec="fund_requests",state="pending",col=0,hb=("HB6","refused while an advance is released and not liquidated — enforced, with a readable message"))
s("6.9","exec","Approve the request",rec="fund_requests",state="approved",gate=("23","Head of Finance","Director",None),col=1,dev="no role check, no same-person check; the approved amount is not bounded by the requested amount")
s("6.10","treas","Release the funds",rec="fund_requests",state="released",col=2,dev="the person who approved can release")
s("6.11","treas","Liquidate the advance",rec="fund_requests",state="liquidated",col=3,dev="a reference is required — correct; nothing checks what it points at")
# --- write off ---
s("6.12","treas","Raise a write-off — seven categories",rec="write_offs",state="pending_approval",col=4,dev="the gate is derived from severity, not from the amount")
s("6.13","exec","Approve the write-off",rec="write_offs",state="approved",gate=("1 or 2 or 3","set by amount",None,None),col=5,dev="G1 up to ₱50k · G2 ₱50k to ₱100k · G3 above ₱100k in the specification; the code reads severity instead, so a ₱5,000,000 minor write-off raises G1")
# --- variation and forecast ---
s("6.14","proj","Raise a variation order",rec="variation_orders",state="draft",col=7,dev="the mutation exists and no screen calls it")
s("6.15","exec","Approve the variation order",gate=("8","Director","COO",None),col=8,dev="no approve mutation exists; gate9ApprovalId is never written and the value adjustment reaches nothing")
s("6.16","treas","Cash forecast — secured, gated, projected",rec="cash_forecast_lines",col=9,dev="a gated line must carry a gate — correct")
s("6.17","platform","Three-month gap detected on read",kind="auto",col=10,dev="correct — three consecutive months with no secured or gated line")
s("6.18","platform","Pay a supplier",kind="auto",col=11,dev="there is no accounts payable anywhere: no supplier invoice, no subcontractor invoice, no payment record. The forecast covers cash in only")
for a,b in [("6.1","6.2"),("6.2","6.3"),("6.3","6.4"),("6.4","6.5"),("6.5","6.6"),("6.6","6.7"),
            ("6.8","6.9"),("6.9","6.10"),("6.10","6.11"),("6.11","6.12"),("6.12","6.13"),("6.13","6.14"),("6.14","6.15"),("6.15","6.16"),("6.16","6.17"),("6.17","6.18")]: m.edge(a,b)
m.edge("6.4","6.2","disputed: the claim is reworked",kind="return")
m.edge("6.11","6.8","liquidated: a new request can be raised",kind="return")
m.banner="Gate 11 is the specification's gate for a progress claim and has no code — finance raises gates 25a and 25b, which the specification reserves for inventory transfers · gate 12 retention invoice has no record at all · the write-off gate is read from severity, not the amount · there is no accounts payable anywhere in the platform"
info=m.render("part6.svg"); print(info)
import re
svg=open("part6.svg").read()
open("part6.min.svg","w").write(re.sub(r'>\n\s*<','><',svg))
w,h=re.search(r'width="(\d+)" height="(\d+)"',svg).groups()
open("part6.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:A3 landscape;margin:5mm}} html,body{{margin:0;background:#fff}} svg{{width:{w}px;height:{h}px;display:block}}</style></head><body>'+svg+'</body></html>')
print("canvas",w,"x",h)
