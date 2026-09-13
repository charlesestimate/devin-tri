# Magnus Workspace Platform — Base44 build specification

## Part 03 · Blocks and site reporting, Permits, Inventory and warehouses

**Prerequisite: Part 01 complete; Part 02 at least as far as `project_id`, `project_block_id` and the block spine.** Section A of this part carries the mechanism by which progress is recorded and by which people are paid; section C carries the highest-consequence one-off action in the whole build (the opening stock lock).

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

# A. BLOCKS AND SITE REPORTING

**The site reports on the blocks. There is no separate site reporting module and no separate Construction item in the sidebar.** A daily site report is the mechanism by which block progress is recorded, **and it is also the document on which people are paid.**

## A1. The block spine — fixed for every tenant, not configurable by anybody

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

What varies per project is which blocks are *included*, never what the blocks are. A console holder attempting to add, remove or rename a block code is refused.

**`project_block`** — project_block_id · project_id · block_code · included · **value_weight (locked when the bill of materials is costed)** · state (`not_started`/`blocked_material`/`in_progress`/`complete`/`signed_off`) · signed_off_by · signed_off_on · material_readiness (derived, not stored) · percent_complete (derived, not stored).

**Structural dependencies — a project manager may add to, never remove:** B0 gates B1 (**hard block 3**) · an approved Construction Safety and Health Program gates B0 (**hard block 2**) · B5 and B6 together gate B7 · on ground-mount only, B11 gates B1 · a block's design completeness releases that block's procurement · bill of materials line closure gates that block's construction. Additional dependencies: **`block_dependency`** — project_id · predecessor_block · successor_block · structural (true for the fixed ones; a structural row cannot be deleted).

**Mounting type determines B1's material and audit fields.** Rooftop: rails, L-feet and clamps; audit fields slope, roof type, structural integrity, area. Ground-mount: piles or foundations, posts, rails and clamps; audit fields topography, soil bearing, drainage, access.

## A2. The daily site report

**`site_report`** — site_report_id · project_id · **workday_number (sequential per project, seeded at migration)** · report_date · **person_in_charge** · weather (controlled list — content from the Safety Officer with the Persons In Charge; leave the list configurable) · **work_stopped_by_weather** · look_ahead · **working_hours_start · working_hours_end (site-level, recorded once — not attendance, not a clock)** · **created_on_device · received_by_server** · form_revision_id (the controlled form revision in force, Part 05) · state (`draft`/`submitted`/`verified`) · client_message_key (device idempotency key).

- **One site report per project per workday** — enforced in the write.
- **No per-person start time, end time, duration or location exists anywhere in this platform.**
- **`created_on_device` determines which workday a report belongs to, never `received_by_server`.**
- **Tomorrow's report is pre-populated from today's incomplete activities and today's `look_ahead`** — a form default computed when the form opens, not a scheduled job.
- Submitting a site report **closes the site report task** owned by the Person In Charge for that day (Part 04) in the same transaction, and **restores the project's thread if archived** (Part 05).
- The first site report activity on any block is refused without an approved Construction Safety and Health Program document — hard block 2.

**`toolbox_meeting`** — site_report_id · topic (proposed from today's permits to work and recent near misses; the Person In Charge may override) · **photograph_file_id (required, in-app capture only, never from the gallery)** · **attendees (list of named person references, required, never an integer)** · conducted_by. **One per site report. Required.** This one record is the safety record, the attendance record for payroll, and the verify layer of deployment.

**`site_report_activity`** — site_report_id · **project_block_id (required)** · description · percent_accomplished · manpower_allocated (from `toolbox_meeting.attendees`) · blocked · blocked_reason (`material`/`predecessor_block`/`external_or_utility`/`weather`/`manpower`/`client_access`) · **blocked_expected_clear_date (required wherever knowable)** · document_revision_id (the drawing revision in force on the report date — link to the revision, never the document).

Expected clear dates: material → the outstanding line's expected arrival date, automatically · predecessor block → its forecast completion · external or utility → entered · weather → not applicable · manpower → deployment · client access → entered, and accumulates as client delay.

**`site_photograph`** — site_photograph_id · site_report_id · project_block_id · file_id · created_on_device · caption. Ten to twenty-five per report, approximately 300 kilobytes each after compression. A permanent retention class.

**`non_conformance_report`** — non_conformance_report_id · project_id · project_block_id (required where against work) · source (`delivery`/`site`/`client`) · goods_receipt_id (required where `delivery`) · description · photograph file list (at least one where source is not `delivery`) · raised_by · raised_on · **owner_id** · required_action · target_close_date · state (`open`/`action_taken`/`closed`/`void`) · closed_by · closed_on · **closure_evidence_file_id (required in `closed`)**. Closure requires **gate 19**; `void` requires a reason and is reported. Creatable offline. A safety inspection raises a `corrective_action` (Part 04), never a non-conformance report; neither raises the other.

## A3. Completion — derived, never typed

```
block percent complete   = sum of percent_accomplished across that block's site report activities (capped at 100)
project percent complete = sum over included blocks of (block percent complete × value_weight)
```

**No person anywhere types a project percentage complete. No such field exists on any screen.** General Requirements carries no weight. **Weights re-base only on an accepted variation order, never on a cost correction, and the interface displays percentage complete both before and after.** Progress billing (Part 06) runs off this number.

**Block state** advances by derivation and by one human act: `not_started` → `in_progress` on the first activity; `blocked_material` when readiness is `not_ready` and an activity is blocked on material; `complete` at 100; `signed_off` by the Project Manager (B0's sign-off is what releases hard block 3).

**Cost per block:** material committed at purchase order issue · labour from deployment × labour rate · subcontractor · equipment.

## A4. Turnover

The **Turnover Document** is gate 21. One date, entered once, starts three clocks (Part 02 §B). A site stock location on the project closes at turnover with a closing count first (section C).

## A5. Screens

- **Site report capture — offline-first, pre-populated from yesterday, toolbox meeting required with photograph and named attendees, every activity bound to a block. This is the most important screen in the platform and the one most likely to be abandoned if it is slow.** Built for a phone on a rooftop; the upload queue is visible on it.
- Site report list — filed, late, missing, by project and by Person In Charge.
- Block detail — activities, photographs, state, dependencies, material readiness with the arrival date, percentage before and after the last variation.
- Non-conformance reports · Turnover Document.

---

# B. PERMITS

**A permit here is a government or utility authorisation for a project. A permit to work (Part 04) is a same-day authorisation for a hazardous activity. They share a word and nothing else. Separate tables, no shared code.**

**One route. No branches.** 50 kilowatt-peak, 100 kilowatt-peak and 1 megawatt are identical, with or without battery storage. **Do not build any logic that selects a permitting path by system size.**

**`permit_type`** — permit_type_id · permit_type_name · group (`local_government_unit`/`environmental_and_safety`/`utility_interconnection`) · issuing_body_class · gates_what (`mobilisation`/`start_of_construction`/`energisation`/`closeout`/`none`).

**`project_permit`** — project_permit_id · project_id · permit_type_id · **issuing_body (the specific office)** · responsible_person · **mode (`parallel`/`prerequisite`)** · date_filed · **expected_approval_date (required once `filed`)** · expected_date_source (`office_median`/`all_offices_median`/`default`) · expected_date_rebased_on · date_approved · expiry_date · fee_amount · state (`not_required`/`to_file`/`preparing`/`filed`/`awaiting_response`/`additional_requirement`/`approved`/`rejected`/`expired`) · last_followed_up · follow_up_count · **regulatory_version_in_force_at_filing** · reference_number.

**`permit_requirement`** — permit_type_id · issuing_body · requirement_description · first_observed_on_project · **times_observed** · last_observed. **Accumulated, never maintained — no editing screen exists.**

**`permit_duration_observation`** — permit_type_id · issuing_body · **days_filed_to_approved (working days)** · follow_up_count · project_id. Written in the same transaction as `approved`.

**`permit_consultant_engagement`** — project_permit_id · party_id · fee · reason · approved under **gate 20, no threshold**. Accumulates which offices keep needing outside help.

**`additional_requirement` is a distinct state**, and entering it does three things in the same transaction: raises a task to supply it, owned by whoever can produce it · writes (or increments) the requirement in `permit_requirement` for that office · re-bases `expected_approval_date` and records that it was re-based rather than missed.

**Expected approval date, in priority order at filing:** the accumulated median for this permit type at this issuing body · the accumulated median across all offices · **a provisional default of 90 working days (configuration)**. Always shown with its sample size.

**What permits gate:** prerequisite-mode permit → mobilisation, **hard block 4** · Construction Safety and Health Program → start of construction, **hard block 2** · Permission to Operate and interconnection approval → energisation · occupancy and closeout permits → project closeout, and final billing where the contract makes it a condition (**surfaced valued** as unbilled revenue).

**Regulatory versions:** each project records the regulatory requirements in force when it filed (`regulatory_version` — description · effective_from · region). A project filed under old rules is not judged against new ones.

**The platform never files anything.** It holds the deadline, records the reference once a person has filed, and stops.

**Screens:** permit register per project · requirement library per office, read-only · consultant engagements.

---

# C. INVENTORY AND WAREHOUSES

**`location`** — location_id · **location_type (`warehouse`/`site_stock`)** · name · **region** · **custodian_id (a named person)** · project_id (required where `site_stock`) · state (`open`/`closed`) · opening_balance_state (`unlocked`/`locked`) · opening_count_date · opening_lock_date · locked_by.

Seed: Laguna (Luzon, custodian Jay) · Sorsogon (Bicol, Bernie) · Dumaguete (Visayas, Paul). **A project running beyond twelve weeks holds a site stock location. Site stock is stock.** A site stock location closes at project turnover with a closing count first.

**`item`** — item_id · item_code · description · specification · **unit_of_measure** · **is_serialised** · category · **reorder_point — operations and maintenance spares only; refused on project material**.

**`stock_position`** — item_id · location_id · quantity_on_hand · **quantity_in_transit** · quantity_quarantined · valuation_basis (`specific_identification` for serialised, `weighted_average` otherwise) · average_cost.

**`stock_serial`** — item_id · serial_number · location_id · state (`on_hand`/`in_transit`/`quarantined`/`issued`/`disposed`) · cost.

**`stock_issue`** — issue_id · location_id · item_id · quantity · **project_id and project_block_id (both required)** · issued_by · issued_on · unit_cost_at_issue. **Issue of quarantined material is refused at every permission level — hard block 5**, logged.

**`stock_return`** — from a site: re-enters stock **at the cost it was issued at**; the originating block's cost reduces by the same amount.

## C1. The transmittal — form MRTC-PROC-F003, field for field

**`transmittal`** — transmittal_number · job_order_number · **from_location · to_location** · purpose · system_reference_number · date · time_of_release · lines (item, quantity, unit, description with brand, size, colour, capacity, serials where serialised) · **prepared_by · confirmed_by · received_by (each a signature image and date)** · **route_class (derived from the regions of the two locations: `within_region` 3 days expected, `inter_island` 10 days — configuration)** · expected_transit_days · state (`draft`/`awaiting_approval`/`issued`/`in_transit`/`received`/`received_short`/`cancelled`) · form_revision_id.

- All four directions are transmittals: warehouse → warehouse · warehouse → site · site → warehouse · site → site.
- **Gate 25a** for any inter-island transfer at any value; **gate 25b** for within-island above ₱100,000 (configuration). Value is the sum of line quantity × current average or specific cost.
- A transmittal may be cancelled only before `issued`, by the approver, with a reason.
- **Stock moves on receipt, not on despatch.** `issued` decreases origin `quantity_on_hand` and increases origin-to-destination `quantity_in_transit`; the receiving signature decreases in transit and increases destination. Total stock across all states is conserved during transit.
- **When received quantity differs from sent quantity, the platform raises, in the same transaction, a discrepancy notification to both custodians and the Procurement Head, sets `received_short`, and raises a `stock_adjustment` with source `short_receipt` under gate 26.** This is what makes the receiving signature return somewhere reconcilable.
- A transmittal in transit beyond its expected days is queryable; nothing chases it.

## C2. Counts and adjustments

**`physical_count`** — physical_count_id · location_id · count_type (`opening`/`quarterly`/`high_value_monthly`/`spot`/`closing`) · **counted_by (never the custodian alone on an opening count)** · counted_on · lines (item · counted_quantity · system_quantity at count) · state (`scheduled`/`counting`/`variances_raised`/`closed`/`locked`) · locked_by · locked_on.

**`stock_adjustment`** — stock_adjustment_id · location_id · item_id · counted_quantity · system_quantity · **variance (derived)** · **source (`physical_count`/`short_receipt`)** · count_id (required where `physical_count`) · **closing_reason (controlled list, including `measurement_estimate_on_non_unit_item`)** · state (`raised`/`investigated`/`approved`/`posted`) · investigated_by · approved_by · approved_on (**gate 26, every adjustment, no threshold**) · posted_on.

**Zero tolerance: every difference is recorded and explained before the count closes.** The platform reports how often each closing reason is used, by warehouse and by item, so *measurement estimate* applied to panels is visible as a pattern. Variance by warehouse and custodian is a Check for investigation, never a custodian score.

**Cadence** (configuration): all items quarterly, high-value items monthly.

## C3. The opening balance — the highest-consequence one-off action in the build

Sequence per warehouse: count (not the custodian alone) → spot check by Cristy → **lock under gate 27, no alternate** → only then is the warehouse live. **Both the count date and the lock date are recorded.** Before the lock, imported opening stock is reversible (Part 10); after the lock it is not. No issue, transmittal or adjustment may post at a location whose opening balance is `unlocked`.

## C4. Quarantine

**`quarantine`** — item_id · location_id · quantity or serials · reason (`damaged`/`wrong_item`/`short`/`dispute`/`supplier_non_conformance`) · source (goods receipt or count) · raised_on · state (`held`/`released`/`disposed`) · released_by · release_reason · owner. Release or disposal is recorded with a reason and an owner. Quarantined material by value, age and reason is queryable.

## C5. Screens

Stock by location including in transit and site stock · transmittal capture and receipt with signature (offline-capable for the receiving signature) · physical counts and adjustments with closing-reason distribution · quarantine · opening balance status per warehouse · item catalogue.

---

## D. Gates and hard blocks this part wires

| Action | Hard block first | Gate |
|---|---|---|
| First activity on B1 | 3 (B0 must be `signed_off`) | — |
| First activity on any block | 2 | — |
| Stock issue of quarantined material | 5 | — |
| Non-conformance closure | — | 19 |
| Turnover Document | — | 21 |
| Transmittal inter-island | — | 25a |
| Transmittal within-island above threshold | — | 25b |
| Stock adjustment | — | 26 |
| Opening balance lock | — | 27 |
| Permit consultant engagement | — | 20 |

All through the single engine; each raises a Task notification to the approver in the same transaction.

---

## E. Checks before Part 04 starts

1. Submit a site report with no toolbox record — refused. Confirm `attendees` holds person references, not an integer. Save an activity with no block — refused.
2. Search every screen for a field where a person types a project percentage. There must be none. Complete every construction block with permits open — the curve reads 100.
3. Attempt B1's first activity with B0 unsigned — refused under hard block 3, logged, message names the block, the condition, the release and who can supply it.
4. As a console holder, attempt to add, remove or rename a block code — refused.
5. Create Monday's report offline, synchronise Thursday — it is Monday's report; tomorrow's report opens pre-filled from incomplete activities.
6. Six permit cases (50, 100, 1,000 kilowatt-peak, with and without storage) produce the same permit set; no branch logic exists. Three building permits at one office averaging 60 days — the fourth forecasts 60 with sample size 3, not 90.
7. Issue a transmittal Laguna → Dumaguete: route inter-island, 10 days, gate 25a raised at ₱30,000; a ₱30,000 within-island transfer raises nothing. Receive 18 of 20 — discrepancy reaches both custodians and the Procurement Head; adjustment raised under gate 26.
8. Issue quarantined material at every permission level — refused and logged. Issue material with no block — refused.
9. Count one unit short of anything — an investigation is required before close; the closing reason appears in the distribution query.
10. Post an issue at an unlocked warehouse — refused. Lock under gate 27 — both dates recorded.
11. Acceptance tests 61 to 90 from Part 12 pass, with output pasted.
