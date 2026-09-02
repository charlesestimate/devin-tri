Build a multi-tenant operations platform for Magnus Renewable Tech Corp, a solar engineering, procurement and construction company in the Philippines running approximately fifty megawatt-peak of commercial and industrial projects with about sixty people across offices, project sites and three regional warehouses in Laguna, Sorsogon and Dumaguete.

You choose the technology stack, the framework, the user interface library and the hosting. Two requirements in section 2 name a layer rather than a product, and those two are not negotiable.

Read this entire instruction before writing any code. Where this instruction states a rule, implement the rule exactly and do not substitute a simpler equivalent. Where this instruction is silent, ask rather than decide. An invented decision that looks reasonable is the most expensive defect this project can produce, precisely because nobody will notice it.

---

# 1. THE GOVERNING PRINCIPLE OF THIS BUILD

This platform is a record, a permission boundary, and a Model Context Protocol server. **It has no intelligence of its own and it performs no unattended action.**

All monitoring, chasing, ranking, escalating, summarising, forecasting, reporting and analysis is performed by external artificial intelligence agents connecting through the Model Context Protocol server in section 12. The platform's job is to hold correct data, refuse the transactions it must refuse, and expose everything it knows to an authenticated agent.

**Build no scheduler, no cron job, no background worker, no queue processor, no timer, no polling loop, no rules engine, no workflow engine, no notification engine, no ranking algorithm and no digest.** There is no exception to this paragraph. The complete list of what must not be built is section 15.

Four kinds of computation are permitted, because they are arithmetic evaluated at the moment a person or an agent asks, not background activity:

1. **Derived values computed on read** — percentage complete, material readiness, badge counts, resource availability, accumulated medians, project stage.
2. **Hard block and gate evaluation** — computed at the instant a transaction is attempted.
3. **Permission resolution** — computed at the instant a request is served.
4. **Same-transaction derivation** — a value computed and stored inside the same database transaction as the human action that caused it, using only fields that action supplied. The turnover date computing three expiry dates is same-transaction derivation. Raising an invoice three years later is not.

If a feature requires something to happen while nobody is looking at the screen, that feature does not belong in this platform. It belongs to an agent.

## 1.1 The one exception, and it is a safety requirement

Three notification categories also send a device push notification with mandatory acknowledgement: **a safety stop or work suspension · an incident or near-miss requiring immediate action · a statutory deadline breached or imminent.** This list is configurable — categories may be added — and **these three can never be removed and their acknowledgement can never be switched off by any administrator.**

This is delivery, not automation: the push fires in the same transaction as the record being created. **Nothing chases an unacknowledged item.** Unacknowledged items are queryable through the Model Context Protocol; an agent escalates them.

---

# 2. THE TWO REQUIREMENTS THAT NAME A LAYER

**Tenant isolation is enforced at the database row level.** Every table carries `tenant_id` from the first migration. Isolation is implemented with database row-level security policies, never with a filter added in application code. A query written without an application-layer filter must return no rows belonging to another tenant. An application filter passes every test until one query is written without it, at which point one organisation sees another's data.

**The audit log is append-only, enforced by database constraints.** The audit table rejects `UPDATE` and `DELETE` at the database level, for every role including the database owner and including you. A log protected only by application code that declines to offer a delete button is not immutable — it is inconvenient.

Everything else is your decision.

---

# 3. THE EIGHT LOCKED PRINCIPLES

Every feature is checked against these.

**L1 · The platform records and warns.** It blocks only where the law requires it, money would be irreversibly committed, or a physical action cannot be undone. There are exactly six hard blocks and the list is closed.

**L2 · Every control ships with its verification.** Wherever the platform captures an assertion it must also capture something capable of contradicting it. The Person In Charge's headcount is meaningless without the toolbox photograph and the variance between them.

**L3 · Capture must have consequence.** The company's dominant historical defect — found thirteen times during design — is records completed correctly and sent somewhere nothing reads them. **If a field is captured and never used, delete the field.**

**L4 · Workload is visible. Presence is never tracked.** No location, no activity, no keystrokes, no login-time metric, no clock — for anybody, at any permission level. This is a legal constraint under Philippine labour law and a commitment made to staff at rollout. **No configuration option may switch it on.**

**L5 · Accumulate, do not maintain.** Reference data is accumulated from what happened, never maintained by hand. Build the accumulation, not the maintenance screen.

**L6 · The audit log is append-only.**

**L7 · Operational data informs the conversation; it never produces the rating.**

**L8 · Safety approvals are never automated.** Permits to work, lifting a safety stop, closing an incident investigation and the Professional Electrical Engineer seal are decided by a qualified person, every time.

---

# 4. TERMINOLOGY — NO ABBREVIATIONS ANYWHERE

Every column name, label, button, status value, notification, report heading and error message uses the full term. An abbreviation may appear in parentheses after the full term on first use in the interface, and never alone.

Write `person_in_charge`, never `pic`. `non_conformance_report`, never `ncr`. `bill_of_materials`, never `bom`. Also spelled in full everywhere: Provisional Acceptance Certificate · Final Acceptance Certificate · Notice to Proceed · Permission to Operate · Operations and Maintenance · Professional Electrical Engineer · Engineering, Procurement and Construction · Battery Energy Storage System · Distribution Utility · Local Government Unit · Construction Safety and Health Program · Department of Labor and Employment · Bureau of Internal Revenue · Social Security System · Magnus Renewable Tech Corp.

*Progress curve* and *S-curve* are both permitted — the S is a shape, not an abbreviation.

Labels live in configuration as a controlled set, so wording is corrected in one place rather than across the codebase. **This rule applies to your commit messages and your questions back to Magnus.**

---

# 5. THE SIX HARD BLOCKS — CLOSED LIST

A hard block stops the transaction. There is no override, no proceed-anyway, no delegation, no permission level and no console screen that releases it. **Every attempt is logged, including every attempt that fails, which is all of them.**

| # | Blocked action | Released only by | Configurable value |
|---|---|---|---|
| 1 | Mobilisation of a project | **The insurance certificate document attached. Not a tick-box** | ₱2,000,000 contract value |
| 2 | Start of construction | Department of Labor and Employment approved Construction Safety and Health Program recorded | — |
| 3 | Start of the first electrical block | **Block B0 Site Safety Infrastructure reaching state `signed_off`** | — |
| 4 | Mobilisation where permits are required first | Prerequisite permit issued | Which permit types apply |
| 5 | Issue of quarantined material to a site | Quarantine released, or material disposed | — |
| 6 | **Release of funds against a project** | **Signed contract document uploaded** | — |

**Hard block 6 blocks three specific actions and the third is the one most likely to be missed:** the project cannot leave `setup`; no fund release; **and no purchase order may be raised.** Blocking payment while allowing purchase orders means Magnus has committed money without a contract and discovers it when payment is due. The block sits on the commitment.

The `hard_block` table has **six rows, no delete permission, and deliberately no `active` column.** A boolean that can be set to false is a switch, and no switch may exist. Do not add one for symmetry with the `gate` table.

**A hard block is evaluated before any gate on the same action.** A blocked action never raises an approval request — do not ask a person to approve something the platform will then refuse.

**The blocked-action message states: which block · what specific condition is unmet · what would release it · and who can supply it.** It must never say "you do not have permission." That is a different fact, it sends the person to the wrong place, and it teaches people that the platform is arbitrary. A hard block message is an instruction, not a refusal.

**Do not add a seventh hard block, and do not promote a warning to a block because it seemed more correct.**

## 5.1 The five refusals to produce an output — not hard blocks, and the list is closed

None of these stops work on a site. Each refuses to produce **one output** until its own input exists, and each clears the moment it does.

| # | Refusal |
|---|---|
| 1 | **The payroll register is not produced while any site day in the period has no site report** |
| 2 | **A payroll period does not close while any acknowledgement sheet is outstanding** |
| 3 | **A requester with an unliquidated advance cannot raise the next fund request** |
| 4 | **Offboarding cannot complete while any open task, approval or deliverable owned by the departing person is unreassigned** |
| 5 | **An unclassified document cannot be attached to a work instruction or cited as the governing revision** |

Anything that is neither a hard block nor one of these five **records and warns.**

---

# 6. THE TWENTY-EIGHT APPROVAL GATES

**Gates are database rows, not code. If a gate value appears in a source file, it is wrong.**

Seed **twenty-nine rows** for twenty-eight gate numbers — gate 25 splits into `25a` and `25b`. `gate_id` is text, not an integer. **Numbers 13 to 17 are permanently reserved and are never loaded**, and no bare `25` row exists. An earlier draft numbered five hard blocks at 13 to 17; that numbering is withdrawn so every gate number already in use still points at the same gate.

| # | Gate | Trigger | Primary | Alternate | Window (recorded only) |
|---|---|---|---|---|---|
| 1 | Write-off | up to ₱50,000 | Head of Finance | Chief Operating Officer | 3 |
| 2 | Write-off | ₱50,001 to ₱100,000 | Chief Operating Officer | Chief Executive Officer | 3 |
| 3 | Write-off | above ₱100,000 | Chief Executive Officer | **none** | — |
| 4 | Purchase order | up to ₱100,000 | Procurement Officer | Procurement Head | 2 |
| 5 | Purchase order | above ₱100,000 | Procurement Head | Chief Operating Officer | 3 |
| 6 | Quotation release to client | **all — no threshold** | Director on the project | Chief Executive Officer | 2 |
| 7 | Quotation below policy markup | more than 5 percentage points below policy | Chief Executive Officer | **none** | — |
| 8 | Variation order issued to client | all | Director on the project | Chief Executive Officer | 2 |
| 9 | Contract signature | all | Chief Executive Officer | **none** | — |
| 10 | Counsel contract review | every engineering, procurement and construction contract | **Atty. Caneja — `primary_person`, holds no platform account** | **Chief Executive Officer accepting the risk on record — not a substitute reviewer** | 3 |
| 11 | Progress claim issued | all | Head of Finance | Chief Operating Officer | 2 |
| 12 | Retention invoice issued | all | Head of Finance | Chief Operating Officer | 5 |
| 18 | Design release for permitting | all | **Professional Electrical Engineer seal — `primary_person`, holds no platform account** | **none — statutory professional act** | — |
| 19 | Non-Conformance Report closure | all | Project Manager | Chief Operating Officer | 3 |
| 20 | Permit consultant engagement | **all — no value threshold** | Chief Operating Officer | Chief Executive Officer | 3 |
| 21 | Turnover Document issue to client | all | Project Manager | Chief Operating Officer | 2 |
| 22 | System constant change | all | Chief Executive Officer | **none** | — |
| 23 | Payroll release | all | Head of Finance | Chief Operating Officer | 1 |
| 24 | New hire, or assignment of a role to a person | all | Department head | Chief Operating Officer | 5 |
| 25a | **Inter-island** warehouse transfer | **any value** | Procurement Head | Chief Operating Officer | 2 |
| 25b | Within-island transfer | above ₱100,000 | Procurement Head | Chief Operating Officer | 2 |
| 26 | Stock adjustment after count variance | **all — zero tolerance** | Head of Finance | Chief Operating Officer | 3 |
| 27 | Opening stock balance lock | one-off per warehouse | **Cristy, after spot check — `primary_person`** | **none** | — |
| 28 | **Permit to work** | all | Safety Officer of record | **none** | — |
| 29 | **Safety stop lifted** | all | Safety Officer of record | **none** | — |
| 30 | **Incident investigation closure** | all | Safety Officer, countersigned by Chief Operating Officer | **none** | — |
| 31 | Threshold change | all | Domain owner | Chief Executive Officer | — |
| 32 | Change to what a role may do | all | Administration Console holder | Second console holder | — |
| 33 | Document controlled-versus-archive classification | all | **Cristy — `primary_person`** | **none** | — |

**Gate 7 band:** policy markup is 115% major equipment and 130% balance of system. A Director may quote down to **110% major** and **125% balance of system**. Below that, Chief Executive Officer only.

## 6.1 Gate rules

**R1 · Nothing is ever auto-approved, on any gate, under any condition.** There is no transition to `approved` that is not caused by a named person deciding.

**R2 · `window_working_days` is stored and displayed. The platform never acts on it.** No timer fires, no authority passes down, nothing escalates by itself. A request stays with its primary until a human decides, or until the alternate explicitly takes it. An agent reading pending approvals through the Model Context Protocol is what chases an overdue approval. *This is a deliberate departure from the source specification — see section 16, deviation D1.*

**R3 · The alternate must hold equal or greater approval authority than the primary. The platform refuses to save an alternate with a lower limit** — a save-time refusal, never a warning. An alternate with a lower limit silently lowers the gate and creates an avoidance route.

**R4 · A gate with no alternate never moves.** It waits. Gates 3, 7, 9, 18, 22, 27, 28, 29, 30 and 33 have no alternate.

**R5 · Gates 18, 28, 29 and 30 have no shortcut of any kind** — no alternate, no window, no delegation, and no configuration setting may give them one. These are statutory and professional acts.

**R6 · A person may not approve their own request.** Where a person's roles make them both requester and approver, the request is offered to the alternate and logged as such. **This does not apply to gates 10 and 18**, where the internal person is recording an external professional's decision rather than making one, and is named as the recorder rather than the approver.

**R7 · Approval authority is the highest limit among a person's current roles. Never the sum.**

**R8 · Rejection requires a note. Approval does not.**

**R9 · Gate 10 records two different outcomes and they must not be collapsed.** `approved` means counsel reviewed it. **`proceeded_without_review` means the Chief Executive Officer accepted the risk on record and Magnus signed without counsel review.** The platform must be able to state at any time exactly which contracts were signed without counsel review. A rising count is a signal about counsel capacity, not about risk appetite.

**R10 · Gates are deactivated, never deleted.** Historical approval requests reference them.

**R11 · A module declares which gates apply to it. No module implements approval logic of its own.** Build one engine. Approval logic implemented eighteen times means the eighteenth will not behave like the first.

**R12 · Windows are measured in working days** using the company working calendar, wherever a window is displayed.

## 6.2 Statutory rate changes — dual control, outside the gate sequence

Not one of the twenty-eight, but it operates identically. **Human Resource enters the rate; Finance approves it.** Every rate carries an effective date. **An unapproved rate change never reaches a payroll run — it sits `pending`.** Both identities and both timestamps enter the audit log.

## 6.3 Compensating controls that are reports, not gates

These are **queries**, exposed through the Model Context Protocol. Nothing computes them on a schedule.

Purchase orders committing 50% or more of a block budget · Director approval turnaround, gate 6 · contracts signed without counsel review, gate 10 · discounting by client, Director and period, gate 7 · new headcount cost against budget, gate 24 · threshold change history, gate 31 · non-conformance ageing and same-day closure rate, gate 19 · quarterly access review, gate 32 · console change history.

---

# 7. IDENTITY, ROLES AND ACCESS

**The platform stores no password, no credential, no reset flow and no recovery question.**

Build it as: **each tenant configures an identity provider, and the Magnus tenant's identity provider is Google Workspace.** Do not build it as: the platform uses Google. The second is simpler, passes every Phase A test, and requires a rebuild the day the first outside tenant arrives.

Access is verified against the provider on each session, never cached indefinitely. **A person whose provider account is disabled moves to `suspended` automatically and immediately, with no administrator action.**

**A person holds one or more roles, never exactly one.** A director also carries deals as an account executive; a regional operations person is also a warehouse custodian. A single-role model fails on the first real person at this company. **Permissions are the union of all roles current on the date of the action.**

**Site crew members do not sign in.** They are named, deployed and paid, and never open the platform. Model them as **a person who is not a user**, not as a user with no permissions. `signs_in` is a statement of fact, not a permission.

**Two external gate holders hold authority without an account** — counsel on gate 10 and the sealing Professional Electrical Engineer on gate 18. The approval is recorded in the platform by the internal person carrying the request, naming the consultant, the date and the document received. **The platform never contacts them.**

---

# 8. THE DATA MODEL

Every table carries `tenant_id` and standard audit columns (`created_at`, `created_by`, `updated_at`, `updated_by`). Field lists are complete for the load-bearing objects and name every field for the rest.

## 8.1 Foundation

**`tenant`** — tenant_id · legal_name · short_name · state (`active`/`suspended`/`closed`) · configuration_profile_id · identity_provider · identity_provider_configuration · created_on · created_by. **Magnus is tenant one. Not tenant zero, and not a default.** A suspended tenant's data is retained and unreadable; nothing is deleted.

**`person`** — person_id · full_name · **aliases (text list)** · photograph · population (`office`/`field`/`warehouse`/`consultant`) · employment_basis (`employee`/`subcontractor_personnel`/`consultant`) · employer (reference to `party`) · signs_in (boolean) · identity_subject (required when `signs_in` is true, empty otherwise) · home_region (`Luzon`/`Bicol`/`Visayas`/`Mindanao`) · status (`pending`/`active`/`suspended`/`departed`/`archived`) · first_seen · last_seen (accumulated, not entered) · vouched_by (required for subcontractor personnel).

`aliases` is required in practice: the same person appears in existing records under several spellings, and without aliases migration creates duplicates — **and a duplicated person breaks deployment, payroll and toolbox attendance reconciliation simultaneously, in ways that look like three unrelated faults.**

**No person record is ever deleted.**

**`role`** — role_id · role_name (full term) · department · reports_to_role (empty only for Chief Executive Officer) · is_approver · active. **Roles are deactivated, never deleted** — historical records reference them and must still display the role name correctly.

**`person_role`** — person_id · role_id · effective_from · effective_to (empty means current) · assigned_by. A role change **closes the old row and adds a new one. It never overwrites.** Both may be current at once during a handover, and that is expected — building role change as replacement makes a handover impossible to represent, and handovers are when things get dropped.

**`permission`** — role_id · object_type · action (`view`/`create`/`edit`/`delete_attempt`/`approve`/`export`) · record_scope · money_visibility.

`record_scope`: `own` · `project` · `department` · `region` · `all`.
`money_visibility`: `none` (sees the record, sees no monetary value on it anywhere including exports and printed views) · `cost` · `price` · `margin`.

**These are independent axes and must never be folded together.** A Person In Charge needs the full material list for their site and must not see its cost. Collapsing the axes forces a choice between hiding work and exposing margin.

**`capability_tag`** — person_id · capability (controlled list) · level (`trained`/`competent`/`can_supervise`) · evidence (document reference) · certification_expiry · maintained_by. **Capability determines what a person can be assigned. It grants no screen access.**

**`console_holder`** — person_id · holder_rank (`primary`/`second`) · granted_by · granted_on. **Exactly two. The platform refuses to save a third and refuses to remove the second.** One holder is a continuity failure; three or more and configuration drifts because nobody knows the current state.

**`gate`** — gate_id (text) · gate_name · module · object_type · trigger_condition · primary_role (required unless `primary_person` is set) · primary_person · alternate_role · alternate_person · window_working_days · active.

**`gate_trigger`** — trigger_type (`always`/`value_above`/`value_below`/`percentage_below`/`condition`) · threshold_value · threshold_basis (`absolute_peso`/`percentage_of_policy`/`percentage_of_block_budget`) · condition_expression.

**`approval_request`** — request_id · gate_id · object_reference (polymorphic) · raised_at · current_approver · **original_approver (never changes)** · passed_down_at · state (`awaiting_primary`/`awaiting_alternate`/`approved`/`rejected`/`proceeded_without_review`/`withdrawn`) · decided_by · decided_at · decision_note (required on rejection) · arrival_channel (`screen`/`model_context_protocol`).

**`hard_block`** — block_id (1–6) · block_name · blocked_action · release_condition · configured_value. **No `active` column.**

**`hard_block_attempt`** — block_id · attempted_by · attempted_at · object_reference · release_condition_state (why it was still blocked).

**`notification`** — notification_id · **recipient (always exactly one person)** · category (`task`/`response`/`check`/`information`) · source_module · **object_reference (every notification points at a record)** · headline · raised_at · state (`open`/`acknowledged`/`acted`/`superseded`/`escalated`) · acted_at · **cleared_by_event** · requires_acknowledgement · acknowledged_at · escalated_to.

**`system_constant`** — system_constant_id · constant_name · value · unit · effective_from · changed_by · changed_on · previous_value · reason (required).

Seed five rows with `effective_from` set to the go-live date:

| Constant name | Value | Unit |
|---|---|---|
| Specific Yield | 1,277 | kilowatt-hours per kilowatt-peak per year |
| Area Per Kilowatt Peak | 7 | square metres |
| Lease Reference Rate | 6.70 | Philippine peso per kilowatt-hour, value-added tax inclusive |
| Markup Major Equipment | 115 | percent |
| Markup Balance Of System | 130 | percent |

**A change never overwrites. It inserts a new row with a new effective date.** Work built before a change keeps the value it was built with; new work uses the new value. Gate 22 applies, primary Chief Executive Officer, no alternate. This exists because a yield constant moved from 1,400 to 1,277 and nothing recorded which models used which value, leaving roughly ₱3.6 million a year of projection difference to be restated by hand.

**`configuration_value`** — configuration_key · value · data_type · changed_by · changed_on · previous_value · reason. Approximately thirty operational thresholds, every controlled list, every interface label, landing screens per role, retention schedules, the push list. Gate 31 applies.

**No Magnus-specific literal appears anywhere in the source code.** Not ₱2,000,000, not ₱100,000, not 1,277, not 7 square metres per kilowatt-peak, not ₱6.70, not any label or brand name. All of it is configuration.

**`audit_entry`** — audit_entry_id · tenant_id · object_type · object_id · action · previous_value · new_value · changed_by · changed_at · module · arrival_channel · **previous_entry_hash · entry_hash**.

Logged: create · update · delete attempt · approval · rejection · status change · threshold change · system constant change · permission change · **hard block attempt** · sign-in · data export.

**Page views are NOT logged.** That is surveillance of people, it collides with L4, and it would be the most convincing possible evidence that the platform is a monitoring instrument whatever anyone says about it.

Provide a **verification routine that walks the hash chain and reports intact or broken**, reachable from the administration screen and through the Model Context Protocol.

**Cryptographic erasure.** The Philippine Data Privacy Act gives a data subject the right to erasure; an append-only log cannot delete. Resolve this in the architecture in the first release — it cannot be retrofitted. Personal data inside a log entry is encrypted with a key specific to that data subject. On a valid erasure request **the key is destroyed.** The entry, its position and its hash survive; the content becomes permanently unrecoverable; the entry displays `Content removed under data-subject request, [date], [authority].` The chain still verifies.

## 8.2 Navigation and notification (module 3)

**Two things exist, they look similar, and they must not share a single line of code.**

| | Personal notification panel | Executive exception view |
|---|---|---|
| Question | What is waiting for me? | What is wrong in the business? |
| Scope | Personal | Company-wide |
| Completeness | **Complete. Nothing ranked away, capped, collapsed or summarised** | Ranked and capped by the agent that reads it |
| Ordering | Chronological within category | Agent's judgement |
| Cleared by | **The underlying work being done** | Never cleared |

A shared component will eventually inherit ranking into the personal panel, because ranking looks obviously useful and a long list looks like a problem to solve. **It is not a problem. If a person has forty items addressed to them, they see forty.**

**Notification rules:**

- **Exactly one recipient per notification.** Group and role-addressed notifications do not exist. A thing requiring three people produces three notifications, each clearing independently. Shared notifications are ignored by all recipients, each assuming another has it.
- **Every notification points at a record.**
- **`information` never badges.** A badge is a claim that something requires the person; if information badges, the badge becomes a count of things to dismiss and people stop reading the number. Information is visible in the panel and never counted.
- **A notification clears only when the underlying work is done, never by reading, opening, or dismissing it.** `cleared_by_event` records what actually cleared it. If a person can clear a badge by looking at it, the badge counts attention rather than work.
- **Badges are computed on read from the underlying records. Never store a running total.** A stored counter drifts, and a drifted badge is worse than no badge because the person opens the panel, finds nothing, and learns to ignore it.
- **No role sees another person's notification panel** — not a manager, not a director, not a console holder. A person's panel is a live record of what they have not yet done, and making it visible to a manager converts it into a productivity monitor. Managers see workload through module 13, which shows the work rather than the person's inbox.
- **Notifications are written by people acting in the platform, by same-transaction derivation, and by agents through the Model Context Protocol. Nothing generates a notification on a timer.**

**Landing screen per role**, configurable, defaulting to: Person In Charge → Today · Project Manager → My Projects · Director → My Projects · Chief Executive Officer → Executive view · Head of Finance → Approvals and cash · Procurement → Buying checklist · Safety Officer → Today · Warehouse custodian → Warehouse · Human Resource → People. Each shows, in this order: **what is overdue · what is due today · what is blocked and waiting on someone else · what is coming.** A landing screen that opens on a list of everything is not a landing screen — it is the person's own filing cabinet, and it puts the work of deciding what matters onto them every morning.

**Global search** on one box present on every screen, covering projects, blocks, people, documents, purchase orders, materials, permits, messages and tasks. **Scoped by permission — a result a person may not open does not appear at all**, rather than appearing and then being refused, which confirms the existence of records they have no right to know about.

**Every record has a permanent addressable deep link** — a project, a block, a document revision, a purchase order line, a message. This is what makes a conversation about work resolvable; without it people re-describe records to each other inside the platform exactly as they did in the group chat, and the platform has changed the venue rather than the problem. A deep link followed without permission shows a courteous refusal naming who can grant access, and no record content.

## 8.3 Pipeline — Customer Relationship Management (module 4)

**`account`** — account_id · account_name · industry · active.

**`site`** — site_id · account_id · address · **region (derived from province, never typed)** · **local_government_unit** · distribution_utility · host_party.

**Account, site and contact are three objects, not one. Collapsing site into account is the single most common modelling error in this domain and it is expensive.** A client with eleven branches is one account and eleven sites, each with its own assessment, local government unit, distribution utility and permit history. Modelled as one, the accumulated permit-duration learning is attributed to the wrong place and becomes useless.

**`contact`** — contact_id · full_name · account_id · position · electronic_mail_address · telephone_number. A contact may serve several accounts over time.

**`opportunity`** — opportunity_id · account_id · site_id · owner · stage (`qualified`/`site_assessed`/`proposal_issued`/`negotiation`/`won`/`lost`) · estimated_capacity_kilowatt_peak · estimated_value · model (`sale`/`lease`/`power_purchase`) · expected_decision_date · loss_reason.

**Loss reasons:** price · timeline · technical · relationship or incumbent · **client did not proceed at all** · financing. **Reason required above ₱10,000,000.** *Client did not proceed* is recorded and reported separately from *lost to a competitor* — a market where half the losses never proceeded is a sales-cycle problem; half lost to competitors is a pricing problem, and they call for opposite responses.

**`site_assessment`** — site_assessment_id · site_id · roof_type · roof_condition · usable_area_square_metres · obstructions · structural_opinion · **structural_confidence (`high`/`medium`/`low`, required)** · tapping_point_voltage · tapping_point_phase · tapping_point_spare_capacity · consumption_profile · photographs (in-app capture only) · assessed_by · assessed_on.

Collected once, on site, and consumed by design without re-collection. **Every field not captured here is a second site visit** — on a Sorsogon or Dumaguete site that is a day and a flight, not an hour. `structural_confidence` earns its own field because a low-confidence assessment that later fails structural certification becomes a reinforcement variation order, and **a pattern of low-confidence assessments becoming reinforcement variations is a pricing signal. Recorded after the fact, everyone remembers being confident.**

**`proposal`** — proposal_id · opportunity_id · version · capacity_kilowatt_peak · markup_major_applied · markup_balance_of_system_applied · **contingency_percentage** · system_constant_versions_used · state (`draft`/`awaiting_approval`/`issued`/`superseded`/`won`/`lost`) · **frozen_at**.

The proposal is **structured on the same block spine as construction**, which is what allows it to become block value weights without re-costing. A quotation structured any other way must be taken apart and rebuilt after the contract is signed, and the two versions then disagree.

**`contingency_percentage` is internal and appears on no client-facing output** — not the proposal document, not an export, not a printed view. It accumulates per client, answering a question Magnus cannot currently ask: which clients consistently require contingency, and does the work eventually consume it.

**When an opportunity is won the winning proposal version becomes immutable.** It is what the contract was priced against, and every later margin question is answered against it or not answered at all.

**On `won`:** the winning proposal freezes · a project is created in `setup` · the site assessment carries to the design package · the proposal's block structure seeds the project blocks · **the project cannot become `active` until the signed contract is uploaded — hard block 6.** Sales winning is not Magnus being committed; nothing spends money until the contract exists.

**A proposal is a commercial judgement. The platform structures it; a person prices it.**

## 8.4 Project and contract (module 5)

**Magnus signs on client paper. There is no Magnus standard contract and the terms differ every time.** The platform cannot assume any clause exists, cannot default any term, and cannot infer retention, liquidated damages, payment terms or insurance obligations from a template, because there is no template. **Do not build a contract template engine. Build a record of what this particular contract says.**

**`party`** — party_id · **legal_name (the name on the contract, not the trading name)** · **party_type — multi-valued: `client`/`asset_owner`/`offtaker`/`subcontractor`/`supplier`/`consultant`/`other`** · taxpayer_identification_number (required where invoiced or paid) · address · contacts · **is_related_party** · accreditation_state (`accredited`/`provisional`/`suspended` — subcontractors and suppliers) · insurance_certificate_id · insurance_expiry · **insurance_exclusions (a field, not an attachment nobody reads)** · bank_account_details · categories_supplied · currency.

**One record for every organisation.** A subcontractor is a party, not a separate object; so is a supplier. The alternative — a subcontractor record beside a supplier record beside a client record — produces three places where the same company's insurance expiry is recorded and two of them are wrong. *This merges the separate `supplier` object in the source specification; see section 16, deviation D9.*

**Supplier bank details are change-controlled.** A change is logged with before and after values, **requires confirmation by a second named person**, and **the next payment to that party after a bank change is flagged.** Nothing is blocked; it is made visible. This is the single most exploited weakness in construction procurement worldwide: an email arrives saying the account has changed, someone updates the record, and the next payment goes to a stranger — invisible because it looks exactly like maintenance.

**Several subcontractor policies exclude injury to contractors' workmen**, which is precisely the risk the certificate appears to cover. **A certificate on file with an unread exclusion is worse than no certificate, because it produces confidence.**

**`project`** — project_id · project_name · client (reference to `party`) · site_address · **region (derived from province)** · local_government_unit · capacity_kilowatt_peak · contract_value · project_manager · **director (approver on gates 6 and 8)** · permit_dependency · expected_permit_duration_days · contract_id (empty until uploaded — **this emptiness is what blocks**) · status (`setup`/`active`/`suspended`/`turned_over`/`closed`/`cancelled`) · **planned_percentage_curve (a list of date and planned-percentage pairs, entered once from the contract programme — there is no scheduling engine)** · turnover_date · generation_monitoring_source · generation_monitoring_access.

**Project status transitions:** `setup` → `active` requires the signed contract document (hard block 6) · `active` → `suspended` is recorded with a reason and the party responsible · `suspended` → `active` · `active` → `turned_over` on the Turnover Document, gate 21 · `turned_over` → `closed` requires **both** retention released **and** defects liability expired · any → `cancelled` by a Director, with open commitments listed and resolved first.

**There is no stored `phase` field and no project phase badge.** A single project routinely has design complete on some blocks, procurement running on others and construction under way on a third set. **Stage is computed on read from block states and displayed as a distribution, never a single word.** It is the first thing that looks missing and the first thing that becomes wrong.

**`contract`** — contract_id · project_id · **signed_document (the signed copy — not a tick-box, not a draft, not an unsigned final)** · contract_value · currency · date_signed · client_signatory · payment_terms_days · retention_percentage · retention_reference_date_basis · retention_release_months · **counsel_review_state (`reviewed`/`proceeded_without_review`/`pending`)** · related_party · superseded_by.

**Retention terms are read out of the document by a person and entered. Nothing is defaulted or inferred.** Retention is time-based and Magnus must send the bill — it is not released by a certificate, an acceptance event or a client action. **It is the most forgettable receivable in this business**, becoming billable long after everyone has stopped thinking about the project.

**`risk_term`** — contract_id · clause_family · **present (`present`/`absent`/`not_yet_read`)** · summary · exposure_flag · read_by · read_at.

**Eight clause families, all eight rows created on every contract, all defaulting to `not_yet_read`:** liquidated damages and delay · payment terms and milestones · retention · insurance obligations placed on Magnus · warranty and defects liability · variation and change procedure · termination and suspension · limitation of liability and indemnity.

**`not_yet_read` must be distinguishable from `absent`.** *We have not read the termination clause* and *this contract has no termination clause* are different facts with different consequences, and collapsing them produces confident wrong answers about Magnus's exposure across the portfolio.

**`project_party`** — project_id · party_id · role. Eight roles: client · host · asset owner · offtaker · financier · engineering, procurement and construction contractor · operations and maintenance provider · landlord. **One party may hold several roles; one role may be held by several parties.** On a straightforward sale the client holds four. **Do not model party as a single field on the project.**

**`variation_order`** — variation_order_id · contract_id · reference · description · value_change (may be negative) · capacity_change_kilowatt_peak · time_change_days · **blocks_affected (required)** · state (`draft`/`issued`/`accepted`/`rejected`) · raised_by · raised_on · approved_by · approved_on (gate 8, required in `issued`) · client_accepted_on · supporting_document_id.

**A variation order never overwrites the contract.** Only `accepted` re-bases block value weights and moves the contract value; `issued` and `rejected` change nothing. **A variation order that is never accepted is the most common way scope is given away** — it is visible as an ageing `issued` record.

**At contract signature the platform creates, in the same transaction:** the eight `risk_term` rows at `not_yet_read` · the retention schedule dates computed from the three retention fields · the permit dependency flag as entered at contract review. **The billing schedule, deliverable tasks and client obligations are entered by a person or generated by an agent** — *see section 16, deviation D4.*

**Deliverable tasks and client obligations are two separate lists, deliberately.** Client obligations are the half nobody records and the half that produces disputes. A project delayed because the client did not provide roof access is a client delay **only if the obligation and its date were recorded when the contract was signed.** Recorded afterwards, it is an argument.

**The permit dependency flag is set at contract review, never discovered later.** A permit-required project is not delayed by weeks — it is delayed by a quarter or more before a single crew mobilises. That is a commercial fact belonging in the quotation and the programme, not in the schedule log.

**The turnover date is entered once and, in the same transaction, sets three stored dates:** retention becomes billable · warranty and defects liability expiry · operations and maintenance obligation expiry. **Nothing is separately keyed, so nothing can be separately wrong.**

**Related-party contracts** are flagged, reported separately, and their documentation requirements are stricter — Magnus Energy Corp is the current case. **The platform flags; it does not compute the tax position.**

**Portfolio views:** all active projects company-wide (count, capacity, contract value, aggregate progress) · my projects · by region · by stage distribution · by client · related party. Every view respects `record_scope` and `money_visibility`, **with one deliberate exception: the all-active portfolio total returns every active project regardless of the viewer's assignments, because a company total filtered by assignment is not a company total.** `money_visibility` still applies in full — a viewer without it sees count, capacity and progress and no value. **This is the only record view in the platform that crosses `record_scope`.**

## 8.5 Design and engineering (module 6)

**`design_package`** — design_package_id · project_id · **site_assessment_id (the design opens with the assessment data already present — a second site visit to gather it is a defect)** · revision · design_capacity_kilowatt_peak · mounting_type (`rooftop_ballasted`/`rooftop_penetrating`/`ground_mount`/`carport`/`mixed`) · state (`in_progress`/`internal_complete`/`with_sealing_engineer`/`sealed`/`superseded`) · sealed_by · sealed_at · superseded_by.

**`design_deliverable`** — deliverable_id · design_package_id · **block_id (required on the three deliverables produced per block: the single line diagram, the layout and the bill of materials — this is what lets one block's design be complete before the package is, which is what releases that block's procurement)** · deliverable_type · owner · state (`not_started`/`in_progress`/`waiting`/`complete`) · **waiting_on (`magnus`/`sealing_engineer`/`client`)** · **waiting_since** · document_revision_id.

**Nine deliverables per package:** Photovoltaic layout plan · Single Line Diagram · Electrical plans · Structural plans and mounting details · Structural Assessment Certification · Equipment datasheets and specifications · Earthing and lightning protection design · Cable schedule and electrical load schedule · **Bill of materials**.

**`waiting` always carries both `waiting_on` and `waiting_since`. There is no anonymous waiting.** `waiting_since` resets on every transition; cumulative days by party accumulate per project. **This split is the difference between a design that is late and a project being delayed by someone else** — with it, the platform can state with dates how many days a project waited on the client, which is exactly the evidence a delay claim requires and exactly what nobody has six months later. Thresholds: sealing engineer 3 days, client 7 days.

**`bill_of_materials_line`** — line_id · design_package_id · **block_id (required)** · item_description · specification · quantity · unit_of_measure · is_serialised · unit_cost *(design writes all of the above)* · **expected_arrival_date · purchase_status · purchase_order_reference · quantity_received** *(procurement writes these four)*.

**This is one object with two views. Design owns its content; procurement owns its purchasing status. There is no second procurement list.** If procurement is given its own list populated from the bill of materials, the two diverge within one project — a design revision changes a quantity, procurement's copy still says the old number, and **nobody discovers it until a crew is on site and the material is short.** The divergence is silent and it is guaranteed.

**Every line carries a block.** This makes three things possible: material readiness per block · cost per block, which block value weights are computed from · the five percent committed cost overrun flag, measured against a **block** budget. A line with no block breaks all three.

**`professional_seal`** — design_package_id · **revision_sealed (the seal attaches to a revision, not a package)** · engineer · licence_number · licence_valid_to · professional_tax_receipt_number · professional_tax_receipt_year · sealed_at · turnaround_days.

**Review and seal are one act by one external consultant, tracked as one step** — correct precisely because the sealing engineer is external, so the seal is a genuine independent check rather than a professional formality on the sealer's own drawing. **Record the turnaround: the external sealing engineer sits on the permitting critical path.**

**Licence and Professional Tax Receipt validity are checked at the seal date and re-checked retrospectively.** If a licence is later found to have lapsed before a seal date, **every design sealed in that window is flagged.** A design sealed under a lapsed licence is a permit application built on an invalid professional act, discovered — if at all — by the local government unit rather than by Magnus.

**The Structural Assessment Certification has three outcomes and two are commercial events:** pass, design proceeds · **reinforcement required — this raises a variation order under gate 8, never a task.** It is additional scope with a cost the client either accepts or does not; recorded as a task, the work gets done and the money is never asked for, which is capture without consequence at the most expensive possible point · fail, design cannot proceed on this structure, escalates to Director immediately with no threshold.

**Design revision after construction has started is normal, not an error.** A bill of materials line already `ordered` **must never be silently edited by a design revision.** The material is bought. The platform flags the conflict and requires a person to decide: keep, return, or absorb. Silently changing an ordered line produces a warehouse holding something no document says was ever bought. **A sealed revision that is superseded requires its own seal; the old seal does not carry forward.**

**Block value weights** are computed from block cost — materials **and** labour — as block cost ÷ total block cost, **excluding General Requirements**, and lock when the bill of materials is costed. **Design capacity may differ from contract capacity: record both, reconcile neither.**

## 8.6 Procurement (module 7)

**Procurement has no list of its own.** It writes four fields onto rows design created. `purchase_status`: `to_buy` · `requisitioned` · `ordered` · `in_transit` · `partially_received` · `received` · `cancelled`. **`expected_arrival_date` is required from the moment status becomes `ordered`.** The default view is grouped by block, showing what to buy, quantity, specification, status and expected arrival.

**There is no separate requisition object and no request-for-quotation object.** A requisition is a state of a bill-of-materials line. Supplier quotations are attachments against the purchase order; the comparison is a view over those attachments and the party register, **not a record of its own**, and no bid scoring exists — a person decides.

**`purchase_order`** — purchase_order_id · project_id (**blocked where the project has no contract — hard block 6**) · party_id · currency · exchange_rate_applied · exchange_rate_date · total_value · state (`draft`/`awaiting_approval`/`approved`/`issued`/`partially_received`/`received`/`cancelled`) · expected_arrival_date.

**`purchase_order_line`** — purchase_order_id · **bill_of_materials_line_id (empty only for an off-design purchase)** · **off_design_reason (required where the above is empty)** · off_design_block_id · quantity_ordered · unit_price · quantity_received.

**`goods_receipt`** — receipt_id · purchase_order_id · received_at_location · received_by · **received_on_device · received_by_server** · photographs (in-app capture only) · condition (`accepted`/`damaged`/`wrong_item`/`short`).

**Committed cost begins at `issued`, not at payment.** The moment a purchase order is issued Magnus has committed the money. The five percent overrun flag is measured against **committed cost, not spend** — that is the whole point: it catches the overrun while purchase orders can still be amended, rather than when the invoice arrives and nothing can be done.

**Material readiness per block, computed on read:** `ready` — every line for this block is `received` · `partially_ready` — some received, some outstanding · **`not_ready` — this block is not startable.** Each not-ready block carries **the latest `expected_arrival_date` among its outstanding lines**, so it is visible before mobilisation rather than discovered on site. *Blocked, waiting on material* is a complaint. *Blocked, material arriving on the fourteenth* is a plan. **A crew mobilised to a block whose material has not arrived is a wasted day, a wasted trip, and on an inter-island project a wasted week.**

**A partial delivery does not close the line.** `quantity_received` accumulates; the outstanding balance keeps its own expected arrival date, which the supplier must supply and which may differ from the original. A block containing any partially received line is `partially_ready`, never `ready`.

**There is no approval point above the Procurement Head at any value.** This is deliberate: major equipment is already committed at contract signature under gate 9 and by the costed bill of materials, so a purchase order **executes a decision rather than making one.** The compensating control is a query, not a gate: **a purchase order committing fifty percent or more of its block's budget is reported without requiring approval.** No friction is added; an order of unusual size becomes visible the day it is raised. *Watch item: on blocks dominated by a single item — panels, inverters — one order routinely is most of the block, so this may fire on every project for those blocks and never for any other. If that happens the threshold is doing nothing useful and should be revisited.*

**Off-design purchases are real, legitimate and must be possible** — a consumable runs out, a fitting is wrong, something breaks. They are recorded with a **required reason and a block attribution**, and never solved by procurement adding a line to the design. They are the honest measure of how good the design's bill of materials is, and **a rising off-design rate is an estimating problem, not a procurement problem.**

**The five percent overrun query must state which of two things it is:** same items at a higher price (a market condition) or **additional items not in the bill of materials (a scope or estimating problem)**. They need different responses and must not arrive looking identical. At five percent this will fire on ordinary supplier price movement as well as on genuine overruns, and **if every flag looks the same the list is ignored within a quarter.**

**Foreign currency:** the actual rate and its date are recorded on every foreign-currency transaction; project cost carries the rate at time of purchase; **the difference against the quotation rate appears as a foreign exchange variance on the project, not inside the margin.** A project's reported margin must reflect the work, not the currency.

**Supplier performance is accumulated, never scored by hand. Do not build a screen where someone rates a supplier out of five** — it will be filled in once, by one person, from memory, and be wrong within a quarter. **The delivery record already contains the truth:** on-time delivery rate, damage and wrong-item rate, fill rate, price movement by item, and actual lead time, all derived.

**A receipt marked `damaged`, `wrong_item` or `short` quarantines the material in the same transaction. Hard block 5 then prevents its issue.** *The Non-Conformance Report is raised by a person or an agent, not automatically — section 16, deviation D5.*

## 8.7 Blocks and site reporting (module 8)

**The site reports on the blocks. There is no separate site reporting module.** A daily site report is not a diary — it is the mechanism by which block progress is recorded, and **it is also the document on which people are paid.** Without every activity belonging to a block, the report is a narrative and the progress curve is a guess.

**The block spine is fixed for every tenant and is not configurable by anybody**, including a console holder, not per project, not per tenant. **Standardisation is the product**: if every company reshapes the spine, no two projects can be compared and there is no common language between Magnus and its subcontractors. A subcontractor mandated onto this platform is being given Magnus's way of working — that is the point of mandating it, and a configurable spine gives it away. What varies per project is which blocks are *included*, not what the blocks are.

| Code | Name |
|---|---|
| B0 | Site Safety Infrastructure — catwalks, walkways, lifelines |
| B1 | Array — mounting structure and modules |
| B2 | Direct Current Cabling |
| B3 | Inverter |
| B4 | Inverter To Panel Board |
| B5 | Panel Board |
| B6 | Panel Board To Tapping Point |
| B7 | Tapping Point |
| B8 | Transformer — *conditional, include flag* |
| B9 | Network And Monitoring |
| B10 | Miscellaneous |
| B11 | Civil — *optional and parallel on rooftop; mandatory and gates B1 on ground-mount* |
| General Requirements | Permits, documentation, overhead — **carries no value weight** |
| Battery Energy Storage System | *Conditional, include flag* |

**`project_block`** — project_block_id · project_id · block_code · included · **value_weight (locked when the bill of materials is costed)** · state (`not_started`/`blocked_material`/`in_progress`/`complete`/`signed_off`) · material_readiness (derived, not stored) · percent_complete (derived, not stored).

**Structural dependencies, which a project manager may add to but may never remove:** B0 gates B1 (hard block 3) · an approved Construction Safety and Health Program gates B0 (hard block 2) · B5 and B6 together gate B7 · on ground-mount only, B11 gates B1 · a block's design completeness releases that block's procurement · bill of materials line closure gates that block's construction.

**Mounting type determines B1's material and audit fields.** Rooftop: rails, L-feet and clamps on existing structure; audit fields slope, roof type, structural integrity, area. Ground-mount: piles or foundations, posts, then rails and clamps; audit fields topography, soil bearing, drainage, access.

**`site_report`** — site_report_id · project_id · **workday_number (sequential per project, seeded at migration)** · report_date · **person_in_charge (accountable for this report)** · weather (controlled list) · **work_stopped_by_weather** · look_ahead · **working_hours_start · working_hours_end (site-level, recorded once — not attendance, not a clock)** · created_on_device · received_by_server · state (`draft`/`submitted`/`verified`).

**No per-person start time, end time, duration or location exists anywhere in this platform.**

**`created_on_device` determines which workday a report belongs to, never `received_by_server`.** A report written on Monday and synchronised on Thursday is Monday's report. Without this, every cycle-time figure the platform produces is wrong and every same-day capture requirement is unauditable.

**Tomorrow's report is pre-populated from today's incomplete activities and today's `look_ahead`.** The Person In Charge confirms or amends rather than re-typing. This is a form default computed when the form opens, not a scheduled job — **and it is what makes daily reporting survivable on a rooftop.** A blank form every morning is a form that gets shorter every week until it is worthless.

**`toolbox_meeting`** — site_report_id · topic (proposed from today's permits to work and recent near misses; the Person In Charge may override) · **photograph (required, in-app capture only, never from the gallery)** · **attendees (list of named person references, required)** · conducted_by. **One per site report. Required.**

**`attendees` is a list of named people, not a headcount integer.** A count cannot be paid, cannot be reconciled against a photograph, and cannot answer who was exposed after an incident. **This one record serves three purposes: a safety record, the attendance record for payroll, and the verify layer of deployment. One capture, three consequences. It must never be made optional, shortened, or moved off the site report.**

**`site_report_activity`** — site_report_id · **project_block_id (required — every activity belongs to a block)** · description · percent_accomplished · manpower_allocated (from `toolbox_meeting.attendees`) · blocked · blocked_reason (`material`/`predecessor_block`/`external_or_utility`/`weather`/`manpower`/`client_access`) · **blocked_expected_clear_date (required wherever knowable)**.

Expected clear dates come from: material → the outstanding line's expected arrival date, automatically · predecessor block → its forecast completion · external or utility → entered · weather → not applicable · manpower → deployment · client access → entered, and accumulates as client delay. **Anonymous blocking is how work disappears.**

**`site_photograph`** — site_photograph_id · site_report_id · project_block_id · image · created_on_device · caption. Ten to twenty-five per report, approximately 300 kilobytes each after compression.

**`non_conformance_report`** — non_conformance_report_id · project_id · project_block_id (required where against work rather than a delivery) · source (`delivery`/`site`/`client`) · goods_receipt_id (required where source is `delivery`) · description · **photograph_id list (at least one where source is not `delivery` — where source is `delivery` the evidence is the goods receipt's own photographs, because a warehouse receipt has no site report)** · raised_by · raised_on · **owner_id (accountable for closure)** · required_action · target_close_date · state (`open`/`action_taken`/`closed`/`void`) · closed_by · closed_on · **closure_evidence_id (required in `closed`)**. Closure requires gate 19; `void` requires a reason and is reported.

**Same-day closure is the pattern that makes this record worthless**, so the ageing query reports the closure rate alongside the ageing — a report closed the moment it is raised is visible as a pattern rather than invisible as a good number. **It is creatable offline**, because the moment a non-conformance is noticed on a roof is the moment it is recorded, or it is not recorded.

**A safety inspection raises a `corrective_action`, not a non-conformance report. The two are different instruments and neither raises the other.**

**Completion, derived and never typed:**

```
block percent complete   = sum of percent_accomplished across that block's site report activities
project percent complete = sum over included blocks of (block percent complete × value_weight)
```

**No person anywhere in this platform types a project percentage complete.** There is no such field on any screen, in any form. Search for one before you ship; there must be none. **Totals are computed, never typed** — manpower totals, percentages, hours.

**General Requirements carries no value weight — you cannot install a permit.** Including overhead means a construction curve can never reach one hundred percent while paperwork is open.

**Weights re-base only on an accepted variation order, never on a cost correction**, and **the interface must display percentage complete both before and after.** A project moving from 62 percent to 58 percent overnight with no site activity is correct and will be read as a defect unless the platform says why.

**Progress billing runs off this number.** A percentage entered carelessly on a rooftop becomes money claimed from a client and later becomes revenue recognised in a period. **Every strict rule here has a financial reason, not a hygiene one.**

**Weather is delay evidence, not a field.** `work_stopped_by_weather` is a contractual record. Weather delay is a claimable extension under most of the contracts Magnus signs, **and it is claimable only if it was recorded on the day, on the site, by the person there.** Recorded a month later during a dispute it is an assertion; recorded daily it is evidence.

**The Turnover Document is gate 21.** One date, entered once, starts three clocks. A defect reported after turnover traces to the block, the site report, the date and the people recorded present that day — **a defect claim in year three is answered by the year-one record or it is not answered at all.** That is what the named attendees list makes possible, and it is a warranty asset.

**Cost per block:** material committed at purchase order issue · labour from deployment × rate · subcontractor · equipment.

## 8.8 Permits (module 9)

**A permit here is a government or utility authorisation for a project. A permit to work in module 12 is a same-day authorisation for a hazardous activity. They share a word and nothing else. Do not merge them and do not let them share a table.**

**One route. No branches.** 50 kilowatt-peak, 100 kilowatt-peak and 1 megawatt are identical, with or without battery storage — both confirmed by the Chief Executive Officer, and both closed by removal rather than by answer. **Do not build a rules engine that selects a permitting path by system size.** If you find yourself writing branch logic here, stop and re-read this paragraph. The 100 kilowatt-peak cap in the Magnus manuals is a net metering programme boundary, not a change in how a project gets approved. **Because the route does not change with size, every project's history informs every other project's forecast, and the accumulated learning becomes useful far sooner.**

**`permit_type`** — permit_type_id · permit_type_name · group (`local_government_unit`/`environmental_and_safety`/`utility_interconnection`) · issuing_body_class · gates_what.

**`project_permit`** — project_permit_id · project_id · permit_type_id · **issuing_body (the specific office, not the class)** · responsible_person · **mode (`parallel`/`prerequisite`)** · date_filed · **expected_approval_date (required once `filed`)** · date_approved · expiry_date · fee_amount · state (`not_required`/`to_file`/`preparing`/`filed`/`awaiting_response`/`additional_requirement`/`approved`/`rejected`/`expired`) · last_followed_up · follow_up_count · **regulatory_version_in_force_at_filing**.

**`permit_requirement`** — permit_type_id · issuing_body · requirement_description · first_observed_on_project · **times_observed** · last_observed.

**`permit_duration_observation`** — permit_type_id · issuing_body · **days_filed_to_approved (working days)** · follow_up_count · project_id.

**This module's primary output is not a status board.** The largest identified waste in permitting is not slow government offices — it is that per-local-government-unit knowledge is rediscovered every time. Two liaison officers independently learn the same requirements for the same office and none of it is written anywhere; **when one of them leaves, it is gone.** Build the accumulation: what was actually required, on which project, and how long it actually took. **Do not build a screen where someone maintains a requirements list** — it will be populated once and be wrong within two projects.

`times_observed` is what separates this from a wish list: *this office has asked for this on every project we have filed there* is a fact; *this came up once in 2024* may not recur.

**`additional_requirement` is a distinct state, not a delay.** Entering it does three things: raises a task to supply it, owned by whoever can produce it — **often engineering, not the liaison** · **writes the requirement to the library** so the next project at that office includes it first time · **re-bases `expected_approval_date` and records that it was re-based rather than missed.** *The permit is late* teaches nothing. *This office requires a document we did not know about* stops the same delay on the next four projects.

**Expected approval date sources, in priority order:** accumulated median for this permit type at this issuing body · accumulated median across all offices · **provisional default of 90 working days for a building permit. Ninety days is a planning constant, not a bad case** — a programme built on an optimistic permit assumption was wrong when it was written.

**`follow_up_count` accumulates per office**, producing a fact nobody currently has: how many chases this office typically requires. That is a resourcing number for the liaison team.

**`prerequisite` mode carries hard block 4 and is a critical-path exception from day one, with no ageing threshold.**

**What permits gate:** prerequisite-mode permit → mobilisation, hard block 4 · Construction Safety and Health Program → start of construction, hard block 2 · Permission to Operate and interconnection approval → energisation · **occupancy and closeout permits → project closeout, and final billing where the contract makes it a condition.**

**Closeout permits are a commercial exposure, not an administrative one.** Where a contract conditions final payment on closeout permits, **an open permit is unbilled revenue** — the kind that stays unbilled for years because the project is finished and nobody is looking. Surface it valued.

**Each project records the regulatory requirements in force when it was filed.** Rules change — the Department of Labor and Employment moving Construction Safety and Health Program submission to an online portal is a current example. **A project filed under the old rules must not be judged against the new ones.**

**Gate 20 has no value threshold, and this was a deliberate removal rather than an unset value.** The reason to engage a permit consultant is almost never the size of the fee — **it is that a permit is stuck.** A threshold would hide the cheap engagements, which are exactly the ones that reveal a pattern. **Every engagement approved means the platform accumulates which local government units keep needing outside help.**

**Permit fees go to project cost**, so cost accumulates by permit type and local government unit — the figure that lets Magnus price and programme new territory instead of guessing.

**The platform never files anything.** It holds the deadline, records the reference once a person has filed, and stops there. **A platform that shows a filing as submitted when a person still had to do it produces exactly the failure it exists to prevent — a control that looks satisfied and is not.**

## 8.9 Inventory and warehouses (module 10)

**`location`** — location_id · **location_type (`warehouse`/`site_stock`)** · name · **region (drives the route class on a transfer)** · **custodian_id (a named person, accountable for count variances)** · project_id (required where `site_stock`, empty on a warehouse) · state (`open`/`closed` — a site stock location closes at project turnover, and a closing count is required first).

Seed: Laguna (Luzon, Jay) · Sorsogon (Bicol, Bernie) · Dumaguete (Visayas, Paul).

**A project running beyond twelve weeks holds a site stock location. Site stock is stock.** Without it, material issued to a long project disappears from inventory the day it is issued and reappears only as a variance months later.

**`item`** — item_id · description · specification · **unit_of_measure** · **is_serialised** · category · **reorder_point — operations and maintenance spares only.** Project material is bought against the bill of materials; **a reorder point on project material would buy things no project needs.**

**`stock_position`** — item_id · location_id · quantity_on_hand · **quantity_in_transit** · quantity_quarantined · valuation_basis.

**`transmittal`** — transmittal_number · job_order_number · **from_location · to_location** · purpose · system_reference_number · date · time_of_release · line items (quantity, unit, item description with brand, size, colour, capacity) · **prepared_by · confirmed_by · received_by (each a signature and date)** · state (`draft`/`awaiting_approval`/`issued`/`in_transit`/`received`/`received_short`/`cancelled`). A transmittal may be cancelled only before `issued`, by the approver, with a reason. `received_short` raises a stock adjustment and gate 26. **A transmittal with no state is the leak this module exists to close** — stock that has left one place and not arrived anywhere is only visible if the record has somewhere to sit between the two.

This is the digitised form MRTC-PROC-F003, field for field. **The digitised form becomes the controlled version and the paper form is superseded** — otherwise Magnus holds two live versions of the same form, both claiming to be current.

**All four directions are real and all four are transmittals:** warehouse → warehouse · warehouse → site · **site → warehouse** · site → site.

**The defect this module exists to close is not a missing signature.** The form has always carried a RECEIVED BY block; Magnus designed acknowledgement in from the beginning. **The defect is that the receiving signature never returns anywhere reconcilable** — it is signed, filed, and nothing compares what was sent against what was acknowledged. **This is the clearest instance of the company's dominant pattern: a control that exists, is performed correctly, and is read by nothing. The platform's change is not to add a signature. It is to make the signature return.**

**Stock moves on receipt, not on despatch.** Issue decreases origin and increases in transit; the receiving signature decreases in transit and increases destination. **Stock that has left one warehouse and not arrived at another is IN TRANSIT — a real state with a real balance.** Modelled as arriving on despatch, an inter-island shipment is counted at its destination for ten days before it exists there, **and a shipment that never arrives is invisible until a count.**

**Route class derives from the FROM and TO fields already on the form** — no new input from the custodian. Within region: 3 days expected transit. Inter-island: 10 days. Where a project site is the destination, the class follows the site's region. A transmittal in transit beyond its expected days is queryable.

**When the received quantity differs from the sent quantity the platform raises a discrepancy in the same transaction, to both custodians and the Procurement Head.** This single behaviour converts the signature from a filed piece of paper into a control: a shipment that arrives short is known **on the day it arrives, at both ends, by the two people who can still do something about it** — not at the next count, by a person who was not there.

**`physical_count`** — physical_count_id · location_id · count_type (`opening`/`quarterly`/`high_value_monthly`/`spot`) · **counted_by (never the custodian alone on an opening count)** · counted_on · state (`scheduled`/`counting`/`variances_raised`/`closed`/`locked`) · locked_by · locked_on.

**`stock_adjustment`** — stock_adjustment_id · location_id · item_id · counted_quantity · system_quantity · **variance (derived, never typed)** · **source (`physical_count`/`short_receipt`)** · count_id (required where source is `physical_count`; a short receipt raises the adjustment without a count) · **closing_reason** · state (`raised`/`investigated`/`approved`/`posted`) · investigated_by · approved_by · approved_on (gate 26).

**Zero tolerance: every difference between counted and expected quantity is recorded and explained before the count closes. No item is exempt, whatever its unit of measure. Gate 26 applies to every adjustment, with no value threshold.**

**`measurement_estimate_on_non_unit_item` is a valid closing reason, and it is what keeps zero tolerance honest.** Cable, ties, bolts and sealant cannot be counted to a true zero; applied there, zero tolerance produces an investigation on every count and **within months people write explanations that mean nothing just to close the count. A control that always concludes the same way stops being read.** The closing reason lets the count close honestly in one action. The variance is still recorded and still visible. Nothing is waived — **and the platform reports how often each reason is used**, so *measurement estimate* being applied to panels is visible as a pattern rather than buried in free text.

**Valuation:** serialised items — panels, inverters, batteries — by specific identification; everything else by weighted average. **Surplus returned from a site re-enters stock at the cost it was issued at**, and the originating block's cost reduces by the same amount. Returned at a current or average price, a project's cost silently changes because material came back, and block cost, value weight and reported margin all move with it. **At cost, the return is neutral.**

**Cadence:** all items quarterly, high-value items monthly. **Variance by warehouse and custodian is reported as a Check for investigation, never as a custodian score.**

**The opening balance is the highest-consequence one-off action in the entire build.** Gate 27, Cristy locks each warehouse after a spot check, no alternate. Everything the inventory module ever reports is measured against it; wrong, it produces confident incorrect answers indefinitely, and **the error is nearly impossible to find later because it looks like an accumulation of small variances rather than a single wrong starting point.** **Both the count date and the lock date are recorded** — anything moving between them is the classic source of an opening error, and with both dates held the error is findable rather than permanent. Sequence: count → spot check → lock → only then is the warehouse live. *Recorded tension, accepted: zero tolerance applies to every count thereafter while the baseline itself is spot checked rather than counted in full.*

**Quarantine.** Material in dispute, damaged, wrong, or under a supplier non-conformance is quarantined. **Hard block 5: quarantined material cannot be issued to a site, at any permission level.** A quarantined item is not merely labelled — it cannot be issued, because material accepted into a warehouse and then installed is functionally impossible to recall from a roof. Release or disposal is recorded with a reason and an owner.

**Every issue names a project and a block.**

## 8.10 Manpower, workforce and equipment (module 11)

**Two objectives, and the second is the one currently invisible: see the resources, and request the resources needed.** Seeing resources is useful. **Recording what was asked for and not supplied is what makes hiring an evidence-based decision rather than an argument.** A declined resource request is today a conversation that happens and leaves no trace.

**`resource_availability`** — computed, never entered: resource_id · resource_class · current_assignment · **`available_from` — when it frees up** · status (`available`/`assigned`/`in_transit`/`maintenance`/`unavailable`). *Where is it now* is a status board. **When does it free up is a plan** — a single generator or lifting rig on an inter-island portfolio can only be scheduled around if the release date is visible.

**`resource_request`** — request_id · **project_id and project_block_id (both required)** · resource_class (manpower/equipment/vehicle/skill) · what · how_many · skill_or_asset (capability tag) · **needed_from · needed_until** · **why** · requested_by · allocator (routed by class and region) · state (`requested`/`allocated`/**`partially_allocated`**/`declined`/`fulfilled`/`cancelled`) · **decline_reason (required on decline, from the controlled list — free text alone is not accepted)**.

**Decline reasons, and they must never be aggregated into a single decline rate:** no one available with this skill (**a capability shortage — hiring evidence**) · resource committed elsewhere at higher priority (a scheduling conflict) · equipment unavailable or under maintenance (**a capital decision**) · request not justified (a management judgement) · needed-from date not achievable (a planning failure, somewhere). *No one available* four times in a quarter is a hiring case; *committed elsewhere* four times is a scheduling problem, and hiring would not fix it.

**`partially_allocated` is a distinct state. Three of five people is not fulfilment.**

**A request unfulfilled past its needed-from date is a block that either did not start or started short-handed** — a schedule fact and often a cost fact that today leaves no trace at all. It is valued against the block it was raised for.

**`deployment`** — deployment_id · person_id · project_id · block_id · **planned_from · planned_to (the plan layer)** · **recorded_days (derived — days this person appears in a toolbox attendance list)** · **verified_days (derived — days carrying both the toolbox photograph and a signed acknowledgement sheet line)** · **labour_rate (money per day, effective-dated, set by Human Resource, changed under gate 31 — a rate change never restates a closed period)** · state (`planned`/`active`/`ended`).

**Three layers, and the platform reports the variance between them without ever silently overwriting one with another.** Plan against record is a scheduling fact — did the people intended actually go. Record against verify is a control. **Overwriting the plan with the record makes every project look perfectly resourced in hindsight; overwriting the record with the verify layer destroys the only evidence that the two ever differed.** Both numbers are true statements about different things, and the variance is the information. **This is verification of a record, never surveillance of a person.**

**Roster continuity:** a person appearing in two projects' toolbox lists on the same day is flagged. Usually a data error, occasionally something else — either way worth knowing, and neither is currently detectable.

**`equipment`** — equipment_id · description · serial_number · **custodian (a named person, never a location)** · certification_expiry · maintenance_due · **utilisation (accumulated from deployment, never entered)**. Equipment held by a place is equipment nobody is accountable for. **Expired lifting gear on a site is a legal and a safety exposure, and it is the class of thing discovered by an inspector rather than by the company.** Utilisation answers whether a second one is needed, with evidence rather than opinion.

**Scheduling awareness shows approved leave and assignment overlap when a deployment is planned. It never shows the reason for leave, any medical information, or any presence, location or activity data — at any permission level.**

**Bench depth:** any capability held by fewer than two people, where that capability sits on a project critical path, is flagged continuously. Three such capabilities exist; one is confirmed — **only one person can programme the battery energy storage systems.** This is a single point of failure no organisation chart shows, **the mitigation costs shadowing time rather than a salary, and it is a live exposure now rather than a platform feature.**

**Permissions on this module:** Project Manager — sees own projects and the available pool, requests, does not allocate, rates per money visibility · Department head — own department, requests and allocates, sees rates · Chief Operating Officer — all, requests and allocates, sees rates · Person In Charge — **own site only**, requests, does not allocate, **no rates** · Human Resource — all people, neither requests nor allocates, sees rates. **No role sees a person's leave reason, medical information or presence data through this module.**

**Deployment records carry a regularization exposure under Philippine labour law.** A long continuous deployment record for a person engaged as a site worker is evidence in a regularization question. **The platform records the truth; counsel decides the retention period.**

## 8.11 Safety (module 12)

**DO NOT REDESIGN SAFETY.** Magnus already has a complete occupational safety and health system — manual `MRTC-OSH-GDL-00 Rev 00`, eighteen chapters, six permit-to-work types with a seven-step process, a full emergency plan, an eighteen-point incident investigation record, inspection cadences, a corrective action tracker and thirteen named performance indicators. **The manual is not the problem. The problem is that it commits to thirteen indicators with no mechanism to produce them.**

This is the third instance of the same company-wide finding: **Magnus writes excellent policy that assumes data infrastructure it does not have.** The procurement scorecard scores against reference prices that do not exist. The monthly report is reconstructed by hand and carried eight arithmetic errors in July. The safety manual promises thirteen indicators nothing computes. **This is the clearest available statement of what the whole platform is for.**

**Implement the manual. Do not improve it, simplify it, or substitute a general safety module for it.**

**`permit_to_work`** — project_id · block_id · type · **valid_from · valid_to — same day only** · **named_worker_id list** · issued_by · issued_on · state (`requested`/`issued`/`closed`/`expired` — `expired` is set by the clock at end of day, never by a person).

**Six types, all approved by the Safety Officer of record, built configurable per type** so a future split of approving authority needs configuration rather than code: **working at height (carries hard block 3)** · hot work · electrical work on live systems · confined space entry · lifting operations · excavation.

**Gate 28: never auto-approved, no delegation window, and no configuration setting can change this.** Issuing a permit to work is a professional judgement by a qualified person. **There must be no code path, no permission level and no screen through which this becomes automatic or delegable.**

**Competency-gated: a worker with lapsed training cannot be named on the relevant permit.** The manual already requires this and nothing currently enforces it — **this is one of the clearest examples in the entire specification of a control that exists on paper and does not exist in practice, and enforcement costs one check against the capability tags.**

**An open permit past its validity window is a live finding, not an expired record.**

**`incident`** — project_id · occurred_on · classification (`near_miss`/`first_aid`/`medical_treatment`/`lost_time`/`disabling`/`fatality`) · **the eighteen investigation points from the manual** · photograph_id list · investigated_by · closed_by · closed_on · state (`reported`/`under_investigation`/`closed`). **Gate 30, countersigned by the Chief Operating Officer.**

**Near-miss reporting must be frictionless: a per-site Quick Response code to a simple no-login form.** Anyone physically on site — Magnus staff, subcontractor crews, delivery drivers — scans, adds a photograph and a sentence, submits. No account, no install, **no identity captured in any dashboard.** The Safety Officer triages everything received. **Every field added to this form reduces the number of reports, which reduces safety, not paperwork.**

**NON-RETALIATION IS A PRODUCT REQUIREMENT, enforced in software.** No reporter identity in any dashboard, report or export. No per-person incident counts outside the safety function. **A system that lets someone be counted for reporting will stop receiving reports. That is a safety outcome, not a data outcome.**

**`safety_stop`** — project_id · block_id · **raised_by — any person on site, no minimum role, no approval** · raised_on · reason · photograph_id · lifted_by · lifted_on · state (`active`/`lifted`).

Crew and subcontractor personnel do not sign in, so they raise one through **the same per-site Quick Response code as the near-miss form, which carries a stop-work option routing immediately to the Safety Officer and the Person In Charge.** Account holders raise it from the block. It stops work on the named block immediately. **Raising one is never recorded against the person who raised it.**

**Gate 29: only the Safety Officer lifts it. No alternate, no delegation window, no configuration setting.** There is no other transition out of `active`. **The accepted consequence, confirmed as a deliberate design position: with no named alternate, a safety stop with an unreachable Safety Officer halts work indefinitely. That is the safe failure direction and it is the correct one.** The mitigation is operational — ensure each project's Safety Officer is reachable, or name a second qualified officer — **not a platform setting.**

**`corrective_action`** — source (`inspection`/`incident`/`near_miss`/`audit`) · source_id · owner_id · **hierarchy_of_controls_level** · target_date · state (`open`/`action_taken`/`verified`/`void`) · evidence_id. **Closing one without evidence is permitted and is reported. Nothing is blocked.** `void` requires a reason and is reported.

**`inspection`** — type (`daily_walk`/`weekly_checklist`/`monthly_audit`) · project_id · performed_by · performed_on · **item-level answers** · state (`scheduled`/`performed`/`actions_raised`).

Cadence: daily walk every working day by the Safety Officer or Person In Charge · weekly checklist by the Safety Officer · monthly audit by the Safety Officer.

**All three routines are structured checklists, each item answered individually**, which is what lets the platform report which items fail most often, on which projects, and whether a failure recurs after it was closed. **That is the difference between knowing the walk happened and knowing what it keeps finding.**

**Keep the daily walk deliberately short.** A structured daily checklist that takes two minutes gets done properly every day; **one that takes fifteen gets copied from yesterday — and a copied checklist is worse than no checklist, because it produces confident data that is false.**

**⚠ OPEN DEPENDENCY, BLOCKING: the item content of all three checklists must come from Alma Codog, and the manual `MRTC-OSH-GDL-00 Rev 00` itself is not available.** The manual names the thirteen indicators, the seven permit-to-work steps and the eighteen investigation points. **Build the structure to hold checklists of any length and leave the content slots empty. Do not invent them.**

**The thirteen indicators are all computed from records the platform already holds. None is typed by anyone**, and no screen exists for entering an indicator value. **Leading indicators are given visual priority over lagging ones** — a leading indicator can still change the outcome. Two further indicators are recommended: **near-miss to incident ratio** — a falling ratio is usually reporting collapsing rather than safety improving, and it looks like good news on every dashboard until something happens — and **hierarchy of controls distribution**, which shows whether corrective actions eliminate hazards or rely on personal protective equipment, the weakest control and the most commonly chosen.

**Statutory obligations are stored with their deadlines and are queryable. Nothing raises them on a schedule** — *section 16, deviation D7.* Work Accident/Illness Report by the twentieth of the month following a disabling injury or death · Annual Medical Report by 31 March · Safety Officer designation on establishment and on change · safety committee meetings. **Non-compliance penalties reach ₱50,000 per day.**

**The Construction Safety and Health Program is a schedule item, not a safety-department task.** Status is a field on the project and it gates the Site Safety Infrastructure block. **This is an external critical-path dependency of the same class as client design approval or the sealing engineer, and it appeared nowhere in the original design.** Approval takes as long as it takes, and the project cannot start construction until it arrives. **Fall protection before roof work is Republic Act 11058, not a preference**, and hard block 3 doubles as the compliance record — a timestamped trail that protection was in place before crews went up.

**The site emergency card is held offline on every phone** — nearest hospital, ambulance, evacuation point, first aiders on duty, client contact. **The moment it is needed is the moment the signal is worst.** A live first-aider roster is held per site.

**Subcontractor personnel are recorded, linked to their employing subcontractor, and inherit that subcontractor's accreditation and insurance status from the party record, exclusions included.**

**Nothing in this module is ever deleted.** An incident, a near miss, a safety stop and a corrective action are closed, voided or superseded — never removed.

## 8.12 Tasks and deliverables (module 13)

**A task is a person's guide to their day. Not a project management artefact, not a timesheet, not a project plan.** A task is what one person does; project sequencing lives in modules 6, 7 and 8, where dependencies are structural rather than assigned.

**`task`** — task_id · title · **owner (exactly one person — never two, never a team, never a role)** · project_id · project_block_id · **output_type (required)** · output_object (polymorphic) · source · priority (`normal`/`priority`) · **committed_date (set once, permanent, never overwritten)** · current_date · **recommit_count** · state · blocked_by_person · blocked_expected_clear · grade.

**There is no `hours`, `time_spent`, `started_at` or activity field, and there never will be.** The moment a duration field exists someone asks for a report on it and the platform becomes a timesheet in everything but name. **L4 is not satisfied by choosing not to report on a field that exists — it is satisfied by the field not existing.**

**Eight output types, and no task exists without one:** Document · Sales outcome · Business opportunity · Approval or decision recorded · Record or data entry · Physical work · Communication sent · Verification.

**Where the output is a platform object, creating that object closes the task in the same transaction.** A site report filed closes the site report task; a purchase order approved closes the approval task. **This is what makes the rule survivable** — if every task also required someone to mark it done, the mandatory-output rule would be pure overhead and people would stop using the list. **The output IS the completion.**

*"Follow up with the client"* is not a task. *"Send the client the revised proposal"* is, and the sent proposal is the evidence. **Output type is reportable, which answers a question the company cannot currently answer at all: what does this department actually produce?**

**States:** `draft` · `pending_approval` · `to_do` · `in_progress` · **`blocked`** · `done` · `graded`.

**A task cannot enter `blocked` without a named blocker and, wherever knowable, an expected clear date. When a task is blocked on a person it appears on that person's daily screen as something they are holding up.** Anonymous blocking is a task nobody is responsible for clearing, sitting in a list nobody escalates.

**The daily screen shows, in this order — and the order is the specification:** overdue · **blocked (in its own section — not the person's fault, and it must not sit in their overdue list accusing them, showing the named blocker and the expected clear date)** · due today · priority · due this week.

**Unfinished work carries forward automatically and is never silently dropped.** A task that disappears at midnight teaches people the platform loses things, **and a person who believes that keeps their real list somewhere else — the moment a private list exists, the platform's task data is decorative.**

**Sources:** derived · requested · **recurring (a standing obligation, stored with its cadence — an agent instantiates it, nothing schedules it)** · self-registered · claimed. **Self-registration matters:** much real work is never assigned by anyone, and a platform holding only assigned work is systematically wrong about exactly the people who take initiative.

**The open assignment board** holds work that needs doing and has no owner. A person **claims** it, which sets them as owner, and may **release** it back with a reason. An unclaimed task older than ten working days is queryable for the department head.

**Priority is scarce: two levels only, and a requester may hold at most three priority items at one time, across all their requests.** Scarcity is the entire mechanism — with unlimited priority everything becomes priority within a month and the marker means nothing. **The limit is what makes marking something a priority a real decision: the requester must choose what to un-prioritise.** Three levels were considered and rejected — a middle level is where everything goes.

**`committed_date` is kept forever.** If moving a date overwrites it, a task moved five times looks exactly like a task delivered on time. **`recommit_count` is the only honest measure of whether commitments in this company mean anything, and it costs one extra column.** A third recommitment is a different problem from a delay — once is a change of plan; three times is a task that is not going to be done, or was never sized correctly, and it needs a conversation rather than a fourth date.

**Grading a task is not appraising a person.** Grades are `met`/`partially_met`/`did_not_meet`, optional per task, set by the requester or the owner's manager, and visible on tasks and in the performance *conversation* as context a human reads. **The platform computes no aggregate grade score per person. There is no code path that turns a set of grades into a number describing a person.**

**A person with no open task for three working days is flagged to their manager and their director as a Check — never to the person, and never on their record.** A person with no task has not failed at anything: **they have not been given work, which is a management failure, and the notification must go where the failure is.** Sending it to the person converts a management signal into an accusation and converts the module into the surveillance instrument L4 forbids. No flag is raised for approved leave, suspension, or roles the console defines as not task-based.

**Load is displayed as a band — light, normal, heavy — never as a number.** Signals: open commitments · deadline density · spread across projects · ageing · queue depth and planned-versus-reactive ratio for support staff. **A load number invites comparison between people, and comparison between people is a rating.** A band supports the only legitimate question — does this person have room for more work — without producing a figure that can be ranked. **Work-in-progress limits per role are set after one quarter of real data, not guessed now.**

## 8.13 Communication (module 14)

**This module replaces something that works.** Magnus runs on Facebook Messenger group chats, one per project plus department groups. People are fast in them, they are on everyone's phone already, and they cost nothing. **A replacement that is merely equivalent will lose.** The only thing this offers that Messenger cannot is **the conversation happening on the record it is about** — the block, the purchase order, the permit — with a permanent link, in front of the data, findable years later by someone who was not there. **If a discussion about a purchase order takes more taps than posting in a group chat, people will post in the group chat. Speed is not a nice-to-have here; it is the whole competitive position.**

**`thread`** — thread_id · object_type · object_id · channel_id. Created lazily on first message; no object carries an empty thread row.

**Every object carries a thread, without exception and without configuration:** project · block · task · site report · transmittal · permit · purchase order · bill of materials line · goods receipt · progress claim · fund request · write-off · stock adjustment · variation order · Non-Conformance Report · safety stop · document · person · design deliverable. **There is no screen where an administrator decides which objects have threads** — a missing thread is the one place a conversation goes back to Messenger, and **once it goes back for one thing it goes back for everything.**

**When something is about a record, the conversation belongs on the record.** Channels exist for work that genuinely has no object — office administration, commercial discussion, a question with no home yet. **They are the exception, not the default. A platform whose channels carry most of the conversation has rebuilt Messenger inside itself and gained nothing.**

**`message`** — message_id · thread_id · author · body · created_on_device · received_by_server · **client_message_key (generated on the device before the first attempt, for de-duplication on retry)** · reply_to · hidden_by · hidden_reason.

**`mention`** — message_id · **mentioned_person (exactly one per row)** · notification_id.

**`attachment`** — message_id · file · capture_source (`in_app_camera`/`file`).

**`channel`** — channel_id · channel_type (`project`/`department`/`direct`) · linked_object · members · read_only. **Membership follows roles and project assignment automatically:** a person leaving a project leaves its channel; a person leaving the company loses all of them immediately on identity provider disablement.

**The mention is the attention mechanism, and notification is governed by the mention, not by the thread. A thread nobody is mentioned on notifies nobody.** The alternative — notifying everyone who ever commented — is how a group chat becomes unreadable and is precisely what Magnus is leaving. **A person notified about everything mutes it, and once muted the thread cannot reach them even when it matters** — at which point the platform has lost the ability to call their attention, which is the objective. A mention names exactly one person; mentioning three creates three notifications. **The notification opens the object, not the message.**

**There is no subscription, no watch and no mute.** They exist to manage noise that mention-based notification does not create, **and adding them would let a person mute the mechanism by which the company calls their attention.**

**A direct message is the one message that notifies without a mention**, because a direct message has no other audience.

**Search is load-bearing, not a feature.** Magnus's Messenger history contains almost ninety percent of the information about how projects actually ran. Search covers message text, attachment filenames and the object a thread belongs to, scoped by `record_scope`.

**Convert a message to a task in one action** — the single most valuable feature in this module. **The failure mode of every group chat in every company is that work is agreed in conversation and never recorded anywhere with an owner and a date.** Conversion is the bridge, **and it must be one tap, because the moment it is three, people stop.** The created task requires an output type, which forces the conversation to say what was actually agreed.

**A photograph attached to a message is not a site record.** Site photographs belong on the site report where they are dated, placed and attributed. Where a photograph is offered on a block thread, the platform prompts: *attach to today's site report instead?*

**Messages are append-only. A correction is a new message.** An administrator may **hide** a message for genuinely inappropriate content; the hiding is itself logged with who, when and why, and the message is not deleted — the thread shows that a message was hidden. **A conversation that can be silently rewritten is not evidence of anything, and this record is expected to answer questions years later.**

**Offline:** compose queue · automatic resumable retry · **messages send in composition order, not completion order** · **de-duplication by `client_message_key`** · **text sends before attachments — a message is never held hostage by its photograph.** Duplicated messages on retry destroy trust in a channel faster than any other defect, and they are the standard symptom of a weak-signal environment.

**Legal hold suspends retention entirely on a nominated project or thread**, set and released by a console holder, logged.

**Reactions exist** — acknowledgement without a message reduces noise. **Pin, bookmark, quote and reply exist.**

## 8.14 Document control (module 15)

**So that nobody builds from a superseded drawing, and so that a question asked in year three can be answered by the record made in year one.**

Magnus's documents sit across eight Google Workspace accounts, so **this is an authority problem, not a recovery problem** — nothing is at risk of being lost. **The problem is that nobody can say which copy governs.** Two people can hold two revisions of the same drawing, both in good faith, **and only the site discovers the difference.**

**`document`** — document_id · document_number · title · **classification (`controlled`/`archive`/`unclassified`)** · classified_by · owner · attached_to_object · review_cycle_months · next_review_due · legal_hold.

**`document_revision`** — revision_id · document_id · revision_number · file · status (`draft`/`for_review`/`approved`/**`in_force`**/`superseded`/`withdrawn`) · approver · approved_at · **in_force_from · in_force_to (empty means current)** · superseded_by · seal.

**`document_acknowledgement`** — **revision_id (acknowledgement is of a revision, never of a document)** · person_id · acknowledged_at.

**`required_document`** — module · object_type · document_type · mandatory · gates_what. **The register is derived from module declarations, never maintained.** There is no screen where someone builds a checklist of required documents per project — **a hand-maintained checklist drifts from what the platform actually enforces, and then people trust the checklist.**

**THE REVISION-IN-FORCE RULE — the single most valuable rule in this module and the one most likely to be built as *link to the document* rather than *link to the revision*.** Every historical record references **the revision that was in force at the time of the record**, not the current revision. A site report made on 3 March references the drawing revision in force on 3 March. A purchase order on 14 May references the bill of materials revision in force on 14 May. A permit filing references the sealed revision submitted, permanently.

**Link to `revision_id`. Never to `document_id`. Anywhere.**

A defect appears in year three and the question is whether the crew built what the drawing said. If site reports link to the document, opening one shows today's revision — revision 7, while the crew built revision 3 — **and the record then appears to prove the crew was wrong when it proves nothing at all.**

**Exactly one revision of a controlled document is `in_force` at any moment. Superseded revisions are retained and never silently replaced, and a superseded revision opened by anyone must say so on the face of it and link to the revision that governs.** The most common way the wrong thing gets built is not a missing document — **it is an old one that looks current.**

**Controlled versus archive:** controlled means only the current revision may be used — drawings, specifications, procedures, company forms, manuals. Archive is kept for reference and nothing depends on its currency — photographs, correspondence, reports, certificates received. **Archive documents may never be referenced as governing.**

**Classification is by a person under gate 33, with no automatic default and no alternate. An unclassified document is visible but not usable for construction** — it can be seen, opened, discussed and attached to a message thread, carries a clear unclassified mark on every view, **and cannot be attached to a work instruction or referenced as the governing revision.** This separates reading a document from building from it: nothing stops while Cristy is unavailable, **and the failure controlled documents exist to prevent cannot occur, because an unclassified document can never be the governing revision.**

**Company forms are controlled documents with revision numbers** — the transmittal form, the daily site report, safety forms, the payroll acknowledgement sheet. **The platform implements the form's current revision, and the form's revision is recorded on every record created from it, so records created under the old revision remain readable as they were.** This is how a form quietly diverges: the paper form gains a field, the platform does not, and for eighteen months two versions of the truth exist.

**A new revision of an acknowledged document resets acknowledgement for everyone on its distribution list.** A person who acknowledged revision 2 has not read revision 5, **and a system that says they have is worse than one that says nothing.**

**A review that confirms no change still records a review** — the document is then demonstrably current rather than merely old.

**Six permanent classes, never subject to any retention schedule:** site photographs · as-built drawings · test and commissioning records · structural certificates · permits · contracts. **A defect claim in year twelve is answered by the year-one photograph set, or it is not answered at all.**

**Legal hold** suspends retention entirely on a nominated project, document, thread or person's records. Set and released by a console holder, logged. **It overrides every retention rule, including erasure requests, to the extent the law permits — which is a question for counsel, not for the platform.**

**Documents are produced elsewhere and controlled here.** There is no document editing inside the platform.

## 8.15 Finance and cash (module 16)

**This is a sub-ledger. It is not a general ledger. Do not build accounting.** The platform holds no chart of accounts, posts no journals and produces no statutory financial statements. **It reads from Magnus's accounting system and never writes to it.**

**Build the six things the accounting system cannot produce**, because they require project structure it does not hold: work in progress schedule · **committed cost, because a purchase order is not an accounting entry** · cost to complete · estimate at completion · over- and under-billing · **certified against claimed, because the client's certification lives in correspondence**.

**`billing_milestone`** — project_id · sequence · description · basis (`percentage_of_completion`/`milestone_event`/`fixed_date`) · amount or percentage · state (`not_due`/`claimable`/`claimed`/`certified`/`invoiced`/`paid`).

**`progress_claim`** — claim_id · project_id · **percent_complete_claimed (from module 8, derived, never typed)** · amount_claimed · **amount_certified (entered when the client certifies; may differ)** · date_claimed · date_certified · state (`draft`/`awaiting_approval`/`claimed`/`awaiting_certification`/`certified`/`invoiced`/`paid`/`disputed`).

**Claimed and certified are two numbers, always.** Collapsing them loses the single most useful commercial fact in the module: **which clients certify what Magnus claims, and which do not.** A client who habitually certifies ninety percent of every claim is a pricing decision, not an accounting detail.

**Uncertified claims are queryable at thirty days — one billing cycle.** Long enough that ordinary client processing does not trigger it; short enough that a claim cannot sit a quarter. **The query carries the amount, the client, the age, and that client's own average certification time.** A client habitually running at forty-five days reads differently from one who has gone quiet, **and without the client's own baseline every slow certification looks identical and the list gets ignored.**

**`fund_request`** — request_id · project_id · requested_by · amount · purpose · state (`requested`/`approved`/`released`/`liquidated`) · **liquidation_due (15 days from release)** · liquidation_documents. **Hard block 6 applies. An unliquidated advance blocks the requester's next request** — refusal 3 — and Finance and Human Resource are informed.

**`write_off`** — write_off_id · subject (`receivable`/`retention`/`stock`/`advance`) · subject_id · project_id · **amount (determines which of gates 1, 2 and 3 applies)** · reason · **recovery_attempts — deliberately optional: a write-off with no recovery history is permitted and is reported. Requiring the field would make the condition unreportable because it could never occur** · requested_by · requested_on · state (`requested`/`approved`/`posted`/`rejected`) · approved_by · approved_on.

**A write-off is irreversible money.** That is why the ladder has three gates rather than one, and why gate 3 has no alternate — **above ₱100,000 there is no authority above the Chief Executive Officer to pass it to. Nothing else in the platform writes value off.**

**`cash_forecast_line`** — month (twelve forward) · direction (`in`/`out`) · **confidence (`secured`/`gated`/`projected`)** · amount · source_object.

**A forecast presenting one number is a forecast nobody can act on.** `secured` — contracted, certified or invoiced; will arrive unless something goes wrong. **`gated` — real money held behind a specific gate, with a named owner and an age.** `projected` — expected but not committed, from the pipeline weighted by stage.

**Gated cash is the band that matters, and every gated line carries the gate, the owner and the age.** *₱4.2 million arrives in March* is a projection. ***₱4.2 million is sitting behind six uncertified claims averaging forty-one days, owned by three people*** is a morning's work. **The second is what this module is for.**

**Three-month cash-gap detection is in scope and is a query:** a projected negative position within three months, valued, with the gated cash that would close it listed first.

**Percentage of completion under Philippine Financial Reporting Standards 15 comes from block value weights** — materials and labour, General Requirements excluded. `earned = contract value × percentage of completion`; `billed = sum of invoiced milestones`; `position = billed − earned`. **Over-billed is a liability. Under-billed is unbilled revenue — money Magnus has earned and not asked for.**

**Cost per block:** material committed at purchase order issue · labour from deployment × `labour_rate` · subcontractor · equipment. **The five percent overrun flag is measured against committed cost, not spend, and must state whether the cause is price or additional items.**

**Markup actual against policy — 115% major equipment, 130% balance of system — is reported by project, client, Director and period.** The risk is not the single large discount, which is visible anyway. **It is a pattern of individually reasonable concessions that only reads as margin erosion when seen together.**

**Foreign exchange variance appears on the project, not inside the margin.**

**Retention is scheduled at contract signature with a stored date. The invoice is raised by a person or an agent reading that date — section 16, deviation D4.** **The platform closes this leak going forward and cannot reach backwards:** projects turned over before the platform existed still require a person to check whether the retention bill was ever issued. **That is cash Magnus may be owed and has not asked for, and no software recovers it.**

**The accounting interface reads at period close and on demand. The reconciliation is the control that makes the sub-ledger trustworthy:** sub-ledger project cost against general ledger project cost, per period, **with the variance shown rather than absorbed.** Without it two systems hold two numbers and nobody knows which is right — which is the position today, with the platform added.

**⚠ Build dependency, still open: whoever maintains the accounting platform must be available when this module is built. That person is not yet named. Do not design the export format around a guess.**

**The Bureau of Internal Revenue Computerized Accounting System registration question stands separately.** Moving off QuickBooks onto a custom platform is very likely the change that requires re-registration. **This exposure exists whether or not this platform is ever built. The platform neither creates nor resolves it.**

## 8.16 Human Resource (module 17)

**THE GOVERNING RULE: operational data informs the conversation. It never produces the rating.**

**Five things the platform must never do:** compute a rating, score or index from task counts, load bands, on-time percentages or grades · **rank people against one another** · track presence, location or activity · convert a score to money by formula · expose engagement survey responses per person.

**Why this is a design constraint and not a policy: once a number becomes the score, people manage the number. Site reports get filed to look good rather than to be accurate — and the site data is what the entire platform depends on.** The first thing to degrade would be the input everything else is built from.

**Evidence is opened, never computed.** A reviewer opens a person's work in the period — deliverables produced, tasks completed, reports filed, and their grades — and reads it. **The platform computes nothing from it and displays no derived figure.**

**Magnus today has neither documented career paths nor compensation bands.** This module can record promotions, salary history, reviews, role history, training and certification now. **The structures for career paths and bands are built and left empty, ready the day Magnus defines them.** Until they exist, the platform cannot tell an employee what they must do to reach the next role — **and that last capability is the one that actually retains people. Defining the paths and the bands is Human Resource work that should run in parallel with the build, not after it. If Magnus never defines them, this section is a filing cabinet** — recorded so that is a known choice rather than a disappointment.

**`employee`** — person_id (extends `person`, never duplicates it) · employment_status (`probationary`/`regular`/`project_based`/`consultant`) · date_hired · **regularization_due** · level · manager · **buddy (named, and never the manager — a new person will ask a peer what they will not ask a manager)**.

**`requisition`** — requisition_id · **resource_request_id — a requisition originates from a declined resource request, not from a manager's judgement that the team feels stretched** · role_title · department · headcount · justification · raised_by · raised_on · state (`draft`/`open`/`filled`/`withdrawn`).

**The hiring instrument is evidence:** arrival against completion, sustained · bench depth · **declined resource requests the platform recorded and nobody could fill.** **The question is never *is this person working hard*. It is *does more work arrive than this team can complete*** — a team-level flow fact that produces no number about any individual. **The same data answers it without ever producing a number about a person. This is why module 13 refuses to compute per-person productivity.**

**`candidate`** — candidate_id · requisition_id · full_name · contact · source · documents · state (`applied`/`screened`/`interviewed`/`offered`/`hired`/`rejected`/`withdrawn`) · **`retention_expiry`, set on creation, never left blank.** A rejected applicant's curriculum vitae is personal data of a non-employee under the Data Privacy Act, with a defined retention period and a deletion path.

**`interview_record`** — interview_record_id · candidate_id · interviewer_id · scheduled_on · scores · written_comment · **`submitted_at` — no interviewer sees another's record until their own is submitted.**

**`offer`** — offer_id · candidate_id · requisition_id · position · salary · start_date · **probationary_end (seeds the regularization diary)** · state (`draft`/`awaiting_approval`/`issued`/`accepted`/`declined`/`lapsed`) · approved_by · approved_on (gate 24).

**`objective`** — person_id · quarter · **objective_text, written by the person, not assigned to them** · references_work. Three to five per quarter. **Objectives reference work, never counts.** *Complete the Sorsogon design package* is an objective; *close forty tasks* is a target that changes behaviour and measures nothing.

**`review`** — person_id · quarter · reviewer · went_well · did_not_go_well · **what_is_in_the_way** · next · rating (`exceeded`/`met`/`developing`/`not_meeting`) · **rating_reasons (required free text, written by a human)**. **There is no `rating_score`, no numeric equivalent and no aggregate anywhere.**

**Quarterly, light form, fifteen minutes. Question three earns the cadence.** It is the only question in a performance conversation whose answer is usually the manager's or the company's problem rather than the employee's — **and it is the question an annual cycle asks eleven months too late.** **The form must be genuinely short**; a quarterly cadence with an annual-sized form is completed properly twice and then becomes a formality. **The cadence and the form are designed together, or the decision defeats itself.**

**Compliance with holding reviews is visible. Ratings are never aggregated into a scoreboard, a distribution, or a ranking.**

**Recognition is peer-visible and never convertible to money by formula.** A recognition scheme with an automatic monetary conversion stops being recognition within one quarter and becomes a currency people optimise.

**`engagement_response`** — survey_period · question · response. **`person_id` is NOT STORED. Not encrypted, not restricted — not stored.** A survey people believe is identifiable returns the answers people think are safe. **The only way to be believed is for the link not to exist, and that is a schema decision, not a policy one.** Four questions, quarterly, anonymous, trended.

**Onboarding:** a pre-arrival checklist completed **before day one, not on it** — equipment, access, personal protective equipment · day one account, roles, capability tags **and a first task** · a named buddy · 30/60/90 check-ins as recurring obligations on the manager · **the probationary and regularization decision, diarised and gated.**

**The regularization decision is diarised, never remembered.** Philippine law attaches consequences to the probationary period and its expiry, **and a decision not made by the date is a decision made by default — the default being regularization.** The decision task appears well before the date and escalates as it approaches.

**Onboarding completion by manager is reported.** A manager whose new hires consistently arrive without equipment or access is a visible fact rather than a rumour.

**Dual career track: a senior engineer must be able to advance without becoming a manager, at equal level and equal band.** This is the single most important structural decision in career design for an engineering company and the one most often got wrong. **Where the only path upward runs through management, the best engineers either leave or become mediocre managers, and the company loses twice.**

**Stay interviews twice a year, diarised, before resignation.** **An exit interview tells you why someone left. A stay interview is the only one that can change the outcome.**

**Exit:** resignation, notice and reason category · **an exit interview not conducted by the person's manager** · offboarding as an access event that blocks on unreassigned work · **knowledge handover as a task with a deliverable, not a conversation** · attrition by tenure, role, region, and regretted against non-regretted.

**Attrition by manager is reported** — the single most informative people metric a company has and almost never looked at — **as a Check for the department head to investigate, never as a manager score. A manager with high attrition may have the hardest team in the company.**

**Employee self-service is the half people actually touch and the half most often built last and worst:** my objectives and capabilities · **my next level and the gap to it, where paths exist** · training and certifications with expiry · leave request and balance · personal detail update · **payslip access** · certificate of employment request. **A platform that makes an employee ask Human Resource for their own leave balance has added a step to their life rather than removed one — and the goal was the best workplace available.**

**A console holder has no access to salary, performance ratings, disciplinary records or medical information. Administering permissions is not a reason to see them.** **Manager salary visibility is off by default and must be explicitly configured, never inherited from managing someone.**

**Statutory questions for counsel, not for the platform to resolve:** probationary and regularization requirements · the deployment record and regularization exposure · Labor Code Article 105 · thirteenth-month pay · statutory leave · Social Security System, PhilHealth and Pag-IBIG obligations · Data Privacy Act retention for employee and candidate data · Department of Labor and Employment inspection records · **the aggregation exposure, because this module concentrates salary, medical, disciplinary and performance data in one place** · the outstanding payroll deduction authorisation.

## 8.17 Payroll (module 18)

**This module contains the highest-consequence rules in the platform. Two carry legal exposure and one carries the company's largest fraud surface. None may be simplified.**

**Magnus builds payroll rather than renting it because payroll already runs on spreadsheets and is compliant** — Magnus already owns the statutory maintenance obligation, and renting would not remove it. **What is new is that the obligation becomes visible, owned and dual-controlled rather than resident in one person's spreadsheet.**

**Separation of duties, preserved exactly as today: Human Resource computes and approves the register; Finance processes payment under gate 23. Neither may do the other's step**, and this must not be "simplified" into one role because one platform now holds both.

**`payroll_period`** — period_id · period_start · period_end · state (`open`/**`blocked_incomplete_reports`**/`computed`/`approved`/`released`/`distributed`/`closed`) · **site_report_completeness (derived)** · **acknowledgement_sheet_document_id** · **acknowledgement_lines_returned (derived)** · computed_by · approved_by · released_by.

**`payroll_line`** — person_id · period_id · **days_worked (from the deployment record and toolbox attendance — not from a clock)** · basic_pay · overtime · allowances · statutory_deductions (computed) · other_deductions · net_pay (computed, never entered) · **rate_table_version** · project_id · project_block_id.

**`statutory_rate_table`** — table_type (Social Security System / PhilHealth / Pag-IBIG / withholding tax) · **brackets — tables and brackets, not a single percentage** · **effective_from / effective_to** · entered_by (Human Resource) · approved_by (Finance) · state (`pending`/`approved`/`superseded`) · legal_reference.

**Philippine statutory contributions are bracket tables, not flat percentages. A rate field alone cannot represent them, and a system built on percentages produces figures that are close and wrong.** The tables are data, configured through the administration screens and through the Model Context Protocol, never written into code.

**A payroll period computes at the rates in force during that period, not at today's rates. Re-opening a March period in November must reproduce March's figures exactly.** Without this every historical payroll silently rewrites itself the moment a rate changes, **which makes every prior remittance unverifiable and every audit unanswerable. `rate_table_version` on each line is what makes this provable rather than merely intended.**

**A named owner carries a recurring obligation to check for statutory changes.** The obligation is a stored recurring definition, not a memory — and not a scheduler.

**THE BOUNDARY, STATED EXACTLY: you may update a rate to what the law now says. You may not override what the law then produces.** Changing a Social Security System bracket table when the law changes it is maintenance; correcting a mis-entered bracket under dual control is maintenance. **Editing the resulting contribution figure on an individual payslip is falsifying a statutory computation. There is no permission level at which the second is available.**

**THE SITE-REPORT BLOCK — "no report, no payroll".** The payroll register for a period cannot be generated while any site day in that period has no site report.

**The block is on the payroll RUN. It is NEVER on an individual worker. No worker is ever dropped from a register.** Escalation is to the Person In Charge and their manager.

**Philippine Labor Code Article 116 makes it unlawful to withhold any amount from a worker's wages without that worker's consent.** A worker who attended the toolbox meeting, worked all day, and is unpaid because their Person In Charge did not file has done nothing wrong and is owed their wages — **dropping them from the register is a wage claim against Magnus for a third party's administrative omission.**

**Landing the block on the run is a strictly stronger version of the same policy.** An unreported day blocks an entire crew's payroll, **which no Person In Charge will let stand** — so the report always arrives, everybody is paid on time, and Magnus carries no Article 116 exposure. **The policy loses nothing and gains enforceability.**

**Attendance comes from the toolbox meeting record on the daily site report. There is no clock-in, no clock-out, no location and no presence capture of any kind.** `days_worked` is a count of days on which a person appears in a toolbox attendance list, evidenced by the toolbox photograph. **This applies to field crews only** — office and management staff are salaried, never appear in a toolbox list by design, **take `days_worked` from the company working calendar, and their pay does not vary with it.**

**Overtime hours are recorded only on days when overtime was actually worked**, because that is the only day on which hours change the pay. **On every other day, the record is the day.** The site-level `working_hours_start`/`_end` on the site report is not a contradiction: those are the hours the site worked, recorded once, attached to no person.

**The headcount variance query reports every site day where the number of people paid does not match the number of attendees recorded.** Every control ships with its verification — **a photograph nobody compares against anything is capture without consequence, and this is the comparison that makes the photograph a control rather than a file.**

**THE ACKNOWLEDGEMENT SHEET IS THE ONLY SECOND PARTY IN THE ENTIRE PAYROLL CHAIN.** The Person In Charge photographs the toolbox meeting, writes the report that determines who is paid, and physically hands over the cash. **One person controls the record, the amount and the money** — and crew members do not sign in, so nothing else independently confirms that a named worker was present and was paid.

The control: the platform produces a printed distribution sheet from the approved register · **each worker signs beside their own amount** · the sheet is photographed and uploaded the same day · it is attached to the payroll period · **a period is not `distributed` until every sheet is returned.** **Cost: paper and a phone. It can start this week, before any software exists.**

**Remove the sheet and one person controls the record, the amount and the money, with the workers' own signatures absent.** That is not a gap in a report — it is the absence of any independent confirmation that the money reached the people named.

**Cutover requires three consecutive payroll cycles matching the existing spreadsheet to the peso.** Not one — **one match can be coincidence; three is a working system.** **Not approximately** — any variance is investigated and explained before the next cycle. **Payroll has monthly, quarterly and annual behaviours — thirteenth-month pay, tax year boundaries, bracket transitions — that a single cycle cannot exercise. A first-cycle match proves the common case works.** After cutover the spreadsheet is retained read-only as the reference for every historical period.

**A console holder has no access to the register, a payslip, or a rate table.** Project Managers and Persons In Charge have none either. **Salary is the most sensitive data in the platform and it must not be reachable by virtue of administering permissions.**

## 8.18 Reporting and measurement (module 19)

**There is no exception engine and no nightly pass — section 16, deviations D2 and D3.** Every exception in the source specification exists here as **a query, evaluated on request, returning its own evaluation timestamp and the number of rules it evaluated.** An agent reads them, ranks them, and decides what matters.

**Silence must never be ambiguous.** Every query returns either results or an explicit statement of what was checked and when — *Cash — checked 09:14, twelve rules, no exceptions.* **A dashboard that shows nothing may mean nothing is wrong, or that the check did not run, or that the data did not arrive, or that the rule was never built. An executive cannot tell the difference, and after the first time silence turns out to have meant "broken", it is never trusted again.**

**Every exception row a query returns carries four things:** what (the fact) · **who — a named person who can act, never a department** · how long (age) · **so what — the consequence, valued wherever a value exists.** *Permit outstanding on Sorsogon* is a status. ***Permit outstanding 61 days; crews cannot mobilise; ₱1.4 million of programme sitting idle; Jeferson*** is a decision. **"So what" is what separates an exception list from a list of complaints.**

**Drill path, always available from any exception: exception → domain → record → audit log.** An exception a person cannot drill into is a rumour with a number attached, **and the second question after *what is wrong* is always *since when, and who changed it.*** Every level respects `record_scope` and `money_visibility`.

**Six domains:** Projects · Cash · People · Safety · Permits · Operations and maintenance (Phase A: underperforming sites **ranked by estimated lost generation valued at that site's tariff — never by a severity label. A string offline on a 5 megawatt-peak plant and an inverter down on a 6.5 kilowatt-peak residential system are not the same event.**).

**Role scoping:** Chief Executive Officer and Chief Operating Officer — all six domains company-wide · Director — own projects plus company-wide safety and cash · Head of Finance — cash and permits company-wide · Project Manager — own projects only · Safety Officer — safety company-wide · Human Resource — people company-wide. **Money visibility applies independently.**

**`measure_register`** — measure · source records · **owner (a named person)** · cadence · **the decision it informs (required — the platform refuses to save a measure without one)**.

**A measure with no decision attached is deleted, not archived.** *"What we can measure, we can control"* has a second half usually dropped: **measurement is control only where someone acts on it.** A measure nobody acts on is not control — **it is cost: the cost of capturing it, the cost of reading past it, and the cost of the confidence it creates that something is being managed.** The register forces the question at the point a measure is created: **whose decision does this change?**

**`report_register`** — every standing report, by module, with its owner and cadence. **A standing report nobody reads is removed.**

**FOUR GAMING GUARDS — restated here because this is where they are most likely to be quietly broken by good intentions:**

1. **Load is banded, never scored, and never an appraisal input.**
2. **Grades attach to deliverables, not to persons. No aggregate per-person score exists.**
3. **Reporter identity is never shown.**
4. **Safety indicators are never a personal performance score.**

**Every one of these will look like a missing feature to someone building a dashboard.** *Surely the Chief Executive should see who reports the most near misses.* **No — that is how near-miss reporting stops.**

**The person with no assigned task reaches the People domain as a count across managers, never as a named individual on an executive screen.**

**The board pack is generated from platform data on request, never assembled by hand.** Magnus's monthly report is currently reconstructed by hand and carried eight arithmetic errors in July; generation removes an entire class of error and several days of work.

## 8.19 Administration (module 21)

**The single place everything in the platform is configured, with the right authority, without a code change.**

**Configurable:** system constants (gate 22, Chief Executive Officer only, effective-dated) · approximately thirty operational thresholds (gate 31) · approval gate limits, primaries, alternates and windows (**alternate authority validated at save**) · **hard block values only** · roles, permissions and money visibility (gate 32) · labels and terminology · the push list (**additions permitted; the three cannot be removed**) · landing screens per role · retention schedules and legal hold · statutory rate tables (**Human Resource enters, Finance approves**).

**NOT configurable, by any permission level, screen, protocol call or database route:**

1. **The audit log cannot be made editable.**
2. **Statutory calculation RESULTS cannot be overridden.**
3. **Tenant isolation cannot be disabled.**
4. **The EXISTENCE of any of the six hard blocks.**

**Hard blocks appear on the console as read-only rows with their configured value editable and no enable, disable, delete or bypass control of any kind.** Do not add one for symmetry with the gate screen. **Every attempt to disable one is logged, including attempts that fail — which is all of them.**

**Every configuration change is logged with what changed, previous value, new value, who, when, reason where required, and the arrival channel.** System constants, hard block values, approval gate limits and statutory rates all require a reason. **It costs one sentence, and in a year it is the difference between knowing why the yield figure moved and guessing.**

**The threshold churn query shows which thresholds move most often.** A threshold that keeps firing is annoying, and **the cheapest way to stop the annoyance is to move the number rather than fix the problem — after which the platform looks calm while nothing has improved.** Reporting every change makes loosening visible as loosening. No friction is added to legitimate tuning.

**The recorded concentration:** the Chief Executive Officer is both a console holder and the top approver on the high-value gates, **so one person can raise an approval limit and approve against it. In a company of sixty this is accepted, and it is accepted knowingly rather than unnoticed.** Two things keep it visible: the quarterly access review, and **a weekly console change digest to a second named person — recommended Finance, who already holds the second half of the dual control on statutory rates. It costs nothing and changes no permission. Without it, the audit trail on the highest-privilege actions in the platform is written and never read** — capture without consequence at the most sensitive point in the system, committed by the module whose job is to prevent it everywhere else. *In this build the digest is a query an agent delivers, not a scheduled mail.*

**Three disciplines, from day one:**

1. **Magnus's configuration and the platform's capability are separate things. Magnus is a row of configuration, not assumptions in the code.**
2. **No Magnus-specific literal anywhere in the codebase.**
3. **A second configuration profile exists in test from early on — an invented engineering, procurement and construction company with different stages, thresholds and roles.**

**Discipline 3 is the cheapest and most reliable multi-tenancy test that exists. If the platform cannot run the invented second company, it is not a product — it is Magnus's internal tool with a `tenant_id` column.** That difference is discovered either now, for the cost of one test profile, or later, for the cost of a rebuild.

**The block spine is the deliberate exception. It is identical for every tenant and is not configurable.**

**Configuration is a governance act, one change at a time, each with a reason. There is no bulk configuration import.**

## 8.20 Data, security and compliance (module 22)

**The obligations are Magnus's, not a vendor's.** Wherever the data physically sits, Magnus is the personal information controller for employee salaries, candidate curricula vitae and client personal data.

**The platform concentrates sensitive data that is currently scattered.** Salary, medical, disciplinary, performance and client commercial data in one place is a materially different exposure from the same data across eight accounts and a spreadsheet — **better controlled, and worth more to lose.** Mitigations, reviewable as a set: console holders have no access to salary, ratings, disciplinary or medical data · engagement responses store no `person_id` · reporter identity never appears in any dashboard · money visibility is a separate permission axis · quarterly access review · cryptographic erasure.

**Backup: automated, encrypted, per tenant. Restore: tested, on a schedule, to a working system, with date, duration and outcome recorded and reported to the console holders.** **An untested backup is not a backup. It is a belief.** The failure mode is not that backups are absent — **it is that they run for two years and nobody has ever restored one, so nobody knows the restore takes eleven hours, or omits attachments, or fails. That is discovered on the day it matters, which is the worst possible day to discover it.** The restore test is a stored recurring obligation with a named owner.

**Magnus can export its own data in full, at any time, in a documented, re-importable format.** The strategic case for building rather than renting is that the platform is an asset on Magnus's balance sheet. **An asset whose data cannot be extracted is not an asset — it is a dependency. The export path is what makes the ownership real, and it is also the answer to the only serious question an acquirer or an investor will ask about the technology.** Export is logged and respects the exporter's permissions. **Build and test it now, not promised for later.**

**Retention schedules are `[CONFIGURED]`, pending counsel. Do not invent retention periods, and do not take a platform position on regulatory sufficiency.**

**A security review is required before any outside tenant is admitted** — not before internal go-live, where identity is delegated and the platform is internal.

## 8.21 Integrations and accumulated reference data (module 24)

**The accounting system: the platform READS. It does not write.** Period close and on demand. The reconciliation shows the variance rather than absorbing it.

**Government channels: the platform produces the remittance figures. It does not file.** Bureau of Internal Revenue, Social Security System, PhilHealth, Pag-IBIG, and the Department of Labor and Employment online compliance portal. **It holds the deadline, records the reference once a person has filed, and stops there. Filing is a person's act, and the platform must not appear to have filed anything.**

**No outbound electronic mail, for anything, including summaries and digests.** The only outward delivery is the device push carve-out in section 1.1.

**Generation monitoring** fields exist from the first release, populated for company-owned lease and independent power producer assets and empty for handed-over projects. **Magnus currently has no performance visibility on systems it built and handed over; the field is where that changes when the data becomes available, and it does not require the integration to exist first.**

**Electronic signature** where a counterparty requires it — not a platform-wide signing mechanism. **Electronic wallet payroll is deferred**: it would remove the cash distribution exposure entirely but depends on crews holding accounts and on site connectivity. **Recorded as the structural fix, not scheduled.**

**Import path: one-time, for migration.** Master data with aliases · opening stock balances · active projects with blocks, value weights and workday counters. **Every import is logged and reversible before the opening balance lock. After the lock it is not.**

**ACCUMULATED REFERENCE DATA — there must be no administrative screen for maintaining any of the following.** An administrative screen for maintainable reference data is a screen nobody updates, holding numbers that are wrong within a quarter — **and worse than absent, because people trust them. Build the accumulation. Not the screen.**

Price history by item · actual supplier lead time · supplier performance · block cycle time · **permit duration per local government unit** · **permit requirements per office with times observed** · permit fees per type and office · consultant engagements per office · **actual yield, which is eventually the evidence behind the 1,277 assumption** · **client certification behaviour** · client payment behaviour · **structural outcome history — assessment confidence against certification result** · **resource demand: requested, allocated, declined by reason** · arrival against completion by team · time to hire and **source effectiveness at twelve months, not people hired** · attrition by tenure, role, region and manager · off-design purchase rate · checklist item failure rates · threshold churn · approval turnaround and pass-down.

**Every accumulated figure is presented with its sample size** — *median 62 days, from 4 observations*, never *62 days* — and **falls back to the documented default where history is insufficient. Never presented as certainty.** **A median from four observations and a median from forty are different kinds of statement, and a platform that presents them identically teaches people to distrust both.** Show the count; let the reader decide how much weight it carries.

**This section is the platform's compounding value.** Magnus today prices new territory by guessing, estimates permit durations by memory and judges suppliers by impression — **none of that is a failure of judgement; it is the absence of accumulated evidence.** The modules deliver from day one; this delivers from month twelve, and keeps delivering.

## 8.22 Migration and cutover (module 25)

**More platforms fail at cutover than fail at build.** Everything else can be correct and the platform still fails here, for reasons that are not technical: **a parallel channel left open, an opening balance that was wrong, a store people kept using, a Person In Charge whose first photograph failed.**

**Two rules govern this entirely:**

1. **Nothing is authoritative until its predecessor is frozen.** A channel that still works is a channel people keep using.
2. **Nothing is loaded that nobody will maintain.** A migrated record that is wrong on day one is worse than an absent one, because people trust it.

**Not migrated:** finished projects' documents (remain in Google Workspace, searchable) · finished projects' Messenger history (archived and searchable, nothing extracted) · historical accounting (stays in the accounting system) · the four hundred gigabyte archive (**triaged, not absorbed**). **Attempting to migrate everything consumes the build. Live projects come across; finished projects stay where they are.**

**Master data load: people with aliases · equipment with a named custodian each · items with unit of measure and serialised flag · suppliers with taxpayer identification and accreditation state · clients, sites and contacts, with sites separate from accounts.**

**Active project load: project and contract · blocks with include flags · value weights from the costed bill of materials · workday counters seeded** (without seeding, every migrated project appears to have begun on cutover day and every cycle-time figure for the first year is wrong) · current block states and percentage complete **derived from the loaded position, never typed** · open purchase orders and committed cost · open permits with expected approval dates.

**Every live project's signed contract is uploaded before it can become active. Retention terms are read out of each one.**

**Document triage: every live project's documents come across before go-live · classification under gate 33 · old locations made read-only by the Workspace administrator on the cutover date · an exception list naming anything not classified or migrated, with a reason.** **A known gap is manageable; an unknown one is discovered on site.** This is real preparation work sitting before the build, on the critical path, **and it is the kind of work assumed into someone's spare time. Cristy needs a date and, quite possibly, help.**

**Communication cutover: a live project moved mid-flight, chosen for speed rather than waiting for a new project to start.** Field-test the photograph path first · extract the pilot's Messenger history as the operating state, not a transcript · move the team · **rename the pilot's Messenger group and make it read-only** · run several weeks and fix what breaks · remaining projects follow on a named date. **A channel that still works is a channel people keep using, and the pilot then proves only that people prefer what they already know. A half-migrated team is worse than either end state.**

**Freezing, not deleting:** payroll spreadsheet retained read-only after three matching cycles · pilot Messenger group read-only · **document stores read-only on the cutover date** · accounting system continues. **Freezing removes the temptation to keep using it. Deleting removes the ability to check it — and in the first year, checking is exactly what builds trust in the new numbers.**

**Training by role. The Person In Charge's is the longest and the most important — on their own phone, on site, offline behaviour included.**

**What is said to staff at rollout, in plain words, and this is part of the deliverable:**

- **The workload you register is never used in your appraisal.**
- **No number the platform produces will decide your rating.**
- **The platform does not track where you are or when you log in.**

**Staff behaviour follows what they believe, not what is true.** Unstated, people under-register — **and the task and site data, which everything else is built on, goes hollow.**

---

# 9. MOBILE AND FIELD — THE PART ON WHICH THE PLATFORM SUCCEEDS OR FAILS

Every other part can be excellent and the platform still dies here. **The Person In Charge is the only site user** and is the source of the site report, the toolbox attendance record, the payroll attendance, the block progress, and the photographs that carry all of it.

**If the mobile path fails silently once — one delivery photograph that appears to upload and does not — that person returns to Facebook Messenger permanently and does not come back. A director testing from an office will never discover it.**

**Deliver as a progressive web application, not a native store application.** No store approval on the critical path, no install friction, no two codebases, and updates reach every device the next time it opens. **The decisive argument is not cost — it is that a fix reaching a Person In Charge in Sorsogon must not wait on a store review.** In the first months there will be fixes, and the interval between finding one and the field having it is the interval in which people go back to Messenger.

**Field users CREATE records offline. Field users do NOT EDIT shared records offline.** Creation never conflicts; editing does. **This single restriction removes the great majority of synchronisation complexity at almost no cost in real capability** — a Person In Charge on a roof is recording what happened, not amending someone else's record.

**No approvals offline, ever. Capture offline; decide online.** An approval given against a cached state that has since changed is a decision made on information that was already wrong — **and it carries a human's name, so it is indistinguishable from a considered judgement.**

**Photographs:** in-app capture only, **never from the device gallery** — a gallery photograph has no reliable date, place or provenance, and the toolbox photograph is attendance evidence in a payroll chain. **Never written to the device gallery** — once there it is outside company control permanently and synchronises to a personal cloud account, including client site data. Compressed on the device (mandatory, not an optimisation), queued, resumable upload, **original retained until synchronisation is confirmed**, text before attachments.

**Failure must be visible.** A failed or pending upload is shown to the Person In Charge with a retry and is never silently dropped. **A silent failure is worse than a visible one: the person believes the record is filed, the report shows as incomplete days later, and the trust cost lands on the platform rather than on the connection. Show the queue. Show what has not gone.**

**Nothing captured in the field is ever discarded by the platform.** Someone stood on a roof and recorded it. A record that cannot be synchronised is **retained on the device and shown as unsent, indefinitely.** A record whose parent has since changed is **accepted and flagged for review, never rejected silently.** A record whose parent has been deleted is **held and raised as a Check.** **Nothing is resolved by deletion.** Two creations of the same logical record are de-duplicated by the device-generated key.

**Sizing:** ten to twenty-five photographs per daily report at approximately 300 kilobytes each, across roughly twelve active projects — **approximately 72 megabytes per working day, 1.5 gigabytes per month, 18 gigabytes per year of site photography alone.** Uncompressed the same volume is roughly ten times larger. **The platform reports actual storage growth per project**, so the cost appears as a visible line rather than a surprise in month eight.

**Data allowance is a real cost to a real person.** Persons In Charge upload from personally owned phones on personal data allowances. **This is the most likely cause of late or missing reports, and it is not a technical problem. A person who is paying to file the company's records will file fewer of them.** Compression reduces it; it does not remove it. **Magnus should decide how the data cost is covered — a small operating cost against a report that now blocks a payroll run.**

**Low-signal behaviour:** the application opens and works with no connection, with today's work cached · text before attachments · background retry with backoff · **the queue is visible** · **the site emergency card works offline.**

**What a Person In Charge actually opens — the Today screen:** site report status · toolbox meeting with the topic proposed from today's permits to work and recent near misses · deployment for the day · open permits to work · deliveries expected today · **the upload queue.**

**FIELD-TEST THIS PATH BEFORE BUILDING ANY INTERFACE ON TOP OF IT.** A Person In Charge, on a real rooftop, on real Bicol or Sorsogon signal, capturing a photograph and filing a report — offline queue, retry, compression, background upload, visible queue. **Not a developer on office wifi. Not a director with a demonstration. The actual person, the actual site, the actual signal.**

---

# 10. PERSONAL DEVICES AND REVOCATION

All field users work on personally owned phones. **The company does not own them and will never wipe them.** The application holds a working cache and an offline queue only — no permanent local copy of company data. **On revocation the cache becomes unreadable and the account is dead. Server-side revocation is the entire security control.** Device management applies to company-owned laptops only.

---

# 11. THE ACCESS LIFECYCLE

**Onboarding:** Human Resource creates the person record · department head assigns roles under gate 24 · the identity provider account is created outside the platform and linked by `identity_subject` · capability tags assigned by the department head · **the person appears in the platform only after roles are assigned. A record with no role has no access at all, rather than default access.**

**Role change or transfer:** the old `person_role` closes with an `effective_to` date and a new row is added. `record_scope` values of `department` and `region` follow the current role, **which means access to the previous department's records ends on the effective date. Flag this to the person's manager before it takes effect** — a transfer that silently removes access to work still in progress is discovered as a fault rather than as a policy.

**Departure, and the order matters:** identity provider account disabled → person moves to `suspended` automatically · Human Resource sets `departed` · **every open task, approval and deliverable owned by that person is listed and must be reassigned — the platform blocks the completion of offboarding, it does not merely warn** · console holder status removed, with a replacement named first if held · device cache becomes unreadable · **the person record is retained. Nothing is deleted.**

**Step three is the one usually skipped and the one that matters.** A departure that leaves approvals owned by a disabled account creates gates nobody can pass and work nobody can find.

**Quarterly access review under gate 32:** per person, current roles, the permissions those roles grant, **and what that person has actually used in the period.** Console holders review and remove what is no longer needed. **Permission changes are made in a hurry because someone needs access to finish something today, and hurried grants are how access quietly accumulates on people who no longer need it — nothing ever removes it, because removal is nobody's task.** The review makes it somebody's task on a schedule.

---

# 12. THE MODEL CONTEXT PROTOCOL SERVER — THE SECOND PRODUCT SURFACE

This is not an add-on. **It is how the platform is operated, monitored and configured.** Build it to the same standard as the user interface and expose through it everything a person can see or do on a screen.

**The server has no permissions of its own. It has the permissions of the authenticated person, and no more.**

## 12.1 Authentication, scoping and audit

- The connecting person authenticates as themselves against the tenant's identity provider. **There is no service account, no platform identity, and no "changed by the assistant". Every action carries a human being's name.**
- Every call is tenant-scoped by the same database row-level policies that scope the interface.
- **Scope at the query layer, never by filtering an answer after computation.** An answer filtered after the fact has already read the data. An assistant answering *what is our margin on the Del Monte project* for a person with `money_visibility` of `none` has defeated every permission in one sentence — **and nobody would know, because the answer looks helpful.**
- **It refuses rather than estimates.** Where the data does not support an answer, it says so.
- **Every figure returned cites the records it came from.** An answer with no source records is not an answer the platform gives.
- Every call is written to the audit log with `arrival_channel` of `model_context_protocol` — who, when, what was read or written.

## 12.2 Read tools

Expose list, get and search for **every object in section 8**, plus these computed reads, evaluated on request and each returning its own evaluation timestamp and rule count:

Percentage complete per block and per project against the planned curve · material readiness by block across all active projects, with the date each becomes startable · blocks not startable with mobilisation planned · projects with no submitted site report in the last two working days · site report compliance by Person In Charge · **approval requests pending, with age in working days and the recorded window** · blocked activities with reason and expected clear date · cumulative days lost by blocked reason and responsible party · weather stoppage days per project · non-conformance reports open, with ageing and same-day closure rate · design deliverables waiting, split by party waited on, with cumulative days per party · sealing engineer turnaround · designs sealed under a licence later found lapsed · design capacity against contract capacity · **the twelve-month cash forecast in three confidence bands, every gated line naming its gate, owner and age** · projected negative cash position within three months, valued, with the gated cash that would close it · claims uncertified beyond thirty days with the client's own average certification time · receivables ageing · retention receivable scheduled, due and overdue · retention, warranty and operations obligations becoming due within N days · over- and under-billing by project · committed cost against block budget with the five percent flag stating price or additional items · cost and margin per block and per project · markup actual against policy by client, Director and period · foreign exchange variance by project · off-design purchase rate by project and block · purchase orders committing 50% or more of a block budget · supplier on-time delivery, fill rate, damage rate and actual lead time · supplier bank detail change register · price movement by item · stock by location including in transit and site stock · transmittals in transit beyond expected days · transmittal reconciliation sent against received · quarantined material by value, age and reason · count variance by warehouse and custodian with closing-reason distribution · material issued by project and block · permits past their expected approval date · prerequisite permits outstanding · closeout permits blocking final billing, valued · follow-ups required per office · permit duration, requirement and fee accumulation per office with sample sizes · safety stops open · incidents open · permits to work issued by type and open past validity · workers with lapsed training named on a permit · corrective actions open, overdue, and closed without evidence · **the thirteen safety indicators once the manual is supplied** · near-miss to incident ratio · hierarchy of controls distribution · checklist item failure rates · Construction Safety and Health Program status by project · subcontractor accreditation and insurance with exclusions · resource availability with release dates · **resource requests declined by reason, never as a single combined rate** · requests unfulfilled past their needed-from date · deployment variance across all three layers · roster continuity conflicts · equipment utilisation · capabilities held by fewer than two people on a critical path · certifications expiring within N days · **people with no assigned task, as a count across managers** · output type by department · commitment reliability by team · blocked task ageing by blocker and reason · load bands by team · open assignment board depth · objects with no thread activity on active projects · mention response time by team · messages converted to tasks · channel versus object thread ratio · required-document register per project · documents missing where they gate something · unclassified backlog and age · acknowledgements outstanding by revision · documents overdue for review · superseded revisions accessed · headcount by department, region and employment basis · new headcount cost against budget · attrition by tenure, role, region and manager · time to hire and source effectiveness at twelve months · onboarding completion by manager · review-held compliance · engagement trended in aggregate · regularization decisions due · site days blocking the payroll register · paid headcount against toolbox attendance variance · acknowledgement sheets outstanding · statutory rate change history · parallel run variance by cycle · statutory remittance summary per agency per period · sub-ledger to general ledger variance · contracts signed without counsel review · risk-term exposure by clause family and contracts with unread families · client obligations outstanding · related-party contract register · pipeline by stage, capacity and value · markup and discounting patterns · win and loss by reason · contingency carried per client · structural confidence against later reinforcement variations · hard block attempts · threshold change history · console change history · access review status · restore test record · legal holds in force · export history · retention status by class · **the audit chain verification result**.

**These are queries, not alerts.** The platform computes them when asked and does nothing with them. **An agent asks, decides what matters, and writes a notification or a task back through the write tools.**

## 12.3 Write tools

Create and update for every object; submit an approval decision on any pending request — always as the authenticated person and always subject to that person's permissions.

## 12.4 Configuration tools

Everything the administration screens configure: thresholds · gate limits, primaries, alternates and windows · roles, permissions and money visibility · labels and terminology · controlled lists · the push list · landing screens · retention schedules and legal hold · system constants · **statutory rates and tables**.

**Seven rules govern every configuration write, and all seven are mandatory:**

1. **Authenticated as a person.** The change carries a human's name.
2. **Same authority as the screen.** If that person cannot change a threshold on the console, they cannot change it here.
3. **Same gates apply.** Gate 22 for system constants, gate 31 for thresholds, gate 32 for permissions, dual control for statutory rates. **No gate is relaxed because the change arrived over this interface.**
4. **Confirmation before applying.** The proposed change is stated back in full and confirmed by the person before anything is written. *Raise the receivable threshold a bit* must become **"Change overdue receivable escalation from 30 days to 45 days. Confirm?"** before a single byte is written. **Natural language is ambiguous and configuration is not. A configuration change inferred from an ambiguous instruction and applied silently is the worst failure this interface can produce, because it looks like it worked.**
5. **Reason recorded** where the field requires one.
6. **Logged identically to a screen change**, plus the arrival channel. **A change made here and the same change made on the screen must be indistinguishable in every respect except that one recorded fact.**
7. **Effective dating preserved.** A constant or rate changed here carries its effective date exactly as on the screen.

**Statutory rates ARE writable here, deliberately, under the same dual control as the screen.** This is the answer to the objection that building payroll means maintaining statutory tables forever: it does — **and the maintenance is a conversation rather than a code change. That is what makes the build-versus-rent decision hold.**

## 12.5 Never writable by any client

Not through the Model Context Protocol, not through the screens, not through the database, not at any permission level:

1. **The audit log.**
2. **Statutory calculation results.**
3. **Tenant isolation.**
4. **The existence of any of the six hard blocks.** Values inside them are configurable; their existence is not.

**Enumerate every tool and every parameter the server exposes and prove that none of them, in any combination, can disable a hard block. This is the single most important test in the build.**

**External clients — Claude Desktop, Claude Code, and any agent runtime — each authenticate as a person, are tenant-scoped, and are audited identically. No client has elevated authority by virtue of being a different client.**

---

# 13. SCREENS

Every screen is a view of section 8. Keep the interface thin.

**Foundation:** sign-in (identity provider redirect only) · notification inbox (complete, unranked, uncapped, four categories) · global search · **My Approvals** — one list, every gate, sorted by age, each row showing what, which gate, the value or condition that triggered it, who raised it, how long it has waited and the recorded window for the gate · **approval detail — the object being approved, in full. The approver must be able to see what they are approving without navigating away, or they will approve without reading** · Today (the Person In Charge landing screen) · My Day (tasks).

**Pipeline:** accounts, sites and contacts · opportunity list and record · site assessment capture · proposal builder and version history.

**Projects:** project list and record with contract, risk terms, project parties, variation orders, blocks, documents, permits and tasks · block detail with activities, photographs, state, dependencies and material readiness · portfolio views.

**Design:** design package with the nine deliverables and their waiting states · bill of materials grouped by block · seal record with licence validity.

**Procurement:** the buying checklist (the bill of materials, grouped by block, showing what to buy, quantity, specification, status and expected arrival) · purchase orders · goods receipts · party register with bank change control.

**Site:** **site report capture — offline-first, pre-populated from yesterday, toolbox meeting required with photograph and named attendees, every activity bound to a block. This is the most important screen in the platform and the one most likely to be abandoned if it is slow** · site report list (filed, late, missing, by project and by Person In Charge) · non-conformance reports · Turnover Document.

**Permits:** permit register per project · requirement library per office, read-only.

**Inventory:** stock by location including in transit and site stock · transmittal capture and receipt with signature · physical counts and adjustments · quarantine.

**People and equipment:** resource availability with release dates · resource requests · deployment with all three layers shown · equipment register.

**Safety:** permits to work · incidents and near misses · safety stops · corrective actions · inspections · the offline emergency card · **the per-site Quick Response near-miss and stop-work form, no login.**

**Work:** task lists · document library with classification, revisions and the governing revision marked · threads on every object · channels.

**Money:** billing milestones · progress claims with claimed and certified shown separately · fund requests · write-offs · cash forecast in three bands · sub-ledger reconciliation.

**People (Human Resource):** employee record · requisitions, candidates, interviews, offers · objectives and quarterly reviews · **employee self-service** · payroll periods, register, statutory rate tables, acknowledgement sheets.

**Administration:** tenant · system constants with effective dates, history and reasons · configuration values · thresholds by domain · approval gates · **hard block rows, read-only with values editable and no enable control** · roles and permissions · access review · labels · push list with the three shown as non-removable · change log with arrival channel · **audit chain verification** · read-only audit log view.

**A blocked-action message names the block, the unmet condition, what releases it and who can supply it — never "you do not have permission."**

**No salary, performance rating, disciplinary record or medical data appears on any screen outside module 17, and a console holder has no access to them by virtue of administering permissions.**

---

# 14. ACCEPTANCE TESTS

**The build is not done until all of these pass. None is visible in a demonstration and none will be revealed by clicking through the screens.** Turn them into a test suite that runs, not prose that is read.

## The seven that decide whether the platform is fit for use

1. **The audit log is genuinely immutable.** Alter an entry using direct database access. The verification routine must report a broken chain.
2. **Tenant isolation is enforced at row level.** Write a query with no application-layer filter. It must return nothing belonging to another tenant.
3. **Offline capture preserves creation time and survives reconnection.** Create records offline, reconnect after a delay, confirm both timestamps and that no record is lost or duplicated.
4. **Percentage-of-completion and payroll calculations are correct.** Verify against manually computed cases. The platform will produce a number; **the test is whether it is the right number.**
5. **Cryptographic erasure works over the immutable log.** Erase a data subject; content unrecoverable, chain still verifies.
6. **Effective dating on system constants.** Build a record, change a constant, reopen the record — it shows the value it was built with. Build a new record — it uses the new value.
7. **A hard block cannot be disabled.** Attempt to switch off each of the six from the administration screen, from the database, by permission escalation, **and through the Model Context Protocol.** All four routes must fail, for all six blocks, and every attempt must be logged.

## The test of this entire specification

8. **Nothing runs unattended.** Deploy, leave the platform for twenty-four hours with no user and no agent connected. **Nothing must have changed:** no notification created, no state advanced, no approval moved, no invoice raised, no task generated, no escalation fired. Inspect the audit log to confirm it is empty for that period. **If anything happened at all, you built automation that must be removed.**

## Governance

9. **No auto-approval.** Let every gate sit indefinitely. No request reaches `approved`.
10. **Alternate authority refusal.** Attempt to save an alternate with a lower limit than the primary. **Save must fail — a warning is not a pass.**
11. **Self-approval.** Give one person both requester and approver roles. Their request is offered to the alternate and logged as such.
12. **Block precedes gate.** Trigger an action that is both hard-blocked and gated. **No approval request is created.**
13. **Gate 10 distinguishes two outcomes.** A contract proceeding without review records `proceeded_without_review`, never `approved`, and appears in the counsel query.
14. **Gate 25 splits correctly.** A ₱30,000 inter-island transfer requires approval; a ₱30,000 within-island transfer does not.
15. **No module implements its own approval.** Code review: search for approval logic outside the engine. There must be none.
16. **Hard block table has no `active` column**, and no enable, disable or delete control exists on any screen.
17. **Blocked-action message.** Trigger each hard block. The message names the block, the unmet condition, what releases it and who can supply it — **and never says "you do not have permission."**
18. **Gate 18 has no alternate.** Let a seal sit indefinitely. It never passes down and is never auto-approved.

## Identity and permissions

19. **Multi-role union.** Two roles with different permissions produce the union, and the approval limit is the higher, never the sum.
20. **Money visibility is independent.** `record_scope` = `project` with `money_visibility` = `none` sees the full material list and **no cost figure anywhere, including in exports and printed views.**
21. **Identity revocation.** Disable the provider account. The session ends and cannot be resumed, with no administrator action.
22. **Console holder count.** Attempt a third holder and removal of the second. Both fail.
23. **Crew are not users.** A person with `signs_in` false has no `identity_subject`, appears in deployment and payroll, and cannot be granted a session.
24. **Offboarding blocks on open work.** Attempt to complete offboarding for a person holding an open approval. It must refuse and list the item.
25. **Console holder is excluded from Human Resource and payroll data.** Attempt to view salary, a rating, a disciplinary record, the payroll register, a payslip or a rate table. All must fail.
26. **Role history survives.** Deactivate a role referenced by a historical approval. The historical record still displays the role name correctly.

## Pipeline and contract

27. **Site is separate from account.** One account with eleven sites in different local government units, each carrying its own assessment and permit history.
28. **Sizing references the constant.** Change the specific yield. New proposals use the new value; existing proposals retain the value they were built with, and the version used is retrievable.
29. **Contingency never leaves.** Export and print a proposal in every available format. The contingency percentage appears in none of them.
30. **Winning version is frozen.** Win an opportunity, then attempt to edit the winning proposal. Must fail.
31. **Gate 6 applies to every quotation.** A ₱50,000 quotation still requires Director approval.
32. **Gate 7 band.** Price at 112% major equipment — a Director may approve. Price at 108% — Chief Executive Officer only, no pass-down.
33. **Loss reason above ₱10,000,000.** Close a ₱12,000,000 opportunity as lost with no reason. Must fail. *Did not proceed* is reported separately from *lost to a competitor*.
34. **Won does not mean active.** The project is created in `setup` and cannot become active without the signed contract.
35. **Hard block 6 blocks purchase orders, not only payments.** Raise a purchase order on a contractless project. Must fail.
36. **A tick-box does not satisfy a document block.** Set every contract field except `signed_document`; the block must still hold. Same for the insurance certificate.
37. **Unread is not absent.** A contract with unpopulated risk terms reports as `not_yet_read`, never as having no such clause.
38. **No stored phase.** Confirm no `phase` column exists. A project with blocks in three stages displays a distribution.
39. **Variation does not overwrite.** The original contract is intact; value weights re-base only on `accepted`.
40. **One date, three clocks.** Enter a turnover date. Retention, warranty and operations obligations all start from it, with no second entry anywhere.
41. **Portfolio total crosses record scope.** The all-active view returns count, capacity, value and progress for every active project regardless of the viewer's assignments, subject only to money visibility.

## Design, procurement and site

42. **One bill of materials, two views.** Confirm no second procurement table exists.
43. **Every bill of materials line has a block.** Must fail without one.
44. **Seal attaches to a revision.** Seal revision 3, create revision 4 — revision 4 is unsealed and cannot be released for permitting.
45. **Retrospective licence check.** Enter a licence expiry earlier than an existing seal date. Every affected design is flagged.
46. **Waiting is never anonymous.** Every deliverable in `waiting` has both `waiting_on` and `waiting_since`, and cumulative client days are the sum of all waiting periods.
47. **Ordered lines are not silently changed.** Revise a design altering an `ordered` line. The platform flags the conflict and requires a decision; it does not edit the line.
48. **Reinforcement raises a variation, not a task.**
49. **Weights exclude General Requirements**, and re-base only on an accepted variation — a cost correction alone moves nothing.
50. **Capacity difference is visible.** Design capacity below contract capacity: both shown, neither overwritten.
51. **Expected arrival is required.** Move a line to `ordered` with no arrival date. Must fail.
52. **Block readiness is computed.** Receive all but one line: the block is `partially_ready` and carries the outstanding line's arrival date.
53. **Committed cost begins at issue.** Issue a purchase order, pay nothing — committed cost against the block increases immediately.
54. **Overrun states its kind.** An overrun by price and one by extra items are distinguishable.
55. **Partial delivery.** Receive half a line: the line stays open, the balance keeps its own arrival date, the block is not ready.
56. **Off-design is recorded, not absorbed.** A reason and a block are required, and it appears in the off-design query.
57. **Bank change control.** Change a party's bank details: a second person must confirm, previous values are retained, and the next payment is flagged.
58. **No manual supplier score.** Confirm no screen exists for rating a supplier.
59. **Foreign exchange variance.** Quote at one rate, buy at another: margin is unaffected; the difference appears as a variance.
60. **Non-conformance quarantines.** Receive a damaged item: the material is quarantined and hard block 5 prevents its issue.
61. **No typed percentage.** Search the entire platform for any field where a person enters a project percentage complete. **There must be none.**
62. **Every activity has a block.** Save a site report activity with no block. Must fail.
63. **General Requirements has no weight.** With all construction blocks complete and permits open, the construction curve reads one hundred percent.
64. **Hard block 3.** Attempt to start B1 with B0 unsigned. Must fail and be logged.
65. **Toolbox meeting required, attendees named.** Submit a report with no toolbox record — must fail. Confirm `attendees` holds person references, not an integer.
66. **Headcount variance is reported.** Pay for eight, record six attendees: the variance appears to the Project Manager and Finance.
67. **Variation shows before and after.** Both percentages display on an accepted variation.
68. **The spine is not configurable.** As console holder, attempt to add, remove or rename a block code. All must fail.
69. **Blocked material carries a date** automatically from the outstanding purchase order line.
70. **Weather stoppage is retained** as dated evidence attributed to the person who recorded it.

## Permits, inventory and safety

71. **One permitting route.** Projects at 50, 100 and 1,000 kilowatt-peak, with and without storage: **all six cases produce the same permit set. No branch logic exists.**
72. **Permits and permits to work are separate tables** with no shared type or code path.
73. **Expected date required on filing**, and the 90-working-day default applies with no history.
74. **Accumulation overrides the default.** Three building permits at one office averaging 60 days: the fourth forecasts from that history, not from 90.
75. **Requirement library accumulates**, appears at filing on the next project at that office with `times_observed`, **and no screen exists for hand-editing it.**
76. **Additional requirement is not a delay.** A task is raised, the library is written, the date re-bases, and the record shows re-based rather than missed.
77. **Prerequisite blocks mobilisation** and appears as an exception from day one with no ageing threshold.
78. **Closeout exposure is valued.** A turned-over project with an outstanding closeout permit conditioning final billing shows the unbilled amount.
79. **Gate 20 has no threshold.** Engage a consultant for ₱2,000: approval is still required.
80. **Stock moves on receipt.** Issue a transmittal: origin decreases, in transit increases, destination unchanged until the receiving signature. Total stock across all states is conserved during transit.
81. **Discrepancy raises immediately.** Receive 18 of 20: a discrepancy reaches both custodians and the Procurement Head on receipt.
82. **Route class derives from the form.** Laguna → Dumaguete is inter-island, 10 days, with no extra input. A Bicol site destination from Laguna is also inter-island.
83. **All four directions.** Site → warehouse is accepted as a normal transmittal.
84. **Hard block 5.** Attempt to issue quarantined material at every permission level. All must fail and be logged.
85. **Zero tolerance.** Count one unit short on any item: an investigation is required before the count closes, and the closing reason appears in the distribution query.
86. **Every issue names a block.** Issue material with no block. Must fail.
87. **Surplus returns at cost.** After a price change, the originating block's cost reduces by the amount originally issued.
88. **Site stock is stock.** Material issued to a site stock location remains in inventory, at that location.
89. **Opening balance records both dates.** Count date and lock date both retrievable.
90. **Reorder points do not apply to project material.**
91. **Gate 28 cannot be automated.** Attempt to auto-approve, delegate or set a window on a permit to work at every level including console holder. All must fail.
92. **Competency gating.** Name a worker with lapsed training on a permit to work. Must fail.
93. **Permit validity is enforced.** An open permit past its window appears as a live finding, not an expired record.
94. **Near-miss needs no login.** Scan the site code on a device with no account: the form submits.
95. **No reporter identity anywhere.** Search every screen, query and export for reporter identity or per-person incident counts. **There must be none outside the safety function.**
96. **Push acknowledgement cannot be disabled** on the three carve-out categories; adding a fourth category succeeds.
97. **Safety indicators are derived.** Confirm no screen exists for entering an indicator value.
98. **Corrective actions closed without evidence are permitted and reported.**
99. **Emergency card works offline.**
100. **Subcontractor exclusions are held.** A policy excluding injury to contractors' workmen is stored and reported, not just the certificate.

## Work, money and people

101. **No duration fields.** Schema review: no `hours`, `time_spent`, `started_at` or activity field on `task`. **No per-person clock-in, clock-out, location or duration anywhere in the platform.** The site-level `working_hours_start`/`_end` is not attached to any person and does not fail this test.
102. **Output type required.** Save a task with no output type. Must fail.
103. **Automatic closure.** File a site report; its task closes with no separate action.
104. **One owner.** Attempt to assign a task to two people. Must fail.
105. **Blocked requires a name**, and appears on the blocker's daily screen.
106. **Carry-forward.** Leave a task unfinished overnight: it is on tomorrow's screen, not lost.
107. **Committed date is permanent.** Move a date four times; the original is retrievable and `recommit_count` reads 4.
108. **Priority is scarce.** A fourth priority item from one requester must fail until one is released.
109. **No aggregate per-person score.** Search for any computation producing a rating, score, index or load number from task counts, grades, load or on-time data. **There must be none.**
110. **No ranking of people** on any screen, query or export.
111. **No-task flag routes correctly.** The Check appears for the manager and director; nothing appears on the person's screen or record; the executive view shows a count across managers, never names. No flag is raised for approved leave.
112. **Load is a band.** No numeric load value is exposed on any screen, report or export.
113. **Self-registration counts identically** to assigned work.
114. **Mention governs notification.** Post ten messages mentioning nobody: no notification is raised for anyone, including previous participants. **No mute, watch or subscription control exists.**
115. **Message de-duplication and ordering.** Forced retries post once; five queued messages post in composition order; text arrives before a large attachment.
116. **Messages are append-only.** Attempt to edit or delete as console holder. Must fail; hiding is available and is itself logged.
117. **One-tap conversion.** Convert a message to a task: one action, output type required, link back retained.
118. **Photograph prompt.** Attach a photograph to a block thread: the platform offers to attach it to today's site report instead.
119. **Records link to revisions, not documents.** Create a site report against revision 3, issue revisions 4 and 5, reopen — it shows revision 3. A permit filing still references the revision submitted.
120. **One revision in force**, and a superseded revision announces itself and links to the governing revision.
121. **Unclassified is visible but unusable.** It opens and is discussable; attaching it to a work instruction must fail.
122. **Acknowledgement is per revision.** Acknowledge revision 2, issue revision 3 — the person shows as not acknowledged.
123. **Required-document register is derived**, with no screen for hand-building a checklist.
124. **Form revision is recorded on records**, and records created under a previous revision remain readable as they were.
125. **Permanent classes never expire** under any retention run; **legal hold overrides retention.**
126. **No general ledger.** Schema review: no chart of accounts, no journal table. No write path to the accounting system.
127. **Fund release blocked** on a contractless project. Must fail and be logged.
128. **Claimed and certified are separate.** Certify less than claimed; both are retained and the variance appears in the client query.
129. **Uncertified escalation carries the client baseline** — amount, client, age and that client's average certification time.
130. **Three confidence bands.** Every forecast line is secured, gated or projected, and every gated line names a gate, an owner and an age.
131. **Gap detection.** Construct a negative position in month two: an exception is available, valued, listing the gated cash that would close it.
132. **Over- and under-billing** compute correctly from earned against billed.
133. **Reconciliation reports variance**, not absorbed.
134. **Unliquidated advance blocks the next request.**
135. **No computed rating.** Confirm no computation produces a rating from operational data; a rating saved with no reasons must fail.
136. **Engagement responses are not identifiable.** Schema review: no `person_id` on `engagement_response`.
137. **Buddy is not the manager.** Must fail.
138. **Regularization is diarised.** The decision task appears ahead of the date.
139. **Source effectiveness is twelve-month** — people still employed at twelve months, not people hired.
140. **Self-service works without Human Resource.** An employee views their leave balance, certifications and payslip with no Human Resource action.
141. **Attrition by manager is a Check**, not a manager score.
142. **Payroll: the block lands on the run.** Leave one site day unreported. **The register cannot be generated, and no individual worker is dropped.**
143. **Historical reproducibility.** Compute March, change a rate in June, re-open March: March reproduces exactly, and each line names the rate version used.
144. **Unapproved rates do not compute.** Enter a rate, do not approve it, run payroll — the old rate is used.
145. **Statutory figures cannot be overridden.** Attempt to edit a computed statutory deduction on one payslip at every permission level. All must fail.
146. **Brackets, not percentages.** Verify a bracket-boundary salary against the published table to the peso.
147. **Attendance has no clock**, and `days_worked` derives from toolbox attendance with no separate entry.
148. **Separation of duties.** Attempt to compute and release payroll as one person. Must fail.
149. **Acknowledgement gates the period.** Close a period with a sheet outstanding. Must fail.
150. **Three-cycle parallel run.** Attempt payroll cutover after one matching cycle. Must refuse.
151. **Overtime only where worked.** Hours are recordable only on overtime days.

## Reporting and Model Context Protocol

152. **Silence states what was checked.** A domain with no exceptions states the check time and rule count. **A blank panel is a failure.**
153. **Every exception names a person**, never only a department, and carries a valued "so what" wherever a value exists.
154. **Drill reaches the log.** From any exception, drill to the record and then its audit history.
155. **Measure register enforces a decision.** Create a measure with no decision attached. Must fail.
156. **Gaming guards hold.** Search every screen, query and export for a per-person load score, a per-person grade aggregate, reporter identity, or a per-person safety score. **None may exist.**
157. **Role scoping.** As Project Manager, confirm only own-project exceptions appear.
158. **Board pack generates** with no manual assembly step.
159. **Money visibility respected over the protocol.** Ask about margin as a person with `money_visibility` of `none`. No answer, and **the underlying query never reads the value.**
160. **Record scope respected over the protocol.** Ask about a project outside scope. No answer, and **no acknowledgement that the project exists.**
161. **Configuration carries a human name.** Change a threshold: the log names the person, never the platform, and records the arrival channel.
162. **Same authority.** As a person without threshold authority, attempt the change over the protocol. Must fail identically to the screen.
163. **Confirmation before applying.** Issue an ambiguous configuration instruction: the change is stated back in full and requires explicit confirmation before any write.
164. **Gates apply.** Change a system constant: gate 22 fires with no alternate.
165. **Statutory rates writable, results not.** Update a contribution table — succeeds under dual control. Attempt to override a computed deduction — must fail.
166. **Tenant scoping.** Authenticate as one tenant: no data or configuration of another is reachable.
167. **Every call audited** — reads and writes both.
168. **No tool can disable a hard block.** Enumerate every tool and parameter and attempt it by every route. All fail and are logged.

## Field, product and migration

169. **Full offline day.** Fly-mode for a full working day: report, toolbox record with photographs, checklists and messages all captured, then synchronise correctly.
170. **Offline day attribution.** Create offline Monday, sync Thursday. It is Monday's report.
171. **No approvals offline.** Refused, with a clear reason.
172. **No silent loss.** Force upload failures: every record is retained and shown as unsent.
173. **Queue is visible**, with retry.
174. **Resumable upload** survives interruption; **the original is retained** if the application is killed mid-upload.
175. **Gallery prohibition.** Capture ten photographs: none appears in the device gallery, and **no route exists to attach one from the gallery.**
176. **Compression.** Uploaded size is approximately 300 kilobytes per photograph.
177. **Revocation kills the device cache.**
178. **Pre-population.** Leave activities incomplete: tomorrow's report opens pre-filled.
179. **No Magnus literals in code.** Search for ₱2,000,000, ₱100,000, 1,277, 7, ₱6.70, 115, 130 and the approved brand names as literals. **There must be none.**
180. **Second tenant profile runs.** Configure an invented company with different stages, thresholds and roles. The platform runs it.
181. **Full export works.** Export all Magnus data: complete, documented and re-importable. Export is logged and permission-scoped.
182. **Tested restore.** Restore to a working system and record date, duration and outcome.
183. **No outbound email.** Schema and configuration review: no outbound mail transport is configured and no notification or digest leaves the platform by email.
184. **The platform does not file.** Confirm no route submits anything to any government channel.
185. **Aliases prevent duplicates.** Migrate a person under three spellings: one record results.
186. **Workday seeding.** Load a live project at workday 84: its next report is 85, not 1.
187. **Import reversible before lock**, refused after.
188. **Old stores are read-only.** Attempt to add a file to a frozen document location. Must fail.
189. **Accumulated figures carry sample size.** Every accumulated figure displays its observation count.

---

# 15. DELIBERATELY NOT BUILT — DO NOT ADD ANY OF THESE

**Read this section before starting each module, not after. The most expensive thing you can do on this project is build something nobody asked for.**

| Not built | Why |
|---|---|
| Any scheduler, cron job, background worker, queue processor, timer or polling loop | Section 1 |
| An exception engine, rules engine or workflow engine | Agents do this |
| A nightly pass of any kind | Section 1 |
| Ranked exception lists, severity scoring, consequence ordering, item caps | Judgement, not a rule |
| Automatic escalation of anything to anyone | A person or an agent escalates |
| Automatic pass-down of approval authority when a window expires | Windows are recorded, never acted on |
| Auto-approval of anything, at any threshold, ever | R1 |
| Automatic raising of retention invoices, progress claims or billing schedules | The dates are stored; an agent reads them |
| Automatic generation of deliverable tasks or client obligations at contract signature | An agent generates; the platform stores |
| Automatic Non-Conformance Report or corrective action creation | A person or an agent raises them |
| Automatic statutory-deadline task creation | The deadlines are stored and queryable |
| Automatic instantiation of recurring obligations | The cadence is stored; an agent instantiates |
| Outbound electronic mail or short message service, for anything including digests | Only the three-category push carve-out leaves the platform |
| Notification digests, summaries or roll-ups | Section 8.2 |
| An in-platform chat assistant or any large language model call from inside the platform | The intelligence connects from outside |
| Emergent-findings pipelines, token budgets, steering prompts, nightly narrative | Deleted entirely |
| Predictive progress curves, delay forecasting, conditional deliverable adjustment, bill of materials generation, lead scoring, opportunity probability weighting, approval-probability prediction, predictive cash modelling | These require accumulated history the company does not yet have |
| Autonomous agent action taken without a human decision | An agent acting on unproven data does not fail visibly — it fails confidently |
| Automatic resource allocation or optimisation, supplier selection, bid scoring, automated proposal generation or pricing | The platform shows and records; a person decides |
| Administrative screens for maintaining any accumulated reference data | Section 8.21 |
| A general ledger, chart of accounts, journal posting, statutory financial statements, or writing to the accounting system | It is a sub-ledger |
| Automatic filing or submission to any government portal | Filing is a person's act |
| Any presence, location, activity, keystroke or login-time tracking, for anybody, at any level | L4. No console setting may switch it on |
| Page-view or navigation logging | Surveillance of people |
| Fatigue tracking from consecutive days worked | Too close to the presence boundary; pending counsel |
| Any field where a person types a project percentage complete | Section 8.7 |
| Hours, timers, time tracking or activity feeds on tasks | Section 8.12 |
| Any per-person rating, score, index, aggregate grade, numeric load value, ranking or forced distribution | L7 |
| Automatic conversion of ratings or recognition to money | Section 8.16 |
| Identifiable engagement survey responses | Section 8.16 |
| Reporter identity or per-person incident counts outside the safety function | Section 8.11 |
| A headcount integer in place of named toolbox attendees | Section 8.7 |
| Photograph upload from, or writing to, the device gallery | No reliable date, place or provenance |
| Site photographs stored as message attachments | Section 8.13 |
| Silent discarding of any field-captured record | Section 9 |
| A configurable block spine, removable structural block dependencies, or a project phase badge | Standardisation is the product |
| Weight re-basing on a cost correction | Section 8.5 |
| A seventh hard block, an `active` flag on hard blocks, or any override, exception or emergency path | Section 5 |
| A shared implementation for gates and hard blocks | They differ in kind, not degree |
| A separate procurement buying list, or procurement creating bill of materials lines | Section 8.5 |
| A structured request-for-quotation and comparison object | Section 8.6 |
| A manual supplier rating screen | Section 8.6 |
| An approval point above the Procurement Head | Section 8.6 |
| Blocking a bank detail change | Second-person confirmation and payment flagging — visible, not prevented |
| Automatic reordering, or reorder points on project material | Section 8.9 |
| A hand-maintained permit requirement library or duration table | Section 8.8 |
| Capacity-based permitting branches, or a separate battery storage permitting route | Section 8.8 |
| Merging permits with permits to work | Section 8.8 |
| A tolerance band on stock counts, or custodian variance as a score | Section 8.9 |
| Stock arriving on despatch, or surplus returned at current or average price | Section 8.9 |
| A second live version of form MRTC-PROC-F003 | The digitised form supersedes the paper one |
| Barcode or serial scanning | Not required now; `is_serialised` lets it be added without a rebuild |
| Overwriting one deployment layer with another, or a single combined decline rate | Section 8.10 |
| Equipment custody by location, or manually entered utilisation | Section 8.10 |
| Leave reason visible to anyone but Human Resource | Section 8.10 |
| Auto-approval or delegation on any permit to work; an alternate Safety Officer for lifting a safety stop | Gates 28 and 29 |
| Additional fields on the near-miss form; manually entered safety indicators | Section 8.11 |
| Safety checklist content invented by the builder | It comes from Alma Codog |
| A general safety module replacing the manual | Section 8.11 |
| A contract template or clause library; defaulted or inferred retention terms; automatic clause extraction | Magnus signs on client paper |
| Any tax computation on related-party contracts | The platform flags; it does not compute |
| A single party field on the project | Section 8.4 |
| Site as a field on the account; collapsing *did not proceed* into *lost* | Section 8.3 |
| Contingency on any client-facing output; editing a frozen winning proposal; a value threshold on gate 6 | Section 8.3 |
| Links from records to a document rather than a revision | Section 8.14 |
| Deleting or silently replacing superseded revisions | Section 8.14 |
| Automatic classification by document type; blocking unclassified documents from being read | Gate 33 |
| Acknowledgement of a document rather than a revision; a hand-maintained required-document checklist | Section 8.14 |
| Document editing inside the platform | Documents are produced elsewhere and controlled here |
| Thread subscription, watch or mute; message editing or deletion; presence, typing or read receipts; voice or video calling | Section 8.13 |
| A configuration screen for which objects carry threads | Section 8.13 |
| Real-time messaging infrastructure | Not required at this tier; polling is sufficient and materially cheaper |
| Migration of Messenger history into threads | Archive separately |
| Password storage, reset or recovery; sign-in for site crew members; a single-role-per-person model | Section 7 |
| One combined permission level mixing record scope and money visibility | Section 8.1 |
| Any view of another person's notification panel; ranking, filtering or capping in the personal panel; badges on Information; stored badge counters; group or role-addressed notifications; clearing a notification by reading it | Section 8.2 |
| Removing any of the three push carve-out categories | Section 1.1 |
| Offline editing of shared records, or offline approval | Section 9 |
| A native store application | Section 9 |
| Deletion of any person, role, gate, message, incident, safety record or audit entry | Nothing is deleted |
| A service account or platform identity for any agent | Every action carries a human's name |
| Any tool, verb or parameter capable of disabling a hard block | Test 168 |
| Any elevated authority through the Model Context Protocol, or silent application of a configuration change | Section 12.4 |
| Retention periods invented by the platform, or a platform position on regulatory sufficiency | Counsel decides |
| A platform position on Bureau of Internal Revenue registration | Counsel and Finance decide |
| Bulk configuration import | Configuration is a governance act, one change at a time, each with a reason |
| Backups without a tested restore | Section 8.20 |
| Migration of finished projects' documents or messages; absorption of the historical archive; migration of historical accounting | Section 8.22 |
| Typed percentage complete on migrated projects | Section 8.22 |
| Deletion of any superseded system at cutover; a cutover leaving any parallel channel writable | Freezing removes temptation; deleting removes the ability to check |
| Payroll cutover on fewer than three matching cycles; deleting the legacy spreadsheet | Section 8.17 |
| Dropping an unreported worker from the payroll register | Article 116 |
| Payroll visibility for Project Managers, Persons In Charge or console holders | Section 8.17 |
| Populated career paths and compensation bands | Magnus has not defined them; the structures exist and are empty |
| Exit interviews conducted by the person's manager; a management-only career ladder | Section 8.16 |
| External or client participation in threads; tenant configuration screens for other tenants | A later phase |
| Subscription billing, client portals or marketplace features | Not in this release |
| Electronic wallet payroll | Deferred, and recorded as the structural fix for the cash exposure |
| A security review gate before internal go-live | Required before any outside tenant, not before this release |

---

# 16. DEVIATIONS FROM THE SOURCE SPECIFICATION

**Every one of these is a deliberate simplification made to remove automation from the platform. Each is listed with what is lost, so it can be reviewed rather than discovered.**

**Automation will be layered onto this platform before deployment, by agents and possibly by a scheduler added later. Every deviation below must therefore be reversible without a schema change:** keep `window_working_days`, `passed_down_at`, `original_approver`, the `awaiting_alternate` and `escalated` states, the stored retention and statutory deadline dates, and the recurring-obligation cadence definitions **exactly as specified**, even though nothing in this build acts on them. Removing a field because nothing reads it yet would make the later automation a migration instead of an addition.

**D1 · Approval windows no longer act.** The source specification passes authority to the alternate automatically when a window elapses. Here the window is stored and displayed but nothing fires. **Lost:** automatic pass-down, and the pass-down-rate report as a live signal. **Replaced by:** an agent reading pending approvals with their age against the recorded window. **Gate 29's age-escalation and gate 10's `proceeded_without_review` both become explicit human or agent actions rather than transitions the platform makes.**

**D2 · No nightly pass.** The source specification recomputes every exception at 23:00, ages open items, fires escalations and raises scheduled obligations, then delivers a directors' report at 06:00. **Lost:** the 06:00 report and the structural guarantee that a check ran overnight. **Replaced by:** on-demand queries that each return their own evaluation timestamp and rule count, which preserves the *silence means checked* requirement at the moment of asking.

**D3 · No exception ranking or twelve-item cap.** The source specification ranks by consequence, then irreversibility, then age, and caps at twelve. **Lost:** a deterministic, auditable ordering. **Replaced by:** agents ranking from the same underlying facts. The four required contents of every exception — what, who, how long, so what — are retained on every row.

**D4 · Retention and progress-claim invoices are not raised automatically.** The source specification raises the retention invoice on its date with no human action and calls this the structural fix for the most forgettable receivable in the business. **This is the highest-value automation being removed.** The date is computed and stored at turnover; **an agent must read it. If no agent runs, the retention leak reopens.** Accepted by the Chief Executive Officer on the basis that automation is layered on before deployment; the stored date is what makes that possible.

**D5 · Non-Conformance Reports are not raised automatically on a damaged, wrong or short delivery.** Quarantine still happens in the same transaction and hard block 5 still holds. Only the report creation moves to a person or an agent.

**D6 · Corrective actions are not raised automatically from a failed inspection item.** The failed item is recorded; a person or an agent raises the action.

**D7 · Statutory obligations do not raise themselves.** Deadlines are stored and queryable. A disabling injury no longer creates the Work Accident/Illness Report task automatically. **Non-compliance penalties reach ₱50,000 per day, so this deserves a named agent obligation and a named human owner.**

**D8 · No escalation ladders anywhere** — stale site reports, uncertified claims, unacknowledged push items, overdue corrective actions, ageing safety stops, unclaimed board tasks, capability shortages, expiring certifications and insurance. All remain queryable with their ages; none chases anybody.

**D9 · The `supplier` object is merged into `party`.** The source specification defines both, which contradicts its own rule that a subcontractor is a party rather than a separate object — a rule justified by the observation that three records for one company produce three insurance expiry dates and two of them are wrong. **This resolves a genuine contradiction in the source documents.**

**D10 · The in-platform assistant and the artificial-intelligence layer are deleted entirely.** The source specification's in-platform assistant, nightly narrative and emergent-findings pipeline do not exist, and neither do the token budget or steering prompt that configured them. **The Model Context Protocol server satisfies both halves of the Chief Executive Officer's instruction — connect Claude to the platform, and configure the platform using Claude — without any model running inside it.**

**D11 · Recurring obligations are definitions, not instances.** A cadence is stored against the obligation; nothing instantiates the task. An agent does.

**D12 · Weekly digests are queries, not deliveries.** The console change digest and the daily overdue digest are exposed as queries. An agent delivers them.

**Everything else in the source specification is implemented as written.** The six hard blocks and the five refusals · the twenty-eight gates as data · row-level tenant isolation · the hash-chained append-only log with cryptographic erasure · record scope and money visibility as independent axes · effective-dated system constants · the fixed block spine and derived completion · offline field capture with dual timestamps · the revision-in-force rule · the payroll statutory boundary and the Article 116 rule · non-retaliation · and every gaming guard, unchanged.

---

# 17. HOW TO PROCEED

Build in this order and **do not compress the first phase.**

**Phase 0 — Foundation. One owner. Nothing else starts.**
Multi-tenant schema with `tenant_id` on every table from the first migration · database row-level security · the append-only hash-chained audit log with cryptographic erasure · identity, roles, `record_scope` and `money_visibility` · **the twenty-nine gate rows and six hard block rows as seed data, not code** · system constants and configuration values, effective-dated · the notification model and badge computation · the tenant record · continuous integration and a tested restore from backup.

**Everything downstream inherits this phase's mistakes. A `tenant_id` retrofitted onto populated tables is a migration, not an edit, and an append-only log cannot be retrofitted onto a table that has been edited for four months.**

**Prove it before building a single feature screen:** run acceptance tests 1, 2, 5, 7, 9, 10, 16, 22 and 168.

**Phase 1 — three streams, concurrent.**
*Stream A — the project spine, the critical path, internally serial:* pipeline → project and contract → design → procurement → blocks and site reporting. **Publish `project_id`, `project_block_id` and the block spine on day one — two other streams are waiting on nothing else.** Adding people does not shorten this stream: a contract exists before a design, a design produces the bill of materials, procurement buys against it, and a block cannot progress until material arrives. **That chain is the business, not the code.**
*Stream B — work management:* tasks → communication → document control. Needs only `project_id` and `block_id` from stream A. Stub both and proceed. **This stream carries the Messenger switch-off, which is an operational event rather than a code event.**
*Stream C — field, inventory and safety:* inventory → manpower → safety → mobile. Publishes `deployment.labour_rate`, without which stream D cannot compute labour cost, and `location_id`, which procurement needs for receipt and quarantine. **Build the safety checklist structure and leave the content slots empty. Do not invent them.**

**Phase 2 — after the spine delivers real values, not stubs.**
*Stream D — money, in this fixed order:* finance → **payroll** → human resource. **Payroll before Human Resource. Human Resource depends on payroll, not the reverse.** Cannot start until block value weights and `deployment.labour_rate` are real — **a stub gives you a working screen over meaningless numbers.** Externally blocked until the accounting platform maintainer is named.
*Stream E — permits.* Small and self-contained; slots in any time after projects, design, blocks, tasks and communication exist.

**Phase 3 — reporting and measurement queries, then migration and cutover.** These read what the other streams wrote and create almost nothing of their own. **Building them early produces confident screens over data that does not exist yet.**

**Build the Model Context Protocol server incrementally alongside each module rather than at the end.** It is the second product surface, not a final integration step.

**Field-test the photograph and offline path before building any interface on top of it** — section 9. **A Person In Charge, a real rooftop, real Bicol or Sorsogon signal.**

**Create a second, entirely invented test tenant early and keep it populated.**

**Turn the acceptance tests in section 14 into a test suite that runs, not prose that is read. They are already written and already numbered against rules. That is the single highest-return day of work in the whole build.**

**One registry for every fact that appears more than once** — gates, hard blocks, constants, thresholds. Change it there; never restate it. **Write a script that checks the seed data and every rule number in a test against the registry. Nothing merges until it returns clean. Nothing is recorded as done until a later check confirms it — not because the person who did it said so.**

**Sixteen items are open at the time of writing. Three block building; the rest block nothing. None is a developer's to solve, and the item numbers are the ones used throughout the source data room.**

| # | Open | Owner | Blocks |
|---|---|---|---|
| **1** | **Safety checklist content — daily walk, weekly checklist, monthly audit** | **Alma Codog** | **Section 8.11 inspections. Build the structure; leave the slots empty** |
| **2** | **Accounting platform maintainer — who maintains it, and their availability** | **To be named** | **Section 8.15. Do not design the export format around a guess** |
| 3 | Primary Administration Console holder | Chief Executive Officer to name | — |
| 4 | Opening stock count dates for Laguna, Sorsogon and Dumaguete | Jay, Bernie, Paul | — |
| 5 | Pilot project, its Person In Charge and project manager | Chief Executive Officer | — |
| 6 | Cristy's document migration date, and help | Chief Executive Officer | — |
| 7 | **The counsel list, canonical:** retention periods · cryptographic erasure sufficiency · Labor Code Article 105 · probationary and regularization requirements · payroll deduction authorisation · aggregation exposure · subcontractor insurance clause · related-party documentation · fatigue tracking · thirteenth-month pay, statutory leave and Social Security System, PhilHealth and Pag-IBIG obligations · the eight-family contract playbook · suspension entitlement · Department of Labor and Employment inspection records · National Privacy Commission registration position | Atty. Caneja | Leave every affected value `[CONFIGURED]` |
| 8 | Subcontractor insurance exclusions; commercial general liability renewal | Insurance broker | — |
| 9 | Data allowance cover for Persons In Charge | Chief Executive Officer | — |
| 10 | Developer seats — one or two | Waits on the builder | — |
| 11 | Retention policy split — which classes beyond the six permanent ones are kept, and for how long | Atty. Caneja | — |
| 12 | Whether the accounting platform is registered as a Computerized Accounting System with the Bureau of Internal Revenue | To be confirmed | — |
| 13 | The controlled weather selection list — exact values | Safety Officer with the Persons In Charge | — |
| 14 | Whether any project uses a daily report format other than the standard one | Project Managers | — |
| 15 | Starting expected permit durations per local government unit, and whether the safety programme is submitted online in each region | Jeferson, Austin | — |
| **16** | **The safety manual `MRTC-OSH-GDL-00 Rev 00` itself** — it names the thirteen indicators, the seven permit-to-work steps and the eighteen investigation points | **Alma Codog** | **Section 8.11 — permits to work, incident investigation, indicators** |

**Eight things that are not software and do not wait for it**, recorded because cutover is when they get forgotten: renew the commercial general liability cover — **no company-wide cover since 28 February 2026, against ₱43.5 million of equity, the most urgent item in this entire exercise** · check retention billing on every project turned over in the last eighteen months · restate every model built on 1,400 kilowatt-hours per kilowatt-peak · verify subcontractor insurance by reading the exclusions · start the payroll acknowledgement sheet this week, on paper · train a second person on battery energy storage programming · send the builder's questions · tell the investor that four approved objectives are a later phase.

**Where this instruction is silent, ask. Do not decide. Every question is cheaper than every assumption.**
