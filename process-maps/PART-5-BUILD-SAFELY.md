# Part 5 of 10 — Build Safely

**Level-1 cross-functional map · as specified · 8 September 2026**
**Companion files:** `Part 5 — Build Safely (A3 landscape).pdf` and `.svg` in the same folder

---

## 1. What this process is for

This is the part the company exists to do, and the part where people can be hurt.

Three chains run at once. **Getting on site** turns a resource request into crews and
equipment at a location. **The daily loop** is one site report per project per day, with a
toolbox meeting, activities against blocks, submission and approval. **The safety chain**
runs continuously alongside: permits to work, safety stops, incidents, near misses,
inspections, corrective actions and non-conformance reports.

**Starts:** an issued-for-construction design package and an approved permit from Part 3.
**Ends:** blocks complete, incidents closed, non-conformance reports closed.

Four of the company's six hard blocks live in this part — HB1 insurance, HB2 safety and
health programme, HB3 block B0, HB4 prerequisite permit — and locked principle L8 says
**safety approvals are never automated**.

**None of the four hard blocks has any code. Neither of the two safety gates checks that
the approver is a Safety Officer.** Anyone signed in can issue a hot-work permit, and the
person who raises a safety stop can lift it themselves.

---

## 2. Lanes in this map

| Lane | Roles | What they do here |
| --- | --- | --- |
| **External Authorities** | Department of Labor and Employment | Approve the Construction Safety and Health Program. Drawn dashed: outside the company |
| **Executive** | Project Manager · Director as gate holders | One gate: closing a non-conformance report |
| **Safety** | Safety Officer | Owns the permit to work, the safety stop, incidents and inspections |
| **Projects** | Project Manager | Approves the day's report; reviews non-conformance |
| **Site Execution** | Person In Charge · crews | Files the report, raises stops and non-conformance |
| **Human Resource and Manpower** | Human Resource Head · Project Manager | Requests, deploys and mobilises people and equipment |
| **The Platform** | — | Computes block completion and days worked; should hold the hard blocks |

---

## 3. Getting on site, then the daily loop

| # | Lane | Action | Record → state | Gate or block | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 5.1 | Manpower | Raise a resource request | `resource_requests` → `open` | — | A request can be declined but never formally accepted — allocation happens by deploying against it |
| 5.2 | Manpower | Create the deployment | `deployments` → `planned` | — | The workforce person is marked deployed and the request allocation advances. Nothing checks they are at this project's site |
| 5.3 | Manpower | Mobilise the deployment | → `mobilised` | **HB1** · **HB4** | **Checks only that the deployment is `planned`.** HB1 insurance certificate and HB4 prerequisite permit belong here and neither exists in code |
| 5.4 | Site | Assign equipment to the project | `equipment_deployments` | — | Assign and return only. No condition on return, no calibration date, no operator |
| 5.5 | Platform | **Automatic:** the project stage should become construction | `projects` | — | **The only stage mutation in the platform is setup → design.** No code sets a project to procurement, construction, commissioning or handover. A project can never leave design |
| 5.6 | Site | Open the site report for the day | `site_reports` → `draft` | — | One per project per day, correctly refused on a duplicate. A date in the future is accepted. `createdOnDevice` is recorded but never surfaced |
| 5.7 | Site | Record the toolbox meeting and who attended | `toolbox_meetings` | — | `photographRef` is in the schema and **no screen uses it** — the toolbox photograph cannot be attached |
| 5.8 | Site | Add the day's activities against blocks | `site_report_activities` | — | Every activity must name a block — correct. Cumulative percent complete is never checked against the previous entry, so progress can go backwards without comment |
| 5.9 | Site | Submit the report | → `submitted` | — | **Refused without a toolbox meeting.** The one enforced safety precondition in this part |
| 5.10 | Projects | Approve the report | → `approved` | — | No role check and no same-person check — the person who submitted can approve |
| 5.11 | Platform | **Automatic:** block completion computed on read | `project_blocks` | — | Correct — never stored. This is L5 working as designed |
| 5.12 | Platform | **Automatic:** days worked derived from toolbox attendance | payroll | — | **Correct, and important.** Presence is never tracked; a person is paid for a day because their name is on that day's toolbox meeting |

### The toolbox meeting is the most consequential record on site

Two rules meet here and both are honoured. **L4 — presence is never tracked:** there is no
clock-in anywhere in the platform. **L3 — capture must have consequence:** the attendance
list on the toolbox meeting is what the payroll module counts to work out how many days a
person worked.

That makes one small form do three jobs at once. It is the safety briefing, it is the
attendance record, and it is the pay record. It is also the only thing standing between a
crew and an unsubmitted report, because a site report cannot be submitted without it.

**Two consequences to be deliberate about before Tuesday.** A worker left off the list is
not paid for that day, and there is no other route to correct it. And the photograph that
would evidence the briefing actually happened has a field in the database and no way to
attach it.

---

## 4. The safety chain

| # | Lane | Action | Record → state | Gate or block | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 5.13 | External | The Department of Labor and Employment approves the Construction Safety and Health Program | — | **HB2** | **No code checks it, and the programme has no record in the platform at all** — there is nowhere to file the approval |
| 5.14 | Safety | Create a permit to work — six types | `permits_to_work` → `draft` | — | The issuer is **supplied by the caller**, not taken from the person acting. The same-day rule the schema promises is not enforced, and `expired` is unreachable — no code ever sets it |
| 5.15 | Safety | Issue the permit | → `issued` | **G28 · Safety Officer · no alternate** | **No Safety Officer check.** `issuePermitToWork` verifies only that the permit is a draft. Anyone signed in can issue a hot-work or confined-space permit. The competency list the schema names **does not exist anywhere** |
| 5.16 | Site | Any person raises a safety stop | `safety_stops` → `active` | — | **Correct.** Any person may raise it and the actor is recorded from the session |
| 5.17 | Safety | Lift the safety stop | → `cleared` | **G29 · Safety Officer · no alternate** | **No Safety Officer check and no same-person check.** The person who raised the stop can lift it. The clearance note is optional |
| 5.18 | Safety | Record an incident — eighteen fields | `incidents` → `open` | — | The statutory deadline is **typed by hand**, never derived from type or severity |
| 5.19 | Safety | Report a near miss | `near_misses` → `open` | — | **Genuinely anonymous.** There is no reporter field on the record at all — not hidden, absent. Correct, and rare |
| 5.20 | Safety | Safety inspection — pre-work, weekly, incident-triggered | `safety_inspections` → `open` | — | Findings are free text |
| 5.21 | Safety | Corrective action — hierarchy of controls | `corrective_actions` → `open` | — | **Must link to an incident or an inspection — enforced.** The five levels of the hierarchy of controls are recorded properly |
| 5.22 | Site | Raise a non-conformance report | `non_conformance_reports` → `open` | — | |
| 5.23 | Projects | Review the report | → `pending_closure_approval` | — | Transitions are validated against a state table — correct |
| 5.24 | Executive | Close the report | → `closed` | **G19 · Project Manager · Director · 3 days** | **The approval reference is a string the caller supplies.** The same pattern as gate 4: the check is that the string is not empty |
| 5.25 | Platform | **Automatic:** no project reaches commissioning with an open report | — | **HB3** | **The mutation the schema names does not exist.** And there is no block B0 — the spine starts at Mobilization, and blocks have no status, so "B0 signed off" is not a state anything can be in |

### The two safety gates are the most serious finding in the series so far

Locked principle L8 says safety approvals are never automated. The platform honours the
letter of that — nothing is automated — while leaving the door open entirely:

- **Gate 28, permit to work.** The specification says *Safety Officer of record on the
  project, same-day validity, no alternate*. The code checks that the permit is in draft.
  Nothing else. Any signed-in person can issue a permit for hot work, working at height,
  confined space, electrical isolation, excavation or chemical handling.
- **Gate 29, safety stop lift.** The specification says *Safety Officer of record, reason
  required, no alternate*. The code checks that the stop is not already cleared. The reason
  is optional and the person who raised the stop can lift it.

The record of *who* did it is captured correctly in both cases — the actor comes from the
session and the audit entry is written. What is missing is the check on *whether they may*.
That is a smaller fix than it sounds: the role is already on the person, and the refusal
pattern already exists in `approveAdjustment`.

**These two belong at the top of Monday's list, above everything commercial.** A wrong
purchase order costs money. A hot-work permit issued by someone who is not a safety officer
is how a person gets burned.

---

## 5. The RACI

| Step | Safety Officer | Person In Charge | Project Manager | Human Resource Head | Director | Warehouse Custodian | Department of Labor and Employment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5.1 Raise resource request | | C | **R** | **A** | | | |
| 5.2 Create deployment | | I | C | **R / A** | | | |
| 5.3 Mobilise (HB1, HB4) | C | I | **A** | **R** | I | | |
| 5.4 Assign equipment | | **R** | **A** | | | C | |
| 5.5 Stage becomes construction | I | I | **A** | I | I | | |
| 5.6 Open the site report | | **R / A** | I | | | | |
| 5.7 Toolbox meeting | **C** | **R / A** | I | I | | | |
| 5.8 Day's activities | | **R / A** | C | | | | |
| 5.9 Submit the report | I | **R / A** | I | | | | |
| 5.10 Approve the report | | I | **R / A** | | | | |
| 5.11 Block completion | I | I | **I** | | I | | |
| 5.12 Days worked | | I | C | **I** | | | |
| 5.13 Safety and Health Program (HB2) | **R** | I | **A** | I | C | | **R** |
| 5.14 Create permit to work | **R / A** | C | I | | | | |
| 5.15 Issue the permit (G28) | **A** | I | I | | | | |
| 5.16 Raise a safety stop | **I** | **R** | **I** | | | | |
| 5.17 Lift the safety stop (G29) | **A** | I | **I** | | I | | |
| 5.18 Record an incident | **R / A** | C | **I** | I | **I** | | I |
| 5.19 Report a near miss | **A** | **R** | I | | | | |
| 5.20 Safety inspection | **R / A** | C | I | | | | |
| 5.21 Corrective action | **A** | **R** | C | | | | |
| 5.22 Raise non-conformance | C | **R** | **A** | | | | |
| 5.23 Review the report | C | I | **R / A** | | I | | |
| 5.24 Close the report (G19) | C | I | **A** | | C | | |
| 5.25 No commissioning with an open report | I | I | **A** | | **I** | | |

**Reading the matrix.** The Safety Officer is Accountable on five steps and shares none of
them with anyone — every one of gate 28, gate 29, the incident, the near miss and the
inspection sits with a single role and no alternate. That is deliberate and right: safety
authority should not be delegable. It is also precisely why the missing role check matters
so much. The matrix says one person decides; the code says anyone does.

The Person In Charge is Responsible on eight steps, more than any other role in the series
so far, and every one of them happens on a phone in Sorsogon or Dumaguete.

---

## 6. Hand-offs

| From → To | At step | What crosses | What stalls it |
| --- | --- | --- | --- |
| Part 3 → Site | → 5.3 | The approved permit and the issued-for-construction package | Nothing checks either. HB4 has no code |
| Manpower → Site | 5.3 → 5.4 | Crews on site | |
| Site → Projects | 5.9 → 5.10 | The day's report | Nobody is told (RC-H). A report can sit submitted indefinitely |
| **Site → Payroll** | **5.7 → 5.12** | **The attendance list** | Nothing. This join works — and it is the reason the toolbox meeting matters |
| Site → Safety | 5.16 → 5.17 | An active safety stop | Nobody is told, and work does not actually stop — nothing in the platform blocks on an active stop |
| Safety → Executive | 5.23 → 5.24 | A report awaiting closure | Nobody is told |
| Site → Part 8 | 5.11 → handover | Block completion | The stage cannot advance, so handover is unreachable |

---

## 7. Where the live build differs from this map

| | Deviation | Step | Reference |
| --- | --- | --- | --- |
| 1 | **Gate 28 has no Safety Officer check** — anyone can issue a permit to work | 5.15 | New |
| 2 | **Gate 29 has no Safety Officer check and no same-person check** — the raiser can lift their own stop | 5.17 | New |
| 3 | **Hard blocks 1, 2, 3 and 4 have no code anywhere.** The hard-block helper functions exist and **nothing calls them** | 5.3, 5.13, 5.25 | Structural |
| 4 | **A project can never leave design** — the only stage mutation is setup → design | 5.5 | Structural |
| 5 | **There is no block B0.** The spine starts at Mobilization and blocks have no status | 5.25 | Register |
| 6 | The competency list the schema names does not exist | 5.15 | New |
| 7 | The same-day rule on permits is not enforced; `expired` is unreachable | 5.14 | New |
| 8 | The permit issuer is supplied by the caller rather than taken from the actor | 5.14 | New |
| 9 | Gate 19's approval reference is a string the caller supplies | 5.24 | RC-A |
| 10 | An active safety stop blocks nothing — work can continue and be reported | 5.16 | New |
| 11 | The statutory reporting deadline on an incident is typed by hand | 5.18 | New |
| 12 | The toolbox photograph has a field and no way to attach a file | 5.7 | 2-09 |
| 13 | A site report can be filed for a date in the future | 5.6 | New |
| 14 | The person who submits a site report can approve it | 5.10 | RC-A |
| 15 | Nobody is notified at any hand-off | all | RC-H |

**What stands out.** Three things in this part are genuinely well built — the anonymous near
miss, the hierarchy of controls on corrective actions, and the toolbox meeting doing the
work of an attendance system without ever tracking presence. All three are about *recording*
things honestly. Everything that is missing is about *refusing* things: not one safety
approval checks who is approving.

---

## 8. The third register — and why item 12 is now urgent

Part 4 found gates 25a and 25b claimed by two modules. Part 5 shows that this is not an
isolated slip. There are **three registers of gate meanings** in this system, and they
disagree:

1. **The specification** — the thirty rows in `convex/foundation/seed.ts`.
2. **The live rows** — what the database actually holds, which the seeder never updates.
3. **The schema comments** — what each module's author believed the gate number meant when
   they wrote that module.

Here is register three against register one, for every gate a module claims:

| Gate | The specification says | The module's comment says | |
| --- | --- | --- | --- |
| 4 | Purchase Order Up To ₱100,000 | "Purchase Order Issue" | **differs** |
| 5 | Purchase Order Above ₱100,000 | "Purchase Order Amendment" | **differs** |
| 8 | Variation Order | "Contract Execution" | **differs** |
| 9 | Signed Customer Agreement | "Contract or Agreement Variation" | **differs** |
| 10 | Contract Risk Review | "Risk Register Review" | same control, different words |
| 18 | Design Package Release For Permitting | "Design Freeze" | same control, different words |
| 19 | Non-Conformance Report Closure | Non-conformance closure | same |
| 20 | Permit Consultant Engagement | "authorises permit submission" | **differs** |
| 23 | Fund Request Release | Fund request approval and release | same |
| 24 | Role Assignment | "formal offer" (Human Resource) | **differs** |
| 25a | Inter-Island Inventory Transfer | progress claim submission (Finance) | **differs** |
| 25b | Within-Island Transfer Above ₱100,000 | claim certification (Finance) | **differs** |
| 26 | Inventory Variance Write-Off | on stock adjustments, not counts | **wrong record** |
| 28 | Permit To Work Issue | Permit to work issue | same |
| 29 | Safety Stop Lift | Safety stop clearance | same |
| 30 | **Incident Investigation Closure** | Service Report Sign-Off (O&M) **and** Payroll certification (Payroll) | **differs twice** |
| 31 | Threshold and Configuration Change | Disbursement authorisation (Payroll) | **differs** |
| 32 | Role Permission Change | Access review | same control, different words |
| 33 | Document Classification | document publication | **differs** |

**Eleven gate numbers mean something different in the module that uses them than in the
specification you wrote.** Gate 30 — which the specification reserves for closing an
incident investigation, the most serious approval in the company — is used by two other
modules for unrelated things, and the incident closure it was meant for has no approval at
all.

**This is why register item 12 cannot wait.** It is not a labelling tidy-up. Until it is
settled, every gate Hercules builds will be built against whichever register that module's
author happened to read, and the same numbers will keep drifting apart. The decision you
need to make is one sentence long: *the thirty rows in `seed.ts` are the register, and every
module comment and live row that disagrees is wrong.* Once that is stated, the fixes are
mechanical.

---

## 9. Two corrections to earlier parts

**Part 3 was slightly wrong about gate 20.** I said its only occurrence in the codebase was
the seed definition. That is not quite right: `convex/schema/permits.ts` mentions Gate 20
twice in comments, describing it as authorising permit *submission* rather than consultant
*engagement*. The substantive finding stands — **no code raises gate 20** — but the gate is
not entirely absent from the source, and the comment that does mention it describes a
different control. It belongs in the table above.

**Part 0 placed hard block 3 in this part, and that is correct — but it cannot fire.** HB3
requires "Block B0 Site Safety Infrastructure" to reach the state *signed off*. The block
spine has nine blocks beginning at Mobilization; there is no B0. And `project_blocks` has no
status column at all — completion is computed from site report activities, so a block cannot
be signed off. HB3 is not merely unimplemented; the data model has no place for it.

---

## 10. What is deliberately not in this part

- **Payroll itself.** Part 7 — this part produces the attendance that feeds it.
- **Commissioning, handover and turnover.** Part 8, with gates 21 and 34.
- **Paying subcontractors and claiming progress.** Part 6.
- **The document register that should hold the safety and health programme.** Part 9, gate 33.
