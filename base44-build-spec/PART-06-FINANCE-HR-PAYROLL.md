# Magnus Workspace Platform — Base44 build specification

## Part 06 · Finance and cash · Human Resource · Payroll

**Prerequisite: Parts 01 to 04 delivering real values — block value weights, committed cost from issued purchase orders, `deployment.labour_rate`, toolbox attendance.** Build in this fixed order: **Finance → Payroll → Human Resource.** Payroll before Human Resource: Human Resource depends on payroll, not the reverse. A stub here gives a working screen over meaningless numbers.

**⚠ Open dependency:** whoever maintains Magnus's accounting platform must be available when section A's reconciliation is built. That person is not yet named. Do not design the read format around a guess.

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

# A. FINANCE AND CASH

**This is a sub-ledger. It is not a general ledger. Do not build accounting.** No chart of accounts, no journals, no statutory financial statements. It reads from Magnus's accounting system and never writes to it.

**Build the six things the accounting system cannot produce:** work in progress schedule · **committed cost** · cost to complete · estimate at completion · over- and under-billing · **certified against claimed**.

**`billing_milestone`** — billing_milestone_id · billing_milestone_number (prefixed by `project_number`) · project_id · sequence · description · basis (`percentage_of_completion`/`milestone_event`/`fixed_date`) · amount or percentage · state (`not_due`/`claimable`/`claimed`/`certified`/`invoiced`/`paid`). Entered by a person or an agent after contract signature (deviation D4).

**`progress_claim`** — claim_id · claim_number (prefixed by `project_number`) · **contract_id (the claim is against the contract; the screen passes the contract, never the project alone)** · project_id · **percent_complete_claimed (derived from Part 03 §A3, never typed)** · amount_claimed · **amount_certified (entered when the client certifies; may differ)** · date_claimed · date_certified · state (`draft`/`awaiting_approval`/`claimed`/`awaiting_certification`/`certified`/`invoiced`/`paid`/`disputed`) · approved_by · approved_on (**gate 11**) · invoice_document_file_id · issued_to_contact. **Claimed and certified are two numbers, always.** Uncertified claims are queryable at thirty days (configuration) carrying amount, client, age and **that client's own average certification time**.

**`fund_request`** — request_id · project_id · requested_by · amount · purpose · state (`requested`/`approved`/`released`/`liquidated`) · **liquidation_due (15 days from release — configuration)** · liquidation document file list · released_by · released_on. **Hard block 6 applies to release.** **An unliquidated advance blocks the requester's next request (refusal 3)**; Finance and Human Resource are notified in the same transaction as the refusal.

**`write_off`** — write_off_id · write_off_number (prefixed by `project_number` where a project exists) · subject (`receivable`/`retention`/`stock`/`advance`/`service_charge`) · subject_id · project_id · **amount (determines gate 1, 2 or 3)** · reason · **recovery_attempts (deliberately optional; a write-off with none is permitted and reported)** · requested_by · requested_on · state (`requested`/`approved`/`posted`/`rejected`) · approved_by · approved_on. **Nothing else in the platform writes value off.**

**`retention_receivable`** — contract_id · amount · billable_on (from the turnover date) · invoiced_on · invoice_document_file_id · approved under **gate 12** · state (`scheduled`/`due`/`invoiced`/`paid`/`overdue` — `due` and `overdue` derived on read from the stored date). The invoice is raised by a person or an agent reading the date (deviation D4).

**`cash_forecast_line`** — computed on read, twelve months forward: month · direction (`in`/`out`) · **confidence (`secured`/`gated`/`projected`)** · amount · source_object_type (progress claim, retention, fund request, pipeline opportunity, service charge, supplier invoice, payroll period) · source_object_id · **gate, owner and age for every gated line**. Three-month cash-gap detection is a query: a projected negative position within three months, valued, with the gated cash that would close it listed first.

**Percentage of completion under Philippine Financial Reporting Standards 15** comes from block value weights (General Requirements excluded): `earned = contract value × percentage of completion` · `billed = sum of invoiced milestones` · `position = billed − earned`. Over-billed is a liability; under-billed is unbilled revenue.

**Cost per block:** material committed at purchase order issue · labour from deployment × `labour_rate` · subcontractor (from supplier invoices attributed to the block) · equipment. **The five percent overrun flag is measured against committed cost and states whether the cause is price or additional items.**

**Markup actual against policy** is reported by project, client, Director and period. **Foreign exchange variance appears on the project, not inside the margin.**

**Accounts payable** is the `supplier_invoice` of Part 02 §D, with a payment record: **`supplier_payment`** — supplier_invoice_id · amount · paid_on · paid_by · bank_account_id · **bank_change_flag (true where the party's bank account changed since the previous payment)** · reference. Nothing is blocked; the flag is visible on the payment and in the register.

**`accounting_read`** — period · general ledger project cost by project (read at period close and on demand from the accounting system, format to be agreed with its maintainer) · **reconciliation: sub-ledger project cost against general ledger project cost, per period, with the variance shown rather than absorbed.**

**Screens:** billing milestones · progress claims with claimed and certified shown separately and a Print/Send producing the invoice document · fund requests · write-offs · retention receivables · cash forecast in three bands · supplier invoices and payments · sub-ledger reconciliation.

---

# B. PAYROLL

**This module contains the highest-consequence rules in the platform. None may be simplified.**

**Separation of duties, preserved exactly: Human Resource computes and approves the register; Finance releases payment under gate 23. Neither may do the other's step; a single person cannot both compute and release.**

**`payroll_period`** — period_id · period_start · period_end · population (`field`/`office`) · state (`open`/**`blocked_incomplete_reports`**/`computed`/`approved`/`released`/`distributed`/`closed`) · **site_report_completeness (derived — every site day in the period on every active project has a submitted site report)** · missing_site_days (derived list) · **acknowledgement_sheet_file_ids** · **acknowledgement_lines_returned (derived)** · computed_by · computed_at · approved_by · released_by · released_on · distributed_on · closed_on.

**`payroll_line`** — person_id · period_id · **days_worked (from the toolbox attendance — field crews; from the working calendar — office and management)** · basic_pay · overtime_hours (recorded only on days overtime was worked) · overtime · allowances · statutory_deductions (computed; each named with the bracket row applied) · other_deductions (each with the worker's written authorisation reference) · net_pay (computed, never entered) · **rate_table_version (per table type)** · project_id · project_block_id · payslip_file_id · acknowledgement_line_returned.

**`statutory_rate_table`** — table_type (`social_security_system`/`philhealth`/`pag_ibig`/`withholding_tax`) · **brackets (lower bound · upper bound · employee share · employer share or rate)** · **effective_from · effective_to** · entered_by (Human Resource) · approved_by (Finance) · approved_at · state (`pending`/`approved`/`superseded`) · legal_reference. **Tables and brackets, never a single percentage.** Configured through Administration and the protocol; never in code. The live tables must be the published statutory tables, entered with their legal reference; test data is never approved into a live tenant.

**Rules:**

- **A period computes at the rates in force during that period. Re-opening March in November reproduces March exactly.** `rate_table_version` on each line is what makes this provable.
- **An unapproved rate never reaches a run — it sits `pending`.**
- **THE BOUNDARY: you may update a rate to what the law now says. You may not override what the law then produces.** There is no permission level at which a computed statutory deduction on a payslip is editable.
- **THE SITE-REPORT BLOCK — "no report, no payroll".** The register cannot be generated while any site day in the period has no site report (refusal 1). **The block is on the run, never on a worker. No worker is ever dropped from a register.** The period sits `blocked_incomplete_reports`, listing the missing days; the Person In Charge and their manager receive a notification in the same transaction as the blocked attempt.
- **Attendance comes from the toolbox meeting record. No clock-in, clock-out, location or presence capture of any kind.** Field crews only; office staff take `days_worked` from the working calendar.
- **The headcount variance query** reports every site day where the number of people paid differs from the attendees recorded.
- **THE ACKNOWLEDGEMENT SHEET.** The platform prints a distribution sheet from the approved register (a controlled form revision); each worker signs beside their own amount; the sheet is photographed and uploaded the same day; **a period is not `distributed` until every sheet is returned, and does not `close` while any line is unacknowledged (refusal 2).**
- **Gate 23** on `approved` → `released`, Head of Finance primary.
- **Cutover requires three consecutive cycles matching the existing spreadsheet to the peso.** `parallel_run` — period · spreadsheet_total · platform_total · variance · explanation · matched. Cutover is refused with fewer than three matched cycles.
- **Payslips** are produced per line as a `file` record and reachable through employee self-service only by the person they belong to.
- **Visibility: a console holder, a Project Manager and a Person In Charge have no access to the register, a payslip or a rate table.** Human Resource and the Head of Finance only.
- **A named owner carries a recurring obligation to check for statutory changes** — a `recurring_definition`, not a scheduler.

**Screens:** payroll periods with completeness and missing days · register · statutory rate tables with dual-control state · acknowledgement sheets · parallel run record · payslip (self-service).

---

# C. HUMAN RESOURCE

**THE GOVERNING RULE: operational data informs the conversation. It never produces the rating.** Five things the platform never does: compute a rating, score or index from task counts, load bands, on-time percentages or grades · rank people · track presence · convert a score to money by formula · expose engagement responses per person.

**`employee`** — person_id (extends `person`) · employment_status (`probationary`/`regular`/`project_based`/`consultant`) · date_hired · **regularization_due** · level · manager · **buddy (named, never the manager — refused)** · career_path_id (empty until paths exist) · compensation_band_id (empty until bands exist).

**`salary_history`** — person_id · amount · effective_from · reason · set_by. Visible to Human Resource, the Head of Finance and — **only where explicitly configured per manager, off by default** — the manager. Never to a console holder.

**`requisition`** — requisition_id · **resource_request_id (a requisition originates from a declined resource request)** · role_title · department · headcount · justification · raised_by · raised_on · state (`draft`/`open`/`filled`/`withdrawn`).

**`candidate`** — candidate_id · requisition_id · full_name · contact · source · document file list · state (`applied`/`screened`/`interviewed`/`offered`/`hired`/`rejected`/`withdrawn`) · **retention_expiry (set on creation, never blank)**.

**`interview_record`** — interview_record_id · candidate_id · interviewer_id · scheduled_on · scores · written_comment · **submitted_at — no interviewer sees another's record until their own is submitted.**

**`offer`** — offer_id · candidate_id · requisition_id · position · salary · start_date · **probationary_end (seeds the regularization diary)** · state (`draft`/`awaiting_approval`/`issued`/`accepted`/`declined`/`lapsed`) · approved_by · approved_on (**gate 24**).

**`objective`** — person_id · quarter · **objective_text (written by the person)** · references_work (object references). Three to five per quarter; objectives reference work, never counts.

**`review`** — person_id · quarter · reviewer · went_well · did_not_go_well · **what_is_in_the_way** · next · rating (`exceeded`/`met`/`developing`/`not_meeting`) · **rating_reasons (required free text)**. **No `rating_score`, no numeric equivalent, no aggregate anywhere.** Review-held compliance is visible; ratings are never aggregated into a scoreboard, distribution or ranking. The evidence view opens the person's deliverables, tasks, reports and grades in the period for a human to read; it computes nothing.

**`recognition`** — from_person · to_person · text · visible to peers · **never convertible to money by formula.**

**`engagement_response`** — survey_period · question · response. **`person_id` is not stored.** Four questions, quarterly, anonymous, trended.

**`leave_request`** — person_id · from · to · type · reason (**visible to Human Resource only**) · state · approved_by. **`leave_balance`** — derived. Scheduling awareness (Part 04) shows approved dates only.

**`training_record`** and **`certification`** — person_id · description · evidence file · expiry (feeds `capability_tag`).

**`onboarding`** — person_id · pre-arrival checklist (equipment, access, personal protective equipment — completed before day one) · day-one items (account, roles under gate 24, capability tags, **a first task**) · buddy · 30/60/90 check-ins as `recurring_definition` rows on the manager · **regularization decision: a task diarised well before `regularization_due`; the decision is recorded, never defaulted.** Onboarding completion by manager is reported.

**`exit`** — person_id · resignation_date · notice · reason_category · **exit interview conducted by someone other than the manager (refused otherwise)** · knowledge handover task (with a deliverable) · regretted. Offboarding is the access event of Part 08 §G: it blocks on unreassigned work (refusal 4). Attrition by tenure, role, region, and **by manager as a Check for the department head, never a manager score.**

**Career structures — built and left empty:** `career_path` (dual track: engineering and management at equal level and band) and `compensation_band`. Until Magnus defines them, self-service shows *no path defined yet*.

**Employee self-service:** my objectives and capabilities · my next level and the gap (where paths exist) · training and certifications with expiry · leave request and balance · personal detail update (the person card fields) · **payslip access** · certificate of employment request. No Human Resource action is needed for any of these reads.

**Stay interviews** twice a year, diarised as recurring definitions, conducted before resignation.

**Statutory questions are for counsel** — probationary and regularization, Labor Code Article 105, thirteenth-month pay, statutory leave, Social Security System, PhilHealth and Pag-IBIG, Data Privacy Act retention, Department of Labor and Employment inspection records, the aggregation exposure, payroll deduction authorisation. Leave every affected value `[CONFIGURED]`.

**Screens:** employee record · requisitions, candidates, interviews, offers · objectives and quarterly reviews · recognition · engagement survey (anonymous entry, trended aggregate) · leave · onboarding and exit checklists · employee self-service.

---

## D. Gates and notifications this part wires

| Action | Hard block first | Gate | Notification in the same transaction |
|---|---|---|---|
| Progress claim issue | — | 11 | Head of Finance (Task) |
| Retention invoice | — | 12 | Head of Finance (Task) |
| Fund release | 6 | — | Requester (Response) |
| Write-off | — | 1, 2 or 3 by amount | Approver (Task) |
| Payroll release | — | 23 | Head of Finance (Task) |
| Payroll blocked on site reports | — | — | Person In Charge and manager (Check) |
| Statutory rate entered | — | dual control | Finance approver (Task) |
| Offer | — | 24 | Department head (Task) |
| Regularization due | — | — | Manager (Task, raised by the onboarding record's diary at creation) |
| Unliquidated advance refusal | — | — | Finance and Human Resource (Check) |

---

## E. Checks before Part 07 starts

1. Schema review: no chart of accounts, no journal table, no write path to the accounting system.
2. Release funds on a contractless project — refused and logged under hard block 6. A requester with an unliquidated advance raises another — refused; Finance and Human Resource notified.
3. Certify less than claimed — both retained; the client query shows the variance and the client's average certification time. Every forecast line is `secured`, `gated` or `projected`; every gated line names gate, owner and age. Construct a negative position in month two — the gap query returns it valued with the gated cash that would close it.
4. Leave one site day unreported — the register cannot be generated, the period reads `blocked_incomplete_reports` naming the day, and no worker is dropped. File the report — it computes.
5. Compute March, change a rate in June, re-open March — identical to the peso; each line names its rate version. Enter a rate and do not approve it — the old rate is used. Attempt to edit a computed statutory deduction at every permission level — refused. Verify a bracket-boundary salary against the published table to the peso.
6. Attempt to compute and release as one person — refused. Close a period with a sheet outstanding — refused. Attempt cutover after one matching cycle — refused.
7. As a console holder, attempt to view salary, a rating, a disciplinary record, the register, a payslip or a rate table — all refused.
8. Set the buddy to the manager — refused. Save a rating with no reasons — refused. Schema review: no `person_id` on `engagement_response`. Search for any computation producing a rating, score, index or ranking from operational data — none.
9. An employee views leave balance, certifications and payslip with no Human Resource action.
10. Acceptance tests 126 to 151 from Part 12 pass, with output pasted.
