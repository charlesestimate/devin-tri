# Part 10 of 10 — The consolidated register

**8 September 2026 · four Google Sheets in the same Drive folder**

| Sheet | What is in it |
| --- | --- |
| **Part 10 — Registers** | Read me · Gate register (30 gates: specified label, live label, specified and live approvers, which modules name it, whether it is in code) · Hard blocks (6, specified against live) · Roles live (32) · People live (66) |
| **Part 10 — Consolidated RACI** | 172 steps from Parts 2 to 9 against 30 roles |
| **Part 10 — Deviations register** | 106 numbered deviations, by part, with step and reference |
| **Part 10 — Process steps and hand-offs** | 147 steps with record, state and gate · 56 hand-offs between lanes |

Everything is derived mechanically from two sources: the `convex/` source export of
8 September 2026, and the live platform read over the Model Context Protocol the same day.

---

## What the register shows that no single part could

**Thirty gates are specified. Five raise an approval request in code: 6, 7, 18, 24 and 34.**
Seventeen record an approval without the engine. Five name an act the code performs without
ever naming the gate. Three have no record of the act at all — gate 9 (signed customer
agreement), gate 12 (retention invoice), gate 27 (opening stock lock).

**Nothing outside `convex/foundation/gates.ts` ever calls `approveRequest`, `rejectRequest`
or `checkGateAuthorisation`.** A scan of every file in the backend returns zero callers. The
live `approval_requests` table contains gates 6, 7, 24 and 34 and nothing else — exactly what
the code predicts, which is the strongest confirmation in the series that the reading is right.

**Twenty-five of the thirty live gate labels differ from `seed.ts`.** Five agree: gates 18, 22,
26, 33 and 34.

**All six live hard blocks carry a different label and a different meaning from the six the
specification names.** The specification's block 3 depends on a block B0 that does not exist in
the construction spine.

**Thirty-two roles exist; seven are held by nobody.** Sixty-six people; the People tab shows
which hold no role and which single role grant carries a gate 24 approval.

---

## How to use it on Monday

1. Open **Registers → Gate register**. Sort on the "In code" column. The three rows reading
   *No code — no record of this act at all* are missing capability, not missing wiring.
2. Filter the same tab on *Approval recorded without the engine* — seventeen rows. That is the
   Monday instruction from Part 8, with the list attached.
3. Open **Deviations register** and filter Reference on `RC-A`. Every one of those closes when
   the seventeen rows above route through `foundation/gates.ts`.
4. **Registers → Gate register**, "Live primary" column: the five empty rows are gates 22, 24,
   31, 32 and 33. Filling them is an afternoon on a screen that already exists, and it is the
   single highest-value hour in this whole series.

---

## What this series established

- The platform has **two things that are finished and correct**: the gate engine in
  `foundation/gates.ts`, and the hash-linked audit chain with its verifier.
- It has **three registers that disagree** — `seed.ts`, the live rows, and each module's own
  comment — and eleven gate numbers mean something different depending on which you read.
- The **authority model is a convention, not a control**: 56 role grants, one gate 24 approval,
  and that one raised and approved by the same person.
- The **irreversible operation is the ungated one**: cryptographic erasure needs a non-blank
  reason and nothing else.

**Next: `PROMPT-MONDAY.md`, reshaped by Parts 8, 9 and 10.**
