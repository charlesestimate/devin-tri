# Monday — twelve changes, then publish. Sixty-three people arrive Tuesday.

Two automated testers swept the live platform on Saturday and raised 74 findings. This prompt
contains **only the twelve that must be true before sixty-three employees start using it**.
Everything else is deliberately held.

I have verified every line reference below against the current source. **Build all twelve. Do
not redesign anything. Do not fix anything not listed here. Do not reply with a plan — build it,
publish it, and report against section 13.**

Order matters: Part A protects money, Part B is four small repairs, Part C lets the test data be
removed before anyone sees it, and Part D bounds what the assistant may do.

---

# PART A — the control layer

## 1. Record self-approval. Do not block it — yet.

`convex/inventory/inventory.ts:432` is the only place in the codebase that checks whether the
approver is the person who raised the record:

```ts
if (adj.createdByPersonId === tc.personId)
  throw new ConvexError({ code: "FORBIDDEN",
    message: "You cannot approve your own adjustment (Gate 26)" });
```

Every other approval mutation was written without it. On Saturday a tester raised and approved
**fourteen** records unopposed — a ₱9,482,000 purchase order, a ₱99,000,000 billing milestone, a
₱5,000,000 fund request and a ₱5,000,000 write-off among them.

**The company has decided that blocking self-approval is not right for this stage.** Build the
mechanism and ship it in the permissive position, so it can be turned on later without another
round of work.

### What to change

**1a. Mark it, everywhere.** In each approval mutation, compare the approver against the person who
raised the record. When they are the same, set `selfApproved: true` on the approval and record the
same fact in the audit entry. **Refuse nothing.** Nobody is blocked and nobody sees a new dialog.

**1b. One shared helper**, `checkSelfApproval(raiserPersonId, approverPersonId)`, called from every
approval mutation. These are the sixteen:

```
design/packages.ts        approveDesignFreeze
finance/finance.ts        certifyBillingMilestone, certifyProgressClaim,
                          approveFundRequest, approveWriteOff
payroll/payroll.ts        approveRateTable, approvePeriod
pipeline/proposals.ts     approveInternalReview, approveWon
construction/reports.ts   approveSiteReport
inventory/inventory.ts    approveAdjustment            (already blocks — leave it blocking)
om/om.ts                  approveVisitSignOff
foundation/gates.ts       approveRequest
```
Plus the purchase order approval and issue path in `procurement/`, and the document revision
publish path in `documents/`. **Enumerate them yourself and report the full list.**

**1c. The switch.** One row in `configuration_values`, which already exists with a `by_tenant_key`
index:

```
key:   "self_approval_mode"
value: "record"              "record" or "block"
```

While it reads `record`, the helper only marks. When a console holder changes it to `block`, the
same helper refuses, with the message *"You raised this request, so you cannot approve it. It needs
a second person."* **Ship it set to `record`.** Changing it is a console-holder action on
Administration and is itself audited.

**1d. Make it countable.** A record approved by the person who raised it shows a quiet marker on
screen; the Board Pack carries a tile counting them; the Exception Report lists each one with who,
what and when. This costs nobody any time and it means the history is complete rather than silent.

**1e. The helper lives in the domain layer, not in the screen.** `convex/mcp/` reimplements writes
inline rather than calling the domain modules, so a check added only to a page will not bind the
protocol. Put it where both paths pass through it.

**1f. An agent session is an actor like any other** and is marked the same way. When the mode is
later set to `block`, it is bound like anyone else.

## 2. Stop presenting the approval gate as a choice

`convex/finance/finance.ts:12`:

```ts
function gateIdForSeverity(severity: "minor" | "moderate" | "major"): string {
  if (severity === "minor") return "1";
  if (severity === "moderate") return "2";
  return "3";
}
```

The write-off severity dropdown carries the gate in its own option labels — *"Minor (Gate 1)"*,
*"Moderate (Gate 2)"*, *"Major (Gate 3)"* — so the person raising the record picks the gate before
typing an amount. Tested Saturday: **₱50,000 and ₱5,000,000 both raised Gate 1** when the severity
matched. The amount changed nothing.

### What to change

**2a. Derive the gate from the amount.** Use the money-authority thresholds already stored on the
gate rows seeded by `convex/foundation/seed.ts`. Severity stays as a description of the event; it
must no longer select a gate.

**2b.** Remove the gate numbers from every severity option label.

**2c.** Show the derived gate read-only on the form, so the person can see what their amount
requires before they submit.

**2d.** The same function is written a second time, independently, in
`convex/mcp/group3bInternals.ts`. **Fix the domain rule first, then make the protocol layer call
it** — do not leave two copies.

## 3. Five validations that let impossible things through on Saturday

Each of these was accepted by the live platform. Fix these five only.

| Field | What was accepted | Rule to apply |
| --- | --- | --- |
| Project → Attach Signed Contract → Date Signed | **31 Dec 2027**, which then unlocked the project's hardest gate | Not in the future |
| Payroll → Adjust → Adjusted Days Worked | **999** in a fifteen-day period | Not more than the days in the period |
| Finance → Add Milestone → Billing Amount | Milestones totalling **622%** of contract value | Warn above 100% of contract, refuse above a threshold you choose |
| Pipeline → Add Site → area and voltage | **−5,000 m²** and **−13.8 kV** | `min="0"`, as the bill-of-materials and activity forms already do correctly |
| Inventory → Transfer → Dispatch and Receive | 25 units moved out of a location holding **zero**; **30** received against 25 dispatched | Refuse a dispatch above stock on hand; cap a receipt at the quantity dispatched |

**3a.** Also: a form that refuses must say which field refused it. Several today return nothing at
all — the dialog stays open and the button appears dead.

---

# PART B — four small repairs

## 4. The progress claim failure is one line

Both testers failed to create a progress claim — nine attempts, three payloads, two projects,
every one returning only `"Failed to create"`.

`src/pages/finance/_components/ProgressClaimsTab.tsx:60`:

```ts
contractId: projectId as unknown as Id<"contracts">,
```

**The client sends the project's identifier where the contract's identifier is required**, cast
twice so TypeScript cannot object. Convex rejects it at the argument boundary; because that is not
a `ConvexError`, the catch at line 72 falls through to its generic string — which is why no reason
ever reached the user.

**4a.** Resolve the project's actual contract and pass it. The dialog has no contract picker; add
one, or look it up.
**4b.** Delete the cast.
**4c.** The Finance header tiles read only from progress claims, which is why they showed
**"Total Claimed PHP 0"** while ₱99,000,000 sat certified on the row below. Make them read
milestones as well.

## 5. Dates default to the Coordinated Universal Time clock

Measured Saturday, browser confirmed in Asia/Manila:

| Field | Philippine time | Defaulted to |
| --- | --- | --- |
| Record Professional Seal → Sealed At | 11:10 | `2026-09-05T03:09` |
| Record Delivery → Received At | 11:22 | `2026-09-05T03:22` |

Eight hours behind. **Between midnight and 07:59 Philippine time the defaulted date is yesterday** —
which is when site crews raise permits. A goods receipt taken at 11:22 is on record as 03:22.

**5a.** The fault is confined to **client-defaulted `datetime-local` values** — `toISOString()` is
being sliced instead of a local datetime string being built. Plain date defaults and every
server-set timestamp are already correct; do not touch those.
**5b.** One shared helper, used for every `datetime-local` default in the product.

## 6. There is no error boundary anywhere in the application

I searched `src/` for `ErrorBoundary`, `componentDidCatch` and `errorElement`. **Zero matches.**
One failing query can therefore take down the sidebar, the header and every control at once, and
the only way out is a browser reload.

**6a.** One boundary at the route level, one per tab panel, showing what failed and offering a way
back without reloading.
**6b.** Sixty-three people start on Tuesday. This is the difference between one person reporting a
broken panel and sixty-three reporting that the platform is down.

## 7. Two one-word fixes

**7a. A safety stop cannot be raised without a project.** `convex/safety/safety.ts:192` declares
`projectId: v.id("projects")` as required. Incidents (line 39) and near misses (line 160) correctly
use `v.optional`. Make the safety stop match. It is the one control that exists for an emergency and
a person stopping work must never be blocked by a dropdown.

**7b. Video attachments.** `src/pages/messages/_components/ThreadPanel.tsx:742` and
`ChannelPanel.tsx:743` both read:

```
accept="image/*,application/pdf,.doc,.docx,.xls,.xlsx,.csv,.txt"
```

Add `video/*` to both. **There is no file size limit anywhere in the client** — add one in the same
change (25 MB is a reasonable starting point) and tell the user when a file exceeds it, because a
phone video from a site is far larger than anything the product handles today.

---

# PART C — so the test data can be removed before Tuesday

## 8. A way to delete the test records

Two testers created **87 records across 45 tables** on the live platform, every one carrying `Z1-`
or `Z2-` in its name, description or notes. Most cannot be deleted through the interface at all —
locations, catalogue items, permit types, equipment and workforce records have no delete control.

`Clear All Test Data` is **not** the answer: it deletes `persons` and `person_roles`, which would
destroy all sixty-three onboarded staff and every role assignment, while leaving `channels` and
`channel_members` pointing at deleted people.

**8a.** Add one operation to **Migration and Cutover**: *"Delete records by name prefix"*. It takes
a prefix, **lists what it would delete first and requires confirmation**, then deletes.
**8b.** It must never touch `persons`, `person_roles`, `users`, `audit_entries`, gates, roles,
hard blocks or system constants.
**8c.** Audit entries are preserved by design. Do not change that — the test history staying in the
chain is correct.

## 9. The screen must show what the write actually did

Every state transition on a purchase order produced a correct success toast while the badge and the
buttons kept the old state. Four transitions needed four full page reloads to see the truth.

**The consequence is not cosmetic: the Approve button stays on screen after a successful approval,
inviting a second press on a ₱9,482,000 order.** The same happens on design package status, and the
physical count list renders **completely empty** after a submit until the page is reloaded.

**9a.** Re-read after every mutation that changes a status, so the badge and the available actions
reflect the new state without a reload.
**9b.** Disable the button while its mutation is in flight.

## 10. Remember the selected project

Every reload and every navigation resets the header to "Select project…", and the URL never changes
from `/procurement`. Nothing can be bookmarked, shared in a message, or reopened. Combined with
item 9, checking a status costs three clicks of re-navigation.

**10a.** Put the project in the URL. **10b.** Remember the last project per person across modules.

## 11. The landing page says twenty-nine gates. There are thirty.

`src/pages/Index.tsx:12` contains a hardcoded string: `"29 configured gates, full audit trail"`. It
is not a live count. `convex/foundation/seed.ts` says *"Exact 30 rows per F3.1"* and
`convex/foundation/tenants.ts:117` treats a tenant as configured at `gateCount >= 30`.

Fix the number. The same three lines also ship **"EPC"** and **"PTWs"** on the front page of a
platform whose specification forbids abbreviations — write them out. Change nothing else on
that page.

---

---

# PART D — what the protocol may see and do

## 12. The assistant's boundary

The Chief Executive Officer works with an assistant that operates this platform over the protocol
endpoint. It must be able to report on the state of these controls and carry out changes he has
approved.

**12a. Readable over the protocol:** the value of `self_approval_mode`; how many self-approvals have
been recorded, by whom, and on what; which records are awaiting approval and who is being waited on.

**12b. Writable only under the short-lived `decide` scope:** changing `self_approval_mode`. Every
such change is audited with the session identifier that made it.

**12c. Never available over the protocol, under any scope:** approving a statutory rate table
(Gate 32), and approving or disbursing a payroll period (Gate 30). Those two reach a real person's
pay and need a human at the keyboard.

# 13. What to report back

Do not report that these are done. Report each with its proof.

1. **Self-approval.** List every approval mutation you found and confirm the helper is called from
   each. Then raise a write-off and approve it yourself: confirm it **succeeds**, is marked, and
   appears on the Board Pack tile and in the Exception Report.
2. **The switch.** Set `self_approval_mode` to `block`, repeat the same test, paste the refusal,
   then set it back to `record` and confirm it succeeds again. Ship it on `record`.
3. **Gate from amount.** Raise four write-offs — ₱50,000 and ₱5,000,000, each at minor and major
   severity — and give me the four gates as a table. Confirm the two copies of the rule now agree.
4. **Validation.** Try all five impossible values in the table at item 3 and paste each refusal.
5. **Progress claim.** Create one, then say what the Total Claimed tile reads.
6. **Dates.** State the Philippine time, then open Record Delivery and say what Received At holds.
7. **Error boundary.** Force a query to throw on one tab; confirm the sidebar and other tabs live.
8. **Safety stop.** Raise one with no project.
9. **Video.** Attach a video to a message, and attach one over the size limit.
10. **Prefix delete.** Run it in preview mode for `Z1-` and paste the list it says it would delete.
    Do not run it for real — the Chief Executive Officer will.
11. **Gates.** Say what the landing page reads now.
12. **Protocol.** Confirm `self_approval_mode` is readable over the protocol, changeable only under
    the `decide` scope, and that rate table and payroll approval are unreachable over it entirely.

If any item cannot be built as written, say which and why **before** publishing the rest. Do not
substitute a different fix without saying so.
