# Magnus Workspace Platform — Base44 build specification

## Part 07 · Operations and Maintenance — the service line

**Prerequisite: Parts 01 to 06 — this part needs `site`, `item`, `purchase_order`, `document`, `task`, `write_off` and `cash_forecast_line` to exist and hold real values.** It is the last stream of Phase 2.

**This is the only part that specifies a service line rather than a project.** A service relationship attaches to a **site**, never to a project, and outlives every project on it. It generates recurring revenue with no completion. It covers assets that may have no project record — **every field that would come from a project is optional, and every function works without it.**

**The governing rule: a service agreement is a promise with a clock on it. The platform's job is to make every clock visible before it runs out.** Every object answers one of four questions: what did we promise · what is due · what happened · what are we owed.

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

## 1. Amendments already applied in earlier parts

These are stated here so the builder can confirm them rather than discover them: `project.site_id` (Part 02) · generation monitoring lives on `serviced_asset`, not on the project · `party_type` includes `operations_and_maintenance_provider` · `contract.warranty_months` · `write_off.subject` includes `service_charge` · `cash_forecast_line` accepts `service_charge` · the permanent retention classes are eight, including service agreements and work-order evidence · the sidebar's eighteenth item, *Operations and Maintenance*, after Safety and before Documents.

**Gate decisions, recorded:** gate 9 covers any signed customer agreement including a service agreement · gate 11 covers a service charge · **gate 34 — warranty claim submission, Head of Finance, alternate Chief Operating Officer, window 3.** No hard block is added or extended: a charge is created only from an `active` agreement, and `active` is unreachable without the signed document.

---

## 2. Objects

**`service_agreement`** — service_agreement_id · agreement_reference · **site_id (required)** · account_id · project_id (optional) · **agreement_document_file_id (required to reach `active`)** · commencement_date · term_months · **expiry_date (derived at activation, same transaction, never typed)** · **renewal_notice_days (configuration, default 90, gate 31)** · predecessor_agreement_id · successor_agreement_id · scope_of_service (`preventive`/`corrective`/`preventive_and_corrective`/`monitoring_only`) · charge_basis (`fixed_periodic`/`per_kilowatt_peak`/`per_visit`/`hybrid`) · charge_amount · charge_period (`monthly`/`quarterly`/`annual`) · escalation_percentage · escalation_month · payment_terms_days · **state (stored: `draft`/`active`/`renewed`/`terminated`)** · **effective_status (derived on read, section 3)** · signed_under_gate_9_request_id.

**`service_level_term`** — service_level_term_id · service_agreement_id · **severity (`total_outage`/`partial_outage`/`degraded`/`cosmetic`)** · **response_hours** · **restoration_hours**. One row per agreement per severity; `active` is refused without at least one. **Severity governs the promise; it never governs ranking.**

**`serviced_asset`** — serviced_asset_id · asset_reference · site_id · service_agreement_id (optional) · project_id · design_package_id (both optional) · capacity_kilowatt_peak · commissioning_date · **warranty_expiry_date (derived as turnover date plus `contract.warranty_months` where a project exists — computed in whichever transaction comes second; typed only where Magnus did not build the asset)** · **generation_monitoring_source · generation_monitoring_access** · **expected_annual_yield_kilowatt_hours (derived at creation: capacity × the Specific Yield constant in force that day, storing the constant version; recomputed only when capacity changes)** · specific_yield_constant_version · **tariff_per_kilowatt_hour** · state (`monitored`/`under_service`/`service_lapsed`/`decommissioned`).

**`serviced_asset_equipment`** — serviced_asset_equipment_id · serviced_asset_id · item_id (optional) · equipment_class (`panel`/`inverter`/`battery`/`mounting`/`monitoring`/`other`) · manufacturer · model · serial_number · quantity · installed_date.

**`generation_reading`** — generation_reading_id · serviced_asset_id · period_start · period_end · granularity (`daily`/`monthly`) · generated_kilowatt_hours · ingestion_source (`manual`/`portal_export`/`integration`) · ingested_at · ingested_by. Populating it is a data task; it does not wait for an integration.

**`maintenance_plan`** — maintenance_plan_id · service_agreement_id · activity · **interval_months (configuration default per activity, gate 31)** · first_due_date · **next_due_date (stored; advanced by `interval_months` in the same transaction that closes a preventive work order raised from this plan)** · estimated_hours · required_capability · is_active. **The plan is the obligation; the task is the commitment; the work order is the visit. No scheduler instantiates any of them** — a person or agent reading `next_due_date` creates the task with `source = recurring`.

**`work_order`** — work_order_id · work_order_number · serviced_asset_id · service_agreement_id (optional) · originating_task_id · originating_plan_id · origin (`preventive`/`fault`/`client_request`/`warranty`/`monitoring_alert`) · **severity** · **raised_on_device · raised_received_by_server** · **responded_on_device · responded_received_by_server** · **restored_on_device · restored_received_by_server** · closed_at (server time) · reported_by · **assigned_to (must be a person who signs in)** · assigned_at · fault_description · root_cause · action_taken (**all three required to reach `closed` from `restored`**) · parts_used (stock issues from operations and maintenance spares, Part 03) · attendees (named persons on the visit) · **evidence_file_id (required to reach `closed`)** · **is_billable (default false)** · state · cancel_reason · client_message_key.

**`warranty_claim`** — warranty_claim_id · serviced_asset_id · work_order_id · **claimed_against (`supplier`/`subcontractor`/`magnus`)** · **purchase_order_id (required where `supplier`)** · contract_id · clause_family (`warranty_and_defects_liability` where `magnus` and a contract exists) · counterparty_party_id (required where `subcontractor`) · raised_at · claim_value · **evidence_file_id (required)** · state (stored: `raised`/`submitted`/`accepted`/`rejected`/`settled`; **derived `expired` on read** where the asset's warranty has passed and the stored state is `raised` or `submitted`) · rejection_reason · settled_value.

**`service_charge`** — service_charge_id · service_charge_number · service_agreement_id · work_order_id (for a billable visit) · period_start · period_end · **amount (generated — never typed)** · basis (copied from the agreement at creation) · state (`scheduled`/`approved`/`issued`/`paid`/`cancelled`) · approved_by (gate 11) · issued_on · invoice_document_file_id · paid_on · cancel_reason. **No screen accepts a typed amount. There is no `written_off` state** — an uncollectable charge goes to `write_off` under gates 1 to 3.

---

## 3. States and transitions

**`service_agreement.effective_status`, computed on read from stored dates — this is how the module holds its clocks without a timer:**

| Effective status | When |
|---|---|
| `draft` · `renewed` · `terminated` | The stored state |
| `active` | Stored `active` and today is before `expiry_date` − `renewal_notice_days` |
| `expiring` | Stored `active` and today is on or after `expiry_date` − `renewal_notice_days` and before `expiry_date` |
| `lapsed` | Stored `active`, today on or after `expiry_date`, `successor_agreement_id` empty |

| From | To | Who | Condition |
|---|---|---|---|
| `draft` | `active` | Director | **`agreement_document_file_id` present AND at least one `service_level_term`; gate 9 approved.** Same transaction: `expiry_date` computed; every `service_charge` for the term created as `scheduled` per `charge_basis` (below), escalation applied after `escalation_month`; a Task notification to the Head of Finance for the first charge |
| `active` | `active` | Director | Term extended in place — `expiry_date` moves; charges for the added periods created in the same transaction |
| `active` | `renewed` | Director | A successor reaches `active` with `predecessor_agreement_id` set; the predecessor's `successor_agreement_id` is set in the same transaction |
| `active` | `terminated` | Chief Operating Officer | **Reason required.** `scheduled` charges after termination cancelled in the same transaction |

**Charges created at activation by `charge_basis`:** `fixed_periodic` — one per `charge_period` for the term at `charge_amount` · `per_kilowatt_peak` — one per period, `charge_amount` × summed capacity of the assets under the agreement at activation · `hybrid` — the periodic component plus per-visit charges from billable work orders · `per_visit` — none at activation; every charge comes from a billable work order.

**`work_order`** — `raised` · `assigned` · `in_progress` · `restored` · `closed` · `cancelled`:

| From | To | Who | Condition |
|---|---|---|---|
| `raised` | `assigned` | Project Manager, Director, or the site's Person In Charge | Owner named; `assigned_at` stamped; **Task notification to the owner in the same transaction** |
| `assigned` | `in_progress` | Assigned owner | **Stamps `responded_on_device` — stops the response clock**; closes the assignment task |
| `in_progress` | `restored` | Assigned owner | **Stamps `restored_on_device` — stops the restoration clock** |
| `in_progress` | `closed` | Assigned owner | **`origin = preventive` only.** Advances the originating plan's `next_due_date` in the same transaction |
| `restored` | `closed` | Assigned owner | `root_cause`, `action_taken`, `evidence_file_id` present. **If `is_billable`, the service charge is created in the same transaction** with a Task notification to the Head of Finance |
| any | `cancelled` | Project Manager or Director | **Reason required** |

**Offline rule:** a work order is raised offline like any field record. **The assigned owner, and only the assigned owner, may capture `in_progress` and `restored` offline**, queued with a device idempotency key. Assign, close and cancel are online only.

**`warranty_claim`:** `raised` → `submitted` — Head of Finance, **gate 34** · `submitted` → `accepted` or `rejected` — Head of Finance, rejection reason required · `accepted` → `settled` — Head of Finance. Raising a claim notifies the Head of Finance (Task).

**`service_charge`:** `scheduled` → `approved` — Head of Finance, **gate 11** · `approved` → `issued` — Head of Finance, invoice document produced, **enters the cash forecast under `secured`** · `issued` → `paid` · `scheduled` or `approved` → `cancelled` — reason required.

---

## 4. Service level measurement — computed on read

| Measure | Derivation |
|---|---|
| Response | `responded_on_device` − `raised_on_device`, against `response_hours` of the term matching the work order's severity |
| Restoration | `restored_on_device` − `raised_on_device`, against `restoration_hours` |

**Both use device time, in elapsed hours, not working hours.** The service level is reported, never scored against a person — no screen, query or export aggregates breaches by named engineer.

## 5. Generation and underperformance

Underperformance = expected yield (pro-rated to the reading period) − actual generation, **valued at `tariff_per_kilowatt_hour`.** The operations domain of the executive view ranks by valued lost generation, never by a severity label.

## 6. Gates that apply

1, 2, 3 (write-off ladder for an uncollectable charge) · **9** (agreement signature) · **11** (charge approval) · 19 (non-conformance closure where a work order raises one on an asset with a project) · 22 (Specific Yield constant) · 31 (`renewal_notice_days`, plan intervals, warranty-expiry window) · 33 (agreements and evidence classification) · **34** (warranty claim submission).

## 7. Notifications and queries

**Same-transaction notifications:** work order assigned → Task to owner (cleared at `in_progress`) · agreement activated → Task to Head of Finance for the first charge (cleared at `approved`) · billable work order closed → Task to Head of Finance (cleared at `approved`) · warranty claim raised → Task to Head of Finance (cleared at `submitted`) · asset created with no active agreement → Information to the account executive.

**Queries, each returning its evaluation timestamp, rule count and sources:** agreements `expiring` with days to expiry · `lapsed` with days since · maintenance plans due within N days, and past due with no task · work orders in `assigned` or `in_progress` past `response_hours` · work orders in `in_progress` past `restoration_hours` · warranty expiring within the window with an open work order · claims with derived status `expired` · underperforming assets ranked by valued shortfall · charges issued and unpaid beyond payment terms · assets with no agreement · assets with no reading in N days. **Recipients and scopes are by account, not project.**

## 8. Permissions

| Role | Agreements | Work orders | Charges | Service level | Claims |
|---|---|---|---|---|---|
| Chief Operating Officer | all | all | view | all | view |
| Director | own accounts, full | own accounts | view | own accounts | view |
| Head of Finance | view | view | full | view | full |
| Account executive | own accounts | view | view | own accounts | none |
| Project Manager | view, own sites | own site orders | none | own sites | none |
| Person In Charge | none | own site only — raise, assign, update | none | none | none |

Money visibility and record scope apply unchanged.

## 9. Reports and accumulated data

**Reports:** service level attainment by agreement and period · response and restoration distribution by severity · work orders by origin · recurring service revenue by client and period · agreements expiring in the next two quarters · warranty claims raised, settled, expired, with value · lost generation by site, valued · parts consumption from spares · **cost to serve against charge, by agreement.**

**Accumulated, never maintained, always with sample size:** mean time to respond and restore by severity · failure rate by equipment model and age · warranty claim success rate by supplier · actual cost to serve against agreement value.

## 10. Screens

Agreements with service level terms and effective status · serviced assets and equipment · generation readings (manual entry and portal-export upload) · maintenance plans with next due dates · work orders with the owner's `in_progress` and `restored` capturable offline · warranty claims · service charges with Print/Send · service level attainment.

## 11. Migration

Existing agreements load with signed documents, commencement dates and terms; **an agreement whose document is not loaded stays `draft` and produces no charge.** In-force warranties load with expiry dates. Open work orders load with device timestamps where known, server timestamps otherwise, marked migrated.

## 12. Deliberately not built in this part

A timer moving an agreement to `expiring` or `lapsed` · a scheduler creating charges, tasks or work orders · predictive failure modelling, automatic dispatch, yield-degradation forecasting · a client-facing portal · a separate service-line ledger · a `written_off` charge state · technician utilisation as a score · severity as a ranking input · a spare-parts module of its own · service level in working hours · a typed service charge · a seventh hard block · any gate beyond 34 or widening of 9 and 11 beyond what is recorded.

---

## 13. Checks before Part 08 starts

1. Create an agreement on a site with no project — activates and functions fully. Attempt `draft` → `active` without the document — refused; without a service level term — refused.
2. Activate with a 12-month term, monthly fixed charge — twelve `scheduled` charges exist from the same mutation; no code path creates a charge for a `draft` agreement.
3. Set expiry 89 days out with a 90-day notice — effective status reads `expiring` on the next read; no stored transition, no audit entry. Let one pass expiry with no successor — `lapsed`; the query returns days since; nothing ran.
4. Raise a work order offline, synchronise later — both raised timestamps stored and differ. Raise 17:00 Friday, respond 10:00 Monday — 65 hours. Two severities on one agreement measure against their own rows. Close a preventive order — direct to `closed`, `restored_on_device` empty, the plan's `next_due_date` advances in the same mutation.
5. As a non-owner, attempt an offline `in_progress` — refused; as the owner, it queues with an idempotency key and posts once.
6. Supplier claim on an asset with no project — succeeds with `purchase_order_id`, fails without. Attempt `raised` → `submitted` without gate 34 — refused; the gate table holds thirty-one rows, none 13 to 17.
7. Close a billable order — the charge is created in the same mutation; no screen accepts a typed amount; issue it — it appears in the forecast under `secured`. Attempt to write off a charge outside gates 1 to 3 — refused.
8. Two sites, equal shortfall, different tariffs — the higher tariff ranks above. Change the Specific Yield constant — existing assets keep their version.
9. Every operations query returns its evaluation timestamp with no agent connected. No screen, query or export aggregates breaches by engineer.
10. Acceptance tests 190 to 214 from Part 12 pass, with output pasted.
