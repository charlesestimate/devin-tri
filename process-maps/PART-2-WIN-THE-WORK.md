# Part 2 of 10 — Win the Work: Pipeline to Contract

**Level-1 cross-functional map · as specified · 8 September 2026**
**Companion files:** `Part 2 — Win the Work (A3 landscape).pdf` and `.svg` in the same folder

---

## 1. What this process is for

To take an enquiry from a prospective client to a **signed contract and a project that is
allowed to leave setup** — with the company's two commercial controls applied on the way: an
internal review before a proposal leaves the building, and a won decision before a project exists.

**Starts:** a Sales role creates an account.
**Ends:** the platform advances the project from `setup` to `design`, which it will only do once a
signed contract is attached — hard block 6. Part 3 begins there.

Every step below names the record it moves and the state it leaves it in. All states are values
the schema permits; all transitions are mutations that exist in the code.

---

## 2. Lanes in this map

| Lane | Roles | Why they are here |
| --- | --- | --- |
| **Client** | The customer | Grants site access, reviews and accepts the proposal, signs the agreement. Drawn dashed: outside the company |
| **Executive** | Director · Chief Operating Officer · Chief Executive Officer | Holds all four gates in this part |
| **Sales and Pipeline** | Account Manager · Sales Engineer · Account Officer · Business Development Officer · Vice President for Sales | Responsible for every step from account to won |
| **Projects and Site** | Project Manager | Takes over at contract |
| **The Platform** | — | Creates the project, freezes the proposal, seeds the risk terms, and enforces hard block 6 |

---

## 3. The steps

| # | Lane | Action | Record → state | Gate · A · C · window | Block | Deviation today |
| --- | --- | --- | --- | --- | --- | --- |
| 2.1 | Sales | Create account, contact and site | `parties` · `contacts` · `sites` | — | — | Site accepts negative area and voltage (1-11) |
| 2.2 | Sales | Create opportunity | `opportunities` → `prospect` | — | — | |
| 2.3 | Sales | Start assessment | `opportunities` → `assessing` | — | — | |
| 2.4 | Client | Grants site access, shares load data | — | — | — | |
| 2.5 | Sales | Record site assessment | `site_assessments` → `proceed` · `proceed_with_conditions` · `do_not_proceed` | — | — | Accepts a future assessment date (1-09) |
| 2.6 | Sales | **Proceed?** | decision | — | — | |
| 2.7 | Sales | Mark lost or on hold | `opportunities` → `lost` · `on_hold` | — | — | |
| 2.8 | Sales | Create proposal — cost build-up, markups, contingency, yield | `proposals` → `draft` · `opportunities` → `proposing` | — | — | Annual lease figure multiplies roof area by a per-kilowatt-hour rate — out by ~182× (§3.3 of the sweep analysis) |
| 2.9 | Sales | Submit for internal review | `proposals` → `submitted_for_review` · `approval_requests` → `pending` | **G6** raised | — | |
| 2.10 | Executive | Review proposal: approve or reject | `proposals` → `approved_internal` · `rejected_internal` | **G6 · Director · COO · —** | — | **RC-A** the raiser can approve their own request |
| 2.11 | Sales | Send to client | `proposals` → `sent_to_client` | — | — | No confirmation; one mis-click sends a commercial document (1-20) |
| 2.12 | Client | Reviews, negotiates, accepts or declines | `proposals` → `under_negotiation` → `accepted` · `declined` | — | — | |
| 2.13 | Sales | Submit for won decision | `opportunities` → `negotiating` · `approval_requests` → `pending` | **G7** raised | — | **Register:** G7 is specified as *markup more than five points below policy* — a conditional gate. The code raises it on every won decision |
| 2.14 | Executive | Decide won | `opportunities` → `won` · or back to `proposing` | **G7 · Director · — · —** | — | **RC-A** |
| 2.15 | Platform | **Automatic:** project created, proposal frozen, eight risk terms seeded | `projects` → `setup` · `proposals` → `frozen` · `risk_terms` × 8 → `not_yet_read` | — | — | |
| 2.16 | Projects | Create contract — type, value, retention, warranty | `contracts` → `draft` | — | — | Contract record stays `draft` forever; nothing on the Contract tab can sign it (1-14) |
| 2.17 | Client | Signs the agreement | — | — | — | |
| 2.18 | Projects | Attach signed contract document and date | `projects.contractSignedAt` set | **G9 · CEO · — · —** | — | **G9 is specified but no code raises it.** Signed date accepts 31 December 2027 and immediately unlocks the setup gate (1-08) |
| 2.19 | Projects | Acknowledge the eight risk terms; contract risk review | `risk_terms` → `acknowledged` · `accepted` · `rejected` | **G10 · Director · COO · —** | — | **G10 is specified but no code raises it.** The schema carries a `riskReviewOutcome` (approved · proceeded without review · rejected) that nothing sets. Terms display no text, so acknowledgement is uninformed (1-23) |
| 2.20 | Projects | Assign project parties — ten seat roles from Project Manager to Client Representative | `project_parties` | — | — | `assignProjectParty` exists as a mutation; **no control in the interface** (1-04) |
| 2.21 | Platform | **Automatic:** advance from setup | `projects` → `design` | — | **HB6** no signed contract, project cannot leave setup | Enforced. But the *live* HB6 row describes a different rule (RC-N); the enforcement here is a stage check, not the named block |

---

## 4. The RACI

One **A** per step. Where a step has a gate, A is the gate's primary approver and C its alternate.
Where it has none, A is the role that owns the record. **I** is who the specification intends to be
told — and nobody is told today (RC-H).

| Step | Sales role | VP Sales | Director | COO | CEO | Project Manager | Head of Finance | Client |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.1 Account, contact, site | **R / A** | I | | | | | | |
| 2.2 Opportunity | **R / A** | I | | | | | | |
| 2.3 Start assessment | **R** | **A** | | | | | | I |
| 2.4 Site access | | | | | | | | **R** |
| 2.5 Site assessment | **R** | **A** | | | | C | | |
| 2.6 Proceed? | **R** | **A** | | | | | | |
| 2.7 Lost / on hold | **R** | **A** | I | | | | | |
| 2.8 Create proposal | **R** | **A** | | | | C | C | |
| 2.9 Submit for review | **R** | I | I | | | | | |
| 2.10 Review proposal (G6) | I | I | **A** | C | | | | |
| 2.11 Send to client | **R** | **A** | I | | | | | **I** |
| 2.12 Client decision | I | I | | | | | | **R** |
| 2.13 Submit for won | **R** | I | I | | | | | |
| 2.14 Decide won (G7) | I | I | **A** | | | I | I | |
| 2.15 Project created | I | | | | | **I** | I | |
| 2.16 Create contract | | | | | | **R / A** | C | |
| 2.17 Client signs | | | | | | I | | **R** |
| 2.18 Attach signed contract (G9) | | | | | **A** | **R** | I | |
| 2.19 Risk terms and review (G10) | | | **A** | C | | **R** | | |
| 2.20 Project parties | | | I | | | **R / A** | | |
| 2.21 Advance from setup | | | | | | I | I | |

**Reading the matrix.** Sales is Responsible for fourteen of the twenty-one steps and never
Accountable for money — the Vice President for Sales is, until a gate hands accountability to the
Director. The Director is Accountable on three of the four gates. The Chief Executive Officer
appears exactly once, on the signed agreement, which is the one commercial act the specification
reserves for the top of the company. The Project Manager takes over at 2.16 and is not consulted
before it, except on the assessment and the proposal — the two places where what is promised
becomes what must be built.

---

## 5. Hand-offs — where this process stalls

| From → To | At step | What crosses | What stalls it |
| --- | --- | --- | --- |
| Client → Sales | 2.4 → 2.5 | Site access and load data | The client. The assessment cannot be recorded without a visit |
| Sales → Executive | 2.9 → 2.10 | A proposal awaiting review | **Nobody is told** the request exists (RC-H). The approver finds it only by opening the record |
| Executive → Sales | 2.10 → 2.11 | An approved proposal | Same |
| Sales → Client | 2.11 → 2.12 | The proposal | The client's own timeline. `under_negotiation` is the holding state |
| Sales → Executive | 2.13 → 2.14 | A won decision | Same as 2.9 |
| Platform → Projects | 2.15 → 2.16 | A new project in setup | The Project Manager is not told a project exists (RC-H) |
| Projects → Client | 2.16 → 2.17 | The contract | The client's signature |
| Client → Projects | 2.17 → 2.18 | The signed agreement | The physical document reaching whoever attaches it |

Four of the eight hand-offs stall on the same cause: nothing tells the next person. That is why
the approvals inbox is the first item of the next fix prompt.

---

## 6. Where the live build differs from this map

| | Deviation | Step | Reference |
| --- | --- | --- | --- |
| 1 | The raiser can approve their own proposal review and won decision | 2.10, 2.14 | RC-A |
| 2 | **Gate 7 is raised on every won decision.** The specification's gate 7 is *markup more than five points below policy* — meant to fire only when a proposal undercuts policy, not on every deal | 2.13 | Register |
| 3 | **Gate 9 — signed customer agreement, Chief Executive Officer — is specified but nothing raises it.** A signed contract is attached with no approval at all | 2.18 | Register |
| 4 | **Gate 10 — contract risk review, Director — is specified but nothing raises it.** The schema has the outcome field; nothing sets it | 2.19 | Register |
| 5 | Project parties: the mutation exists, the control does not | 2.20 | 1-04 |
| 6 | A contract signed date of 31 December 2027 is accepted and unlocks the setup gate | 2.18 | 1-08 |
| 7 | A site assessment dated 2027 is accepted | 2.5 | 1-09 |
| 8 | Risk terms have no text; all eight can be acknowledged with one click each | 2.19 | 1-23 |
| 9 | Send to Client has no confirmation dialog | 2.11 | 1-20 |
| 10 | The contract record reads `draft` permanently; only the project header knows it was signed | 2.16 | 1-14 |
| 11 | The proposal's annual lease figure multiplies square metres by a per-kilowatt-hour rate | 2.8 | sweep §3.3 |
| 12 | Nobody is notified at any hand-off | all | RC-H |

**What this means for the register decision.** Of the four gates the specification places in this
part, the code enforces two — and one of those two it enforces on the wrong condition. Gates 9 and
10 are the two that guard the contract, and today the contract is the least-controlled step in the
process: a date typed into a box unlocks everything downstream. Whichever register you choose,
these two gates need to exist in code.

---

## 7. What is deliberately not in this part

- **The proposal's arithmetic** — markups, contingency, yield, lease. It is a calculation, not a
  process step. Its one defect is noted at 2.8.
- **Variation orders.** They belong to the contract but happen during construction; they are in
  Part 6 with the rest of the money.
- **Messages on the opportunity or project.** A channel, not a step.
- **The register conflict itself.** Stated once in Part 0; marked where it bites here.
