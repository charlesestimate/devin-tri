> **SUPERSEDED — do not send this file.** Its ten items are carried into
> `CONSOLIDATED-FIX-PROMPT.md`, which also covers the Group 3 findings and
> orders everything by priority. Kept here as a record only.

# Prompt for Hercules — Group 2 conformance fixes

Group 2 is deployed and I verified all 39 tools over the protocol. The objects
exist and the risk-term register seeds itself inside the project-creation
mutation, which is correct. Ten defects follow. Each names the section of the
master prompt it violates and the call that proved it. Fix all ten, then report
against the numbered list — one line per item, stating the file and function you
changed and the call you ran to prove it. Do not report an item complete on the
basis of the code reading correct.

---

**1. Hard block 6 is not enforced. Highest priority.**

Project `mn78eke2yn0tsg4365vfgxyw118dqmsv` has no contract row and no signed
document. Over the protocol it moved `setup` → `procurement` → `construction`,
both accepted.

Section 8.3 says the project cannot leave `setup` until the signed contract is
uploaded. Section 5 lists this among the six blocks nobody may override. You
wrote the check against a state named `active`, and the project lifecycle has no
`active` state — it is setup / design / procurement / construction /
commissioning / handover / completed / on_hold / cancelled. The check therefore
never fires.

Gate **every** transition out of `setup` on a contract row existing for the
project AND that contract carrying a signed document reference. Refuse with the
hard-block message and the block number, on the write path, not in a report.
Also fix `hardBlock6Active` to read the same condition, which is why it has been
returning false.

**2. Winning an opportunity produces none of its four consequences.**

`update_opportunity` with `status: "won"` returned success and did nothing else.
No project, no frozen proposal, no seeded blocks, no site assessment carried
forward.

Section 8.3 and section 1 item 4: on `won`, inside the single mutation that
changes the stage and nothing else — no follow-up action, no scheduled step —
the winning proposal freezes, a project is created in `setup`, the site
assessment carries to the design package, and the proposal's block structure
seeds the project blocks. One human action, one mutation, four stored
consequences.

Build all four inside `update_opportunity`. `create_project` stays for migration
of historical records only; mark it so in its description.

**3. A won opportunity's proposal is still editable.**

With the opportunity at `won`, `update_proposal` changed `systemSizeKwp` from 480
to 999 and accepted it. Section 8.3: the winning proposal version becomes
immutable. Section 15 lists "editing a frozen winning proposal" among the things
the platform must refuse. Refuse every field change on a frozen proposal, over
the protocol and in the browser alike. Status alone may move to `superseded`.

**4. An approved variation order does not move the contract value.**

VO for ₱1,850,000 moved to `approved`; the contract stayed at ₱31,500,000
instead of ₱33,350,000, and block value weights did not re-base.

Section 8.4: only `accepted` re-bases block value weights and moves the contract
value; `issued` and `rejected` change nothing. Your enum is draft /
pending_approval / approved / rejected / cancelled — the state the money is
attached to does not exist. Rename to the specified vocabulary, migrate existing
rows, and do the re-base inside the same mutation. Section 8.7 additionally
requires the interface to show percentage complete before and after the re-base.

**5. The proposal state machine is not the specified one.**

Section 8.3 specifies draft / awaiting_approval / issued / superseded / won /
lost. You built draft / submitted_for_review / approved_internal /
rejected_internal / sent_to_client / under_negotiation / accepted / declined /
frozen. Replace with the specified six and migrate existing rows.

`superseded` is not optional. Without it there is no way to record that version 1
was replaced by version 2, and version history is what every later margin
question is answered against.

**6. `site_assessment` is missing the fields the section exists for.**

`structural_confidence` (`high`/`medium`/`low`) is marked **required** in section
8.3 and is absent. It is the field the section argues for at length: a pattern of
low-confidence assessments becoming reinforcement variations is a pricing signal.

Add it, and add these as structured fields, not prose: `roof_type`,
`usable_area_square_metres`, `obstructions`, `structural_opinion`,
`tapping_point_voltage`, `tapping_point_phase`, `tapping_point_spare_capacity`,
`consumption_profile`, `photographs` (in-app capture only).

Keep your free-text notes fields alongside them. Remove `recommendation`, or keep
it as an extra — but it is not a substitute for `structural_confidence`, which is
what the section actually requires. Spare capacity at the tapping point written in
prose cannot be queried, and section 8.3 says every field not captured here is a
second site visit.

**7. No enum is declared in any Group 2 input schema.**

Five wrong guesses produced five `-32603 Internal error` responses carrying raw
Convex validator text and source line numbers, for example
`at async handler (../../convex/mcp/group2Internals.ts:587:6)`.

Three problems: the allowed values are not discoverable from `tools/list`; the
failure is a generic internal error rather than a refusal, so a client cannot
tell a bad value from a broken server; and the stack trace leaks source paths to
any token holder.

Group 1 does this correctly — `create_person` refuses with *Invalid homeRegion
"Nigeria". Must be one of: Luzon, Bicol, Visayas, Mindanao, overseas.* Do the
same across every Group 2 tool: put the allowed values in the input schema
`enum` and in the description, validate in the handler, and refuse with that
message shape. Never let a Convex validator error reach the protocol.

This is not cosmetic. The migration import is an agent reading 25 spreadsheet
sheets and mapping their values onto these enums.

**8. Nothing can post into a record thread over the protocol.**

`post_message` requires a `threadId` or `channelId`, and no tool returns or
creates the thread belonging to an object. `list_threads` returned empty for
project, variation_order, project_block, opportunity, proposal and contract.

Lazy creation is correct. The gap is that a record's conversation is unreachable
until a human opens it in the browser and types the first message. Add
`get_or_create_object_thread(objectType, objectId)` returning the thread, or let
`post_message` accept `objectType` + `objectId` and create the thread on first
write exactly as the browser does. Section 8.13 requires a thread on every
object without exception; that must hold over the protocol too.

**9. `account` is still collapsed into `party`.**

Section 8.3 defines `account` — account_id, account_name, industry, active — as
its own object, separate from the section 8.4 `party`. `list_parties` with
`partyType: "customer"` is not a substitute: it cannot model a customer whose
contracting entity is a different legal name, which is the shape of Magnus
Energy Corp in our own pipeline.

Section 15 settles it independently: its not-built register forbids "site as a
field on the account" and cites section 8.3. A rule about what may not be a field
on the account presumes the account is an object with fields.

Build `account` with its own table and its own list / get / search / create /
update tools, linked to `party`.

**10. There is no way to assign a role to a person, and almost nobody has one.**

`list_persons` returns 22 people. **21 of them have an empty `roles` array.** The
only exception is Kidron Magnus, who carries `project_manager`. Karl Ivan
Estadola, the Chief Executive Officer, has no role. Beda Escobedo, the Chief
Operating Officer, has no role.

There is no `list_roles`, no `assign_role` and no `revoke_role` tool among the 95,
so a role cannot be granted over the protocol at all.

This is not administrative tidying. The Chief Operating Officer appears on
**fifteen of the thirty gate rows** in section 4 — confirming authority on gates
1, 5, 11, 12, 19, 21, 23, 24, 25a, 25b, 26 and 34; proposer on gates 2 and 20;
countersignatory on gate 30. The Chief Executive Officer is the confirming
authority on gates 2, 8 and 20. If neither person holds their role, **no gate in
the platform can resolve** — every write-off, purchase order above ₱100,000,
progress claim, payroll release, stock adjustment and inter-island transfer has
a confirming authority that no account can satisfy.

Note also gate 24: *"New hire, or assignment of a role to a person"* is itself
gated, proposed by a department head and confirmed by the Chief Operating
Officer. So role assignment must go through the gate machinery, not around it.

Build `list_roles`, `assign_role` and `revoke_role`. `assign_role` raises gate 24
rather than writing directly. Report which of the seeded roles exist by name, and
whether Chief Executive Officer, Chief Operating Officer, Head of Finance,
Procurement Head, Department Head, Safety Officer and Process Engineer are among
them — several of the titles the gate table depends on may not have been seeded.

---

## Test data to clear

The verification chain is tagged "Group 2 verification" in the notes field, on
Calamba Agro Industrial Corporation, project PRJ-2026-0041. Delete it once these
fixes are in, or tell me you have kept it deliberately.

## What I will do when you report

I will call `tools/list` on the published deployment, then re-run every call in
this list and confirm each one now refuses or derives as specified. An item is
complete when the call proves it, not when the code reads correct.
