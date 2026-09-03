# Group 2 protocol verification — 3 September 2026

Verified against the published deployment `elegant-cormorant-29`, over the
Model Context Protocol, decide-scope session `n57e846n37jy6h59rgfdw92zkd8dq5z3`,
caller Karl Ivan Estadola. No browser was used. Every statement below is the
result of a call, not a reading of Hercules' report.

---

## 1. What was verified

`tools/list` returns **95 tools** (was 56 after Group 1, so 39 added). All nine
Group 2 objects are reachable: opportunity, site_assessment, proposal, project,
contract, project_party, project_block, risk_term, variation_order.

A complete commercial chain was created end to end over the protocol, on the
Calamba Agro Industrial Corporation record:

| # | Object | Identifier | Result |
|---|---|---|---|
| 1 | opportunity | `md7e1tb0ccsgve8zyrc4bat9cx8dpvqq` | Calamba Agro 480 kWp rooftop |
| 2 | site_assessment | `mx7ec99yn4m5ey0px0t4tmf5598dqt0z` | proceed_with_conditions |
| 3 | proposal | `ms7e17hr95kqzw4z7z7hy8fq4x8dqzzd` | PRP-2026-0041 v1 |
| 4 | project | `mn78eke2yn0tsg4365vfgxyw118dqmsv` | PRJ-2026-0041 |
| 5 | contract | `n972pjc4a5dfyqqrbaw1sgqze98dpz0p` | CTR-2026-0041, ₱31,500,000, epc_lump_sum |
| 6 | project_party | `nd784qgqgdv7p3rjnewbx5ss518dqjb6` | engineer_in_charge, Alfie Villalon |
| 7 | project_block | `q571vt8e8333spz03rcdfg0xh98dqdz4` | B0 enabling works |
| 8 | project_block | `q57dprxf2xsxmjm154h8kpg3qx8dqfgb` | B1 east roof electrical |
| 9 | variation_order | `ns7ehd33qvgwsye2axjc0x4k4h8dqwpd` | VO-2026-0041-01, ₱1,850,000 |

**Three things are right and worth saying so.**

**The risk-term register seeds itself.** `list_risk_terms` on the new project
returned rows whose `_creationTime` is identical to the project's, to the
fraction of a millisecond — `1788470238337.614`. The register is written inside
the project-creation mutation, not by a follow-up step. That is same-transaction
derivation done correctly, and it is why there is no `create_risk_term` tool.
Nothing is missing there.

**No invalid value was ever stored.** Five deliberately wrong enum values were
rejected at the database. The refusal is ugly (see D7) but it holds.

**The session boundary is intact.** `get_session_info` returns scope `decide`,
the caller, the session identifier and an expiry of 2026-09-04T01:39:36Z.

---

## 2. Defects, ranked by what they cost

### D1 — Hard block 6 is not enforced at all. *(most serious)*

Project PRJ-2026-0041 has **no contract linked and no signed document**. Over the
protocol it moved `setup` → `procurement` → `construction`. Both calls returned
`"Project ... updated"`.

Section 8.3: *"the project cannot become `active` until the signed contract is
uploaded — hard block 6."* Section 5 lists it among the six blocks that cannot be
overridden by anyone, including you.

Two things are wrong. There is no `active` state at all — the lifecycle is
setup / design / procurement / construction / commissioning / handover /
completed / on_hold / cancelled — so the block was written against a state that
does not exist and therefore never fires. And nothing else was substituted for
it. This is the same root cause as the earlier `hardBlock6Active` reporting bug:
it is not a reporting bug, the block is absent from the write path.

The block must gate every transition out of `setup`. A project reaching
`procurement` is a project raising purchase orders; a project reaching
`construction` is a project mobilising people to a roof. Both spend money, which
is exactly what section 8.3 says sales winning does not authorise.

### D2 — Winning an opportunity produces none of its four consequences.

`update_opportunity` with `status: "won"` returned success. After it: no project
was created, the proposal did not freeze, no project blocks were seeded from the
proposal's block structure, and the site assessment did not carry to the design
package. `search_projects` returned `[]`.

Section 8.3, and section 1 item 4: *"On `won`, inside the single mutation that
changes the stage and nothing else — no follow-up action, no scheduled step:
the winning proposal freezes · a project is created in `setup` · the site
assessment carries to the design package · the proposal's block structure seeds
the project blocks."* It is named there explicitly as *"one human action, one
mutation, four stored consequences."*

Today `create_project` is a separate manual call taking opportunityId,
proposalId and a project number the user invents. It is a step a person must
remember, on the one transition where forgetting it costs the most.

### D3 — The proposal on a won opportunity is still editable.

With the opportunity at `won`, `update_proposal` changed `systemSizeKwp` from
480 to 999 and was accepted. Section 8.3: *"When an opportunity is won the
winning proposal version becomes immutable. It is what the contract was priced
against, and every later margin question is answered against it or not answered
at all."* Section 15, the deliberately-not-built register, lists *"editing a frozen
winning proposal"* among the things the platform must refuse, citing section 8.3.

The test value has been restored to 480 and the change noted on the record.

### D4 — An approved variation order does not move the contract value.

VO-2026-0041-01 for ₱1,850,000 was moved to `approved`. The contract stayed at
₱31,500,000. It should read ₱33,350,000, and the block value weights should have
re-based.

Section 8.4: *"A variation order never overwrites the contract. Only `accepted`
re-bases block value weights and moves the contract value."* Note the state name
— the built enum is draft / pending_approval / approved / rejected / cancelled,
with no `accepted`, so the state the spec attaches the money to does not exist.
Section 8.7 also requires the interface to show percentage complete **before and
after** a re-base, so that a project dropping from 62% to 58% overnight reads as
correct rather than as a defect.

### D5 — The proposal state machine is not the specified one.

| Built | Specified (§8.3) |
|---|---|
| draft | draft |
| submitted_for_review | awaiting_approval |
| approved_internal | — |
| rejected_internal | — |
| sent_to_client | issued |
| under_negotiation | — |
| accepted | won |
| declined | lost |
| frozen | — |
| — | **superseded** |

`superseded` is the one that matters. Without it there is no way to record that
version 1 was replaced by version 2, and the version history is precisely what
every later margin question is answered against.

### D6 — `site_assessment` drops the fields the section was written for.

`structural_confidence` is marked **required** in section 8.3 and is not in the
tool at all. It is the single field the spec argues for at length: *"a pattern of
low-confidence assessments becoming reinforcement variations is a pricing
signal. Recorded after the fact, everyone remembers being confident."* Our own
VO in this test is a purlin-reinforcement variation — the exact case the field
exists to predict — and there is nothing on the assessment to correlate it
against.

Also absent as structured fields: `roof_type`, `usable_area_square_metres`,
`obstructions`, `structural_opinion`, `tapping_point_voltage`,
`tapping_point_phase`, `tapping_point_spare_capacity`, `consumption_profile`,
`photographs` (in-app capture only). They were replaced by five free-text boxes:
roofCondition, shadingNotes, gridCondition, accessNotes, structuralNotes — and a
`recommendation` enum the spec does not define was added in their place.

Section 8.3: *"Every field not captured here is a second site visit — on a
Sorsogon or Dumaguete site that is a day and a flight, not an hour."* Spare
capacity at the tapping point written in prose cannot be queried, so the question
"which sites can take another 200 kW" is a second visit.

### D7 — No enum is declared in any Group 2 input schema.

Five wrong guesses, five identical failures. Example:

```
create_contract  contractType: "epc"
→ -32603 Internal error
  "Failed to insert or update a document in table \"contracts\" ...
   Validator: v.union(v.literal(\"epc_lump_sum\"), ...)
   at async handler (../../convex/mcp/group2Internals.ts:587:6)"
```

Three problems. The allowed values are not discoverable from `tools/list`, so
they must be guessed. The failure arrives as a generic internal error rather than
a refusal, so a client cannot distinguish "you sent a bad value" from "the server
is broken". And the stack trace leaks source paths and line numbers to any token
holder.

Group 1 does this correctly — `create_person` refuses with *"Invalid homeRegion
"Nigeria". Must be one of: Luzon, Bicol, Visayas, Mindanao, overseas."* Group 2
needs the same treatment, and it is not cosmetic: the migration import is an
agent reading 25 spreadsheet sheets and mapping their values onto these enums.
Undiscoverable vocabularies turn that into trial and error at scale.

Affected at minimum: `site_assessment.recommendation`, `proposal.status`,
`project.status`, `contract.contractType`, `project_party.role`,
`variation_order.status`.

### D8 — Nothing can post into a record thread over the protocol.

`post_message` requires either a `threadId` or a `channelId`. No tool returns or
creates the thread belonging to an object. `list_threads` returned `[]` for
project, variation_order, project_block, opportunity, proposal and contract.

Lazy thread creation is correct and was our decision. But the consequence is that
until a human opens a record in the browser and types the first message, that
record's conversation is unreachable from the protocol. Your hourly-scheduler
plan — Claude connecting each hour, reading what needs answering, replying where
it is mentioned — cannot touch any record thread that a person has not already
opened. It also means historical discussion cannot be imported alongside the
records during migration.

Needed: `get_or_create_object_thread(objectType, objectId)` returning the
thread, or let `post_message` accept `objectType` + `objectId` and create the
thread on first write, exactly as the browser does.

### D9 — `account` is still collapsed into `party`.

Unresolved from the Group 1 note. Section 8.3 defines `account` (account_id,
account_name, industry, active) as its own object, separate from the section 8.4
`party`. `list_parties` with `partyType: "customer"` is not a substitute: it
cannot model a customer whose contracting entity is a different legal name — the
shape of Magnus Energy Corp in your own pipeline.

Section 15 settles it independently. Its not-built register forbids *"site as a
field on the account"* and cites section 8.3. A rule about what may not be a
field on the account presumes the account is an object with fields. It cannot be
a filtered view of `parties`.

---

## 3. Still open from earlier rounds

- `get_board_pack` returns no pending-approvals count.
- Self-approval (R6) is enforced session-against-session, not person-against-person.
  Two tokens held by one person are one person.
- `propose_decision` is free text with no object linkage, so confirming it
  changes nothing real.
- O&M, milestone 6: seven of nine module-26 tables do not exist.

---

## 4. Test data left in the platform

All of it is tagged "Group 2 verification" in the notes field and belongs to
Calamba Agro Industrial Corporation, PRJ-2026-0041. It should be deleted before
the managers test, or kept deliberately as a worked example. The proposal's
systemSizeKwp was restored to 480 after the immutability test; nothing else was
left altered.
