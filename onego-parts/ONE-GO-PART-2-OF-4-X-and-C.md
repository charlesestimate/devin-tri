# CONFORMANCE BUILD INSTRUCTION — CONTINUATION 2 OF 4

This continues the same message. Part X is repeated in full because the earlier copy was cut off inside it.

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

**Membership is automatic and logged.** A person joins the account space when assigned to anything under the account: sales owner on the opportunity, Director on the project, Project Manager, design engineer on a deliverable, Person In Charge on a site report, procurement officer on a purchase order, assigned owner on a work order. A person leaves the space when no assignment under the account remains, except Directors, who remain. Console holders are not members by virtue of the seat. A person may also be invited by a current member, logged, and removed by the inviter or a Director, logged. Membership changes never delete history.

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

In Administration, under Integrations, a console holder connects one Google account by OAuth. **It is a dedicated Google account owned by Magnus for this purpose, not a person's own account. Karl connects it from the Integrations screen once the account exists; build the connection so that until it is connected, files stay `staged` in platform storage and the Integrations screen says so.** Request only the scope that limits access to files the application created. The connection stores the refresh token encrypted, the account's email, the root folder identifier, when it was connected and by whom. Disconnecting is logged and does not delete anything in Drive. The connection state, quota used and the count of files pending upload are shown on the same screen.

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

