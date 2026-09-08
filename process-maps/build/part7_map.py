from swimlane import Map
m=Map("Part 7 — People and Pay",
      "Level-1 cross-functional map · as specified · hiring, managing and paying · gate 24 · the four statutory rate tables · no gates in the specification for payroll · 8 September 2026",
      [("ext","External: Candidate and Agencies"),("exec","Executive"),("hr","Human Resource"),("pay","Payroll"),("site","Managers and Staff"),("platform","The Platform")])
s=m.step
# --- hire ---
s("7.1","hr","Raise a headcount requisition",rec="hr_requisitions",state="open",col=0)
s("7.2","hr","Add candidates",rec="candidates",state="applied",col=1)
s("7.3","hr","Schedule and record interviews",rec="interview_records",col=2,dev="the record is hidden from the candidate until it is submitted — correct")
s("7.4","hr","Create the offer",rec="hr_offers",state="draft",col=3)
s("7.5","exec","Record the approval and issue the offer",rec="hr_offers",state="issued",gate=("24","HR Head","Director",None),col=4,dev="the reference is required and trimmed — better than most; G24 in the specification is Role Assignment, not an offer")
s("7.6","ext","The candidate responds",kind="external",rec="hr_offers",state="accepted | declined",col=5)
s("7.7","hr","Create the employee record",rec="employees",col=6,dev="separate from the person record; nothing links a hired candidate to it automatically")
s("7.8","platform","Regularisation diarised at six months",kind="auto",rec="regularization_records",col=7,dev="a diary entry, never an automatic conversion — correct")
# --- manage ---
s("7.9","site","An employee requests leave",rec="leave_requests",state="pending",col=0)
s("7.10","site","The manager reviews it",rec="leave_requests",state="approved | declined",col=1,dev="no same-person check — an employee can approve their own leave; an over-application clamps the balance to zero instead of refusing")
s("7.11","site","The employee writes their own objectives",rec="performance_objectives",col=2,dev="written by the person, not set for them — correct")
s("7.12","site","The manager acknowledges them",rec="performance_objectives",state="acknowledged",col=3)
s("7.13","hr","Quarterly review — self, manager, acknowledgement",rec="performance_reviews",col=4,dev="reasons are required and there is no numeric score — correct")
s("7.14","site","Engagement survey response",rec="engagement_responses",col=5,dev="fully anonymous — no person is stored and no audit entry is written, deliberately")
# --- pay ---
s("7.15","hr","Enter the four statutory rate tables and brackets",rec="statutory_rate_tables",state="draft",col=5)
s("7.16","pay","Approve each table — immutable afterwards",rec="statutory_rate_tables",state="approved",col=6,dev="the code names this G32, which the specification reserves for Role Permission Change; no check that a Finance role approves")
s("7.17","pay","Open the payroll period",rec="payroll_periods",state="open",col=7,dev="an overlapping open period is correctly refused")
s("7.18","pay","Add workers — never removed",rec="payroll_lines",state="computed",col=8,dev="Article 116 honoured: there is no remove mutation. A days adjustment needs a reason of at least ten characters")
s("7.19","platform","Run payroll three times",kind="auto",rec="payroll_periods",state="running → ready_to_approve",col=9,dev="refused unless all four tables are approved; the table versions are locked to the period on the first run and stamped on every line. Nothing compares the three runs — it is a count, not a reconciliation")
s("7.20","exec","Approve the period",rec="payroll_periods",state="approved",gate=("30","COO",None,None),col=10,dev="G30 in the specification is Incident Investigation Closure; three runs are required first — enforced")
s("7.21","site","The worker acknowledges the payslip",rec="payroll_lines",state="acknowledged",col=11,dev="refused unless the period is approved — correct")
s("7.22","exec","Disburse",rec="payroll_periods",state="disbursed",gate=("31","Head of Finance",None,None),col=12,dev="G31 in the specification is Threshold and Configuration Change")
s("7.23","platform","The protocol can set any status directly",kind="auto",col=13,dev="toolUpdatePayrollPeriod writes the status straight through — open to disbursed in one call, past the three runs, both gates and the approved-tables check")
for a,b in [("7.1","7.2"),("7.2","7.3"),("7.3","7.4"),("7.4","7.5"),("7.5","7.6"),("7.6","7.7"),("7.7","7.8"),
            ("7.9","7.10"),("7.10","7.11"),("7.11","7.12"),("7.12","7.13"),("7.13","7.14"),
            ("7.15","7.16"),("7.16","7.17"),("7.17","7.18"),("7.18","7.19"),("7.19","7.20"),("7.20","7.21"),("7.21","7.22"),("7.22","7.23")]: m.edge(a,b)
m.edge("7.6","7.2","declined: back to the candidate list",kind="return")
m.edge("7.19","7.18","each run recomputes every line",kind="return")
m.banner="Payroll is the best-guarded module in the platform — and the protocol can drive a period from open to disbursed in one call, past the three parallel runs and both gates · gates 24, 30, 31 and 32 all mean something else in the specification · nobody checks that a manager is not approving their own leave"
info=m.render("part7.svg"); print(info)
import re
svg=open("part7.svg").read()
open("part7.min.svg","w").write(re.sub(r'>\n\s*<','><',svg))
w,h=re.search(r'width="(\d+)" height="(\d+)"',svg).groups()
open("part7.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:A3 landscape;margin:5mm}} html,body{{margin:0;background:#fff}} svg{{width:{w}px;height:{h}px;display:block}}</style></head><body>'+svg+'</body></html>')
print("canvas",w,"x",h)
