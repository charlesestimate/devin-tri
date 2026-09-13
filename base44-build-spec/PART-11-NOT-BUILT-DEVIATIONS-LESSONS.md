# Magnus Workspace Platform — Base44 build specification

## Part 11 · Deliberately not built · Deviations from the source specification · Lessons from the first build

**Read section A before starting each part, not after.** The most expensive thing a builder can do on this project is build something nobody asked for. Section C lists what the first build got wrong so that this build does not repeat it.

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

# A. DELIBERATELY NOT BUILT — DO NOT ADD ANY OF THESE

| Not built | Why |
|---|---|
| Any scheduler, cron job, background worker, queue processor, timer, polling loop, automation, trigger or workflow — including the builder's own automation features | Part 01 §2 |
| Any client-side write to a governed table | Part 01 §4 |
| A person record created to give an agent an identity; a service account | Part 09 §1 |
| An exception engine, rules engine or workflow engine; a nightly pass | Agents do this |
| Ranked exception lists, severity scoring, consequence ordering, item caps | Judgement, not a rule |
| Automatic escalation of anything to anyone; automatic pass-down when a window expires | Windows are recorded, never acted on |
| Auto-approval of anything, at any threshold, ever | R1 |
| Automatic raising of retention invoices, progress claims or billing schedules | The dates are stored; an agent reads them |
| Automatic generation of deliverable tasks or client obligations at signature | An agent generates; the platform stores |
| Automatic Non-Conformance Report or corrective action creation | A person or an agent raises them |
| Automatic statutory-deadline task creation; automatic instantiation of recurring obligations | Stored and queryable; an agent instantiates |
| Outbound electronic mail or short message service, for anything | Only the three-category push leaves the platform |
| Notification digests, summaries or roll-ups | Part 01 §9 |
| An in-platform chat assistant or any language-model call from inside the platform | The intelligence connects from outside |
| Predictive curves, delay forecasting, bill of materials generation, lead scoring, probability weighting, approval prediction, predictive cash modelling | No accumulated history yet |
| Autonomous agent action without a human decision | It fails confidently, not visibly |
| Automatic resource allocation, supplier selection, bid scoring, automated proposal generation or pricing | A person decides |
| Administrative screens for maintaining accumulated reference data | Part 08 §D |
| A general ledger, chart of accounts, journal posting, statutory statements, or writing to the accounting system | It is a sub-ledger |
| Automatic filing to any government portal | Filing is a person's act |
| Any presence, location, activity, keystroke or login-time tracking; page-view logging; fatigue tracking | L4 |
| Any field where a person types a project percentage complete; hours, timers or activity feeds on tasks | Parts 03 and 04 |
| Any per-person rating, score, index, aggregate grade, numeric load value, ranking or forced distribution; automatic conversion of ratings or recognition to money; identifiable engagement responses | L7 |
| Reporter identity or per-person incident counts outside the safety function | Part 04 §B |
| A headcount integer in place of named toolbox attendees | Part 03 §A2 |
| Photograph upload from, or writing to, the device gallery; site photographs as message attachments; silent discarding of any field record | Parts 05 and 08 |
| A configurable block spine, removable structural dependencies, or a project phase badge | Standardisation is the product |
| Weight re-basing on a cost correction | Part 02 §C |
| A seventh hard block, an `active` flag on hard blocks, or any override, exception or emergency path; a shared implementation for gates and hard blocks | Part 01 §6 |
| A separate procurement list; procurement creating bill of materials lines; a request-for-quotation object; a supplier rating screen; an approval above the Procurement Head; blocking a bank change | Part 02 §D |
| Automatic reordering, or reorder points on project material; a tolerance band on counts; custodian variance as a score; stock arriving on despatch; surplus returned at current price; a second live version of form MRTC-PROC-F003; barcode scanning | Part 03 §C |
| A hand-maintained permit requirement library or duration table; capacity-based permitting branches; merging permits with permits to work | Part 03 §B |
| Overwriting one deployment layer with another; a combined decline rate; equipment custody by location; entered utilisation; leave reason visible beyond Human Resource | Part 04 §A |
| Auto-approval or delegation on any permit to work; an alternate for lifting a safety stop; additional fields on the near-miss form; entered safety indicators; invented checklist content; a general safety module | Part 04 §B |
| A contract template or clause library; defaulted or inferred terms; automatic clause extraction; tax computation on related parties; a single party field on the project; site as a field on the account; collapsing *did not proceed* into *lost*; contingency on client output; editing a frozen proposal; a threshold on gate 6 | Part 02 |
| Links from records to a document rather than a revision; deleting or replacing superseded revisions; automatic classification; blocking unclassified documents from being read; acknowledgement of a document rather than a revision; a hand-built required-document checklist; document editing in the platform | Part 05 §B |
| Thread subscription, watch or mute; a per-person hide of a conversation; message deletion; message editing outside a post-restricted company channel; presence, typing or read receipts; voice or video; a configuration screen for which objects carry threads; real-time infrastructure beyond polling; migration of Messenger history into threads; external or client participation in threads | Part 05 §A |
| Password storage, reset or recovery; sign-in for site crew; a single-role model; one combined permission level | Part 01 §5 |
| Any view of another person's notification panel; ranking or capping in the panel; badges on Information; stored badge counters; group-addressed notifications; clearing a notification by reading it; removing a push carve-out category | Part 01 §9 |
| Offline editing of shared records; offline approval; a native store application | Part 08 §E |
| Deletion of any person, role, gate, message, thread, channel, incident, safety record, file record or audit entry | Nothing is deleted |
| Any tool, verb or parameter capable of disabling a hard block; elevated authority through the protocol; silent application of a configuration change; a break-glass scope | Part 09 |
| Retention periods invented by the platform; a position on Bureau of Internal Revenue registration; bulk configuration import; backups without a tested restore | Parts 01 and 08 |
| Migration of finished projects; absorption of the archive; typed percentage on migrated projects; deletion of any superseded system; payroll cutover on fewer than three cycles; dropping an unreported worker; payroll visibility for Project Managers, Persons In Charge or console holders | Parts 06 and 10 |
| Populated career paths and bands; exit interviews by the manager; a management-only ladder | Part 06 §C |
| Tenant configuration screens for other tenants; subscription billing; client portals; marketplace features; electronic wallet payroll; a security review gate before internal go-live | Later phases |

---

# B. DEVIATIONS FROM THE SOURCE SPECIFICATION

Every one is a deliberate simplification made to remove automation. **Each must be reversible without a schema change:** keep `window_working_days`, `passed_down_at`, `original_approver`, the `awaiting_alternate` and `escalated` states, the stored retention and statutory deadline dates, and the recurring-obligation cadence definitions exactly as specified, even though nothing acts on them.

- **D1 · Approval windows no longer act.** Stored and displayed; nothing passes authority down. An agent reads pending approvals with age against the window.
- **D2 · No nightly pass.** On-demand queries returning their own evaluation timestamp and rule count.
- **D3 · No exception ranking or twelve-item cap.** Agents rank from the same facts; the four contents of every row are retained.
- **D4 · Retention and progress-claim invoices are not raised automatically.** The highest-value automation removed. The date is stored; an agent must read it. If no agent runs, the retention leak reopens.
- **D5 · Non-Conformance Reports are not raised automatically** on a damaged, wrong or short delivery. Quarantine still happens in the same transaction.
- **D6 · Corrective actions are not raised automatically** from a failed inspection item.
- **D7 · Statutory obligations do not raise themselves.** Non-compliance penalties reach ₱50,000 per day; this deserves a named agent obligation and a named human owner.
- **D8 · No escalation ladders anywhere.** Everything remains queryable with its age.
- **D9 · The `supplier` object is merged into `party`.**
- **D10 · The in-platform assistant and artificial-intelligence layer are deleted.** The protocol server satisfies both halves of the instruction — connect Claude to the platform, and configure the platform using Claude — without any model inside it.
- **D11 · Recurring obligations are definitions, not instances.**
- **D12 · Weekly digests are queries, not deliveries.**
- **D13 · Google Workspace sign-in is deferred to the tuning phase.** The identity provider remains a property of the tenant; the only field that knows the provider's user identifier is `person.identity_subject`. **Before production: switch the Magnus tenant to Google Workspace, domain-restricted, disable the password path, and confirm that disabling a Workspace account ends the platform session.**

**Everything else in the source specification is implemented as written.**

---

# C. LESSONS FROM THE FIRST BUILD — SIXTEEN THINGS NOT TO REPEAT

Each was found by reading the first build's source and its live data in September 2026. Each is now a stated rule in the relevant part and a test in Part 12.

| # | What happened | Rule in this specification |
|---|---|---|
| 1 | Thirty gate rows shipped with no primary or alternate on any of them; every approval screen refused for a month | Part 01 §7 — seed rows ship populated; a gate with no primary is a build defect |
| 2 | A complete, correct approval engine existed and **nothing called it**; seventeen approval points stored an approval reference as a plain string and checked nothing | R11 — every approval point calls the one engine; test 15 |
| 3 | A role took effect the instant its gate 24 request was raised; a refusal never revoked it; the newly granted role could approve its own grant | Part 01 §5 — `pending_approval` confers nothing; R6 extended; tests 260 to 262 |
| 4 | Anyone signed in could reconfigure any gate | R13 — gate reconfiguration under gate 31 |
| 5 | Cryptographic erasure — the only irreversible operation — needed only a non-blank reason | Gate 35; legal hold refuses |
| 6 | The compliance export fell back to an **unfiltered** read when a tenant index was missing, named phantom tables from a hand-kept list, and omitted twenty-one real ones | Part 08 §C — schema-enumerated, tenant-filtered, no fallback |
| 7 | Protocol tools reimplemented mutations: a constant patched in place (a version dated 2030 to 2026), a revision set in force from free text, a role granted with no gate and no duplicate check, a role created without the uniqueness check the screen has | Part 09 §1 — every tool calls the screen's function |
| 8 | Three registers — seed specification, live rows, module comments — disagreed on twenty-five gate labels and eleven gate meanings | One registry, one seed, a script that checks every gate number in code and tests against it |
| 9 | Four of six hard blocks existed as rows and helpers nothing called; the spine lacked B0 | Part 01 §6 — every block wired; Part 03 spine includes B0 |
| 10 | A goods receipt moved no stock; procurement and inventory shared no data | Part 02 §D — receipt moves stock in the same transaction |
| 11 | No accounts payable existed | `supplier_invoice` and `supplier_payment` |
| 12 | Nobody was notified at any hand-off; every approval sat unseen | Part 01 §9 — notification in the same transaction at every hand-off |
| 13 | The only upload in the product was the chat composer; nothing could be attached, sent or printed | Part 05 §C — one reusable file control; Print/Send on the documents that leave |
| 14 | Console holder add and remove checked nothing; legal hold was a free boolean; revoking a role needed nothing; purchase order numbers collided across projects; a progress claim could not be created from the screen | Part 01 §5; Part 05 §B; per-tenant numbering; claim keyed to contract |
| 15 | Unread counters were kept correctly and drawn on one of three sections; the company channel was excluded from the total | Part 05 §A1 — every row and header wired; tested against the database |
| 16 | Deliberately fake statutory rate tables were approved into the live tenant and became immutable | Part 06 §B — live tables carry a legal reference; test data never approved in a live tenant |

**Also recorded:** a success message reading *Gate 24 approval request raised* was read by staff as failure — every hand-off message says what happens next and who is waiting on it. A project could never leave design because only one stage mutation existed — stage is derived from block states and no stage mutation exists to forget. A person with zero permission rows saw every module — a role with no rows sees nothing.
