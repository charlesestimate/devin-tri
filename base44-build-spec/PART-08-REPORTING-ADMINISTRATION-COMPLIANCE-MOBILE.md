# Magnus Workspace Platform — Base44 build specification

## Part 08 · Reporting and measurement · Administration · Data, security and compliance · Integrations and accumulated reference data · Mobile and field · Devices · The access lifecycle

**Prerequisite: Parts 01 to 07.** Reporting reads what the other parts wrote and creates almost nothing of its own; built early it produces confident screens over data that does not exist. **The mobile path (section E) is the exception to that ordering: field-test it before building any screen on top of it — it belongs to the first week, not the last.**

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

# A. REPORTING AND MEASUREMENT

**There is no exception engine and no nightly pass.** Every exception exists as **a query, evaluated on request, returning its own `evaluation_timestamp`, `rules_evaluated` and `sources`.** An agent reads them, ranks them, and decides what matters.

**Silence must never be ambiguous.** A domain with no exceptions states *Cash — checked 09:14, twelve rules, no exceptions.* A blank panel is a failure. **A domain that evaluates zero rules is a blank panel** — every domain below ships with its rule list implemented.

**Every exception row carries four things:** what · **who (a named person who can act, never a department)** · how long (age) · **so what (the consequence, valued wherever a value exists).** Every figure returned anywhere — summary, board pack, exception — carries a `sources` list of record identifiers.

**Drill path from any exception: exception → domain → record → audit log.** Every level respects record scope and money visibility.

**Six domains and their minimum rule lists:**

| Domain | Rules |
|---|---|
| Projects | no submitted site report in the last two working days · blocked activities with reason and expected clear date · blocks not startable with mobilisation planned · non-conformance reports open with ageing and same-day closure rate · design deliverables waiting by party with cumulative days · purchase orders past expected arrival · goods received short or damaged with no non-conformance report · variation orders ageing in `issued` · client obligations outstanding · percentage complete against the planned curve |
| Cash | uncertified claims beyond thirty days with the client baseline · retention due and overdue · projected negative position within three months · gated cash by gate, owner and age · closeout permits blocking final billing, valued · supplier payments after a bank change · unliquidated advances past due · service charges unpaid beyond terms |
| People | resource requests unfulfilled past needed-from · declined requests by reason · people with no assigned task, as a count across managers · regularization decisions due · certifications expiring within N days · bench depth · onboarding incomplete by manager · acknowledgement sheets outstanding · site days blocking payroll |
| Safety | safety stops open · incidents open · permits to work past validity · workers with lapsed training named on a permit · corrective actions open, overdue, closed without evidence · Construction Safety and Health Program status by project · statutory deadlines within N days · unacknowledged pushes |
| Permits | past expected approval date · prerequisite permits outstanding · additional requirements open · follow-ups required per office · consultant engagements open · regulatory version mismatches |
| Operations and maintenance | the eleven queries of Part 07 §7, **underperforming sites ranked by estimated lost generation valued at that site's tariff — never by severity** |

**Role scoping:** Chief Executive Officer and Chief Operating Officer — all six company-wide · Director — own projects plus company-wide safety and cash · Head of Finance — cash and permits company-wide · Project Manager — own projects · Safety Officer — safety company-wide · Human Resource — people company-wide. Money visibility applies independently.

**`measure_register`** — measure · source records · **owner (a named person)** · cadence · **decision_informed (required — save refused without it)**. A measure with no decision is deleted.

**`report_register`** — every standing report, by module, owner and cadence.

**FOUR GAMING GUARDS:** load is banded, never scored, never an appraisal input · grades attach to deliverables, not persons; no per-person aggregate · reporter identity is never shown · safety indicators are never a personal score. The person with no task reaches the People domain as a count across managers, never as a named individual on an executive screen.

**The board pack is generated from platform data on request** — a `file` record under Reports — never assembled by hand.

**Screens:** the executive view (six domains, each stating its check time and rule count) · exception drill · measure register · report register · board pack.

---

# B. ADMINISTRATION

**The single place everything is configured, with the right authority, without a code change.** Part 01 §11 lists the screens; this section states the rules.

**Configurable:** system constants (gate 22) · thresholds (gate 31) · gate limits, primaries, alternates and windows (alternate authority validated at save; reconfiguration itself under gate 31, R13) · **hard block values only** · roles, permissions and money visibility (gate 32) · labels · the push list (additions permitted; the three cannot be removed) · landing screens · retention schedules and legal hold · statutory rate tables (Human Resource enters, Finance approves) · working calendar · controlled lists · console holders (by a current console holder, replacement named first).

**NOT configurable, by any permission level, screen, protocol call or database route:** the audit log cannot be made editable · statutory calculation results cannot be overridden · tenant isolation cannot be disabled · the existence of any of the six hard blocks.

**Every configuration change is logged** with what changed, previous value, new value, who, when, reason where required, and arrival channel. System constants, hard block values, gate limits and statutory rates require a reason.

**The threshold churn query** shows which thresholds move most often. **The console change digest** is a query an agent delivers to a second named person (recommended Finance), not a scheduled mail.

**Three disciplines:** Magnus is a row of configuration, not assumptions in code · no Magnus literal anywhere · the invented second tenant exists in test from early on. **The block spine is the deliberate exception — identical for every tenant.** No bulk configuration import.

**Agent sessions** (Part 09): every session currently authorised, the person it acts as, scope, expiry, when authorised, last call, and a revoke control. Every person sees, on their own profile, the sessions acting under their name and can revoke any; console holders see all in the tenant.

---

# C. DATA, SECURITY AND COMPLIANCE

**The obligations are Magnus's.** Wherever the data sits, Magnus is the personal information controller. Mitigations, reviewable as a set: console holders have no access to salary, ratings, disciplinary or medical data · engagement responses store no `person_id` · reporter identity never appears · money visibility is a separate axis · quarterly access review · gated cryptographic erasure · legal hold.

**Backup: automated, encrypted, per tenant.** (The builder's platform backup counts only if a restore of it has been exercised.) **Restore: tested, to a working system, with date, duration and outcome recorded** — `restore_test` — and reported to the console holders. The restore test is a `recurring_definition` with a named owner.

**Full export.** `data_export` — requested_by · requested_at · scope · file_id · tables_included · row_counts. Magnus can export its own data in full, at any time, in a documented, re-importable format (one file per table, with a manifest listing every table and its row count). **The export enumerates every table in the schema from the schema itself — never from a hand-maintained list** — so a new table cannot be omitted, a phantom cannot be named, and **every table is read through the tenant filter with no unfiltered fallback.** Export is logged and respects the exporter's permissions and money visibility. Build and test it in this part, not later.

**Cryptographic erasure** — Part 01 §4.2, under gate 35, refused under legal hold, deletes the Drive files of the data subject (Part 05 §D6).

**Retention schedules are `[CONFIGURED]`, pending counsel.** A retention run is an action a console holder starts, listing what it would remove before it does; the eight permanent classes and anything under legal hold are never included.

**A security review is required before any outside tenant is admitted**, not before internal go-live.

**Screens:** restore test record · export · retention (preview and run) · legal holds · erasure requests (gate 35).

---

# D. INTEGRATIONS AND ACCUMULATED REFERENCE DATA

**The accounting system: the platform reads; it does not write.** **Government channels: the platform produces the remittance figures — Bureau of Internal Revenue, Social Security System, PhilHealth, Pag-IBIG, Department of Labor and Employment — and does not file.** It holds the deadline, records the reference once a person has filed, and stops. **No outbound electronic mail, for anything.** The only outward delivery is the safety push.

**`statutory_remittance`** — agency · period · amount (computed from the payroll lines) · due_on · filed_reference · filed_by · filed_on. **Electronic signature** where a counterparty requires it. **Electronic wallet payroll is deferred** and recorded as the structural fix for the cash distribution exposure. **Google Drive** is the file store (Part 05 §D). The import path is Part 10.

**ACCUMULATED REFERENCE DATA — no administrative screen exists for maintaining any of it.** Price history by item · actual supplier lead time · supplier performance · block cycle time · permit duration per local government unit · permit requirements per office with times observed · permit fees per type and office · consultant engagements per office · actual yield against the Specific Yield constant · client certification behaviour · client payment behaviour · structural outcome history (assessment confidence against certification result) · resource demand (requested, allocated, declined by reason) · arrival against completion by team · time to hire and source effectiveness at twelve months · attrition by tenure, role, region and manager · off-design purchase rate · checklist item failure rates · threshold churn · approval turnaround · storage growth per project.

**Every accumulated figure is presented with its sample size** — *median 62 days, from 4 observations* — and falls back to the documented default where history is insufficient.

---

# E. MOBILE AND FIELD — THE PART ON WHICH THE PLATFORM SUCCEEDS OR FAILS

**The Person In Charge is the only site user** and is the source of the site report, the toolbox attendance record, the payroll attendance, the block progress and the photographs that carry all of it. **If the mobile path fails silently once, that person returns to Facebook Messenger permanently.**

**Deliver as a progressive web application.** No store on the critical path; a fix reaches Sorsogon the next time the application opens.

**Field users CREATE records offline. Field users do NOT EDIT shared records offline.** The exception is Part 07's owner-only work order transitions. **No approvals offline, ever.** Capture offline; decide online.

**The offline queue** — held on the device (IndexedDB) with **device-generated idempotency keys** (`client_message_key` and equivalents on every offline-creatable record: site report, toolbox meeting, activity, photograph, message, non-conformance report, goods receipt, transmittal receipt, incident, safety stop, work order transition): compose queue · automatic resumable retry with backoff · **messages and records send in composition order** · **text before attachments** · de-duplication by key on the server · **the queue is visible** on the Today screen with what has and has not gone, and a retry control · **the original is retained on the device until the server confirms**.

**Photographs:** in-app capture only, **never from the device gallery, never written to the gallery** · compressed on the device to approximately 300 kilobytes (mandatory) · queued and resumable · thumbnails generated once on the server.

**Nothing captured in the field is ever discarded.** A record that cannot be synchronised is retained and shown as unsent, indefinitely. A record whose parent has since changed is accepted and flagged for review. A record whose parent has been deleted is held and raised as a Check. Two creations of the same logical record are de-duplicated by key.

**Sizing:** ten to twenty-five photographs per report, about 72 megabytes per working day across twelve projects, 18 gigabytes a year. **The platform reports storage growth per project.** Data allowance is a real cost to a real person; Magnus decides how it is covered (open item 9).

**Low-signal behaviour:** the application opens and works with no connection, with today's work cached · background retry · **the site emergency card works offline**.

**The Today screen** (Person In Charge landing): site report status · toolbox meeting with the topic proposed from today's permits to work and recent near misses · deployment for the day · open permits to work · deliveries expected today · **the upload queue**.

**FIELD-TEST THIS PATH BEFORE BUILDING ANY INTERFACE ON TOP OF IT.** A Person In Charge, a real rooftop, real Bicol or Sorsogon signal, a photograph and a report — offline queue, retry, compression, background upload, visible queue. Not a developer on office wifi.

---

# F. PERSONAL DEVICES AND REVOCATION

Field users work on personally owned phones. **The company does not own them and will never wipe them.** The application holds a working cache and an offline queue only. **On revocation the cache becomes unreadable and the account is dead; server-side revocation is the entire security control.** Device management applies to company-owned laptops only.

---

# G. THE ACCESS LIFECYCLE

**Onboarding:** Human Resource creates the person record · the department head assigns roles under gate 24 (the row is `pending_approval` until decided) · the identity provider account is created outside the platform and linked by `identity_subject` · capability tags assigned · **a record with no current role has no access.**

**Role change or transfer:** the old `person_role` closes with `effective_to`; a new row is added. `department` and `region` scope follow the current role, so access to the previous department's records ends on the effective date — **the person's manager is notified before it takes effect.**

**Departure, in this order:** identity provider account disabled → `suspended` automatically · Human Resource sets `departed` · **every open task, approval and deliverable owned by that person is listed and must be reassigned — offboarding refuses to complete otherwise (refusal 4)** · console holder status removed with a replacement named first · device cache becomes unreadable · agent sessions revoked · **the person record is retained.**

**Quarterly access review under gate 32:** per person, current roles, the permissions those roles grant, and what that person has actually used in the period (from the audit log, never from page views). Console holders review and remove what is no longer needed. `access_review` — period · reviewed_by · per-person outcomes · completed_at.

---

## H. Checks before Part 09 starts

1. Each of the six domains states its check time and rule count when empty; every exception names a person and carries a valued so-what; drill reaches the audit log; a measure with no decision is refused.
2. Every summary, exception and board pack figure returns non-empty `sources`; the board pack generates with no manual step.
3. Search every screen, query and export for a per-person load score, a per-person grade aggregate, reporter identity, or a per-person safety score — none.
4. Export all tenant-one data: the manifest lists every table in the schema with row counts; a tenant-two record appears nowhere; re-import into a clean test tenant succeeds. Restore a backup to a working system; date, duration and outcome recorded.
5. Search for outbound mail transport and any route submitting to a government channel — none.
6. A full working day in flight mode: report, toolbox record with photographs, checklists and messages captured; synchronise correctly with creation times preserved. Force upload failures — every record retained and shown as unsent with retry. Kill the application mid-upload — the original is retained. Capture ten photographs — none in the gallery; no route attaches from the gallery; uploaded size about 300 kilobytes.
7. Disable the identity provider account — the session ends, the person is `suspended`, the cache is unreadable, agent sessions are refused.
8. Complete offboarding for a person holding an open approval — refused, listing the item.
9. Acceptance tests 152 to 158, 169 to 184 and 189 from Part 12 pass, with output pasted.
