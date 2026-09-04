# Group 3 protocol verification — 4 September 2026

Verified against the published deployment `elegant-cormorant-29`, over the Model
Context Protocol, decide-scope session `n5729tbs0qcc62gsgvv1hmzfc18dr8md`. No
browser was used. Every statement is the result of a call.

**Headline: the breadth is real, the control layer is not.** 400 tools exist and
dispatch. But the gate table, the hard blocks and the approval routing — the
machinery that makes this a governed platform rather than a database with a web
front end — do not work. A ₱150,000 write-off was routed to the lowest approval
authority by typing one word. A ₱500,000 purchase order was raised against a
project with no signed contract. A hot-work permit was issued by someone who is
not a Safety Officer. None of the three was refused, and none was logged.

---

## 1. What works

`tools/list` returns **400 tools**, up from 95 — 305 added. I sampled 25 read
tools at random: every one dispatched. This is not a stub layer.

- **Operations and Maintenance now exists.** `list_om_schedules`,
  `list_om_visits`, `list_om_readings` and `list_om_defects` all respond, and
  `om_defects` already carries rows. The milestone-6 gap — seven of nine tables
  missing — is closed.
- **Eighteen roles are seeded**, and they match the names the gate table depends
  on: Chief Executive Officer, Chief Operating Officer, Director, Head of
  Finance, Finance Officer, Procurement Head, Procurement Officer, Project
  Manager, Design Engineer, Person In Charge, Safety Officer, Document
  Controller, Warehouse Custodian, Permit Liaison, Human Resource Head, Payroll
  Officer, Sales Officer, Service Technician.
- **Role assignment tools exist** — `list_roles`, `create_person_role`,
  `update_person_role`. Item 10 of the Group 2 fix list is addressed.
- **The gate numbering skeleton is correct**: thirty rows, numbers 1–12, 18–24,
  25a, 25b, 26–34, with 13–17 absent and no bare 25 row. Exactly as section 6
  specifies.
- **The hard block table has six rows and no `active` column**, which is what
  section 5 requires — a boolean that can be set to false is a switch, and the
  spec forbids one.

---

## 2. Defects

### G1 — The gate is chosen by the caller, not derived from the amount. *(most serious)*

`create_write_off` requires `severity` as an input, validated against
`minor` / `moderate` / `major` — which map exactly onto gate rows 1, 2 and 3.

I created a write-off of **₱150,000** and declared it `severity: "minor"`. It was
accepted and stored:

```
amount:   150000
severity: "minor"
gateId:   "1"
status:   "pending_approval"
```

Section 6 specifies:

| Gate | Trigger | Primary | Alternate |
|---|---|---|---|
| 1 | up to ₱50,000 | Head of Finance | Chief Operating Officer |
| 2 | ₱50,001 to ₱100,000 | Chief Operating Officer | Chief Executive Officer |
| 3 | **above ₱100,000** | **Chief Executive Officer** | **none** |

A ₱150,000 write-off is a gate 3 decision that only the Chief Executive Officer
can make, with no alternate. It landed on gate 1. Anyone with write access can
route a write-off of any size to the Head of Finance by typing one word.

The rule is that the gate is derived from the amount and never chosen. Here the
amount is stored and then ignored. **Delete the `severity` input and compute the
gate from `amount` inside the mutation.** The same pattern needs checking
everywhere a gate has a value band: gates 4 and 5 on purchase orders, gate 7 on
markup, gate 25b on transfers.

### G2 — No write raises an approval request.

The ₱150,000 write-off stored `status: "pending_approval"` and `gateId: "1"` and
then created nothing. `list_approval_requests` returns three rows, all
pre-existing, all with:

```
currentApprover: "unassigned"
objectType:      null
objectId:        null
amount:          null
```

They are not attached to any object and are addressed to nobody. So there is no
approval queue: a record can sit at `pending_approval` forever with no person
who has been asked and no screen it appears on.

### G3 — Purchase orders carry no gate at all.

A purchase order for **₱500,000** was created. The stored record has no `gateId`
field and raised no approval request. Section 6 gate 5: above ₱100,000, proposed
by Procurement Head, confirmed by Chief Operating Officer, three working days.

### G4 — Hard block 6 does not fire on purchase orders.

That same ₱500,000 purchase order was raised against project PRJ-2026-0041,
whose only contract is in `draft` status with no signed document reference.

Section 5 anticipates this exact failure by name:

> **Hard block 6 blocks three specific actions and the third is the one most
> likely to be missed:** the project cannot leave `setup`; no fund release; **and
> no purchase order may be raised.** Blocking payment while allowing purchase
> orders means Magnus has committed money without a contract and discovers it
> when payment is due. The block sits on the commitment.

The block sits on none of the three. Yesterday I showed the project walking
`setup` → `procurement` → `construction` with no contract. Today it also raises
purchase orders.

### G5 — Four of the six hard blocks are not the specified ones.

| # | Section 5 requires | Deployment has | |
|---|---|---|---|
| 1 | Mobilisation blocked until the **insurance certificate document** is attached | "A project cannot leave setup without a signed contract" | **wrong** |
| 2 | Start of construction blocked until the **Department of Labor and Employment approved Construction Safety and Health Program** is recorded | "No site report for a workday prevents that day entering payroll" | **wrong** |
| 3 | Start of the first electrical block blocked until **Block B0 Site Safety Infrastructure reaches `signed_off`** | "A site report cannot be submitted without a toolbox meeting that day" | **wrong** |
| 4 | Mobilisation blocked where a **prerequisite permit** is required first | "A project cannot be closed out while a required permit is open" | **wrong** |
| 5 | Issue of quarantined material | Quarantined material blocks deployment | **correct** |
| 6 | Release of funds blocked until the **signed contract document** is uploaded | "No fund disbursement without an approved fund request" | **wrong condition** |

Blocks 1, 2 and 3 are the safety blocks — insurance cover, the Department of
Labor and Employment programme, and the site safety infrastructure block that
must be signed off before anyone works on live electrical. All three are gone,
replaced by process-hygiene rules that belong in the warning layer, not in the
closed list of six things nobody may override.

Block 6 keeps its name but not its condition: it now asks for an approved fund
request rather than a signed contract, which is a different control entirely —
an internal approval instead of a client commitment.

Section 5 also says: *"Do not add a seventh hard block, and do not promote a
warning to a block because it seemed more correct."* Four warnings were promoted
and four blocks were dropped to make room.

### G6 — The hard block attempt log is empty.

`list_hard_block_attempts` returns `[]`. Section 5: *"Every attempt is logged,
including every attempt that fails, which is all of them."* Nothing is logged
because nothing blocks. The three attempts I made today — activating a
contractless project, raising a purchase order against it, issuing a permit —
all succeeded, so there was nothing to record.

### G7 — Thirteen gate numbers point at the wrong action.

| # | Section 6 gate | Deployment label |
|---|---|---|
| 5 | Purchase order above ₱100,000 | Purchase Order Amendment |
| 7 | Quotation below policy markup | Opportunity Won |
| 8 | **Variation order issued to client** | Contract Execution |
| 9 | **Contract signature** | Contract or Agreement Variation |
| 10 | Counsel contract review — Atty. Caneja | Risk Register Review |
| 11 | Progress claim issued | Subcontractor Award |
| 12 | Retention invoice issued | Subcontractor Payment |
| 20 | Permit consultant engagement | Permit Submission |
| 21 | Turnover Document issue to client | Commissioning Authority |
| 23 | **Payroll release** | Fund Request Release |
| 25a | **Inter-island** warehouse transfer | Progress Claim — Submission |
| 25b | Within-island transfer above ₱100,000 | Progress Claim — Certification |
| 30 | **Incident investigation closure** | Payroll Run Approval |

Gates 8 and 9 are swapped with each other. Gate 30 — incident investigation
closure, a safety decision requiring the Safety Officer countersigned by the
Chief Operating Officer — has become a payroll approval, and payroll has moved
from its own gate 23 onto gate 30, displacing it.

This breaks every cross-reference in the instruction. Section 8.5 says a
structural reinforcement *"raises a variation order under gate 8, never a task"*
— gate 8 is now contract execution. Section 6 itself says: *"that numbering is
withdrawn so every gate number already in use still points at the same gate."*

### G8 — Gate rows carry no approver and no threshold.

Fields present on a gate row: `gateId`, `label`, `description`,
`windowWorkingDays`, `active`, `noAlternate`. That is all.

Absent: the primary approver role, the alternate approver role, and the value
band. So even now that roles are assigned, no gate can route to a person, and
R6 — self-approval refused everywhere — cannot be evaluated, because the gate
does not know who is supposed to approve it.

The recorded windows are also wrong on at least twelve rows. Section 6 against
the deployment: gate 2 should be 3 working days and is 5 · gate 5 should be 3
and is 2 · gate 8 should be 2 and is 3 · gate 11 should be 2 and is 3 · gate 12
should be 5 and is unset · gates 19, 20, 21, 24, 25a, 25b and 26 all have
recorded windows in section 6 and none in the deployment.

### G9 — A hot-work permit was issued by someone who is not a Safety Officer.

`create_permit_to_work` accepted PTW-VERIFY-001, type `hot_work`, naming Karl
Ivan Estadola — Chief Executive Officer, not a Safety Officer — as the issuer.
No gate, no refusal.

Locked principle L8: *"Safety approvals are never automated. Permits to work,
lifting a safety stop, closing an incident investigation and the Professional
Electrical Engineer seal are decided by a qualified person, every time."*
Section 6 gate 28: permit to work, Safety Officer of record, **no alternate** —
and section 15 forbids *"auto-approval or delegation on any permit to work."*

Also: `get_permit_to_work` does not exist. `create_permit_to_work` and
`update_permit_to_work` do. A permit can be issued and amended but not read
back.

### G10 — Duplicate role assignments are accepted.

You assigned Chief Executive Officer to yourself at 03:30:00 and Chief Operating
Officer to Beda at 03:29:35 through the browser. My protocol calls a few minutes
later created exact duplicate rows — same person, same role, both
`revoked: false`. There is no uniqueness check.

I have revoked the two duplicates I created. Your originals stand, so both roles
are correctly held.

### G11 — Role assignment bypasses its own gate.

`create_person_role` writes directly. Section 6 gate 24: *"New hire, or
assignment of a role to a person"* — proposed by a department head, confirmed by
the Chief Operating Officer, five working days. Granting someone Chief Operating
Officer is currently a single unreviewed call.

### G12 — The undeclared-enum defect repeated across the new surface.

Of 80 enum-shaped parameters across the 400 tools, **63 declare no enum** in
their input schema. Wrong values still return `-32603 Internal error` carrying
Convex validator text and source paths — for example
`at async handler (../../convex/mcp/group3bInternals.ts:1380:21)`.

This was defect 7 of the Group 2 list, unsent when Group 3 was built. It is now
a habit spread across three files.

---

## 3. What this means

The four groups delivered the objects. The control layer that section 5 and
section 6 exist to specify has been built as **decoration**: a gate table with
the right number of rows and the wrong contents, a hard block table with the
right number of rows and the wrong conditions, an approval queue addressed to
nobody, and an attempt log that has never recorded anything because nothing has
ever been refused.

Nothing in the platform currently stops a person from writing off any amount at
the lowest authority, committing money with no contract, or authorising hot work
without a Safety Officer. Before managers test it, they should be told that
approvals are not yet real, so that nothing they do in it is treated as
authorised.

---

## 4. Test data left in the platform

All marked "TEST DATA - Group 3 verification", all on project PRJ-2026-0041:

- `WO-VERIFY-001` — write-off, ₱150,000, `vs77xfs0esfegsjzqq3pe5pzf58ds3z0`
- `PO-VERIFY-001` — purchase order, ₱500,000, `ps72sf509gxzxbgdr4mfcg24g18dspvs`
- `PTW-VERIFY-001` — permit to work, hot work, `tx7apc71x38023h7n5yt4hb0a18dse2w`

There are no delete tools for these, so they need clearing with the Group 2 test
chain when the fixes go in.
