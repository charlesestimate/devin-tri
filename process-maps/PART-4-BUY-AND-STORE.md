# Part 4 of 10 — Buy and Store

**Level-1 cross-functional map · as specified · 8 September 2026**
**Companion files:** `Part 4 — Buy and Store (A3 landscape).pdf` and `.svg` in the same folder

---

## 1. What this process is for

Two chains again, and this time they genuinely never meet.

**The buy chain** turns a bill of materials line into a purchase order, gets it approved on
an amount band, issues it to the supplier, and records what arrives. Committed cost starts
the moment the order is issued.

**The store chain** holds what the company already owns across three warehouses — Laguna,
Sorsogon and Dumaguete — moves it between them and out to site, corrects it when it is
wrong, and counts it.

**Starts:** an approved bill of materials from Part 3. **Ends:** material on site, and a
stock position the company can trust.

**The structural finding of this part is that the two chains are not connected.** A goods
receipt does not put anything into stock. Not one line of code moves a received quantity
into a stock position. Procurement believes the material arrived; the warehouse has never
heard of it. Every figure on the inventory screen was typed in by hand.

---

## 2. Lanes in this map

| Lane | Roles | What they do here |
| --- | --- | --- |
| **External Suppliers** | The supplier | Deliver. Drawn dashed: outside the company |
| **Executive** | Procurement Head · Director · Chief Operating Officer · Warehouse Custodian as gate holder | Six gates in the specification: 4, 5, 25a, 25b, 26 and 27 |
| **Procurement** | Procurement Head · Procurement Officer | Responsible for the whole buy chain |
| **Warehouse and Logistics** | Warehouse Custodian | Responsible for the whole store chain |
| **Projects and Site** | Project Manager · Person In Charge | Receive transfers and draw material |
| **The Platform** | — | Recomputes delivery status and material readiness |

---

## 3. The buy chain

| # | Lane | Action | Record → state | Gate | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 4.1 | Procurement | Create the purchase order against a project and a supplier | `purchase_orders` → `draft` | — | The order number is `PO-YYYYMM-nnn`, counted from orders **on that project**, so two projects in the same month both produce `PO-202609-001` |
| 4.2 | Procurement | Add order lines, each optionally linked to a bill of materials line | `purchase_order_lines` → `open` | — | The link is optional, and material readiness only counts linked lines |
| 4.3 | Procurement | Submit for approval | → `pending_approval` | **G4 or G5** raised | Correctly refused unless the order has at least one line |
| 4.4 | Executive | Approve the order | → `approved` | **G4 ≤ ₱100,000 · Procurement Head · Director · 2 days** — **G5 > ₱100,000 · Director · Chief Operating Officer · 2 days** | **The approval is not real.** The browser sends `manual-<timestamp>` as the approval reference. No approval request is created, no approver is named, no role is checked, and the amount is never looked at |
| 4.5 | Procurement | Issue the order to the supplier — committed cost begins | → `issued` | — | **HB6** is checked here, and passes on any non-empty reference |
| 4.6 | External | The supplier delivers | — | — | |
| 4.7 | Warehouse | Record the goods receipt | `goods_receipts` → `pending` | — | **Nothing enters stock.** Delivered quantity above ordered quantity is accepted. `accepted + rejected` is never checked against `delivered`. The three inspection statuses — accepted, partially accepted, rejected — cannot be reached: no mutation sets them |
| 4.8 | Platform | **Automatic:** delivery status recomputed | → `partially_delivered` · `fully_delivered` | — | Correct |
| 4.9 | Platform | **Automatic:** material readiness — computed on read, never stored | — | — | Counts only order lines linked to a bill of materials line. An unlinked line reads as zero readiness however much has arrived |
| 4.10 | Procurement | Amend an issued order | — | — | **Does not exist.** The schema reserves `gate5ApprovalId` for it; no mutation writes that field. An issued order is frozen — the error says *"Use an amendment (Gate 5)"* and there is nothing to use |
| 4.11 | Procurement | Add the supplier's bank account | `supplier_bank_accounts` → `confirmed = false` | — | |
| 4.12 | Procurement | **A second person** confirms the account | → `confirmed = true` | — | **Enforced.** The person who added the account cannot confirm it. Adding a new account supersedes the old one |

### Two things worth stating plainly

**The second-person rule on bank accounts works.** It is the second genuine control found so
far, after gate 18. The refusal is specific and readable: *"The person who added the bank
account cannot be the same person who confirms it. A second person must confirm."* This
matters more than it looks — supplier bank fraud is the single most common way a
construction company loses money, and this is the control that stops it.

**Gate 4 and gate 5 are not what the code thinks they are.** The specification says gate 4 is
*Purchase Order Up To One Hundred Thousand Pesos* and gate 5 is *Purchase Order Above One
Hundred Thousand Pesos* — an amount band, exactly like the finance gates. The procurement
schema's own comment says gate 4 is "Purchase Order Issue" and gate 5 is "Purchase Order
Amendment." The field is named `gate4ApprovalId` and there is only one of it, so every
purchase order at every value is routed to gate 4. **A ₱5,000,000 order and a ₱50,000 order
take the same approval path.** This is the same defect as the finance severity bug in
`gateIdForSeverity`, in a second module, arrived at a different way: there the gate was
derived from the wrong field, here the gate is hard-coded into the field name.

---

## 4. The store chain

| # | Lane | Action | Record → state | Gate | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 4.13 | Warehouse | Maintain locations and the item catalogue — seven categories | `locations` · `items` | — | Item code and location code are unique, and correctly refused on collision |
| 4.14 | Warehouse | Create a stock transfer — four directions | `stock_transfers` → `draft` | — | Source and destination must differ; at least one line required. Both correct |
| 4.15 | Warehouse | Dispatch | → `dispatched` | **G25a** inter-island · **G25b** within-island > ₱100,000 | **No stock check.** Dispatching more than exists drives on-hand negative with no warning. **Neither gate is raised anywhere** |
| 4.16 | Projects and Site | Receive at destination | → `received` · `discrepancy` | — | |
| 4.17 | Platform | **Automatic:** discrepancy flagged | `stock_positions` updated | — | **The shortfall vanishes.** In-transit is reduced by the dispatched quantity, on-hand is increased by the received quantity, and the difference is written off silently — no quarantine, no variance record, no adjustment raised |
| 4.18 | Warehouse | Raise a stock adjustment — write up or write off | `stock_adjustments` → `pending_approval` | — | Quantity must be positive. Correct |
| 4.19 | Executive | Approve the adjustment | → `approved`, stock moves | **G26 · Warehouse Custodian · Project Manager** | **The only same-person refusal in the platform.** *"You cannot approve your own adjustment (Gate 26)"* |
| 4.20 | Warehouse | Open a physical count — stock is snapshotted into count lines | `physical_counts` → `open` | **G27** opening stock lock | `lockDate` is stored and locks nothing — transfers and adjustments can move stock while the count is open. **G27 has no code anywhere.** Only items that already have a stock position are snapshotted, so material physically present but never recorded cannot be counted in |
| 4.21 | Warehouse | Submit the counted quantities | → `submitted`, variance computed per line | — | |
| 4.22 | Warehouse | Close the count | → `closed` | — | **Every variance is written straight into stock with no approval at all.** The same person can open, submit and close it |
| 4.23 | Projects and Site | Issue material to site | `stock_transfers` `warehouse_to_site` | — | **HB5** — quarantined material cannot be issued. The `quarantined` quantity **is never set by any code**, so the block can never fire |

### Gate 26 is attached to the wrong record

The specification is precise: gate 26 is *"Approve inventory physical count variance
write-off at zero tolerance."* It belongs on the physical count — the moment a counted
figure overwrites a system figure.

In the build, gate 26 sits on the manual stock adjustment, which the specification does not
gate, and the physical count, which the specification does gate, has no approval on it at
all. So the one warehouse control the company wrote down is enforced on the path nobody
uses and absent from the path that actually rewrites the books. A warehouse custodian who
wants to make a shortfall disappear does not raise an adjustment and get refused — they open
a count, type the number they want, and close it.

**This is the most consequential single finding in Part 4.** It is also the cheapest to fix:
the refusal already exists twelve lines away, in `approveAdjustment`.

---

## 5. The RACI

| Step | Procurement Head | Procurement Officer | Warehouse Custodian | Project Manager | Director | Chief Operating Officer | Person In Charge | Supplier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4.1 Create purchase order | **A** | **R** | | C | | | | I |
| 4.2 Add order lines | **A** | **R** | C | C | | | | |
| 4.3 Submit for approval | **A** | **R** | | I | | | | |
| 4.4 Approve — G4 ≤ ₱100,000 | **A** | I | | I | C | | | |
| 4.4 Approve — G5 > ₱100,000 | C | I | | I | **A** | C | | |
| 4.5 Issue to supplier | **A** | **R** | I | I | | | | **I** |
| 4.6 Supplier delivers | I | I | I | | | | | **R** |
| 4.7 Record goods receipt | I | C | **R / A** | I | | | C | |
| 4.8 Delivery status recomputed | I | I | I | I | | | | |
| 4.9 Material readiness | C | I | I | **I** | | | | |
| 4.10 Amend an issued order | **A** | **R** | | C | C | | | I |
| 4.11 Add bank account | **A** | **R** | | | | | | |
| 4.12 Confirm bank account | **R / A** | | | | C | | | |
| 4.13 Locations and catalogue | C | | **R / A** | | | | | |
| 4.14 Create stock transfer | | | **R / A** | C | | | | |
| 4.15 Dispatch — G25a inter-island | | | **R** | C | **A** | C | | |
| 4.15 Dispatch — G25b within-island | | | **R** | **A** | C | | | |
| 4.16 Receive at destination | | | I | **A** | | | **R** | |
| 4.17 Discrepancy flagged | I | | **I** | **I** | | | | |
| 4.18 Raise stock adjustment | | | **R** | I | | | | |
| 4.19 Approve adjustment — G26 | | | **A** | C | | | | |
| 4.20 Open physical count — G27 | | | **R / A** | I | | | | |
| 4.21 Submit counted quantities | | | **R** | | | | C | |
| 4.22 Close the count | | | **R / A** | I | | | | |
| 4.23 Issue material to site | | | **R** | **A** | | | C | |

**Reading the matrix.** The Warehouse Custodian is Responsible or Accountable on eleven of
the twenty-three steps and is the only role on eight of them. On the physical count — the
one step that can silently rewrite the value of everything the company owns — they are both
Responsible and Accountable, with nobody Consulted. That single cell is the control weakness
of this part written down in one place.

Procurement never appears in the store chain, and the warehouse never appears in the buy
chain except at the goods receipt. That is the disconnect drawn as a matrix.

---

## 6. Hand-offs

| From → To | At step | What crosses | What stalls it |
| --- | --- | --- | --- |
| Engineering → Procurement | Part 3 → 4.2 | The bill of materials line | Nothing. The link auto-fills description, quantity and unit — one of the better joins in the product |
| Procurement → Executive | 4.3 → 4.4 | An order awaiting approval | Nobody is told (RC-H) |
| Procurement → Supplier | 4.5 → 4.6 | The issued order | There is no way to send it. No print, no export, no email — the order exists only on screen |
| Supplier → Warehouse | 4.6 → 4.7 | The delivery | |
| **Warehouse → Warehouse** | **4.7 → 4.13** | **Nothing — this is the break** | Received material never becomes stock. Somebody has to notice the delivery and type it in as an adjustment or a count |
| Warehouse → Site | 4.15 → 4.16 | Material in transit | The receiver has to be on the platform to close it. Sorsogon and Dumaguete work from phones |
| Procurement → Finance | 4.5 → Part 6 | Committed cost | Committed cost is computed from issued orders only, and never compared against the contract value |

---

## 7. Where the live build differs from this map

| | Deviation | Step | Reference |
| --- | --- | --- | --- |
| 1 | **A goods receipt does not move stock.** Procurement and inventory share no data at all | 4.7 | Structural |
| 2 | **The gate 4 approval is a string the browser invents.** No approval request, no approver, no role check | 4.4 | RC-A |
| 3 | **Gates 4 and 5 are collapsed into one field**, so the ₱100,000 band is never applied | 4.4 | Register |
| 4 | **Closing a physical count rewrites stock with no approval**, by one person, unopposed | 4.22 | New |
| 5 | **Gate 26 sits on the adjustment, not on the count** — the specification puts it on the count | 4.19, 4.22 | Register |
| 6 | **The quarantined quantity is never set by any code**, so hard block 5 can never fire | 4.23 | Register |
| 7 | **Gates 25a, 25b and 27 have no code anywhere** — transfers need no approval at any value | 4.15, 4.20 | Register |
| 8 | Dispatching more than exists drives on-hand negative with no warning | 4.15 | 2-04 |
| 9 | A transfer discrepancy writes the shortfall off silently | 4.17 | New |
| 10 | Over-receipt is accepted; the three goods-receipt inspection statuses are unreachable | 4.7 | New |
| 11 | An issued order cannot be amended, and the error tells you to use the amendment that does not exist | 4.10 | New |
| 12 | Order numbers are counted per project, so two projects collide in the same month | 4.1 | New |
| 13 | An issued order cannot be sent to the supplier — no print, no export, no attachment | 4.5 | 2-09 |
| 14 | Nobody is notified at any hand-off | all | RC-H |

**What stands out.** Part 3 had one strong control and one missing gate. Part 4 has two
strong controls — the second-person bank rule and the gate 26 self-approval refusal — sitting
beside the largest structural hole found anywhere in the platform: **buying and storing are
two separate systems that happen to share a menu.**

---

## 8. Three corrections to earlier work

**Gates 25a and 25b are claimed by two modules.** Part 0 assigned them here, from the
specification: 25a is *Inter-Island Inventory Transfer*, 25b is *Within-Island Inventory
Transfer Above One Hundred Thousand Pesos*. But `convex/schema/finance.ts` documents 25a as
the gate for submitting a progress claim to the client and 25b as the gate for recording
certification. Neither module raises them in code, so nothing is broken today — but the two
readings cannot both be right, and **this has to be settled before Part 6 is drawn.** It goes
to the plan's register item 12 alongside the label conflict.

**There is already a button that fixes the register conflict — partly.** Administration →
Setup and Migration → **Run Hard Block Migration** rewrites all six live hard block rows to
the specification wording and corrects seven gate labels, including gate 5 to *Purchase Order
Above One Hundred Thousand Pesos* and gate 25a to *Inter-Island Inventory Transfer*. It is
idempotent and nobody has ever run it. It does not touch the other eighteen labels that
differ, so it narrows the two-register problem rather than closing it.

**Hard block 6 is not what Part 0 said it was.** The specification's HB6 is *"No Signed
Contract — Funds Blocked"*, releasing on a signed contract document. The code's HB6 blocks
issuing a purchase order without a gate 4 approval. Those are two different rules with one
number. The contract check the specification asks for does not exist; what exists is an
approval check that passes on a made-up string. This is why Agent 1's Experiment B found a
refusal that did not mention a contract.

---

## 9. What is deliberately not in this part

- **Paying the supplier.** Part 6 — the invoice, the fund request and the disbursement.
- **Material consumed on site.** Part 5 — issue against a block, and the daily site report.
- **The contract that should gate the first purchase order.** Part 2 raised it; Part 6 spends it.
- **Warehouse staffing and shifts.** Part 7.
