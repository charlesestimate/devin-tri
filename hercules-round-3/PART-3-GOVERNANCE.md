# Magnus Workspace Platform — Hercules build specification, round 3

## Part 3 of 4 · Governance — gates, approvals, role grants, hard blocks, erasure, export, the registers, and the protocol surface

**Prepared for Karl Ivan Estadola, Chief Executive Officer, Magnus Renewable Tech Corp · 17 September 2026**

Third of four parts. **Build after Parts 1 and 2, in its own thread.** Nothing here is new: every item was reported on 8 September in the pending list and checked again on 17 September. They are grouped so that Hercules makes each decision once rather than twelve times. Line numbers are from the 8 September export.

### How to use this document with Hercules

Build mode, new thread, paste the whole part. Fix root causes; paste the evidence in section E. One part, one thread, one report.

### Standing rules that still apply

Gates and hard blocks are data rows; **one approval engine serves every gate and no module implements approval logic of its own**; nothing is ever auto-approved; a hard block is evaluated before any gate and has no switch; the audit log is append-only; every protocol tool calls the same mutation the screen calls; nothing is deleted. Where silent, ask.

---

# A. THE STATE OF THE GATES ON 17 SEPTEMBER

- Thirty gate rows exist. **As of 9 September, twenty-nine had no primary and no alternate.** Only gate 24 (*Role Assignment*) had been configured — on 9 September at 02:47 by Alfie Jie Villalon, a Process Engineer, with primary `chief_executive_officer` and no alternate, and touched again on 10 September — which shows both that the screen works and that **anyone signed in can reconfigure any gate** (§C3). The protocol's `list_gates` **does not return the primary and alternate fields at all** (it returns only label, description, `noAlternate` and window), so the state cannot be re-verified from outside; test G1 asks for the table from the database, and §C10 adds the fields to the tool.
- The approval engine in `convex/foundation/gates.ts` — `approveRequest`, `rejectRequest`, `checkGateAuthorisation` with the R6 self-approval refusal in the specification's own words — **has zero callers outside its own file.** Seventeen approval points across six modules accept an approval reference as a plain string and check nothing.
- Only five gates ever raise a request (6, 7, 18, 24, 34). Live `approval_requests` holds eighteen rows, all unfired; four are Alfie's gate-24 requests (three duplicate Account Officer grants for Althea Marie, one for a suspended person).
- The pilot ground rules published on 4 September still hold: *an approval inside the platform is not an approval*, and *a permit to work that exists only in the platform is not a permit to work.* This part is what withdraws them.

---

# B. THE ONE DECISION — `seed.ts` IS THE REGISTER

Three registers disagree: the seed specification, the live rows, and the comments in the modules. Twenty-five of thirty live gate labels differ from `seed.ts`; eleven gate numbers mean something different in the module that uses them than in the specification (gate 24 is *Role Assignment* in identity and *Employment Offer* in Human Resource; gate 32 has three claimants). **Rule: the thirty rows in `seed.ts` are the register. Every module, every label, every test, every comment is corrected to it, and a script checks every gate number and hard block number that appears in code or tests against the seed and fails the build on any mismatch.** Thirteen open questions then become mechanical corrections.

The register, for reference — number, gate, primary, alternate, window: **1** write-off ≤ ₱50,000 · Head of Finance · Chief Operating Officer · 3 — **2** write-off ₱50,001–100,000 · Chief Operating Officer · Chief Executive Officer · 3 — **3** write-off > ₱100,000 · Chief Executive Officer · none — **4** purchase order ≤ ₱100,000 · Procurement Officer · Procurement Head · 2 — **5** purchase order > ₱100,000 · Procurement Head · Chief Operating Officer · 3 — **6** quotation release, all · Director on the project · Chief Executive Officer · 2 — **7** quotation below policy markup · Chief Executive Officer · none — **8** variation order · Director · Chief Executive Officer · 2 — **9** contract or customer agreement signature · Chief Executive Officer · none — **10** counsel review · Atty. Caneja (person) · Chief Executive Officer accepting the risk · 3 — **11** progress claim or service charge · Head of Finance · Chief Operating Officer · 2 — **12** retention invoice · Head of Finance · Chief Operating Officer · 5 — **18** design release for permitting · Professional Electrical Engineer seal (person) · none — **19** non-conformance closure · Project Manager · Chief Operating Officer · 3 — **20** permit consultant, no threshold · Chief Operating Officer · Chief Executive Officer · 3 — **21** Turnover Document · Project Manager · Chief Operating Officer · 2 — **22** system constant · Chief Executive Officer · none — **23** payroll release · Head of Finance · Chief Operating Officer · 1 — **24** new hire or role assignment · department head · Chief Operating Officer · 5 — **25a** inter-island transfer, any value · Procurement Head · Chief Operating Officer · 2 — **25b** within-island > ₱100,000 · Procurement Head · Chief Operating Officer · 2 — **26** stock adjustment, all · Head of Finance · Chief Operating Officer · 3 — **27** opening stock lock · Cristy (person) · none — **28** permit to work · Safety Officer of record · none — **29** safety stop lifted · Safety Officer of record · none — **30** incident closure · Safety Officer, countersigned Chief Operating Officer · none — **31** threshold change · domain owner · Chief Executive Officer — **32** role permissions · console holder · second console holder — **33** document classification · Cristy (person) · none — **34** warranty claim · Head of Finance · Chief Operating Officer · 3. Numbers 13–17 reserved; no bare 25.

---

# C. THE ITEMS

## C1 · Configure every gate — the single highest-value hour available

Set primary and alternate on all thirty rows from the register above, as **seed data on every tenant creation** and as a one-time correction on the Magnus tenant. Where the primary is a person (10, 18, 27, 33) set `primaryPersonId`; Cristy's record is `ks71rnr6pzhxb6cy8efxd4gvan8dswab`. For gate 24 add the alternate `chief_operating_officer` (Beda) so that Karl is not the only person who can approve a role grant. A gate with no primary is a build defect, not a configuration task: the seed must not ship one.

## C2 · Route every approval through the engine, and make a grant follow its decision

1. Every approval point calls `gates.ts` — `raiseRequest`, `approveRequest`, `rejectRequest`, `checkGateAuthorisation`. The seventeen points: quotation release (6, 7) · variation order (8) · contract signature (9) with counsel outcome (10) · progress claim and service charge (11) · retention invoice (12) · design release (18) · non-conformance closure (19) · permit consultant (20) · Turnover Document (21) · system constant (22) · payroll release (23) · role assignment and offer (24) · transmittal (25a, 25b) · stock adjustment (26) · opening lock (27) · permit to work (28) · safety stop lift (29) · incident closure (30) · threshold (31) · role permission (32) · document classification (33) · warranty claim (34) · write-off (1–3) · purchase order (4, 5). No record reaches an approved state by any other path; the string fields that hold an "approval reference" today are replaced by `approvalRequestId` verified against an approved request in the same mutation.
2. **Raising a request notifies the primary approver (Task) and the alternate (Information) in the same mutation.** Deciding it notifies the requester (Response). This is the hand-off the first build omitted everywhere (Part 4 §D3).
3. **My Approvals** (Part 2 §B3) lists every pending request where the person is primary or alternate; the detail shows the full object.
4. **A role grant is `pending_approval` until gate 24 decides.** `assignRole` (identity.ts lines 533–616) inserts the `person_roles` row live in the same mutation as the request. Change: the row is inserted with `state = "pending_approval"` and confers nothing; `approveRequest` for gate 24 sets it `current`; `rejectRequest` sets it `refused`. Every role-listing query and `resolvePermissions` ignore rows that are not `current`. `assignRole` refuses a duplicate current or pending row for the same person and role, and refuses a subject whose status is not `active` or `pending`. The success message reads *Role assignment requested. Waiting for approval by [primary] (alternate [alternate]).* — never *Gate 24 approval request raised*, which staff read as failure.
5. **R6 extended:** the subject of a grant cannot approve the request that grants them the role; two protocol tokens held by one person are one person.
6. Clean the live requests: approve or refuse Alfie's four gate-24 requests; refuse the two duplicate Account Officer grants for Althea Marie and the grant for the suspended person, with a note.

## C3 · Gate reconfiguration is itself governed

`convex/foundation/adminConfig.ts` `updateGateConfig` (line 12) checks only that the caller is signed in — which is how a Process Engineer configured gate 24. Change: only a console holder may call it; every change raises **gate 31** (console holder as domain owner) and applies on approval; a change to gate 32's own row requires both console holders; R3 (alternate authority not lower than primary) and R5 (no alternate, window or delegation on 18, 28, 29, 30) are refused at save; every change is logged with previous and new values and a reason.

## C4 · Console holder guards

`addConsoleHolder` (identity.ts 983) and `removeConsoleHolder` (1027) check nothing about the caller. Change: caller must be a current console holder; a third holder is refused; removal of the second is refused unless a replacement is named in the same mutation; both logged. A console holder may then use `directAssignRole` (871), which bypasses gate 24 by design — so the guard on the seat is the guard on the bypass.

## C5 · Cryptographic erasure is gated

`convex/compliance/compliance.ts` `performErasure` destroys a person's key permanently and requires only a non-blank reason. It is the only irreversible operation in the platform. Change: raise **gate 35 — cryptographic erasure**, primary the primary console holder, alternate the second console holder (add the row to the seed; the register then holds thirty-one rows and the identifier space 1–35, 13–17 still reserved); refuse under legal hold; delete the person's Drive files through the connection in the same mutation; the entry survives as *Content removed under data-subject request, [date], [authority]*; the chain still verifies. Until the gate is wired, hide the Erase button.

## C6 · Roles, permissions and money visibility — seed and enforce

Seven of thirty-three active roles are held by nobody; most roles have no permission rows; `setRolePermission` (identity.ts 717) carries the comment *Requires gate 32 approval — but for now records it directly.* Change: `setRolePermission` raises gate 32 and applies on approval; seed a `view` permission per module for every existing role matching what the person sees today, so the *no rows, no access* rule of Part 2 §B1.6 can be switched on without anyone losing a screen; `record_scope` and `money_visibility` remain independent axes and are enforced in every list, get, export and printed view. `createRole` over the protocol (`toolCreateRole`) gains the uniqueness check on the machine name that the screen path already has — gate authority resolves by that name.

## C7 · Hard blocks — four of six have no code

Blocks 1, 2, 3 and 4 exist as rows and as helper functions nothing calls; the live labels differ from the six the specification names; the construction spine lacks block **B0 Site Safety Infrastructure**, which block 3 depends on. Change: rename the six rows to the register (mobilisation without insurance certificate · construction without approved Construction Safety and Health Program · first electrical block without B0 signed off · mobilisation without prerequisite permit · issue of quarantined material · fund release, project activation or purchase order without a signed contract); add B0 to the spine and every project; wire each block to its action before any gate on the same action; every attempt — all of which fail — is logged in `hard_block_attempts`; the message names the block, the unmet condition, what releases it and who can supply it, never *you do not have permission*; no `active` column, no enable, disable or delete control on the console; every protocol tool and parameter enumerated with proof that none reaches a block's existence.

## C8 · Two data corrections on the live platform

1. **`markup_major_equipment`** has a version with `effectiveFrom` 1 January 2030 and `effectiveTo` 7 September 2026 — created by the protocol's `update_system_constant` patching a value in place. Fix the tool to call `changeConstant` (versioning) and refuse a version whose `effectiveFrom` is after its `effectiveTo`; correct the row so the current version runs from go-live with no end and 115 as its value, logged.
2. **The four live statutory rate tables are the deliberately fake ones** from the first agent's testing, approved and therefore immutable. Payroll computes against invented brackets. Change: supersede them with the published Social Security System, PhilHealth, Pag-IBIG and withholding tax tables entered by Human Resource with their legal references and approved by Finance under dual control; mark the fake ones `superseded`; refuse approval of any table whose `legal_reference` is empty; never approve test data into a live tenant again.

## C9 · The compliance export

`convex/compliance/compliance.ts` reads each table through its `by_tenant` index and, **when the index does not exist, catches the error and re-reads the table unfiltered, up to 1,000 rows** — fourteen exported tables lack the index, including `audit_entries`, `encryption_keys` and `supplier_bank_accounts`. The export also names 98 tables against a schema of 116: three do not exist and twenty-one real ones are missing, including every operations-and-maintenance table and `payroll_lines`. Change: enumerate tables from the schema, never from a list; read every table through the tenant filter; **delete the unfiltered fallback**; add the missing indexes; the manifest lists every table with its row count; export is logged and respects the exporter's permissions and money visibility.

## C10 · The protocol surface calls the screen's mutations

Tools that reimplemented logic and drifted: `update_system_constant` (patches in place — C8) · `update_document_revision` (takes status as free text and can set a revision in force on an unclassified document without the supersede step) · `create_person_role` (no gate, no duplicate check) · `create_role` (no uniqueness check — C6) · `update_person_role` (accepts `revoked: false`, ignores it, reports success). Change each to a thin adapter over the screen's function. Add the missing tools: `revoke_sign_in`, `correct_sign_in_email` (Part 2), `archive_*` / `restore_*` (Part 1), `list_my_pending_approvals`; and make `list_gates` and `get_gate` return `primaryRoleName`, `primaryPersonId`, `alternateRoleName`, `alternatePersonId` so a gate's configuration can be read from outside. Every decide-scope tool stays propose-then-confirm.

## C11 · Smaller, still real

- **Document reclassification** (controlled ↔ archive) does not exist; gate 33 names an act the platform cannot perform. Build it under gate 33, logged with before and after; a document with an `in_force` revision cannot become archive until that revision is withdrawn.
- **Legal hold** is a free boolean any signed-in person can set or clear. Console holders only, reason required, logged.
- **`revokeRole`** (identity.ts 619) needs no authority. Same authority as assigning; logged with a reason.
- **Progress claim** screen passes a project identifier where a contract identifier is required, so a claim cannot be created from the interface. Key the form to the contract.
- **Purchase order numbers** are counted per project, so two projects in one month both produce `PO-202609-001`. Count per tenant per month.

---

# D. TESTS THAT DECIDE THIS PART

- **G1** Every gate row has a primary; paste `select gateId, primaryRoleName, primaryPersonId, alternateRoleName` for all rows.
- **G2** No approval logic outside `gates.ts`: paste the search for `approvalRef`, `approvedBy =`, `status: "approved"` outside the engine — none.
- **G3** Nothing is auto-approved: every gate sits indefinitely.
- **G4** Alternate with a lower limit — refused at save. A non-console-holder calling `updateGateConfig` — refused. Gate 28 given an alternate — refused.
- **G5** Assign a role: row `pending_approval`, permissions unchanged; approve → `current`; refuse → `refused`; a duplicate → refused; the subject cannot approve their own grant; the message reads as specified.
- **G6** Raising any request notifies the primary (Task) and alternate (Information) in the same mutation; deciding notifies the requester.
- **G7** A third console holder — refused; removing the second without a replacement — refused; a non-holder adding a holder — refused.
- **G8** Erasure without gate 35 — refused; under legal hold — refused; with approval — content unrecoverable, chain verifies, Drive files gone.
- **G9** Trigger each of the six hard blocks by its action — all refuse, all logged, message per the rule; no `active` column; the tool enumeration finds no path to a block's existence.
- **G10** Export: manifest lists every schema table with counts; a tenant-two row appears nowhere; paste the search for the unfiltered fallback — gone.
- **G11** `markup_major_equipment` versions are date-ordered; a version with `effectiveFrom` after `effectiveTo` is refused; the four statutory tables carry legal references and the fake ones read `superseded`.
- **G12** Each protocol tool in C10 refuses exactly what the screen refuses, with the same message.
- **G13** The register script runs clean; every module comment and label for gates 1–34 matches `seed.ts`.

---

# E. REPORT BACK — PASTE THE EVIDENCE

1. The gate table dump (G1) and the register script output (G13).
2. The search output for approval logic outside the engine (G2), and the list of the seventeen call sites now calling the engine, with file and line.
3. One full round trip on gate 11: raise, the two notifications, approve, the requester's notification, the claim's `approvalRequestId`.
4. One gate-24 round trip showing the three states of the `person_roles` row and the refusal of self-approval.
5. `updateGateConfig` refusal for a non-holder; the gate 31 request from a holder's change.
6. The six hard block attempts, logged, with their messages.
7. The erasure refusal without gate 35 and the successful erasure with it, with the chain verification output.
8. The export manifest, and the search output showing the fallback removed.
9. The corrected `markup_major_equipment` rows and the four statutory tables with legal references.
10. Tests G1 to G13 — results pasted. Then, and only then, withdraw pilot ground rules 2 and 3.
