# Magnus Workspace Platform — Base44 build specification

## Part 09 · The Model Context Protocol server — the second product surface

**Build this incrementally alongside every part, not at the end.** It is how the platform is operated, monitored and configured by external agents (Claude Desktop, Claude Code, any agent runtime). **Expose through it everything a person can see or do on a screen, and nothing a person cannot.**

**If Base44 cannot host a Model Context Protocol endpoint natively:** build every tool below as an authenticated HTTP endpoint with the exact name, parameters, scope rule and refusal message, and place a thin protocol adapter in front. The rules are the deliverable; the transport is not.

---

## 0. Standing rules — repeated at the top of every part

1. The platform is a record, a permission boundary and a Model Context Protocol server. **No scheduler, automation, timer, workflow, rules engine, notification engine, ranking or digest.** The only exception is the same-transaction safety push (Part 01 §2.1).
2. Four permitted computations: derived on read · hard block and gate evaluation at the instant of the attempt · permission resolution at the instant of the request · same-transaction derivation from fields the human action supplied.
3. Every table carries `tenant_id`; every read and write goes through the one server-side data-access layer; the client never writes a governed table directly.
4. The audit log is append-only and hash-chained; nothing edits or deletes an entry.
5. Gates and hard blocks are data rows; one approval engine serves every gate; nothing is auto-approved.
6. Every write carries a human's name; no service account; no agent identity.
7. No abbreviations or ampersands anywhere in the interface, field names, statuses or messages.
8. No Magnus-specific literal in code; all values are configuration rows.
9. Presence is never tracked, for anybody, at any level.
10. Where the specification is silent, ask; do not decide.

---

## 1. Authentication, scoping and audit

- **The server has no permissions of its own. It has the permissions of the authenticated person, and no more.** The connecting person authenticates as themselves. There is no service account, no platform identity, no "changed by the assistant".
- **No person record may be created to give an agent an identity. No agent ever holds gate 32 or a console seat.**
- Every call is tenant-scoped at the query layer by the same data-access layer as the screens. **Scope at the query layer, never by filtering an answer after computation.** A person with `money_visibility` of `none` asking for a margin receives a refusal and the underlying query never reads the value. A project outside `record_scope` is not acknowledged to exist.
- **It refuses rather than estimates.** Where the data does not support an answer, it says so.
- **Every figure returned cites the records it came from** (`sources`).
- Every call — reads and writes — is written to the audit log with `arrival_channel = model_context_protocol`, the `agent_session_id` and the session scope.
- **Every tool calls the same server-side function the screen calls.** No tool reimplements a mutation. The first build's constant tool patched values in place, its revision tool set status from free text, its role tool skipped the gate and the duplicate check, and its role-creation tool skipped the uniqueness check — each because it wrote its own path. A tool is a thin adapter over the one function; it never carries logic of its own.

## 2. Sessions and the four scopes

**`agent_session`** — agent_session_id · person_id · **scope** · created_by · created_at · **expires_at** · last_call_at · revoked_at · revoked_by · client_name.

| Scope | May do | May never do | Who may create | Expires |
|---|---|---|---|---|
| `read` | Every list, get and search tool; every computed query; audit chain verification | Any write | Any account holder, for themselves | 90 days |
| `write` | Create and update records the person may create on screen: task, notification, message, non-conformance report, site report and toolbox meeting, generation reading, work order raise, document upload, group membership, archive and restore, a correction to a record the person may edit with a reason | Submit any approval decision; raise a purchase order, fund request, variation order or write-off; any configuration | Any account holder, for themselves | 14 days |
| `decide` | Submit an approval decision on any pending request where the person is primary or alternate; every configuration tool in section 6 under its gate; hard block **values** under gate 31 | Gate 32 and console holder changes; a statutory rate change without the second person's screen confirmation; gates 18, 28, 29 and 30 unless the person is the officer of record; gate 35; self-approval; the existence of any hard block | Console holders only; the second console holder is notified on creation | 12 hours |
| `migrate` | The import tools of Part 10 only | Anything else | Console holders only; second console holder notified | The cutover date recorded in Administration; after it the scope cannot be created |

Rules for all scopes: scope is fixed at creation and stamped on every audit entry · raising scope means a new token · a scope grants nothing the person lacks on screen · **self-approval is refused across sessions — two tokens held by one person are one person** · an expired or revoked token is refused on the next call with the reason · a break-glass fifth scope is **not** built.

**The Agent Sessions tab** shows every session with person, scope, expiry, created by, last call and a revoke control; every person sees and may revoke their own; console holders see all.

## 3. Read tools

**List, get and search for every object in Parts 01 to 07**, tenant-scoped, respecting record scope and money visibility before the query runs. Naming: `list_<object>`, `get_<object>`, `search_<object>`. Every `get_project` returns `site_id`, `client_party_id`, the derived project name and `funds_blocked_no_contract` (true while `contract_id` is empty). Every list accepts pagination and a filter for `migrated`; `list_threads` and `list_channels` accept an archived filter defaulting to excluded.

**Computed queries — each returning `evaluation_timestamp`, `rules_evaluated` and `sources`:**

Percentage complete per block and per project against the planned curve · material readiness by block with the date each becomes startable · blocks not startable with mobilisation planned · projects with no submitted site report in the last two working days · site report compliance by Person In Charge · **`list_pending_approvals`** (request, gate, primary, alternate, age in working days, recorded window, whether the caller may decide it) · blocked activities with reason and expected clear date · cumulative days lost by blocked reason and responsible party · weather stoppage days per project · non-conformance reports open with ageing and same-day closure rate · design deliverables waiting by party with cumulative days · sealing engineer turnaround · designs sealed under a licence later found lapsed · design capacity against contract capacity · the twelve-month cash forecast in three bands with gate, owner and age on every gated line · projected negative cash position within three months with the gated cash that would close it · claims uncertified beyond thirty days with the client's average certification time · receivables ageing · retention scheduled, due and overdue · retention, warranty and operations obligations due within N days · over- and under-billing by project · committed cost against block budget with the five percent flag stating price or additional items · cost and margin per block and project · markup actual against policy by client, Director and period · foreign exchange variance · off-design purchase rate · purchase orders committing 50% or more of a block budget · supplier on-time, fill, damage and lead time · supplier bank detail change register · payments after a bank change · price movement by item · stock by location including in transit and site stock · transmittals in transit beyond expected days · transmittal reconciliation · quarantined material by value, age and reason · count variance by warehouse and custodian with closing-reason distribution · material issued by project and block · permits past expected approval · prerequisite permits outstanding · closeout permits blocking final billing, valued · follow-ups required per office · permit duration, requirement and fee accumulation per office with sample sizes · safety stops open · incidents open · permits to work by type and past validity · workers with lapsed training on a permit · corrective actions open, overdue, closed without evidence · the thirteen safety indicators once supplied · near-miss to incident ratio · hierarchy of controls distribution · checklist item failure rates · Construction Safety and Health Program status by project · subcontractor accreditation and insurance with exclusions · resource availability with release dates · resource requests declined by reason (never a combined rate) · requests unfulfilled past needed-from · deployment variance across all three layers · roster continuity conflicts · equipment utilisation · capabilities held by fewer than two people on a critical path · certifications expiring within N days · people with no assigned task as a count across managers · output type by department · commitment reliability by team · blocked task ageing · load bands by team · open assignment board depth · objects with no thread activity on active projects · mention response time by team · messages converted to tasks · channel versus object thread ratio · required-document register per project · documents missing where they gate something · unclassified backlog and age · acknowledgements outstanding by revision · documents overdue for review · superseded revisions accessed · headcount by department, region and employment basis · new headcount cost against budget · attrition by tenure, role, region and manager · time to hire and source effectiveness at twelve months · onboarding completion by manager · review-held compliance · engagement trended in aggregate · regularization decisions due · site days blocking the payroll register · paid headcount against toolbox attendance · acknowledgement sheets outstanding · statutory rate change history · parallel run variance by cycle · statutory remittance summary per agency per period · sub-ledger to general ledger variance · contracts signed without counsel review · risk-term exposure by clause family and contracts with unread families · client obligations outstanding · related-party register · pipeline by stage, capacity and value · markup and discounting patterns · win and loss by reason · contingency carried per client · structural confidence against later reinforcement variations · hard block attempts · threshold change history · console change history · access review status · restore test record · legal holds in force · export history · retention status by class · storage growth per project · the eleven operations and maintenance queries of Part 07 · **`list_unacknowledged_pushes`** · **`verify_audit_chain(from_sequence, to_sequence, verify_files)`** returning the exact range verified and the true last sequence · **`get_audit_entries(object_type, object_id)`** · **`search_audit(person, arrival_channel, from, to)`** · **`get_account_activity(account_id, from, to)`** — every record and every message under the account in the window, with sources, respecting scope and excluding groups and direct messages the caller is not in · **`list_files_pending_drive`** · **`get_drive_status`** · **`list_channel_members(channel_id)`** · **`list_import_batches`**.

**These are queries, not alerts.** The platform computes them when asked and does nothing with them.

## 4. Write tools (`write` scope)

Create and update for every object the person may create or edit on screen, under the same validation, refusing with the same message the screen shows. Named ones: `create_task` · `update_task` · `claim_task` · `release_task` · **`create_notification(recipient_person_id, category, object_type, object_id, headline)`** — exactly one recipient, one record · **`post_message(thread_object_type, object_id, text, mentions, client_message_key)`** and `post_channel_message(channel_id, …)` · `create_group` · **`invite_member(channel_id, person_id)` · `remove_member` · `leave_channel` · `handover_group_ownership` · `rename_group`** · **`archive_thread` · `restore_thread` · `archive_channel` · `restore_channel`** (same authority rules as the interface) · `create_site_report` with its toolbox meeting and activities · `create_non_conformance_report` · `create_generation_reading` · `raise_work_order` · `upload_document(file_name, content, object_type, object_id)` · `create_person` (status `pending`) · `update_person_contact` (the person card fields) · `create_document_revision` (draft) · `push_pending_files_to_drive` · `verify_file(file_id)`. **No tool deletes anything.**

## 5. Decide tools — propose, then confirm (`decide` scope)

**Every tool that submits an approval or changes configuration is two calls.**

`propose_*` validates the request, applies the gate rule (including R6 across sessions), and returns a statement of the exact change in full sentences plus a one-time `confirmation_code` valid for ten minutes. **Nothing is written.** Example: *Approve progress claim HT-B claim 2 on 480_kW_Calamba Agro Industrial Corporation for ₱4,320,000 under gate 11 as Head of Finance, alternate Chief Operating Officer. Confirm with code 8F3K.*

`confirm_*(confirmation_code)` applies the change under the same gate, writes the same audit entry a screen action would plus arrival channel, session and scope, and returns the record. A code used twice, expired, or presented by a different session is refused.

**Tools:** `propose_approval` / `confirm_approval` (approve or reject, note required on reject) · `propose_threshold_change` / `confirm_threshold_change` (gate 31) · `propose_gate_change` / `confirm_gate_change` (gate 31 for limits, primaries, alternates and windows; never for gate 32; R3 and R5 enforced) · `propose_system_constant` / `confirm_system_constant` (gate 22, effective-dated, versioned — never patched) · `propose_controlled_list_change` / `confirm_controlled_list_change` · `propose_push_list_change` / `confirm_push_list_change` (the three cannot be removed) · `propose_hard_block_value` / `confirm_hard_block_value` (gate 31; value only) · `propose_role_assignment` / `confirm_role_assignment` (raises the gate 24 request; the row is `pending_approval`; no duplicate; subject must be `active` or `pending`) · `propose_document_classification` / `confirm_document_classification` (gate 33) · `propose_publish_revision` / `confirm_publish_revision` (the same in-force function as the screen) · `propose_legal_hold` / `confirm_legal_hold` (console holders, reason required) · `propose_statutory_rate` — creates the pending change for the second person to confirm **on screen**; there is no `confirm_statutory_rate` over the protocol.

**No tool exists that changes a role's permissions, a console seat, tenant isolation, an audit entry, a statutory calculation result, an erasure, or the existence of a hard block.**

## 6. Seven rules on every configuration write

1. Authenticated as a person. 2. Same authority as the screen. 3. Same gates apply — none relaxed because the change arrived here. 4. Confirmation before applying — the proposed change stated back in full. 5. Reason recorded where the field requires one. 6. Logged identically to a screen change, plus the arrival channel. 7. Effective dating preserved.

**Statutory rates are writable here, deliberately, under the same dual control as the screen.**

## 7. Never writable by any client

Not through the protocol, the screens, the database, or any permission level: **the audit log · statutory calculation results · tenant isolation · the existence of any of the six hard blocks.**

**Generate a tool enumeration document** — every tool, every parameter, its scope, and for each whether it can reach a hard block's existence, the audit table, statutory results or another tenant — reachable from Administration and regenerated on every deploy. **A build-failing test walks every tool and parameter and finds none that reaches a hard block's existence.** This is the single most important test in the build.

## 8. Migrate tools

Listed in Part 10 §C. `migrate` scope only.

## 9. Checks before Part 10 starts

1. On a `read` token every write and decide tool refuses. On a `write` token `propose_approval` and every configuration tool refuse; `create_task` and `post_message` succeed.
2. A non-console-holder cannot create a `decide` or `migrate` session; the second console holder is notified when one is created.
3. `propose_threshold_change` returns a statement and a code; nothing changes. `confirm_threshold_change` applies it under gate 31, logged identically to a screen change plus channel, session and scope; the same code again refuses; an expired code refuses; a code from another session refuses.
4. A request raised on Karl's `write` token cannot be approved on Karl's `decide` token.
5. Ask for margin as a Person In Charge — refused; the query never read the value. Ask about a project outside a Project Manager's scope — not acknowledged to exist.
6. `propose_statutory_rate` creates the pending change; nothing over the protocol confirms it.
7. A token past `expires_at` is refused with the reason; a revoked token is refused on the next call.
8. Every summary and exception returns non-empty `sources`; `get_project` on a contractless project reports `funds_blocked_no_contract: true`, and false after the signed contract is uploaded.
9. `propose_system_constant` / `confirm` produces a new version and closes the previous; no tool patches a value in place. `propose_publish_revision` on an unclassified document refuses with the screen's message.
10. The tool enumeration document exists; the build-failing test finds no path to a hard block's existence.
11. Acceptance tests 159 to 168 and 215 to 227 from Part 12 pass, with output pasted.
