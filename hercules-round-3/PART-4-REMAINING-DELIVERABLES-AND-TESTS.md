# Magnus Workspace Platform — Hercules build specification, round 3

## Part 4 of 4 · The remaining module deliverables, the person card and the file controls, and the acceptance tests for the round

**Prepared for Karl Ivan Estadola, Chief Executive Officer, Magnus Renewable Tech Corp · 17 September 2026**

Last of four parts. **Build after Parts 1 to 3, in its own thread.** Section D holds the module gaps that stop daily work; section F holds every test for the round in one list, so that "done" has one meaning. Line numbers are from the 8 September export.

### How to use this document with Hercules

Build mode, new thread, paste the whole part. Fix root causes; paste the evidence in section G. One part, one thread, one report. When all four reports are in, run section F in full and paste the results.

### Standing rules that still apply

No scheduler, timer or automation; derived values are computed on read; same-transaction derivation only from fields the human action supplied. Every write through the tenant wrapper under a human's name. No abbreviations or ampersands. Nothing is deleted. Where silent, ask.

---

# A. WHAT THIS ROUND DOES NOT INCLUDE

Operations and Maintenance beyond what exists, the offline field path re-test on a real rooftop, migration loading, and the second test tenant are not in this round. They stay on the register and follow once Parts 1 to 4 have reported. Nothing here widens the platform: every item is a gap in something already specified.

---

# B. FOUR PRINCIPLES THAT DECIDE THE ITEMS BELOW

1. **Capture must have consequence.** A goods receipt that moves no stock, a hand-off that notifies nobody, a photograph field nothing can fill — each is a record read by nothing.
2. **Derived, never typed.** Project stage, percentage complete, project name, unread totals, task counts.
3. **Every hand-off raises a notification in the same mutation** to exactly one person, pointing at the record.
4. **One reusable control** for attach, send and print, placed once and reused everywhere, so the next screen that needs an upload costs nothing.

---

# C. THE STATE ON 17 SEPTEMBER

- The Google Drive connection is live (`karl.magnuscorp@gmail.com`, root folder `1Xnk7akftMLYDletDKnZPtT56IuBvIL31`, nothing staged) and the `files` module can stage, push, mark and serve. **The only upload control in the product is the chat composer.**
- `persons` holds full name, display name, aliases, population, employment basis, home region, sign-in email and status. **No telephone number, no photograph, no notes field.**
- Procurement and inventory share no data: a goods receipt moves no stock.
- The only project stage mutation is setup → design; nothing sets procurement, construction, commissioning or handover.
- No accounts payable record exists.
- Nobody is notified at any hand-off.

---

# D. THE ITEMS

## D1 · A project's stage is derived from its blocks — remove the stage mutation

`setup` → `active` requires the signed contract (hard block 6). After that there is **no stored phase**: stage is computed on read from block states and shown as a distribution — *design complete on 3 blocks, procurement on 4, construction on 2*. Remove the single setup → design mutation and any `stage` or `phase` column; the project list shows the distribution and the derived name `{capacity}_kW_{Customer}` with the project number beneath (already built — verify it appears everywhere a number appeared).

## D2 · A goods receipt moves stock in the same mutation

`goods_receipts` and `stock_positions` are unconnected. Change `recordGoodsReceipt`: for each received line, increase `stock_positions.quantity_on_hand` at the receiving location (or `quantity_quarantined` where the condition is `damaged`, `wrong_item` or `short`), increment `bill_of_materials_line.quantity_received` and `purchase_order_line.quantity_received`, advance `purchase_status` to `partially_received` or `received`, advance the purchase order state, create serial rows where `is_serialised`, and raise a **discrepancy notification to the receiving custodian and the Procurement Head** where a line is short. A quarantined line is then refused for issue by hard block 5. Material readiness per block (`ready` / `partially_ready` / `not_ready` with the latest expected arrival date) is computed on read from these fields. No separate adjustment is typed to record a receipt.

## D3 · Every hand-off notifies — the same rule stated once, applied everywhere

In the same mutation as the action, to exactly one person, `action_required`, pointing at the record, cleared by the work being done:

| Action | Recipient |
|---|---|
| Approval request raised (every gate) | Primary approver (Task); alternate (Information) |
| Approval decided | Requester (Response) |
| Task assigned, or blocked on a person | Owner; the blocker |
| Site report submitted | Project Manager (Check where any activity is blocked) |
| Goods received short or damaged; transmittal received short | Both custodians and the Procurement Head |
| Resource request raised | Allocator |
| Non-conformance raised | Owner |
| Safety stop raised | Safety Officer and Person In Charge — push with mandatory acknowledgement |
| Permit to work requested | Safety Officer of record |
| Payroll period blocked on missing site reports | Person In Charge and their manager |
| Work order assigned; agreement activated; billable order closed; warranty claim raised | Owner; Head of Finance |
| Sign-in granted; role approved | The person (Information) |
| Console holder added, or a `decide` session created | The other console holder |

Build one helper `notifyHandoff(recipient, category, objectType, objectId, headline)` and call it from each of the mutations above. Search afterwards for any mutation that changes an owner, approver, custodian or assignee without calling it.

## D4 · The person card

Add to `persons`: `mobileNumber`, `alternateNumber`, `contactEmail` (separate from the sign-in address), `photographFileId` (a `files` row — therefore Drive, under *Magnus Platform / Human Resource / People / [person identifier] /*), `contactNote` (free text: *reach him on the site radio*, *on leave until the fifteenth*). A card opens from the People list and from any name anywhere — a message author, a reactor, a task owner, an approver, a site report, a group member — showing photograph, numbers, contact email, note, current roles and sign-in state. Everyone signed in may view; edits are audited; the person may edit their own card from self-service. The photograph upload on the card is the **first use of the file control in D5** and sets the pattern.

## D5 · Attach, send and print — one control, reused

One component: upload (camera-only where the object requires it; file otherwise), preview, download, replace-as-new-revision where the object is a document. Placed on: the person card (photograph) · contract (signed document — this is what releases hard block 6) · party (insurance certificate — hard block 1) · project (Construction Safety and Health Program document — hard block 2) · purchase order (supplier quotations; **Send** produces the purchase order document as a `files` row under the order's folder and records who sent it, when and to which contact) · goods receipt (photographs) · design deliverable · permit (filing reference and approval document) · toolbox meeting and site photographs (camera only, never the gallery) · incident, corrective action and non-conformance evidence · payroll period (acknowledgement sheet photographs) · payslip · progress claim and service charge (**Print** produces the invoice document) · work order and warranty claim evidence. Every file goes through the existing pipe (stage → Drive → mark → serve) into the derived folder tree; no Drive link is ever issued; money visibility applies to what is printed.

## D6 · Accounts payable

`supplier_invoice` — party · purchase order · invoice number · date · amount · currency · due date · document file · state (`received` / `matched` / `approved_for_payment` / `paid` / `disputed`) · matched receipts. `supplier_payment` — invoice · amount · paid on · paid by · bank account used · **flag where the party's bank account changed since the previous payment** · reference. A sub-ledger record: no journal, no ledger. Committed cost stays at purchase order issue; what is owed is now recorded beside it.

## D7 · Smaller items carried from 8 September

- **Sidebar order and wording** per section 13: Dashboard · My Day · Pipeline · Projects · Design and Engineering · Procurement · Permits · Inventory · Manpower and Equipment · Safety · Operations and Maintenance · Documents · Messages · Finance · Human Resource · Payroll · Reports · Administration. No *Tasks* or *Construction* item; no ampersand anywhere (the dashboard cards carry one today).
- **Local government unit** on `sites`, shown on the form and returned by the site tools.
- **Audit chain panel** shows the true last sequence and the exact range verified.
- **Every summary and exception figure returns `sources`**; no exception domain evaluates zero rules.
- **Hard block 6 flag** on every project read: `fundsBlockedNoContract` true while `contractId` is empty.

---

# E. WHAT NOT TO BUILD IN THIS PART

A stored project phase; a typed percentage complete; a separate procurement list; a supplier rating screen; a general ledger or journal; outbound email for any of the notifications above; a notification digest; a notification addressed to a role or a group; any per-person hours, presence or location field on the person card; a Drive sharing link; a gallery upload path.

---

# F. THE ACCEPTANCE TESTS FOR THIS ROUND — RUN ALL AFTER PART 4 REPORTS

Tests from the master specification are cited by their original number; new tests carry a letter.

**Messaging (Part 1)**
- **M1** General (5) — five unread on the row, the Company header, the sidebar and the dashboard; opening clears all four; values match `channel_members.unreadCount`.
- **M2** A mention and a direct message each create one `action_required` notification pointing at the channel; the bell badge counts them; opening the conversation clears them; ten unmentioned messages create none (test 114).
- **M3** Each notification type navigates to its record on click (test: paste the route).
- **M4** A reaction toggles off on the second click; the chip shows who reacted.
- **M5** A new direct message and a new group each work on the first attempt on a throttled connection.
- **M6** `deleteThread` does not exist; archive and restore work for group, account space, record thread and direct; General and Announcement refuse; automatic restore on a new record; archived items are excluded from counts and included in search (tests 237, 243, 246, 247).
- **M7** Announcement refuses a non-administrator post; an administrator's edit stores the revision, shows *edited*, and is audited; a General message cannot be edited (test 116 holds outside Announcement).
- **M8** A person with no link sees the sentence with their address on Messages.
- **M9** The group panel's six controls and `access_for_review` work and are logged; tests 243, 250.
- **M10** Offline order and de-duplication (tests 115, 248); speed (test 244); convert to task (test 245); direct message notifies without a mention (test 249).
- **M11** `get_account_activity` excludes a group the caller is not in (test 251).
- **M12** No mute, watch, subscribe or follow anywhere.

**Access, dashboard, search, configuration (Part 2)**
- **A1–A10** as listed in Part 2 §E, plus tests 21 (identity revocation ends the session), 24 (offboarding blocks on open work), 25 (console holder excluded from Human Resource and payroll data), 26 (role history survives), 152 (silence states what was checked), 180 (second tenant profile runs — deferred, note it).

**Governance (Part 3)**
- **G1–G13** as listed in Part 3 §D, plus tests 9, 10, 11, 12, 15, 16, 17, 18, 22, 35, 36, 60, 64, 84, 91, 127, 145, 168, 181, 259–270 of the Base44 specification's Part 12 where applicable to this build.

**Remaining deliverables (Part 4)**
- **R1** No `stage` or `phase` column; a project with blocks in three states shows a distribution (test 38); the derived name appears on the list, header, search, pickers, channel, notifications and board pack.
- **R2** Record a receipt of 10 with 2 damaged: on-hand rises by 8 and quarantined by 2 at the location in the same mutation; `quantity_received` on the line and the order line read 10; the block reads `partially_ready` with the outstanding line's date; issuing the quarantined 2 is refused under hard block 5 (tests 52, 55, 60).
- **R3** Each row of the D3 table produces exactly one notification to the named person in the same mutation, cleared by the named work (tests 66, 81, 105).
- **R4** The person card opens from six different places; the photograph lands under Human Resource / People in Drive; edits are audited; a person edits their own card.
- **R5** Each object in D5 accepts an upload through the one control; a purchase order's Send and a claim's Print produce `files` rows in the right folders; no Drive link is issued (tests 252, 254, 256).
- **R6** A supplier invoice is matched to a receipt and paid; a payment after a bank change is flagged (test 57).
- **R7** Sidebar in the specified order with no ampersand; `local_government_unit` on the site form; the chain panel shows the true last sequence; every figure returns `sources`; `fundsBlockedNoContract` reads true then false (tests 226, 227).

**The test of the whole platform**
- **Test 8** — leave the deployed platform twenty-four hours with nobody connected; the audit log for the period is empty.

---

# G. REPORT BACK — PASTE THE EVIDENCE

1. The search for `stage` and `phase` columns and mutations (none), and one project list row with the distribution and the derived name.
2. The `recordGoodsReceipt` mutation body and the `stock_positions` rows before and after one receipt with a damaged line.
3. The `notifyHandoff` helper and the list of its call sites with file and line; one notification row from each row of the D3 table.
4. The five new `persons` fields in the schema; the card rendered from a message author and from the People list; the Drive folder of one uploaded photograph.
5. The file control's component and its placements, with one `files` row from a purchase order Send and one from a claim Print.
6. One supplier invoice through received → matched → approved_for_payment → paid, and one flagged payment.
7. The sidebar as rendered; the site form; the chain panel; one `get_project` response.
8. Section F in full — every test, result pasted, no summaries.
