# Part 8 of 10 — Operate and Maintain

**Level-1 cross-functional map · as specified · 8 September 2026**
**Companion files:** `Part 8 — Operate and Maintain (A3 landscape).pdf` and `.svg` in the same folder

---

## 1. What this process is for

The system is built. This part hands it to the client, starts the clocks that run from that
moment — retention, warranty — and then looks after it.

Three chains. **Hand over** turns a finished build into a turnover date, and that date derives
the retention release and warranty expiry. **Maintain** runs scheduled visits: activities,
readings, defects, sign-off. **Warranty** is what the company owes the client afterwards.

**Starts:** commissioning and snagging complete in Part 5. **Ends:** a warranty that expires,
and a retention that should have been invoiced.

This is the last operational part, and it is where the most important finding of the whole
series turned up — not in operations at all, but underneath it.

---

## 2. The finding that reframes Parts 3 to 7

**The platform already has a complete and correct approval engine, and almost nothing calls it.**

`convex/foundation/gates.ts` contains everything the specification asks for:

- `submitApprovalRequest` reads the gate row, refuses if the gate is inactive, refuses if it
  has no primary approver assigned, and copies the primary and alternate role onto the request.
- `approveRequest` **refuses self-approval in the specification's own words** — *"The person
  who raised a request cannot approve it (refusal R6)."* — then checks that the deciding
  person actually holds the primary or alternate role, respects `noAlternate`, and records
  the decider's name for the audit trail.
- `rejectRequest` applies both checks and requires a reason.
- `passToAlternate` refuses on a gate with no alternate path.
- `getMyApprovals` filters out your own requests and matches on role.

R6 is implemented. Role authority is implemented. The alternate path is implemented. It is
good code.

**And twelve approval points across six modules take the approval reference as a plain
string and never touch it:**

| Module | Approval points that take a string |
| --- | --- |
| `finance/finance.ts` | 6 — claim submission, certification, milestone submission and certification, fund request, write-off |
| `payroll/payroll.ts` | 3 — rate table, period approval, disbursement |
| `hr/hr.ts` | 1 — the offer |
| `construction/reports.ts` | 1 — non-conformance closure |
| `procurement/orders.ts` | 1 — purchase order approval |

Three modules do create real approval requests — design, pipeline and operations — and then
**approve them with their own patch**, which carries neither the R6 refusal nor the role
check. No screen in the platform calls `approveRequest` at all; the only references to the
gates module from the interface are three read-only queries.

**This changes what Monday's list is.** Every part of this series has reported the same
defect in different clothes: gate 4's invented string, gate 19's unchecked reference, gates
28 and 29 with no Safety Officer check, five pay-chain approvals with no role check. They
are not twelve separate bugs. **They are one decision, made twelve times, to write a
shortcut instead of calling the engine that was already there.**

The instruction to Hercules is therefore much smaller than the finding count suggests:
*route every gate through `foundation/gates.ts`.* The refusal, the role check, the alternate
path and the audit record all come for free the moment a module stops taking a string.

**A refinement to Part 3.** I called gate 18 "the one gate fully enforced in the product".
The precondition is genuinely enforced — `updateDesignPackage` refuses to release a package
as issued for construction without an approved gate 18, and nothing else in the platform
does anything that careful. But `approveDesignFreeze` approves that request with its own
patch and no R6 check. **The consequence of the approval is enforced; the approval itself is
not.** That is a narrower claim than I made, and it is the accurate one.

---

## 3. Lanes in this map

| Lane | Roles | What they do here |
| --- | --- | --- |
| **External: Client** | The client | Accept the system. Drawn dashed: outside the company |
| **Executive** | Director · Chief Operating Officer · Operations and Maintenance Lead | Two gates: the turnover date and the visit sign-off |
| **Operations and Maintenance** | Service Technician · O&M Lead | Schedules, visits, readings, defects |
| **Projects** | Project Manager | Completes the build and hands it over |
| **Finance** | Finance Officer | The retention invoice that should follow the release date |
| **The Platform** | — | Derives the retention and warranty dates; holds the gate engine |

---

## 4. Handing over

| # | Lane | Action | Record → state | Gate | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 8.1 | Projects | Commissioning and snagging complete | `project_blocks` 8 and 9 | — | Completion is computed from site activities — correct. **The project stage still cannot move**; it is stuck in `design` from Part 5 |
| 8.2 | External | The client accepts the system | — | — | **There is no acceptance record.** No certificate, no signature, no date, nothing to attach |
| 8.3 | Executive | Record the turnover date | `projects.turnoverDate` | **G21 · Director · Chief Operating Officer** | **G21 has no code anywhere.** `recordTurnoverDate` is ungated and any signed-in person can call it |
| 8.4 | Platform | **Automatic:** retention release and warranty expiry derived | `projects` | — | **Both dates are derived from the contract in a single transaction — correct**, and one of the cleanest pieces of code in the product |
| 8.5 | Finance | Raise the retention invoice at the release date | — | **G12** | No record exists — Part 6. The release date is derived correctly and then nothing reads it |

### The turnover date is the most consequential ungated field in the platform

One value sets two clocks. `retentionReleaseDate` decides when the last five to ten per cent
of the contract becomes billable. `warrantyExpiryDate` decides when the company's obligation
ends — and, in this build, when a maintenance visit stops being recordable at all.

The derivation is right. The three dates are written together in one transaction, exactly as
the specification asks. What is missing is any check on who may enter the date it derives
from, or that it is plausible. A turnover date typed a year early shortens the warranty by a
year and brings the retention invoice forward into a period where the work is not finished.

---

## 5. Maintaining

| # | Lane | Action | Record → state | Gate | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 8.6 | Operations | Create the maintenance schedule | `om_schedules` | — | Frequency in calendar days; a next visit date is set once |
| 8.7 | Operations | Create a visit | `om_visits` → `draft` | — | **Refused after warranty expiry**, with a readable message naming the date. The schema calls this *hard block 5* — **a fourth meaning of that number** |
| 8.8 | Operations | Work the visit — nine activity types | → `in_progress` → `completed` | — | Three outcomes per activity: satisfactory, requires attention, not applicable |
| 8.9 | Operations | Record readings | `om_readings` | — | Reading type and unit are free text. Energy, irradiation and performance ratio are not a fixed list, so nothing can be trended reliably |
| 8.10 | Operations | Raise a defect | `om_defects` → `open` → `acknowledged` → `in_repair` → `resolved` · `escalated` | — | Four severities and five states — and **no gate on escalation**, including for a critical defect |
| 8.11 | Operations | Submit the visit for sign-off | `approval_requests` → `pending` | — | **A real approval request**, built from the gate row with the approver role copied onto it. This is the right pattern and one of only three places it is used |
| 8.12 | Executive | Approve the sign-off | `om_visits` → `signed_off` | **G34 · O&M Lead · no alternate** | Approved by its own patch: **no R6 refusal and no role check**. The field is `gate30ApprovalId`, the request is raised against gate 34, and the specification calls neither of them a service report sign-off |
| 8.13 | Platform | **Automatic:** the next visit date advances | `om_schedules` | — | **Never happens.** The schema says it is updated after each visit and no code does it. Nothing ever falls due |

### Three problems that compound

**The schedule never rolls forward.** `nextVisitDate` is set when the schedule is created and
is only ever changed by hand or over the protocol. A quarterly maintenance schedule shows one
date, that date passes, and nothing marks it overdue or moves it on. The maintenance module
cannot tell anybody that a visit is due.

**Warranty expiry ends the record, not the obligation.** Blocking a new visit after warranty
expiry is defensible as written. But a solar company does not stop maintaining a site when
the warranty ends — it moves to a paid maintenance contract. Today that is impossible: the
customer keeps the system, the company keeps servicing it, and there is nowhere to record
the visit.

**Readings are free text.** With no fixed reading types and no units enforced, the one thing
this module exists to produce — a performance history that shows a system degrading — cannot
be assembled.

---

## 6. Warranty

| # | Lane | Action | Gate | Deviation today |
| --- | --- | --- | --- | --- |
| 8.14 | Operations | Submit a warranty claim | **G34 · Warranty Claim Submission** | **There is no warranty claim record anywhere.** `warranty_claim` exists only as a document category in the file module. The gate reserved for it is being consumed by the visit sign-off at 8.12 |
| 8.15 | Platform | The gate engine | — | See section 2 |

---

## 7. The RACI

| Step | Service Technician | O&M Lead | Project Manager | Director | COO | Finance Officer | Client |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8.1 Commissioning complete | I | **I** | **R / A** | I | I | I | **I** |
| 8.2 Client accepts | I | I | **R** | **A** | C | I | **R** |
| 8.3 Turnover date (G21) | I | **I** | **R** | **A** | C | **I** | I |
| 8.4 Dates derived | I | **I** | I | I | I | **I** | I |
| 8.5 Retention invoice (G12) | | I | C | C | I | **R / A** | **I** |
| 8.6 Maintenance schedule | C | **R / A** | I | I | | | I |
| 8.7 Create a visit | **R** | **A** | I | | | | I |
| 8.8 Work the visit | **R** | **A** | I | | | | **C** |
| 8.9 Record readings | **R** | **A** | I | | | | I |
| 8.10 Raise a defect | **R** | **A** | **C** | I | I | | **I** |
| 8.11 Submit for sign-off | **R** | **I** | I | | | | |
| 8.12 Approve the sign-off (G34) | I | **A** | I | I | | | **I** |
| 8.13 Next visit date | I | **I** | | | | | |
| 8.14 Warranty claim (G34) | C | **R** | C | **A** | C | I | **I** |
| 8.15 The gate engine | | | | | | | |

**Reading the matrix.** The O&M Lead is Accountable on eight of the fourteen steps and, on
the sign-off, is the sole approver with no alternate — deliberately, because a service report
is a technical judgement. The Client appears on six steps, more than in any other part except
Part 6: this is the phase where the company is visibly working for someone who is watching.

And the client has no record of their own anywhere in it. No acceptance certificate, no
countersigned service report, no warranty claim. Every interaction with them in this part
happens off the platform.

---

## 8. Hand-offs

| From → To | At step | What crosses | What stalls it |
| --- | --- | --- | --- |
| Site → Projects | Part 5 → 8.1 | Block completion | Nothing — it is computed |
| Projects → Executive | 8.2 → 8.3 | A handed-over system | No acceptance record to carry |
| **Platform → Finance** | **8.4 → 8.5** | **The retention release date** | **Nothing reads it.** The date is derived correctly and no record can bill against it |
| Projects → Operations | 8.3 → 8.6 | A site to maintain | The warranty expiry now gates every visit |
| Operations → Executive | 8.11 → 8.12 | A visit awaiting sign-off | Nobody is told (RC-H) |
| Operations → Client | 8.12 → — | The signed-off service report | There is no document to send |
| Operations → Procurement | 8.10 → Part 4 | A defect needing parts | No link at all — a defect cannot become a purchase order or a stock issue |

---

## 9. Where the live build differs from this map

| | Deviation | Step | Reference |
| --- | --- | --- | --- |
| 1 | **Twelve approval points bypass the working gate engine** | 8.15 | Structural |
| 2 | **Gate 21, the turnover date, has no code** — the field that sets retention and warranty is ungated | 8.3 | Register |
| 3 | **Gate 34 is consumed by the visit sign-off**, and the warranty claim it names has no record | 8.12, 8.14 | Register |
| 4 | The visit sign-off is approved by its own patch — no R6, no role check | 8.12 | RC-A |
| 5 | **The next visit date never advances** — nothing ever falls due | 8.13 | New |
| 6 | There is no client acceptance record | 8.2 | New |
| 7 | Warranty expiry blocks recording a visit, with no paid-maintenance path afterwards | 8.7 | New |
| 8 | Reading types and units are free text | 8.9 | New |
| 9 | A critical defect can be escalated with no approval | 8.10 | New |
| 10 | A defect cannot become a purchase order or a stock issue | 8.10 | New |
| 11 | The derived retention release date is read by nothing | 8.4, 8.5 | Register |
| 12 | Nobody is notified at any hand-off | all | RC-H |

**What stands out.** The date derivation at 8.4 is exemplary and feeds nothing. The approval
request at 8.11 is built exactly right and is then decided by a patch that skips every check
the engine would have applied. This part is a small module sitting on top of a large,
correct foundation that the rest of the platform declined to use.

---

## 10. What is deliberately not in this part

- **The retention invoice itself.** Part 6, gate 12.
- **The documents that should hold the acceptance certificate and the service report.** Part 9, gate 33.
- **Role assignment and the configuration behind the gates.** Part 9, gates 22, 24, 31 and 32.
- **The consolidated matrix.** Part 10.
