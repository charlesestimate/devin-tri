# Set C — Procurement and the Laguna warehouse, with real goods

**For:** the Procurement Head and the Laguna warehouse custodian. Two people.
**Where:** office for Part 1 to Part 2; the Laguna warehouse, on the custodian's own phone, for Part 3 to Part 5.
**Time:** about 3 hours, with a real delivery in the middle.
**Project to use:** P1 — Calamba Agro Industrial Corporation. Its bill of materials and one open purchase order already exist.
**Suppliers to use:** SolarTech Distribution Philippines Inc. (peso) and Nordwind Energy GmbH (euro). Both exist.
**Prefix:** every record you create starts with `HT-C`.

## Why a human has to do this

The browser agent can raise a purchase order. It cannot stand at the receiving bay with a delivery receipt in one hand and a phone in the other, count boxes, find a cracked inverter, or count a shelf. The inventory module lives or dies on that.

## Rules

1. Write down exactly what the screen says when something is refused. Screenshot and number it (C-01, C-02, ...).
2. "Could not find" is a valid answer. Do not invent.
3. Never delete anything. Never edit a record you did not create unless the step says so.
4. Use **one real supplier quotation** (supplier name changed) where the step says so.
5. Karl approves what you cannot. Message him on the platform, not Viber.

## Part 1 — What you see, what you must not see

| Step | Who | Do this | Expected | Record |
|---|---|---|---|---|
| 1.1 | Both | Sign in. Read the sidebar. | Procurement and Inventory visible. | The sidebar as you see it. |
| 1.2 | Procurement Head | Open P1, open the material list. | You see **cost**. Note whether you also see price or margin. | Which figures. |
| 1.3 | Custodian | Open P1, open the material list, then the purchase order. Look for **any peso figure**. Export or print the list. | A warehouse custodian sees **no money anywhere**, including the export. | Every place a peso figure appeared. |
| 1.4 | Custodian | Open Finance, Payroll, Human Resource. | Not in your sidebar, or refused. | Result. |
| 1.5 | Both | Open the supplier SolarTech. | It is one **party** record that is also a supplier; there is no separate supplier module. Contacts, bank details, terms are on it. | Anything missing that your supplier file holds today. |

## Part 2 — Purchase orders (Procurement Head)

| Step | Do this | Expected | Record |
|---|---|---|---|
| 2.1 | Raise `HT-C PO 1` to SolarTech on P1 B2 for 1,000 metres of cable at ₱80: ₱80,000. Submit. | **Gate 4**: up to ₱100,000, primary Procurement Officer, alternate Procurement Head, window 2 days recorded only. | Who it named. |
| 2.2 | Approve it yourself as alternate. Then raise `HT-C PO 2` for ₱250,000 and try to approve it yourself. | PO 1: allowed as alternate **only if you did not raise it** — expect a refusal because you raised it; record which happened. PO 2: **gate 5**, primary Procurement Head, alternate Chief Operating Officer, and again refused because you raised it. Ask Karl to approve PO 2. | Both results, exact text. |
| 2.3 | Raise `HT-C PO 3` to Nordwind for 4 inverters at €5,200. | Currency euro; the exchange rate **and its date** are required and stored on the order; the peso value is derived. | Rate and date fields present? Could you change the rate after approval? |
| 2.4 | Try to add a line to PO 1 for an item that is **not on P1's bill of materials**. | Refused or flagged as off-design; it needs a reason. | Text. |
| 2.5 | Ask Karl which pipeline customer has no contract. Try to raise a purchase order on it. | **Hard block 6**: refused, naming the missing contract, never "no permission". | Text. |
| 2.6 | Take one **real recent supplier quotation** (name changed). Enter it as `HT-C real PO` on P1. Time yourself. | Every field you needed for the real order exists. | Minutes. Fields missing. Fields you never use. How long the same takes you today. |
| 2.7 | Open PO 1's thread and post `HT-C PO 1 note`. Mention the custodian. | Custodian receives exactly one notification opening the order. | Custodian's count. |

## Part 3 — Receiving a real delivery (custodian, at the bay, on your phone)

Use the real delivery Karl arranged, or the next box that arrives. Receive it against `HT-C PO 1` even if the goods differ; note the difference.

| Step | Do this | Expected | Record |
|---|---|---|---|
| 3.1 | Open Inventory on your phone at the bay. Find PO 1. | Reachable within three taps. | Taps needed. |
| 3.2 | Count the goods. Enter the received quantity **less than ordered** (if the delivery is complete, receive 900 of 1,000 anyway and note it). Condition `short`. Photograph the delivery receipt with the app camera. | The line stays open with a balance. A **discrepancy** is raised. The block shows *partially ready*. | Screenshot. Was the delivery receipt photograph required or optional? |
| 3.3 | Receive one unit as `damaged`. | It goes to **quarantine** in the same action. | Where the quarantine shows. |
| 3.4 | Try to **issue** the damaged unit to P1 B2. | **Hard block 5**: refused. The attempt is logged. | Text. Ask Karl to confirm the attempt appears in the audit log. |
| 3.5 | Release the quarantine with a reason and an owner. Issue one good unit to P1 B2 against the bill of materials line. | Laguna stock decreases; the block's readiness changes. | Before and after quantities. |
| 3.6 | Raise a **non-conformance report** on the damaged unit, source `delivery`, with the photograph. | It requires the goods receipt reference and at least one photograph. | Could you save it without a photograph? |
| 3.7 | Do steps 3.2 to 3.3 again with **airplane mode on**, then switch it off. | The receipt was captured offline and synced with both times shown. | Both times. Any duplicate. |

## Part 4 — Transfers (Procurement Head raises, custodian handles)

| Step | Who | Do this | Expected | Record |
|---|---|---|---|---|
| 4.1 | Procurement Head | Raise a transmittal Laguna → Sorsogon, 50 metres of cable (small value), `HT-C transfer 1`. | **Gate 25a**, inter-island, **any value**. Expected transit shown. | Gate shown, transit days. |
| 4.2 | Procurement Head | Raise Laguna → Laguna site store (or any within-island destination) at ₱120,000, `HT-C transfer 2`, and another at ₱30,000, `HT-C transfer 3`. | Transfer 2: **gate 25b**. Transfer 3: no gate. | Results. |
| 4.3 | Custodian | Issue transfer 1. | Laguna decreases, **in transit** increases, Sorsogon unchanged until received. | Three quantities. |
| 4.4 | Custodian, on the phone | Print or view the transmittal form. Compare with the paper transmittal you use today. | The form's **revision number** shows on it. Every field on your paper form is present, including RECEIVED BY. | Fields missing. |
| 4.5 | Custodian | Ask Bernie (Sorsogon) or Karl to receive **40 of 50** at Sorsogon. | A discrepancy of 10 is raised. Nothing is written off by itself. | What appeared. |

## Part 5 — Stock count (custodian, in the warehouse)

| Step | Do this | Expected | Record |
|---|---|---|---|
| 5.1 | Pick one shelf with a real item that also exists in the platform (ask Karl to confirm the item). Count it physically. | — | Physical count. Platform count. |
| 5.2 | Enter a **stock count** `HT-C count 1` with your physical figure. If it matches, enter one unit less on purpose and say so. | A **variance** is raised. **Nothing adjusts by itself.** | Did the stock figure change before approval? It must not. |
| 5.3 | Raise the stock adjustment. | **Gate 26**, Head of Finance primary, Chief Operating Officer alternate, **zero tolerance** — even one unit goes to the gate. | Gate shown. |
| 5.4 | Look for **opening stock balance lock**, gate 27. | It names Cristy after a spot check, no alternate. If Laguna's opening balance is already locked, try to change an opening balance. | What you found. |
| 5.5 | Look for any place that lets you type a stock quantity directly, without a receipt, issue, transfer or count. | There must be **none**. | Anything found. |

## Part 6 — Fit to real work (write answers)

1. Procurement Head: list the steps of your last real purchase from request to payment. Beside each, where the platform holds it, or "nowhere".
2. Custodian: list what you record on paper in one day at Laguna. Beside each, where the platform holds it, or "nowhere".
3. Which figures or quantities did the platform show differently from your stock card or Excel? Which is right?
4. Which words on screen did you not understand, and any abbreviations? Write them exactly.
5. If Laguna went live on this next Monday, what would stop you?

## Report — send to Karl within two days

Word or Google document, `HT-C procurement report — [names] — [date]`.

1. Tester names, roles, custodian's phone model.
2. **Step table:** every step, result (**pass** / **fail** / **could not find** / **blocked, needed Karl** / **not tested**), what happened, screenshot numbers.
3. **Quantity tables** from steps 3.5, 4.3 and 5.1.
4. **Money seen by the custodian** (step 1.3): every place a peso figure appeared.
5. **Things that happened by themselves** (a stock figure changing without approval, a non-conformance report appearing that nobody raised, an escalation).
6. **Fit to real work** answers (Part 6).
7. **Records you created**, by name.
8. **Top three problems**, in order, one sentence each.

Attach all screenshots, numbered. Attach a photograph of the paper delivery receipt and the paper transmittal you compared against.
