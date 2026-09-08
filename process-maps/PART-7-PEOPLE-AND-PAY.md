# Part 7 of 10 — People and Pay

**Level-1 cross-functional map · as specified · 8 September 2026**
**Companion files:** `Part 7 — People and Pay (A3 landscape).pdf` and `.svg` in the same folder

---

## 1. What this process is for

Sixty-three people. Three chains: **hire** them, **manage** them, **pay** them.

**Starts:** a headcount requisition, or a payroll cutoff. **Ends:** a disbursed payroll period
with every worker acknowledged.

The specification names no gates for payroll at all — and the build has more working
controls here than anywhere else in the platform. **Payroll is the best-guarded module in
the product.** Rate tables are immutable once approved. Payroll cannot run until all four
are approved. Three parallel runs are required before approval. Workers can be added and
never removed. A days adjustment needs a written reason. Every payroll line records which
four table versions produced it.

**And the protocol can drive a period from `open` to `disbursed` in one call, past all of it.**

---

## 2. Lanes in this map

| Lane | Roles | What they do here |
| --- | --- | --- |
| **External: Candidate and Agencies** | The candidate · Social Security System · PhilHealth · Pag-IBIG · Bureau of Internal Revenue | Accept or decline; set the statutory rates the company must apply |
| **Executive** | Human Resource Head · Director · Chief Operating Officer · Head of Finance | Three approvals: the offer, the period, the disbursement |
| **Human Resource** | Human Resource Head | Recruitment, employee records, reviews, and entering the rate tables |
| **Payroll** | Payroll Officer | Approving tables, the period, the lines |
| **Managers and Staff** | Every employee and their manager | Leave, objectives, engagement, acknowledging the payslip |
| **The Platform** | — | Diarises regularisation, runs the payroll computation |

---

## 3. Hiring

| # | Lane | Action | Record → state | Gate | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 7.1 | Human Resource | Raise a headcount requisition | `hr_requisitions` → `open` | — | Optionally linked to a resource request from Part 5 |
| 7.2 | Human Resource | Add candidates | `candidates` → `applied` | — | Retention expiry is diarised on the candidate — correct |
| 7.3 | Human Resource | Schedule and record interviews | `interview_records` | — | **The record is hidden from the candidate until it is submitted — correct** |
| 7.4 | Human Resource | Create the offer | `hr_offers` → `draft` | — | |
| 7.5 | Executive | Record the approval and issue the offer | → `issued` | **G24 · Human Resource Head · Director** | The reference is **required and trimmed** — stricter than gates 11, 19 and 23. But G24 in the specification is *Role Assignment*, not an offer |
| 7.6 | External | The candidate responds | → `accepted` · `declined` | — | The candidate status moves to hired or rejected in the same transaction — correct |
| 7.7 | Human Resource | Create the employee record | `employees` | — | The employee record is separate from the person record, and **nothing links a hired candidate to it**. Someone re-types the name |
| 7.8 | Platform | **Automatic:** regularisation diarised at six months | `regularization_records` | — | **A diary entry, never an automatic conversion.** Exactly right — the platform reminds, a person decides |

---

## 4. Managing

| # | Lane | Action | Record → state | Deviation today |
| --- | --- | --- | --- | --- |
| 7.9 | Staff | An employee requests leave — seven types | `leave_requests` → `pending` | |
| 7.10 | Managers | The manager reviews it | → `approved` · `declined` | **No same-person check — an employee can approve their own leave.** An over-application clamps the balance to zero rather than refusing, so ten days taken against a four-day balance silently becomes four |
| 7.11 | Staff | The employee writes their own objectives | `performance_objectives` | **Written by the person, not set for them — correct** |
| 7.12 | Managers | The manager acknowledges them | → `acknowledged` | |
| 7.13 | Human Resource | Quarterly review — self assessment, manager review, acknowledgement | `performance_reviews` | **Reasons are required and there is no numeric score — correct.** A three-step review with the employee acknowledging at the end |
| 7.14 | Staff | Engagement survey response | `engagement_responses` | **Fully anonymous.** No person is stored, and **no audit entry is written either** — the code says so in a comment, because an audit row would break the anonymity. This is the most careful piece of privacy design in the platform |

---

## 5. Paying

| # | Lane | Action | Record → state | Gate | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 7.15 | Human Resource | Enter the four statutory rate tables and their brackets | `statutory_rate_tables` → `draft` | — | Three bracket shapes: fixed, percentage, graduated. Correct for Philippine contributions and Bureau of Internal Revenue bands |
| 7.16 | Payroll | Approve each table — **immutable afterwards** | → `approved` | — | Refused without at least one bracket; the previous approved table is superseded in the same transaction. **Both correct.** The code names this G32, which the specification reserves for *Role Permission Change*, and nothing checks that a Finance role approves |
| 7.17 | Payroll | Open the payroll period | `payroll_periods` → `open` | — | **An overlapping open period is correctly refused** |
| 7.18 | Payroll | Add workers — never removed | `payroll_lines` → `computed` | — | **Article 116 honoured: there is no remove mutation at all.** A days adjustment needs a reason of at least ten characters |
| 7.19 | Platform | **Automatic:** run payroll, three times | → `running` → `ready_to_approve` | — | **Refused unless all four tables are approved**, with a message naming all four. The table versions are locked to the period on the first run and stamped on every line. **Nothing compares the three runs** — it is a count, not a reconciliation |
| 7.20 | Executive | Approve the period | → `approved` | **G30 · Chief Operating Officer · no alternate** | **Three runs are required first — enforced.** G30 in the specification is *Incident Investigation Closure* |
| 7.21 | Staff | The worker acknowledges the payslip | `payroll_lines` → `acknowledged` | — | **Refused unless the period is approved — correct.** Signature, biometric or witness |
| 7.22 | Executive | Disburse | → `disbursed` | **G31 · Head of Finance · no alternate** | G31 in the specification is *Threshold and Configuration Change* |
| 7.23 | Platform | **The protocol can set any status directly** | — | — | `toolUpdatePayrollPeriod` writes the status straight through, and stamps `disbursedAt` and `disbursedBy` when it does |

### The protocol walks around every payroll control

`convex/mcp/group3cInternals.ts` exposes `toolUpdatePayrollPeriod`, which takes a status
string and patches it onto the period. One call moves a period from `open` to `disbursed`.

That single call bypasses, in order:

1. the check that all four statutory rate tables are approved
2. the three parallel runs
3. gate 30, the period approval
4. every worker's acknowledgement
5. gate 31, the disbursement authorisation

The audit entry is written and says `arrivedChannel: "model_context_protocol"`, so it is
visible afterwards. But nothing refuses it at the time. **The screen path is careful and the
protocol path is not**, and both write to the same table.

This belongs on Monday's list next to the two safety gates. The fix is the same shape:
the internal mutation should call the same guarded path the screen calls, or refuse any
status beyond `open` and `cancelled`.

### The four fake rate tables are still in the live database

Agent 1 entered deliberately unmistakable statutory rates during the live sweep — one
bracket per table, round wrong numbers, `Z1-TEST` in every free-text field — and warned at
the top of its report that real payroll must not be run until they are replaced.

Those four tables are **approved**, and approved tables are immutable. They cannot be
edited. The only route is to enter four correct tables and approve them, which supersedes
the test ones automatically — the superseding logic at 7.16 works and is the right mechanism.

**This has to happen before any payroll period is run, not before it is approved.** The
first run locks the table versions onto the period and stamps them on every line. A period
run against the test tables carries those numbers even if correct tables are approved
afterwards.

---

## 6. The RACI

| Step | HR Head | Payroll Officer | Manager | Employee | COO | Head of Finance | Candidate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 7.1 Requisition | **R / A** | | **C** | | I | I | |
| 7.2 Add candidates | **R / A** | | C | | | | **I** |
| 7.3 Interviews | **A** | | **R** | | | | **C** |
| 7.4 Create the offer | **R / A** | | C | | I | C | I |
| 7.5 Issue the offer (G24) | **A** | | I | | C | C | **I** |
| 7.6 Candidate responds | **I** | | I | | | | **R / A** |
| 7.7 Employee record | **R / A** | **I** | I | **I** | | | |
| 7.8 Regularisation diarised | **A** | | **R** | **I** | I | | |
| 7.9 Request leave | I | | **A** | **R** | | | |
| 7.10 Review the leave | **C** | | **R / A** | I | | | |
| 7.11 Write objectives | I | | **A** | **R** | | | |
| 7.12 Acknowledge objectives | I | | **R / A** | I | | | |
| 7.13 Quarterly review | **A** | | **R** | **R** | I | | |
| 7.14 Engagement response | **I** | | | **R / A** | I | | |
| 7.15 Enter the rate tables | **R / A** | C | | | | **C** | |
| 7.16 Approve the tables | C | **R** | | | I | **A** | |
| 7.17 Open the period | I | **R / A** | C | I | | C | |
| 7.18 Add workers | C | **R / A** | **C** | I | | | |
| 7.19 Run payroll ×3 | I | **R / A** | I | | | **I** | |
| 7.20 Approve the period (G30) | C | I | I | I | **A** | C | |
| 7.21 Acknowledge the payslip | I | **I** | C | **R / A** | | | |
| 7.22 Disburse (G31) | I | **R** | | **I** | C | **A** | |
| 7.23 Protocol status change | I | **A** | | | I | I | |

**Reading the matrix.** The pay chain is the only place in the entire series where
accountability genuinely moves between roles at each step: the Human Resource Head enters
the tables, the Head of Finance approves them, the Payroll Officer runs, the Chief Operating
Officer approves the period, the Head of Finance disburses. **Four different roles across
five steps.** That is a real segregation of duties, and it is written into the specification
rather than left to convention.

Not one of those five steps checks the role of the person doing it. The design is right and
the enforcement is absent — the same sentence that describes gates 28 and 29 in Part 5.

The Employee appears as Responsible on four steps. Every one of them is self-service —
their leave, their objectives, their survey answer, their payslip — which is what a person
should own about themselves.

---

## 7. Hand-offs

| From → To | At step | What crosses | What stalls it |
| --- | --- | --- | --- |
| **Site → Payroll** | Part 5 → 7.19 | **Toolbox attendance becomes days worked** | Nothing. This is the join that makes L4 work — presence is never tracked and people are still paid correctly |
| Candidate → Human Resource | 7.6 → 7.7 | An accepted offer | Nothing carries across. The employee record is typed again by hand |
| Human Resource → Payroll | 7.15 → 7.16 | Draft rate tables | Nobody is told (RC-H) |
| Payroll → Executive | 7.19 → 7.20 | A period ready to approve | Nobody is told |
| Payroll → Staff | 7.20 → 7.21 | The payslip | There is no payslip document — the worker acknowledges a row on a screen. No print, no export, no file |
| Payroll → Finance | 7.22 → Part 6 | The disbursement | Payroll is the **only outbound payment the platform has**. It does not appear in the cash forecast |
| Human Resource → Part 9 | 7.16 | Approved rate tables | The tables are configuration and are not in the configuration register |

---

## 8. Where the live build differs from this map

| | Deviation | Step | Reference |
| --- | --- | --- | --- |
| 1 | **The protocol can set a payroll period to any status**, bypassing three runs and both gates | 7.23 | Structural |
| 2 | **The four statutory rate tables in the live database are Agent 1's deliberately fake ones**, and they are approved and immutable | 7.15, 7.16 | 1-warning |
| 3 | **Gates 24, 30, 31 and 32 all mean something else in the specification** | 7.5, 7.16, 7.20, 7.22 | Register |
| 4 | An employee can approve their own leave | 7.10 | RC-A |
| 5 | An over-application clamps the leave balance to zero instead of refusing | 7.10 | New |
| 6 | No role check on any of the five pay-chain approvals | 7.16–7.22 | New |
| 7 | The three parallel runs are counted, never compared | 7.19 | New |
| 8 | A hired candidate does not become an employee record — it is re-typed | 7.7 | New |
| 9 | There is no payslip document to give a worker | 7.21 | 2-09 |
| 10 | Payroll disbursement does not appear in the cash forecast | 7.22 | New |
| 11 | Nobody is notified at any hand-off | all | RC-H |

**What stands out.** Every other part of this series has been a story of good intentions in
the specification and missing checks in the code. Payroll is the reverse: **the checks are
there.** Immutability, the four-table precondition, the three runs, Article 116, the ten-character
reason, the acknowledgement precondition, the version stamping — someone built this
carefully. The failure is not in the module; it is that a second door was left open beside it.

---

## 9. What this part means for Tuesday

Three things follow directly from this map, and all three are onboarding decisions rather
than build items:

**The toolbox meeting list is the pay record.** Part 5 established it; this part is where it
lands. A crew member left off Tuesday's list is not paid for Tuesday, and the only correction
is a days adjustment with a written reason. Say this out loud to the Persons In Charge before
they file the first report.

**The four rate tables must be replaced before the first run, not before the first approval.**
The run locks the versions. Replacing the tables after a run does not correct that period.

**Thirty-seven of the sixty-three people on the platform have no way to sign in.** Forty-five
are marked as signing in; eight of those have a route — a linked identity or a pending
invitation — and the other thirty-seven have neither. That is not a finding from the code;
it is what today's data shows. Every one of them will fail at the door on Tuesday morning.
This is the largest single onboarding blocker in front of you and it has nothing to do with
any gate. Three of the thirty-seven were fixed while this part was being written.

---

## 10. What is deliberately not in this part

- **The site attendance that feeds payroll.** Part 5.
- **Paying suppliers.** Part 6 — and it does not exist.
- **Role assignment, which is what gate 24 actually governs.** Part 9.
- **The configuration register the rate tables ought to sit beside.** Part 9, gates 22 and 31.
