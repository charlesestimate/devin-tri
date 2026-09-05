# The live sweep — 74 findings, 14 root causes, and one sentence that matters more than the rest

**Date:** 5 September 2026
**Inputs:** 1st_AI, commercial chain, 29 defects + 3 experiments · 2nd_AI, six project modules, 25 defects + 20 gaps + phone table
**Checked against:** the source export of 4 September. Five claims verified in code; three of them came back different from what the agents could see.
**Author:** Claude, for Karl Ivan Estadola

---

## 0. The sentence

**One person can raise five million pesos, route it to the lowest approval gate by choosing a
dropdown, and approve it themselves. Nobody is told.**

Both agents did it independently, on your live platform, this morning. It is not a theory from
reading the code any more.

Everything else in this document is smaller than that.

---

## 1. What the numbers say

74 findings raised. About 11 are the same finding seen by both agents from different angles —
which is confirmation, not noise. **63 distinct findings, 14 root causes.**

The three experiments came back as clearly as they could have:

| Experiment | Result |
| --- | --- |
| **A — is the gate set by the amount or the severity?** | **The severity. The amount changes nothing.** |
| **B — does hard block 6 stop a purchase order before the contract is signed?** | **No. Something else does, for a different reason, silently.** |
| **C — can you approve your own request?** | **Yes. Eight out of eight record types, plus six more from the other agent.** |

---

## 2. The fourteen root causes

### RC-A — Segregation of duties does not exist. One check in sixteen.

I counted the approval mutations in `convex/`. **There are sixteen.** Exactly one of them checks
that the approver is not the person who raised the record:

```
convex/inventory/inventory.ts:432
if (adj.createdByPersonId === tc.personId)
  throw new ConvexError({ ... "You cannot approve your own adjustment (Gate 26)" });
```

That single line is the entire segregation-of-duties enforcement on the platform.

It also explains something both agents noticed and neither could account for: the **only** refusal
either of them met, in fourteen self-approval attempts, was on a stock adjustment. They were both
hitting the one guarded control in the product.

What went through unopposed, on your live platform, this morning:

| Record | Amount | Gate | Result |
| --- | --- | --- | --- |
| Purchase order PO-202609-002 | ₱9,482,000 | 4 | "Approval recorded" |
| Purchase order PO-202609-001 | ₱1,850,005 | 4 | "Approval recorded" |
| Billing milestone | ₱99,000,000 | 25a / 25b | "Certified" — **both gate reference fields left blank** |
| Fund request | ₱5,000,000 | 23 | "Fund request approved" — then released, then liquidated |
| Write-off | ₱5,000,000 | 3 | "Write-off approved" |
| Write-off | ₱5,000,000 | 1 | "Write-off approved" — **reference `Z2-TEST-NO-SUCH-GATE-APPROVAL`, accepted** |
| Payroll period PAY-2026-002 | — | 30 | "Payroll period approved" |
| Three statutory rate tables | — | 32 | "Rate table approved" ×3 |
| Proposal, won decision, two site reports, maintenance sign-off, document publish | — | 6, 7, — | all approved by their author |

No warning. No confirmation. No note on any record saying the approver and the requester were the
same person. On four of them the Approve button appeared in the same screen position the Submit
button had occupied one second earlier.

**The capability exists and is simply not wired up.** The supplier bank account form already says
*"a second person (not you) must confirm this bank account"*. The inventory module already refuses.
Every other control was written without the check.

**Fix:** one shared guard, applied to all sixteen. This is the single most important change on the
platform and it is not a large one.

---

### RC-B — The gate is chosen by the person raising the record, not derived from the amount

Your specification says the gate is derived from the amount and is never chosen. 1st_AI ran the
2×2 and it is unambiguous:

| | Amount | Severity | Gate raised |
| --- | --- | --- | --- |
| 1 | ₱50,000 | Minor | **Gate 1** |
| 2 | **₱5,000,000** | Minor | **Gate 1** |
| 3 | ₱50,000 | Major | **Gate 3** |
| 4 | **₱5,000,000** | Major | **Gate 3** |

**A hundredfold change in the amount moved the gate not at all. Changing the severity moved it every
time.** And the severity is a dropdown whose own option labels read *"Minor (Gate 1)"*,
*"Moderate (Gate 2)"*, *"Major (Gate 3)"* — the person raising the write-off is not merely
influencing the gate, they are picking it by name, before they type an amount.

Corroborating, from the same run: the purchase order button read *"Submit for Approval (Gate 4)"*
when the order was worth **₱0.00**, and still read *"Submit for Approval (Gate 4)"* after a
**₱9,482,000** line was added.

This is `convex/finance/finance.ts:12` — the defect I read in the code on Thursday — now
demonstrated on your own data, in your own tenant, with reference numbers you can open.

**RC-A and RC-B compound.** Either alone is serious. Together they mean any amount can be routed to
the lowest gate by its author and approved by that same author. 2nd_AI did precisely this with
₱5,000,000 and a fabricated approval reference.

---

### RC-C — Identifier casts used to silence the type system

**This has now caused two of the three worst defects found in three sweeps, in two different
modules.** It is a habit, not an accident.

**The progress claim failure — I found it, and it is one line.**

Both agents failed to create a progress claim. Nine attempts between them, three different payloads,
two different projects, and every one returned the same useless `"Failed to create"`. It is the
reason 2nd_AI concluded Finance would be abandoned.

`src/pages/finance/_components/ProgressClaimsTab.tsx:60`:

```ts
contractId: projectId as unknown as Id<"contracts">,
```

**The client sends the project's identifier where the contract's identifier is required**, cast
twice so TypeScript cannot object. Convex validates `v.id("contracts")` at the argument boundary and
rejects the call. Because that rejection is not a `ConvexError`, the catch block at line 72 falls
through to its generic string — which is exactly why neither agent could get a reason out of it.

The dialog has no contract picker at all, so the fix is two parts: resolve the project's actual
contract, and delete the cast.

**The same pattern, last week:** `convex/reports/reports.ts:311` and `:342` cast an optional
`projectId` twice and took the whole application down. There are **411** `as Id<…>` casts in
`convex/`. Most are harmless. The ones that are not are invisible until a user finds them.

---

### RC-D — Client-defaulted datetimes use the Coordinated Universal Time clock

Both agents root-caused this independently and their measurements agree to the minute.

| Field | Philippine time | Defaulted to |
| --- | --- | --- |
| Record Professional Seal → Sealed At | 11:10 | `2026-09-05T03:09` |
| Record Delivery → Received At | 11:22 | `2026-09-05T03:22` |
| Record Delivery → Received At | 11:29 | `2026-09-05T03:29` |

Eight hours behind, every time, with the browser confirmed in Asia/Manila.

**It is narrower than we thought, and that is good news.** Plain date fields (Report Date, Visit
Date, Assigned Date) all defaulted correctly to 5 September. Every server-set timestamp is correct.
The fault is confined to **client-defaulted `datetime-local` values** — `toISOString()` being sliced
instead of a local datetime being built.

**Why it matters:** between **00:00 and 07:59 Philippine time the defaulted date is yesterday.**
That is when site crews raise permits. And a goods receipt taken at 11:22 this morning is now
permanently on record as **03:22** — a delivery booked at a time the warehouse is shut.

---

### RC-E — Validation is written per form, and mostly not written

Roughly twenty findings. The ones that carry consequence:

| What was accepted | Where | Why it matters |
| --- | --- | --- |
| Contract **signed 31 Dec 2027** | Project | A signature sixteen months in the future **immediately unlocked the project's hardest gate** and, downstream, all of procurement |
| **999 days worked** in a 15-day period | Payroll | An unbounded multiplier sitting directly in front of a pay run — ₱999,000 for half a month, one worker |
| Milestone at **622% of contract value** | Finance | ₱100,617,000 scheduled against a ₱16,170,000 contract |
| Transfer of 25 units from a location holding **zero** | Inventory | Stock went to **−25**. This is almost certainly how the pre-existing −200 at the Laguna warehouse happened |
| Receiving **30** against **25** dispatched | Inventory | Five units created from nothing; flagged "Discrepancy" and never reconciled |
| Delivered 10, accepted 10, **rejected 5** | Procurement | The rejected units vanish from the arithmetic |
| Cumulative progress moved **25% → 10%** | Construction | Reported project progress silently rewritten, no history, no undo |
| Site area **−5,000 m²**, interconnection **−13.8 kV** | Pipeline | The same product's BOM and activity forms carry `min="0"` and refuse correctly. This form simply does not |

Ten of ten deliberately impossible dates were accepted by 2nd_AI. **One good exception, worth
keeping:** a second site report for a date that already has one is refused with a clear message.

---

### RC-F — The write succeeds and the screen does not change

Every state transition on a purchase order produced a correct success toast while the badge and the
buttons kept the old state. Four transitions, four full page reloads to see the truth.

**The consequence is not cosmetic: the Approve button stays on screen after a successful approval,
inviting a second press, on a ₱9,482,000 purchase order.** Combined with RC-A, nothing would stop it.

Same pattern on the design package status, the physical count list (which renders **completely
empty** after submitting — a warehouse would think an hour's counting was destroyed), the physical
count variance (stays at ±0 while you type, which is the entire point of the screen), and the
professional seal (recorded successfully, then never displayed anywhere — you cannot tell a sealed
drawing from an unsealed one, and nothing stops a second contradictory seal).

---

### RC-G — Functions that exist on the server but have no control in the interface

**Variation orders are not missing. The button is missing.**

1st_AI searched all 1.7 million characters of the shipped client bundle and found only a read query.
I checked the server: **`createVariationOrder` exists at `convex/foundation/projects.ts:606`**, and
the protocol layer exposes `toolCreateVariationOrder` as well. The mutation is written. Nothing in
the browser calls it.

That changes the size of the fix from "build variation orders" to "add the control", and it is why
Experiment A had to be run on write-offs instead.

The same shape elsewhere: project parties have a read query and no create; construction blocks have
no sign-off control (progress is reachable only through Site Reports → Add Activity, which nothing
on the blocks screen tells you); the contract record has no signing action, so it reads **Draft
forever** while the project treats it as signed.

---

### RC-H — Nothing tells anyone anything, and it makes RC-A worse

**There is no approvals inbox anywhere in the product.** Not under My Day, not under Tasks, not
under Reports. 1st_AI left eight approvals outstanding and the notification bell showed two
day-old chat mentions and nothing else.

An approval exists only on the record itself. So nobody is ever told that something is waiting for
them — which means **self-approval is not just permitted, it is the path of least resistance.**
There is no other path.

---

### RC-I — The reports under-report, and they do it confidently

| Screen | Says | While |
| --- | --- | --- |
| Board Pack | "Pending Approvals **0**" | Three write-offs sat pending |
| Board Pack | "Hard Block 6 Active **0**" | Finance displayed a red "Hard Block 6 active" banner |
| Exception Report | "No finance exceptions — **28 rules evaluated**, zero exceptions" | ₱10,100,000 of write-offs, one self-approved, and nine failed claim attempts |
| Measure Register | 1 project of 7, "Open NCRs **0**" | A **Critical** non-conformance was open |
| Finance tiles | "Total Claimed **PHP 0**", "0% of contract" | ₱99,000,000 certified on the row directly below |

The Exception Report's own strapline is *"Silence is never ambiguous — zero results with timestamp
and rule count is an explicit response."* Here the silence is wrong, which is worse than a blank
screen: a director reads a confident zero.

The Finance tiles read only from progress claims — which cannot be created (RC-C). So fixing one
line fixes the headline number too.

---

### RC-J — Two identity rosters, confirmed again

46 platform users in the assignee and custodian pickers. **Three** people in the workforce roster.
Add Employee demands both. A solar installer with no login cannot be an equipment custodian, cannot
be assigned a task, and cannot have a human-resources record. An office user can be a custodian but
cannot be deployed. For a company whose people are mostly on roofs, that is the wrong way round.

---

### RC-K — Mobile is one component, and last week's finding was wrong

**2nd_AI corrected last week's report and I am glad it did.** Last week said four modules were
unusable at 375 pixels. On the live platform, across its six modules: **nothing absent, nothing
unusable.** There is a real mobile layout — the sidebar becomes a working drawer, cards stack,
dialogs go full width, and the New Task dialog is genuinely well built.

What it found instead is a consistent **5 to 53 pixel horizontal overflow**, traced to a single
cause: **the project-picker button in each module header is not width-constrained at mobile
breakpoints.** Fixing that one component removes the overflow from four of the six modules.

The remaining real problem is touch targets: every primary control is **28–32 pixels** where Apple's
minimum is 44 and Android's is 48, and the hamburger is **20×20 with no accessible name**. Sorsogon
and Dumaguete crews work in gloves and rain.

---

### RC-L — Records still cannot be corrected, and one dialog corrupts them

The Add Line dialog retains the previous entry's values as real values. 1st_AI's typing appended to
them, and the bill of materials line is stored with unit **`"pcspcs"`** — which then auto-filled
into a purchase order line. **The corruption is in the data, not the display.** Locations, catalogue
items, equipment and workforce records have no edit and no delete, so it is permanent.

This is the third sweep in which this exact bug has produced a corrupted record.

---

### RC-M — The interface never names a role, anywhere

Eight gate references were shown to 1st_AI. Two named the gate. **None named a role.** The write-off
approval dialog is labelled *"Approval Reference (Gate 1/2/3)"* — it does not even say which of the
three applies to the record in front of you.

That is why the "role asked to approve" column in Experiment A is empty: the platform never displays
one. Combined with RC-A, there is nothing on screen to tell a user that somebody else was supposed
to do this.

---

### RC-N — Hard block 6 is a different rule from the one you specified

Your specification: *a signed contract and released funds are required before any purchase order.*

**What the platform actually does:**

- Hard Block 6 on the platform means *an unliquidated cash advance blocks new **fund requests***.
  1st_AI checked Procurement with Hard Block 6 active: "New PO" was enabled and no warning appeared.
- The thing that actually stops a purchase order is **the project's stage** — and it is implemented
  by **silently omitting the project from the picker**. No message, no greyed-out row. A user would
  conclude their project was missing, not gated.
- The only refusal texts in the whole flow are on the project page: *"No signed contract document
  attached. Required to leave setup."* **Neither wording mentions released funds.**
- And 1st_AI raised, approved and issued a **₱9,482,000** purchase order **before any funds had been
  released at all.** The "released funds" half of your rule is not enforced anywhere.

---

## 3. What neither agent could see — three things I found in the code

**1. The progress claim is one line.** `ProgressClaimsTab.tsx:60`, above. Nine failed attempts,
one cast.

**2. Variation orders already exist on the server.** `foundation/projects.ts:606`. Missing button,
not missing feature.

**3. The proposal's lease figure is out by a factor of about 182, and it goes to customers.**

1st_AI flagged "Annual Lease ₱23,450.00" as unverifiable because the constants live in
Administration. The code settles it.

`convex/foundation/seed.ts:463` seeds the constant:

```
key: "lease_reference_rate",  unit: "₱/kilowatt-hour",  numericValue: 6.70
```

`convex/pipeline/proposals.ts:131` uses it:

```ts
const annualLeaseAmount = roofAreaM2 * proposal.pinnedLeaseReferenceRate;
```

**It multiplies square metres by a rate whose own declared unit is pesos per kilowatt-hour.** Those
units do not combine. On 1st_AI's proposal: 3,500 m² × 6.70 = **₱23,450**. Using the quantity the
constant's unit actually calls for — 638,500 kWh × 6.70 — gives **₱4,277,950**.

Every other figure on that proposal recomputed correctly: the markups, the subtotal, the 5%
contingency, the 1,277 kWh/kWp yield, the 7 m²/kWp roof area. **This one number is wrong, it sits
immediately above Total Project Cost, and it appears on a document you send to a client.**

Which of the two readings is right is your call — it depends on what you meant by the constant. But
the formula and the unit cannot both be correct as they stand.

---

## 4. Four things I would not pay to fix

**1. Toasts. Settled — do not spend a peso on it.** 2nd_AI did the work I asked for and produced the
mechanism: at +16.4 seconds the toast was still up with `document.visibilityState` reading
`"hidden"`; a 1000 ms timer probe returned 1 ms of drift the instant visibility flipped to
`"visible"`, and the toast cleared by +31.3 seconds. Chrome suspends timers in an occluded tab.
**Toasts work. Both of last week's agents were wrong, and so was I for passing it on.**

**2. The Exception Report white screen.** 2nd_AI contradicted last week's finding: it now opens
cleanly, renders per-domain sections with rule counts, and found three real exceptions. Either it
was fixed or the empty test copy caused it. Keep the error boundary in Prompt 1 — it is worth having
regardless — but this specific crash is not currently reproducible.

**3. 1st_AI's dropdown mis-selection.** It recorded picking one supplier and getting another, then
**withdrew it** after failing to reproduce under controlled conditions, saying plainly that if it is
real it is the worst defect on the list. That is exactly right. Have a human click through a
supplier picker once; do not prompt for it.

**4. The semi-monthly halving of a "Fixed — exact PHP amount" bracket.** A ₱1.00 flat rate produced
₱0.50 on a half-month period. Halving a monthly figure for a half-month is defensible arithmetic —
the defect is the word "exact" on a field that is actually monthly. **Relabel it. Do not change the
maths** until you have decided which behaviour you want.

---

## 5. What is sitting on your live platform right now

**Needs your attention before anyone is paid:**

- **Three statutory rate tables are approved with fake rates and the platform makes them
  immutable.** PhilHealth, Pag-IBIG and withholding tax, each one bracket at a flat ₱1.00. 1st_AI
  limited them to effective 16 Sep – expiry 30 Sep, so payroll outside that fortnight is blocked
  rather than silently wrong. They cannot be corrected — only superseded by new tables with a later
  effective date.
- **The SSS table was already fake before either agent arrived.** It is named *"SSS test table 2026
  (test values, not official)"*, approved 3 September, and it produced ₱250.00 on an ₱11,000
  semi-monthly gross. **That one is not from this test.** All four of your statutory tables are
  currently non-official.
- **PAY-2026-002 is approved and sitting at the Disburse button.** 1st_AI did not press it. Its
  "do not pay" warning is in the Notes field, which the period list never displays — so a test
  payroll period is indistinguishable from a real one at a glance.

**Needs cleaning up:** roughly sixty `Z1-` and `Z2-` records, listed in full at the end of both
reports. ₱10,000,000 of write-offs on PRJ-2026-0006, one self-approved. Three write-offs left
deliberately pending so you can see the gate assignment yourself.

**One thing to check:** 2nd_AI wrote a task and a resource request into **PRJ-2026-0041** and
flagged that it could not tell whether that project is real. If it is a live Calamba job, those two
records need removing first.

**Both agents obeyed every restriction.** Administration untouched, Migration untouched, General
untouched, no real person's record altered. 2nd_AI declined to enter a bank account number into a
form or press Confirm on someone else's bank account. 1st_AI declined to press Disburse or to
acknowledge a payslip on a worker's behalf. Between them they withdrew six findings after
disproving them.

---

## 6. What to send Hercules on Monday, and in what order

The plan has changed. **What I had as Prompt 2 is now Prompt 1**, because the control layer is worse
than the code review suggested and sixty people arrive next week.

### Prompt 1 — the control layer. Nothing else goes first.
1. One shared segregation-of-duties guard across all sixteen approval mutations (RC-A)
2. Gate derived from amount; remove the gate names from the severity dropdown (RC-B)
3. Hard block 6 rewritten to your rule, and the procurement stage gate given a visible message
   instead of silently omitting the project (RC-N)
4. `ProgressClaimsTab.tsx:60` — one line, and it fixes the Finance headline tiles too (RC-C)
5. The lease reference rate — decide the unit, then fix the formula or the constant (§3.3)

### Prompt 2 — make the records trustworthy.
Validation layer (RC-E), datetime helper (RC-D), state refresh after write (RC-F), the missing
controls that already exist on the server (RC-G).

### Prompt 3 — make it usable.
Approvals inbox (RC-H), report figures (RC-I), one person record (RC-J), the project-picker width
and touch targets (RC-K), edit and delete (RC-L), name the roles (RC-M).

**Do not re-sweep before Prompt 1.** We now know what is wrong. The next agent run should be a
*verification* run against the fixes, not another discovery run.

---

## 7. On the two agents

Both reports are better than the first pair, and the reason is worth keeping.

They corrected themselves. 2nd_AI withdrew five findings — including one it had recorded as a
defect and then traced to its own scripted click — and it disproved the toast finding with a
measurement rather than an opinion. 1st_AI withdrew the dropdown finding while saying plainly that
it would be the worst defect on the list if real. Both listed the assumptions that weaken their own
conclusions. Both stated what they chose not to press, and why.

1st_AI also flagged a judgement call rather than burying it: it needed a worker for the test payroll
and used the other agent's test person rather than a real employee. That was the right call and
telling you about it was better.

**Where I checked their work against the code, they were right every time.** The three things I
added are things no browser could have seen.
