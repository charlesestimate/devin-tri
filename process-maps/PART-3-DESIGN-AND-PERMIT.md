# Part 3 of 10 — Design and Permit

**Level-1 cross-functional map · as specified · 8 September 2026**
**Companion files:** `Part 3 — Design and Permit (A3 landscape).pdf` and `.svg` in the same folder

---

## 1. What this process is for

Two chains run in parallel from the moment a project leaves setup.

**The design chain** turns an approved sale into a package a crew can build from: deliverables drawn,
sealed by a licensed engineer, reviewed, frozen, and released as **issued for construction**. The
bill of materials falls out of it, and Part 4 buys from that.

**The permit chain** identifies what the site legally needs, gathers the requirements, submits to the
authority, and holds the approved permit that **mobilisation will check for** in Part 5.

**Starts:** the project is in `design`.
**Ends:** a design package at `issued_for_construction` with a bill of materials, and a permit at
`approved`. Neither chain waits for the other, but construction cannot begin without both.

---

## 2. Lanes in this map

| Lane | Roles | What they do here |
| --- | --- | --- |
| **External Authorities** | Distribution utility · local government · Professional Regulation Commission | Decide the permit. Drawn dashed: outside the company |
| **Executive** | Chief Operating Officer · Director · Design Engineer as gate holder | Two gates: the design freeze and the permit consultant |
| **Engineering** | Design Manager · Design Engineer · Process Engineer | Responsible for the whole design chain |
| **Administration and Permits** | Permit Liaison · Document Controller | Responsible for the whole permit chain |
| **Projects and Site** | Project Manager | Receives both outputs; mobilisation depends on them |
| **The Platform** | — | Releases the package once the freeze is approved, and accumulates the requirement library |

---

## 3. The design chain

| # | Lane | Action | Record → state | Gate | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 3.1 | Engineering | Create design package — one of ten disciplines | `design_packages` → `draft` | — | |
| 3.2 | Engineering | Work the package | → `in_progress` | — | |
| 3.3 | Engineering | Add deliverables — nine types, from layout plan to commissioning checklist | `design_deliverables` → `draft` | — | |
| 3.4 | Engineering | Record professional seal — engineer, licence, expiry, discipline | `professional_seals` | — | Recorded, then **never displayed back**. No badge on the deliverable, and a second contradictory seal can be added on top (2-13) |
| 3.5 | Engineering | Issue for review | → `issued_for_review` | — | |
| 3.6 | Engineering | Deliverable review | `design_deliverables` → `in_review` → `approved` | — | A deliverable can go **straight from draft to approved** by the person who drew it. `in_review` can be skipped and no reviewer is named (2-06) |
| 3.7 | Engineering | Issue for approval | → `issued_for_approval` | — | |
| 3.8 | Engineering | Submit design freeze | `approval_requests` → `pending` | **G18** raised | Refused unless the package is at `issued_for_approval` — a correct precondition |
| 3.9 | Executive | Approve the design freeze | `approval_requests` → `approved` | **G18 · Design Engineer · — · —** | **RC-A** the raiser can approve their own request |
| 3.10 | Platform | **Automatic:** package released | → `issued_for_construction` | — | **This is the one gate fully enforced in the product.** `updateDesignPackage` refuses to set `issued_for_construction` without an approved gate 18 |
| 3.11 | Engineering | Bill of materials — seven categories | `bill_of_materials_lines` | — | Item code is free text, not a picker from the catalogue. Nothing checks a line against stock on hand (2-02) |

**Worth stating plainly: gate 18 works.** Of the thirty gates in the specification, this is the first
I have found that is raised, checked, and enforced end to end — the package cannot reach issued for
construction by any route without an approved design freeze. It is the model the other gates should
follow.

**One correction to an earlier finding.** Last week's sweep reported that the platform has no
"issued for construction" status. That was about **deliverables**, whose six statuses end at
`approved`. **Packages do have it**, and it is the gated end state of this chain. The gap is real but
narrower than reported: it is the individual drawing that cannot be marked as the one to build from,
not the package.

---

## 4. The permit chain

| # | Lane | Action | Record → state | Gate | Deviation today |
| --- | --- | --- | --- | --- | --- |
| 3.12 | Administration | Maintain the permit type library | `permit_types` | — | A negative default duration is accepted, so a permit type can expire before it is issued (1-17). The library ships empty, so every customer types the same Philippine permit set from memory (2-28) |
| 3.13 | Administration | Raise a project permit | `project_permits` → `draft` | — | |
| 3.14 | Administration | Set requirements from the library | `project_permit_requirements` → `open` | — | |
| 3.15 | Platform | **Automatic:** requirement observed — the library accumulates | `permit_requirements.timesObserved` | — | The raw field name `timesObserved` is printed to the user (1-18). **The behaviour is correct** — this is L5, accumulate rather than maintain — only the wording is wrong |
| 3.16 | Administration | Requirements ready | → `requirements_set` | — | Refused unless the permit is in `draft` |
| 3.17 | Executive | Engage a permit consultant | — | **G20 · COO · Director · —** | **G20 is specified but no code raises it anywhere.** The only occurrence of gate 20 in the whole codebase is the seed definition |
| 3.18 | Administration | Submit to the authority | → `submitted` | — | |
| 3.19 | External | The authority decides | → `approved` · `rejected` | — | |
| 3.20 | Administration | Record the decision | → `approved` · `rejected` | — | |
| 3.21 | Administration | Close the permit | → `closed` | — | Correctly refused unless the permit is approved |
| 3.22 | Projects | The approved permit is what mobilisation checks for | `project_permits` at `approved` | — | **HB4 fires in Part 5, not here** |

**A correction to Part 0.** The plan listed hard block 4 as belonging to this part. It does not. HB4
— *prerequisite permit required before mobilisation* — is checked at mobilisation, which is Part 5.
What Part 3 produces is the record HB4 looks for. The map shows it at 3.22 as a hand-off, not as a
block in this process.

---

## 5. The RACI

| Step | Design Engineer | Design Manager | Permit Liaison | Doc Controller | COO | Director | Project Manager | Authority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.1 Create package | **R** | **A** | | | | | I | |
| 3.2 Work the package | **R** | **A** | | | | | | |
| 3.3 Add deliverables | **R** | **A** | | | | | | |
| 3.4 Professional seal | **R / A** | C | | I | | | I | |
| 3.5 Issue for review | **R** | **A** | | | | | | |
| 3.6 Deliverable review | C | **R / A** | | | | | | |
| 3.7 Issue for approval | **R** | **A** | | | | | I | |
| 3.8 Submit design freeze | **R** | I | | | | | I | |
| 3.9 Approve freeze (G18) | **A** | C | | | | | I | |
| 3.10 Package released | I | I | | I | | | **I** | |
| 3.11 Bill of materials | **R** | **A** | | | | | C | |
| 3.12 Permit type library | | | **R / A** | C | | | | |
| 3.13 Raise project permit | | | **R / A** | | | | I | |
| 3.14 Set requirements | | | **R / A** | C | | | | |
| 3.15 Library accumulates | | | I | I | | | | |
| 3.16 Requirements ready | | | **R / A** | | | | I | |
| 3.17 Engage consultant (G20) | | | **R** | | **A** | C | I | |
| 3.18 Submit permit | | | **R / A** | | | | I | **I** |
| 3.19 Authority decides | | | I | | | | I | **R** |
| 3.20 Record decision | | | **R / A** | I | | | **I** | |
| 3.21 Close permit | | | **R / A** | | | | I | |
| 3.22 Permit available to mobilisation | | | I | | | | **R / A** | |

**Reading the matrix.** The two chains barely touch. Engineering is Responsible for eleven steps and
never consults Administration; the Permit Liaison is Responsible for eight and never consults
Engineering. **The Project Manager is the only role Informed on both** — and is the person who
cannot mobilise until each has finished. That is the structural risk in this part: two independent
chains, one shared deadline, and no step where they check each other.

The Design Engineer is Accountable for the gate on their own department's work (G18). That is
deliberate in the specification — the design freeze is an engineering judgement, not a commercial
one — but it is also why the same-person guard matters more here than almost anywhere else.

---

## 6. Hand-offs

| From → To | At step | What crosses | What stalls it |
| --- | --- | --- | --- |
| Engineering → Executive | 3.8 → 3.9 | A design freeze awaiting approval | Nobody is told (RC-H) |
| Platform → Procurement | 3.11 → Part 4 | The bill of materials | Nothing. Part 4's purchase order links to a bill of materials line and auto-fills from it — one of the better joins in the product |
| Administration → Executive | 3.16 → 3.17 | A consultant engagement decision | The gate does not exist, so in practice this step is skipped entirely |
| Administration → Authority | 3.18 → 3.19 | The permit application | The authority's own timeline. There is no expected-decision date on the record |
| Authority → Administration | 3.19 → 3.20 | The decision | Someone remembering to check |
| Both chains → Projects | 3.10, 3.22 → Part 5 | An issued-for-construction package and an approved permit | Either one being late. **Mobilisation needs both** |

---

## 7. Where the live build differs from this map

| | Deviation | Step | Reference |
| --- | --- | --- | --- |
| 1 | **G20 permit consultant is specified and never raised.** Its only appearance in the codebase is the seed row | 3.17 | Register |
| 2 | A deliverable goes draft → approved with no reviewer named | 3.6 | 2-06 |
| 3 | A professional seal is recorded and never displayed; a second can be layered on top | 3.4 | 2-13 |
| 4 | The bill of materials item code is free text, disconnected from the catalogue and from stock | 3.11 | 2-02 |
| 5 | Permit types accept a negative default duration | 3.12 | 1-17 |
| 6 | The permit type library ships empty | 3.12 | 2-28 |
| 7 | `timesObserved` is printed to the user | 3.15 | 1-18 |
| 8 | The raiser can approve their own design freeze | 3.9 | RC-A |
| 9 | No file can be attached to a deliverable or a permit — the only upload in the product is the chat composer | 3.3, 3.14 | 2-09 |
| 10 | Nobody is notified at any hand-off | all | RC-H |

**What stands out.** This part has the healthiest control in the platform and one of the weakest side
by side. Gate 18 is fully enforced. Gate 20 does not exist. And the deliverable — the actual drawing
a crew builds from — can be approved by its author, carries a seal nobody can see, and has no file
attached to it.

---

## 8. What is deliberately not in this part

- **Mobilisation and hard block 4.** The permit is produced here; the block fires in Part 5.
- **Purchasing from the bill of materials.** Part 4.
- **Document register and revision control.** Part 9 — the design deliverable and the controlled
  document are two different records today, which is itself a finding recorded there.
- **As-built.** A package status this part can reach, but the work happens at handover in Part 8.
