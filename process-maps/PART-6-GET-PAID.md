# Part 6 of 10 — Get Paid

**Level-1 cross-functional map · as specified · 8 September 2026**
**Companion files:** `Part 6 — Get Paid (A3 landscape).pdf` and `.svg` in the same folder

---

## 1. What this process is for

Everything in Parts 2 to 5 spends money. This is the part that brings it back.

Four chains. **Billing the client** turns work done into a certified claim and a paid
invoice. **Drawing cash** advances money to a project and accounts for it afterwards.
**Writing off** authorises a loss. **Variation and forecast** adjusts the contract value and
projects cash in.

**Starts:** a signed contract from Part 2 and block progress from Part 5. **Ends:** money in
the bank, and a forecast that shows whether more is coming.

**The structural finding of this part: the platform can bill a client but cannot pay a
supplier.** There is no accounts payable anywhere — no supplier invoice, no subcontractor
invoice, no payment record, no remittance. Part 4 can raise a purchase order and receive the
goods; there is nowhere to record the bill, and nowhere to pay it. Cash only ever flows in.

---

## 2. Lanes in this map

| Lane | Roles | What they do here |
| --- | --- | --- |
| **External: Client** | The client and their certifier | Certify or dispute the claim. Drawn dashed: outside the company |
| **Executive** | Head of Finance · Director · Chief Operating Officer | Four gates: the fund request, the three write-off bands, the variation order |
| **Finance: Billing** | Finance Officer | Milestones, claims, certification, invoices |
| **Finance: Treasury** | Head of Finance | Fund requests, write-offs, the cash forecast |
| **Projects and Site** | Project Manager | Raises variation orders; supplies the percent complete |
| **The Platform** | — | Derives percent complete, detects the three-month gap |

---

## 3. Billing the client

| # | Lane | Action | Record → state | Gate | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 6.1 | Billing | Create a billing milestone on the contract | `billing_milestones` → `pending` | — | |
| 6.2 | Billing | Raise a progress claim | `progress_claims` → `draft` | — | **Percent complete is derived from block activities and cannot be typed — correct, and one of the better pieces of design in the platform.** The claimed amount is checked against nothing: not the contract value, not the milestone, not the percent complete |
| 6.3 | Billing | Submit the claim to the client | → `submitted` | **G11 · Head of Finance · Director** | **The code raises gate 25a**, which the specification reserves for inter-island inventory transfers. The approval reference is a string the caller supplies and it is not even checked for emptiness |
| 6.4 | External | The client reviews and certifies | → `certified` · `disputed` | — | |
| 6.5 | Billing | Record the certification | → `certified` | **G11 · Head of Finance · Director** | **The code raises gate 25b.** Certified is correctly a separate field from claimed — and is never compared to it, so a claim of ₱1,000,000 can be certified at ₱9,000,000 |
| 6.6 | Billing | Mark the milestone paid | `billing_milestones` → `paid` | — | The paid amount is not checked against the certified amount |
| 6.7 | Billing | Raise the retention invoice at the release date | — | **G12 · Retention Invoice** | **Does not exist.** There is no retention invoice record anywhere. Retention percent and release months are stored on the contract and a release date is derived at turnover — and nothing bills it |

### Gate 11 is the answer to the question Part 4 left open

Part 4 flagged that gates 25a and 25b are claimed by two modules: the specification says
inventory transfers, the finance schema comments say progress claim submission and
certification, and neither module raises them in code.

That is now settled, and the specification is internally consistent. **Gate 11 is
*Progress Claim or Service Charge*.** It is the gate the specification provides for exactly
this step. Its only appearance in the entire codebase is the label list inside the
Administration migration — no code raises it.

So the finance module did not find a gap and fill it. It reached for two numbers that were
already spoken for, while the correct number sat unused. **25a and 25b belong to inventory.
Gate 11 belongs here.** That resolves register item 12's inventory question without a
decision from you; what still needs your sentence is the general rule.

### The retention hole is worth a number

Every EPC contract in this company carries retention — commonly five to ten per cent, held
back until the release date. The contract record has `retentionPercent` and
`retentionReleaseMonths`, and `recordTurnoverDate` correctly derives `retentionReleaseDate`
from them in a single transaction.

**And there is no record that can bill it.** On a ₱50,000,000 project at five per cent, that
is ₱2,500,000 with no route through the platform. It will be invoiced from a spreadsheet, or
forgotten. Gate 12 exists in the specification precisely because this is the money most
often lost.

---

## 4. Drawing cash, and writing off

| # | Lane | Action | Record → state | Gate or block | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 6.8 | Treasury | Raise a fund request | `fund_requests` → `pending` | **HB6** | **Enforced, and well written.** *"Hard Block 6: Fund request FR-… is released but not yet liquidated. Liquidate the outstanding advance before raising a new request."* It names the block, the condition and the release |
| 6.9 | Executive | Approve the request | → `approved` | **G23 · Head of Finance · Director** | No role check, no same-person check. The approved amount is not bounded by the requested amount |
| 6.10 | Treasury | Release the funds | → `released` | — | The person who approved can release. Two of the three cash controls are the same person |
| 6.11 | Treasury | Liquidate the advance | → `liquidated` | — | A liquidation reference is required — correct. Nothing checks what it points at, and there is no amount |
| 6.12 | Treasury | Raise a write-off — seven categories | `write_offs` → `pending_approval` | — | The gate is derived at creation, from **severity** |
| 6.13 | Executive | Approve the write-off | → `approved` | **G1 ≤ ₱50,000 · G2 ₱50,000–₱100,000 · G3 > ₱100,000** | **The gate is read from severity, not from the amount.** `gateIdForSeverity` maps minor→1, moderate→2, major→3. A ₱5,000,000 write-off marked minor raises gate 1 |

### Hard block 6 is the third meaning of that number

This is the same hard block number in a third, different form:

| Where | What HB6 means there | Enforced? |
| --- | --- | --- |
| **The specification** (`seed.ts`) | *No Signed Contract — Funds Blocked.* Releases on a signed contract document | **No code** |
| **Procurement** (`orders.ts`) | A purchase order cannot be issued without a gate 4 approval | Yes — against a reference the browser invents |
| **Finance** (`finance.ts`) | A new fund request is refused while an advance is released and not liquidated | **Yes, properly** |

Three rules, one number. The finance one is the best-implemented hard block in the platform.
The one the specification actually asks for — no funds against an unsigned contract — is the
one that does not exist.

### The write-off gate is the defect Agent 1 proved on the live platform

This is the finding behind 1st_AI's four-row experiment: ₱50,000 minor → gate 1, ₱5,000,000
minor → gate 1, ₱50,000 major → gate 3, ₱5,000,000 major → gate 3. The amount changed
nothing.

The specification is explicit that **the gate is derived from the amount of money involved
and is never chosen by a person**. Severity is a person's judgement typed into a dropdown.
Deriving the approval band from it hands the choice of approver to the person raising the
write-off — which is exactly the thing the rule exists to prevent.

`gateIdForSeverity` at `convex/finance/finance.ts:12` is four lines long and the fix is to
read `args.amount` instead. It is the cheapest high-value change on Monday's list.

---

## 5. Variation and forecast

| # | Lane | Action | Record → state | Gate | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 6.14 | Projects | Raise a variation order | `variation_orders` → `draft` | — | The mutation exists and **no screen calls it** — the whole variation order feature is reachable only through the protocol |
| 6.15 | Executive | Approve the variation order | — | **G8 · Director · Chief Operating Officer** | **No approve mutation exists.** `gate9ApprovalId` is never written by anything, so the value adjustment reaches nothing. The schema comment calls this gate 9; the specification says gate 9 is the signed customer agreement and gate 8 is the variation order — the two are swapped |
| 6.16 | Treasury | Cash forecast — secured, gated, projected | `cash_forecast_lines` | — | **A gated line must carry a gate — correctly refused otherwise.** The three bands are exactly as specified |
| 6.17 | Platform | **Automatic:** three-month gap detected on read | — | — | **Correct.** Three consecutive future months with no secured or gated line. Computed, never stored |
| 6.18 | Platform | **Automatic:** pay a supplier | — | — | **There is no accounts payable.** No supplier invoice, no subcontractor invoice, no payment, no remittance. The forecast covers cash in only |

---

## 6. The RACI

| Step | Finance Officer | Head of Finance | Director | Chief Operating Officer | Project Manager | Client |
| --- | --- | --- | --- | --- | --- | --- |
| 6.1 Billing milestone | **R** | **A** | I | | C | I |
| 6.2 Raise progress claim | **R** | **A** | I | | **C** | |
| 6.3 Submit the claim (G11) | **R** | **A** | C | | I | **I** |
| 6.4 Client certifies | I | **I** | I | | I | **R / A** |
| 6.5 Record certification (G11) | **R** | **A** | C | | I | I |
| 6.6 Mark paid | **R** | **A** | I | | I | I |
| 6.7 Retention invoice (G12) | **R** | **A** | C | I | I | I |
| 6.8 Raise fund request | C | **R / A** | I | | **R** | |
| 6.9 Approve the request (G23) | I | **A** | C | I | I | |
| 6.10 Release the funds | **R** | **A** | I | | I | |
| 6.11 Liquidate the advance | **R** | **A** | I | | C | |
| 6.12 Raise a write-off | **R** | **A** | I | | C | |
| 6.13 Approve — G1 ≤ ₱50,000 | I | **A** | C | | I | |
| 6.13 Approve — G2 ₱50,000–₱100,000 | I | C | **A** | C | I | |
| 6.13 Approve — G3 > ₱100,000 | I | C | C | **A** | I | |
| 6.14 Raise a variation order | C | C | I | | **R / A** | I |
| 6.15 Approve the variation order (G8) | I | C | **A** | C | **R** | **I** |
| 6.16 Cash forecast | **R** | **A** | I | I | C | |
| 6.17 Three-month gap | I | **I** | **I** | **I** | I | |
| 6.18 Pay a supplier | **R** | **A** | I | | I | |

**Reading the matrix.** The Head of Finance is Accountable on sixteen of the twenty steps —
the highest concentration of accountability anywhere in the series. On the cash chain
(6.8 to 6.11) they are Accountable on all four, and the code lets one person raise, approve,
release and liquidate an advance without a second pair of eyes at any point. **Hard block 6
is what stops that becoming a rolling advance — and it is the only thing that does.**

The Client is Responsible for exactly one step, and it is the one the company's cash flow
depends on. There is no expected-decision date on a submitted claim and nobody is notified
when one is certified.

---

## 7. Hand-offs

| From → To | At step | What crosses | What stalls it |
| --- | --- | --- | --- |
| **Site → Billing** | Part 5 → 6.2 | **Block percent complete** | Nothing. This join works — the claim reads the latest cumulative percent per block and stores a weighted average. It is the strongest link in the product |
| Billing → Client | 6.3 → 6.4 | The submitted claim | There is no way to send it. No invoice document, no export, no attachment |
| Client → Billing | 6.4 → 6.5 | Certification | Someone remembering to check. No expected date, no notification |
| Billing → Treasury | 6.5 → 6.8 | A certified claim to draw against | The link is optional — `progressClaimId` on a fund request is not required |
| **Procurement → Treasury** | Part 4 → 6.18 | **The supplier's bill** | **There is nowhere for it to land.** Committed cost is computed from issued orders; nothing records what is actually owed |
| Projects → Executive | 6.14 → 6.15 | A variation order | No screen raises it and no mutation approves it |
| Treasury → Executive | 6.16 → 6.17 | The forecast | Nothing. The gap detection works |

---

## 8. Where the live build differs from this map

| | Deviation | Step | Reference |
| --- | --- | --- | --- |
| 1 | **There is no accounts payable** — the platform cannot record or pay a supplier bill | 6.18 | Structural |
| 2 | **The write-off gate is read from severity, not the amount** | 6.13 | 1-A |
| 3 | **Gate 11 has no code; finance raises 25a and 25b instead** | 6.3, 6.5 | Register |
| 4 | **Gate 12, the retention invoice, has no record at all** | 6.7 | Register |
| 5 | **Gate 8 has no approve mutation** and the schema calls it gate 9 | 6.15 | Register |
| 6 | The progress claim screen passes the project id where a contract id is required, so the claim cannot be created from the interface | 6.2 | 1-01 |
| 7 | The certified amount is never compared with the claimed amount | 6.5 | New |
| 8 | The paid amount is never compared with the certified amount | 6.6 | New |
| 9 | The claimed amount is never compared with the contract value or the percent complete | 6.2 | New |
| 10 | The approved amount on a fund request is not bounded by the requested amount | 6.9 | New |
| 11 | One person can raise, approve, release and liquidate an advance | 6.8–6.11 | RC-A |
| 12 | Gate 23's approval reference is an unchecked string | 6.9 | RC-A |
| 13 | The variation order has no screen | 6.14 | 1-15 |
| 14 | Nobody is notified at any hand-off | all | RC-H |

**What stands out.** The two best-built things in the whole platform are in this part: the
percent-complete derivation, which cannot be typed by a person, and hard block 6, which
refuses clearly and says how to clear itself. Sitting beside them is the largest missing
feature in the product — half of every transaction the company makes has nowhere to go.

---

## 9. A correction, and a decision that is now smaller

**Part 4 asked you to settle gates 25a and 25b. You no longer need to.** The specification
answers it: gate 11 is the progress claim gate, so 25a and 25b are inventory transfer gates,
and the finance module simply used the wrong numbers. I said in Part 4 that "the two readings
cannot both be right" and asked you to choose — that was the wrong framing. The specification
was never ambiguous; only the code was.

What still needs your sentence is the general rule, and it is unchanged from Part 5: **the
thirty rows in `seed.ts` are the register.** With that stated, gates 4, 5, 8, 9, 11, 12, 20,
24, 25a, 25b, 30, 31 and 33 all become mechanical corrections rather than judgement calls.

---

## 10. What is deliberately not in this part

- **Paying people.** Part 7 — payroll is the one outbound payment the platform does have.
- **Turnover, retention release dates and warranty.** Part 8, gates 21 and 34. This part
  shows only that the invoice which should follow the release date does not exist.
- **The contract itself and the risk review.** Part 2, gates 9 and 10.
- **System constants and the thresholds these gates read.** Part 9, gates 22 and 31.
