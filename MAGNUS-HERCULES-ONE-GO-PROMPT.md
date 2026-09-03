# MAGNUS PLATFORM — CONFORMANCE BUILD INSTRUCTION

This is one message. It replaces every follow-up prompt sent before it and it is read in full before any work starts.

**What happened.** A full end-to-end test of the current build on 3 September 2026, module by module against the original instruction, found that the build borrows the instruction's vocabulary but not its rules. The six hard blocks have different meanings from section 5. Every gate is unassigned and the person who raises an item approves it. Gates are chosen from a dropdown instead of by amount. The block spine is nine generic blocks with typed percentages. There are no roles, no permissions, no sign-in grant, no file upload, no message composer, and Operations and Maintenance, which was specified in a follow-up, is a placeholder. Progress claims fail with a server error. The full findings are restated below, section by section, as what exists and what must exist.

**The rule for this build.** The original instruction is the authority. Where this message restates it, this message wins over the current build. Where the current build and the original instruction differ on anything this message does not mention, the original instruction wins. There are no exceptions and no "equivalent" implementations.

**Reading discipline.** Before writing any code, produce **Deliverable 0: the conformance checklist** — one row per numbered requirement in this message (every line marked with a requirement number such as F1.3 or M4.2) with the columns: requirement · exists / deviates / missing · what will change. Post it in full. Then build in the milestone order in Part H, and after each milestone post the checklist rows for that milestone updated to done, plus the results of the acceptance tests named for it. Do not skip ahead, do not reorder, and do not stop to wait for a reply between milestones.

**The five rules that hold everywhere, unchanged from the original instruction:** no scheduler, timer or cron anywhere in the platform · nothing acts by itself; every write is a person's act or a same-transaction derivation · every database access goes through the tenant wrapper · the audit log is append-only and hash-chained · no abbreviation on any label, including the ampersand.

**Screens under test.** Staff will test on phones and at the warehouse after this build. Nothing in this message is optional because of that.

---
# PART F — FOUNDATION OF CONTROL (Milestone 1)

Nothing in Parts M, X, C or P is safe to build until Part F exists, because every later rule depends on knowing who the person is, what role they hold, and whether a document is a file.

## F1 · Roles, permissions, scope and money visibility (original section 8.1)

**F1.1** Build the `role` and `permission` tables exactly as section 8.1: role_name in full words, department, reports_to_role, is_approver, active; permission by role, object type and action with `record_scope` (own / department / region / all) and `money_visibility` (none / cost / price / margin). Roles are deactivated, never deleted.

**F1.2** Seed these roles as data, each with its permissions: Chief Executive Officer · Chief Operating Officer · Director · Head of Finance · Finance Officer · Procurement Head · Procurement Officer · Project Manager · Design Engineer · Person In Charge · Safety Officer · Document Controller · Warehouse Custodian · Permit Liaison · Human Resource Head · Payroll Officer · Sales Officer · Service Technician. A Person In Charge, Warehouse Custodian and Service Technician have `money_visibility` of none. A console holder has no Human Resource or Payroll data access by virtue of the seat.

**F1.3** Administration › Roles shows the list, each role's permissions, and the people holding it. Changing what a role may do is gate 32.

**F1.4** Every query in the platform applies `record_scope` and `money_visibility` at the query layer, never by filtering a computed answer. Exports and printed views obey the same rule.

## F2 · Persons and sign-in (original section 8.1 and deviation D13)

**F2.1** The `person` record carries every field in section 8.1: full_name, aliases, population (office / field / warehouse / consultant), employment_basis, employer party, signs_in, home_region, status, vouched_by. Persons are created in Administration › Persons and in Human Resource; the Migration screen remains a bulk path. The Manpower "Add Worker" free-text form is removed; the workforce is the persons with population `field`.

**F2.2** Grant sign-in from Administration › Persons: enter the sign-in email; the identity link is created pending and becomes active on that person's first sign-in with that email. Revoke sign-in from the same place. Show "Signs In" only when the link is active. Grant Kidron Magnus sign-in for kidron.magnus@gmail.com as part of this milestone.

**F2.3** Assigning a role to a person raises gate 24 (department head primary, Chief Operating Officer alternate). Gate 24 in the current build is named "Employment Offer"; rename and re-point it. Offers are part of module 17 and carry no gate of their own.

**F2.4** Console holders: exactly two. Fill the second seat with **[SECOND CONSOLE HOLDER]**. Adding a third refuses. Gate 32 alternate is the second holder. Add the Tenants screen showing the tenant record and its identity provider setting.

## F3 · Gates as rows with a role check, and the universal self-approval refusal (original section 6)

**F3.1** Replace the gate rows with the thirty rows of section 6 exactly: numbers 1 to 12, 18 to 24, 25a, 25b, 26 to 34; the exact gate names, triggers, primary and alternate as written there; windows recorded and displayed, never enforced. Gate 34 is the warranty claim submission from section 8.23. The current names on gates 5, 6, 7, 11, 20, 24 and 25a differ and are corrected.

**F3.2** Primary and alternate are **roles**, except gates 10, 18, 27 and 33 which name a `primary_person`. A gate with no primary refuses at submission with a message naming the gate, not silently. "Primary: Unassigned" must not exist after seeding.

**F3.3** The decision screen and the decision mutation check that the deciding person holds the primary or alternate role. Any person picker that lets the raiser name an arbitrary approver, such as the current "Issued By" on a permit to work, is removed.

**F3.4** **Refusal R6, everywhere, without exception:** the person who raised a request cannot approve it, on any gate, in any module, on screen or over the protocol. The current build applies this only on gate 26 and supplier bank confirmation; apply the same check in the single approval path every gate uses. There is one approval path; modules do not implement their own.

**F3.5** The gate that applies is **derived from the amount or condition, never chosen**. Write-off: up to ₱50,000 gate 1, ₱50,001 to ₱100,000 gate 2, above gate 3. Purchase order: up to ₱100,000 gate 4, above gate 5. Transfer: inter-island 25a at any value, within-island above ₱100,000 25b. Quotation markup more than five points below policy: gate 7 only. The severity dropdown on write-offs is removed. Thresholds are configuration under gate 31, never literals.

**F3.6** Gates 3, 7, 9, 18, 22, 27, 28, 29, 30 and 33 have no alternate and no window, and the Administration screen offers no control to add one. The current configure dialog that lets "No alternate" be unticked on gate 28 is removed.

**F3.7** My Approvals: one list, every gate, sorted by age, each row showing what, which gate, the triggering value or condition, who raised it, how long it has waited and the recorded window. Approval detail shows the object, not a summary of it. Board pack and exception counts read from this same query, so "Pending Approvals 0" with nine pending cannot recur.

**F3.8** Statutory rate tables are **not gate 32**. They are dual control under section 6.2: the second person is any other person holding Head of Finance or Human Resource Head, never the author. Rename the current flow.

**F3.9** Every approval, rejection and gate attempt writes an audit entry carrying the actor's name, the gate, the object and the outcome. Audit entries currently carry no actor name; add it to every entry, past and future, where the identity is stored.

## F4 · The six hard blocks, exactly (original section 5)

**F4.1** Replace the six current hard blocks with these six, with these meanings and nothing else:

| # | Blocked action | Released only by | Configurable value |
|---|---|---|---|
| 1 | Mobilisation of a project | The insurance certificate document attached. Not a tick-box | ₱2,000,000 contract value |
| 2 | Start of construction | Department of Labor and Employment approved Construction Safety and Health Program recorded | — |
| 3 | Start of the first electrical block | Block B0 Site Safety Infrastructure reaching state `signed_off` | — |
| 4 | Mobilisation where permits are required first | Prerequisite permit issued | Which permit types apply |
| 5 | Issue of quarantined material to a site | Quarantine released, or material disposed | — |
| 6 | Release of funds against a project | Signed contract document uploaded | — |

**F4.2** Hard block 6 blocks three actions: the project cannot leave `setup`; no fund request may be created or released; no purchase order may be raised. The fund request FR-PRJ-2026-0001-001 created without a contract is the proof this is missing. The refusal names the missing contract and who can upload it.

**F4.3** The current "Daily Report Required for Payroll" and "Toolbox Meeting Required for Site Report" are not hard blocks. The first is refusal 1 in section 5.1; the second is validation on the site report. The current "Open Permit Blocks Closeout" is a permit rule from section 8.8, not hard block 4. The current "Fund Release Requires Approved Request" is ordinary workflow.

**F4.4** Administration › Hard Blocks shows the six rows read-only, with the two configurable values editable under gate 31 with a reason, and no enable or disable control. Every attempt against a hard block is logged, including every attempt that fails.

**F4.5** The blocked-action message states which block, what condition is unmet, what would release it and who can supply it. Never "you do not have permission". Hiding a project from a dropdown is not a hard block; the action must exist and refuse.

## F5 · Files are files (original sections 8.14, 8.7, 8.11; Part C below)

**F5.1** The file store is Google Drive as specified in Part C, section B. Build it in this milestone because everything below needs it.

**F5.2** Every field that currently holds a typed "reference" in place of a document becomes a file reference: signed contract · insurance certificate · Construction Safety and Health Program approval · design revision · professional seal record · non-conformance report evidence · toolbox photograph · site photograph · permit filing and approval · task output · incident and near-miss evidence · work order evidence · warranty claim evidence · goods receipt delivery receipt · payroll acknowledgement sheet. A typed string never satisfies a document requirement anywhere.

**F5.3** Photographs on a phone are captured through the application's own camera control; the gallery is not offered; the photograph is never written to the device gallery.

## F6 · Identifiers, time, dates, currency, links, search, notifications

**F6.1** Every record number is unique across the tenant. PO-202609-001 currently exists on two projects. Purchase orders number per tenant, not per project.

**F6.2** All times are stored in Coordinated Universal Time and displayed in Asia/Manila. Every screen shows one date format, `3 Sep 2026`, and one date-time format, `3 Sep 2026 14:18`. Placeholders are never used as values.

**F6.3** Working days use a company working calendar, Monday to Friday excluding Philippine regular holidays held as a configurable table. Permit expected approval, gate windows and every "working days" figure use it. The permit currently computes 90 calendar days.

**F6.4** Currency displays as ₱ with thousands separators everywhere; "PHP 28,800,000" and "6.7" do not appear. Rates show their full precision, ₱6.70.

**F6.5** Every record has a stable address: /projects/PRJ-2026-0001, /accounts/ACC-0012, /purchase-orders/PO-2026-0044 and so on. Opening a record changes the address; the browser back button returns to the list; a pasted address opens the record.

**F6.6** Global search works: record numbers, names, message text, attachment names, scoped by record scope. Ctrl+K opens it.

**F6.7** The notification inbox is real: every mention, direct message, approval request, task assignment and push lands there for its one recipient, with the four categories, uncapped and unranked.

**F6.8** The audit chain panel shows the true last sequence number and the exact range verified.

**F6.9** No Magnus literal in code: search for ₱2,000,000, ₱100,000, 1,277, 7, 6.70, 115, 130, 50,000 and the brand names. Move every one into configuration.

## F7 · Milestone 1 exit

Run tests 1 to 30 of section 14, tests 259 to 276 in Part T, and the checklist rows F1 to F6. Post results. Continue.

---
# PART M — MODULE CONFORMANCE (Milestones 2 to 5)

Each item states what the test found and what section 8 requires. "Replace" means the current implementation is removed; "add" means it does not exist.

## M1 · Pipeline (section 8.3) — Milestone 2

**M1.1** Replace the single-select account type with the `party` model of section 8.4: legal_name, multi-valued party_type (client / asset_owner / offtaker / subcontractor / supplier / consultant / operations_and_maintenance_provider / other), taxpayer_identification_number, address, is_related_party, accreditation_state, insurance_certificate file, insurance_expiry, insurance_exclusions as a field, bank_account_details with the existing confirmation control, categories_supplied, currency. `account`, `site` and `contact` stay as section 8.3, with `site` carrying province, region derived from province, local_government_unit, distribution_utility from a controlled list (Meralco and the electric cooperatives, extendable under configuration), host_party, and the emergency card fields.

**M1.2** Add to `opportunity`: commercial_model (sale / power purchase / lease / operations and maintenance only), capacity_kilowatt_peak, estimated_value. The lost reason is required at any value; the ₱10,000,000 rule of section 8.3 requires a reason from the controlled list rather than free text above that value. Declining a proposal requires a reason. The under-negotiation transition changes the stage; the toast without a change is a defect.

**M1.3** Site assessment carries structural_confidence, usable_area, tapping_point and the proceed / proceed_with_conditions / do_not_proceed outcome, and the badge shows the stored outcome.

**M1.4** Proposal: markup_major_applied and markup_balance_of_system_applied per proposal, defaulting from the constants; gate 7 fires only when either is more than five points below policy, and a Director may go to 110 and 125 without it. Contingency is its own line, internal, absent from every client-facing output. Gate 6 fires on release to client with the Director on the project as primary; the raiser never approves.

**M1.5** The Lease Reference Rate is **₱6.70 per kilowatt-hour**, value-added tax inclusive, section 8.1. The proposal's lease reference is annual yield in kilowatt-hours multiplied by this rate, not roof area multiplied by it. The current "Annual Lease ₱22,512" on 480 kilowatt-peak is wrong; the correct figure is 480 × 1,277 × 6.70. Relabel and recompute.

**M1.6** A client-facing proposal document exists: a printable page and a portable document file, with no contingency, no cost and no margin on it. "Send to Client" records the sent revision.

**M1.7** On `won`, in one mutation: the proposal freezes; the project is created in `setup` with client, site_id, capacity, Director and Project Manager; the site assessment carries to the design package; the block structure seeds the project blocks. "New Proposal" on a won opportunity refuses with a message, never silently.

**M1.8** Portfolio views by region, by stage and weighted by probability, section 8.3.

## M2 · Project and contract (section 8.4) — Milestone 2

**M2.1** `project` carries every field in section 8.4: client, site_id, region derived, local_government_unit, capacity, contract_value, project_manager, director, permit_dependency, expected_permit_duration_days, contract_id, status with the six states and their transitions, planned_percentage_curve, turnover_date. The stored phase chips (Design, Construction, Completed) are removed; status is `setup` / `active` / `suspended` / `turned_over` / `closed` / `cancelled` and phase is never stored.

**M2.2** `contract` carries signed_document as a file, contract_value, currency, date_signed, client_signatory, payment_terms_days, retention_percentage, retention_reference_date_basis, retention_release_months, warranty_months, counsel_review_state, related_party, superseded_by. Gate 10 records `reviewed` or `proceeded_without_review` as distinct outcomes; a query lists contracts signed without review. Gate 9 contract signature, Chief Executive Officer, no alternate, raised by the Project Manager. The list must never say "contract signed" while the contract record says draft.

**M2.3** `risk_term` per clause family with present / absent / not_yet_read, summary, exposure_flag, read_by, read_at. "Acknowledge" alone is replaced.

**M2.4** `project_party` with the eight roles; the client holds four on a straightforward sale. Add the screen and the add control.

**M2.5** Variation orders: raise, gate 8 with the Director, client acceptance, effect on contract value shown with the original intact.

**M2.6** Mobilise action on the project: hard block 1 above the insurance threshold, hard block 4 where permit_dependency is prerequisite. Construction Safety and Health Program record with its document: hard block 2.

**M2.7** Turnover date, gate 21, entered once, derives retention release date, warranty expiry and operations commencement in the same transaction.

## M3 · Design and engineering (section 8.5) — Milestone 3

**M3.1** The design package is created at `won` from the assessment, with the nine named deliverables of section 8.5 seeded, each with its waiting state carrying who and when, stamped and shown.

**M3.2** Replace the nine generic blocks with the fixed spine of section 8.7: B0 Site Safety Infrastructure · B1 Array · B2 Direct Current Cabling · B3 Inverter · B4 Inverter To Panel Board · B5 Panel Board · B6 Panel Board To Tapping Point · B7 Tapping Point · B8 Transformer (include flag) · B9 Network And Monitoring · B10 Miscellaneous · B11 Civil (include flag; mandatory and gating B1 on ground-mount) · General Requirements (no value weight) · Battery Energy Storage System (include flag). Blocks are seeded at `won`; the "Initialise Blocks" button is removed.

**M3.3** Bill of materials lines require a block. Value weights are computed from block cost, materials and labour, excluding General Requirements, and lock when the bill of materials is costed. Design capacity and contract capacity are both recorded and neither reconciled to the other.

**M3.4** `professional_seal` per section 8.5: revision sealed, engineer, licence_number, licence_valid_to, professional_tax_receipt_number and year, sealed_at in Manila time. A seal under a lapsed licence is refused; a licence later found lapsed flags every seal in the window, visibly. Gate 18 releases the package for permitting; status is not a free dropdown.

**M3.5** Structural outcome "reinforcement required" raises a variation order draft in the same transaction, section 8.5.

## M4 · Procurement (section 8.6) — Milestone 3

**M4.1** The buying checklist: the bill of materials grouped by block, showing what to buy, quantity, specification, purchase status, purchase order reference, expected arrival and quantity received.

**M4.2** Purchase order: gate 4 or 5 derived from value (F3.5); issuing requires expected_arrival_date; currency, exchange_rate_applied and exchange_rate_date required where not peso; numbers unique per tenant; hard block 6 refuses on a project with no contract with the correct message. An off-design line requires a reason and a block, and the "Overrun" badge states what it compares.

**M4.3** Goods receipt: location, received quantity, condition (good / short / damaged / wrong_item), delivery receipt photograph; short, damaged and wrong_item quarantine in the same transaction and raise a discrepancy; the receipt posts to stock at the location. Hard block 5 refuses issue of quarantined material.

**M4.4** Permit consultant engagement is a party engagement under gate 20 with the Chief Operating Officer, section 8.8, not a purchase order under gate 4.

**M4.5** Committed cost against block budget with the five percent flag stating price or additional items, section 8.6.

## M5 · Blocks and site reporting (section 8.7) — Milestone 4

**M5.1** Block states not_started / blocked_material / in_progress / complete / signed_off with start and sign-off actions. Hard block 2 on the first start; hard block 3 on the first electrical block until B0 is signed off; B5 and B6 together gate B7; B11 gates B1 on ground-mount; bill of materials line closure gates the block. Dependencies a Project Manager may add to and never remove.

**M5.2** Site report per section 8.7: one per project per workday; workday_number; person_in_charge; weather; work_stopped_by_weather; look_ahead; working hours; toolbox_meeting with topic, **photograph from the in-app camera**, **attendees as named person references picked from the workforce**, conducted_by; activities each bound to a block with percent_accomplished for that day, not cumulative. Day two opens pre-populated from day one's incomplete activities and look-ahead. The site report is filed by the Person In Charge; there is no approval step on a site report.

**M5.3** Percent complete is derived only: block percent equals the sum of its activities' percent_accomplished, project percent is the value-weighted sum, and the planned curve is shown against it. Every typed percent field is removed.

**M5.4** Non-conformance report with source, block, goods receipt where delivery, photograph required, ageing, and closure under gate 19 with evidence as a file.

**M5.5** Turnover Document under gate 21 sets the turnover date (M2.7).

## M6 · Permits (section 8.8) — Milestone 4

**M6.1** `permit_type` library seeded with the Philippine types: barangay clearance, building permit, electrical permit, fire safety evaluation clearance, occupancy permit, environmental compliance certificate or certificate of non-coverage, distribution impact study, net metering agreement, permission to operate, and the closeout set; each with group and issuing body class. `project_permit` with issuing_body, responsible_person, mode parallel / prerequisite, date_filed, expected_approval_date required once filed in working days, date_approved, expiry_date. Expected approval defaults from accumulated medians, then 90 working days.

**M6.2** Hard block 4 on mobilise for prerequisite permits. Closeout permits block final billing where the contract makes it a condition, section 8.8, not hard block 4.

**M6.3** Permit requirements and durations accumulate per office as section 8.8 and 8.21, with the additional-requirement flow kept.

## M7 · Inventory (section 8.9) — Milestone 4

**M7.1** `location` with custodian person and site_stock locations per project. Stock comes only from goods receipts, transfers, issues, counts and the opening balance; there is no direct quantity field.

**M7.2** Stock cannot go negative. Dispatch or issue beyond on-hand refuses, naming the on-hand figure. In-transit is a balance: dispatch decreases the source and increases in-transit; receipt decreases in-transit and increases the destination; a short receipt raises a discrepancy of the difference with a reason, and nothing is written off by itself.

**M7.3** Transfers: gate 25a for inter-island at any value, gate 25b within-island above ₱100,000, derived from the two locations' regions. Expected transit days per route class.

**M7.4** Issue to a project block against the bill of materials line; quarantine with hard block 5; physical count with variance to gate 26 at zero tolerance; opening balance lock gate 27 per warehouse.

**M7.5** Remove "Seed Warehouses" and every seed button from live screens; seeding is migration or configuration.

## M8 · Manpower, workforce and equipment (section 8.10) — Milestone 5

**M8.1** Workforce is persons (F2.1). Resource request decline requires a reason from the controlled list, never a default. Deployment shows planned, recorded and verified days as three figures; "Deployed" is not shown before the planned start.

**M8.2** Equipment: custodian person, certification_expiry, maintenance_due, utilisation accumulated. Capability tags on persons with validity; a lapsed capability is visible where the person is named on a permit to work.

## M9 · Safety (section 8.11) — Milestone 5

**M9.1** Permit to work: gate 28 decided only by the Safety Officer of record on the project, same-day validity, named workers with capability check, no "issue immediately", no arbitrary issuer. Safety stop: gate 29 lifted only by the Safety Officer with a reason. Incident investigation closure: gate 30 with Chief Operating Officer countersignature. None of the three has an alternate, a window or a delegation control anywhere.

**M9.2** Per-site Quick Response code to a no-login near-miss and stop-work form: a public address per site, photograph and a sentence, no identity captured, stop-work routing to the Safety Officer and the Person In Charge with the push notification and mandatory acknowledgement of section 2.

**M9.3** Offline emergency card per site. Inspection cadence as section 8.11: daily walk, weekly checklist, monthly audit. The thirteen indicators derived, none typed.

**M9.4** Nothing in Safety is deleted; closed, voided or superseded only.

## M10 · Tasks and My Day (section 8.12) — Milestone 5

**M10.1** Tasks live inside My Day; the separate sidebar item is removed. Output type has no default and is required. Committed date is kept as the original with a recommit count and the current date. The requester cannot start or record output on the assignee's task. Load is a band, never a number. The priority cap of three stays.

## M11 · Documents (section 8.14) — Milestone 5

**M11.1** Every registration lands `unclassified`; classification is a separate act under gate 33 by Cristy; unclassified is never offered as a choice. An unclassified document is visible, discussable, and cannot be the governing revision.

**M11.2** Revision path draft → for_review → approved → in_force with an approver who is not the author; publish from draft is removed. Every historical reference links to a revision, never a document. The required-document register is derived from module declarations and shows gaps per project.

## M12 · Finance (section 8.15) — Milestone 5

**M12.1** Fix the progress claim server error first and report its cause. Claims carry the derived percent, gate 11, claimed and certified as separate figures, retention invoice under gate 12 on the derived retention date.

**M12.2** Fund request under hard block 6 with liquidation due fifteen days from release and refusal 3 on the next request while one is unliquidated. Write-off gate by amount (F3.5). Cash forecast in three bands; "gap detected" only where a computed gap exists.

## M13 · Human Resource and payroll (sections 8.16, 8.17) — Milestone 5

**M13.1** Gate 24 on hire and role assignment. Statutory tables under dual control (F3.8), bracket tables not percentages. Refusal 1: no register while a site day has no report; the block is on the run, no worker dropped. Refusal 2: no period close with an acknowledgement sheet outstanding. `days_worked` from toolbox attendance. Rates effective-dated; a reopened period reproduces its figures. Console holder has no access to any of it.

## M14 · Reports and administration (sections 8.18, 8.19) — Milestone 5

**M14.1** Board pack and exception reports read live counts; every domain evaluates more than zero rules; every exception names a person and cites its records. Construction and procurement rules as listed in Part P, section A4.

**M14.2** Every configuration change requires the reason where section 8.19 says so and passes its gate: system constants gate 22, thresholds gate 31, permissions gate 32. The current change to Markup Major Equipment 116 percent effective 1 January 2030 is superseded by a new row restoring 115 with reason "test data".

---
# PART X — OPERATIONS AND MAINTENANCE (Milestone 6)

This part was sent before and was not built. It is repeated in full and is not optional.

## 8.23 OPERATIONS AND MAINTENANCE (module 26)

**This is the only module that specifies a service line rather than a project.** Modules 4 to 8 deliver a project: an opportunity becomes a contract, a contract becomes blocks, blocks become a Turnover Document, and the project closes. **This module specifies what happens after that date, for years, on assets Magnus does not own — and on assets Magnus did not necessarily build.**

**Three consequences hold throughout.** A service relationship attaches to a **site**, never to a project, and outlives every project on it. It generates **recurring revenue with no completion**, which milestone billing cannot express. And it covers assets that may have no project record, no block structure, no as-built drawings and no bill of materials — **every field that would come from a project is optional, and every function works without it.**

**The governing rule: a service agreement is a promise with a clock on it. The platform's job is to make every clock visible before it runs out — not after.** Every object here answers one of four questions: what did we promise · what is due · what happened · what are we owed.

### 8.23.1 Amendments to modules already specified

Seven schema amendments, none optional. Five are single fields. **Apply them before or as the affected module is built; none may be deferred to a later migration.**

| # | Amendment | Why |
|---|---|---|
| 1 | **`project` gains `site_id`** (reference to `site`, module 4), carried across by the `won` handover | `project` carries only free-text `site_address`. Without this a serviced site cannot be joined to the project that built it, and the as-built drawings, test records and structural certificates permanently retained under module 15 become unreachable |
| 2 | **Generation monitoring moves off the project record.** `generation_monitoring_source` and `generation_monitoring_access` are removed from `project` and live on `serviced_asset` | Two places asserted the field; none held a reading |
| 3 | **`party_type` gains `operations_and_maintenance_provider`** | `project_party` already carries the role; the party enumeration did not |
| 4 | **`contract` gains `warranty_months`**, alongside `retention_release_months` | The turnover date starts a warranty clock, but nothing held a warranty duration. Retention was computable; warranty was not. Same pattern, same table |
| 5 | **`write_off.subject` gains `service_charge`** | Gates 1, 2 and 3 approve the only write-off record in the platform. A service charge must reach that path, not invent its own |
| 6 | **`cash_forecast_line.source_object` accepts `service_charge`** | Otherwise recurring revenue cannot enter the twelve-month forecast |
| 7 | **The six permanent retention classes in module 15 become eight:** service agreements, and work-order evidence | A warranty claim in year eight is answered by the year-one work order or it is not answered |

**And the sidebar gains an eighteenth item:** *Operations and Maintenance*, after Safety and before Documents — the work that happens once construction ends.

### 8.23.2 Gate decisions — recorded, approved by the Chief Executive Officer on 2 September 2026

The gate list was closed at twenty-eight and the identifier space fixed at 1 to 33. This module needs three things the list did not provide, and a module that quietly adds a gate is the failure the closed list exists to prevent. **The three below are governance acts, recorded here as decided.**

| Need | Decision |
|---|---|
| Service agreement signature | **Gate 9 is extended** to any signed customer agreement, not only an engineering, procurement and construction contract. No new number |
| Service charge approval | **Gate 11 is extended** to a service charge. Gate 11's original trigger was a progress claim keyed to a project with a percentage complete; a service charge is neither. This is an extension, and it is recorded as one |
| Warranty claim submission | **Gate 34 is added — Warranty claim submission · all · Head of Finance · alternate Chief Operating Officer · window 3 working days (recorded only).** A claim against a supplier commits Magnus's position. **The gate list now has twenty-nine gates and thirty seed rows; the identifier space runs 1 to 34; 13 to 17 remain reserved** |

**No hard block is added, and none is extended.** Hard block 6 is *fund release without a signed contract* and is not extended to service charges. Issuing an invoice is neither law, nor irreversibly committed money, nor an irreversible physical act. **The protection is structural instead:** a charge is created only from an `active` agreement, and `active` is unreachable without the signed document. The unsigned case cannot arise.

### 8.23.3 Objects

**`service_agreement`** — service_agreement_id · **site_id (required — the agreement attaches to the site, never to a project)** · account_id (the counterparty) · project_id (optional — present where Magnus built the asset, empty for third-party service) · **agreement_document_id (required to reach `active`; the signed document is the record, and a field asserting an agreement exists does not satisfy it)** · commencement_date · term_months · **expiry_date (derived from commencement plus term at activation, in the same transaction — never typed)** · **renewal_notice_days (configuration, default 90, gate 31)** · predecessor_agreement_id · successor_agreement_id · scope_of_service (`preventive`/`corrective`/`preventive_and_corrective`/`monitoring_only`) · charge_basis (`fixed_periodic`/`per_kilowatt_peak`/`per_visit`/`hybrid`) · charge_amount · charge_period (`monthly`/`quarterly`/`annual`) · escalation_percentage · escalation_month · **state (stored: `draft`/`active`/`renewed`/`terminated`)** · **effective_status (derived on read — section 8.23.4)**.

**`service_level_term`** — service_level_term_id · service_agreement_id · **severity (`total_outage`/`partial_outage`/`degraded`/`cosmetic`)** · **response_hours (elapsed hours to first response)** · **restoration_hours (elapsed hours to service restored)**. **One row per agreement per severity — not two columns on the agreement. These rows are what Magnus sells.** An agreement with no service level terms is one nobody can be held to and nobody can be shown to have met; `active` is refused without at least one.

**Severity governs the promise. It never governs ranking.** The executive view ranks by estimated lost generation valued at that site's tariff — never by a severity label. Both statements are true and neither may be used for the other's purpose.

**`serviced_asset`** — serviced_asset_id · site_id · service_agreement_id (optional — an asset may be monitored before it is contracted) · project_id · design_package_id (both optional, present only where Magnus built it) · capacity_kilowatt_peak · commissioning_date · **warranty_expiry_date (derived as turnover date plus `contract.warranty_months` where a project exists — computed in whichever transaction comes second, the asset's creation or the turnover date's entry; typed only where Magnus did not build the asset)** · **generation_monitoring_source · generation_monitoring_access (moved here from the project)** · **expected_annual_yield_kilowatt_hours (derived at asset creation — capacity × the specific-yield constant in force that day, storing the constant version used; recomputed only when capacity changes; never typed)** · **tariff_per_kilowatt_hour (site-specific — values lost generation)** · state (`monitored`/`under_service`/`service_lapsed`/`decommissioned`).

**This is the object the original specification said does not exist. It exists here.**

**`serviced_asset_equipment`** — serviced_asset_equipment_id · serviced_asset_id · item_id (optional, where the model is in the catalogue) · equipment_class (`panel`/`inverter`/`battery`/`mounting`/`monitoring`/`other`) · manufacturer · model · serial_number · quantity · installed_date.

**`generation_reading`** — generation_reading_id · serviced_asset_id · period_start · period_end · granularity (`daily`/`monthly`) · generated_kilowatt_hours · ingestion_source (`manual`/`portal_export`/`integration`) · ingested_at. **Without this object nothing in underperformance, lost-generation valuation or the operations domain can run.** Populating it is a data task, not a design task, and it is the single highest-value input this module has.

**`maintenance_plan`** — maintenance_plan_id · service_agreement_id · activity · **interval_months (configuration default per activity, gate 31)** · first_due_date · **next_due_date (stored; advanced by `interval_months` in the same transaction that closes a preventive work order raised from this plan)** · estimated_hours · required_capability (capability tag) · is_active.

**A maintenance plan does not do the work and does not create the task.** It holds the cadence and the next due date — the definition of a recurring obligation, section 16 deviation D11. **A person or an agent reading `next_due_date` creates the task with `source = recurring`, and a work order is raised from that task when the visit is actually scheduled.** The plan is the obligation; the task is the commitment; the work order is the visit. **No scheduler instantiates any of them.**

**`work_order`** — work_order_id · serviced_asset_id · service_agreement_id (optional — goodwill and warranty work happens outside an agreement) · originating_task_id · origin (`preventive`/`fault`/`client_request`/`warranty`/`monitoring_alert`) · **severity (selects which `service_level_term` row applies)** · **raised_on_device · raised_received_by_server** · **responded_on_device · responded_received_by_server (stamped on `in_progress`)** · **restored_on_device · restored_received_by_server (stamped on `restored`)** · closed_at (server time — closure is an office act, not a field act) · reported_by · assigned_to · assigned_at · fault_description · root_cause · action_taken (**all three required to reach `closed`**) · parts_used (item references — operations and maintenance spares, module 10) · **evidence_document_id (required to reach `closed`)** · **is_billable (default false — out-of-scope work is billable)** · state.

**Field-captured. Dual timestamps apply.** **A billable work order does not carry an amount.** It sets `is_billable`, and the service charge is created from it in the same transaction. **No screen accepts a typed charge.**

**The assigned owner must be a person who signs in.** Crew members do not sign in and cannot transition a work order; they are named in the visit's attendance, never as the owner.

**`warranty_claim`** — warranty_claim_id · serviced_asset_id · work_order_id (the work that found it) · **claimed_against (`supplier`/`subcontractor`/`magnus`)** · **purchase_order_id (required where `claimed_against` is `supplier` — supplier warranty lives on the purchase order, not on the client contract)** · contract_id · clause_family (where `claimed_against` is `magnus` and a contract exists — points at clause family 5, warranty and defects liability) · raised_at · claim_value · **evidence_document_id (required)** · state.

**A claim needs a source, and which source depends on who is being claimed against.** Requiring a client-contract clause on every claim would make a supplier claim impossible on an asset Magnus did not build. The rule: `supplier` requires a purchase order · `magnus` requires a contract clause where a contract exists · `subcontractor` requires evidence and a named party. **A defect claim in year three is answered by the year-one record or it is not answered at all. This object is what makes the year-one record reachable.**

**`service_charge`** — service_charge_id · service_agreement_id · work_order_id (set for a billable out-of-scope visit) · period_start · period_end · **amount (generated from the agreement or the work order — never typed)** · basis (copied from the agreement at creation) · state.

**Which charges activation creates depends on `charge_basis`:** `fixed_periodic` — one charge per `charge_period` for the term, at `charge_amount` · `per_kilowatt_peak` — one per period, amount derived as `charge_amount` × the summed `capacity_kilowatt_peak` of the assets under the agreement at activation · `hybrid` — the periodic component as above, plus per-visit charges from billable work orders · **`per_visit` — no charge at activation; every charge comes from a billable work order.** Escalation applies to periods after `escalation_month` in each year.

**This is not a `billing_milestone`.** A milestone is keyed to a project and generated at contract signature. **A service charge has no milestone, no percentage complete and no completion. It recurs until the agreement ends.** Both feed the same cash forecast under `secured` once issued. **There is no `written_off` state** — an uncollectable charge goes to `write_off` under the ladder, amendment 5.

### 8.23.4 States and transitions

**`service_agreement` — stored state and derived status.** The stored `state` moves only by a human hand. **`effective_status` is computed on read from the stored dates, and this is how the module holds its clocks without a timer:**

| Effective status | Computed when |
|---|---|
| `draft` · `renewed` · `terminated` | The stored state, as is |
| `active` | Stored state `active` and today is before `expiry_date` minus `renewal_notice_days` |
| **`expiring`** | Stored state `active` and today is on or after `expiry_date` minus `renewal_notice_days` and before `expiry_date` |
| **`lapsed`** | Stored state `active`, today is on or after `expiry_date`, and `successor_agreement_id` is empty |

**`lapsed` is reached by the passage of time, not by a person — and not by a timer either.** It is a fact about two stored dates, visible the moment anyone or any agent asks. The ninety-day renewal threshold had no home in the original specification; this is the home.

| From | To | Who | Condition |
|---|---|---|---|
| `draft` | `active` | Director | **`agreement_document_id` present AND at least one `service_level_term` row. Refused otherwise.** In the same transaction: `expiry_date` is computed, and every `service_charge` for the term is created in state `scheduled` with escalation applied to periods after `escalation_month` |
| `active` | `active` | Director | Term extended in place — `expiry_date` moves and the charges for the added periods are created in the same transaction |
| `active` | `renewed` | Director | A successor agreement reaches `active` and `successor_agreement_id` is set; the successor carries `predecessor_agreement_id` |
| `active` | `terminated` | Chief Operating Officer | Either party terminates. **Reason required.** Charges in `scheduled` for periods after termination are cancelled in the same transaction |

**`work_order`** — `raised` · `assigned` · `in_progress` · `restored` · `closed` · `cancelled`.

| From | To | Who | Condition |
|---|---|---|---|
| `raised` | `assigned` | Project Manager, Director, or the site's Person In Charge | An owner is named; stamps `assigned_at`. **Raises a Task notification to the owner in the same transaction** |
| `assigned` | `in_progress` | Assigned owner | Work starts. **Stamps `responded_on_device` — this stops the response clock** |
| `in_progress` | `restored` | Assigned owner | Service restored. **Stamps `restored_on_device` — this stops the restoration clock** |
| `in_progress` | `closed` | Assigned owner | **`origin` is `preventive` only.** Nothing was broken, so nothing is restored. **Advances the originating maintenance plan's `next_due_date` in the same transaction** |
| `restored` | `closed` | Assigned owner | `root_cause`, `action_taken` and `evidence_document_id` all present. **If `is_billable`, the service charge is created in the same transaction** |
| any | `cancelled` | Project Manager or Director | **Reason required** |

**`restored` and `closed` are separate on purpose.** Restoration is what the client experiences and what the service level measures; closure is what the record needs. Collapsing them loses the measurement. **A preventive visit never passes through `restored`** — forcing it would stamp a restoration time on work where nothing failed.

**Offline rule for work orders — settling the open dependency on module 23.** A work order is raised offline like any field record. **The assigned owner, and only the assigned owner, may capture the `in_progress` and `restored` transitions offline**, because the device timestamp on those two transitions is the service level measurement itself, and a record with one assigned writer is not a shared record. Both queue with a device-generated idempotency key. Every other transition — assign, close, cancel — is online.

**`warranty_claim`** — stored `raised` · `submitted` · `accepted` · `rejected` · `settled`; **derived `expired` on read** where the asset's `warranty_expiry_date` has passed and the stored state is `raised` or `submitted`.

| From | To | Who | Condition |
|---|---|---|---|
| `raised` | `submitted` | Head of Finance | **Gate 34.** Claim sent to the counterparty — this commits Magnus's position |
| `submitted` | `accepted` · `rejected` | Head of Finance | Counterparty responds. Rejection requires a reason |
| `accepted` | `settled` | Head of Finance | Value received or credited |

**`service_charge`** — `scheduled` · `approved` · `issued` · `paid` · `cancelled`.

| From | To | Who | Condition |
|---|---|---|---|
| — | `scheduled` | Same-transaction derivation | Created at agreement activation for every period in the term, or when a billable work order closes. **Never by a scheduler, never typed** |
| `scheduled` | `approved` | Head of Finance | **Gate 11** |
| `approved` | `issued` | Head of Finance | Sent to the client. **Enters the cash forecast under `secured`** |
| `issued` | `paid` | Head of Finance | Payment received |
| `scheduled` · `approved` | `cancelled` | Head of Finance | Reason required |

### 8.23.5 Service level measurement — computed on read

| Measure | Derivation |
|---|---|
| **Response** | `responded_on_device` − `raised_on_device`, against `response_hours` of the `service_level_term` matching the work order's severity |
| **Restoration** | `restored_on_device` − `raised_on_device`, against `restoration_hours` |

**Both use device time. Both are measured in elapsed hours, not working hours — a system down on a Saturday is down.**

**The service level is reported, never scored against a person.** A breach is a fact about a promise, not a fact about an engineer. No screen, query or export aggregates breaches by named engineer.

### 8.23.6 Generation and underperformance

`expected_annual_yield_kilowatt_hours` is derived from capacity and the effective-dated specific-yield constant; actual generation comes from `generation_reading`. **Underperformance is the shortfall, valued at `tariff_per_kilowatt_hour`.** That valuation is what ranks the operations and maintenance exception — by estimated lost generation valued at that site's tariff, not by a severity label. **Two sites with equal shortfall and different tariffs rank the higher-tariff site above.**

### 8.23.7 Gates that apply

Gates 1, 2, 3 — the write-off ladder, where a service charge becomes uncollectable · **gate 9** — service agreement signature, as extended · **gate 11** — service charge approval, as extended · gate 19 — non-conformance closure, only where a work order raises one on an asset that has a project, since `non_conformance_report.project_id` is required · gate 22 — the specific-yield constant · gate 31 — `renewal_notice_days`, plan intervals, the warranty-expiry warning window · gate 33 — agreements and evidence classification · **gate 34** — warranty claim submission.

### 8.23.8 Notifications and queries

**Two things exist, they look similar, and they must not share a code path.** Notifications below are raised in the same transaction as the human action that causes them. Everything time-based is a query, evaluated on request, that an agent reads.

**Notifications raised in the same transaction:**

| Human action | Notification | To | Cleared by |
|---|---|---|---|
| Work order assigned | **Task** | Assigned owner | Work reaches `in_progress` |
| Agreement activated | **Task** — the first scheduled charge | Head of Finance | Charge reaches `approved` |
| Billable work order closed | **Task** — the charge | Head of Finance | Charge reaches `approved` |
| Warranty claim raised | **Task** | Head of Finance | Claim reaches `submitted` |
| Asset created with no active agreement | **Information** | Account executive | — |

**Queries — each returning its own evaluation timestamp:**

Agreements with effective status `expiring`, with days to expiry · agreements with effective status `lapsed`, with days since · maintenance plans with `next_due_date` within N days, and those past due with no task · work orders in `assigned` or `in_progress` past their `response_hours`, with hours over · work orders in `in_progress` past their `restoration_hours`, with hours over · warranty expiring within the configured window with an open work order on the asset · warranty claims in `raised` or `submitted` with derived status `expired` · underperforming assets, shortfall valued at site tariff, ranked · service charges `issued` and unpaid beyond the agreement's payment terms · serviced assets with no agreement · serviced assets with no generation reading in the last N days.

**Recipients and scopes are by account, not by project**, because a serviced site may have no Project Manager.

### 8.23.9 Permissions

| Role | Agreements | Work orders | Charges | Service level | Claims |
|---|---|---|---|---|---|
| Chief Operating Officer | all | all | view | all | view |
| Director | own accounts, full | own accounts | view | own accounts | view |
| Head of Finance | view | view | **full** | view | **full** |
| Account executive | own accounts | view | view | own accounts | none |
| Project Manager | view, own sites | own site orders | none | own sites | none |
| **Person In Charge** | **none** | **own site only — raise, assign, update** | **none** | **none** | **none** |

Money visibility and record scope apply unchanged.

### 8.23.10 Reports and accumulated data

**Reports:** service level attainment by agreement and period · response and restoration distribution by severity · work orders by origin, preventive against corrective · **recurring service revenue by client and period** · agreements expiring in the next two quarters · warranty claims raised, settled and expired, with value · lost generation by site, valued · parts consumption from operations and maintenance spares · **cost to serve against charge, by agreement — the margin question for the service line.**

**Accumulated, never maintained, always with sample size:** mean time to respond and to restore, by severity · **failure rate by equipment model and age — the input a later predictive phase needs** · warranty claim success rate by supplier, feeding procurement · actual cost to serve against agreement value, feeding pricing.

### 8.23.11 Model Context Protocol

All six objects are exposed for read, write and search under section 12, and all eleven queries above are read tools. `renewal_notice_days`, plan intervals and the warranty-expiry window are configuration tools under gate 31. **No agent creates, assigns, closes or prioritises a work order except as an authenticated person, through the write tools, logged under that person's name.**

### 8.23.12 Migration

Existing agreements are loaded with their signed documents, commencement dates and terms; **an agreement whose document is not loaded stays `draft` and produces no charge.** In-force warranties are loaded with their expiry dates. Open work orders are loaded with their device-side raised timestamps where known, and with the server timestamp otherwise, marked as migrated.

### 8.23.13 Deliberately not built

| Not built | Why |
|---|---|
| A timer that moves an agreement to `expiring` or `lapsed`, or a claim to `expired` | Section 1. These are derived statuses computed from stored dates |
| A scheduler that creates service charges, maintenance tasks or work orders | Section 1. Charges are created at activation; tasks by a person or agent; work orders by a person |
| Predictive failure modelling · automatic work-order dispatch · yield-degradation forecasting | Need accumulated service history |
| A client-facing service portal | A later phase |
| A separate service-line general ledger | One sub-ledger, not two |
| A `written_off` state on the service charge | The write-off ladder holds the only write-off path |
| Technician utilisation as a score | Workload is visible; presence is never tracked, and neither produces a rating |
| Severity as a ranking input | Ranking is by valued lost generation, not by label |
| A spare-parts module of its own | Module 10 already holds operations and maintenance spares |
| Service level in working hours | A system down on a Saturday is down |
| A typed service charge | Generated or it is not a charge |
| A seventh hard block | Issuing an invoice is not law, irreversible money or an irreversible physical act |
| Any gate beyond 34, or any widening of 9 or 11 beyond what is recorded above | The list is closed again at twenty-nine |

---

## ACCEPTANCE TESTS — APPEND TO SECTION 14 AS TESTS 190 TO 214

## Operations and maintenance

190. **An agreement attaches to a site, not a project.** Create an agreement on a site with no project. It activates and functions fully.
191. **A signed document is required.** Attempt `draft` → `active` with no `agreement_document_id`. Must fail.
192. **Service level terms are required.** Attempt `draft` → `active` with no `service_level_term` row. Must fail.
193. **No charge without an active agreement.** Confirm no code path creates a `service_charge` for a `draft` agreement, and that activation is the only path that creates the term's charges — in the same mutation.
194. **Expiring is derived, not fired.** Set expiry 89 days out with a 90-day notice period. The agreement's effective status reads `expiring` on the next read, with no stored transition, no timer and nothing in the audit log.
195. **Lapse is derived, not fired.** Let an expiring agreement pass expiry with no successor. Effective status reads `lapsed`; the lapsed query returns it with days since; nothing ran.
196. **Renewal links both ways.** Sign a successor. Predecessor reaches `renewed`; both carry the link.
197. **Dual timestamps on field capture.** Raise a work order offline; synchronise later. Both `raised_on_device` and `raised_received_by_server` are stored and differ.
198. **Response is measured in elapsed device hours.** Raise at 17:00 Friday on device, respond 10:00 Monday. 65 hours, not one working hour, measured off device time.
199. **Severity selects the promise.** Two work orders, different severities, same agreement. Each measures against its own `service_level_term` row.
200. **A preventive visit does not pass through `restored`.** Close a preventive work order. `in_progress` → `closed` directly; `restored_on_device` stays empty; the originating plan's `next_due_date` advances by its interval in the same mutation.
201. **Service level breaches are never scored against a person.** No screen, query or export aggregates breaches by named engineer.
202. **A maintenance plan holds the cadence and creates nothing.** Activate a plan with a 3-month interval. `next_due_date` is set; no task exists until a person or an agent creates one; the past-due query lists the plan.
203. **A supplier claim needs a purchase order, not a client clause.** Raise a supplier claim on an asset with no project. Succeeds with `purchase_order_id`; fails without.
204. **An asset works with no project.** Create a serviced asset with `project_id` empty. Every function in this module works.
205. **Warranty expiry with open work is queryable.** Open a work order, set warranty expiry inside the window. The warranty-expiring query returns it before expiry.
206. **A service charge is generated, never typed.** No screen accepts a typed charge amount; a billable work order closing creates its charge in the same mutation.
207. **Recurring revenue reaches the forecast.** Issue a service charge. It appears in the twelve-month forecast under `secured`.
208. **A service charge cannot be written off outside the ladder.** Attempt to write off a charge without gates 1 to 3. Must fail.
209. **Lost generation values at site tariff.** Two sites, equal shortfall, different tariffs. The higher-tariff site ranks above.
210. **Yield uses the effective-dated constant.** Change the specific-yield constant. Existing assets keep the version they were derived under.
211. **Nothing dispatches.** Confirm no code path inside the platform creates, assigns, closes or prioritises a work order except a mutation called by an authenticated person, through the screen or the Model Context Protocol, logged under that person's name.
212. **Every operations query returns its evaluation timestamp** and works with no agent connected.
213. **Gate 34 fires.** Attempt `raised` → `submitted` on a warranty claim without Head of Finance approval. Must fail. Confirm the gate table holds thirty rows and no row 13 to 17.
214. **Offline transitions are owner-only.** As a person who is not the assigned owner, attempt an offline `in_progress` transition. Refused. As the assigned owner, it queues with an idempotency key and posts once.

---

---

# PART C — COMMUNICATION AND GOOGLE DRIVE (Milestones 1 and 7)

## A. COMMUNICATION — WHAT MAGNUS ACTUALLY NEEDS

## A1 · The Messages screen is one place for every conversation

One screen, reached from the sidebar item *Messages*, laid out like Google Chat: a left panel and a conversation pane.

Left panel, in this order, each with an unread count:

1. **Direct** — one-to-one conversations with people in the company.
2. **Spaces** — account spaces (A2), project channels, department channels, and invite-only groups (A3).
3. **Threads** — record threads the person has posted on or been mentioned in, newest activity first, each showing the record it belongs to.

An unread count is a display state per person per conversation. **It is not a notification.** Notifications are still created only by a mention or a direct message, section 8.13. A person clears an unread count by opening the conversation. There is no mark-all-read that touches notifications.

The conversation pane shows messages newest at the bottom, the composer, attachments, reactions, pin, bookmark, quote, reply, and **convert to task in one tap**. Every message shows author, sent time and, where different, the device time it was composed. A hidden message shows that a message was hidden, who hid it and why.

**Speed rule, from section 8.13 and measured in test 244:** from opening the application on a phone, a message on a project channel or a record thread takes no more taps than posting in a Messenger group. If it does, the screen is wrong.

## A2 · The account space: one conversation per customer, for the life of the customer

**`channel.channel_type` gains `account`.** An account space is created in the same transaction as the account in Pipeline, linked to the account, and lives as long as the account. It is internal only. Client contacts never see it and cannot be members.

**What it shows.** Its own messages, plus every record thread under the account rolled up in one view: the opportunities and proposals in Pipeline, the site assessment, the design package and its deliverables, the project, its blocks, site reports, permits, purchase orders, non-conformance reports, variation orders, progress claims, and after turnover the service agreements, serviced assets and work orders on that account's sites. Each rolled-up message shows which record it was posted on and opens that record. **A message posted from the account space view onto a record thread is stored on that record thread**, not on the space; the composer shows which thread it will post to, and the default when nothing is selected is the space itself.

**Membership is automatic and logged.** A person joins the account space when assigned to anything under the account: sales owner on the opportunity, Director on the project, Project Manager, design engineer on a deliverable, Person In Charge on a site report, procurement officer on a purchase order, assigned owner on a work order. A person leaves the space when no assignment under the account remains, except Directors and console holders, who remain. A person may also be invited by a current member, logged, and removed by the inviter or a Director, logged. Membership changes never delete history.

**Record scope still governs.** A person who may not see the project's money sees the messages but not the figures the record carries; the roll-up shows message text, never a monetary field.

## A3 · Invite-only groups

**`channel.channel_type` gains `group`.** Any person creates a group, names it, and invites members. **Only members see that the group exists, its membership and its messages.** The creator is the owner; the owner may hand ownership to another member. Members may leave; the owner may remove a member, logged. A group with no owner passes to its longest-standing member. A group is closed, never deleted; a closed group is read-only to its members and searchable by them.

**Groups are not secret from the record.** Two rules keep them answerable years later, and both are visible to every member on the group's information panel so nobody is surprised:

- A console holder may open a group they are not a member of only through a logged *access for review* action that requires a reason and notifies the owner. Hiding a message inside a group follows the same path.
- Legal hold applies to a group like any thread.

Department channels and project channels stay as specified: membership follows roles and assignment automatically, and no invitation is needed.

## A4 · Direct messages

Internal only. Two people, or one person and themselves as notes. A direct message notifies without a mention, section 8.13. Searchable by its two participants only. No group direct message: three people is a group.

## A5 · Everything else in section 8.13 stands

Mention as the only attention mechanism · exactly one person per mention · no subscription, no watch, no mute · append-only, hide only by an administrator with reason · search across message text, attachment filenames and the owning record, scoped by record scope and, for groups and direct messages, by membership · convert to task in one tap, output type required · the site-report prompt when a photograph is offered on a block thread · offline compose queue, composition order, de-duplication by `client_message_key`, text before attachments · reactions, pin, bookmark, quote, reply · legal hold.

## A6 · Read tool for reports

Add to the protocol's read scope: `get_account_activity(account_id, from, to)` returning every record and every message under the account in the window, with sources, respecting record scope and money visibility and excluding groups and direct messages the caller is not a member of. This is what an agent uses to draft a client report; the report itself is written outside the platform and stored under Documents when a person files it.

---

## B. GOOGLE DRIVE AS THE FILE STORE

**Principle: Drive is the disk. The platform is the index.** The platform is the only writer to the folder tree. People open files through the platform. Nobody browses, renames, moves or replaces a file in Drive, because the revision-in-force rule of section 8.14 and the toolbox photograph's place in the payroll chain both depend on the file being exactly what the record says it is.

## B1 · Connection

In Administration, under Integrations, a console holder connects one Google account by OAuth. **It is a dedicated Google account owned by Magnus for this purpose, not a person's own account: [DRIVE ACCOUNT EMAIL].** Request only the scope that limits access to files the application created. The connection stores the refresh token encrypted, the account's email, the root folder identifier, when it was connected and by whom. Disconnecting is logged and does not delete anything in Drive. The connection state, quota used and the count of files pending upload are shown on the same screen.

## B2 · The `file` record

Every stored file has one record: `file_id` · `drive_file_id` · `drive_folder_path` · `original_name` · `mime_type` · `size_bytes` · **`sha256` computed at upload, before Drive** · `uploaded_by` · `uploaded_on_device` · `received_by_server` · `capture_source` (`in_app_camera` / `file`) · `attached_to_object` · `storage_state` (`staged` / `in_drive` / `verified` / `erased`) · `legal_hold`. Attachments, document revisions, toolbox photographs, site photographs, contract documents, insurance certificates, evidence documents and every other stored file reference a `file` record. Existing code that references a Convex storage identifier directly is changed to reference `file_id`.

## B3 · Upload path

1. A phone or browser uploads to the platform exactly as today. Field uploads still go through the offline queue. **A device never talks to Drive.**
2. The server computes `sha256`, writes the `file` record as `staged` with the bytes in platform storage, and in the same request attempts the Drive upload into the derived folder.
3. On success the record becomes `in_drive` with `drive_file_id`, and the staged bytes are removed.
4. On failure the record stays `staged`. **Nothing retries by itself**, section 1 of the original instruction. The Integrations screen shows the pending count, the protocol exposes `list_files_pending_drive` and `push_pending_files_to_drive`, and any later successful upload by any person also pushes up to twenty pending files in the same request. A staged file is fully usable inside the platform meanwhile.
5. `verify_file(file_id)` re-reads the bytes from Drive, recomputes the hash and sets `verified` or raises a discrepancy naming the file. `verify_audit_chain` gains an option to verify every file referenced by the entries in its range.

## B4 · Reading path

Files are served through the platform, which fetches from Drive using the connection and streams to the person after the same permission check the record carries. **No Drive sharing link is ever issued to a person.** Thumbnails for photographs are generated once at upload and stored beside the file in the same folder.

## B5 · Folder tree, derived from the record, never typed

Root: **Magnus Platform**. Second level: the module name exactly as it appears in the sidebar. Third level: the object, as its number and name. Below that, the sub-object. Examples:

| Record | Folder |
|---|---|
| Toolbox photograph, site report workday 63 on PRJ-2026-0001 | Magnus Platform / Projects / PRJ-2026-0001 Calamba Agro Industrial Corporation / Site Reports / 2026-09-03 workday 63 / |
| Signed contract | Magnus Platform / Projects / PRJ-2026-0001 Calamba Agro Industrial Corporation / Contract / |
| Drawing revision 3 | Magnus Platform / Documents / DWG-0412 Single line diagram / Revision 3 / |
| Goods receipt photograph | Magnus Platform / Procurement / PO-2026-044 Nordwind Energy GmbH / Goods Receipts / 2026-10-05 / |
| Incident evidence | Magnus Platform / Safety / INC-2026-007 / |
| Work order evidence | Magnus Platform / Operations and Maintenance / OM-2024-003 Lipa Cold Storage and Logistics Inc. / Work Orders / WO-2026-018 / |
| Message attachment on a block thread | Magnus Platform / Projects / PRJ-2026-0001 Calamba Agro Industrial Corporation / Messages / B1 / |
| Message attachment in a group | Magnus Platform / Messages / Groups / Bicol procurement / |
| Proposal PDF | Magnus Platform / Pipeline / ACC-0012 Calamba Agro Industrial Corporation / OPP-2026-031 / |

Folder names are created on first use. A renamed project renames its folder; Drive file identifiers do not change, so no record breaks. A file name inside a folder is the platform's `file_id` plus the original extension, with the original name kept on the record, so two uploads named `photo.jpg` never collide.

## B6 · Retention and erasure

A retention schedule or a cryptographic erasure request executed by a person under the existing rules deletes the Drive file permanently through the connection, sets `storage_state` to `erased`, keeps the record with its hash, and writes the audit entry. Legal hold refuses it. Nothing deletes on a timer.

## B7 · Moving what is already stored

A one-time action on the Integrations screen, run by a console holder, moves every file currently in platform storage into Drive under the derived folder tree, one batch at a time, showing progress and the count remaining. Each moved file is hashed before and verified after. The action stops on the first discrepancy and reports it. It may be run again to continue.

## B8 · Later move to Google Workspace

The connection is designed so the root folder can be transferred to a Workspace shared drive later with file identifiers intact. Store nothing that depends on the owning account's email.

---

## C. ACCEPTANCE TESTS — APPEND TO SECTION 14 AS TESTS 237 TO 258

## Communication

237. **One screen.** Messages shows Direct, Spaces and Threads with unread counts; opening a conversation clears its count and creates no notification.
238. **Account space is born with the account.** Creating an account creates its space in the same transaction; no separate action.
239. **Roll-up reads across the lifecycle.** Post on the opportunity thread, the project thread, a block thread, a site report thread and a work order thread under one account; the account space shows all five in order, each opening its record.
240. **Post from the roll-up lands on the record.** From the account space, post onto the block thread; the message is stored on the block, not the space.
241. **Automatic membership.** Assign a person as Person In Charge on a site report under the account; they are in the space. Remove the assignment; they are out, and their past messages remain.
242. **Money never rolls up.** A Person In Charge reads the account space; no monetary figure appears in any rolled-up message or record preview.
243. **Invite-only is invisible.** Create a group with two members. A third person cannot find it by search, by list, or by identifier. A console holder cannot read it without *access for review*, which requires a reason and notifies the owner.
244. **Speed.** On a phone, from the home screen to a sent message on a project channel: count the taps. Record it against a Messenger group post. It must not be more.
245. **Convert to task in one tap.** From a message, one tap opens the task with the message quoted; output type required.
246. **No mute anywhere.** Search every screen for mute, watch, subscribe, follow. None exists.
247. **Append-only.** Edit and delete do not exist; hide by an administrator is logged and visible in the thread.
248. **Offline order.** Text, photograph, text composed offline arrive in that order; the photograph never delays the third message; no duplicate after three reconnects.
249. **Direct message notifies without a mention.** Exactly one notification, opening the conversation.
250. **Group ownership passes.** Owner leaves; longest-standing member becomes owner; logged.
251. **Account activity read tool.** `get_account_activity` returns records and messages under the account with sources and excludes a group the caller is not in.

## Drive

252. **Device never touches Drive.** Inspect the client bundle and network calls: no Drive endpoint, no Drive token.
253. **Hash before Drive.** Upload a file; the record carries `sha256` before `drive_file_id`. Replace the file in Drive by hand; `verify_file` reports the discrepancy.
254. **Folder derived.** Upload a toolbox photograph on workday 63 of PRJ-2026-0001; it lands in the folder in B5 exactly. Rename the project; the folder renames; the file still opens from the site report.
255. **Staged survives Drive failure.** Disconnect Drive; upload; the file is `staged`, usable in the platform, counted on Integrations; nothing retries by itself. Reconnect; the next upload pushes it; `push_pending_files_to_drive` pushes the rest.
256. **No sharing links.** Open a file as a person; the network shows the platform serving it; no Drive link is issued.
257. **Legal hold refuses erasure.** Place a hold; execute erasure; refused. Release; execute; the Drive file is gone, the record remains with hash and state `erased`.
258. **Move existing files.** Run B7 on the current store; every file moves, verifies, and every record still opens its file.

---

---

# PART P — THE PROTOCOL: SCOPES, DECIDE, MIGRATE (Milestone 8)

## A. DEFECTS FOUND ON THE ENDPOINT — CLOSE THESE FIRST

**A1 · `hardBlock6Active` reports false on a project with no contract.** `get_finance_summary` on PRJ-2026-0001 returned `contractValue: null` and `hardBlock6Active: false`. Hard block 6 is in force on every project whose `contract_id` is empty. Either the flag is inverted or the evaluation is wrong. Fix the evaluation and rename the field to `fundsBlockedNoContract` so its meaning cannot be misread.

**A2 · `project` carries no site and no client.** `list_projects` returns `opportunityId`, `proposalId` and `siteAssessmentId` but no `siteId` and no client party. Amendment 1 of section 8.23.1 makes `site_id` required on `project`, carried across by the `won` handover, and section 8.4 requires `client` as a reference to `party`. Add both, populate them on the five existing projects from their opportunities, and return them from every project read.

**A3 · Figures return without their records.** Section 12.1: every figure returned cites the records it came from. `get_finance_summary`, `get_inventory_summary`, `get_board_pack` and every exception report return bare totals. Every returned figure carries a `sources` list of record identifiers, and every exception carries the record it was computed from and the person it names.

**A4 · Construction and procurement exception reports evaluate zero rules.** A domain that evaluates no rules is not silence stating what was checked; it is a blank panel, test 152. Implement at minimum: projects with no submitted site report in the last two working days · blocked activities with reason and expected clear date · blocks not startable with mobilisation planned · non-conformance reports open with ageing · purchase orders past expected arrival · goods received short or damaged with no non-conformance report · quarantined material by value and age · transmittals in transit beyond expected days · prerequisite permits outstanding.

**A5 · The audit chain panel shows "Last sequence: 100" while the newest entry is 149.** The panel shows the true last sequence number and the exact range verified, for example "verified entries 50 to 149, last sequence 149".

**A6 · Sidebar drift.** The sidebar shows *Tasks* and *Construction* as separate items and *Design & Engineering* with an ampersand. Section 13 fixes the order: Dashboard · My Day · Pipeline · Projects · Design and Engineering · Procurement · Permits · Inventory · Manpower and Equipment · Safety · Operations and Maintenance · Documents · Messages · Finance · Human Resource · Payroll · Reports · Administration. Tasks live inside My Day; blocks and site reports live inside Projects. *Migration and Cutover* may stay as the last item until the cutover date, after which it is hidden. Part I governs the sidebar and labels; apply it in milestone 9.

---

## B. COMPLETE SECTION 12 — READ, WRITE, DECIDE

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

## C. THE MIGRATE SCOPE — SECTION 8.21 IMPORT PATH OVER THE PROTOCOL

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

## D. ACCEPTANCE TESTS — APPEND TO SECTION 14 AS TESTS 215 TO 236

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

---

# PART I — INTERFACE, LABELS AND USABILITY (Milestone 9)

## I1 · Theme

**I1.1** Light theme by default: white cards on a light neutral ground, dark grey text, one accent colour used for primary actions, active navigation, links and focus. The accent is the Magnus orange from the logo flame. Use these values as design tokens, never as literals scattered through components:

| Token | Value | Use |
|---|---|---|
| accent | #F06818 | primary buttons, active navigation, selected tabs, progress; white text on it only at 18 point or larger, or bold 14 point |
| accent-hover | #D45410 | hover and pressed state |
| accent-text | #C24A0C | links and accent-coloured text on white or light ground (contrast 4.9 to 1) |
| accent-amber | #F8A828 | highlights, badges and charts only, never text |
| accent-tint | #FFF1E8 | selected rows, active sidebar background, notification chips |
| ground | #F5F6F7 | page background |
| surface | #FFFFFF | cards, dialogs, sidebar |
| text | #1F2937 | body text |
| text-muted | #6B7280 | secondary text |
| border | #E5E7EB | dividers and card edges |

The logo keeps its own blue and orange. Blue is not used as an accent anywhere else, and the logo image is the one from the Magnus letterhead. Refusals and hard block messages use a red that is distinct from the accent; warnings amber; success green; none of the three is the accent.

**I1.2** The field screens, site report, toolbox meeting, safety forms and the emergency card, are tested in direct sunlight on a phone: larger type, higher contrast, and a high-contrast switch on the person's profile that applies only to that person.

**I1.3** Dark theme remains available as a personal setting; it is not the default.

## I2 · Sidebar and headers

**I2.1** Exactly eighteen items, this order, these words: Dashboard · My Day · Pipeline · Projects · Design and Engineering · Procurement · Permits · Inventory · Manpower and Equipment · Safety · Operations and Maintenance · Documents · Messages · Finance · Human Resource · Payroll · Reports · Administration. Migration and Cutover appears as a nineteenth item below Administration only until the cutover date. "Tasks" and "Construction" are removed as items; their screens live under My Day and Projects. Every module header repeats the sidebar wording in full.

**I2.2** The brand shows the Magnus name and logo, never "OPS PLATFORM".

## I3 · No abbreviations, no ampersands

**I3.1** Replace every one of these, found on screen during the test, with the full term, including in record prefixes where the prefix is shown as a label: OPS · EPC → engineering, procurement and construction · PTW → permit to work · BOM → bill of materials · BOS → balance of system · CRM → customer relationship management · O&M → operations and maintenance · NCR → non-conformance report · CAR → corrective action · SSS → Social Security System · HR → Human Resource · TIN → taxpayer identification number · PRC → Professional Regulation Commission · NPC → National Privacy Commission · MCP → Model Context Protocol · kWp → kilowatt-peak · kWh → kilowatt-hour · kV → kilovolt · sqm and m² → square metres · PHP → ₱ · HB1 to HB6 → hard block 1 to 6 · WH-LAG, WH-SOR, WH-DUM → Laguna Warehouse, Sorsogon Warehouse, Dumaguete Warehouse · EMP, RRQ, EQP, SN, TRF, ADJ, MOD, PO, SR, BM, FR, WO, PAY, DP, GR as visible labels → the full object name · Insp. · Part. · Cumul. % · Est. · Qty → quantity · pcs → pieces · "3d" → 3 working days · "0h" → 0 hours · "10y" → 10 years · EE Share and ER Share → employee share and employer share · e.g. → for example. Record numbers may keep a short prefix inside the number itself, such as PRJ-2026-0001, because the number is an identifier, not a label; the label beside it is the full word.

**I3.2** Every ampersand used for "and" is replaced: Design and Engineering, Pipeline, Safety, Operations and Maintenance Providers.

## I4 · Usability defects to fix

**I4.1** Dropdowns must not change selection when a person types while the control has focus; typing opens a filter.
**I4.2** The first click on any row, button or navigation item acts; no control requires a second click.
**I4.3** After any status change, the screen reflects the new state without reload.
**I4.4** Escape in a nested dialog closes only that dialog and keeps the form beneath it.
**I4.5** Placeholder text is never treated as a value.
**I4.6** Empty lists on first use show what to do, never a "Seed" button.
**I4.7** Toolbox attendees, blockers, approvers and custodians are picked from persons, never typed.

---
# PART D — TEST DATA AND THE STATE OF THIS DEPLOYMENT (Milestone 10)

**D1** Everything created on 3 September 2026 by the browser test is test data: ten customer accounts, eleven sites, ten contacts, eighteen persons, three warehouses, ten opportunities, ten proposals, five projects, five contracts, one design package, purchase orders, site reports, permits, inventory movements, safety records, tasks, documents, finance records, the payroll period, the statutory test table, and the two earlier trial accounts "test2" and "This is a test". So is every record the staff tests create with the prefix HT-.

**D2** Build a console-holder action under Migration and Cutover: **Clear test data**, which lists what it will remove by object type and count, requires the console holder to type the tenant name, removes those business records, keeps the tenant, roles, gates, hard blocks, system constants, configuration, console holders and the audit log, and writes an audit entry per removed record. It is refused once the cutover date is set. **Do not run it.** Karl runs it in the Hercules chat after the staff tests finish, if this deployment goes live. If a copy goes live instead, it is never run here.

**D3** The audit log is never cleared. Test-period entries remain and are distinguishable by date.

---
# PART T — ACCEPTANCE TESTS 259 TO 290, APPENDED TO SECTION 14

## Foundation

259. **Roles exist and bind.** Assign Person In Charge to Mario Bautista; gate 24 raises to the department head; after approval Mario's queries carry `money_visibility` none.
260. **Self-approval refused on every gate.** For each of the thirty gates, raise as one person and attempt to approve as the same person, on screen and over the protocol. Thirty refusals.
261. **Gate derived from amount.** Write-offs of ₱30,000, ₱75,000 and ₱150,000 land on gates 1, 2 and 3 with no choice offered. Purchase orders of ₱80,000 and ₱8,550,000 land on gates 4 and 5.
262. **Unassigned gate refuses.** Clear a gate's primary in the seed; submission refuses naming the gate.
263. **No alternate can be added** on gates 3, 7, 9, 18, 22, 27, 28, 29, 30 and 33, on screen or over the protocol.
264. **Six hard blocks, exact.** The Hard Blocks screen shows the six rows of F4.1 and nothing else; each is exercised by tests 5 to 10 of section 14.
265. **Hard block 6 on a fund request.** A fund request on a project with no contract refuses with the message of F4.5; a purchase order refuses; the project cannot leave setup.
266. **Hard block 1 is a file.** Mobilise above ₱2,000,000 with no certificate refuses; with a typed string refuses; with a file proceeds. Below the threshold proceeds without one.
267. **Sign-in grant.** Grant sign-in to a person; they sign in; "Signs In" shows; revoke; they cannot.
268. **Two console holders.** The second seat is filled; a third is refused.
269. **Actor on every audit entry.** Every entry shows the person; a search by person returns their entries.
270. **Unique numbers.** Two purchase orders on two projects never share a number.
271. **Manila time.** A record created at 13:10 Manila shows 13:10, not 05:10.
272. **Working days.** A permit filed on a Friday with a 90 working day default shows a date that skips weekends and the holiday table.
273. **Deep link.** Paste /projects/PRJ-2026-0001 in a new tab: the project opens.
274. **Search finds.** Search a purchase order number, a person, a message word: each opens.
275. **Notification inbox.** A mention creates exactly one notification for the mentioned person and it appears in their inbox.
276. **No literals.** Test 179 passes.

## Modules

277. **Party types are multi-valued.** One party is client and asset_owner; another is supplier with a currency of euro.
278. **Lease reference is per kilowatt-hour.** 480 kilowatt-peak shows 480 × 1,277 × 6.70 as the annual lease reference.
279. **Contingency is invisible to the client.** The client-facing document and export carry no contingency, cost or margin.
280. **Won seeds everything.** On won: project in setup with site and client, design package with nine deliverables, fourteen blocks with include flags, in one transaction.
281. **Percent is derived.** No screen has a typed percent; block and project figures follow activities and value weights.
282. **Toolbox is evidence.** A site report without a camera photograph or with typed attendees refuses.
283. **Pre-population.** Day two opens with day one's incomplete activities.
284. **Stock never negative.** Dispatch beyond on-hand refuses; a goods receipt increases stock at its location; a short receipt leaves in-transit and raises a discrepancy.
285. **Transfer gates by geography.** Laguna to Dumaguete at ₱5,000 is gate 25a; Laguna to Laguna site store at ₱120,000 is gate 25b; at ₱30,000 no gate.
286. **Permit to work is the Safety Officer's.** Any other person is refused on gate 28; no issue-immediately control exists.
287. **Quick Response form.** In an incognito window the site's form submits a near miss and a stop-work with no identity captured, and the stop-work pushes to the Safety Officer with mandatory acknowledgement.
288. **Unclassified is a state.** Registering lands unclassified; only gate 33 classifies; an unclassified document cannot govern.
289. **Progress claim works.** Create, gate 11, certify lower, both figures kept.
290. **Clear test data lists and refuses.** The action lists counts, requires the tenant name, and is refused once the cutover date is set. Not executed.

---
# PART H — MILESTONE ORDER AND REPORTING

| Milestone | Parts | Exit tests |
|---|---|---|
| 0 | Deliverable 0: the conformance checklist, every requirement in this message | — |
| 1 | Part F, with Part C section B (Google Drive) built inside it | Section 14 tests 1 to 30; 259 to 276 |
| 2 | M1, M2 | Section 14 pipeline and project tests; 277 to 280 |
| 3 | M3, M4 | Section 14 design and procurement tests; 281 |
| 4 | M5, M6, M7 | Section 14 site, permit and inventory tests; 282 to 285 |
| 5 | M8 to M14 | Section 14 remaining module tests; 286 to 289 |
| 6 | Part X, Operations and Maintenance | 190 to 214 |
| 7 | Part C section A, Communication | 237 to 251; 252 to 258 if not already passed in milestone 1 |
| 8 | Part P, protocol scopes and migration import | 215 to 236 |
| 9 | Part I, interface, labels and usability | 244; a screen-by-screen abbreviation sweep reported as a list |
| 10 | Part D, the clear-test-data action, built and not run | 290 |

After each milestone: post the checklist rows for it marked done, the test results with any failure named, and any place where this message and the original instruction could not both be satisfied. Then continue to the next milestone without waiting. Stop only at the end of milestone 10, or when a requirement cannot be built without a decision that would change data already stored, in which case ask one question and state what you will do if there is no answer.

---
