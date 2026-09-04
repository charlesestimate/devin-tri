# Magnus Workspace Platform — open items register

**As at 4 September 2026.** This is the management view: everything outstanding,
who it waits on, and what it costs. It is the input to the milestone and
deliverables plan, not the plan itself.

---

## 1. Where things stand

Four build groups have been delivered. The **object layer is genuinely built** —
400 tools over the protocol, all dispatching, covering roughly the full section 8
object list including Operations and Maintenance. Google Drive is connected and
verified. Twenty-five roles are seeded. Five people can sign in.

The **control layer is not built**. Gates, hard blocks and approval routing exist
as tables with the right shape and the wrong contents. Nothing in the platform
currently refuses anything.

**Nothing has been sent to Hercules since Group 3 was built.** Everything below
is accumulated, not in progress.

---

## 2. Written but never delivered to Hercules

| # | Deliverable | State | Note |
|---|---|---|---|
| D1 | `CONSOLIDATED-FIX-PROMPT.md` — 27 conformance items | Written, reviewed, **not sent** | Groups 2 and 3 findings, priority-ordered |
| D2 | Interface and branding prompt | **Not written** | Requested 3 September: amber visibility cues matching the logo, MRTC and MEC logos, light theme |
| D3 | Account versus party correction | Folded into D1 item 18 | Nothing separate to send |

D1 is the one that matters. D2 needs drafting when the interface work is
scheduled — it is design work, not conformance, and mixing the two into one
prompt is how the conformance items get lost.

---

## 3. The register

Severity: **Blocker** — unsafe or misleading in use. **Major** — the platform
does not do what was specified. **Minor** — friction, no wrong outcome.

### A · Control layer *(all Blocker)*

| # | Item | Evidence |
|---|---|---|
| A1 | Gate chosen by the caller, not derived from amount | ₱150,000 write-off declared "minor" stored `gateId: "1"`; gate 3 is CEO-only |
| A2 | Gate rows carry no approver and no threshold | Fields are label, description, window, active, noAlternate only |
| A3 | Thirteen gate numbers point at the wrong action | Gates 8 and 9 swapped; gate 30 is payroll, should be incident closure |
| A4 | Recorded windows wrong on twelve rows | Gate 23 payroll should be 1 day |
| A5 | No write raises an approval request | Three existing requests, all `currentApprover: "unassigned"` |
| A6 | Purchase orders carry no gate | ₱500,000 PO stored with no gateId |
| A7 | Hard block 6 does not fire on purchase orders | PO raised against a project with an unsigned draft contract |
| A8 | Four of six hard blocks are not the specified ones | Insurance, DOLE programme and B0 sign-off all missing |
| A9 | Blocked-action message not built | No refusal to carry it |
| A10 | Hard block attempt log empty | Nothing has ever blocked |
| A11 | Permit to work issuable by a non-Safety Officer | Hot-work permit issued naming the CEO |
| A12 | Role assignment bypasses gate 24; duplicates accepted | Two live rows for the same person and role |
| A13 | Board pack shows no pending approvals | Section 8 requires count, age and window |
| A14 | `propose_decision` is free text, links to no object | Confirming changes nothing real |
| A15 | Self-approval checked per session, not per person | Two tokens, one person, R6 passes |

### B · Commercial chain *(Major)*

| # | Item |
|---|---|
| B1 | Winning an opportunity produces none of its four consequences |
| B2 | A won opportunity's proposal is still editable |
| B3 | An approved variation order does not move the contract value |
| B4 | Proposal state machine is not the specified one; `superseded` missing |
| B5 | `site_assessment` missing `structural_confidence` and eight structured fields |
| B6 | `account` still collapsed into `party` |

### C · Protocol and data hygiene *(Major to Minor)*

| # | Item | Severity |
|---|---|---|
| C1 | 63 of 80 enum parameters declare no enum; Convex stack traces reach clients | Major |
| C2 | No way to post into a record thread over the protocol | Major |
| C3 | `employmentBasis` accepts arbitrary strings | Major |
| C4 | A role's permissions cannot be changed, so gate 32 governs nothing | Major |
| C5 | Several list tools require a filter that should be optional | Minor |
| C6 | Test data from verification runs left in the platform | Minor |

All of A, B and C are written up as the 27 items in `CONSOLIDATED-FIX-PROMPT.md`.

### D · Not yet written as instructions

| # | Item | Severity | Why it is not in D1 |
|---|---|---|---|
| D-a | Interface and branding: amber visibility cues, MRTC and MEC logos, light theme | Major | Design work; needs its own prompt |
| D-b | Screens never verified against the current build | **Blocker for the pilot** | Needs a browser agent run, not a prompt |
| D-c | Code never reviewed | Major | Waits on the tar export |
| D-d | Chat and messaging never verified end to end in the browser | **Blocker for the pilot** | Your stated first priority; only the protocol side has been tested |

**D-b and D-d are the two that should be closed before the pilot group starts.**
Everything I have verified is over the protocol. I have never seen a screen. When
the browser agent last tested the interface it found it well behind what the
backend reported, so "the tool works" is not evidence the button works — and chat
is the whole reason the platform exists.

`CLAUDE-CHROME-TEST-BRIEF.md` can be pointed at the current deployment as-is. An
hour of that tells you whether the screens are ready for six people.

---

## 4. Waiting on you

| # | Decision | Blocks |
|---|---|---|
| K1 | Consolidated team role list | Creating the remaining roles in one pass |
| K2 | Roles for Christianah and Alfie — money visibility and record scope | Both still hold no role; permanent once set |
| K3 | Should Vice President for Sales hold gate 6 (quotation release)? | Currently flagged approver but named in no gate |
| K4 | The pilot group — roughly six names and email addresses | Granting sign-in |
| K5 | Tar export to GitHub | Code review, and a restore point |
| K6 | When to send D1 to Hercules | Everything in A, B and C |

## 5. Waiting on the team

| # | Action | Who |
|---|---|---|
| T1 | Sign in once so the identity link activates | Beda, Christianah, Alfie |
| T2 | Read the pilot ground rules before touching the platform | Pilot group |
| T3 | Attach the two DOCX handovers to the Gmail drafts and send | You |
| T4 | Pilot feedback in the five-line format | Pilot group |

---

## 6. What I cannot see

Stated plainly so it is never assumed otherwise.

- **The screens.** Everything verified here is over the Model Context Protocol.
- **The source code.** Every finding is black-box: I can prove a hard block does
  not fire because a project walked past it; I cannot say why without the code.
- **Whether one bug or twelve.** The control-layer failures may share a single
  root cause or be independent. That changes the size of the next milestone
  materially, and the tar export is what settles it.

---

## 7. How this becomes the plan

When the pilot feedback is in and the tar is exported, three inputs combine:

1. This register — what is specified and not built.
2. Pilot feedback — what is built and does not fit the work.
3. Code review — how deep the control-layer failures actually go.

Those three become the milestones. My current reading, subject to the code:

- **Milestone A — make refusal real.** Register section A. Until this lands the
  platform cannot be a system of record for anything involving money or safety.
- **Milestone B — the commercial chain.** Register section B.
- **Milestone C — interface, branding and whatever the pilot returns.** D-a plus
  feedback.
- **Milestone D — hygiene and migration readiness.** Register section C, then the
  twenty-five-sheet import.

Milestone A is not negotiable in ordering. Everything else can be sequenced
around what the pilot says hurts most.
