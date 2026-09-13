# Magnus Workspace Platform — Base44 build specification

## Part 01 · Foundation: principles, tenancy, audit, identity, gates, hard blocks, configuration, navigation

**Build this part first and completely. Nothing in Parts 02 to 12 may start until the checks at the end of this part pass.** Everything downstream inherits this part's mistakes: a tenant identifier added to populated tables later is a migration, and an append-only log cannot be retrofitted onto a table that has been edited for four months.

---

## 0. Standing rules — repeated at the top of every part

These ten rules apply to every part of this specification. When a later part is pasted into a fresh session, these are the rules it still runs under.

1. **The platform is a record, a permission boundary, and a Model Context Protocol server. It has no intelligence of its own and performs no unattended action.** Build no scheduler, cron job, automation, background worker, timer, polling loop, rules engine, workflow engine, notification engine, ranking algorithm or digest. If the builder offers "automations", "scheduled tasks", "triggers" or "workflows", do not use them. The one exception is a device push notification fired in the same transaction as a safety stop, an incident, or a statutory deadline record — delivery, not automation.
2. **Four computations are permitted because they run at the moment a person asks:** derived values computed on read · hard block and gate evaluation at the instant a transaction is attempted · permission resolution at the instant a request is served · same-transaction derivation, where a value is stored inside the same transaction as the human action that caused it, using only the fields that action supplied.
3. **Every table carries `tenant_id` and every read and write goes through one server-side data-access layer** that injects the tenant filter, stamps the tenant on insert, and refuses any update or delete of another tenant's record. The browser or phone never writes a governed table directly.
4. **The audit log is append-only and hash-chained.** No code path, role, screen, protocol tool or administrator can edit or delete an entry.
5. **Gates and hard blocks are data rows, not code.** One approval engine serves every gate; no module implements approval logic of its own. Nothing is ever auto-approved.
6. **Every write carries a human being's name.** No service account, no "changed by the system", no agent identity. An agent acts under the credentials of the real person whose work it assists.
7. **No abbreviations anywhere in the interface, in field names, in status values or in messages.** No ampersands. Write *Design and Engineering*, *person_in_charge*, *bill_of_materials*, *non_conformance_report*. An abbreviation may follow the full term in parentheses on first use, never alone.
8. **No Magnus-specific literal in code.** Not ₱2,000,000, not ₱100,000, not 1,277, not 115, not 130, not a label, not a brand name. All of it is configuration rows.
9. **Presence is never tracked.** No location, activity, keystroke, login-time, clock-in, page-view or duration data about any person, at any permission level. No configuration option may switch it on.
10. **Where this specification is silent, ask rather than decide.** A reasonable-looking invented decision is the most expensive defect this project can produce, because nobody notices it.

---

## 1. What is being built and for whom

A multi-tenant operations platform for **Magnus Renewable Tech Corp**, a solar engineering, procurement and construction company in the Philippines running approximately fifty megawatt-peak of commercial and industrial projects, about sixty people across offices, project sites and three regional warehouses in Laguna, Sorsogon and Dumaguete. Magnus is **tenant one** — not tenant zero and not a default. A second, entirely invented tenant is created early in test and kept populated (section 8.3 of this part).

The platform is delivered as a **progressive web application** — one codebase, phone and desktop, installable without an application store, offline-capable for field capture (Part 08). Two product surfaces exist and are built to the same standard: the screens, and the Model Context Protocol server (Part 09) through which external artificial-intelligence agents read, write, decide and configure under a person's name.

### 1.1 Notes for a Base44 build — verify these before starting

The original specification was written for a hand-built backend. Re-expressed here for Base44, the following need confirming against what Base44 can actually do at the time of the build. Each is a requirement, not a preference; if Base44 cannot meet one natively, the shape of the workaround is given.

| Requirement | What to verify in Base44 | If not native |
|---|---|---|
| One server-side chokepoint for every governed read and write | Whether entity access rules can deny all direct client writes on governed entities, so that only backend functions write them | Every governed entity gets a deny-all client write rule; all writes go through backend functions that apply the tenant stamp, the gate check, the hard block check and the audit entry |
| Tenant filter on every read | Whether entity rules can filter reads by a `tenant_id` matched to the signed-in user's tenant | Reads of governed entities also go through backend functions that inject the filter |
| Append-only audit table | Whether an entity can be made insert-only for every role including administrators | Insert through one backend function only; deny update and delete at the entity rule for every role; the hash chain (section 4) detects any edit made by an owner through the builder's own data console |
| No automations | Base44 offers scheduled and event automations. **Do not create any.** A test in Part 12 confirms none exists | — |
| Offline queue on the phone | Whether the generated React application can hold an IndexedDB queue with device-generated idempotency keys and a visible upload queue (Part 08) | This is required, not optional; if the builder cannot generate it, that is a blocking finding to report |
| Google Drive as the file store | Whether a backend function can hold an encrypted OAuth refresh token as a secret and call the Drive API server-side (Part 05 section D) | — |
| Model Context Protocol endpoint | Whether backend functions can expose an authenticated HTTP endpoint that a Model Context Protocol client can connect to | Build the tool layer as authenticated HTTP endpoints with the exact tool names, parameters and rules of Part 09, and put a thin protocol adapter in front of them; the rules are the deliverable, the transport is not |
| Identity | Base44 has its own sign-in with Google. The platform must model identity as **a property of the tenant** (section 5), with the builder's user identifier stored in exactly one field on the person record | — |
| Built-in artificial intelligence | Base44 can call a language model from inside an application. **The platform makes no language-model call from inside itself, ever.** The intelligence connects from outside through Part 09 | — |
| Outbound electronic mail | Base44 offers a send-mail integration. **Not used, for anything** — no digests, no notifications, no summaries | — |

---

## 2. The governing principle

All monitoring, chasing, ranking, escalating, summarising, forecasting and analysis is performed by external agents connecting through the Model Context Protocol server. The platform's job is to hold correct data, refuse the transactions it must refuse, and expose everything it knows to an authenticated agent.

If a feature requires something to happen while nobody is looking at the screen, that feature does not belong in this platform. It belongs to an agent.

### 2.1 The one exception, and it is a safety requirement

Three notification categories also send a device push notification with mandatory acknowledgement: **a safety stop or work suspension · an incident or near-miss requiring immediate action · a statutory deadline breached or imminent.** The list is configurable — categories may be added — and **these three can never be removed and their acknowledgement can never be switched off by any administrator.** The push fires in the same transaction as the record being created. Nothing chases an unacknowledged item; unacknowledged items are queryable and an agent escalates them.

---

## 3. The eight locked principles

- **L1 · The platform records and warns.** It blocks only where the law requires it, money would be irreversibly committed, or a physical action cannot be undone. Exactly six hard blocks; the list is closed.
- **L2 · Every control ships with its verification.** Wherever an assertion is captured, something capable of contradicting it is captured too.
- **L3 · Capture must have consequence.** If a field is captured and never used, delete the field.
- **L4 · Workload is visible. Presence is never tracked.** A legal constraint under Philippine labour law and a commitment made to staff.
- **L5 · Accumulate, do not maintain.** Reference data is accumulated from what happened, never maintained by hand.
- **L6 · The audit log is append-only.**
- **L7 · Operational data informs the conversation; it never produces the rating.**
- **L8 · Safety approvals are never automated.** Permits to work, lifting a safety stop, closing an incident investigation and the Professional Electrical Engineer seal are decided by a qualified person, every time.

---

## 4. Tenant isolation, audit immutability and uniqueness

### 4.1 Tenant isolation

Every table carries `tenant_id` from the first version of the schema. One data-access layer surrounds every database read and write: it takes the authenticated person, injects the tenant filter on every read, stamps `tenant_id` on every insert, and refuses any update or delete whose target belongs to another tenant. A function called by a person of one tenant with a record identifier from another **returns nothing and writes nothing.** A build-failing test asserts that no governed table is read or written except through this layer.

### 4.2 Audit log immutability

**`audit_entry`** — audit_entry_id · tenant_id · sequence_number (per tenant, gapless) · object_type · object_id · action · previous_value · new_value · **changed_by (always a person — never a system, never an agent)** · changed_at · module · **arrival_channel (`screen` / `model_context_protocol`)** · **agent_session_id (set when the action arrived through an agent acting for that person, empty otherwise)** · agent_session_scope · **previous_entry_hash · entry_hash**.

Rules:

- Inserts go through the data-access layer like every other write, stamped with the acting person's tenant.
- **Update and delete on the audit table throw for every caller, with no exception for any role.**
- Each entry carries the hash of the previous entry. A **verification routine** walks the chain over a requested range and reports intact or broken, stating the exact range verified and the true last sequence number — for example *verified entries 50 to 149, last sequence 149*. Reachable from Administration and through the protocol.
- Logged: create · update · delete attempt · approval · rejection · status change · threshold change · system constant change · permission change · hard block attempt · sign-in · data export · configuration change · archive and restore · file erasure.
- **Page views are not logged.** That is surveillance and collides with L4.

**Cryptographic erasure.** Personal data inside a log entry is encrypted with a key specific to that data subject (`encryption_key` table: person_id · key_material (stored encrypted at rest) · created_at · destroyed_at · destroyed_by · authority). On a valid erasure request **the key is destroyed**; the entry, its position and its hash survive; the content becomes permanently unrecoverable; the entry displays *Content removed under data-subject request, [date], [authority].* The chain still verifies. **Erasure is gated** — see section 7, gate 35 — because it is the only irreversible operation in the platform. Legal hold refuses it.

### 4.3 Uniqueness enforced inside the write

The data layer enforces, as refusals: exactly two console holders · exactly one `in_force` revision per controlled document · one site report per project per workday · one toolbox meeting per site report · thirty-one gate rows with no bare gate `25` row and no rows 13 to 17 · six hard block rows and never a seventh · one role per machine name · one `person_role` row current per person per role at a time · one company channel per name.

---

## 5. Identity, roles and access

**The platform stores no password, no credential, no reset flow and no recovery question.** Each tenant configures an identity provider; **the Magnus tenant's identity provider is Google Workspace**, domain-restricted. During the build the builder's hosted sign-in is tolerated (deviation D13, Part 11), but the identity provider remains a property of the tenant, and **the only field anywhere that knows the provider's user identifier is `person.identity_subject`.** Every other table references `person_id`. A person with no role has no access. Access is verified against the provider on each session; **a person whose provider account is disabled moves to `suspended` automatically and immediately, with no administrator action, and the session ends.**

**`person`** — person_id · full_name · display_name · **aliases (text list)** · population (`office`/`field`/`warehouse`/`consultant`) · employment_basis (`employee`/`subcontractor_personnel`/`consultant`) · employer (reference to `party`) · **signs_in (boolean — a statement of fact, not a permission)** · identity_subject (required when `signs_in` is true, empty otherwise) · sign_in_email · home_region (`Luzon`/`Bicol`/`Visayas`/`Mindanao`) · status (`pending`/`active`/`suspended`/`departed`/`archived`) · first_seen · last_seen (accumulated, not entered) · vouched_by (required for subcontractor personnel) · **mobile_number · alternate_number · contact_email (separate from the sign-in address) · photograph_file_id (a `file` record, therefore Google Drive — Part 05) · contact_note (free text: *reach him on the site radio*)**.

- `aliases` is required in practice: the same person appears in existing records under several spellings. A duplicated person breaks deployment, payroll and toolbox reconciliation simultaneously.
- **No person record is ever deleted.**
- **Site crew members do not sign in.** They are named, deployed and paid, and never open the platform: a person who is not a user, not a user with no permissions.
- **A person card** opens from the People list and from any name anywhere — a message author, a task owner, an approver, a site report — showing photograph, numbers, contact email, contact note and current roles. Everyone signed in may see the numbers; viewing is not audited, editing is. An upload control on the card uses the file pipe in Part 05 and sets the pattern every later upload control reuses.

**`role`** — role_id · **role_name (full term, unique)** · **machine_name (unique; this is what gate authority resolves by)** · department · reports_to_role (empty only for Chief Executive Officer) · is_approver (a marker only — it grants nothing) · active. **Roles are deactivated, never deleted**; historical records must still display the role name.

**`person_role`** — person_id · role_id · effective_from · effective_to (empty means current) · assigned_by · **approval_request_id · state (`pending_approval` / `current` / `closed` / `refused`)**. A role change **closes the old row and adds a new one; it never overwrites.** Both may be current during a handover. **A person holds one or more roles, never exactly one.** Permissions are the union of all roles current on the date of the action. **A grant takes effect when its gate 24 request is approved, not when it is raised** — the row exists as `pending_approval` and confers nothing until the decision; a refusal moves it to `refused`. No duplicate current row for the same person and role. Every role-listing query and every permission resolution ignores rows that are not `current`.

**`permission`** — role_id · object_type · action (`view`/`create`/`edit`/`delete_attempt`/`approve`/`export`) · record_scope (`own`/`project`/`department`/`region`/`all`) · money_visibility (`none`/`cost`/`price`/`margin`). **These two axes are independent and are never folded together.** `none` means the person sees the record and sees no monetary value on it anywhere, including exports and printed views. A role with no permission rows sees nothing — never everything.

**`capability_tag`** — person_id · capability (controlled list) · level (`trained`/`competent`/`can_supervise`) · evidence (document reference) · certification_expiry · maintained_by. Capability determines what a person can be assigned; it grants no screen access.

**`console_holder`** — person_id · holder_rank (`primary`/`second`) · granted_by · granted_on. **Exactly two. The platform refuses a third and refuses to remove the second.** Only a current console holder may add or remove a console holder, and a replacement is named before the removal. A console holder has **no access to salary, performance ratings, disciplinary records, medical information, the payroll register, a payslip or a rate table** by virtue of administering permissions.

**Two external gate holders hold authority without an account** — counsel on gate 10 and the sealing Professional Electrical Engineer on gate 18. The internal person carrying the request records the decision, naming the consultant, the date and the document received. The platform never contacts them.

**Assigning a role on screen.** The Assign Role action is available to a department head, Human Resource, and console holders. It raises gate 24; the success message says exactly what happened: *Role assignment requested. Waiting for approval by [primary role name] (alternate [alternate]).* It never says *approval request raised* alone, which reads as failure. When the gate has no primary configured, the action refuses **before the form opens** with *Gate 24 has no approver configured. A console holder must configure it under Administration → Approval gates.*

---

## 6. The six hard blocks — closed list

A hard block stops the transaction. No override, no proceed-anyway, no delegation, no permission level and no console screen releases it. **Every attempt is logged, including every attempt that fails — which is all of them.**

| # | Blocked action | Released only by | Configurable value |
|---|---|---|---|
| 1 | Mobilisation of a project | **The insurance certificate document attached — not a tick-box** | ₱2,000,000 contract value (configuration) |
| 2 | Start of construction | Department of Labor and Employment approved Construction Safety and Health Program recorded (document) | — |
| 3 | Start of the first electrical block | **Block B0 Site Safety Infrastructure reaching state `signed_off`** | — |
| 4 | Mobilisation where permits are required first | Prerequisite permit issued | Which permit types apply |
| 5 | Issue of quarantined material to a site | Quarantine released, or material disposed | — |
| 6 | **Release of funds against a project** | **Signed contract document uploaded** | — |

Hard block 6 blocks **three** actions: the project cannot leave `setup` · no fund release · **no purchase order may be raised.**

**`hard_block`** — block_id (1–6) · block_name · blocked_action · release_condition · configured_value. **Six rows, no delete permission, and deliberately no `active` column.** A boolean that can be set to false is a switch, and no switch may exist.

**`hard_block_attempt`** — block_id · attempted_by · attempted_at · object_reference · release_condition_state.

- **A hard block is evaluated before any gate on the same action.** A blocked action never raises an approval request.
- **The blocked-action message states which block, what specific condition is unmet, what would release it, and who can supply it.** It never says *you do not have permission.*
- **Every hard block is wired to the action it names** — all six, in the module that owns the action (Parts 02, 03). A block that exists as a row and a helper nothing calls is not a block.
- Do not add a seventh, and do not promote a warning to a block.

### 6.1 The five refusals to produce an output — not hard blocks, closed list

Each refuses one output until its own input exists, and clears the moment it does: **1** the payroll register is not produced while any site day in the period has no site report · **2** a payroll period does not close while any acknowledgement sheet is outstanding · **3** a requester with an unliquidated advance cannot raise the next fund request · **4** offboarding cannot complete while any open task, approval or deliverable owned by the departing person is unreassigned · **5** an unclassified document cannot be attached to a work instruction or cited as the governing revision. Everything that is neither a hard block nor one of these five **records and warns.**

---

## 7. The approval gates — data, not code

**Seed thirty-one rows** for thirty gate numbers: gate 25 splits into `25a` and `25b`; gate 34 was added with Operations and Maintenance; **gate 35 (cryptographic erasure) is added by this specification** so the only irreversible operation is gated. `gate_id` is text. The identifier space runs 1 to 35. **Numbers 13 to 17 are permanently reserved and never loaded**, and no bare `25` row exists.

**Every seed row ships with its primary and alternate populated exactly as below.** The first build shipped thirty gates with no approver on any of them, and every approval screen in the product refused for a month. A gate with no primary is a build defect, not a configuration task.

| # | Gate | Trigger | Primary | Alternate | Window (recorded only) |
|---|---|---|---|---|---|
| 1 | Write-off | up to ₱50,000 | Head of Finance | Chief Operating Officer | 3 |
| 2 | Write-off | ₱50,001 to ₱100,000 | Chief Operating Officer | Chief Executive Officer | 3 |
| 3 | Write-off | above ₱100,000 | Chief Executive Officer | none | — |
| 4 | Purchase order | up to ₱100,000 | Procurement Officer | Procurement Head | 2 |
| 5 | Purchase order | above ₱100,000 | Procurement Head | Chief Operating Officer | 3 |
| 6 | Quotation release to client | all — no threshold | Director on the project | Chief Executive Officer | 2 |
| 7 | Quotation below policy markup | more than 5 percentage points below policy | Chief Executive Officer | none | — |
| 8 | Variation order issued to client | all | Director on the project | Chief Executive Officer | 2 |
| 9 | Contract or customer agreement signature (includes service agreements) | all | Chief Executive Officer | none | — |
| 10 | Counsel contract review | every engineering, procurement and construction contract | Atty. Caneja — `primary_person`, no account | Chief Executive Officer accepting the risk on record — not a substitute reviewer | 3 |
| 11 | Progress claim or service charge issued | all | Head of Finance | Chief Operating Officer | 2 |
| 12 | Retention invoice issued | all | Head of Finance | Chief Operating Officer | 5 |
| 18 | Design release for permitting | all | Professional Electrical Engineer seal — `primary_person`, no account | none — statutory professional act | — |
| 19 | Non-Conformance Report closure | all | Project Manager | Chief Operating Officer | 3 |
| 20 | Permit consultant engagement | all — no value threshold | Chief Operating Officer | Chief Executive Officer | 3 |
| 21 | Turnover Document issue to client | all | Project Manager | Chief Operating Officer | 2 |
| 22 | System constant change | all | Chief Executive Officer | none | — |
| 23 | Payroll release | all | Head of Finance | Chief Operating Officer | 1 |
| 24 | New hire, or assignment of a role to a person | all | Department head (Human Resource Head where none) | Chief Operating Officer | 5 |
| 25a | Inter-island warehouse transfer | any value | Procurement Head | Chief Operating Officer | 2 |
| 25b | Within-island transfer | above ₱100,000 | Procurement Head | Chief Operating Officer | 2 |
| 26 | Stock adjustment after count variance | all — zero tolerance | Head of Finance | Chief Operating Officer | 3 |
| 27 | Opening stock balance lock | one-off per warehouse | Cristy, after spot check — `primary_person` | none | — |
| 28 | Permit to work | all | Safety Officer of record | none | — |
| 29 | Safety stop lifted | all | Safety Officer of record | none | — |
| 30 | Incident investigation closure | all | Safety Officer, countersigned by Chief Operating Officer | none | — |
| 31 | Threshold change | all | Domain owner | Chief Executive Officer | — |
| 32 | Change to what a role may do | all | Administration Console holder | Second console holder | — |
| 33 | Document controlled-versus-archive classification, and reclassification | all | Cristy — `primary_person` | none | — |
| 34 | Warranty claim submission | all | Head of Finance | Chief Operating Officer | 3 |
| 35 | Cryptographic erasure of a data subject | all | Primary console holder | Second console holder | — |

**Gate 7 band:** policy markup is 115% major equipment and 130% balance of system (system constants). A Director may quote down to 110% major and 125% balance of system; below that, Chief Executive Officer only.

**`gate`** — gate_id (text) · gate_name · module · object_type · trigger_condition · primary_role (machine name; required unless `primary_person` is set) · primary_person · alternate_role · alternate_person · window_working_days · active.

**`gate_trigger`** — gate_id · trigger_type (`always`/`value_above`/`value_below`/`percentage_below`/`condition`) · threshold_value · threshold_basis (`absolute_peso`/`percentage_of_policy`/`percentage_of_block_budget`) · condition_expression.

**`approval_request`** — request_id · gate_id · object_type · object_id · raised_by · raised_at · current_approver · **original_approver (never changes)** · passed_down_at · state (`awaiting_primary`/`awaiting_alternate`/`approved`/`rejected`/`proceeded_without_review`/`withdrawn`) · decided_by · decided_at · decision_note (required on rejection) · arrival_channel · agent_session_id.

### 7.1 Gate rules

- **R1 · Nothing is ever auto-approved, on any gate, under any condition.**
- **R2 · `window_working_days` is stored and displayed; the platform never acts on it.** Nothing escalates. A request stays with its primary until a human decides or the alternate explicitly takes it.
- **R3 · The alternate must hold equal or greater approval authority than the primary; the platform refuses to save an alternate with a lower limit** — a save-time refusal.
- **R4 · A gate with no alternate never moves. It waits.**
- **R5 · Gates 18, 28, 29 and 30 have no shortcut of any kind** — no alternate, no window, no delegation, and no configuration setting may give them one.
- **R6 · A person may not approve their own request, and may not approve the request that grants them the role under which they would approve.** Where a person's roles make them both requester and approver, the request is offered to the alternate and logged. Two protocol tokens held by one person are one person. Does not apply to gates 10 and 18, where the internal person is the recorder, not the approver.
- **R7 · Approval authority is the highest limit among a person's current roles. Never the sum.**
- **R8 · Rejection requires a note. Approval does not.**
- **R9 · Gate 10 records two outcomes that must not be collapsed:** `approved` (counsel reviewed) and `proceeded_without_review` (Chief Executive Officer accepted the risk on record).
- **R10 · Gates are deactivated, never deleted.**
- **R11 · A module declares which gates apply to it. No module implements approval logic of its own. Build one engine.** Every approval point in every part of this specification calls the engine's `raise`, `approve`, `reject` and `check_authorisation` functions — there is no other path by which a record reaches an approved state. An approval reference stored as a plain string that nothing checks is the defect that made the first build's approvals meaningless.
- **R12 · Windows are measured in working days** using the company working calendar.
- **R13 · Reconfiguring a gate is itself governed.** Changing a gate's limits, primary, alternate or window requires gate 31 (a console holder is the domain owner for gates); a change to gate 32's own row requires both console holders. No signed-in person may reconfigure a gate without that.

### 7.2 Statutory rate changes — dual control, outside the gate sequence

Human Resource enters the rate; Finance approves it. Every rate carries an effective date. An unapproved rate never reaches a payroll run. Both identities and both timestamps enter the audit log.

### 7.3 Compensating controls that are reports, not gates

Queries exposed through the protocol, never computed on a schedule: purchase orders committing 50% or more of a block budget · Director approval turnaround (gate 6) · contracts signed without counsel review (gate 10) · discounting by client, Director and period (gate 7) · new headcount cost against budget (gate 24) · threshold change history (gate 31) · non-conformance ageing and same-day closure rate (gate 19) · quarterly access review (gate 32) · console change history.

### 7.4 What the approver sees

**My Approvals** — one list, every gate, sorted by age, each row showing what, which gate, the value or condition that triggered it, who raised it, how long it has waited and the recorded window. **Approval detail shows the object being approved in full** — the approver must be able to see what they are approving without navigating away. **When a request is raised, the primary approver receives a Task notification in the same transaction** (section 9), and so does the alternate as Information. This is the hand-off the first build omitted at every one of its approval points; nothing waited for anyone because nobody was told.

---

## 8. System constants and configuration

**`system_constant`** — system_constant_id · constant_name · value · unit · effective_from · effective_to · changed_by · changed_on · previous_value · reason (required) · approval_request_id (verified against an approved gate 22 request before the row is written).

Seed five rows with `effective_from` set to the go-live date:

| Constant name | Value | Unit |
|---|---|---|
| Specific Yield | 1,277 | kilowatt-hours per kilowatt-peak per year |
| Area Per Kilowatt Peak | 7 | square metres |
| Lease Reference Rate | 6.70 | Philippine peso per kilowatt-hour, value-added tax inclusive |
| Markup Major Equipment | 115 | percent |
| Markup Balance Of System | 130 | percent |

**A change never overwrites. It inserts a new row with a new effective date and closes the previous row's `effective_to` to the day before.** Work built before a change keeps the value it was built with. **A version whose `effective_from` is after its `effective_to` is refused at write.** The protocol's constant tool calls the same versioning function as the screen; it never patches a value in place.

**`configuration_value`** — configuration_key · value · data_type · changed_by · changed_on · previous_value · reason. Approximately thirty operational thresholds, every controlled list, every interface label, landing screens per role, retention schedules, the push list, `renewal_notice_days`, maintenance plan intervals, the expected transit days per route class, the insurance threshold for hard block 1, the priority limit per requester. Gate 31 applies. **No bulk configuration import** — one change at a time, each with a reason.

### 8.1 Labels as configuration

Every interface label lives in a controlled set so wording is corrected in one place. The full-term rule applies to every label, status value, button, notification, report heading and error message.

### 8.2 Working calendar

**`working_calendar`** — tenant_id · date · is_working_day · description. Seeded with Philippine national holidays for the go-live year; maintained by Human Resource under gate 31. Every window and every working-day count uses it.

### 8.3 The second tenant

Create an invented engineering, procurement and construction company as tenant two in test, with different stages, thresholds, roles and labels, and keep it populated. If the platform cannot run the invented second company, it is Magnus's internal tool with a tenant column, not a product.

---

## 9. Notifications and the personal panel

**`notification`** — notification_id · **recipient (exactly one person)** · category (`task`/`response`/`check`/`information`) · source_module · **object_type · object_id (every notification points at a record)** · headline · raised_at · raised_by · state (`open`/`acknowledged`/`acted`/`superseded`/`escalated`) · acted_at · **cleared_by_event** · requires_acknowledgement · acknowledged_at · escalated_to.

Rules:

- **Exactly one recipient per notification.** A thing requiring three people produces three notifications.
- **Every notification points at a record**, and opening it opens the record.
- **`information` never badges.**
- **A notification clears only when the underlying work is done** — never by reading, opening or dismissing it. `cleared_by_event` records what cleared it.
- **Badges are computed on read from the underlying records. Never store a running total.**
- **No role sees another person's notification panel** — not a manager, not a console holder.
- Notifications are written by people acting in the platform, by same-transaction derivation, and by agents through the protocol. Nothing generates one on a timer.
- **Every hand-off in every later part raises a notification in the same transaction as the action that creates the hand-off** — an approval request to its approver, a task to its owner, a discrepancy to both custodians, a block on a person to that person, a work order to its assignee. A record sitting in a queue that nobody was told about is the single defect that made the first build slow everywhere.

**Two things exist, look similar, and must not share a line of code:**

| | Personal notification panel | Executive exception view (Part 08) |
|---|---|---|
| Question | What is waiting for me? | What is wrong in the business? |
| Completeness | Complete — nothing ranked away, capped or summarised | Ranked and capped by the agent that reads it |
| Ordering | Chronological within category | Agent's judgement |
| Cleared by | The underlying work being done | Never cleared |

If a person has forty items addressed to them, they see forty.

**Landing screen per role**, configurable, defaulting to: Person In Charge → Today · Project Manager → My Projects · Director → My Projects · Chief Executive Officer → Executive view · Head of Finance → Approvals and cash · Procurement → Buying checklist · Safety Officer → Today · Warehouse custodian → Warehouse · Human Resource → People. Each shows, in this order: what is overdue · what is due today · what is blocked and waiting on someone else · what is coming.

---

## 10. Navigation, search, deep links, badges and theme

**Sidebar — build the full sidebar on day one, in this exact order, with a placeholder for every module not yet built:** Dashboard · My Day · Pipeline · Projects · Design and Engineering · Procurement · Permits · Inventory · Manpower and Equipment · Safety · Operations and Maintenance · Documents · Messages · Finance · Human Resource · Payroll · Reports · Administration. Eighteen items. *Migration and Cutover* may sit last until the cutover date, then is hidden. There is no *Site Reporting* item and no separate *Tasks* or *Construction* item — site reports and blocks live under Projects; tasks live in My Day. No ampersand.

**Two live counts on the sidebar and the dashboard, both computed on read:**

- **Messages (X)** — X = the person's unread conversations total across Direct, Spaces and Company channels (Part 05). This is a display state, not a notification.
- **Task (X)** — X = tasks owned by the person whose state is not `done`, `graded` or cancelled. It does not change until a task is delivered or cancelled; an overdue task keeps counting.

**Global search** on one box on every screen, covering projects, blocks, people (by name, alias and nickname), documents, purchase orders, materials, permits, messages and tasks. **Scoped by permission — a result a person may not open does not appear at all.**

**Every record has a permanent addressable deep link.** A deep link followed without permission shows a courteous refusal naming who can grant access, and no record content.

**Theme control** in the top bar, immediately left of the notification bell: one icon button opening a menu of three themes with the current one marked — **Bright**, **Dark**, **Magnus Green and Orange**. Stored per browser; no database field. The Magnus theme uses cool green surfaces and Magnus orange for accent and focus; every text-on-background pairing must measure 4.5:1 or better, and text on the orange accent is dark, not white. Every screen is checked under all three themes.

---

## 11. Foundation screens

- Sign-in (identity provider redirect only) · notification inbox (complete, unranked, uncapped, four categories) · global search · My Approvals and approval detail · Today (Person In Charge landing) · My Day (tasks).
- **Administration:** tenant · system constants with effective dates, history and reasons · configuration values · thresholds by domain · approval gates (every row showing primary and alternate; save refused under R3; reconfiguration under R13) · **hard block rows, read-only with values editable and no enable, disable, delete or bypass control** · roles and permissions (gate 32) · console holders · access review · labels · push list with the three shown as non-removable · working calendar · change log with arrival channel · **audit chain verification with the true last sequence** · read-only audit log view · agent sessions (Part 09) · Integrations (Part 05) · Migration and Cutover (Part 10).

---

## 12. Checks before Part 02 starts — paste the evidence, not a sentence

1. Search output showing no automation, scheduled function, trigger or workflow exists in the application.
2. Search output showing no governed entity is written from the client; the entity rules deny it.
3. The gate table holds thirty-one rows; no row 13 to 17; no bare 25; every row has a primary; `select gate_id, primary_role, primary_person, alternate_role` pasted in full.
4. The hard block table holds six rows and has no `active` column; the console shows no enable, disable or delete control.
5. Attempt a third console holder and removal of the second — both refused.
6. Attempt to update and to delete an audit entry from a backend function — both throw. Edit one through the builder's data console — verification reports a broken chain and the true last sequence.
7. Erase a test data subject under gate 35 — content unrecoverable, chain verifies.
8. Change a system constant under gate 22 — a new row, previous row closed, effective dates ordered; attempt a version with `effective_from` after `effective_to` — refused.
9. Assign a role — the `person_role` row is `pending_approval`, confers nothing, and the primary approver holds a Task notification; approve — `current`; refuse — `refused`.
10. The full eighteen-item sidebar exists in order with placeholders; Messages (X) and Task (X) render.
11. Tenant two exists with different thresholds, roles and labels; a person of tenant two cannot read or write any tenant-one record by identifier.
12. Acceptance tests 1, 2, 5, 6, 7, 9, 10, 16, 22 and 168 from Part 12 pass, with output pasted.
