# Code review — root cause of the control-layer failures

**4 September 2026.** First reading of the exported source. This answers the
sizing question: are the control-layer failures one bug or a dozen?

**Neither. They are one architectural fault plus a set of misread rules.** That
distinction changes how Milestone A should be ordered, and it means fixing the
protocol alone would fix nothing.

---

## 1. The export is complete

Two different artefacts, both whole.

| File | Size | What it is |
|---|---|---|
| `app.tar.gz` | 736 KB compressed, 4.2 MB extracted, 280 files | **The source code** — `convex/` backend and `src/` frontend |
| `snapshot_...zip` | 175 KB, 236 files | **A data export** — one `documents.jsonl` and `generated_schema.jsonl` per table, 116 tables |

Verification of the source:

- **All 400 live tools are defined in it.** I extracted every tool name from
  `convex/mcp/*.ts` and compared against `tools/list` on the deployment: 400 of
  400 matched, none missing.
- **No truncation.** Every large file terminates on valid syntax;
  `handler.ts` ends with an explicit end-of-file marker.
- 93 backend TypeScript files across 25 modules, 159 frontend files.
- `node_modules` and `.git` excluded, which is correct and expected.

Two things the spec demands are correctly observed and worth saying:
**no scheduler anywhere** — no `ctx.scheduler`, no `runAfter`, no `runAt`, no
`crons` file, exactly as section 2.4 requires — and the section 2.6 enforcement
tests exist (`convex-enforcement.test.ts`,
`communication-enforcement.test.ts`). The tenant wrapper is used consistently.

---

## 2. Root cause one — two write paths that share no code

The protocol layer does not call the application. It reimplements it.

```
convex/mcp/*.ts imports:
  internalMutation, internalQuery   (Convex)
  v, ConvexError                    (Convex)
  Doc, Id                           (generated types)
  createTenantDb, createTenantQueryDb
  appendAuditEntry
```

**That is the entire import list. Nothing from `finance/`, `procurement/`,
`foundation/`, or any other domain module.** Across the protocol layer there are
**178 direct `db.insert` and `db.patch` calls** — every write reimplemented
inline rather than delegated.

So any rule enforced in a domain mutation is absent from the protocol path *by
construction*, not by oversight. This is why all three of my test calls
succeeded: the protocol never reaches the code that would have refused them.

It also means every fix has to be written twice, and the two paths will drift
apart on the next change.

## 3. Root cause two — where the rules exist, they are the wrong rules

This is the finding that matters more, because it rules out the easy diagnosis.
The browser path is **not** correct-but-bypassed. It carries the same defects,
written independently.

### The gate is derived from severity in both paths

`convex/finance/finance.ts` line 12:

```ts
function gateIdForSeverity(severity: "minor" | "moderate" | "major"): string {
  if (severity === "minor") return "1";
  if (severity === "moderate") return "2";
  return "3";
}
```

`convex/mcp/group3bInternals.ts`, inside `toolCreateWriteOff`:

```ts
// Derive gateId from severity
const severityToGate: Record<string, string> = { minor: "1", moderate: "2", major: "3" };
const gateId = severityToGate[args.severity] ?? "1";
```

The same defect, twice, in two files, by two different mechanisms. **`amount` is
stored and never consulted** in either. Section 6 sets gate 1 at up to ₱50,000,
gate 2 at ₱50,001 to ₱100,000 and gate 3 above ₱100,000 — Chief Executive
Officer, no alternate. The thresholds appear nowhere in the codebase; a search
for `50000` and `100000` across finance and foundation returns nothing.

Neither path raises an approval request. Both set `status: "pending_approval"`
and stop.

### Hard block 6 is implemented as a different rule entirely

`convex/procurement/orders.ts` does check something, in `issuePurchaseOrder`:

```ts
// Hard block 6 — must have Gate 4 approval
if (!po.gate4ApprovalId) {
  ... actionType: "hard_block.attempt" ...
  throw new ConvexError({ code: "FORBIDDEN",
    message: "Hard block 6: A purchase order cannot be issued without Gate 4 ... approval." });
}
```

Three things are wrong. Section 5 hard block 6 releases on **the signed contract
document**, not on a gate 4 approval — the code has substituted an internal
approval for a client commitment. It sits on `issuePurchaseOrder`, so **creating**
a purchase order is unblocked. And the protocol's `toolCreatePurchaseOrder` has
no check at all, which is why my ₱500,000 order went through against a project
with no signed contract.

`convex/foundation/hardBlocks.ts` exists and does real work — it queries the
table, logs attempts, patches configurable values. **The protocol layer never
imports it.**

---

## 4. What this means for Milestone A

Not twelve independent bugs. Not one. **One mechanical convergence plus a
bounded set of rule corrections** — and the order is the important part.

**Wrong order:** fix the protocol tools. They would then correctly enforce rules
that are themselves wrong, and the work is thrown away.

**Right order:**

1. **Correct the rules in the domain layer.** Gate derived from amount with the
   section 6 thresholds. Approval requests raised inside the gated mutation, with
   the approver role resolved. The six hard blocks reseeded and enforced as
   specified, on create as well as issue. Roles consulted for record scope and
   money visibility. This is real design work but it is bounded — the rules are
   fully written down in sections 5 and 6.

2. **Then converge the protocol onto it.** Replace the 178 direct writes with
   calls to the domain mutations. Largely mechanical, and it is what stops this
   recurring: after it, a rule fixed once is fixed on both paths.

Step 2 is the structural fix. Without it, every item on the 27-item list gets
implemented twice for the rest of the platform's life, and the two copies drift
— which is exactly how the platform arrived here.

## 5. Revised reading of the 27-item list

- **Items 1 to 12 (control layer)** — these are step 1. They are domain-layer
  work, not protocol work. The protocol symptoms I reported are downstream.
- **Item 19 (undeclared enums)** — genuinely protocol-only, independent, cheap.
- **Everything else** — largely unchanged, but each should be fixed in the domain
  and inherited by the protocol, not written twice.

I would add one item to the list: **the protocol layer must not write to tables
directly.** Section 2.6 already fails the build for `ctx.db` outside the tenant
wrapper. The same technique applies here — fail the build on a `db.insert` inside
`convex/mcp/` — which makes the convergence permanent instead of a one-off tidy.
