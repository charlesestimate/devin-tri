Build a multi-tenant operations platform for Magnus Renewable Tech Corp, a solar engineering, procurement and construction company in the Philippines running approximately fifty megawatt-peak of commercial and industrial projects with about sixty people across offices, project sites and three regional warehouses in Laguna, Sorsogon and Dumaguete. You choose the technology stack, the framework and the hosting. Two requirements below name a layer rather than a product, and those two are not negotiable.

Read this entire instruction before writing any code. Where this instruction states a rule, implement the rule exactly and do not substitute a simpler equivalent. Where this instruction is silent, ask rather than decide. Do not add features that are not listed here.

## 1. THE GOVERNING PRINCIPLE OF THIS BUILD

This platform is a record, a permission boundary, and a Model Context Protocol server. It has no intelligence of its own and it performs no unattended action.

All automation, monitoring, ranking, chasing, escalating, summarising, reporting and analysis is performed by external artificial intelligence agents that connect through the Model Context Protocol server specified in section 9. The platform's job is to hold correct data, refuse the transactions it must refuse, and expose everything it knows to an authenticated agent.

Therefore, build no scheduler, no cron job, no background worker, no queue processor, no timer, no polling loop, no rules engine, no workflow engine, no notification engine, no ranking algorithm, no digest, and no outbound email, short message service or push notification of any kind. There is no exception to this paragraph. A complete list of what must not be built appears in section 12.

Four kinds of computation are permitted, because they are arithmetic evaluated at the moment a person or an agent asks for a value, not background activity:

1. Derived completion percentages, computed on read from stored activity records.
2. Hard block evaluation, computed at the instant a transaction is attempted.
3. Permission resolution, computed at the instant a request is served.
4. Audit hash chaining, computed at the instant a record is written.

If a feature requires something to happen while nobody is looking at the screen, that feature does not belong in this platform. It belongs to an agent.

## 2. THE TWO REQUIREMENTS THAT NAME A LAYER

You choose everything else. These two must be enforced by the database itself, because both are meaningless if enforced by application code that a future query can forget to include.

**Tenant isolation is enforced at the database row level.** Every table carries a `tenant_id` column from the very first migration. Isolation is implemented with database row-level security policies, not with a filter added in application code. A query written without an application-layer filter must return no rows belonging to another tenant.

**The audit log is append-only, enforced by database constraints.** The audit table rejects `UPDATE` and `DELETE` at the database level, for every role including the database owner and including you. Application code that merely declines to offer a delete button does not satisfy this.

Everything else — language, framework, hosting, user interface library, mobile approach — is your decision.

## 3. IDENTITY AND ACCESS

The platform stores no password, no credential, no reset flow and no recovery question. Identity is delegated to an external identity provider.

Build it as: **each tenant configures an identity provider, and the Magnus tenant's identity provider is Google Workspace.** Do not build it as: the platform uses Google. The second is simpler, passes every test today, and requires a full rebuild the day a second tenant arrives.

Access is verified against the identity provider on each session and is not cached indefinitely. When a person's identity provider account is disabled, their platform access ends at that moment, with no administrator action.

**A person holds one or more roles, never exactly one.** A director also carries deals as an account executive; a regional operations person is also a warehouse custodian. Permissions are the union of all roles current on the date of the action. Approval authority is the highest limit among the person's current roles, never the sum.

**Site crew members do not sign in.** They exist in the platform as people who are named, deployed and paid, and they never open the application. Model them as a person who is not a user, not as a user with no permissions. The distinction appears immediately in every user count and access review.

## 4. THE DATA MODEL

Every table carries `tenant_id`, `created_at`, `created_by`, `updated_at`, `updated_by`.

**No abbreviations anywhere.** Every column name, label, button, status value, error message and report heading uses the full term. An abbreviation may appear in parentheses after the full term on first use in the interface, and never alone. Write `person_in_charge`, not `pic`. Write `non_conformance_report`, not `ncr`. Write `bill_of_materials`, not `bom`. This applies to the database, the interface and your own commit messages.

### 4.1 `tenant`
`tenant_id`, `tenant_name`, `identity_provider`, `identity_provider_configuration`, `active`.

### 4.2 `person`
`person_id`, `full_name`, `aliases` (text list), `photograph` (image, optional), `population` (enumeration: `office`, `field`, `warehouse`, `consultant`), `employment_basis` (enumeration: `employee`, `subcontractor_personnel`, `consultant`), `employer` (reference to `party`), `signs_in` (boolean), `identity_subject` (text, required when `signs_in` is true and empty otherwise), `home_region` (enumeration: `Luzon`, `Bicol`, `Visayas`, `Mindanao`), `status` (enumeration: `pending`, `active`, `suspended`, `departed`, `archived`), `first_seen` (date), `last_seen` (date), `vouched_by` (reference to `person`, required for subcontractor personnel).

`aliases` is required in practice — the same person appears in existing company records under several spellings, and without aliases the platform creates duplicates when historical data is loaded.

No person record is ever deleted. Historical site reports, approvals and payroll registers reference it permanently.

### 4.3 `role`
`role_id`, `role_name` (full term, no abbreviation), `department`, `reports_to_role` (reference to `role`, empty only for Chief Executive Officer), `is_approver` (boolean), `active` (boolean). Roles are deactivated, never deleted.

### 4.4 `person_role`
`person_id`, `role_id`, `effective_from` (date), `effective_to` (date, empty means current), `assigned_by` (reference to `person`).

A role change closes the old row with an `effective_to` date and adds a new row. It never overwrites. Both may be current at once during a handover, and that is expected.

### 4.5 `permission`
`role_id`, `object_type`, `action` (enumeration: `view`, `create`, `edit`, `delete_attempt`, `approve`, `export`), `record_scope`, `money_visibility`.

`record_scope` (enumeration): `own` — records where this person is owner or assignee; `project` — all records on projects this person is assigned to; `department`; `region`; `all`.

`money_visibility` (enumeration): `none` — sees the record, sees no monetary value on it anywhere including exports and printed views; `cost` — sees what Magnus paid; `price` — sees what the client was charged; `margin` — sees both and the difference.

**These two are independent axes and must not be folded together.** A Person In Charge needs the full material list for their site and must not see its cost. Collapsing the axes forces a choice between hiding work and exposing margin.

### 4.6 `capability_tag`
`person_id`, `capability` (from a controlled list held in configuration), `level` (enumeration: `trained`, `competent`, `can_supervise`), `evidence` (reference to `document`, optional), `certification_expiry` (date), `maintained_by` (reference to `person`).

Capability determines what a person can be assigned. It grants no screen access.

### 4.7 `console_holder`
`person_id`, `holder_rank` (enumeration: `primary`, `second`), `granted_by`, `granted_on`.

**Exactly two holders. The platform refuses to save a third and refuses to remove the second.** One holder is a continuity failure; three or more and configuration drifts because nobody knows the current state.

### 4.8 `party`
One record for every organisation: clients, asset owners, offtakers, subcontractors, suppliers, consultants.

`party_id`, `party_name`, `party_type` (multi-valued: `client`, `asset_owner`, `offtaker`, `subcontractor`, `supplier`, `consultant`), `tax_identification_number`, `address`, `contact_name`, `contact_electronic_mail_address`, `contact_telephone_number`, `active`.

### 4.9 `project`
Contract terms are fields on the project, not a separate object.

`project_id`, `project_name`, `client` (reference to `party`), `site_address`, `capacity_kilowatt_peak` (decimal), `mounting_type` (enumeration: `rooftop`, `ground_mount`), `battery_energy_storage_system_included` (boolean), `contract_value` (decimal), `contract_signed_date` (date), `signed_contract_document` (reference to `document`), `insurance_certificate_document` (reference to `document`), `construction_safety_and_health_program_approval_document` (reference to `document`), `permit_required_before_mobilisation` (boolean, set at contract review and never discovered later), `expected_permit_duration_working_days` (integer), `prerequisite_permit_document` (reference to `document`), `retention_percentage` (decimal), `retention_reference_date` (date), `retention_release_period_months` (integer), `retention_becomes_billable_on` (date, stored), `warranty_period_months`, `operations_and_maintenance_period_months`, `turnover_date` (date), `planned_percentage_curve` (stored series of date and planned percentage pairs), `generation_monitoring_source` (text, optional), `generation_monitoring_access` (text, optional), `project_manager` (reference to `person`), `state` (enumeration: `pipeline`, `contracted`, `mobilised`, `in_construction`, `turned_over`, `closed`).

`turnover_date` is entered once and drives three stored dates: `retention_becomes_billable_on`, the warranty expiry and the operations and maintenance expiry. All three are computed and stored at the moment the turnover date is entered. Nothing raises an invoice — an agent reads these dates and acts.

### 4.10 `project_block`
**The block spine is fixed for every tenant and is not configurable by anybody, including a console holder, and not per project.** Standardisation is the product: if every company reshapes the spine, no two projects can be compared and there is no common language between Magnus and its subcontractors.

The fourteen block codes, seeded identically for every project:

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
| B8 | Transformer (conditional, carries an include flag) |
| B9 | Network And Monitoring |
| B10 | Miscellaneous |
| B11 | Civil (optional and parallel on rooftop; mandatory and gates B1 on ground-mount) |
| General Requirements | Permits, documentation, overhead |
| Battery Energy Storage System | Conditional, carries an include flag |

Fields: `project_block_id`, `project_id`, `block_code` (enumeration from the table above), `included` (boolean), `value_weight` (decimal, locked once set), `state` (enumeration: `not_started`, `blocked_material`, `in_progress`, `complete`, `signed_off`), `percent_complete` (derived on read, never stored, never typed).

Structural dependencies, which a project manager may add to but may never remove:
- B0 gates B1 — this is hard block 3.
- An approved Construction Safety and Health Program gates B0 — this is hard block 2.
- B5 and B6 together gate B7.
- On ground-mount only, B11 gates B1.

**General Requirements carries no value weight**, because you cannot install a permit, and including overhead means a construction curve can never reach one hundred percent while paperwork is open.

### 4.11 `site_report`
One per project per workday. This is the mechanism by which block progress is recorded and it is also the document on which people are paid.

`site_report_id`, `project_id`, `workday_number` (integer, sequential per project), `report_date` (date), `person_in_charge` (reference to `person`, accountable for this report), `weather` (enumeration, controlled list), `work_stopped_by_weather` (boolean), `look_ahead` (text, optional), `working_hours_start` (time), `working_hours_end` (time), `created_on_device` (timestamp), `received_by_server` (timestamp), `state` (enumeration: `draft`, `submitted`, `verified`).

`working_hours_start` and `working_hours_end` are site-level, recorded once by the Person In Charge. They are not attendance and not a clock. **No per-person start or end time exists anywhere in this platform.**

**`created_on_device` determines which workday a report belongs to, never `received_by_server`.** A report written on Monday and synchronised on Thursday is Monday's report.

Tomorrow's report is pre-populated from today's incomplete activities and today's `look_ahead` value, so the Person In Charge confirms or amends rather than re-types. This is a form default computed when the form opens. It is not a scheduled job.

### 4.12 `toolbox_meeting`
One per site report, required. **This is the attendance record.**

`site_report_id`, `topic` (text, required), `photograph` (image, required, captured in the application only and never selected from the device gallery), `attendees` (list of references to `person`, required), `conducted_by` (reference to `person`).

**`attendees` is a list of named people, not a headcount integer.** A count cannot be paid, cannot be reconciled against a photograph, and cannot answer who was exposed after an incident.

### 4.13 `site_report_activity`
`site_report_id`, `project_block_id` (required — every activity belongs to a block, with no exception), `description`, `percent_accomplished` (decimal, this activity's contribution to that block), `manpower_allocated` (integer, drawn from `toolbox_meeting.attendees`), `blocked` (boolean), `blocked_reason` (enumeration, required when blocked: `material`, `predecessor_block`, `external_or_utility`, `weather`, `manpower`, `client_access`), `blocked_expected_clear_date` (date, required where knowable).

### 4.14 `site_photograph`
`site_photograph_id`, `site_report_id`, `project_block_id` (where applicable), `image`, `created_on_device`, `caption`.

Ten to twenty-five per daily report, approximately three hundred kilobytes each after compression. **Photographs are captured in the application and are never written to the device photo gallery.** A site photograph in a personal gallery is permanently outside company control and is backed up to that individual's personal cloud storage.

### 4.15 `non_conformance_report`
`non_conformance_report_id`, `project_id`, `project_block_id` (required where the non-conformance is against work rather than a delivery), `source` (enumeration: `delivery`, `site`, `client`), `material_delivery_id` (required where `source` is `delivery`), `description`, `photograph_id` (list, at least one required where `source` is not `delivery`), `raised_by`, `raised_on`, `owner_id` (accountable for closure), `required_action`, `target_close_date`, `state` (enumeration: `open`, `action_taken`, `closed`, `void`), `closed_by`, `closed_on`, `closure_evidence_id` (reference to `document`, required in `closed`).

Closure requires approval gate 19 and closure evidence. `void` requires a reason.

### 4.16 `material_delivery`
The thin material record. It exists so that hard block 5 is real and so that block progress reflects material arriving on site.

`material_delivery_id`, `project_id`, `project_block_id`, `party_id` (the supplier), `description`, `quantity`, `unit_of_measure`, `expected_arrival_date` (date), `received_date` (date), `received_by` (reference to `person`), `photograph_id` (list), `state` (enumeration: `expected`, `received`, `quarantined`, `quarantine_released`, `disposed`, `issued_to_site`).

**Material in state `quarantined` cannot move to `issued_to_site`. This is hard block 5.**

### 4.17 `task`
`task_id`, `title`, `description`, `project_id` (optional), `project_block_id` (optional), `assigned_to` (reference to `person`), `raised_by`, `due_date`, `state` (enumeration: `open`, `in_progress`, `done`, `cancelled`), `completed_on`, `completed_by`.

Tasks are created by people and by agents. Nothing creates a task automatically.

### 4.18 `document` and `document_revision`
`document`: `document_id`, `document_name`, `project_id` (optional), `document_type`, `classification` (enumeration: `controlled`, `archive`, `unclassified`), `classified_by`, `classified_on`, `current_revision_id`.

`document_revision`: `document_revision_id`, `document_id`, `revision_label`, `file`, `uploaded_by`, `uploaded_on`, `superseded_on`.

**A document with classification `unclassified` is visible and discussable, carries a clear unclassified mark, and cannot be attached to a work instruction or cited as the governing revision.** Classification is performed by a person under gate 33 and has no automatic default.

### 4.19 `notification`
A single inbox of items addressed to a person. `notification_id`, `person_id`, `category` (enumeration: `task`, `response`, `check`, `information`), `title`, `body`, `link_object_type`, `link_object_id`, `created_at`, `acknowledged_at`.

**This panel is complete and is never ranked, never capped, never filtered and never summarised.** If a person has forty items addressed to them, they see forty. Rows are written by people acting in the platform and by agents through the Model Context Protocol. The platform itself generates no notification on a timer and sends nothing outward — no electronic mail, no short message service, no push. Delivery beyond this inbox is an agent's responsibility.

### 4.20 `system_constant`
Effective-dated. `system_constant_id`, `constant_name`, `value`, `unit`, `effective_from` (date), `changed_by`, `changed_on`, `previous_value`.

Seed these five rows with `effective_from` set to the go-live date:

| Constant name | Value | Unit |
|---|---|---|
| Specific Yield | 1,277 | kilowatt-hours per kilowatt-peak per year |
| Area Per Kilowatt Peak | 7 | square metres |
| Lease Reference Rate | 6.70 | Philippine peso per kilowatt-hour, value-added tax inclusive |
| Markup Major Equipment | 115 | percent |
| Markup Balance Of System | 130 | percent |

**A change never overwrites. It inserts a new row with a new effective date.** Any model, proposal or projection built before a change keeps the value it was built with; new work uses the new value. Every constant change requires approval gate 22, whose primary is the Chief Executive Officer with no alternate.

This exists because a yield constant moved from 1,400 to 1,277 and nothing recorded which models used which value, leaving roughly ₱3.6 million a year of projection difference to be restated by hand.

### 4.21 `configuration_value`
`configuration_key`, `value`, `data_type`, `changed_by`, `changed_on`, `previous_value`. Every operational threshold, every controlled list, every interface label.

**No Magnus-specific literal appears anywhere in the source code.** Not ₱2,000,000, not ₱100,000, not 1,277, not 7 square metres per kilowatt-peak, not any label. All of it is configuration. Threshold changes require approval gate 31.

### 4.22 `audit_entry`
`audit_entry_id`, `tenant_id`, `object_type`, `object_id`, `action`, `previous_value`, `new_value`, `changed_by`, `changed_at`, `module`, `arrival_channel` (enumeration: `screen`, `model_context_protocol`), `previous_entry_hash`, `entry_hash`.

Logged: every create, update, delete attempt, approval, rejection, status change, threshold change, system constant change, permission change, hard block attempt, sign-in, and data export.

**Page views are not logged.** That is surveillance of people and it is forbidden.

Each entry holds a cryptographic hash of the previous entry, so an alteration to history breaks the chain and becomes detectable. Provide a verification routine that walks the chain and reports whether it is intact, reachable from the administration screen and through the Model Context Protocol.

**Cryptographic erasure.** The Philippine Data Privacy Act gives a data subject the right to erasure; an append-only log cannot delete. Resolve this in the architecture, in the first release, because it cannot be retrofitted. Personal data inside a log entry is encrypted with a key specific to that data subject. On a valid erasure request the key is destroyed. The entry, its position and its hash all survive; the personal content becomes permanently unrecoverable; the entry then displays: `Content removed under data-subject request, [date], [authority].` The chain still verifies.

## 5. THE SIX HARD BLOCKS — CLOSED LIST

A hard block stops the transaction. There is no override, no proceed-anyway, no delegation, no permission level and no console screen that releases it. **Every attempt is logged.** Seed them as six rows with `block_id` 1 to 6. They are not approval gates and they do not take gate numbers.

| # | Block | Condition | Released only by |
|---|---|---|---|
| 1 | Mobilisation without insurance cover recorded | contract value above ₱2,000,000 (configurable) | The insurance certificate document attached. Not a tick-box |
| 2 | Construction without an approved Construction Safety and Health Program | all projects | Department of Labor and Employment approval document recorded |
| 3 | The first electrical block before Site Safety Infrastructure sign-off | all projects | Block B0 reaching state `signed_off` |
| 4 | Mobilisation where the contract or local government unit requires a permit first | projects where `permit_required_before_mobilisation` is true | Permit document attached |
| 5 | Issue of quarantined material to a project | all | Quarantine released, or material disposed |
| 6 | Fund release against a project without a signed contract | all projects | Signed contract document attached to the project |

**An administrator may change a configurable value inside a block. No administrator, at any permission level, through any interface, may switch a block off.** There must be no code path, no permission level, no console screen and no Model Context Protocol tool or parameter through which a hard block can be disabled. **Do not add a seventh.** Do not promote a warning to a block because it seemed more correct.

## 6. THE TWENTY-EIGHT APPROVAL GATES

**Gates are database rows, not code.** If a gate value appears in a source file, it is wrong. Seed twenty-nine rows, because gate 25 splits into 25a and 25b. **Gate numbers 13 to 17 are permanently reserved and are never loaded.**

`gate`: `gate_id` (text, so `25a` and `25b` are valid), `gate_name`, `limit_description`, `primary_role` (nullable), `primary_person` (nullable, used where the approver holds no platform account), `alternate_role` (nullable), `alternate_person` (nullable), `window_working_days` (integer, nullable), `applies_to_object_type`, `active`.

`approval_request`: `approval_request_id`, `gate_id`, `object_type`, `object_id`, `requested_by`, `requested_on`, `decided_by`, `decided_on`, `decision` (enumeration: `approved`, `rejected`), `reason` (text), `arrival_channel`, `state` (enumeration: `pending`, `approved`, `rejected`).

**`window_working_days` is stored and displayed. The platform never acts on it.** No timer fires, no authority passes down automatically, nothing is ever auto-approved and nothing ever escalates by itself. A named human being decides, or the request stays pending. An agent reading the pending list through the Model Context Protocol is what chases an overdue approval.

| # | Gate | Limit | Primary | Alternate | Window (recorded only) |
|---|---|---|---|---|---|
| 1 | Write-off | up to ₱50,000 | Head of Finance | Chief Operating Officer | 3 |
| 2 | Write-off | ₱50,001 to ₱100,000 | Chief Operating Officer | Chief Executive Officer | 3 |
| 3 | Write-off | above ₱100,000 | Chief Executive Officer | none | none |
| 4 | Purchase order | up to ₱100,000 | Procurement Officer | Procurement Head | 2 |
| 5 | Purchase order | above ₱100,000 | Procurement Head | Chief Operating Officer | 3 |
| 6 | Quotation release to client | all | Director on the project | Chief Executive Officer | 2 |
| 7 | Quotation below policy markup | more than 5 percentage points below policy | Chief Executive Officer | none | none |
| 8 | Variation order issued to client | all | Director on the project | Chief Executive Officer | 2 |
| 9 | Contract signature | all | Chief Executive Officer | none | none |
| 10 | Counsel contract review | every engineering, procurement and construction contract | Atty. Caneja (`primary_person`; counsel holds no platform account) | Chief Executive Officer accepting the risk on record | 3 |
| 11 | Progress claim issued | all | Head of Finance | Chief Operating Officer | 2 |
| 12 | Retention invoice issued | all | Head of Finance | Chief Operating Officer | 5 |
| 18 | Design release for permitting | all | Professional Electrical Engineer seal (`primary_person`; holds no platform account) | none — statutory act, cannot be delegated | none |
| 19 | Non-Conformance Report closure | all | Project Manager | Chief Operating Officer | 3 |
| 20 | Permit consultant engagement | all, no value threshold | Chief Operating Officer | Chief Executive Officer | 3 |
| 21 | Turnover Document issue to client | all | Project Manager | Chief Operating Officer | 2 |
| 22 | System constant change | all | Chief Executive Officer | none | none |
| 23 | Payroll release | all | Head of Finance | Chief Operating Officer | 1 |
| 24 | New hire, or assignment of a role to a person | all | Department head | Chief Operating Officer | 5 |
| 25a | Inter-island warehouse transfer | all, any value | Procurement Head | Chief Operating Officer | 2 |
| 25b | Within-island warehouse transfer | above ₱100,000 | Procurement Head | Chief Operating Officer | 2 |
| 26 | Stock adjustment after count variance | all, zero tolerance | Head of Finance | Chief Operating Officer | 3 |
| 27 | Opening stock balance lock | one-off, per warehouse | Cristy, after spot check (`primary_person`) | none | none |
| 28 | Permit to work | all | Safety Officer | none | none |
| 29 | Safety stop lifted | all | Safety Officer | none | none |
| 30 | Incident investigation closure | all | Safety Officer, countersigned by Chief Operating Officer | none | none |
| 31 | Threshold change | all | Domain owner | Chief Executive Officer | none |
| 32 | Change to what a role may do | all | Administration Console holder | Second console holder | none |
| 33 | Document controlled-versus-archive classification | all | Cristy (`primary_person`) | none | none |

**Gates 18, 28, 29 and 30 have no shortcut of any kind.** No alternate, no window, no delegation, and no configuration setting may give them one. Permits to work, the lifting of a safety stop, the closure of an incident investigation and the Professional Electrical Engineer seal are decided by a qualified person, every single time.

**A person may not approve their own request**, with two carve-outs: gates 10 and 18, where the internal person is recording an external professional's decision rather than making one.

Rows for gates whose module is not built in this release are still seeded. They sit inactive against `applies_to_object_type` values that do not yet exist, and they are wired when their module lands. **Do not renumber, do not omit, do not invent a gate.**

Statutory rate changes operate identically but are not one of the twenty-eight: Human Resource enters, Finance approves, every rate carries an effective date, and an unapproved rate never reaches a payroll run. Build the dual-control mechanism now even though payroll is not in this release.

## 7. DERIVED COMPLETION

```
block percent complete   = sum of percent_accomplished across that block's site report activities
project percent complete = sum over included blocks of (block percent complete × value_weight)
```

**No person anywhere in this platform types a project percentage complete.** There is no such field, on any screen, in any form. Search for one before you ship; there must be none.

`value_weight` locks once set. It re-bases only on an approved variation order under gate 8, never on a cost correction. **When a variation re-bases the weights, the interface must display percentage complete both before and after.** A project moving from 62 percent to 58 percent overnight with no site activity is correct, and will be read as a defect unless the platform says why.

This number is the basis on which Magnus invoices its clients. An activity percentage entered carelessly on a rooftop becomes money claimed from a customer.

## 8. FIELD AND OFFLINE BEHAVIOUR

All field users work on their own personally owned phones. The company does not own them and will never wipe them. The application therefore holds a working cache and an offline queue only, and no permanent local copy of company data. On revocation the cache becomes unreadable and the account is dead; server-side revocation is the entire security control.

- **Field users create records offline** — site reports, photographs, toolbox meetings, activities, non-conformance reports. Creation never conflicts.
- **Field users do not edit shared records offline.** This removes most synchronisation complexity at almost no cost in capability.
- **No approvals offline, ever.** An approval is a decision with consequence and must be made against current data. Capture offline; decide online.
- Photographs are compressed on the device, queued, and uploaded resumably. The original is retained until synchronisation is confirmed.
- Both `created_on_device` and `received_by_server` are stored on every field-captured record.

Test this path on a genuinely poor connection before building any interface on top of it. A Person In Charge on a rooftop in Sorsogon uploading a delivery photograph: if that fails silently even once, that person returns to Facebook Messenger permanently and does not come back. A director testing from an office will never discover it.

## 9. THE MODEL CONTEXT PROTOCOL SERVER — THE SECOND PRODUCT SURFACE

This is not an add-on. It is how the platform is operated, monitored and configured. Build it to the same standard as the user interface, and expose through it everything a person can see or do on a screen.

**The server has no permissions of its own. It has the permissions of the authenticated person, and no more.**

### 9.1 Authentication and scoping
- The connecting person authenticates as themselves against the tenant's identity provider. **There is no service account, no platform identity, and no "changed by the assistant".** Every action carries a human being's name.
- Every call is tenant-scoped by the same database row-level policies that scope the interface.
- Scope at the query layer, never by filtering an answer after computation. An answer filtered after the fact has already read the data.
- **Every call is written to the audit log** — who, when, what was read or written, and `arrival_channel` of `model_context_protocol`.

### 9.2 Read tools
Expose list, get and search for every object in section 4: projects, blocks, site reports, toolbox meetings, activities, photographs, non-conformance reports, material deliveries, tasks, documents, people, roles, permissions, parties, notifications, approval requests, gates, hard blocks, system constants, configuration values and the audit log.

Also expose these computed reads, evaluated on request:
- Percentage complete per block and per project, with the planned percentage for the same date.
- Projects with no submitted site report in the last two working days.
- Site report compliance by Person In Charge — filed, late, missing.
- Approval requests pending, with age in working days and the recorded window.
- Blocked activities with reason and expected clear date.
- Non-conformance reports open, with age and same-day closure rate.
- Material deliveries expected, overdue and quarantined.
- Projects where retention, warranty or the operations and maintenance obligation becomes due within a caller-supplied number of days.
- Toolbox attendee count against paid headcount, where payroll data exists.
- Capabilities held by fewer than two people.
- Certifications expiring within a caller-supplied number of days.
- The audit chain verification result.

**These are queries, not alerts.** The platform computes them when asked and does nothing with them. An agent asks, decides what matters, and writes a notification or a task back through the write tools.

### 9.3 Write tools
Create and update for every object, and submit an approval decision on any pending request, always as the authenticated person and always subject to that person's permissions.

### 9.4 Configuration tools
Everything the administration screens configure is configurable here: thresholds, gate limits, gate primaries, gate alternates, gate windows, roles, permissions, money visibility, labels and terminology, controlled lists, and statutory rates and tables.

**Seven rules govern every configuration write, and all seven are mandatory:**

1. **Authenticated as a person.** The change carries a human's name.
2. **Same authority as the screen.** If that person cannot change a threshold on the administration screen, they cannot change it here.
3. **Same gates apply.** Gate 22 for system constants, gate 31 for thresholds, gate 32 for permissions. No gate is relaxed because the change arrived over this interface.
4. **Confirmation before applying.** The proposed change is stated back in full and confirmed by the person before anything is written. `Raise the receivable threshold a bit` must become `Change overdue receivable escalation from 30 days to 45 days. Confirm?` before a single byte is written. **A configuration change inferred from an ambiguous instruction and applied silently is the worst failure this interface can produce, because it looks like it worked.**
5. **Reason recorded** where the field requires one.
6. **Logged identically to a screen change**, plus the arrival channel.
7. **Effective dating preserved.** A constant or rate changed here carries its effective date exactly as it would on the screen.

### 9.5 Never writable by any client
Not through the Model Context Protocol, not through the screens, not through the database, not at any permission level:

1. The audit log.
2. Statutory calculation results. **You may update a rate to what the law now says. You may not override what the law then produces.** Changing a Social Security System contribution table is maintenance; editing the resulting figure on an individual payslip is falsifying a statutory computation.
3. Tenant isolation.
4. **The existence of any of the six hard blocks.** Values inside them are configurable; their existence is not.

**Enumerate every tool and every parameter the server exposes and prove that none of them, in any combination, can disable a hard block.** This is the single most important test in the build.

## 10. SCREENS TO BUILD

Keep the interface thin. Every screen is a view of section 4 and nothing more.

1. **Sign-in** — identity provider redirect only.
2. **Notification inbox** — complete, unranked, uncapped, grouped only by the four categories.
3. **Project list and project record** — contract terms, blocks with derived percentages, documents, deliveries, non-conformance reports, tasks.
4. **Block detail** — activities, photographs, state, dependencies, material readiness.
5. **Site report capture** — offline-first, pre-populated from yesterday, toolbox meeting required with photograph and named attendees, activities each bound to a block. This is the most important screen in the platform and the one most likely to be abandoned if it is slow.
6. **Site report list** — filed, late, missing, by project and by Person In Charge.
7. **Non-conformance report list and record.**
8. **Material delivery list and record**, including the quarantine state.
9. **Task list** — mine, and by project.
10. **Document library** — classification, revisions, current revision marked, unclassified documents clearly marked as unusable for construction.
11. **People and roles** — person record, roles with effective dates, capability tags. **No salary, no performance rating, no disciplinary record and no medical data appears on any screen in this platform**, and a console holder with full permissions has no access to them by virtue of that fact.
12. **Approvals** — my pending approvals, and the full request history with decisions and reasons.
13. **Administration** — tenant, identity provider, system constants with effective dates, configuration values, gate rows, hard block rows (values editable, existence not), console holders, audit chain verification, and a read-only view of the audit log.

## 11. ACCEPTANCE TESTS — THE BUILD IS NOT DONE UNTIL ALL OF THESE PASS

None of these is visible in a demonstration and none will be revealed by clicking through the screens.

1. **The audit log is genuinely immutable.** Alter an entry using direct database access. The verification routine must report a broken chain.
2. **Tenant isolation is enforced at row level.** Write a query with no application-layer filter. It must return nothing belonging to another tenant.
3. **Offline capture preserves creation time and survives reconnection.** Create records offline, reconnect after a delay, confirm both timestamps are correct and that no record is lost or duplicated.
4. **Percentage of completion is correct.** Verify against manually computed cases. The platform will produce a number; the test is whether it is the right number.
5. **Cryptographic erasure works over the immutable log.** Erase a data subject, confirm the content is unrecoverable and the hash chain still verifies.
6. **Effective dating on system constants.** Build a record, change a constant, reopen the record — it must show the value it was built with. Then build a new record and confirm it uses the new value.
7. **A hard block cannot be disabled.** Attempt to switch off each of the six from the administration screen, from the database, by permission escalation, and through the Model Context Protocol. **All four routes must fail, for all six blocks, and every attempt must be logged.**
8. **No typed percentage.** Search the entire platform for any field where a person enters a project percentage complete. There must be none.
9. **Every activity has a block.** Save a site report activity with no block. Must fail.
10. **Toolbox meeting required, attendees named.** Submit a site report with no toolbox record — must fail. Confirm `attendees` holds person references, not an integer.
11. **Hard block 3.** Attempt to start B1 with B0 unsigned. Must fail and be logged.
12. **Hard block 5.** Attempt to issue quarantined material to a site. Must fail and be logged.
13. **The spine is not configurable.** As a console holder, attempt to add, remove or rename a block code. All must fail.
14. **Photographs stay in the platform.** Capture a site photograph. It must not appear in the device photo gallery.
15. **Offline day attribution.** Create a report offline on Monday, synchronise on Thursday. It is Monday's report.
16. **Multi-role union.** Give one person two roles with different permissions. They receive the union, and their approval limit is the higher of the two, never the sum.
17. **Money visibility is independent.** A person with `record_scope` of `project` and `money_visibility` of `none` sees the full material list and no cost figure anywhere on it, including in exports and printed views.
18. **Identity revocation.** Disable the identity provider account. The session ends and cannot be resumed, with no administrator action.
19. **Console holder count.** Attempt to save a third holder, and to remove the second. Both must fail.
20. **Crew are not users.** A person with `signs_in` false has no `identity_subject`, appears in reports and deployment, and cannot be granted a session.
21. **Model Context Protocol respects money visibility.** Ask about margin as a person with `money_visibility` of `none`. No answer, and the underlying query never reads the value.
22. **Model Context Protocol respects record scope.** Ask about a project outside the person's scope. No answer, and no acknowledgement that the project exists.
23. **Configuration through the Model Context Protocol carries a human name.** Change a threshold. The log names the person, never the platform, and records the arrival channel.
24. **Same authority through both surfaces.** As a person without threshold authority, attempt the change through the Model Context Protocol. It must fail identically to the screen.
25. **Confirmation before applying.** Issue an ambiguous configuration instruction. The change is stated back in full and requires explicit confirmation before any write.
26. **Gates apply through the Model Context Protocol.** Change a system constant. Gate 22 fires, with no alternate and no pass-down.
27. **Every Model Context Protocol call is audited.** Confirm both reads and writes appear in the audit log.
28. **Nothing runs unattended.** Deploy the platform, leave it with no user and no agent connected for twenty-four hours. **Nothing must have changed:** no notification created, no state advanced, no approval passed down, no invoice raised, no message sent. Inspect the audit log to confirm it is empty for that period.

Test 28 is the test of this entire specification. If anything at all happened, you built automation that must be removed.

## 12. DELIBERATELY NOT BUILT — DO NOT ADD ANY OF THESE

| Not built | Why |
|---|---|
| Any scheduler, cron job, background worker, queue processor, timer or polling loop | Section 1. Agents do this |
| An exception engine, a rules engine or a workflow engine | Agents do this |
| Ranked exception lists, severity scoring, consequence ordering | Judgment, not a rule |
| Automatic escalation of anything to anyone | A person or an agent escalates |
| Automatic pass-down of approval authority when a window expires | Windows are recorded, never acted on |
| Auto-approval of anything, at any threshold, ever | Nothing is ever auto-approved |
| Automatic raising of retention invoices, progress claims or billing schedules | The dates are stored; an agent reads them |
| Automatic generation of deliverables, tasks or obligations at contract signature | An agent generates; the platform stores |
| Outbound electronic mail, short message service or push notification | Delivery is an agent's job |
| Notification digests, summaries or roll-ups | Section 4.19 |
| An in-platform chat assistant or any large language model call from inside the platform | The intelligence connects from outside, over the Model Context Protocol |
| Nightly narrative passes, emergent findings pipelines, token budgets, steering prompts | Deleted entirely |
| Predictive progress curves, delay forecasting, conditional deliverable adjustment, bill of materials generation | These require accumulated history the company does not yet have |
| Autonomous agent action taken without a human decision | An agent acting on unproven data does not fail visibly — it fails confidently |
| Administrative screens for maintaining reference data — prices, cycle times, supplier performance, permit durations | These are accumulated from what happened, or computed on request. A maintenance screen nobody updates holds numbers that are wrong within a quarter |
| A general ledger, chart of accounts or journal posting | An external accounting system does this. This platform is a project sub-ledger |
| Any presence, location, activity, keystroke or login-time tracking, for anybody, at any level | Legal constraint under Philippine labour law and a commitment made to staff at rollout. **Workload is visible; presence is never tracked.** No console setting may switch this on |
| Any field where a person types a project percentage complete | Section 7 |
| A headcount integer in place of named toolbox attendees | Section 4.12 |
| Photograph upload from the device gallery | A gallery photograph has no reliable date, place or provenance |
| A configurable block spine | Section 4.10. Standardisation is the product |
| Removable structural block dependencies | A project manager may add one; nobody may remove one |
| A seventh hard block | The list of six is closed |
| Password storage, reset or recovery of any kind | Identity is delegated |
| Sign-in for site crew members | They are people, not users |
| A single-role-per-person model | It fails on the first real person at this company |
| One combined permission level mixing record scope and money visibility | They are independent axes |
| Offline approval | Capture offline; decide online |
| Deletion of any person, role or audit record | Historical records reference them permanently |
| Page-view logging | Surveillance of people |
| A service account or platform identity for any agent | Every action carries a human's name |
| Any tool, verb or parameter capable of disabling a hard block | Test 7 |
| Subscription billing, client portals or marketplace features | Not in this release |

## 13. HOW TO PROCEED

Build in this order and do not compress the first step:

1. **Foundation.** Multi-tenant schema with `tenant_id` on every table from the first migration, database row-level security, the append-only hash-chained audit log with cryptographic erasure, identity and the permission model, the twenty-nine gate rows and six hard block rows as seed data, system constants and configuration values. Do not shorten this. A `tenant_id` retrofitted onto populated tables is a migration, not an edit, and an append-only log cannot be retrofitted onto a table that has been edited for four months.
2. **Prove it.** Run acceptance tests 1, 2, 5, 7 and 19 before building a single screen.
3. **The project spine.** Parties, projects, blocks, material deliveries, site reports, toolbox meetings, activities, photographs, non-conformance reports.
4. **Work management.** Tasks, documents, notifications.
5. **The Model Context Protocol server**, covering everything built above.
6. **Run all twenty-eight acceptance tests, including test 28.**

Create a second, entirely invented test tenant early and keep it populated. **If the platform cannot run a second, invented company, it is not a product — it is an internal tool with a `tenant_id` column.**

Where this instruction is silent, ask. Do not decide. An invented decision that looks reasonable is the most expensive defect this project can produce, precisely because nobody will notice it.
