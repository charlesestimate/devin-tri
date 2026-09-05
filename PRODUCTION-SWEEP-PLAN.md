# Sweeping the live platform this week — my thoughts, and the plan

**Date:** 5 September 2026 · **Target:** `magnus-solar-workspace-platform-446354.onhercules.app` (main)
**Constraint:** no Hercules credits until Monday. Chrome agents cost nothing.

---

## 1. My view: do it. It is better than the test branch, not a compromise.

The empty test branch is what limited both sweeps to step 6 of 17. **Production is
already seeded** — it has the thirty gates, the roles, the system constants and
PRJ-2026-0041. So the half of the platform nobody has ever tested is testable on
main **today**, without waiting for Monday's fix:

proposal → won opportunity → project → contract → block sign-off → purchase order,
and the six modules behind them.

That is where your thirty gates and six hard blocks actually live. It is the part of
the platform you care most about, and it is the part that has never been exercised by
anyone. Testing it this week costs nothing and makes Monday's credits go further,
because we will be fixing a list we have finished writing instead of one we are still
discovering.

**But three things in your terms need to change, and one of them is serious.**

---

## 2. The serious one: Clear All Test Data is not the cleanup you think it is

You wrote: *"We later remove the records during the start of migration."* I read what
that button actually does. It would take your onboarding with it.

`convex/foundation/clearTestDataInternal.ts` — what the operation deletes and keeps:

| | |
| --- | --- |
| **Deleted** | `persons` · `person_roles` · `workforce_persons` · `trades` · every operational record |
| **Kept** | `users` · `channels` · `channel_members` · `audit_entries` · gates · roles · hard blocks · system constants |

Read those two rows together.

**It deletes every person record and every role assignment** — Beda, Jennifer, Alf,
Christiana, Alma, Kidron and the forty-two staff from the spreadsheet, plus every role
you assigned in the browser and every one I assigned over the protocol.

**And it keeps every group chat and every membership row**, now pointing at people who
no longer exist.

So running it after the sweep would undo a week of your onboarding, leave the message
spaces holding dangling references, and — because there is still no way to create a
person except the paste box in Migration and Cutover — you would rebuild the whole
roster by hand.

**Do not plan to use it on main.** The cleanup has to be targeted instead. See §6.

One more reason not to trust it by eye: the file's own header comment claims it
preserves `approval_requests`, and the code clears them on the first line of the list.
I went by the array, not the comment.

---

## 3. Three additions to "Administration is the only restriction"

Restricting Administration is right and it covers the destructive operation. It is not
sufficient on a live platform with real people in it.

### 3a. Never approve a statutory rate table
`convex/payroll/payroll.ts:397` — `approveRateTable`. Approving a table **supersedes
the previous one** (line 428) and the payroll run re-reads the approved table every
time. An agent hand-entering plausible-looking Social Security System brackets and
approving them creates the basis on which real people are paid. Creating a payroll
period is fine and useful. **Approving a rate table is forbidden outright.**

### 3b. Never touch a person, space, message or record it did not create
Your staff are in there. On the test branch the agents added members, removed members,
renamed groups and hid a message — all correct behaviour on an empty branch, all
unacceptable on main. Specifically forbidden: adding or removing any real person,
assigning or revoking any role, hiding or deleting anyone's message, renaming or
joining any existing space, and posting to **General** or any company-wide channel.

### 3c. Every record it creates carries a `Z-` prefix
Not `A-` or `B-` — those are burned on the test branch and I want the production test
records to be unmistakable. Every account, site, opportunity, project, permit type,
document, worker, space and message starts with `Z-`. This is what makes §6 possible.

---

## 4. Sequence it before onboarding, not alongside it

You said users are not yet onboarded. **That is the window.** Every test record created
before real work starts is cleanly separable; every one created after is entangled with
it.

- **Now → Sunday:** the two agents sweep. Only Karl's account is in use.
- **Sunday:** I clean up, using §6.
- **Monday:** Hercules gets Prompt 1 and Prompt 2, with a complete list.
- **After that:** staff onboard onto a fixed platform with the test records gone.

If staff start creating real records while the agents are still working, that ordering
collapses and cleanup becomes a manual reconciliation.

---

## 5. What the two agents do — the division you agreed to

Both are told to hunt bugs **and** gaps this time. Splitting by label is what produced
your eight duplicates; splitting by territory will not.

**1st_AI — the commercial chain, end to end.**
Create a `Z-` account, site and opportunity, then drive it all the way: proposal →
won → project → contract → risk terms → project blocks B0/B1 → design package →
bill of materials → purchase order → goods receipt → progress claim → fund request.
This is the first time anyone will have walked it. It is where the six hard blocks
live, and hard block 6 — signed contract and fund release — should refuse a purchase
order until the contract is signed.

**2nd_AI — the six modules that were empty all night**, now with a real project to
work in: Tasks and Deliverables, Design and Engineering, Procurement, Construction,
Operations and Maintenance, Finance. Desktop pass, then phone pass, same as before.

No overlap. Between them they cover the half of the platform that has never been seen.

---

## 6. What I get for free, and it is the most valuable part

There is a defect in the code that neither browser sweep could see and that I have so
far only been able to argue from reading:

`convex/finance/finance.ts:12` derives the approval gate from **severity**
(minor → gate 1, moderate → 2, major → 3). Your specification says the gate is derived
from the **amount** and is never chosen. The same wrong rule was written a second time,
independently, in `convex/mcp/group3bInternals.ts`.

On a live tenant with real gates configured, an agent can now **prove it empirically**:
raise two variation orders on a `Z-` project — one small, one large, both marked the
same severity — and record which gate each one raises and who it asks. If they raise
the same gate, the defect is demonstrated on your own data, with screenshots, and
Prompt 2 stops being my reading of the source and becomes a reproduction.

That evidence costs nothing and it is the strongest thing we could hand Hercules.

---

## 7. Cleanup, and how we make it real

**Sunday, by hand — what can be deleted:** contacts and messages have delete controls.
Spaces can be deleted (you established that). I will remove what the interface allows.

**What cannot be deleted, and this is a known defect:** permit types offer only
Deactivate; inventory locations and items offer nothing; sites have no delete. So some
`Z-` records will survive until we have a tool.

**Monday, one line added to Prompt 1:** a Migration and Cutover operation that deletes
records whose reference or name begins with a given prefix, within a named set of
tables, reporting what it deleted before it does it. That is a small, contained
addition — and it is the tool you will want again every time you test.

Until then, the `Z-` prefix means every test record is identifiable at a glance, and
your staff can be told in one sentence: **anything starting with `Z-` is a test record,
ignore it.**

---

## 8. What I need from you before I write the briefs

1. **Confirm the window** — that no staff will create real records before Sunday.
2. **Confirm 3a** — the agents may create payroll periods but must never approve a
   statutory rate table.
3. **Anything else on main that must not be touched** that I have not thought of.
   Live supplier records, a real client account, anything already in Documents.

Say yes and I will write both briefs the way I wrote the last two — fully autonomous,
no questions, one report each, and a coordination space so they do not collide.

---

## 9. One thing I got wrong, and have corrected

I told you Prompt 1 should make Hercules put Clear All Test Data behind a typed
confirmation. **It already is.** `src/pages/admin/page.tsx:2110` requires the phrase
`CLEAR ALL TEST DATA` typed exactly, the button stays disabled until it matches, and
the server re-validates it independently. The tester reported it as "one click,
irreversible" because it never pressed the button — it described the list item, not
the guard behind it, and I passed that on without checking.

I have rewritten that item. It now asks for two real things instead: separate it
visually from the seeding operations, and move `trades` out of the delete list into
the preserved reference data, so that clearing test data no longer leaves a workspace
unable to add a worker.

**Re-download `PROMPT-1-UNBLOCK.md` before you send it Monday.** The version I gave you
earlier would have paid to build something that already ships.
