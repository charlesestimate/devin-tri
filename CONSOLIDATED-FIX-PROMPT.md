# Prompt for Hercules — consolidated conformance fixes, Groups 2 and 3

Groups 2 and 3 are deployed. I verified all 400 tools over the Model Context
Protocol against the published deployment. The object layer is genuinely
built — 305 new tools dispatch, Operations and Maintenance exists, eighteen
roles are seeded with the right names, the gate table has the correct thirty-row
numbering skeleton and the hard block table correctly has six rows and no
`active` column. That work is real and I am not asking you to redo it.

**The control layer is not built.** The gate table has the right number of rows
and the wrong contents. The hard block table has the right number of rows and
the wrong conditions. The approval queue is addressed to nobody. The attempt log
has never recorded anything, because nothing has ever been refused. Over the
protocol today I routed a ₱150,000 write-off to the lowest approval authority by
typing one word, raised a ₱500,000 purchase order against a project with no
signed contract, and issued a hot-work permit as someone who is not a Safety
Officer. All three succeeded silently.

Twenty-eight items follow, in three parts. **Part A is the priority — nothing in
the platform is safe to use until it is done.** Each item names the section it
violates and the call that proved it.

Report against the numbered list, one line per item, naming the file and function
you changed and **the call you ran to prove it**. Do not report an item complete
because the code reads correct — items 1 through 6 all passed a clean build and
none of them work.

---

# PART A — THE CONTROL LAYER

## 1. The gate is chosen by the caller instead of derived from the amount

`create_write_off` takes `severity` as a required input, validated as
`minor` / `moderate` / `major`, mapping onto gate rows 1, 2 and 3. I created a
write-off of ₱150,000 declared `"minor"`. It stored `gateId: "1"`.

Section 6: gate 1 is up to ₱50,000 (Head of Finance); gate 3 is above ₱100,000
(Chief Executive Officer, no alternate). The gate is derived from the amount and
is never chosen.

Delete the `severity` input. Compute the gate from `amount` inside the mutation.
Then audit every other gate with a value band and do the same: gates 4 and 5
(purchase order, ₱100,000 boundary), gate 7 (markup below policy), gate 25b
(within-island transfer above ₱100,000). Any tool that lets a caller name a band,
a tier, a severity or a gate is the same defect.

## 2. Gate rows carry no approver and no threshold

A gate row has `gateId`, `label`, `description`, `windowWorkingDays`, `active`
and `noAlternate`. It has no primary approver role, no alternate approver role
and no value band.

So no gate can route to a person even now that roles are assigned, and R6 —
self-approval refused everywhere — cannot be evaluated, because the row does not
know who should approve it.

Add `primaryRoleName`, `alternateRoleName` (null where section 6 says **none**),
and the value band where the gate has one. Reseed all thirty rows from the
section 6 table.

## 3. Thirteen gate numbers point at the wrong action

| # | Section 6 gate | You built |
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
closure, a safety decision needing the Safety Officer countersigned by the Chief
Operating Officer — has become a payroll approval, and payroll has moved off its
own gate 23 onto gate 30, displacing it.

Section 6 states the reason this must not happen: *"that numbering is withdrawn
so every gate number already in use still points at the same gate."* Section 8.5
tells you a structural reinforcement *"raises a variation order under gate 8"* —
which now means contract execution.

Reseed all thirty rows verbatim from the section 6 table: number, action,
trigger, primary, alternate, window.

## 4. The recorded windows are wrong on twelve rows

Section 6 against the deployment: gate 2 should be 3 working days and is 5 · gate
5 should be 3 and is 2 · gate 8 should be 2 and is 3 · gate 11 should be 2 and
is 3 · gate 12 should be 5 and is unset · gates 19, 20, 21, 24, 25a, 25b and 26
each have a recorded window in section 6 and none in the deployment.

The window is recorded only, never enforced — but it is what the exception
report ages approvals against, so a missing window means an approval never reads
as late.

## 5. No write raises an approval request

The ₱150,000 write-off stored `status: "pending_approval"` and `gateId: "1"` and
created nothing. `list_approval_requests` returns three pre-existing rows, every
one of them `currentApprover: "unassigned"` with `objectType`, `objectId` and
`amount` all null.

So a record can sit at `pending_approval` forever, asked of nobody, appearing on
no screen.

Every gated write must, inside the same mutation, create an approval request
carrying the object type, the object id, the amount, the derived gate, the
approver role resolved to a person, and the arrival channel. A gated write with
no approval request is not a gated write.

## 6. Purchase orders carry no gate

A ₱500,000 purchase order was created with no `gateId` and no approval request.
Section 6 gate 5: above ₱100,000, Procurement Head to Chief Operating Officer,
three working days. Below ₱100,000 is gate 4, Procurement Officer to Procurement
Head, two days. Derive it from `totalValue`.

## 7. Hard block 6 does not fire on purchase orders — the case section 5 named

That ₱500,000 purchase order was raised against project PRJ-2026-0041, whose
only contract is `draft` with no signed document.

Section 5 anticipates this by name:

> **Hard block 6 blocks three specific actions and the third is the one most
> likely to be missed:** the project cannot leave `setup`; no fund release;
> **and no purchase order may be raised.** Blocking payment while allowing
> purchase orders means Magnus has committed money without a contract and
> discovers it when payment is due. The block sits on the commitment.

Yesterday the same project moved `setup` → `procurement` → `construction` with
no contract at all. The block sits on none of its three actions. Implement all
three, on the write path.

## 8. Four of the six hard blocks are not the specified ones

| # | Section 5 requires | You seeded |
|---|---|---|
| 1 | Mobilisation blocked until the **insurance certificate document** is attached — not a tick-box. Configurable value: ₱2,000,000 contract value | "A project cannot leave setup without a signed contract" |
| 2 | Start of construction blocked until the **Department of Labor and Employment approved Construction Safety and Health Program** is recorded | "No site report for a workday prevents that day entering payroll" |
| 3 | Start of the first electrical block blocked until **Block B0 Site Safety Infrastructure reaches `signed_off`** | "A site report cannot be submitted without a toolbox meeting that day" |
| 4 | Mobilisation blocked where a **prerequisite permit** is required first. Configurable: which permit types apply | "A project cannot be closed out while a required permit is open" |
| 5 | Issue of quarantined material to a site | correct |
| 6 | Release of funds blocked until the **signed contract document** is uploaded | "No fund disbursement without an approved fund request" — wrong condition |

Blocks 1, 2 and 3 are the safety blocks: insurance cover, the Department of
Labor and Employment programme, and the site safety infrastructure that must be
signed off before anyone works on live electrical. All three are missing. In
their place are process-hygiene rules that belong in the warning layer.

Section 5: *"Do not add a seventh hard block, and do not promote a warning to a
block because it seemed more correct."* Four warnings were promoted and four
blocks were dropped to make room for them.

Reseed the six rows from the section 5 table and implement each on the write
path. The rules you invented are worth keeping — as warnings, not as blocks.

## 9. The blocked-action message

Section 5: *"The blocked-action message states: which block · what specific
condition is unmet · what would release it · and who can supply it. It must
never say 'you do not have permission.'"* Build the message in that shape, and
return it over the protocol as a refusal, not as a `-32603` internal error.

## 10. The hard block attempt log has never recorded anything

`list_hard_block_attempts` returns `[]`. Section 5: *"Every attempt is logged,
including every attempt that fails, which is all of them."* Log every attempt,
including the successful ones once the blocks actually fire.

## 11. A hot-work permit was issued by someone who is not a Safety Officer

`create_permit_to_work` accepted PTW-VERIFY-001, type `hot_work`, naming the
Chief Executive Officer as issuer. No gate, no refusal.

Locked principle L8: *"Safety approvals are never automated. Permits to work,
lifting a safety stop, closing an incident investigation and the Professional
Electrical Engineer seal are decided by a qualified person, every time."*
Section 6 gate 28: Safety Officer of record, **no alternate**. Section 15
forbids *"auto-approval or delegation on any permit to work; an alternate Safety
Officer for lifting a safety stop."*

Refuse a permit to work whose issuer does not hold Safety Officer. Same for
gate 29 (safety stop lifted) and gate 30 (incident investigation closure).

Also: `get_permit_to_work` does not exist, while create and update do. A permit
can be issued and amended but never read back. Add it, and sweep for other
objects missing a `get`.

## 12. Role assignment bypasses its own gate, and duplicates are accepted

`create_person_role` writes directly. Section 6 gate 24: *"New hire, or
assignment of a role to a person"* — department head to Chief Operating Officer,
five working days. Granting Chief Operating Officer is currently one unreviewed
call.

Separately, the same person can be assigned the same role twice: two live rows
now exist for two people, both `revoked: false`, because there is no uniqueness
check. Section 2.3 requires uniqueness rules to be enforced inside the mutation
as a refusal. Add one, and de-duplicate the existing rows.

---

# PART B — THE COMMERCIAL CHAIN

## 13. Winning an opportunity produces none of its four consequences

`update_opportunity` with `status: "won"` returns success and does nothing else.
No project, no frozen proposal, no seeded blocks, no site assessment carried
forward.

Section 8.3 and section 1 item 4: on `won`, inside the single mutation that
changes the stage and nothing else — no follow-up action, no scheduled step —
the winning proposal freezes, a project is created in `setup`, the site
assessment carries to the design package, and the proposal's block structure
seeds the project blocks. *"One human action, one mutation, four stored
consequences."*

Build all four inside `update_opportunity`. Keep `create_project` for migration
of historical records only, and say so in its description.

## 14. A won opportunity's proposal is still editable

With the opportunity at `won`, `update_proposal` changed `systemSizeKwp` from
480 to 999 and accepted it. Section 8.3: the winning proposal version becomes
immutable. Section 15 lists *"editing a frozen winning proposal"* among the
things the platform must refuse. Refuse every field change on a frozen proposal.
Status alone may move to `superseded`.

## 15. An approved variation order does not move the contract value

A variation order for ₱1,850,000 moved to `approved`; the contract stayed at
₱31,500,000 instead of ₱33,350,000, and block value weights did not re-base.

Section 8.4: *"Only `accepted` re-bases block value weights and moves the
contract value; `issued` and `rejected` change nothing."* Your enum is draft /
pending_approval / approved / rejected / cancelled — the state the money is
attached to does not exist. Use the specified vocabulary, migrate existing rows,
and re-base inside the same mutation. Section 8.7 also requires the interface to
show percentage complete before and after the re-base.

## 16. The proposal state machine is not the specified one

Section 8.3 specifies draft / awaiting_approval / issued / superseded / won /
lost. You built draft / submitted_for_review / approved_internal /
rejected_internal / sent_to_client / under_negotiation / accepted / declined /
frozen.

`superseded` is not optional: without it there is no way to record that version 1
was replaced by version 2, and version history is what every later margin
question is answered against. Replace with the specified six and migrate.

## 17. `site_assessment` is missing the fields the section exists for

`structural_confidence` (`high`/`medium`/`low`) is marked **required** in section
8.3 and is absent. It is the field the section argues for at length: a pattern of
low-confidence assessments becoming reinforcement variations is a pricing signal.

Add it, and add these as structured fields rather than prose: `roof_type`,
`usable_area_square_metres`, `obstructions`, `structural_opinion`,
`tapping_point_voltage`, `tapping_point_phase`, `tapping_point_spare_capacity`,
`consumption_profile`, `photographs` (in-app capture only).

Keep your free-text notes alongside them. Spare capacity written in prose cannot
be queried, and section 8.3 says every field not captured here is a second site
visit — on a Sorsogon or Dumaguete site that is a day and a flight.

## 18. `account` is still collapsed into `party`

Section 8.3 defines `account` — account_id, account_name, industry, active — as
its own object, separate from the section 8.4 `party`. `list_parties` with
`partyType: "customer"` cannot model a customer whose contracting entity is a
different legal name, which is the shape of Magnus Energy Corp in Magnus's own
pipeline.

Section 15 settles it independently: its not-built register forbids *"site as a
field on the account"* and cites section 8.3. A rule about what may not be a
field on the account presumes the account is an object with fields.

Build `account` with its own table and its own list / get / search / create /
update tools, linked to `party`.

---

# PART C — PROTOCOL HYGIENE

## 19. Sixty-three of eighty enum-shaped parameters declare no enum

Across the 400 tools, 63 of 80 enum-shaped input parameters carry no `enum` in
their schema. A wrong value returns `-32603 Internal error` carrying raw Convex
validator text and source paths, for example
`at async handler (../../convex/mcp/group3bInternals.ts:1380:21)`.

Three problems: the allowed values are not discoverable from `tools/list`, so a
client must guess; the failure is a generic internal error, so a client cannot
tell a bad value from a broken server; and the stack trace leaks source paths to
any token holder.

Group 1 does this correctly — `create_person` refuses with *Invalid homeRegion
"Nigeria". Must be one of: Luzon, Bicol, Visayas, Mindanao, overseas.* Apply that
everywhere: allowed values in the schema `enum` and in the description, validated
in the handler, refused with that message shape. **No Convex validator error
should ever reach the protocol.**

This is not cosmetic. The migration import is an agent reading twenty-five
spreadsheet sheets and mapping their values onto these enums.

## 20. Nothing can post into a record thread over the protocol

`post_message` requires a `threadId` or `channelId`, and no tool returns or
creates the thread belonging to an object. `list_threads` returned `[]` for
project, variation_order, project_block, opportunity, proposal and contract.

Lazy creation is correct. The gap is that a record's conversation is unreachable
until a human opens it in the browser and types the first message. Add
`get_or_create_object_thread(objectType, objectId)`, or let `post_message` accept
`objectType` + `objectId` and create the thread on first write exactly as the
browser does. Section 8.13 requires a thread on every object without exception;
that must hold over the protocol too.

## 21. Several list tools require a filter that should be optional

`list_roles` requires `limit`. `list_person_roles` requires `personId`.
`list_threads` requires `objectType`. `list_hard_block_attempts` requires
`limit`. A list tool that cannot list is a query tool. Make the filters optional
with sensible defaults, keeping pagination.

## 22. `employmentBasis` on a person is completely unvalidated

`create_person` accepted `employmentBasis: "zzz"` and stored it. The field has no
enum and no handler check, while `population`, `homeRegion` and `status` on the
same object all validate correctly.

Give it an enum. It must include at least `employee`, `consultant`,
`project_based` and `on_call` — the last two carry the engagement distinction for
site installers, which is recorded on the person rather than as a separate role.
One probe record, `ks7848gaa08b1qz0mcj34dghr58ds5hv`, is marked `departed` and
renamed "ZZ DELETE ME - probe artefact"; delete it.

## 23. A role's permissions cannot be changed, so gate 32 has nothing to gate

`update_role` accepts only `label`, `description` and `active`. It cannot change
`recordScope`, `moneyVisibility`, `isApprover` or `name`.

Section 6 gate 32 is *"Change to what a role may do — Administration Console
holder, alternate Second console holder."* That gate exists precisely to govern
changes to record scope, money visibility and approver status. Today those
changes are impossible, so the gate governs nothing — and a role created with the
wrong money visibility can only be replaced, never corrected.

Allow `recordScope`, `moneyVisibility` and `isApprover` to be updated, routed
through gate 32 with two console holders. `name` stays immutable; it is the
internal key.

## 24. The board pack shows no pending approvals

`get_board_pack` returns `activeProjects`, `activeDeployments`, `openTasks`,
`openNcrs`, `openIncidents` and a project breakdown. It does not return approvals
pending.

Section 8 requires, among the board pack figures: *"approval requests pending,
with age in working days and the recorded window."* An approval waiting past its
window is the single figure the pack exists to surface, and it is the one absent.
Add it — count, age in working days per request, and the gate's recorded window —
once item 5 makes approval requests real.

## 25. `propose_decision` is free text and links to nothing

`propose_decision` takes one argument: `proposal`, a string. It does not name an
object, an object type, an amount or a gate. `confirm_decision` then takes a
session id and a code.

So the propose-then-confirm handshake changes nothing real. Two people can
faithfully complete it and no record moves, because the proposal was a sentence
rather than a reference to a row.

Give it `objectType`, `objectId`, the intended change, and the derived gate.
Confirming must apply that change to that row inside the mutation, or refuse.

## 26. Self-approval is enforced against sessions, not people

`confirm_decision` requires `proposingSessionId` to differ from the confirming
session. Two tokens held by the same person are two sessions and one person, so
the check passes while R6 is violated.

R6 refuses self-approval everywhere. Compare the `personId` behind each session,
not the session identifier — and once item 2 gives gates their approver roles,
also refuse where the proposer and confirmer resolve to the same person through
any role.

## 27. The protocol layer must not write to tables directly

Root cause, found on reading the source. `convex/mcp/*.ts` imports
`internalMutation`, `internalQuery`, Convex validators, generated types,
`createTenantDb` and `appendAuditEntry` — **and nothing from any domain module.**
Across the protocol layer there are **178 direct `db.insert` and `db.patch`
calls**: every write reimplemented inline rather than delegated to the mutation
that owns the rule.

That is why every control-layer failure I reported reproduces over the protocol
regardless of what the domain enforces: the protocol never reaches it.
`convex/foundation/hardBlocks.ts` exists and works; the protocol layer never
imports it.

Two consequences. Every fix on the 26 items above has to be written twice or the
paths drift. And a rule added next month is enforced on the screen and not over
the protocol, silently.

Replace the 178 direct writes with calls to the domain mutations, then **fail the
build on any `db.insert` or `db.patch` inside `convex/mcp/`** — the same
technique section 2.6 already uses for `ctx.db` outside the tenant wrapper.

Do this **after** items 1 to 12, not before. The domain rules are themselves
wrong today: `finance.ts` derives the write-off gate from
`gateIdForSeverity(args.severity)`, and `orders.ts` implements hard block 6 as a
gate 4 approval check rather than a signed-contract check. Converging the
protocol onto rules that are wrong would make both paths wrong in the same way
and throw the work away.

## 28. Test data to clear

Marked "Group 2 verification" or "TEST DATA - Group 3 verification", all on
Calamba Agro Industrial Corporation / PRJ-2026-0041:

- opportunity `md7e1tb0ccsgve8zyrc4bat9cx8dpvqq`, site assessment
  `mx7ec99yn4m5ey0px0t4tmf5598dqt0z`, proposal `ms7e17hr95kqzw4z7z7hy8fq4x8dqzzd`,
  project `mn78eke2yn0tsg4365vfgxyw118dqmsv`, contract
  `n972pjc4a5dfyqqrbaw1sgqze98dpz0p`, variation order
  `ns7ehd33qvgwsye2axjc0x4k4h8dqwpd`, two project blocks, one project party
- write-off `vs77xfs0esfegsjzqq3pe5pzf58ds3z0` (₱150,000)
- purchase order `ps72sf509gxzxbgdr4mfcg24g18dspvs` (₱500,000)
- permit to work `tx7apc71x38023h7n5yt4hb0a18dse2w` (hot work)

Delete them, or tell me you have kept them deliberately as a worked example.

---

## What I will do when you report

I will re-run every call in this list against the published deployment. In
particular I will create a ₱150,000 write-off declared `minor` and expect it to
land on gate 3 or be refused; raise a purchase order against a contractless
project and expect hard block 6; and issue a permit to work as a non-Safety
Officer and expect a refusal naming gate 28. An item is complete when the call
proves it.
