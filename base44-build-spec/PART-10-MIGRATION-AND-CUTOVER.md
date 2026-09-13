# Magnus Workspace Platform — Base44 build specification

## Part 10 · Migration and cutover

**Prerequisite: Parts 01 to 09.** More platforms fail at cutover than fail at build — a parallel channel left open, an opening balance that was wrong, a store people kept using, a Person In Charge whose first photograph failed.

**Two rules govern this entirely:** nothing is authoritative until its predecessor is frozen · nothing is loaded that nobody will maintain.

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

## A. What is and is not migrated

**Not migrated:** finished projects' documents (remain in Google Workspace, searchable) · finished projects' Messenger history (archived and searchable, nothing extracted) · historical accounting · the four hundred gigabyte archive (triaged, not absorbed).

**Master data:** people with aliases · equipment with a named custodian each · items with unit of measure and serialised flag · suppliers with taxpayer identification and accreditation state · clients, sites and contacts, with sites separate from accounts.

**Active projects:** project and contract · blocks with include flags · value weights from the costed bill of materials · **workday counters seeded** · current block states and percentage complete **derived from the loaded position, never typed** · open purchase orders and committed cost · open permits with expected approval dates. **Every live project's signed contract is uploaded before it can become active; retention terms are read out of each one.**

**Document triage:** every live project's documents come across before go-live · classification under gate 33 · old locations made read-only by the Workspace administrator on the cutover date · an exception list naming anything not classified or migrated, with a reason. Cristy needs a date and, quite possibly, help.

**Communication cutover:** one live project moved mid-flight · field-test the photograph path first · extract the pilot's Messenger history as operating state, not a transcript · move the team · **rename the pilot's Messenger group and make it read-only** · run several weeks · remaining projects follow on a named date.

**Freezing, not deleting:** payroll spreadsheet retained read-only after three matching cycles · pilot Messenger group read-only · document stores read-only on the cutover date · accounting system continues.

**Training by role.** The Person In Charge's is the longest and the most important — on their own phone, on site, offline behaviour included.

**What is said to staff at rollout, in plain words, and this is part of the deliverable:** *The workload you register is never used in your appraisal. No number the platform produces will decide your rating. The platform does not track where you are or when you log in.*

---

## B. The migration record

**Every imported record** carries `migrated = true`, `import_batch_id` and `source_reference`. Every import writes one audit entry per row under the importing person with arrival channel, session identifier and scope `migrate`. Reports and lists may filter migrated from born-on-platform records.

**`import_batch`** — import_batch_id · sheet · imported_by · imported_at · row_count · created · updated · refused (with reasons) · reversed_at · reversed_by · reversal_reason.

**`tenant.cutover_date`** — set in Administration. After it, the `migrate` scope cannot be created, existing migrate tokens are refused, and no non-stock batch may be reversed.

**An import writes state; it does not decide.** No gate is replayed on migrated state. The gate outcome as it happened is stored where the row carries it (counsel review state, approver and date on open purchase orders). Role assignments arrive as **pending gate 24 requests**, not approved.

**Every import tool** takes a batch of rows in the column layout of the migration workbook, returns `import_batch_id` and one result per row (created, updated, refused with reason), and **writes nothing if the batch fails validation as a whole.** Rows link by natural key: person `full_name` including aliases · party `legal_name` · account `account_name` · site `site_name` · item `item_code` · project `project_code` · agreement `agreement_reference` · asset `asset_reference`. A link that does not resolve refuses the row.

---

## C. The import tools — `migrate` scope, in loading order

1. `import_roles`
2. `import_persons` — aliases stored; a person arriving under a spelling already in `aliases` **updates the existing record**; `signs_in` with an email creates the pending identity link; role assignments raise gate 24 as pending requests
3. `import_parties`
4. `import_accounts` — each creates its account space
5. `import_sites` — region derived from province; local government unit; emergency card fields
6. `import_contacts`
7. `import_items`
8. `import_equipment` — custodian must be a person
9. `import_locations`
10. `import_opening_stock` — into an unlocked opening balance; serialised items require serials; `quarantined` condition loads into quarantine
11. `import_projects` — `status` may be `setup`, `active`, `suspended` or `turned_over`; `active` or beyond requires a contract row with a signed document in the same batch or already loaded (**hard block 6**); `mobilised = yes` at or above the insurance threshold requires the certificate (**hard block 1**); `cshp_approved = yes` requires the document; workday counter seeded from `workday_counter_at_cutover` and `first_site_day`; planned curve stored as given; `turnover_date` on a turned-over project derives the three dates in the same transaction
12. `import_contracts` — the signed document uploaded by `upload_migration_document(file_name, content)` before or in the same batch; `counsel_review_state` stored as given; risk terms recorded as read where given
13. `import_project_parties`
14. `import_project_blocks` — value weights computed from loaded block costs excluding General Requirements and locked; `state_at_cutover` stored; **`percent_complete_at_cutover` seeds one migration site-report activity per block dated the day before cutover** so the derived figure equals the loaded position and the field is never typed again; `signed_off_date` on B0 satisfies hard block 3 for B1
15. `import_bill_of_materials`
16. `import_open_purchase_orders` — states `issued` and `partially_received` only; approver and date stored as the gate outcome; exchange rate and date required where not peso; hard block 6 applies
17. `import_project_permits` — `expected_approval_date` required where filed
18. `import_billing_milestones` — claimed, certified, invoice and paid values stored as given
19. `import_service_agreements` — `active` requires the document and at least one service level term in the batch, else loads as `draft` and produces no charge; expiry derived
20. `import_service_level_terms`
21. `import_serviced_assets` — warranty expiry derived where a project exists, typed only where not; expected yield derived
22. `import_asset_equipment`
23. `import_maintenance_plans`
24. `import_open_work_orders` — device timestamps where given, server otherwise, marked migrated; assigned owner must sign in
25. `import_open_warranty_claims`

**Plus:** `validate_import(sheet, rows)` — runs every check, writes nothing · `list_import_batches` · `reverse_import(import_batch_id)` — allowed until the opening stock lock for a stock batch's warehouse and until the cutover date for every other batch; removes the records and writes a reversal audit entry per row; refused after · `request_opening_stock_lock(location_id)` — creates the gate 27 request for Cristy, who decides on screen.

**The Migration and Cutover screen** shows batches, rows, refusals and reversals, the cutover date field, and the same workbook upload as a fallback for a person without an agent. **It has no button that approves anything.**

---

## D. Loading workflow

1. Karl fills the workbook, or points at the spreadsheets and Drive folders it should be filled from.
2. An agent validates offline: duplicates and aliases, links between sheets, missing contract and agreement documents, projects with no site, items with no unit, agreements with no service level term, open purchase orders on projects with no contract.
3. Load in the order above, one sheet per batch, on a `migrate` token. Karl checks each on screen.
4. A wrong batch is reversed and reloaded.
5. Jay, Bernie and Paul count; Cristy spot-checks; gate 27 locks each warehouse. The `migrate` scope ends on the cutover date.

**Real contracts, people and stock are loaded once, into the deployment that will go live** — decide before any real data is loaded whether the current deployment is production or a development copy.

---

## E. The pilot ground rules — published to the pilot group as a page in the platform

Until the approval engine is wired to every gate and every gate holds an approver: **the platform is a rehearsal; today's real process still runs** · **an approval inside the platform is not an approval** · **safety records in the platform authorise nothing.** The page states what is worth testing hard (messages, search, records people create anyway, files and Drive, the phone on site), what to leave alone (payroll, approvals, permits to work), that pilot data may not survive corrections, and the five-line defect format: what I was doing · what I expected · what happened · where · device and signal. **This build removes the need for rules 2 and 3 by shipping every gate configured and wired in Part 01** — the page is still published, and the rules are withdrawn one at a time as the checks in Part 12 pass.

---

## F. Checks before Part 11 and Part 12

1. Import the same person under three spellings across two batches — one record.
2. Import a project as `active` with no contract document — refused naming hard block 6; with the document — loads active.
3. Import a block at 55 percent — reads 55 from the migration activity; no percent field is typed anywhere afterwards. A project imported with counter 62 files its next report as workday 63.
4. Import an agreement without its document — `draft`, no service charge.
5. Import opening stock, reverse — stock zero, reversal logged per row. Lock under gate 27 — reverse refuses.
6. Set the cutover date to yesterday — creating a `migrate` session refuses; existing ones refuse on the next call.
7. Every imported record carries `migrated`, `import_batch_id`, `source_reference`; a report filters on it.
8. No import tool creates an approved state that was not in the row; role assignments arrive as pending gate 24 requests.
9. Acceptance tests 185 to 188 and 228 to 236 from Part 12 pass, with output pasted.
