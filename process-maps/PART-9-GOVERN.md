# Part 9 of 10 — Govern

**Level-1 cross-functional map · as specified · 8 September 2026**
**Companion files:** `Part 9 — Govern (A3 landscape).pdf` and `.svg` in the same folder

---

## 1. What this process is for

Parts 2 to 8 mapped what the company does. This part maps **who is allowed to change the
rules those parts run on**, and how anyone would later prove what was changed and by whom.

Four chains. **Stand the console up** creates the two people who hold the keys. **Configure**
changes the numbers and the approvers — thresholds, system constants, gate assignments.
**Grant authority** decides who holds which role and what a role may do. **Prove it** is the
audit chain, the export and the erasure.

**Starts:** the first sign-in, before any project exists. **Ends:** an export that a regulator,
an auditor or a buyer could read.

This is the part where the platform's own safeguards are the subject rather than the tool, and
it produced the sharpest single finding of the series.

---

## 2. The finding

**Fifty-six role grants are live in the company. Exactly one carries a gate 24 approval, and
that one was raised and approved by the same person.**

I counted this on the live platform this afternoon, person by person: 56 rows in
`person_roles`, 2 revoked, and one single row carrying a `gateRequestId`. That request
(`j971ag7x740fhjej2f57wp4hr18dpbfa`) has `requestedBy` and `decidedBy` set to the same
person — you — with timestamps exactly one minute apart on the round minute, which is the
signature of a row written directly rather than one produced by an approval screen.

Six of the fifty-five ungated grants I made myself, an hour before writing this, when I added
the Design and Permitting teams. The tool let me. It asked nothing.

That is not a criticism of the tool call. It is the point of the part: **the platform's
authority model is currently a convention, not a control.** Everyone has behaved well, so
nothing has gone wrong. Nothing in the code would have stopped it if someone had not.

---

## 3. Lanes in this map

| Lane | Who | Why it is here |
| --- | --- | --- |
| Console Holders | The two key-holders | The only bypass the platform admits to in writing |
| Executive | Chief Executive Officer, Chief Operating Officer | Named on gates 22, 31 and 32 |
| Department Heads | Directors, Head of Finance | Named on gate 24 |
| Document Control | Document Controller | Named on gate 33 |
| Model Context Protocol | The second door | Governance is where the two doors differ most |
| The Platform | Derived and automatic | Seeding, the audit chain, the sidebar |

The Model Context Protocol earns a lane of its own in this part and no other. Everywhere else
it is a convenience. Here it is a second writer to the same tables with different rules, and
in three places the difference is destructive.

---

## 4. Standing the console up

The platform admits exactly two console holders. `addConsoleHolder` refuses a third, and
`removeConsoleHolder` refuses to remove the last one. Both refusals are correct and both are
written plainly.

Neither mutation checks that the caller is a console holder.

While fewer than two holders exist, any signed-in person can add themselves. A console holder
may then use `directAssignRole`, which is the one honest bypass in the platform: it is
console-holder only, and its audit entry records `bypassedGate: "24"` in as many words. So the
escalation path is short and it is not hypothetical — it is: add yourself as the second holder,
then grant yourself any role including Chief Executive Officer.

The live rows show the mechanism half-built. There are two holders, both added by the same
person. The first carries `holderRank: "second"` — the bootstrap sets that literal on the
first holder — and the second carries no rank at all. Gate 32's specification reads *"first
console holder only"*. **Against this data there is no first console holder.** The rule cannot
be evaluated even in principle.

---

## 5. Configuring

### The five governing gates have no approver

| Gate | `seed.ts` says | The live row says | Primary approver | Alternate |
| --- | --- | --- | --- | --- |
| 22 | System Constant Change | System Constant Change | **none** | none |
| 24 | Role Assignment | **Employment Offer** | **none** | none |
| 31 | Threshold and Configuration Change | Threshold Configuration | **none** | none |
| 32 | Role Permission Change | **Access Review** | **none** | none |
| 33 | Document Classification | Document Classification | **none** | none |

Every one of the five has `primaryRoleName` and `primaryPersonId` empty. The roles they name —
Chief Executive Officer, Chief Operating Officer, Director, Head of Finance, Document
Controller — all exist, are active, and are marked as approvers. **This is unconfigured, not
unconfigurable.** It is an afternoon's work on the Administration screen.

It has one immediate consequence. `assignRole` refuses to run when gate 24 has no primary
approver, with the message *"Gate 24 (Role Assignment) has no primary approver assigned.
Contact an administrator."* **Role assignment through the Administration screen cannot succeed
today.** That is why every grant in section 2 arrived by tool call or direct assignment: the
front door is bolted and the side door is open.

Gate 24 also carries the register problem from Part 5 in its purest form. `seed.ts` calls it
Role Assignment; the live row calls it Employment Offer; the human resources module uses it for
offers and the identity module uses it for role grants. An approver opening that request sees
"Employment Offer" and is in fact approving a grant of authority.

Gate 32 has three claimants: `seed.ts` calls it Role Permission Change, `compliance.ts` calls
it Access Review, and `identity.ts` uses it for permission upserts. The live row sides with
compliance.

### Changing a gate is itself ungated

`updateGateConfig` takes no approval reference at all — there is no argument for one. It
enforces one rule correctly (a no-alternate gate can never be given an alternate, F3.6) and
nothing else.

It can change the approver on **gate 31 itself**. The guard can move its own guard, in one
call, with no second signature.

### The system constants

`changeConstant` does the right thing structurally: it closes the open version by setting
`effectiveTo`, then inserts a new row. The timeline is preserved rather than overwritten.

Its `approvalRequestId` is an **optional** argument, stored into `changedByGate` without being
looked up, without being checked for approval, and without being checked to be a gate 22
request at all. The comment above it says *"requires gate 22 approval"*. It does not.

Live: nine constant rows, four keys, six changes made — and `changedByGate` is empty on every
single row. Gate 22 has never fired.

### The second writer has already done damage

`update_system_constant`, over the Model Context Protocol, patches `numericValue` **in place**.
It does not close a version and open a new one. It rewrites what a constant used to be.

The result is visible in the live data:

| Key | From | To | Value |
| --- | --- | --- | --- |
| markup_major_equipment | 2026-09-03 | 2030-01-01 | 115 |
| markup_major_equipment | **2030-01-01** | **2026-09-07** | 116 |
| markup_major_equipment | 2026-09-07 | open | 120 |

The middle row begins three years and four months after it ends. Two consequences follow
mechanically from `getConstantAtDate`, which filters on `effectiveFrom <= date` and takes the
last:

- **Today**, the 115 row claims to be in force until 2030 while the lookup returns 120 from
  7 September. The stored window is a lie; the answer happens to be right.
- **From 1 January 2030**, the lookup selects the 116 row, sees its `effectiveTo` has already
  passed, and **throws** rather than returning a number. A pricing constant with a fixed future
  failure date.

Nothing in this is exotic. Two writers were given the same table and different ideas about what
"change" means.

---

## 6. Granting authority

### The role goes live before the gate is answered

`assignRole` raises a real gate 24 request — one of the few places in the platform that builds
one properly, copying the approver role off the gate row. In the same transaction it inserts
the `person_roles` row with `revoked: false`.

The comment calls this "a pending state". Nothing anywhere treats it as one. Every consumer —
the sidebar, the person list, and `checkGateAuthorisation` in the gate engine itself — filters
on `revoked`, never on whether the governing request was approved. And no code path revokes the
row if the request is refused. A refused gate 24 leaves the role in place for ever.

This composes into something worse. Because the role is live immediately, and because R6 refuses
**the requester**, not the subject:

**A assigns B the Chief Operating Officer role. B holds it from that instant. B is now
authorised on every gate whose primary is Chief Operating Officer — including gate 24. B
approves the request that granted B the role.**

R6 is never touched. It is working exactly as written. The hole is that the grant is effective
before the decision.

### Removing authority needs nothing at all

`revokeRole` takes a person-role id and an optional reason. No gate, no role check, no
console holder. Granting authority raises a request that nobody answers; taking it away raises
nothing. If a hostile actor ever reached the platform, revoking the Chief Operating Officer's
roles would be the first thing available to them and the cheapest.

### The second door again

`create_person_role` over the Model Context Protocol raises no gate, checks no duplicate and
checks no console holder. `create_role` has no uniqueness check on the machine name, while the
screen path `createRole` does — and gate authorisation resolves by machine name. A duplicate
`chief_operating_officer` role would confer every Chief Operating Officer gate on whoever holds
it. Worse, the screen path reads that name with `.unique()`, so once a duplicate exists the
Administration screen throws on that role permanently.

`update_person_role` accepts `revoked: false` and silently ignores it — only `true` is acted on.
It returns "updated" either way.

### Permissions decide the menu and nothing else

`setRolePermission` carries its own confession in the comment above it: *"Requires gate 32
approval — but for now records it directly and logs it. Full gate enforcement will be layered
in Milestone 1 conformance fix."* Gate 32 is a to-do note.

That matters less than it looks, because the `permissions` table has exactly one consumer in
the entire product: `getMyVisibleObjectTypes`, the query behind the navigation sidebar. **No
mutation anywhere asks whether the caller holds a permission before writing.** Permissions
paint the menu. They do not restrain anyone.

There is also a duplicate register underneath: `roles` carries `recordScope` and
`moneyVisibility`, and every `permissions` row carries its own. Two places hold the same fact
and no code reconciles them.

---

## 7. Documents

Document control is the best-built module in this part and it is governed by the weakest gate.

**Gate 33 is named for an act the platform cannot perform.** The register calls it Document
Classification — *"classify or reclassify a document"*. `documentClass` is set at
`createDocument` and there is no reclassification path anywhere: not in the module, not on the
screen, not in the tool surface. `update_document` takes title, status, legal hold and tags,
and not the class. A document filed under the wrong class is filed under the wrong class for
ever, and each revision snapshots that class as it is published.

The one thing gate 33 does enforce is the precondition: an `unclassified` document cannot be
published in force. That is hard block 4 and it works. The *approval* half has no code at all —
`publishRevision` has no gate, no approver check and no self-approval refusal.

`publishRevision` is otherwise careful: it supersedes the current in-force revision, sets
`in_force_to`, links the supersession and moves the document pointer, all in one transaction.
Its `in_force_from` is a free argument, so a revision can be recorded as having been in force
before it existed, and the superseded revision's end date moves with it.

Three more, briefly:

- **Legal hold is a free boolean.** It is the strongest control in the module — it blocks new
  revisions, blocks voiding, blocks the retention timer — and any signed-in person can set it
  and any signed-in person can clear it, with no reason recorded and no gate.
- **`update_document_revision` takes `status` as free text** over the Model Context Protocol.
  A revision can be set to `in_force` without the unclassified refusal and without superseding
  the current one. Two in-force revisions then break `publishRevision` for that document
  permanently, because it reads the current one with `.unique()`.
- **`doc_requirements.requiredByGateId` is a number.** Gates 25a and 25b are strings. Those two
  gates can never be expressed as a document requirement.

---

## 8. Proving it

Two things in this part are completely right, and they are the two that matter most to an
auditor.

**The audit chain.** Every write appends a hash-linked, sequence-numbered entry, and
`verifyAuditChain` walks it, recomputes each hash over a canonical ordering of the same fields,
and reports the first sequence at which it breaks. It is on the Administration screen. It works.
It is the second piece of the platform, after the gate engine, that is finished and correct.

**The attested export.** Initiated by a person and attested by a person, with no scheduler
anywhere — exactly as the locked principles require. The shape of it is right, and it is the
nearest thing to a complete picture of the company that anyone can hold.

It is not, however, complete, and it has a flaw that will matter the day a second tenant
exists. The schema defines 116 tables. The export names 98. Three of those 98 are not tables
at all — `payroll_workers`, `payroll_rate_tables` and `payroll_disbursements` do not exist —
and the loop's `catch` quietly reports them as empty rather than failing. **Twenty-one real
tables are missing**, among them every operations-and-maintenance table (visits, readings,
defects, schedules), `payroll_lines` — the actual pay amounts — the statutory rate tables,
`identity_links`, `files`, `configuration_values`, and the whole of internal messaging.

The flaw is in the fallback. Each table is read through its `by_tenant` index; if that index
does not exist the code catches the error and re-reads the table **unfiltered**, taking up to
1,000 rows. Fourteen of the exported tables have no `by_tenant` index, and they include
`audit_entries`, `encryption_keys` and `supplier_bank_accounts`. On a single-tenant deployment
this is invisible and harmless. On the day a second tenant is created, the compliance export —
the artefact whose entire purpose is to be handed to an outsider — begins including another
company's audit chain, key rows and supplier bank details.

Each table is also capped at 10,000 rows with no flag to say it was truncated. `audit_entries`
will pass that line first, and when it does the export will silently stop being the record it
claims to be.

And then there is the one that is not right at all.

### Cryptographic erasure

`performErasure` destroys a person's encryption key permanently. Their audit entries become
unreadable for ever. It is the only genuinely irreversible operation in the platform.

It requires: a reason string that is not blank.

No gate — no gate in the register covers it. No role check. No console-holder check. No second
signature. Any signed-in person can erase any other person, including a console holder, and the
audit entry recording that they did so is written into a chain that the erasure has just made
partly unreadable.

This is the item from Part 9 that should not wait for Monday.

---

## 9. The RACI

| Step | Console Holder | CEO | COO | Director | Doc Controller | Everyone signed in |
| --- | --- | --- | --- | --- | --- | --- |
| 9.1 First console holder | **R / A** | **I** | I | | | |
| 9.2 Second console holder | **A** | **C** | **C** | I | | **R today** |
| 9.3 Gate rows seeded | **I** | I | I | | | |
| 9.4 Configure a gate (G31) | **C** | **C** | **R / A** | I | I | **R today** |
| 9.5 Gates unconfigured | I | **I** | **I** | I | I | |
| 9.6 Change a constant (G22) | I | I | **R / A** | **C** | | **R today** |
| 9.7 Constant by tool call | I | I | **I** | | | **R** |
| 9.8 The timeline | | | **I** | | | |
| 9.9 Assign a role (G24) | C | I | **A** | **R** | | **R today** |
| 9.10 Screen path refuses | I | I | **I** | **I** | | |
| 9.11 Role by tool call | **I** | I | **I** | I | | **R** |
| 9.12 Direct assignment | **R / A** | I | I | I | | |
| 9.13 Change permissions (G32) | **C** | **R / A** | **C** | I | | **R today** |
| 9.14 Sidebar painted | | | I | | | **I** |
| 9.15 Classify a document (G33) | | | I | C | **R / A** | **R today** |
| 9.16 Publish a revision | | | I | C | **A** | **R today** |
| 9.17 Revision by tool call | | | I | | **I** | **R** |
| 9.18 Legal hold | | **C** | **C** | I | **A** | **R today** |
| 9.19 Audit chain | **I** | **I** | **I** | I | I | |
| 9.20 Cryptographic erasure | **C** | **A** | **C** | I | | **R today** |
| 9.21 Export and attest | **R** | **A** | **C** | I | I | **R today** |

**Reading the matrix.** The right-hand column is the finding. On nine of the twenty-one steps,
the person who is Responsible in the live build is *anyone with a sign-in* — and on seven of
those nine, the specification names a specific officer. The gap between column six and columns two
to five is the whole of Part 9.

The Chief Executive Officer appears as Accountable exactly twice, on permissions and on
erasure, and holds neither control today.

---

## 10. Hand-offs

| From → To | At step | What crosses | What stalls it |
| --- | --- | --- | --- |
| Console → Executive | 9.2 → 9.4 | The right to configure | Nothing checks it |
| **Executive → every other part** | **9.4 → all** | **Who approves what** | **Nothing. One call, no signature** |
| Executive → Finance and Sales | 9.6 → Parts 2, 4, 6 | Markups, yields, rates | Already inconsistent — see section 5 |
| **Department Head → the gate engine** | **9.9 → all** | **A person's authority** | **The grant is live before the answer** |
| Executive → the sidebar | 9.13 → 9.14 | What a role may see | Nothing else consumes it |
| Document Control → Site | 9.16 → Part 5 | A revision in force | Correct, and ungated |
| Platform → the auditor | 9.19 → 9.21 | The proof | Erasure can quietly remove part of it, and the export omits 21 tables |

---

## 11. Where the live build differs from this map

| # | The map says | The live build | Severity |
| --- | --- | --- | --- |
| G-1 | Erasure is authorised | Reason string only; no gate, no role, irreversible | **Highest** |
| G-2 | Gates 22, 24, 31, 32, 33 have approvers | All five empty | **Highest** |
| G-3 | A role takes effect when gate 24 is approved | Live on insert; refusal never revokes | **Highest** |
| G-4 | Role assignment works on the screen | Refuses — gate 24 has no primary | High |
| G-5 | Constant changes carry a gate reference | Six changes, zero references | High |
| G-6 | One writer per table | Tool calls overwrite constant history; one key is already incoherent | High |
| G-7 | Gate config is approved | `updateGateConfig` takes no approval argument and can rewrite gate 31 | High |
| G-8 | Console holders are added by console holders | Neither add nor remove checks the caller | High |
| G-9 | Gate 32 governs permissions | Comment admits no enforcement; permissions only paint the sidebar | Medium |
| G-10 | Gate 33 governs reclassification | No reclassification path exists | Medium |
| G-11 | Legal hold is controlled | Free boolean, either direction, no reason | Medium |
| G-12 | Revisions become in force through publish | Tool call sets the status directly and can break the document | Medium |
| G-13 | Removing a role is governed | `revokeRole` needs nothing | Medium |
| G-14 | A gate has one meaning | Gate 24 has two, gate 32 has three | Medium |
| G-15 | There is a first console holder | One row says "second", the other says nothing | Low |
| G-16 | Document requirements can name any gate | `requiredByGateId` is a number; 25a and 25b cannot be expressed | Low |
| G-17 | The export is the complete record | 98 of 116 tables, three of them phantom; every O&M table and `payroll_lines` missing | High |
| G-18 | The export is tenant-scoped | 14 tables fall back to an unfiltered read — including `audit_entries`, `encryption_keys`, `supplier_bank_accounts` | **Highest on a second tenant** |

Eighteen items. Three of them — G-1, G-2 and G-18 — are worth more than the other fifteen
together. G-2 is an afternoon on a screen that already exists. G-18 costs nothing today and
costs everything on the day the platform serves a second company.

---

## 12. What this changes about Monday

Part 8 reduced twelve reported defects to one instruction: *route every approval through
`foundation/gates.ts`*. Part 9 adds four more, and three of them are smaller than they look.

1. **Configure the five governing gates.** No code. The screen exists, the roles exist. This
   alone turns G-2, G-4 and half of G-3 from findings into settings.
2. **Make the grant follow the decision, not precede it.** One filter — a role is effective when
   it has no governing request, or its governing request is approved — applied in
   `checkGateAuthorisation` and in the two queries that list a person's roles.
3. **Put a gate on erasure**, or until then, remove the button. It is the one thing here that
   cannot be undone.
4. **Delete the unfiltered fallback in the export.** Add the missing `by_tenant` indexes and let
   the read fail loudly rather than succeed across tenants. Four lines, and it stops being a
   data-protection incident waiting for a second customer.

The Model Context Protocol findings (G-6, G-12) are a different shape and belong in a separate
instruction: the tool surface should call the same mutations the screens call, not reimplement
them. That is the theme of Part 10.

---

## 13. What is deliberately not in this part

Money thresholds and amount bands are gate 31's subject in name, but they live in the gate rows
and in code constants, not in `configuration_values` — which holds two sequence counters and
nothing else. Mapping where each threshold actually lives belongs with the consolidated register
in Part 10, not here.

Tenant setup, the retention policy and the backup log are governance too. They are single-screen
records with no cross-lane flow, and a swimlane map would flatter them.

---

**Next: Part 10 — the consolidated RACI and the gate register, as a Google Sheet.**
