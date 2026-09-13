# Magnus Workspace Platform — Base44 build specification

## Part 02 · The commercial chain: Pipeline, Project and Contract, Design and Engineering, Procurement

**Prerequisite: Part 01 built and its twelve checks passed.** This part is the critical path of the whole build and is internally serial: an opportunity becomes a contract, a contract produces a design, the design produces the bill of materials, procurement buys against it. **Publish `project_id`, `project_block_id` and the block spine (Part 03 section 1) on the first day of this part** — Parts 04 and 05 wait on nothing else.

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

Every table below also carries `created_at`, `created_by`, `updated_at`, `updated_by`. Every object below carries a message thread (Part 05) without configuration.

---

# A. PIPELINE — CUSTOMER RELATIONSHIP MANAGEMENT

**`account`** — account_id · account_name · industry · active. **Creating an account creates its account space (Part 05 §A2) in the same transaction.**

**`site`** — site_id · account_id · site_name · address · province · **region (derived from province, never typed)** · **local_government_unit** · distribution_utility · host_party · emergency card fields (nearest hospital, ambulance number, evacuation point, client site contact).

**Account, site and contact are three objects, not one.** A client with eleven branches is one account and eleven sites, each with its own assessment, local government unit, distribution utility and permit history.

**`contact`** — contact_id · full_name · account_id · position · electronic_mail_address · telephone_number. A contact may serve several accounts over time.

**`opportunity`** — opportunity_id · account_id · site_id · owner (person) · stage (`qualified`/`site_assessed`/`proposal_issued`/`negotiation`/`won`/`lost`) · estimated_capacity_kilowatt_peak · estimated_value · model (`sale`/`lease`/`power_purchase`) · expected_decision_date · loss_reason.

**Loss reasons (controlled list):** price · timeline · technical · relationship or incumbent · **client did not proceed at all** · financing. **Reason required above ₱10,000,000 (configuration).** *Client did not proceed* is recorded and reported separately from *lost to a competitor*.

**`site_assessment`** — site_assessment_id · site_id · roof_type · roof_condition · usable_area_square_metres · obstructions · structural_opinion · **structural_confidence (`high`/`medium`/`low`, required)** · tapping_point_voltage · tapping_point_phase · tapping_point_spare_capacity · consumption_profile · photographs (in-app capture only, `file` records) · assessed_by · assessed_on. Collected once, on site, and consumed by design without re-collection. Assessment confidence against later reinforcement variations is accumulated (Part 08).

**`proposal`** — proposal_id · opportunity_id · version · capacity_kilowatt_peak · markup_major_applied · markup_balance_of_system_applied · **contingency_percentage** · system_constant_versions_used (the identifiers of the constant rows in force when the version was built) · state (`draft`/`awaiting_approval`/`issued`/`superseded`/`won`/`lost`) · **frozen_at** · block lines (one per included block: block_code · quantity · cost · price).

- The proposal is **structured on the block spine** (Part 03 §1), which is what lets it become block value weights without re-costing.
- **`contingency_percentage` is internal and appears on no client-facing output** — not the proposal document, not an export, not a printed view.
- Sizing uses the Specific Yield and Area Per Kilowatt Peak constants in force on the day the version is built, and records which versions were used.
- **Gate 6** applies to every quotation release, no threshold. **Gate 7** applies when the applied markup is more than 5 percentage points below policy (system constants Markup Major Equipment 115 and Markup Balance Of System 130): a Director may approve down to 110 major and 125 balance of system; below that only the Chief Executive Officer, no alternate.
- **When an opportunity is won the winning proposal version becomes immutable** (`frozen_at`). Any later edit is refused.

**The `won` handover — one mutation, four stored consequences, no follow-up action:** the winning proposal freezes · a project is created in `setup` with `site_id`, `client` (the account's party) and `opportunity_id` carried across · the site assessment is linked to the design package · the proposal's block structure seeds the project blocks with their include flags. The project cannot become `active` until the signed contract is uploaded — hard block 6.

**A proposal is a commercial judgement. The platform structures it; a person prices it.** No pricing engine, no lead scoring, no probability weighting.

**Screens:** accounts, sites and contacts · opportunity list and record · site assessment capture (offline-capable, in-app camera) · proposal builder and version history.

---

# B. PROJECT AND CONTRACT

**Magnus signs on client paper. There is no Magnus standard contract.** Build a record of what this particular contract says; do not build a template engine, a clause library or any defaulting of terms.

**`party`** — party_id · **legal_name (the name on the contract)** · trading_name · **party_type (multi-valued: `client`/`asset_owner`/`offtaker`/`subcontractor`/`supplier`/`consultant`/`operations_and_maintenance_provider`/`other`)** · taxpayer_identification_number (required where invoiced or paid) · address · contacts · **is_related_party** · accreditation_state (`accredited`/`provisional`/`suspended`) · insurance_certificate_file_id · insurance_expiry · **insurance_exclusions (a field, not an attachment nobody reads)** · categories_supplied · currency.

**One record for every organisation.** A subcontractor and a supplier are parties, not separate objects.

**`party_bank_account`** — party_id · bank · account_name · account_number · effective_from · entered_by · **confirmed_by (a second named person, required before the row is usable)** · confirmed_at · previous_account_id. **Supplier bank details are change-controlled:** the change is logged with before and after, requires confirmation by a second named person, and **the next payment to that party after a bank change is flagged.** Nothing is blocked; it is made visible.

**`project`** — project_id · **project_number (structural, immutable, prefix for every document number under it)** · client (reference to `party`) · **site_id (reference to `site`, carried by the `won` handover)** · opportunity_id · proposal_id · site_address · **region (derived from the site's province)** · local_government_unit · capacity_kilowatt_peak · contract_value · project_manager · **director (approver on gates 6 and 8)** · permit_dependency · expected_permit_duration_days · contract_id (empty until uploaded — **this emptiness is what blocks**) · insurance_certificate_file_id · construction_safety_and_health_program_state · construction_safety_and_health_program_file_id · mobilised_on · status (`setup`/`active`/`suspended`/`turned_over`/`closed`/`cancelled`) · **planned_percentage_curve (a list of date and planned-percentage pairs, entered once from the contract programme)** · turnover_date · retention_billable_on · warranty_expiry_on · operations_obligation_expiry_on.

**The project name is derived on read, never stored:** `{capacity}_kW_{Customer}` — capacity from the proposal's system size in kilowatt-peak shown as stored, Customer from the client party's `legal_name`. Example: `480_kW_Calamba Agro Industrial Corporation`. Two parts only. It appears everywhere the project is shown — list, record header, search, pickers, the project channel, notifications, the board pack, every exception — with `project_number` as secondary text beneath it. When a variation changes capacity or a customer's legal name is corrected, the name follows the data the next time anyone opens the screen. `project_number` is the tiebreaker where two projects share a name.

**Project status transitions:**

| From | To | Condition |
|---|---|---|
| `setup` | `active` | Signed contract document present — **hard block 6**, evaluated in this mutation |
| `active` | `suspended` | Reason and the party responsible recorded |
| `suspended` | `active` | — |
| `active` | `turned_over` | Turnover Document, **gate 21** |
| `turned_over` | `closed` | **Both** retention released **and** defects liability expired |
| any | `cancelled` | By a Director, with open commitments listed and resolved first |

**Mobilisation** (`mobilised_on` set) is refused where contract value is at or above the hard block 1 threshold and no insurance certificate document is attached — a document, not a tick-box; and where any `prerequisite`-mode permit is not `approved` — **hard block 4**. Start of construction (the first site report activity on any block) is refused without an approved Construction Safety and Health Program document — **hard block 2**.

**There is no stored `phase` field and no phase badge.** Stage is computed on read from block states and displayed as a distribution, never a single word.

**`contract`** — contract_id · project_id · **signed_document_file_id (the signed copy)** · contract_value · currency · date_signed · client_signatory · payment_terms_days · retention_percentage · retention_reference_date_basis · retention_release_months · **warranty_months** · **counsel_review_state (`reviewed`/`proceeded_without_review`/`pending`)** · related_party · superseded_by.

**Retention terms are read out of the document by a person and entered. Nothing is defaulted or inferred.** Retention is time-based; Magnus must send the bill.

**`risk_term`** — contract_id · clause_family · **present (`present`/`absent`/`not_yet_read`)** · summary · exposure_flag · read_by · read_at. Eight clause families, all eight rows created on every contract at `not_yet_read`: liquidated damages and delay · payment terms and milestones · retention · insurance obligations placed on Magnus · warranty and defects liability · variation and change procedure · termination and suspension · limitation of liability and indemnity. `not_yet_read` is never displayed as `absent`.

**`project_party`** — project_id · party_id · role (`client`/`host`/`asset_owner`/`offtaker`/`financier`/`engineering_procurement_and_construction_contractor`/`operations_and_maintenance_provider`/`landlord`). Many to many.

**`variation_order`** — variation_order_id · contract_id · reference · description · value_change (may be negative) · capacity_change_kilowatt_peak · time_change_days · **blocks_affected (required)** · state (`draft`/`issued`/`accepted`/`rejected`) · raised_by · raised_on · approved_by · approved_on (**gate 8**, required in `issued`) · client_accepted_on · supporting_document_file_id. **Only `accepted` re-bases block value weights and moves the contract value.** An ageing `issued` record is visible as the most common way scope is given away.

**At contract signature (gate 9), in the same transaction:** the eight `risk_term` rows · the retention schedule dates computed from the three retention fields · the permit dependency flag as entered at contract review. The billing schedule, deliverable tasks and client obligations are entered by a person or generated by an agent — two separate lists: **`deliverable_task`** and **`client_obligation`** (project_id · description · due_on · owner or client contact · state).

**The turnover date is entered once and, in the same transaction, sets three stored dates:** `retention_billable_on` · `warranty_expiry_on` (turnover plus `warranty_months`) · `operations_obligation_expiry_on`. Nothing is separately keyed.

**Related-party contracts** are flagged and reported separately; documentation requirements are stricter; the platform computes no tax position.

**Portfolio views:** all active projects company-wide · my projects · by region · by stage distribution · by client · related party. Every view respects `record_scope` and `money_visibility`, **with one exception: the all-active portfolio total returns every active project regardless of the viewer's assignments**, with money visibility still applied. This is the only record view in the platform that crosses record scope.

**Screens:** project list and record with contract, risk terms, parties, variation orders, blocks, documents, permits, tasks, deliverable tasks and client obligations · party register with bank change control · portfolio views.

---

# C. DESIGN AND ENGINEERING

**`design_package`** — design_package_id · project_id · **site_assessment_id (the design opens with the assessment present)** · revision · design_capacity_kilowatt_peak · mounting_type (`rooftop_ballasted`/`rooftop_penetrating`/`ground_mount`/`carport`/`mixed`) · state (`in_progress`/`internal_complete`/`with_sealing_engineer`/`sealed`/`superseded`) · sealed_by · sealed_at · superseded_by.

**`design_deliverable`** — deliverable_id · design_package_id · **block_id (required on the three per-block deliverables: single line diagram, layout, bill of materials)** · deliverable_type · owner · state (`not_started`/`in_progress`/`waiting`/`complete`) · **waiting_on (`magnus`/`sealing_engineer`/`client`)** · **waiting_since** · document_revision_id.

**Nine deliverables per package:** Photovoltaic layout plan · Single Line Diagram · Electrical plans · Structural plans and mounting details · Structural Assessment Certification · Equipment datasheets and specifications · Earthing and lightning protection design · Cable schedule and electrical load schedule · Bill of materials.

**`waiting` always carries both `waiting_on` and `waiting_since`.** `waiting_since` resets on every transition; cumulative days by party accumulate per project. Thresholds (configuration): sealing engineer 3 days, client 7 days. A block's design completeness (its three per-block deliverables `complete`) releases that block's procurement.

**`bill_of_materials_line`** — line_id · design_package_id · **block_id (required)** · item_description · specification · quantity · unit_of_measure · is_serialised · unit_cost *(design writes these)* · **expected_arrival_date · purchase_status · purchase_order_reference · quantity_received** *(procurement writes these four)* · item_id (optional link to the catalogue).

**One object, two views. There is no second procurement list.** A design revision that changes a line already `ordered` **does not edit the line**: the platform flags the conflict and requires a person to decide — keep, return, or absorb — recorded on the line.

**`professional_seal`** — design_package_id · **revision_sealed** · engineer (party or name) · licence_number · licence_valid_to · professional_tax_receipt_number · professional_tax_receipt_year · sealed_at · turnaround_days (derived) · recorded_by. **Gate 18**, no alternate; the internal person records the external engineer's act. **A superseded sealed revision requires its own seal.** Licence and Professional Tax Receipt validity are checked at the seal date and **re-checked retrospectively: a licence expiry entered earlier than an existing seal date flags every design sealed in that window.**

**Structural Assessment Certification** has three outcomes: pass · **reinforcement required — raises a variation order under gate 8, never a task** · fail — escalates to the Director immediately.

**Block value weights** = block cost (materials **and** labour) ÷ total block cost, **excluding General Requirements**, locked when the bill of materials is costed. **Design capacity may differ from contract capacity: record both, reconcile neither.**

**Screens:** design package with the nine deliverables and their waiting states · bill of materials grouped by block with the ordered-line conflict marker · seal record with licence validity.

---

# D. PROCUREMENT

**Procurement has no list of its own.** It writes four fields onto bill of materials lines. `purchase_status`: `to_buy` · `requisitioned` · `ordered` · `in_transit` · `partially_received` · `received` · `cancelled`. **`expected_arrival_date` is required from the moment status becomes `ordered`.** The default view — the **buying checklist** — is grouped by block: what to buy, quantity, specification, status, expected arrival.

No requisition object, no request-for-quotation object, no bid scoring. Supplier quotations are attachments on the purchase order; comparison is a view; a person decides.

**`purchase_order`** — purchase_order_id · **purchase_order_number (unique per tenant — `PO-YYYYMM-NNN` counted per tenant per month, never per project)** · project_id · party_id · currency · exchange_rate_applied · exchange_rate_date · total_value · state (`draft`/`awaiting_approval`/`approved`/`issued`/`partially_received`/`received`/`cancelled`) · expected_arrival_date · approved_by · approved_on · **document_file_id (the purchase order document produced by the platform for sending to the supplier)**.

- **Raising a purchase order on a project with no contract is refused — hard block 6, evaluated before the gate.**
- **Gates 4 and 5** by value; **there is no approval point above the Procurement Head at any value.** The compensating control is a query: purchase orders committing 50% or more of the block's budget.
- **Committed cost begins at `issued`, not at payment.**
- A purchase order carries a **Send** action that produces the document (a `file` record under the purchase order's Drive folder, Part 05) and records who sent it, when, and to which contact. Nothing is emailed by the platform; the person downloads or shares the document.

**`purchase_order_line`** — purchase_order_id · **bill_of_materials_line_id (empty only for an off-design purchase)** · **off_design_reason (required where empty)** · off_design_block_id (required where empty) · quantity_ordered · unit_price · quantity_received.

**`goods_receipt`** — receipt_id · purchase_order_id · **received_at_location (a `location`, Part 03)** · received_by · **received_on_device · received_by_server** · photographs (in-app capture only) · condition (`accepted`/`damaged`/`wrong_item`/`short`) · lines (purchase_order_line_id · quantity_received · serials where serialised).

**A goods receipt moves stock, in the same transaction:** each received line increases `stock_position.quantity_on_hand` at the receiving location (or `quantity_quarantined` where condition is not `accepted`), increments `bill_of_materials_line.quantity_received` and `purchase_order_line.quantity_received`, advances `purchase_status` to `partially_received` or `received`, and advances the purchase order state. The first build received material into nothing and a custodian typed it again as an adjustment — the largest single gap in the daily work of the warehouses. **A receipt marked `damaged`, `wrong_item` or `short` quarantines the material in the same transaction; hard block 5 then prevents its issue.** The Non-Conformance Report is raised by a person or an agent (deviation D5).

**Material readiness per block, computed on read:** `ready` — every line received · `partially_ready` — some outstanding · `not_ready` — not startable, carrying the **latest `expected_arrival_date` among outstanding lines**. A partial delivery does not close the line; the balance keeps its own expected arrival date.

**Off-design purchases** are legitimate, recorded with a required reason and block, and never solved by adding a line to the design. The **five percent overrun query** against committed cost per block **states which of two things it is:** same items at a higher price, or additional items not in the bill of materials.

**Foreign currency:** actual rate and date recorded on every foreign-currency transaction; project cost carries the rate at purchase; **the difference against the quotation rate appears as a foreign exchange variance on the project, not inside the margin.**

**Supplier performance is accumulated, never scored by hand:** on-time delivery rate, damage and wrong-item rate, fill rate, price movement by item, actual lead time — all derived from receipts. No rating screen.

**`supplier_invoice`** — supplier_invoice_id · party_id · purchase_order_id · invoice_number · invoice_date · amount · currency · due_on · document_file_id · state (`received`/`matched`/`approved_for_payment`/`paid`/`disputed`) · matched_receipt_ids · paid_on · paid_by · **bank_account_id used (flagged where the party's bank account changed since the previous payment)**. This is the accounts payable record the first build lacked — what is actually owed, against what was committed. It is a sub-ledger record (Part 06); it posts no journal.

**Screens:** the buying checklist · purchase orders with Send · goods receipts (offline-capable, in-app camera) · supplier invoices · party register with bank change control.

---

## E. Gates and hard blocks this part wires

| Action | Hard block evaluated first | Gate |
|---|---|---|
| Quotation release | — | 6, and 7 where below the band |
| Contract signature | — | 9; counsel review recorded under 10 |
| Project `setup` → `active` | 6 | — |
| Mobilisation | 1, 4 | — |
| First construction activity | 2 | — |
| Variation order `issued` | — | 8 |
| Design release for permitting | — | 18 |
| Purchase order `awaiting_approval` → `approved` | 6 | 4 or 5 by value |
| Turnover Document | — | 21 |

Every one of these calls the single engine of Part 01 §7. The approver receives a Task notification in the same transaction.

---

## F. Checks before Part 03 starts

1. Win an opportunity: one mutation; project in `setup` with `site_id` and `client`; proposal frozen; blocks seeded. Attempt to edit the winning proposal — refused.
2. Attempt `setup` → `active` with every contract field set except the signed document — refused with a message naming hard block 6, the unmet condition, what releases it and who can supply it; the attempt is logged.
3. Raise a purchase order on a contractless project — refused, hard block 6, no approval request created.
4. Price at 112% major — Director may approve; at 108% — Chief Executive Officer only, no pass-down.
5. Enter a turnover date — three dates set, none separately entered.
6. Record a goods receipt — stock at the location increases in the same transaction; a `damaged` line lands in quarantine; issuing it is refused under hard block 5.
7. Two projects in the same month — purchase order numbers do not collide.
8. Export and print a proposal in every format — contingency appears in none.
9. The project list shows `480_kW_Calamba Agro Industrial Corporation` with the number beneath; rename the party — the name follows.
10. Acceptance tests 27 to 60 from Part 12 that this part makes runnable pass, with output pasted.
