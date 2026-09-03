# Test brief — Magnus operations platform, phase 1

You are testing a newly built operations platform on behalf of its owner, Karl Ivan Estadola, Chief Executive Officer of Magnus Renewable Tech Corp. The platform is open in the current tab, signed in as Karl, who is a console holder with every permission. Your job is to **populate it with the data below, exercise every module end to end, and report exactly what works, what fails, what is missing and what is untestable** — so the builder can be given a precise list of fixes.

**Platform:** https://magnus-solar-workspace-platform-446354.onhercules.app/
**Second account for this test:** `kidron.magnus@gmail.com` (person record: Kidron Magnus, Project Manager). This account is signed in on a **different browser that you cannot reach**. Never sign Karl out. For any step marked *as the Project Manager*, stop, tell Karl exactly what to do in the other browser (which screen, which button, which record), and wait for Karl to say it is done before you continue. If Karl is not available, do the step as Karl, expect refusals, and record it as *blocked — needs second account*. Before Phase 3, check Administration for the Project Manager account: it must be assigned to the Magnus tenant with the Project Manager role and linked to the Kidron Magnus person record. If it shows as pending, ask Karl to complete the assignment first.

---

## Ground rules — read every one

1. **Never invent a result.** If you did not see it, it is *not verified*. If a screen did not load, say so. A report that claims a pass you did not observe is worse than no report.
2. **Record before you move on.** After every step, note: what you did · what you expected · what happened · a screenshot if it differs. Keep a running log; the final report is built from it.
3. **Do not delete anything, and do not change configuration except where a step says to.** You may create test records freely. You may *attempt* forbidden actions where a step says to — the refusal is the test.
4. **Do not switch off, bypass or work around anything that refuses you.** A refusal is usually the platform working. Record it and continue.
5. **If a field is required and the data table does not give a value, use something plausible and note what you used.** Do not skip the record.
6. **Watch the terminology.** The platform must never show an abbreviation alone — *PIC*, *NCR*, *BOM*, *PTW*, *EPC*, *O&M*, *PO*, *kWp*, *LGU*, an ampersand for "and". Every time you see one, note the screen and the exact text. This is a finding, not a nitpick.
7. **Watch for anything that happens by itself.** This platform must do nothing while nobody is acting — no automatic escalation, no timer, no scheduled task, no auto-approval. If something changed that you did not cause, that is a serious finding: record what, where, and when.
8. **Do not take screenshots of, or record, anything that looks like a real password or token.**
9. When a step is impossible because the module does not exist, record *not built* and move to the next step. Do not stop.

---

## Phase 0 — Inventory (do this first, before creating anything)

Open every sidebar item in order and classify each as **real screen** (has forms, lists, actions), **placeholder** ("coming soon" or similar), or **broken** (error, blank, spinner that never resolves). For each real screen, list the buttons and forms it exposes in one line.

Then open **Administration** and record these counts exactly as displayed:

| Check | Expected |
|---|---|
| Approval gate rows | 30, none numbered 13 to 17, gate 34 present |
| Hard block rows | 6, with editable value on block 1 and **no enable or disable control** |
| System constants | 5 — Specific Yield 1,277 · Area Per Kilowatt Peak 7 · Lease Reference Rate 6.70 · Markup Major Equipment 115 · Markup Balance Of System 130 — each with an effective date |
| Tenants | 2 — Magnus and an invented test company |
| Console holders | Karl in the second seat; primary seat named or empty |
| Audit chain verification | a button or action that runs and reports *intact* |
| Agent sessions screen | present, probably empty |

Record the sidebar order you see. Expected: Dashboard · My Day · Pipeline · Projects · Design and Engineering · Procurement · Permits · Inventory · Manpower and Equipment · Safety · Operations and Maintenance · Documents · Messages · Finance · Human Resource · Payroll · Reports · Administration — eighteen items, nothing else.

---

## Phase 1 — Master data

### 1.1 Parties (organisations)

Create these under whatever screen holds parties, clients or suppliers. `party_type` may allow several values.

**Ten customers — replace the bracketed names with the real prospects before starting:**

| # | Legal name | Type | Province · Local government unit | Related party |
|---|---|---|---|---|
| C1 | `Calamba Agro Industrial Corporation` | client | Laguna · Calamba | no |
| C2 | `Lipa Cold Storage and Logistics Inc.` | client, asset_owner | Batangas · Lipa | no |
| C3 | `Sorsogon Provincial Hospital Foundation` | client | Sorsogon · Sorsogon City | no |
| C4 | `Dumaguete Bay Resort and Convention Center` | client, offtaker | Negros Oriental · Dumaguete | no |
| C5 | `Dasmariñas Plastics Manufacturing Corporation` | client | Cavite · Dasmariñas | no |
| C6 | `Legazpi Ice Plant and Fisheries Cooperative` | client | Albay · Legazpi | no |
| C7 | `Mandaue Furniture Exports Inc.` | client | Cebu · Mandaue | no |
| C8 | `Santa Rosa Motor Assembly Corporation` | client | Laguna · Santa Rosa | no |
| C9 | `Naga City Commercial Mall Holdings Inc.` | client | Camarines Sur · Naga | no |
| C10 | Magnus Energy Corp | client, asset_owner | Laguna · Biñan | **yes** |

**Three suppliers and two subcontractors:**

| Legal name | Type | Notes |
|---|---|---|
| SolarTech Distribution Philippines Inc. | supplier | currency PHP, categories: panels, inverters |
| Pacific Cable and Electrical Supply Corp. | supplier | currency PHP, categories: cabling, panel boards |
| Nordwind Energy GmbH | supplier | currency EUR — for the foreign-currency test |
| Bicol Roofworks Services | subcontractor | accreditation `accredited`; insurance expiry 6 months from today; **insurance exclusions: "injury to contractors' workmen"** |
| Visayas Solar Installers Cooperative | subcontractor | accreditation `provisional`; insurance expiry 45 days from today; exclusions: none |

Also add **Magnus Renewable Tech Corp** as a party if it does not already exist.

**Test while you are here:** on SolarTech, change the bank account details. Expect: the change is logged with before and after, and it either asks for a second person's confirmation or flags it. Record what actually happened.

### 1.2 Accounts, sites and contacts

For each of the ten customers create one account and one site (address in the province above, the local government unit above, distribution utility: Meralco for Laguna, Batangas and Cavite; SORECO for Sorsogon; NORECO for Dumaguete; ALECO for Albay; VECO for Cebu; CASURECO for Naga). Give C2 **two** sites — a second in Batangas · Tanauan — and confirm both attach to one account. One contact per account.

### 1.3 People and roles

Create these person records. None of them signs in yet except the Project Manager, whose email is the second account above.

| Full name | Population | Roles to assign | Signs in |
|---|---|---|---|
| Cristy Villanueva | office | Document Controller, Warehouse Lead | no |
| Jay Ramos | warehouse | Warehouse Custodian — Laguna | no |
| Bernie Cabrera | warehouse | Warehouse Custodian — Sorsogon | no |
| Paul Dela Cruz | warehouse | Warehouse Custodian — Dumaguete | no |
| Jeferson Tolentino | office | Permit Liaison Officer — Bicol | no |
| Austin Reyes | office | Permit Liaison Officer — Visayas | no |
| Alma Codog | office | Safety Officer | no |
| Roberto Santos | office | Head of Finance | no |
| Melanie Cruz | office | Procurement Head | no |
| Diego Fernandez | office | Director | no |
| **`Kidron Magnus`** | office | **Project Manager** | **yes — the second account** |
| Mario Bautista | field | Person In Charge | no |
| Six crew members: Ramon Aquino, Jun Mendoza, Erwin Castillo, Noel Garcia, Rey Salazar, Tonyo Villar | field | none — crew | **no** |

Record whether assigning a role raised an approval under **gate 24**, who it was addressed to, and whether Karl could approve it. Confirm that the six crew members have **no sign-in** and cannot be given one without changing a flag.

**Give Karl these additional roles for the duration of the test:** Director, Head of Finance, Procurement Head, Chief Operating Officer. The platform must accept multiple roles on one person. Record whether it did.

### 1.4 Locations

Confirm three warehouses exist — Laguna (Jay), Sorsogon (Bernie), Dumaguete (Paul). If they do not, create them.

---

## Phase 2 — Pipeline

Create ten opportunities, one per customer:

| Cust. | Site | Capacity kWp | Model | Estimated value ₱ | Take it to | Outcome |
|---|---|---|---|---|---|---|
| C1 | Calamba | 480 | sale | 28,800,000 | proposal → **won** | project P1 |
| C2 | Lipa | 1,000 | lease | 55,000,000 | proposal → **won** | project P2 |
| C3 | Sorsogon | 150 | sale | 9,600,000 | proposal → **won** | project P3 |
| C4 | Dumaguete | 250 | power purchase | 16,000,000 | proposal → **won** | project P4 |
| C5 | Dasmariñas | 60 | sale | 3,900,000 | proposal → **won** | project P5 |
| C6 | Legazpi | 320 | sale | 19,000,000 | proposal → **lost** | reason: price |
| C7 | Mandaue | 800 | lease | 45,000,000 | proposal → **lost** | reason: **client did not proceed** |
| C8 | Santa Rosa | 200 | sale | 12,500,000 | proposal → **lost** | **try with no reason first — must refuse above ₱10,000,000** — then reason: timeline |
| C9 | Naga | 100 | sale | 6,200,000 | negotiation | leave open |
| C10 | Biñan | 500 | sale | 30,000,000 | negotiation | leave open — related party |

**For C1 to C6, add a site assessment** before the proposal: roof type, usable area, a **structural confidence** value (make C3 `low`), tapping point details. Record whether structural confidence is a required field.

**Proposals — the gate tests are here:**
- C1: markup major equipment **115%**, balance of system 130% — policy. Release to client. Expect **gate 6** to fire, addressed to the Director on the project. Approve as Karl (he holds Director). Record who it was addressed to and whether approval succeeded.
- C2: major **112%** — within the Director's band. Expect gate 6 only, not gate 7.
- C3: major **108%** — below the band. Expect **gate 7**, addressed to the Chief Executive Officer, **with no alternate**. Karl is the Chief Executive Officer, so approve — but first note: did the platform refuse because Karl raised it himself? Record either way.
- C4 and C5: policy markup.
- On every proposal, enter a **contingency percentage** of 6. Then export or print the proposal in every way the screen offers and **confirm the contingency does not appear** anywhere client-facing.
- Mark C1 won. Then **try to edit the winning proposal** — expect refusal. Check that a project P1 now exists in `setup`, and that it **cannot be made active** — try it.

Record the pipeline views: by stage, by region, weighted value. Note any abbreviation.

---

## Phase 3 — Project and Contract (the raise steps are done by the Project Manager in the other browser)

For **P1 to P5**, as the Project Manager:

1. Open the project. Record: is there a `site_id` linking it to the pipeline site, or only a free-text address? Is there a **phase badge or a stored phase field**? (There must not be — stage should display as a distribution of block states.)
2. **Hard block 6 before the contract:** try to raise a purchase order on P1, and try to request funds on P1. Both must refuse with a message that names the missing contract, who can upload it, and **never says "you do not have permission"**. Record the exact message.
3. **Tick-box test:** fill in every contract field on P1 — value, dates, signatory, payment terms, retention 10% / turnover date / 12 months, **warranty 24 months** — but attach no document. Try to move the project to active. Must refuse.
4. Attach a signed contract document (any PDF you can upload — a one-page PDF you create is fine; name it "P1 signed contract"). Contract values: P1 ₱28,800,000 · P2 ₱55,000,000 · P3 ₱9,600,000 · P4 ₱16,000,000 · **P5 ₱1,900,000** (below the insurance threshold — deliberate).
5. **Risk terms:** eight clause families must exist, all `not_yet_read`. On P1 read four of them (mark present, one with an exposure flag) and leave four unread. Confirm the display distinguishes *not yet read* from *absent*.
6. **Project parties:** on P2 (lease) add the customer as client, host and offtaker, and Nordwind as nothing — confirm one party can hold several roles.
7. **Permit dependency:** P3 and P4 = **permit required before mobilisation**, expected 90 working days. P1, P2, P5 = not required.
8. **Counsel review, gate 10:** on P1 record that Atty. Caneja reviewed it. On P2 record *proceeded without review*. Confirm the two are stored as different outcomes, and that a query or list shows "contracts signed without counsel review" containing P2.
9. **Contract signature, gate 9:** ask Karl to request signature on each from the Project Manager browser. Then, as Karl in your browser, approve. Record whether gate 9 is shown with **no alternate**. Then, as Karl, **request signature on P5 yourself and try to approve it yourself** — expect refusal.
10. Move P1 to P4 to active. **Insurance, hard block 1:** on P1 (above ₱2,000,000) try to mobilise with no insurance certificate. Must refuse. Attach a certificate document (any PDF), then mobilise. On **P5** (below the threshold) mobilise without one — must be allowed.
11. **Variation order:** on P1 raise a variation of +₱1,200,000 affecting blocks B1 and B3. Expect gate 8. Approve. Mark it accepted by the client. Record whether contract value changed and whether the original contract is intact.
12. **Turnover date:** do not enter one yet.

Check the portfolio view: does the all-active total show five projects, total capacity, total value — and does it still show them when signed in as the Project Manager who is only assigned to some?

---

## Phase 4 — Design and Engineering (P1, P2, P3)

1. Open the design package for P1. It should already carry the site assessment data. Record whether the nine deliverables are listed by name.
2. Confirm every project has the block spine: B0 to B11, General Requirements, Battery Energy Storage System. **Try to add, rename or remove a block as Karl** — must refuse.
3. Add bill of materials lines, each **on a block**: P1 — B1: 900 panels at ₱9,500; B3: 4 inverters at ₱420,000; B2: 3,000 metres of direct current cable at ₱180; B5: 1 panel board at ₱650,000; B0: lifelines and catwalk at ₱380,000 lump. **Try to save a line with no block** — must refuse.
4. Mark the design deliverables through their states. Put one into `waiting` — it must demand **who** it is waiting on and stamp **when**. Set it waiting on the client.
5. Structural Assessment Certification on P3: record the outcome as **reinforcement required**. Expect a **variation order** to be raised, not a task.
6. Record whether block value weights are shown, whether General Requirements has weight zero, and whether they lock.
7. Record the professional seal fields — licence number, validity, professional tax receipt. Enter a licence expiry **earlier than today's date** on a sealed revision and see whether the design is flagged.

---

## Phase 5 — Procurement (P1)

1. The buying checklist must be **the bill of materials grouped by block**, not a separate list. Record what you see.
2. Raise a purchase order to SolarTech for the panels, value **₱8,550,000**. Expect **gate 5** (above ₱100,000), addressed to the Procurement Head. Approve as Karl. Then raise one to Pacific Cable for ₱80,000 — expect **gate 4**.
3. Move a line to `ordered` **without an expected arrival date** — must refuse. Then set a date 21 days out.
4. Raise an **off-design purchase** — 40 bags of cable ties, not on the bill of materials — a reason and a block must be required.
5. Raise one to Nordwind in EUR, €12,000 at a stated exchange rate. Record whether the rate and its date are captured.
6. **Goods receipt:** receive the panels at Laguna — 850 of 900, condition `short`. Expect: the line stays open with a balance, the block is *partially ready*, and a discrepancy is raised. Receive 4 inverters, condition **`damaged`**. Expect: quarantined. Then **try to issue those inverters to P1** — **hard block 5** must refuse, at every route you can find.
7. Record committed cost against the P1 block budget after the purchase orders — before any payment.

---

## Phase 6 — Blocks and site reporting (P1, then P5)

Do this as the Project Manager where possible, and note anything only a Person In Charge should be able to do.

1. **Hard block 2:** try to start B0 on P1 with no Construction Safety and Health Program approval recorded — must refuse. Record the approval (attach any PDF). Start B0.
2. **Hard block 3:** try to start B1 while B0 is not signed off — must refuse and be logged. Sign off B0. Start B1.
3. **Site reports, three consecutive workdays on P1**, Person In Charge Mario Bautista, weather clear / clear / rain with **work stopped by weather** on day 3:
   - Toolbox meeting on every report: topic, **a photograph** (use the capture control; if the only option is to pick a file from the device, record that as a finding — the specification forbids gallery upload), and **named attendees** — day 1: five of the six crew; day 2: all six; day 3: four.
   - Activities, each bound to a block: day 1 B0 40%, day 2 B0 60% and B1 5%, day 3 B1 blocked — reason `weather`.
   - **Try to save an activity with no block** — must refuse. **Try to submit a report without a toolbox meeting** — must refuse.
   - Record whether **day 2's report opened pre-populated** from day 1's incomplete activities and look-ahead.
4. Search the block and project screens for **any field where a person types a percentage complete**. There must be none. Record the derived percentage per block and for the project after day 2.
5. Raise a **non-conformance report** on P1 B1 with a photograph. Try to close it without evidence — must refuse. Close with evidence — expect **gate 19**.
6. On P5, file one site report, then enter a **turnover date**. Record whether retention, warranty and operations dates were derived from it with no second entry.

---

## Phase 7 — The remaining modules, one pass each

**Permits (P3, P4):** create the permit set for each. Confirm the same permit types appear for a 150 and a 250 kilowatt-peak project — no branching. File the building permit on P3 with no expected approval date — must refuse; then file — expect a default of 90 working days. On P4 move a permit to `additional_requirement` — expect a task raised, the requirement written to the library, and the date re-based. **Try to mobilise P3 with the prerequisite permit outstanding — hard block 4 must refuse.** Engage a permit consultant at ₱2,000 — expect gate 20 regardless of value.

**Inventory:** raise a transmittal Laguna → Dumaguete for 200 panels. Expect **gate 25a** regardless of value and an expected transit of 10 days. Issue it; record that Laguna decreased, in-transit increased, Dumaguete unchanged. Receive **180 of 200** at Dumaguete — expect a discrepancy to both custodians and the Procurement Head, and a stock adjustment awaiting **gate 26**. Raise a within-island transfer Laguna → the P1 site for ₱30,000 — expect **no gate**. Try to issue material with no block — must refuse.

**Manpower and Equipment:** raise a resource request on P1 B1 for 4 crew, needed from next Monday. Decline it with no reason — must refuse; decline with *no one available with this skill*. Create a deployment for Mario on P1; record whether planned, recorded and verified days are shown as three separate figures. Add one piece of equipment (a lifting rig) — the custodian must be a **person**, not a warehouse; try a location — must refuse. Enter a certification expiry in the past.

**Safety:** raise a permit to work, working at height, on P1 B1, naming two crew. Record whether it demands a same-day validity window. **Try to auto-approve, delegate or set a window on gate 28** anywhere in Administration — must not be possible. Give one crew member a lapsed capability and try to name them — must refuse. **Raise a safety stop on P1 B1**, then try to lift it as Karl — only the Safety Officer may; record what happened. **Open a private or incognito window** and find the per-site near-miss form — it must submit with no sign-in. Record the URL. Check that the three inspection routines exist as structured checklists with **empty item slots**, not invented content.

**Tasks (My Day):** create a task with no output type — must refuse. Create four tasks with different output types. Mark a fifth as priority when you already hold three priority items — must refuse. Move a task's date three times — record whether the original committed date is still shown and the recommit count reads 3. Put a task into blocked with no named blocker — must refuse. Look for any **hours or duration field** — there must be none. Check the load indicator is a **band**, not a number.

**Messages:** open P1 and post a message on the project thread, then on the B1 block thread, then on the SolarTech purchase order thread. Post one message mentioning the Project Manager. Ask Karl to check the Project Manager browser: **exactly one** notification, category Response, opening the object. Record what Karl reports. Post ten messages mentioning nobody — nobody should be notified. Look for any mute, watch or subscribe control — there must be none. Try to edit or delete a message — must refuse; hide should exist for an administrator. Attach a photograph on the block thread — the platform should offer to attach it to today's site report instead.

**Documents:** upload a drawing for P1, revision 1, classify it `controlled`, set it in force. Upload revision 2 and set it in force — revision 1 must show as superseded and link to revision 2. Upload a document and **leave it unclassified** — it must be viewable but **refuse to be attached to a work instruction**. Check the required-document register for P1 lists the signed contract and insurance certificate as satisfied.

**Finance:** for P1 create three billing milestones. Raise a progress claim — the percentage must be **the derived figure**, not typed. Expect gate 11. Record the claim, then enter a certified amount **lower** than claimed — both must be retained. Raise a **fund request on P5** — allowed, contract exists. Raise a write-off of ₱30,000 — gate 1; ₱75,000 — gate 2; ₱150,000 — gate 3 with no alternate. Open the cash forecast — every line must be `secured`, `gated` or `projected`, and every gated line must name a gate, an owner and an age.

**Human Resource and Payroll:** open Mario's record. Confirm **no salary, rating, disciplinary or medical field** is visible to Karl as console holder anywhere in Human Resource or Payroll. Enter a Social Security System contribution table row — expect it to sit `pending` until Finance approves. Open a payroll period covering the three P1 site days plus one day with no report — the register **must refuse to generate** and must not drop any worker. File the missing day, generate, and check `days_worked` for each crew member equals the toolbox days you recorded. Try to edit a computed statutory deduction on one line — must refuse.

**Operations and Maintenance:** create a service agreement on the **C6 site (Legazpi) — a site with no project**. Try to activate with no document — refuse. Attach one, add four service level terms (total outage 4h/24h, partial 8h/48h, degraded 24h/120h, cosmetic 72h/240h), fixed monthly ₱45,000, 24 months. Activate. Record: was `expiry_date` derived, and were **24 scheduled charges created at once**? Create a serviced asset on that site, 320 kilowatt-peak, and a work order, severity partial outage; move it to in progress and restored; record the response and restoration hours the platform computes. Raise a warranty claim against SolarTech **without a purchase order** — must refuse.

**Reports:** open every report. Each must state **what was checked and when**, even when empty. Record any report that is simply blank.

**Administration:** change a threshold with no reason — must refuse. Change the hard block 1 value from ₱2,000,000 to ₱2,500,000 — allowed, reason required. **Try to disable each of the six hard blocks** by every control you can find — must fail, and the attempt must appear in the audit log. Try to add a third console holder — must refuse. Run the audit chain verification. Open the read-only audit log and confirm your actions today appear with your name.

---

## Phase 8 — Cross-cutting checks

1. **Notification panel:** open it. Create an Information-category item if you can — the badge must not count it. Open a Task-category item and navigate away without doing it — the badge must not change.
2. **Search:** as the Project Manager, search for a project they are not assigned to. It must **not appear at all**.
3. **Deep links:** copy the URL of P1's B1 block and the SolarTech purchase order. Paste each into a new tab — it must open the exact record.
4. **Money visibility:** if a Person In Charge account exists in another browser, ask Karl to open P1's material list. No cost figure anywhere, including exports. If not, record *untestable in phase 1*.
5. **Nothing runs unattended:** note the time. Open the audit log, find the last entry, and record its timestamp. Return after your final step and confirm no entry was written by anything other than you or the Project Manager.
6. **Abbreviation sweep:** list every abbreviation you noted, with its screen.

---

## The report

Deliver one Markdown document, in this order:

1. **Top ten findings** — the ten most consequential things, each one sentence, ranked by how much of the specification they break or how much of the business they block.
2. **Inventory** — the phase 0 table and counts.
3. **Findings by module** — for each phase, a table: step · result (**pass** / **fail** / **not built** / **blocked — needs second account** / **not verified**) · what happened · screenshot reference. Failures carry exact reproduction steps.
4. **Things that happened by themselves** — anything from rule 7, or "none observed".
5. **Abbreviations found** — screen and text.
6. **Usability friction** — anything slow, unclear or that took more taps than it should, especially on the site report screen.
7. **Data created** — every record you made, with its name and identifier, so it can be found or cleaned up.
8. **Untestable in phase 1** — everything that needs a Person In Charge, Head of Finance, Safety Officer or Director account to prove.

Do not summarise a failure into a sentence that sounds like a pass. Do not round "mostly works" up. The builder will act on this report literally.
