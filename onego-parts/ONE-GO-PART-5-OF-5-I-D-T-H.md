# CONFORMANCE BUILD INSTRUCTION — CONTINUATION 5 OF 5

This continues the same message. It completes the instruction. Part H is the milestone order for the whole instruction, all five pieces included. Deliverable 0 covers every requirement number in all five.

---
# PART I — INTERFACE, LABELS AND USABILITY (Milestone 9)

## I1 · Theme

**I1.1** Light theme by default: white cards on a light neutral ground, dark grey text, one accent colour used for primary actions, active navigation, links and focus. The accent is the Magnus orange from the logo flame. Use these values as design tokens, never as literals scattered through components:

| Token | Value | Use |
|---|---|---|
| accent | #F06818 | primary buttons, active navigation, selected tabs, progress; white text on it only at 18 point or larger, or bold 14 point |
| accent-hover | #D45410 | hover and pressed state |
| accent-text | #C24A0C | links and accent-coloured text on white or light ground (contrast 4.9 to 1) |
| accent-amber | #F8A828 | highlights, badges and charts only, never text |
| accent-tint | #FFF1E8 | selected rows, active sidebar background, notification chips |
| ground | #F5F6F7 | page background |
| surface | #FFFFFF | cards, dialogs, sidebar |
| text | #1F2937 | body text |
| text-muted | #6B7280 | secondary text |
| border | #E5E7EB | dividers and card edges |

The logo keeps its own blue and orange. Blue is not used as an accent anywhere else, and the logo image is the one from the Magnus letterhead. Refusals and hard block messages use a red that is distinct from the accent; warnings amber; success green; none of the three is the accent.

**I1.2** The field screens, site report, toolbox meeting, safety forms and the emergency card, are tested in direct sunlight on a phone: larger type, higher contrast, and a high-contrast switch on the person's profile that applies only to that person.

**I1.3** Dark theme remains available as a personal setting; it is not the default.

## I2 · Sidebar and headers

**I2.1** Exactly eighteen items, this order, these words: Dashboard · My Day · Pipeline · Projects · Design and Engineering · Procurement · Permits · Inventory · Manpower and Equipment · Safety · Operations and Maintenance · Documents · Messages · Finance · Human Resource · Payroll · Reports · Administration. Migration and Cutover appears as a nineteenth item below Administration only until the cutover date. "Tasks" and "Construction" are removed as items; their screens live under My Day and Projects. Every module header repeats the sidebar wording in full.

**I2.2** The brand shows the Magnus name and logo, never "OPS PLATFORM".

## I3 · No abbreviations, no ampersands

**I3.1** Replace every one of these, found on screen during the test, with the full term, including in record prefixes where the prefix is shown as a label: OPS · EPC → engineering, procurement and construction · PTW → permit to work · BOM → bill of materials · BOS → balance of system · CRM → customer relationship management · O&M → operations and maintenance · NCR → non-conformance report · CAR → corrective action · SSS → Social Security System · HR → Human Resource · TIN → taxpayer identification number · PRC → Professional Regulation Commission · NPC → National Privacy Commission · MCP → Model Context Protocol · kWp → kilowatt-peak · kWh → kilowatt-hour · kV → kilovolt · sqm and m² → square metres · PHP → ₱ · HB1 to HB6 → hard block 1 to 6 · WH-LAG, WH-SOR, WH-DUM → Laguna Warehouse, Sorsogon Warehouse, Dumaguete Warehouse · EMP, RRQ, EQP, SN, TRF, ADJ, MOD, PO, SR, BM, FR, WO, PAY, DP, GR as visible labels → the full object name · Insp. · Part. · Cumul. % · Est. · Qty → quantity · pcs → pieces · "3d" → 3 working days · "0h" → 0 hours · "10y" → 10 years · EE Share and ER Share → employee share and employer share · e.g. → for example. Record numbers may keep a short prefix inside the number itself, such as PRJ-2026-0001, because the number is an identifier, not a label; the label beside it is the full word.

**I3.2** Every ampersand used for "and" is replaced: Design and Engineering, Pipeline, Safety, Operations and Maintenance Providers.

## I4 · Usability defects to fix

**I4.1** Dropdowns must not change selection when a person types while the control has focus; typing opens a filter.
**I4.2** The first click on any row, button or navigation item acts; no control requires a second click.
**I4.3** After any status change, the screen reflects the new state without reload.
**I4.4** Escape in a nested dialog closes only that dialog and keeps the form beneath it.
**I4.5** Placeholder text is never treated as a value.
**I4.6** Empty lists on first use show what to do, never a "Seed" button.
**I4.7** Toolbox attendees, blockers, approvers and custodians are picked from persons, never typed.

---
# PART D — TEST DATA AND THE STATE OF THIS DEPLOYMENT (Milestone 10)

**D1** Everything created on 3 September 2026 by the browser test is test data: ten customer accounts, eleven sites, ten contacts, eighteen persons, three warehouses, ten opportunities, ten proposals, five projects, five contracts, one design package, purchase orders, site reports, permits, inventory movements, safety records, tasks, documents, finance records, the payroll period, the statutory test table, and the two earlier trial accounts "test2" and "This is a test". So is every record the staff tests create with the prefix HT-.

**D2** Build a console-holder action under Migration and Cutover: **Clear test data**, which lists what it will remove by object type and count, requires the console holder to type the tenant name, removes those business records, keeps the tenant, roles, gates, hard blocks, system constants, configuration, console holders and the audit log, and writes an audit entry per removed record. It is refused once the cutover date is set. **Do not run it.** Karl runs it in the Hercules chat after the staff tests finish, if this deployment goes live. If a copy goes live instead, it is never run here.

**D3** The audit log is never cleared. Test-period entries remain and are distinguishable by date.

---
# PART T — ACCEPTANCE TESTS 259 TO 290, APPENDED TO SECTION 14

## Foundation

259. **Roles exist and bind.** Assign Person In Charge to Mario Bautista; gate 24 raises to the department head; after approval Mario's queries carry `money_visibility` none.
260. **Self-approval refused on every gate.** For each of the thirty gates, raise as one person and attempt to approve as the same person, on screen and over the protocol. Thirty refusals.
261. **Gate derived from amount.** Write-offs of ₱30,000, ₱75,000 and ₱150,000 land on gates 1, 2 and 3 with no choice offered. Purchase orders of ₱80,000 and ₱8,550,000 land on gates 4 and 5.
262. **Unassigned gate refuses.** Clear a gate's primary in the seed; submission refuses naming the gate.
263. **No alternate can be added** on gates 3, 7, 9, 18, 22, 27, 28, 29, 30 and 33, on screen or over the protocol.
264. **Six hard blocks, exact.** The Hard Blocks screen shows the six rows of F4.1 and nothing else; each is exercised by tests 5 to 10 of section 14.
265. **Hard block 6 on a fund request.** A fund request on a project with no contract refuses with the message of F4.5; a purchase order refuses; the project cannot leave setup.
266. **Hard block 1 is a file.** Mobilise above ₱2,000,000 with no certificate refuses; with a typed string refuses; with a file proceeds. Below the threshold proceeds without one.
267. **Sign-in grant.** Grant sign-in to a person; they sign in; "Signs In" shows; revoke; they cannot.
268. **Two console holders.** The second seat is filled; a third is refused.
269. **Actor on every audit entry.** Every entry shows the person; a search by person returns their entries.
270. **Unique numbers.** Two purchase orders on two projects never share a number.
271. **Manila time.** A record created at 13:10 Manila shows 13:10, not 05:10.
272. **Working days.** A permit filed on a Friday with a 90 working day default shows a date that skips weekends and the holiday table.
273. **Deep link.** Paste /projects/PRJ-2026-0001 in a new tab: the project opens.
274. **Search finds.** Search a purchase order number, a person, a message word: each opens.
275. **Notification inbox.** A mention creates exactly one notification for the mentioned person and it appears in their inbox.
276. **No literals.** Test 179 passes.

## Modules

277. **Party types are multi-valued.** One party is client and asset_owner; another is supplier with a currency of euro.
278. **Lease reference is per kilowatt-hour.** 480 kilowatt-peak shows 480 × 1,277 × 6.70 as the annual lease reference.
279. **Contingency is invisible to the client.** The client-facing document and export carry no contingency, cost or margin.
280. **Won seeds everything.** On won: project in setup with site and client, design package with nine deliverables, fourteen blocks with include flags, in one transaction.
281. **Percent is derived.** No screen has a typed percent; block and project figures follow activities and value weights.
282. **Toolbox is evidence.** A site report without a camera photograph or with typed attendees refuses.
283. **Pre-population.** Day two opens with day one's incomplete activities.
284. **Stock never negative.** Dispatch beyond on-hand refuses; a goods receipt increases stock at its location; a short receipt leaves in-transit and raises a discrepancy.
285. **Transfer gates by geography.** Laguna to Dumaguete at ₱5,000 is gate 25a; Laguna to Laguna site store at ₱120,000 is gate 25b; at ₱30,000 no gate.
286. **Permit to work is the Safety Officer's.** Any other person is refused on gate 28; no issue-immediately control exists.
287. **Quick Response form.** In an incognito window the site's form submits a near miss and a stop-work with no identity captured, and the stop-work pushes to the Safety Officer with mandatory acknowledgement.
288. **Unclassified is a state.** Registering lands unclassified; only gate 33 classifies; an unclassified document cannot govern.
289. **Progress claim works.** Create, gate 11, certify lower, both figures kept.
290. **Clear test data lists and refuses.** The action lists counts, requires the tenant name, and is refused once the cutover date is set. Not executed.

---
# PART H — MILESTONE ORDER AND REPORTING

| Milestone | Parts | Exit tests |
|---|---|---|
| 0 | Deliverable 0: the conformance checklist, every requirement in this message | — |
| 1 | Part F, with Part C section B (Google Drive) built inside it | Section 14 tests 1 to 30; 259 to 276 |
| 2 | M1, M2 | Section 14 pipeline and project tests; 277 to 280 |
| 3 | M3, M4 | Section 14 design and procurement tests; 281 |
| 4 | M5, M6, M7 | Section 14 site, permit, inventory and offline tests, including 169 to 172; 282 to 285 |
| 5 | M8 to M14 | Section 14 remaining module tests; 286 to 289 |
| 6 | Part X, Operations and Maintenance | 190 to 214 |
| 7 | Part C section A, Communication | 237 to 251; 252 to 258 if not already passed in milestone 1 |
| 8 | Part P, protocol scopes and migration import | 215 to 236 |
| 9 | Part I, interface, labels and usability | 244; a screen-by-screen abbreviation sweep reported as a list |
| 10 | Part D, the clear-test-data action, built and not run | 290 |

After each milestone: post the checklist rows for it marked done, the test results with any failure named, and any place where this message and the original instruction could not both be satisfied. Then continue to the next milestone without waiting. Stop only at the end of milestone 10, or when a requirement cannot be built without a decision that would change data already stored, in which case ask one question and state what you will do if there is no answer.

---
