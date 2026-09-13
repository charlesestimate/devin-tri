# Magnus Workspace Platform — Base44 build specification

## Part 00 · How to use these parts, what they cover, and what was added

**13 September 2026 · prepared for Karl Ivan Estadola, Chief Executive Officer, Magnus Renewable Tech Corp**

This is the complete specification of the Magnus Workspace Platform, re-expressed for a Base44 build so that the same platform can be generated there and compared with the Hercules build. It is partitioned into twelve parts because no builder accepts thirty-six thousand words in one message, and because each part ends with checks that must pass before the next part starts.

Everything decided between 2 and 8 September 2026 is folded in: the archive function, the unread numbers, the Announcement channel with editable posts, Task (X) on the dashboard, the person card with the photograph on Google Drive, invite-only groups and rename, the derived project name, the three themes, the four protocol scopes with propose-then-confirm, the twenty-five migration import tools, Operations and Maintenance with gate 34, and the sixteen defects found in the first build — each turned into a rule and a test so the second build cannot repeat them.

---

## 1. The parts

| Part | File | Words | Build order |
|---|---|---|---|
| 01 | `PART-01-FOUNDATION.md` | 6,100 | **First. Nothing else starts until its twelve checks pass** |
| 02 | `PART-02-PIPELINE-PROJECT-DESIGN-PROCUREMENT.md` | 3,000 | Phase 1, stream A — serial |
| 03 | `PART-03-BLOCKS-SITE-PERMITS-INVENTORY.md` | 2,700 | Phase 1, stream A continues; inventory may run in parallel |
| 04 | `PART-04-MANPOWER-SAFETY-TASKS.md` | 2,300 | Phase 1, streams B and C — needs only `project_id`, `project_block_id`, `location_id` |
| 05 | `PART-05-MESSAGING-DOCUMENTS-DRIVE.md` | 3,900 | Phase 1, stream B — build the Drive file store first, then Messages, then Documents |
| 06 | `PART-06-FINANCE-HR-PAYROLL.md` | 2,500 | Phase 2 — after the spine delivers real values; Finance → Payroll → Human Resource |
| 07 | `PART-07-OPERATIONS-AND-MAINTENANCE.md` | 2,400 | Phase 2, last in the stream |
| 08 | `PART-08-REPORTING-ADMINISTRATION-COMPLIANCE-MOBILE.md` | 2,700 | Phase 3 for reporting; **the mobile section (E) is field-tested in week one** |
| 09 | `PART-09-MODEL-CONTEXT-PROTOCOL-SERVER.md` | 2,500 | Built incrementally alongside every part, never at the end |
| 10 | `PART-10-MIGRATION-AND-CUTOVER.md` | 1,700 | Phase 3 |
| 11 | `PART-11-NOT-BUILT-DEVIATIONS-LESSONS.md` | 2,400 | Read before every part, not after |
| 12 | `PART-12-ACCEPTANCE-TESTS.md` | 3,600 | Turned into a suite that runs; each part names its tests |

Every part opens with the same ten standing rules so that a part pasted into a fresh builder session still runs under them.

---

## 2. How to feed this to Base44

1. **Start with Part 11 section A and Part 01 in the first message**, in that order. Ask for the twelve checks at the end of Part 01 as pasted evidence before anything else is built. If the builder offers automations, scheduled functions, an in-app assistant or send-mail, decline each.
2. **Before Part 02, settle the table in Part 01 §1.1** — the nine things Base44 must be able to do (deny client writes on governed entities, tenant-filtered reads, an insert-only audit entity, no automations, an offline queue, a server-side Drive connection, a protocol endpoint or its HTTP equivalent, identity as a tenant property, no internal language-model call). Any *no* is a finding to record before building on, not after.
3. **One part per session, checks pasted at the end of each.** Do not let the builder summarise a check; ask for the search output, the query result, the refusal message.
4. **Part 09 travels with every part.** After each module, ask for that module's list, get, search and write tools, and for the tool enumeration document to be regenerated.
5. **Part 08 section E in week one:** a Person In Charge, a real rooftop, real Sorsogon signal, one photograph, one report. If the queue is not visible or a failure is silent, stop and fix it before any screen is built on top.
6. **Part 12 at the end of each part and in full before "complete".** Test 8 — twenty-four hours with nobody connected and an empty audit log — is run for real, not simulated.
7. **Compare against Hercules on the checks, not on the screens.** Both builds will look plausible. The checks are what tell them apart.

---

## 3. Coverage matrix — every source item and where it lives

| Source | Item | Part |
|---|---|---|
| Master specification §1–§2 | Governing principle, no automation, the two chokepoint requirements, uniqueness, offline | 01 §2, §4; 08 §E |
| §3, §4, §5 | Eight locked principles, no abbreviations, six hard blocks, five refusals | 01 §3, §0.7, §6 |
| §6 | Thirty gate rows, gate 7 band, R1–R12, statutory dual control, compensating queries | 01 §7 |
| §7 | Identity, roles, multi-role, crew not users, external gate holders | 01 §5 |
| §8.1 | Foundation tables, constants (five seeds), configuration, audit, erasure | 01 §4, §5, §8 |
| §8.2 | Notifications, personal panel versus executive view, landing screens, search, deep links | 01 §9, §10 |
| §8.3 | Account, site, contact, opportunity, assessment, proposal, the `won` handover | 02 §A |
| §8.4 | Party, bank change control, project, contract, risk terms, project parties, variations, turnover, portfolio | 02 §B |
| §8.5 | Design package, nine deliverables, waiting, bill of materials, seal, structural outcomes, weights | 02 §C |
| §8.6 | Procurement on the bill of materials, purchase orders, receipts, readiness, off-design, currency, supplier performance | 02 §D |
| §8.7 | Block spine, site report, toolbox, activities, photographs, non-conformance, derived completion, turnover | 03 §A |
| §8.8 | One permitting route, accumulation, additional requirement, expected dates, what permits gate | 03 §B |
| §8.9 | Locations, items, positions, the transmittal, stock on receipt, discrepancy, counts, zero tolerance, opening lock, quarantine | 03 §C |
| §8.10 | Resources, requests and decline reasons, three deployment layers, equipment, bench depth | 04 §A |
| §8.11 | Safety from the manual, permits to work, incidents, near-miss form, safety stop, corrective actions, inspections, indicators, emergency card | 04 §B |
| §8.12 | Tasks, output types, closure on output, blocked, priority scarcity, committed date, load bands, no-task Check | 04 §C |
| §8.13 | Communication rules — mention, no mute, append-only, search, convert, offline order | 05 §A6 |
| §8.14 | Document control, revision-in-force, classification under gate 33, forms as controlled documents, permanent classes, legal hold | 05 §B |
| §8.15 | Sub-ledger, milestones, claims, fund requests, write-offs, cash forecast bands, percentage of completion, reconciliation | 06 §A |
| §8.16 | Human Resource, no rating from data, requisitions from declined requests, reviews, anonymous engagement, onboarding, exit, self-service | 06 §C |
| §8.17 | Payroll, separation of duties, bracket tables, historical reproducibility, no report no payroll, acknowledgement sheet, three cycles | 06 §B |
| §8.18 | Exception queries with timestamp and rule count, four contents, drill, six domains, measure register, gaming guards, board pack | 08 §A |
| §8.19 | Administration — configurable, not configurable, change log, churn, second tenant | 08 §B; 01 §11 |
| §8.20 | Backup with tested restore, full export, retention `[CONFIGURED]`, security review | 08 §C |
| §8.21 | Accounting read, government figures not filing, no mail, accumulated reference data with sample size | 08 §D |
| §8.22 | Migration and cutover, freezing not deleting, training, what is said to staff | 10 §A |
| §8.23 | Operations and Maintenance in full, amendments, gate 34, extensions to 9 and 11 | 07 |
| §9, §10, §11 | Mobile and field, devices and revocation, access lifecycle | 08 §E, §F, §G |
| §12 | Protocol server — authentication, read, write, configuration rules, never writable | 09 |
| §13 | Screens and the eighteen-item sidebar | 01 §10, §11; each part's Screens |
| §14 | Acceptance tests 1–214 | 12 |
| §15, §16, §17, §18 | Not built, deviations D1–D13, build order, self-verification | 11 §A, §B; 00 §2; each part's Checks |
| MCP prompt A1–A6 | Hard block 6 flag, project site and client, sources on every figure, zero-rule domains, chain panel true last sequence, sidebar drift | 09 §3; 02 §B; 08 §A; 01 §4.2, §10 |
| MCP prompt B1–B5, scopes decisions | Four scopes, propose-then-confirm, agent sessions tab, no break-glass | 09 §2, §5 |
| MCP prompt C | Twenty-five import tools, validate, reverse, opening stock lock request | 10 §C |
| MCP prompt D | Tests 215–236 | 12 |
| Chat and Drive prompt A1–A6 | Messages screen, account space, groups, direct, `get_account_activity` | 05 §A1–A4; 09 §3 |
| Chat and Drive prompt B1–B8 | Drive as file store — connection, `file` record, upload, read, folder tree, erasure, move, Workspace later | 05 §D |
| Chat and Drive prompt C | Tests 237–258 | 12 |
| Archive prompt | Who may archive, read-only, searchable, restore, automatic restore, Archived section, protocol tools | 05 §A7; 09 §4 |
| Naming and groups prompt | Derived project name, `project_number` immutable, `local_government_unit`, group information panel, rename, member tools | 02 §B; 02 §A; 05 §A4; 09 §4 |
| Theme picker prompt | Three themes, contrast, placement | 01 §10 |
| Pending list A1 | Archive a thread or space | 05 §A7 |
| Pending list A2 | Unread numbers — General (5), Messages (X) | 05 §A1; 01 §10; test 279 |
| Pending list A3 | Task (X) that persists until delivered | 01 §10; 04 §C |
| Pending list A4 | Announcement channel beside General, administrator-only posting, editable with revisions | 05 §A5 |
| Pending list A5 | Person card — numbers, email, photograph on Drive, note; upload control reused | 01 §5; 05 §C |
| Pending list B1–B16 | Sixteen first-build defects | 11 §C; tests 259–280 |
| Pilot ground rules | Published in-platform page; rules withdrawn as checks pass | 10 §E |
| Decisions of 8 September | Drive for files; General open, Announcement restricted and editable; unread is a bug | 05 |

---

## 4. Additions this specification makes beyond the Hercules prompts — strike any you disagree with

These are my decisions, taken to close defects found in the first build. Each is small, each is marked in the part where it appears, and each can be removed without touching anything else.

| # | Addition | Where | Why |
|---|---|---|---|
| 1 | **Gate 35 — cryptographic erasure**, primary console holder, alternate second console holder. The gate table therefore holds thirty-one rows | 01 §7 | Erasure is the only irreversible operation and the first build let anyone with a reason string perform it (B4) |
| 2 | **R13 — reconfiguring a gate is itself under gate 31**; gate 32's own row needs both console holders | 01 §7.1 | Alfie reconfigured gate 24 on 9 September with no authority check |
| 3 | **A role grant is `pending_approval` until gate 24 decides**, and the subject of a grant cannot approve it | 01 §5 | B3 |
| 4 | **Every seed gate row ships with its primary and alternate populated** | 01 §7 | B1 — thirty gates with no approver |
| 5 | **Archive is a shared state with an owner**, per the archive prompt of 8 September — not the per-person flag the pending list first suggested; **a direct conversation may be archived by either participant, for both** | 05 §A7 | The archive prompt supersedes the pending list's first sketch; direct conversations were not covered by either, so I chose the rule that matches the others |
| 6 | **`supplier_invoice` and `supplier_payment`** — accounts payable as a sub-ledger record | 02 §D; 06 §A | B9 — nothing recorded what was owed |
| 7 | **Purchase order numbers counted per tenant per month, never per project** | 02 §D | B16 collision |
| 8 | **Every hand-off raises a notification in the same transaction** — stated as a foundation rule, not left to each module | 01 §9 | B13 |
| 9 | **One reusable file control with Print/Send** on every object that leaves the company | 05 §C | B14 |
| 10 | **Export enumerates the schema and never falls back to an unfiltered read** | 08 §C | B5 |
| 11 | **A role with no permission rows sees nothing** | 01 §5 | The first build showed every module to a person with zero rows |
| 12 | **Tests 259–280** | 12 | One test per first-build defect |
| 13 | **Part 01 §1.1** — the nine Base44 capabilities to verify before building | 01 | The original was written for a hand-built backend |

Everything else is the Hercules specification as written, with Convex-specific wording replaced by platform-neutral wording (a "wrapper around `ctx.db`" becomes "one server-side data-access layer"; "`ctx.scheduler` and `crons`" becomes "the builder's automations and scheduled functions").

---

## 5. What Base44 will most likely struggle with — watch these

Recorded so the comparison with Hercules is fair. None of these is a reason to skip the requirement.

1. **The append-only audit table and the hash chain** — an owner of a Base44 application can usually edit any row through the builder's console. The specification accepts that and relies on the chain to detect it; what Base44 must guarantee is that no *application* path can edit it.
2. **The offline queue with a visible upload list and device idempotency keys** — a generated React front end may not carry this without explicit, repeated instruction. Test 169 to 178 decide it.
3. **The Model Context Protocol endpoint** — Base44 backend functions can expose HTTP; whether a protocol client can connect directly is to be verified. The HTTP-tools-plus-adapter fallback in Part 09 keeps the rules intact either way.
4. **Google Drive server-side with an encrypted refresh token** — needs a backend secret and a backend function; the device must never see the token.
5. **Denying client-side writes to governed entities** — Base44's per-entity access rules must be checked for every governed entity; one entity left open is one tenant seeing another.
6. **The temptation of built-in features** — automations, the in-app language model, send-mail, and a "user" object standing in for `person`. Each is declined in the standing rules; each will be offered.
