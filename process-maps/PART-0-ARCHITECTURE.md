# Magnus Workspace Platform — Process Maps and RACI
## Part 0 of 10: Architecture, conventions and the plan

**Prepared for:** Karl Ivan Estadola, Chief Executive Officer, Magnus Renewable Tech Corp
**Date:** 8 September 2026
**Basis:** the platform as **specified** — drawn from the specification embedded in the source
(`convex/foundation/seed.ts`), the schema's own state machines, and the thirty roles the platform
enforces. Where the live build differs from the specification, the map says so and points at the
finding that proves it.

---

## 1. What this series is, and how to read it

This is a set of cross-functional swimlane process maps covering the whole company as the platform
models it, each accompanied by a RACI matrix. Every map answers four questions for every step:

- **Who does it** — the lane the step sits in, and the role that performs it
- **What record changes** — the platform table and the state it moves to
- **Who must approve, and by when** — the gate, its primary and alternate approver, and its window
- **What can stop it** — the hard block that fires if a precondition is missing

**Nothing on these maps is invented.** Every lane is a department the platform defines. Every gate,
approver and window is a row in the specification. Every record state is a value the schema
permits. Where I have had to choose — how to group thirteen departments into readable lanes, which
process a shared step belongs to — the choice is stated and can be changed.

### The one thing to hold in mind

**These maps show the platform as specified, not as it runs today.** On Saturday two testers
demonstrated that the live build lets a person approve their own request, chooses the approval gate
from a dropdown, and never names an approver on screen. Those are not the design. They are
deviations, and I found their cause on Sunday: the live gate and hard-block tables were seeded from
an older definition and never updated, so the code has been running against a register that the
specification has since corrected.

Each deviation is marked on the map where it occurs, with the symbol **⚠** and a reference. That
makes this series three things at once: the onboarding guide, the governance document, and the
acceptance test for the fixes.

---

## 2. Source of truth

| Element | Where it comes from | Count |
| --- | --- | --- |
| Departments → lanes | `roles.department` on the live platform | 13, consolidated to 12 lanes |
| Roles | `roles` table — the thirty the platform enforces | 30 (13 flagged as approvers) |
| Gates, primary and alternate approvers, windows | `GATE_DEFS` in `seed.ts` — the specification | 30 |
| Hard blocks | `HARD_BLOCK_DEFS` in `seed.ts` — the specification | 6 |
| Record states ("blocks") | Every `status`/`stage` union in `convex/schema/*.ts` | 46 state machines |
| Process flow | The commercial chain as walked end to end on 5 September, plus the six project modules | — |
| Deviations | The two sweep reports and the root-cause analyses of 5–6 September | 14 root causes |

**Where the specification and the live build disagree, the specification wins on the map** and the
disagreement is marked. Two disagreements are large enough to state here:

1. **25 of 30 gate labels differ** between the specification and the live rows. In the
   specification, gate 30 is *Incident Investigation Closure*; on the live platform and in the
   payroll code it is *Payroll Run Approval*. Gate 24 is *Role Assignment* versus *Employment Offer*.
   Gates 25a/25b are *inventory transfers* versus *progress claim submission and certification*.
2. **All six hard blocks differ.** The specification's six are insurance certificate, safety and
   health program, block B0 sign-off, prerequisite permit, quarantined material, and signed contract.
   The live six are a different set.

**Consequence for the maps:** the specification has **no gate at all** for payroll approval,
employment offers, or progress-claim certification — yet the live platform gates all three, and the
schema itself hard-codes `gate24_pending` as an offer status. The maps will show these as **"live
gate, not in specification"** so the register decision (plan item 12) can be made with the whole
picture visible.

---

## 3. The lanes

Thirteen departments are too many for a readable map. Twelve lanes, each map showing only the lanes
it uses (four to seven per map):

| # | Lane | Roles in it |
| --- | --- | --- |
| 1 | **Client and External Parties** | Customer, supplier, distribution utility, local government, Professional Regulation Commission — not platform roles, but every cross-functional map needs the party the company is serving |
| 2 | **Executive** | Chief Executive Officer · Chief Operating Officer · Director |
| 3 | **Sales and Pipeline** | Vice President for Sales · Account Manager · Account Officer · Sales Engineer · Sales Officer · Business Development Officer |
| 4 | **Engineering** | Design Manager · Design Engineer · Process Engineer |
| 5 | **Procurement and Inventory** | Procurement Head · Procurement Officer · Warehouse Custodian |
| 6 | **Projects and Site** | Project Manager · Person In Charge · Project Foreman · Solar Installer |
| 7 | **Safety** | Safety Officer |
| 8 | **Finance and Payroll** | Head of Finance · Finance Officer · Payroll Officer |
| 9 | **Human Resources** | Human Resource Head · Human Resource Officer |
| 10 | **Administration and Permits** | Document Controller · Administrative Staff · Operations Coordinator · Permit Liaison |
| 11 | **Operations and Maintenance** | Service Technician |
| 12 | **The Platform** | Automatic steps, hard blocks, record state changes, the audit chain, and the protocol. This lane is where the platform itself acts — it is what makes these maps different from a paper process |

*Director sits in Executive rather than Projects because the specification makes it the primary
approver on eleven gates spanning finance, procurement, contracts and permits. It behaves as an
executive role, whatever department the record says.*

---

## 4. The RACI convention, tied to the platform's own fields

Every step gets exactly one **A**. Never two, never none.

| Letter | Meaning here | Where it comes from |
| --- | --- | --- |
| **R** — Responsible | The role that performs the step: creates or advances the record | The role whose scope permits the mutation, confirmed against who actually does it |
| **A** — Accountable | The single role that approves or is answerable | **The gate's `primaryRoleName`.** Where a step has no gate, the role that owns the record type |
| **C** — Consulted | Must be asked before the step completes | **The gate's `alternateRoleName`**, plus any role the specification names — e.g. Safety Officer on a site report |
| **I** — Informed | Told after the fact | Who the specification intends to be notified. **The live platform emits no notifications** (⚠ RC-H), so this column is design intent until that is built |
| **Window** | Working days the approver has | The gate's `windowWorkingDays` — where set. 11 of 30 gates carry one |

Three rules I apply and will hold to:

1. **One A per step.** If the specification names two, the primary is A and the alternate is C.
2. **R and A may be the same role only where the specification says so** — and on the live
   platform they are the same *person* far more often than that, which is marked ⚠ RC-A.
3. **The Platform lane is never R, A or C.** It is where automatic consequences happen. Hard blocks
   are shown in that lane as stop signs on the step they block.

---

## 5. Notation

| Symbol | Meaning |
| --- | --- |
| Rounded box | A step performed by a person — labelled with the action and the record |
| Diamond | A decision the process branches on |
| **Gate badge** `G6 · Director · alt COO · 3d` | An approval gate: number, primary approver, alternate, window |
| **Stop sign** `HB6` | A hard block: the step cannot proceed while the precondition is unmet |
| Grey box in the Platform lane | An automatic step — a state change, a number assigned, an audit entry |
| Arrow between lanes | A hand-off. Every hand-off is a place the process can stall, so each one is named |
| `[draft → submitted]` | The record state the step moves through, from the schema |
| **⚠ RC-A** | The live build deviates here. The reference is to the root-cause register |
| **● spec gap** | The specification is silent here and the live build has filled the silence |

---

## 6. The gate register — the specification

Thirty gates. Numbers 13 to 17 are permanently reserved. Approvers are roles; windows are working
days.

| Gate | What it approves | Primary | Alternate | Window |
| --- | --- | --- | --- | --- |
| 1 | Write-off up to ₱50,000 | Person In Charge | Project Manager | 3 |
| 2 | Write-off ₱50,001 to ₱100,000 | Project Manager | Director | 3 |
| 3 | Write-off above ₱100,000 | Chief Operating Officer | — | — |
| 4 | Purchase order up to ₱100,000 | Procurement Head | Director | 2 |
| 5 | Purchase order above ₱100,000 | Director | Chief Operating Officer | 2 |
| 6 | Proposal release to client | Director | Chief Operating Officer | — |
| 7 | Markup more than five points below policy | Director | — | — |
| 8 | Variation order | Director | Chief Operating Officer | 3 |
| 9 | Signed customer agreement | Chief Executive Officer | — | — |
| 10 | Contract risk review | Director | Chief Operating Officer | — |
| 11 | Progress claim or service charge | Head of Finance | Chief Operating Officer | 3 |
| 12 | Retention invoice | Head of Finance | Chief Operating Officer | — |
| 18 | Design package release for permitting | Design Engineer | — | — |
| 19 | Non-conformance report closure | Project Manager | Director | 3 |
| 20 | Permit consultant engagement | Chief Operating Officer | Director | — |
| 21 | Turnover date entry | Director | Chief Operating Officer | — |
| 22 | System constant change | Chief Operating Officer | — | — |
| 23 | Fund request release | Head of Finance | Chief Operating Officer | 2 |
| 24 | Role assignment | Director | Chief Operating Officer | — |
| 25a | Inter-island inventory transfer | Director | Chief Operating Officer | — |
| 25b | Within-island transfer above ₱100,000 | Project Manager | Director | — |
| 26 | Inventory variance write-off | Warehouse Custodian | Project Manager | — |
| 27 | Opening stock lock | Warehouse Custodian | — | — |
| 28 | Permit to work issue | Safety Officer | — | — |
| 29 | Safety stop lift | Safety Officer | — | — |
| 30 | Incident investigation closure | Chief Operating Officer | — | — |
| 31 | Threshold and configuration change | Chief Operating Officer | — | — |
| 32 | Role permission change | Chief Executive Officer | Chief Operating Officer | — |
| 33 | Document classification | Document Controller | — | — |
| 34 | Warranty claim submission | Head of Finance | Chief Operating Officer | 3 |

**Who carries the weight:** Director is primary on 11 gates and alternate on 4. Chief Operating
Officer is primary on 6 and alternate on 12. Head of Finance is primary on 4. Safety Officer holds
the two safety gates alone with no alternate — which is correct, and which means a Safety Officer on
leave stops permits to work for that site.

---

## 7. The hard-block register — the specification

Six, and the list is closed. A hard block is not an approval — nobody can waive it. The step simply
cannot happen until the precondition exists.

| Block | Rule | Fires on |
| --- | --- | --- |
| HB1 | **Insurance certificate required** before project mobilisation | Mobilisation |
| HB2 | **Construction safety and health program required** before construction starts | First construction activity |
| HB3 | **Block B0 must be signed off** before the first electrical block | Electrical works |
| HB4 | **Prerequisite permit required** before mobilisation | Mobilisation |
| HB5 | **Quarantined material cannot be issued to site** | Stock issue and transfer |
| HB6 | **No signed contract, no funds** — blocks leaving setup and blocks any purchase order | Leaving setup · Purchase order · Fund request |

---

## 8. The parts — what each one maps, in the order they will be delivered

Each part is one process, end to end, with every lane it touches, every record and its states,
every gate and hard block placed, and its own RACI table. Delivered one at a time, each as a Drive
link, so you can review Part 1 while Part 2 is being drawn.

| Part | Title | Scope | Lanes used | Gates | Hard blocks | Records and states |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | **The Company on One Page** | Level-0 landscape: the value chain from opportunity to maintenance, with the support processes beneath it, and every gate and block placed | All 12 | All 30 | All 6 | — |
| **2** | **Win the Work** — Pipeline to Contract | Account → contact and site → opportunity → site assessment → proposal → internal review → send to client → accept → won → project created → contract → risk terms → project parties | Client · Executive · Sales · Projects · Platform | 6, 7, 9, 10 | HB6 | `opportunities` (7 states) · `site_assessments` · `proposals` (9) · `projects` (9) · `contracts` (5) · `risk_terms` (4) |
| **3** | **Design and Permit** | Design package → deliverables → professional seal → issue for review → approval → issued for construction → bill of materials · Permit type library → project permits → requirements → submission → consultant engagement | Engineering · Executive · Admin & Permits · Client/External · Platform | 18, 20 | HB4 | `design_packages` (8) · `design_deliverables` (6) · `professional_seals` · `project_permits` (7) |
| **4** | **Buy and Store** — Procurement and Inventory | Purchase order from bill of materials → approval by amount → issue → delivery → goods receipt · Supplier bank verification · Locations → items → transfers (by direction and value) → adjustments → physical counts → equipment | Procurement & Inventory · Executive · Projects · Client/External · Platform | 4, 5, 25a, 25b, 26, 27 | HB5 | `purchase_orders` (8) · `po_lines` (4) · `goods_receipts` (4) · `stock_transfers` (4 directions × 4 states) · `stock_adjustments` (3) · `physical_counts` (3) · `equipment_items` (4) |
| **5** | **Build Safely** — Construction, Manpower and Site Safety | Mobilisation (insurance, permit, safety program) → workforce and deployments → the nine construction blocks → daily: toolbox meeting → site report → activities → approval · Permits to work by type · Safety stop raise and lift · Incident → investigation → corrective action → closure · Near miss · Inspections · Non-conformance → closure | Projects · Safety · Executive · Human Resources · Platform | 19, 28, 29, 30 | HB1, HB2, HB3 | `deployments` (4) · `site_reports` (3) · `permits_to_work` (6 types × 4 states) · `safety_stops` (2) · `incidents` (3 states × 5 severities) · `near_misses` · `corrective_actions` (3) · `safety_inspections` (3 types) · `non_conformance_reports` (4 severities × 3 states) |
| **6** | **Get Paid** — Finance | Billing milestones → progress claims (submit, certify) → retention · Fund requests → release → liquidation · Write-offs by amount band · Variation orders · Cash forecast | Finance · Executive · Projects · Client · Platform | 1, 2, 3, 8, 11, 12, 23 | HB6 | `billing_milestones` · `progress_claims` (6) · `fund_requests` (5) · `write_offs` (4) · `variation_orders` (5) |
| **7** | **People and Pay** — Human Resources and Payroll | Requisition → candidate → interview → offer → hire → employee → regularization → leave → performance review · Payroll period → statutory tables → lines from toolbox attendance → three parallel runs → approve → disburse → acknowledge | Human Resources · Finance & Payroll · Executive · Projects · Platform | **● none in specification** — live build gates offers (24) and payroll (30) | — | `hr_requisitions` (4) · `candidates` (7) · `hr_offers` (6) · `employees` (4 types) · `regularization_records` (4) · `leave_requests` (4) · `performance_reviews` (3) · `payroll_periods` (6) · `statutory_rate_tables` (3) · `payroll_lines` (3) |
| **8** | **Operate and Maintain** — Commissioning, O&M and Warranty | Commissioning → turnover date → handover · Maintenance schedules → visits → readings → defects → escalation → sign-off · Warranty claims | O&M · Projects · Executive · Finance · Client · Platform | 21, 34 | — | `projects` (commissioning → handover → completed) · `om_visits` (5) · `om_defects` (5) · `om_schedules` |
| **9** | **Govern** — Documents, Administration and the Protocol | Document register → revision → classification → in force → acknowledgement · Persons, roles, role assignment, console holders · System constants and thresholds · The audit chain · What the protocol may read, write and decide | Admin & Permits · Executive · Platform | 22, 24, 31, 32, 33 | — | `documents` (3) · `document_revisions` (5) · `persons` (3) · `roles` · `console_holders` · `mcp_sessions` (4 scopes) |
| **10** | **The Consolidated RACI** | Every step from Parts 2–9 in one matrix: rows are steps, columns are the thirty roles, cells are R/A/C/I, with the gate and window beside each row | — | — | — | Delivered as a Google Sheet so it can be filtered by role, by department, or by gate |

**Two things this ordering does on purpose.** Part 1 gives you the whole company before any detail.
Parts 2 through 6 follow the money in the order it moves — win, design, buy, build, get paid — which
is also the order sixty-three people will meet them. Parts 7 to 9 are the support processes that
run alongside. Part 10 is the index.

---

## 9. What each part will contain, and in what form

Every part from 1 to 9 is delivered as **two files in the same Drive folder**:

1. **A Google Doc** — the narrative: what the process is for, where it starts and ends, the steps in
   order with their lane, record and state, every gate and block explained, the RACI table, the
   hand-offs, and the deviations with their references.
2. **A PDF of the swimlane diagram** — one page per process, landscape, drawn to be legible printed
   on A3 and pinned to a wall. Lanes across, time left to right, gates and blocks placed on the step
   they govern.

Part 10 is a **Google Sheet**.

Parts are numbered and named identically in the Doc, the PDF and the sheet, so a step can be found
by the same reference in all three.

---

## 10. What the maps will expose — so it is not a surprise

Drawing a process as specified against a platform as built surfaces things. These are the ones I can
already see, and each will be marked where it occurs:

| | What the map will show | Reference |
| --- | --- | --- |
| 1 | **One person raising and approving** — the live build has one same-person check in sixteen controls | ⚠ RC-A |
| 2 | **Gate chosen, not derived** — write-off gates 1–3 are picked from a dropdown, not from the amount | ⚠ RC-B |
| 3 | **Approver never named** — every approval request on the live platform resolves to "unassigned" because the gate rows lack the role fields | ⚠ Register |
| 4 | **Nobody is told** — the I column is design intent; no notification is emitted anywhere | ⚠ RC-H |
| 5 | **Hard block 6 means something else live** — the specification blocks purchase orders without a signed contract; the live build blocks fund requests while an advance is unliquidated | ⚠ RC-N |
| 6 | **Payroll and hiring have no gate in the specification** — the live build gates both; the schema hard-codes `gate24_pending` | ● spec gap |
| 7 | **Two rosters** — the workforce a foreman deploys and the persons who can be assigned, approved or paid are different lists with no bridge | ⚠ RC-J |
| 8 | **The protocol can set a payroll period to disbursed** by passing a string, skipping the three runs and the gate | ⚠ 12c |
| 9 | **Progress claim certification** — the specification's gate 11 covers it; the live build cannot create a claim at all | ⚠ RC-C |

None of these change what the map draws. They change what the map *marks*. When the Monday fixes
land and the register is reconciled, the marks come off and the map is unchanged — which is the
point of drawing it as specified.

---

## 11. Delivery sequence

| Order | Part | What you get |
| --- | --- | --- |
| Now | **0** — this document | The plan, for your review and correction before anything is drawn |
| Next | **1** — The Company on One Page | The landscape. One PDF, one Doc |
| Then | **2 → 9**, one at a time | Each process, Doc and PDF, in the order above |
| Last | **10** — The Consolidated RACI | The Sheet |

**Before I draw Part 1, three things you can correct in this document:**

- The **twelve lanes** and which roles sit in each (§3) — in particular, Director in Executive
- The **part boundaries** (§8) — where one process ends and the next begins
- Whether the **specification register** (§6, §7) is the one you want the company run by. If the
  live register is what you actually intend, say so, and every map is redrawn against it

Nothing else in this series depends on a question I have not asked.
