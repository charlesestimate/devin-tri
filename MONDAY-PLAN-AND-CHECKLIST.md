# Monday to Tuesday — the plan, the checklist, and what to tell sixty-three people

**Written:** 5 September 2026 · **Verified against:** the source export and data snapshot you
uploaded today, not the older ones
**Monday 7 September:** fix · **Tuesday 8 September:** onboarding

---

## 1. Where things actually stand

I re-checked all nine code findings against the export you just sent. **Nothing has been fixed and
every line reference still holds** — `ProgressClaimsTab.tsx:60` and `finance.ts:12` are exactly
where they were; there is still exactly **one** self-approval check in the entire codebase; there is
still **no error boundary anywhere**.

From the data snapshot, the facts that shape this plan:

| | |
| --- | --- |
| People already onboarded | **63 persons** |
| Projects | 7 — five in design signed 3 Sep, **PRJ-2026-0006** (the test one, contract dated **31 Dec 2027**), and **PRJ-2026-0041** |
| Test records left by the two agents | **87 records across 45 tables** |
| Statutory rate tables | **all four approved, all four fake** |
| Payroll periods | PAY-2026-001 open · **PAY-2026-002 approved**, 16–30 Sep, sitting at Disburse |

**On PRJ-2026-0041** — 2nd_AI asked whether it was a real job. From the snapshot it has **no signed
contract**, was created 4 September, and carries the same client and capacity as PRJ-2026-0001. It
looks like a duplicate created during protocol testing, including my own. **Confirm before anyone
deletes it**, but I do not believe it is a live Calamba job.

**On the rate tables** — this is the sharpest thing in the snapshot:

| Table | Effective | Expires | Real? |
| --- | --- | --- | --- |
| SSS | **1 Jan 2026** | **never** | No — "test values, not official" |
| PhilHealth | 16 Sep 2026 | 30 Sep 2026 | No — flat ₱1.00 |
| Pag-IBIG | 16 Sep 2026 | 30 Sep 2026 | No — flat ₱1.00 |
| Withholding tax | 16 Sep 2026 | 30 Sep 2026 | No — flat ₱1.00 |

The danger window is **precisely 16–30 September**, because that is the only fortnight in which all
four are simultaneously in force — and **PAY-2026-002 is approved for exactly that period.** Outside
it, payroll is blocked for want of an approved table, which is safe but will confuse whoever tries.

---

## 2. The shape of Monday

One prompt, fourteen items, all verified. It is deliberately smaller than the full defect list because
**you have one day and you cannot publish something large the night before sixty-three people
arrive.**

| | |
| --- | --- |
| **Part A — protects money** | Self-approval **recorded, not blocked**, with a switch to block it later · gate derived from amount, not chosen · five validations that let impossible things through |
| **Part B — small repairs** | Progress claims (one line) · Philippine-time dates · error boundary · safety stop without a project · video attachments |
| **Part C — before Tuesday** | Delete-by-prefix tool · screen refreshes after a write · remember the selected project · the gate count |
| **Part D — the boundary** | What the assistant may read, may change under your approval, and may never touch |
| **Part E — the backup** | The export already exists and **silently misses twenty-two tables, including every message ever sent.** Fix the list, report per-table counts, add a read-only verify |
| **Part F — the phone** | Four one-line faults: touch targets below the minimum, the picker that overflows five modules, Payroll's unscrollable tabs, and **Raise Stop clipped off the screen** |

Each is independently verifiable, so if Hercules runs out of time you can still publish the ones
that landed.

---

## 3. Checklist — only you can do these

### Before you prompt (fifteen minutes)

- [ ] **Confirm PRJ-2026-0041 is not a live job.** If it is, say so and I will scope the cleanup
      around it.
- [ ] **Do not press Disburse on PAY-2026-002.** It is approved and one click from paying on fake
      rates.
- [ ] Nothing to decide. Self-approval ships **permitted and recorded**; the switch to block it is
      built and set to `record`, so turning it on later is one action, not another round of work.

### After Hercules publishes (thirty minutes)

- [ ] Work section 15 of the prompt yourself. It is fourteen checks and each one is a single action.
- [ ] **On your own phone**, press Raise Stop on Safety and open Statutory Rate Tables on Payroll.
      Those two are what the field crews meet on day one.
- [ ] **Take a backup Tuesday morning, before anyone signs in**, and run Verify on it. That file is
      your clean starting point — the one you can always go back to.
- [ ] Check the Board Pack shows a **self-approval counter**. That number is the only thing that
      tells you later whether the practice stayed rare or became the norm.
- [ ] **Run the delete-by-prefix tool in preview for `Z1-` and `Z2-`.** Read the list before you
      confirm it. 87 records; the audit entries stay and that is correct.
- [ ] Check PRJ-2026-0006 is gone with them. It is the test project carrying the 2027 contract, the
      ₱99M milestone and ₱10M of write-offs.

### Payroll — do this before 16 September, not before Tuesday

- [ ] Enter and approve genuine **SSS, PhilHealth, Pag-IBIG and withholding tax** tables. Approving
      a new one supersedes the old, which is the only way to remove a fake one — the platform makes
      approved tables immutable.
- [ ] Date them **1 September 2026 or earlier** so they supersede cleanly.
- [ ] Check the SSS figure: the fake table produced **₱250.00** on an ₱11,000 semi-monthly gross.
- [ ] Then delete or void PAY-2026-002.

**This is not a Tuesday blocker.** Nobody onboarding will run payroll. But it is the only finding in
the entire sweep that could reach a real person's pay, so it does not get forgotten.

---

## 4. Tuesday — what to open, and what to hold

Open everything **except three modules**, for one week.

**Open on day one:** everything except Payroll.

**Hold nothing.** Open all twenty-two screens on Tuesday.

I previously advised holding Finance, Procurement approvals and Payroll for a week. **That advice
was based on approvals being recorded with no trace of who approved what.** With item 1 marking
every self-approval and counting it on the Board Pack, the history is honest from day one, so the
reason for the hold is gone.

Payroll is the exception, and not for control reasons: the four statutory rate tables are still
fake. Nobody should run a pay period until they are replaced — see the payroll checklist above.

Not because money will be lost — nothing on the platform moves cash — but because until the guard
lands, every approval recorded is an approval your audit chain will show as uncontrolled. **The
audit chain is the one thing that cannot be cleaned.** A week of clean history costs you nothing;
a week of uncontrolled approvals is permanent.

If item 1 of the prompt lands cleanly on Monday, open all three on Tuesday and ignore this section.

### Something you can send them

> The workspace platform is live from today. Everything you need for your daily work is open:
> messages, your day, site reports, safety, tasks, inventory, documents and permits. Use it exactly
> as you would have used the group chats.
>
> Payroll is the one thing not to touch yet — the contribution tables are still being loaded.
>
> You may still see a few records whose names begin with `Z1-` or `Z2-`. Those are test records
> from the weekend and they are being removed. Ignore them.
>
> If something looks wrong, say so in the workspace rather than working around it. Finding
> problems this week is the point.

---

## 5. What I am deliberately holding back, and why

Not because these do not matter — because they will not fit in one day and they do not bite on
Tuesday.

| Held | Why |
| --- | --- |
| **Attachments on records** — photos and video on site reports, non-conformances, defects, documents | The single file input in the product is the chat composer. This is the biggest missing feature you have, and it is a week of work across five screens, not a day. **First item in the next prompt.** |
| Variation orders | `createVariationOrder` already exists at `foundation/projects.ts:606`; only the button is missing. Nobody needs it on Tuesday. |
| The proposal lease figure | It is out by roughly 182× and it goes to clients — but it needs **your decision** on what the constant means before anyone changes a formula. |
| Approvals inbox | Real, and it is why self-approval is the path of least resistance. Bigger than a day. |
| One person record | Two rosters, no bridge. An architectural decision, not a Monday fix. |
| Report figures reading zero | Item 4 of the prompt fixes the worst of it as a side effect. |
| Mobile overflow and touch targets | One unconstrained button causes most of it. Nothing is unusable. |
| Editing and deleting records | Real, permanent, and not a Tuesday problem. |
| Toasts | **Settled — do not spend money.** The dismissal timer stalls only in an automated browser. Both earlier reports were wrong, and so was I for repeating it. |

---

## 6. What is switchable, and what is not

A fair question, and the honest answer is narrower than it sounds.

**There is one switch: `self_approval_mode`.** It ships on `record` and a console holder moves it to
`block` in one action. That is the only place where the platform is deliberately looser than it
will eventually be.

**Everything else in Monday's prompt is a repair.** A contract dated 2027 unlocking a gate, dates
eight hours behind, a progress claim that cannot be created, stock going negative — none of those
have a permissive setting worth keeping. There is nothing to switch on a bug.

**And I would not add more switches.** Every switch is code to build now, a thing to forget later,
and one more way for two workspaces to behave differently. One switch plus a written register beats
ten switches nobody remembers.

So the register is below. Some of it is a switch; most of it is work with a trigger attached.

### The tighten-later register

| | What | How it tightens | What triggers it |
| --- | --- | --- | --- |
| 1 | **Self-approval** | Switch `self_approval_mode` from `record` to `block` | Outside investment, **or** a second approver exists in Finance and Procurement, **or** the Board Pack counter shows it has become routine |
| 2 | **Statutory rate tables** | Enter and approve four genuine tables; supersede the fakes | **Hard date: before 16 September 2026.** Not a judgement call |
| 3 | **Payroll disbursement** | Require a second person to release a pay run | When the Head of Finance is active on the platform |
| 4 | **Hard block 6** | Enforce your rule — signed contract *and* released funds — rather than the stage gate that stands in for it today | Monday's item is a partial fix; the full rule when the first real purchase order is raised |
| 5 | **Attachments on records** | Photos and video on site reports, non-conformances, defects and documents | Next prompt. This is the biggest missing feature you have |
| 6 | **Approvals inbox** | Tell people something is waiting for them | Next prompt. Until it exists, approvals are found only by opening the record |
| 7 | **One person record** | Merge or bridge the workforce roster and the platform roster | Before the next intake of field staff |
| 8 | **Variation orders** | Add the button; `createVariationOrder` already exists on the server | When the first variation is raised on a live job |
| 9 | **The lease constant** | Decide whether ₱6.70 is per kilowatt-hour or per square metre, then fix the formula or the constant | **Before the next proposal goes to a client.** It is currently out by roughly 182× |
| 10 | **Restore from a backup** | Build the import: identifier remapping, dependency order, chunked writes | First item of the next prompt. Monday only makes the backups honest; it does not make them restorable |

Items 2 and 9 have real deadlines. The rest move when the trigger arrives.

**On backups.** Monday's item 13 makes the export complete and checkable. It does **not** build the
restore — writing 117 tables back means remapping every internal identifier, importing in
dependency order and chunking around the write limits, and that must not be built untested the
night before onboarding. So from Tuesday you will have honest monthly backups that you have
verified, and no way to load one back until the next prompt. That is the right order: a backup you
cannot trust is worse than no backup, and a restore you have never tested is worse still.

## 6. The register

Everything found, with its evidence:

- `SWEEP-2-ROOT-CAUSE-2026-09-05.md` — the live sweep, 74 findings, 14 root causes
- `SWEEP-ROOT-CAUSE-2026-09-05.md` — the branch sweep, 63 findings
- `PROMPT-MONDAY.md` — what you send tomorrow
- `CONSOLIDATED-FIX-PROMPT.md` — the protocol-layer items, still unsent
- `PROMPT-1-UNBLOCK.md` — **retired.** It was written for an empty tenant; production is already
  seeded, so most of it does not apply. Its four still-relevant items are folded into the Monday
  prompt.

**Three findings came from reading the code and no browser could have found them:** the progress
claim cast, the variation order that already exists on the server, and the lease figure. All three
are confirmed against the export you sent today.
