This message completes section 12 of the original instruction, the Model Context Protocol server, and adds the one-time migration import path from section 8.21 to it. It also closes six defects found by connecting to the endpoint on 3 September. **Read all of it, then build it in the order A, B, C, D.** Nothing here changes the less-brain position: every call is made by a person, every write carries that person's name, nothing runs on a timer, and no tool in any combination can disable a hard block.

Testing of the screens is in progress by a browser agent and by staff. Keep deploying; this work is server-side. Do not rename or move any screen while it runs.

---

# A. DEFECTS FOUND ON THE ENDPOINT — CLOSE THESE FIRST

**A1 · `hardBlock6Active` reports false on a project with no contract.** `get_finance_summary` on PRJ-2026-0001 returned `contractValue: null` and `hardBlock6Active: false`. Hard block 6 is in force on every project whose `contract_id` is empty. Either the flag is inverted or the evaluation is wrong. Fix the evaluation and rename the field to `fundsBlockedNoContract` so its meaning cannot be misread.

**A2 · `project` carries no site and no client.** `list_projects` returns `opportunityId`, `proposalId` and `siteAssessmentId` but no `siteId` and no client party. Amendment 1 of section 8.23.1 makes `site_id` required on `project`, carried across by the `won` handover, and section 8.4 requires `client` as a reference to `party`. Add both, populate them on the five existing projects from their opportunities, and return them from every project read.

**A3 · Figures return without their records.** Section 12.1: every figure returned cites the records it came from. `get_finance_summary`, `get_inventory_summary`, `get_board_pack` and every exception report return bare totals. Every returned figure carries a `sources` list of record identifiers, and every exception carries the record it was computed from and the person it names.

**A4 · Construction and procurement exception reports evaluate zero rules.** A domain that evaluates no rules is not silence stating what was checked; it is a blank panel, test 152. Implement at minimum: projects with no submitted site report in the last two working days · blocked activities with reason and expected clear date · blocks not startable with mobilisation planned · non-conformance reports open with ageing · purchase orders past expected arrival · goods received short or damaged with no non-conformance report · quarantined material by value and age · transmittals in transit beyond expected days · prerequisite permits outstanding.

**A5 · The audit chain panel shows "Last sequence: 100" while the newest entry is 149.** The panel shows the true last sequence number and the exact range verified, for example "verified entries 50 to 149, last sequence 149".

**A6 · Sidebar drift.** The sidebar shows *Tasks* and *Construction* as separate items and *Design & Engineering* with an ampersand. Section 13 fixes the order: Dashboard · My Day · Pipeline · Projects · Design and Engineering · Procurement · Permits · Inventory · Manpower and Equipment · Safety · Operations and Maintenance · Documents · Messages · Finance · Human Resource · Payroll · Reports · Administration. Tasks live inside My Day; blocks and site reports live inside Projects. *Migration and Cutover* may stay as the last item until the cutover date, after which it is hidden. **Make this change after the browser agent's test completes, not during it.**

---

# B. COMPLETE SECTION 12 — READ, WRITE, DECIDE

## B1 · Session scopes

Every agent session carries exactly one scope, fixed at creation, stored on the session record, shown on the Agent Sessions tab, and stamped on every audit entry with the session identifier. Raising scope means a new token. Four scopes:

| Scope | May do | May never do | Who may create | Expires |
|---|---|---|---|---|
| `read` | Every list, get and search tool; every computed query; audit chain verification | Any write | Any account holder, for themselves | 90 days |
| `write` | Create and update records the person may create on screen: task, notification, message, non-conformance report, site report and toolbox meeting, generation reading, work order raise, document upload, a correction to a record the person may edit, with a reason | Submit any approval decision; raise a purchase order, fund request, variation order or write-off; any configuration | Any account holder, for themselves | 14 days |
| `decide` | Submit an approval decision on any pending request where the person is primary or alternate; every configuration tool in section 12.4 under its gate; hard block **values** under gate 31 | Gate 32 and console holder changes; a statutory rate change without the second person's screen confirmation; gates 18, 28, 29 and 30 unless the person is the officer of record; self-approval; the existence of any hard block | Console holders only; the second console holder receives a notification on creation | 12 hours |
| `migrate` | The import tools in section C only | Anything else | Console holders only; second console holder notified | The cutover date recorded in Administration; after that date the scope cannot be created |

Rules that apply to all scopes: the session acts as the person and no more, section 12.1 · a scope grants nothing the person lacks on screen · self-approval is refused across sessions, since two tokens held by one person are one person · every call is logged with `arrival_channel = model_context_protocol`, the session identifier and the scope · an expired or revoked token is refused on the next call with the reason.

## B2 · Read tools

Expose list, get and search for every object in section 8, tenant-scoped at the query layer, respecting `record_scope` and `money_visibility` before the query runs, never by filtering a computed answer. A person with `money_visibility` of `none` asking for a margin receives a refusal and the underlying query never reads the value, test 159. A project outside `record_scope` is not acknowledged to exist, test 160.

Expose every computed query in section 12.2, each returning `evaluation_timestamp`, `rules_evaluated`, and `sources`. Add `list_pending_approvals` (request, gate, primary, alternate, age in working days, recorded window, whether the caller may decide it), `list_unacknowledged_pushes`, `verify_audit_chain(from_sequence, to_sequence)`, `get_audit_entries(object_type, object_id)` and `search_audit(person, arrival_channel, from, to)`.

## B3 · Write tools

Create and update for every object the person may create or edit on screen, under the same validation the screen applies, refusing with the same message the screen shows. `create_notification(recipient_person_id, category, object_reference, headline)` writes exactly one notification to one person pointing at one record. `post_message(thread_object_type, object_id, text, mentions)` posts to the object's thread. No tool deletes anything.

## B4 · Decide tools: propose, then confirm

Every tool that submits an approval or changes configuration is two calls.

`propose_*` validates the request, applies the gate rule, and returns a statement of the exact change in full sentences plus a one-time `confirmation_code` valid for ten minutes. Nothing is written. Example return: "Approve progress claim HT-B claim 2 on PRJ-2026-0001 for ₱4,320,000 under gate 11 as Head of Finance alternate Chief Operating Officer. Confirm with code 8F3K."

`confirm_*(confirmation_code)` applies the change under the same gate, writes the same audit entry a screen action would write plus the arrival channel, session identifier and scope, and returns the record. A code used twice, expired, or presented by a different session is refused.

Tools: `propose_approval` / `confirm_approval` on any pending request · `propose_threshold_change` / `confirm_threshold_change` under gate 31 · `propose_gate_change` / `confirm_gate_change` under gate 31 for limits, primaries, alternates and windows, never for gate 32 · `propose_system_constant` / `confirm_system_constant` under gate 22, effective-dated · `propose_controlled_list_change` / `confirm_controlled_list_change` · `propose_push_list_change` / `confirm_push_list_change` · `propose_statutory_rate` which creates the pending change for the second person to confirm on screen under dual control; there is no `confirm_statutory_rate` over the protocol.

No tool exists that changes a role's permissions, a console seat, tenant isolation, an audit entry, a statutory calculation result, or the existence of a hard block. **Enumerate every tool and every parameter in a generated document reachable from Administration, and prove by a build-failing test that no call and no sequence of calls disables a hard block, section 12.5.**

## B5 · Token expiry and the Agent Sessions tab

Add `scope`, `expires_at` and `created_by` to the session record and the tab. Show scope and expiry on every row. Creating a `decide` or `migrate` session from any account that is not a console holder is refused. The second console holder receives a notification with the creator, scope and expiry.

---

# C. THE MIGRATE SCOPE — SECTION 8.21 IMPORT PATH OVER THE PROTOCOL

**Purpose.** Live records are loaded as they stand, once, before cutover. An import writes state; it does not decide. No gate is replayed on migrated state. The gate outcome as it happened is stored where the row carries it.

**Every imported record** carries `migrated = true`, `import_batch_id` and `source_reference`. Every import writes one audit entry per row under the importing person with arrival channel, session identifier and scope `migrate`. Reports may filter migrated from born-on-platform records.

**Every import tool** takes a batch of rows in the column layout of the migration workbook, returns `import_batch_id`, one result per row (created, updated, refused with reason), and writes nothing if the batch fails validation as a whole. Rows link to other records by natural key: person `full_name` including aliases, party `legal_name`, account `account_name`, site `site_name`, item `item_code`, project `project_code`, agreement `agreement_reference`, asset `asset_reference`. A link that does not resolve refuses the row.

**Tools, in loading order:**

1. `import_roles`
2. `import_persons` — aliases stored; a person arriving under a spelling already in `aliases` updates the existing record, test 185; `signs_in` with an email creates the pending identity link; role assignments raise gate 24 as pending requests, not approved
3. `import_parties`
4. `import_accounts`
5. `import_sites` — region derived from province; emergency card fields stored
6. `import_contacts`
7. `import_items`
8. `import_equipment` — custodian must be a person
9. `import_locations`
10. `import_opening_stock` — loads into an unlocked opening balance; serialised items require serials; `quarantined` condition loads directly into quarantine
11. `import_projects` — `status` may be `setup`, `active`, `suspended` or `turned_over`; `active` or beyond requires a contract row with a signed document in the same batch or already loaded, hard block 6; `mobilised = yes` above the insurance threshold requires the insurance certificate, hard block 1; `cshp_approved = yes` requires the document; the workday counter is seeded from `workday_counter_at_cutover` and `first_site_day`; the planned curve is stored as given; `turnover_date` on a turned-over project derives retention, warranty and operations dates in the same transaction
12. `import_contracts` — the signed document file is uploaded by `upload_migration_document(file_name, content)` before or in the same batch; `counsel_review_state` stored as given; risk terms recorded as read
13. `import_project_parties`
14. `import_project_blocks` — value weights computed from the loaded block costs excluding General Requirements and locked; `state_at_cutover` stored; `percent_complete_at_cutover` seeds one migration site-report activity per block dated the day before cutover so the derived figure equals the loaded position and the field is never typed again; `signed_off_date` on B0 satisfies hard block 3 for B1
15. `import_bill_of_materials`
16. `import_open_purchase_orders` — states `issued` and `partially_received` only; approver and date stored as the gate outcome; exchange rate and date required where not peso; hard block 6 applies
17. `import_project_permits` — `expected_approval_date` required where filed
18. `import_billing_milestones` — claimed, certified, invoice and paid values stored as given
19. `import_service_agreements` — `active` requires the document and at least one service level term in the batch, else loads as `draft` and produces no charge, section 8.23.12; expiry derived from commencement plus term
20. `import_service_level_terms`
21. `import_serviced_assets` — warranty expiry derived where a project exists, typed only where not; expected yield derived from capacity and the constant in force
22. `import_asset_equipment`
23. `import_maintenance_plans`
24. `import_open_work_orders` — device timestamps where given, server timestamp otherwise, marked migrated; assigned owner must sign in
25. `import_open_warranty_claims`

**Plus:** `validate_import(sheet, rows)` runs every check and writes nothing · `list_import_batches` · `reverse_import(import_batch_id)`, allowed until the opening stock lock for a stock batch's warehouse, and until the cutover date for every other batch; reversal removes the records and writes a reversal audit entry per row; after the lock or the date it is refused · `request_opening_stock_lock(location)` creates the gate 27 request for Cristy, who decides on screen.

**Migration screen.** The existing Migration and Cutover screen shows the batches, their rows, refusals and reversals, the cutover date field, and the same workbook upload as a fallback for a person without an agent. It has no button that approves anything.

---

# D. ACCEPTANCE TESTS — APPEND TO SECTION 14 AS TESTS 215 TO 236

## Protocol scopes

215. **Read scope cannot write.** On a `read` token, every write and decide tool refuses.
216. **Write scope cannot decide.** On a `write` token, `propose_approval` and every configuration tool refuse; `create_task` and `post_message` succeed.
217. **Decide requires a console holder.** A non-console-holder account cannot create a `decide` or `migrate` session; the second console holder is notified when one is created.
218. **Propose writes nothing.** `propose_threshold_change` returns a statement and a code; the threshold is unchanged; no audit entry other than the proposal is written.
219. **Confirm applies once.** `confirm_threshold_change` with the code applies it under gate 31 and logs it identically to a screen change plus arrival channel, session and scope. The same code a second time refuses. An expired code refuses. A code from a different session refuses.
220. **Self-approval across sessions.** A request raised on Karl's `write` token cannot be approved on Karl's `decide` token.
221. **Money visibility over the protocol.** Test 159 on a Person In Charge token.
222. **Record scope over the protocol.** Test 160 on a Project Manager token.
223. **No path to a hard block.** The generated tool enumeration exists; the build-failing test walks every tool and parameter and finds none that reaches a hard block's existence.
224. **Statutory rates need the second person.** `propose_statutory_rate` creates the pending change; nothing over the protocol confirms it.
225. **Expiry.** A token past `expires_at` is refused with the reason.
226. **Every figure has sources.** Every summary and exception returns non-empty `sources`.
227. **Hard block 6 flag.** A project with no contract reports `fundsBlockedNoContract: true`; after the signed contract is uploaded it reports false.

## Migration

228. **Aliases collapse.** Import the same person under three spellings across two batches; one record results, test 185 over the protocol.
229. **Active needs the document.** Import a project as `active` with no contract document; the row is refused naming hard block 6. Import with the document; it loads active.
230. **Position is derived, not typed.** Import a block at 55 percent; the block reads 55 percent from the migration activity; no percent field is typed anywhere afterwards.
231. **Workday counter seeds.** A project imported with counter 62 files its next site report as workday 63.
232. **Draft agreement produces no charge.** Import an agreement without its document; state `draft`, no service charge exists.
233. **Reverse before lock.** Import opening stock, reverse it, stock is zero and the reversal is logged per row. Lock the warehouse under gate 27; reverse again refuses.
234. **Migrate scope ends.** Set the cutover date to yesterday; creating a `migrate` session refuses; existing ones are refused on the next call.
235. **Migrated is visible.** Every imported record carries `migrated`, `import_batch_id` and `source_reference`; a report filters on it.
236. **Nothing decides.** No import tool creates an approved state that was not given in the row; role assignments arrive as pending gate 24 requests.

---

# E. THEN CONTINUE

Build A, then B, then C, then run D. Report the generated tool enumeration document and the results of tests 215 to 236 when done, then resume any remaining milestones without waiting to be prompted.
