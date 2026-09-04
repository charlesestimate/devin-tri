# Two overnight sweeps, grouped into root causes

**Date:** 5 September 2026
**Inputs:** 1st_AI bug sweep (31 defects, desktop, `bug-test/v3`) · 2nd_AI gap sweep (32 gaps + mobile table, `bug-test/v2`)
**Cross-checked against:** the source export of 4 September, 04:25 (`convex/` and `src/`)
**Author:** Claude, for Karl Ivan Estadola

---

## 0. Read this first

**Your production platform is not broken the way these reports read.** Both agents worked on an
*empty* test tenant. The single finding that dominates both reports — the platform cannot make a
proposal — is a **new-tenant** problem. Production was seeded when it was built: it has the thirty
gates, the roles, the system constants and PRJ-2026-0041. Your team can still work next week.

What the empty tenant did do is **stop both sweeps at step 6 of 17**. Nobody has ever tested
proposal → won → project → contract → block sign-off → purchase order, or the six modules behind
them. That is the real cost of the night, and it is recoverable for free.

**The numbers.** 63 findings raised. 8 are the same finding seen by both agents independently
(which is confirmation, not noise). **55 distinct findings. They reduce to 14 root causes.**
Six of the fourteen are one-line or one-component fixes.

---

## 1. The fourteen root causes, by blast radius

### RC-1 — The tenant is never seeded, and the seeder that already exists is not reachable
**Explains 12 findings:** A-08, A-16, A-13, A-31, A-02, B-01, B-03a, B-28, B-29, and the project
requirement that makes A-20 and A-24 fatal.

I found the seeder. `convex/foundation/seed.ts:21` — `seedFoundation` — creates tenants, **the
thirty gates** ("Exact 30 rows per F3.1"), the hard blocks, the system constants (`specific_yield`
is at line 451) and the roles, in one mutation, and returns a count of each. **It is written, it is
complete, and it is correct.** Nothing calls it when a tenant is created, and nothing in
Administration → Setup and Migration exposes it.

So the string `specific_yield` that stopped both agents is not missing code. It is a mutation that
exists and is never run.

Three smaller seeders sit in the same state — `manpower.ts:67 seedTrades`, `inventory.ts:66
seedLocations`, `dataMigrations.ts:118 seedRoles`. Roles is the clearest symptom: the Roles tab
renders one paragraph and nothing else (A-31), and the fix is on a different tab under a different
name.

**Fix:** call the foundation seed at tenant creation. Until then, expose "Seed System Constants"
beside the operations already listed. **Size: small. Unblocks eight screens.**

---

### RC-2 — Two identity rosters that never meet
**Explains 8 findings:** A-04, A-22, A-24, A-28a, B-04, B-06, B-25, B-27.

`persons` and `workforce_persons` are separate tables with no bridge, and **neither has a create
control in the product**. The only way to create a person is a paste box inside Migration and
Cutover — a one-off migration tool being used for a weekly event.

What that produces, all verified by one agent or the other:

- A worker you hire in Manpower cannot be issued a permit to work (the dropdowns list Persons only)
- …cannot be paid (Add Employee picks Persons only)
- …cannot be added to a group chat
- …cannot be assigned a task (Assign To offered exactly one name — the signed-in account)
- Add Employee will happily link person B-Alpha Reyes to workforce record B-Delta Ramos and save it
- Neither record has a job title field, so Chief Executive Officer had to be filed as "Site Admin"

**Fix:** one bridge, plus a create control on Administration → Persons and inside Add Employee.
**Size: medium — it is a data-model decision, not a screen fix.** This is the one to think about
before prompting.

---

### RC-3 — Optional foreign keys read as if they were required, with the type system silenced
**Explains the application-killer:** A-30.

`convex/schema/safety.ts:73` declares `projectId: v.optional(v.id("projects"))`.

`convex/reports/reports.ts:311` and `:342` read it like this:

```ts
const project = await db.get("projects",
  (incident as Record<string, unknown>)["projectId"] as Id<"projects">);
```

Two casts in one expression. The first throws away the type, the second asserts the missing thing is
present. TypeScript would have caught this and was told twice not to.

**The error message decodes exactly.** 1st_AI recorded `Unable to decode ID: Invalid ID length 8`.
`"projects"` is eight characters. When `incident.projectId` is `undefined`, the table name itself
reaches the ID decoder. 1st_AI's INC-0001 was filed with no project — Incidents correctly make it
optional — and that one record takes the report down.

Across `convex/` there are **411 `as Id<…>` casts** and **36 `as Record<string, unknown>` casts**.
Not all are dangerous. Every one sitting on a field the schema marks `v.optional` is this same bug
waiting for a record.

**Fix:** guard the two lines today. Then audit the casts that land on optional fields.
**Size: two lines, then a sweep.**

---

### RC-4 — There is no error boundary anywhere in the application
**Explains:** A-30's blast radius, A-06, B-32.

I searched `src/` for `ErrorBoundary`, `componentDidCatch` and `errorElement`. **Zero matches.**

That is why one failing query on one tab white-screens the sidebar, the header and every control,
and the only way out is a browser reload. It is also why a route change shows a blank pane for up to
five seconds and a cold load shows a dark screen for eight to twelve with no spinner: there is no
fallback layer at all.

**Fix:** one boundary at the route level, one per tab panel, one suspense fallback.
**Size: small — and it converts every future RC-3-class bug from an outage into a broken panel.**
Of everything in this document, this is the highest ratio of protection to effort.

---

### RC-5 — Validation is written per form, by hand, and mostly not written
**Explains 10 findings:** A-01, A-07, A-14, A-15, A-17, A-19, A-21, A-27, A-29, B-25.

Accepted and saved without complaint:

| What was entered | Where | Consequence |
| --- | --- | --- |
| Payroll period 30 Sep → **1 Sep** | Payroll | A period that ends 29 days before it begins, runnable once the statutory tables are approved |
| Permit type default duration **−30 days** | Permits | A permit that expires a month before it is issued, in the shared library |
| Incident dated **31 Dec 2027** | Safety | A statutory register that accepts future events |
| Headcount **0**, target date **1 Jan 2020** | Human Resource | Rendered as "1 Jan" with no year — indistinguishable from this January |
| TIN `not-a-tin-at-all` | Pipeline | Stored verbatim; the placeholder shows the exact required shape |
| File reference `this is not a url` | Documents | Produces a live "View" link to a dead page |

And two silent failures: a group chat with no members closes the dialog and saves nothing (A-01), and
New Opportunity's button simply does not respond until you find the field it will not name (A-07).

It is not that validation is absent — Inventory's unit cost correctly rejects negatives, "Legal name
is required" fires correctly, Payroll's run guard is genuinely good and names all four statutory
tables. **It is that each form was validated by hand and most were skipped.**

**Fix:** shared validators (date range, positive integer, Philippine TIN, storage reference) and one
rule: a blocked submit must name the field that blocked it. **Size: medium, mechanical.**

---

### RC-6 — Nothing in the platform tells anyone anything
**Explains 5 findings:** A-32, A-25, A-23c, A-24, B-30.

The notification panel said "No notifications" after three hours in which two agents created
accounts, sites, opportunities, an employee, a near miss, permit types, an incident, a payroll
period and dozens of messages — and in which one had a message hidden by an administrator, one was
@mentioned, and one had a task assigned. Messages has no unread indicator of any kind; the numbers
beside COMPANY, DIRECT and SPACES are conversation counts. A mention renders as plain grey text.

Meanwhile **Administration → Audit Chain recorded all of it** — 88 entries, chain intact, verified.

**This is L3.** Your own principle: capture must have consequence. Records are being completed
correctly and sent somewhere nothing reads them. The audit chain is the strongest thing on the
platform and nothing downstream of it ever reaches a person.

**Fix:** emit from the events the audit chain already writes. **Size: medium.** Note this is not
presence, typing or read receipts — those stay in §15 where you put them. An unread count is a
different thing and does not track anybody.

---

### RC-7 — Time is Coordinated Universal Time, not Philippine time
**Explains 1 finding, and it is expensive:** B-09.

At 01:16 on Saturday 5 September, My Day said 5 September and Reports evaluated at 5 September — but
the Site Assessment saved as 4 September and New Permit to Work defaulted its issue date to
04/09/2026. The code uses `new Date().toISOString()` for stamps and defaults (e.g.
`convex/safety/safety.ts:322`). Philippine time is UTC+8.

**Between midnight and 8 a.m. Philippine time, every date default is yesterday.** A permit to work
is same-day and expires at the end of its issue date. A permit raised at 6 a.m. — which is when
site crews raise them — is born expired. Every site report and assessment filed before 8 a.m. is
dated the day before.

**Fix:** one date helper, local time, used everywhere. **Size: small. Consequence: large.**

---

### RC-8 — The phone gets the desktop layout
**Explains 4 blocking findings and 21 more:** B-02, B-03b, B-07, B-08 plus the mobile table
(4 absent · 4 hidden · 4 unusable · 13 degraded).

The four that stop work on a phone:

1. **Raise Stop is clipped off the right edge** on Safety. Icon and one letter render; the pane will
   not scroll sideways. This is the one control that exists for an emergency, it is always used on a
   phone, and on a phone it cannot be pressed.
2. **Payroll's tab strip is clipped** with no arrows and no scrollbar, so Statutory Rate Tables
   cannot be reached — and payroll cannot run until those four tables are approved.
3. **There is no Sign out and no user row** in the phone drawer. On a shared site handset that is a
   security problem.
4. **Documents, Manpower and Inventory keep their two-pane desktop layout at 375 px** — a 60 px
   detail pane printing on top of the list, names wrapping one word per line, a search box rendering
   as "Searc".

**The fixes already exist in your codebase.** Messages collapses correctly (list → tap → conversation
→ back). Reports, Administration and Migration already solve tab overflow with a scrolling rail.
So this is applying two patterns you already own to five screens, plus a drawer footer, plus header
stacking below 640 px. **Four shared components, not twenty-two screen rewrites.**

---

### RC-9 — The interface is written in the database's language
**Explains 7 findings:** A-18, B-21, B-22, B-23, B-26, B-31, B-32. **This is a §4 violation.**

Printed to users: `specific_yield`, `timesObserved`, `view = true`,
`{capacity}_kW_{account}_{project number}`, `document_revision.create`,
`workforce_person.status_change`, `https://hercules-cdn.com/file_…`, and `craw` — an internal token
in the Migration help text that I cannot account for.

Gate and hard-block numbers are printed as user-facing help — "Assign Role raises gate 24",
"Hard Block 6 Active" as a headline metric — with nothing anywhere explaining what a gate is.

One customer is called an **Account**, a **Customer**, a **Client** and a **Party**. Dates appear in
four formats. "Balance of System" is spelled out in Inventory and abbreviated to "BOS Equipment" on
the proposal form. "Issued PTWs" and "New Permit to Work" sit on the same screen.

**On the gate count disagreement — Administration is right and the landing page is wrong.**
`src/pages/Index.tsx:12` contains a hardcoded string: `"29 configured gates, full audit trail"`.
It is not a live count. The specification is exactly thirty (1–12, 18–24, 25a, 25b, 26–34) and
`seed.ts` says so. The same three lines ship "EPC" and "PTWs" on the front page.

---

### RC-10 — The entry points are decorative
**Explains 7 findings:** A-09, A-10, A-12, B-10, B-11, B-12, B-14, B-15.

The global search box is inert — click does nothing, the keyboard shortcut does nothing, and it
shows the Mac Command symbol on every platform. It is the most prominent control in the product.

The Dashboard's four cards are not links or buttons in the accessibility tree at all. **I found why:
they are the `FEATURES` array from `src/pages/Index.tsx` — the signed-out marketing hero, re-used as
the signed-in landing page.** They were never meant to be clickable. That also explains why the
Dashboard shows no data: it was never a dashboard.

Three of the six My Day quick actions land on the same screen, and two of them contradict their own
labels — "Report Near Miss" is described on the row as anonymous and sends you to the Safety Stops
list instead of the anonymous form, which is the best-designed form in the platform.

---

### RC-11 — Documents stores references and can never store a file
**Explains 2 findings:** A-21, B-05.

Add Revision asks for "File Reference (CDN URL or Storage ID)". There is no file picker anywhere in
the module, and the platform offered to **publish** a controlled revision with no file behind it.

The galling part: **the upload pipeline exists and works.** The Messages paperclip does it correctly
— staged, sent, folder-per-thread in Drive, survives a full reload, both agents verified it. It is
simply not wired to Documents.

**Fix:** point the revision dialog at the uploader you already have, and refuse to publish an empty
revision. **Size: small.**

---

### RC-12 — Created records cannot be corrected, and one form corrupts them
**Explains 2 findings, which compound:** A-03, B-20.

Add Worker retains abandoned input and re-presents it as a fresh form. That already produced a
corrupted record: a validation-blocked attempt at "A-Alpha Reyes", then a reopen, then retyping —
saved as **`A-Alpha ReyesA-Alpha Reyes`**, EMP-0001.

And permit types offer only Deactivate; inventory locations and items offer nothing; sites have a
pencil but no delete. **So the corrupted record is permanent.** A typo in a permit type name is
permanent. Either problem alone is an annoyance; together they are damage.

---

### RC-13 — Messages: your healthiest module, with a short defined list
**Explains 4 findings:** A-23, A-25, A-26, B-16.

Working and verified by both agents: pin, bookmark, reply with quoted context, search with a proper
empty state, create group, add and remove member, direct messages, image and file attachments
surviving a reload, hide message with a required reason and a tombstone, rename, and the phone
layout.

Still wrong, all small:

- Opening a space scrolls to the **oldest** message; sending does not scroll to the newest
- **Enter accepts the mention list as "send"** — 2nd_AI's "@Karl" posted as plain text and the rest
  of the sentence became a second message
- The @ picker lists everyone in the tenant including **non-members of the space**, and the sent
  mention renders as grey text, not a chip. A supervisor can @ someone into a space they cannot read
  and believe they have been told
- No unread indicator of any kind (see RC-6)
- Rename updates the sidebar and posts a system message but leaves the conversation header and the
  Group info heading stale
- An image attachment renders as a bare thumbnail with no filename and no download; a non-image gets
  a proper chip with both
- Messages never remembers the last conversation

**Do these in one pass.** 2nd_AI's judgement is worth repeating verbatim: fix the scroll-to-newest,
the Enter-on-mention, the clipped Raise Stop and the phone sign-out, and a foreman would keep this
open on site instead of Messenger. Those four are the difference.

---

### RC-14 — Developer maintenance is exposed as product, including a one-click irreversible wipe
**Explains 1 finding. This is a risk, not a defect:** B-29.

Administration → Setup and Migration lists "Migrate Hard Blocks to Specification", "Seed Roles",
"Backfill General Channel", "Seed Project Names" — and, in the same scrolling list,
**"Clear All Test Data"**: one click, irreversible, every operational record.

Both agents deliberately refused to press it. **Sixty staff arriving next week will not all be that
careful.** Move it behind a typed confirmation on its own screen before the pilot, or hide it.

---

## 2. Five findings I would not pay to fix, and why

Discovery is cheap now. Spending Hercules credits on these would not be.

**1. "Toasts never dismiss" (A-05 / B-19) — verify by hand first, ten seconds.**
`src/components/ui/sonner.tsx` sets no duration, so it uses sonner's four-second default, and there
are no explicit toast durations anywhere in `src/`. Sonner pauses its dismissal timer while the
document is unfocused — which is the normal state of an automated browser being screenshotted.
**This is probably an artefact of how the agents drove the page.** Open the platform, save something,
and count. The *other* half of the finding is real either way: the toast sits on top of the Messages
send button, and that is a position fix, not a timer fix.

**2. Shipping the four statutory tables (B-03a) — that is your decision, not a defect.**
2nd_AI is right that SSS, PhilHealth, Pag-IBIG and withholding are published national schedules and
that hand-keying them is days of work. But shipping them means **Magnus owns the compliance risk of
keeping them current** for every tenant, and they change. My recommendation: ship them with effective
dates *and* a required acknowledgement that they were verified against the current circular. Do not
let this be decided by a developer as a convenience.

**3. "Not maintained — grows over time" on the Requirement Library (B-28).**
2nd_AI read this as a warning that nobody looks after it. It is **L5 stated correctly** — accumulate,
do not maintain. Reword it for a human. Do not redesign it.

**4. Capping the account legal name (A-14).**
Do not add a length limit. Philippine corporate legal names are genuinely that long. The defect is
that one long name pushes Type, Region and Industry off the edge **for every other row**. Fix the
column, not the field.

**5. "Make the Dashboard the Board Pack" (B-10).**
A good idea and probably the right one — Reports → Board Pack already contains what this company
needs. But it is a redesign, not a defect. It goes in the open items register, not in a fix prompt.

Also noted: **1st_AI withdrew A-11 after retesting it** and left the number in place so the numbering
stayed stable. That is the behaviour you want from a tester, and it is worth knowing the report was
written by something willing to take a finding back.

---

## 3. What neither agent could see, and it is where the money is

Both sweeps were run through a browser. **The control layer is invisible from a browser**, and it is
where the code review of 4 September found the failures that matter most:

1. **The approval gate is derived from severity instead of from amount.** `convex/finance/finance.ts:12`
   maps minor → gate 1, moderate → 2, major → 3. Your specification is explicit and repeated: the
   gate is derived from the amount and is never chosen. The same wrong rule was written a **second
   time, independently**, in `convex/mcp/group3bInternals.ts`.
2. **Hard block 6 is implemented as the wrong rule.** `convex/procurement/orders.ts` checks for a
   gate-4 approval. Hard block 6 is the signed contract and fund release.
3. **The protocol layer imports nothing from the domain layer** — 178 direct `db.insert` / `db.patch`
   calls in `convex/mcp/*`, every write reimplemented inline.

A browser sweep cannot see any of this because it produces a plausible screen every time. **It
produces the wrong approval silently.** These are Part A of `CONSOLIDATED-FIX-PROMPT.md`, written on
4 September and never sent.

---

## 4. What to do, in order

The point of this ordering is that **each step makes the next one cheaper**, and one of the four
steps costs no Hercules credits at all.

### Prompt 1 — "Make an empty tenant usable." Send this one now. It is small.
1. Call the foundation seed at tenant creation; expose "Seed System Constants" in Setup and Migration (RC-1)
2. Guard the two unguarded project reads at `reports.ts:311` and `:342` (RC-3)
3. Add an error boundary at the route level and per tab panel (RC-4)
4. One Philippine-time date helper, used everywhere (RC-7)
5. Make Project optional on Raise Safety Stop, matching Incidents (A-20)
6. Move Clear All Test Data behind a typed confirmation (RC-14)
7. Fix the hardcoded "29 configured gates" — it is thirty (RC-9)

Seven items. All small. **Unblocks eight screens and removes the two things that can take the
application down or lose the data.**

### Then re-sweep with the two Chrome agents. This costs no Hercules credits.
Nobody has ever tested proposal → won → project → contract → block sign-off → purchase order, or
Tasks, Design, Procurement, Construction, Operations and Maintenance, or Finance. That is where the
six hard blocks and the thirty gates actually live — the part of the platform you care most about
and the part that has never been exercised by anyone. **Discovery is free now. Use it before paying
for fixes.**

### Prompt 2 — The control layer.
`CONSOLIDATED-FIX-PROMPT.md` Part A: fix the domain rules first (gate from amount, hard block 6),
then converge the protocol onto them. Ordering matters — converging first would spread the wrong
rules.

### Prompt 3 — Make it enterable by sixty people.
RC-2 (one person record) and RC-5 (shared validators). RC-2 is the one that needs a decision from
you before it is prompted, because it is a data-model change.

### Prompt 4 — Make it usable on a phone and pleasant to read.
RC-8 (four shared components, using two patterns you already own), RC-13 (the Messages list),
RC-9 (the language), RC-11 (wire Documents to the uploader you already have).

---

## 5. Coverage debt — what is still untested by anyone

**Never reached at all** (blocked by RC-1): the entire commercial chain past a proposal, and the
contents of Tasks, Design and Engineering, Procurement, Construction, Operations and Maintenance,
Finance, and Projects.

**Reached but not exercised:** Human Resource → Recruitment, Performance, Engagement, Regularization ·
Inventory → Transfers, Adjustments, Physical Counts · Manpower → Resource Requests, Equipment ·
Administration → Hard Blocks, Console Holders, Tenants, Agent Sessions, Integrations, Compliance ·
Migration → Parties, Inventory Items, Project Seeds, Cutover · Safety → Corrective Actions,
Inspections.

**Cannot be tested this way:** on-screen keyboard occlusion at phone width (a desktop preview has no
keyboard) · the native operating-system file picker (1st_AI built the files in the page instead;
the attachment path itself was fully exercised end to end).

**One housekeeping item:** 1st_AI asks that the account
"A-ZZZ Edge Case Corporation With A Deliberately Very Long Legal Name…" be deleted from the test
branch — while it exists it breaks the Accounts table for every other row.

---

## 6. Two notes on method

**These reports are unusually good, and you should know why.** Both agents recorded what they did,
what they expected, what happened, whether it repeated, and the exact console text. One of them
retested a finding and withdrew it. Both listed their assumptions, including the ones that weaken
their own conclusions — 1st_AI explicitly refused to state how the B- persons were created because
it had not watched it happen. Both refused to press the irreversible button. That is why I have been
able to take almost all of it at face value and check only the parts where the code could settle it.

**Where I checked, the code agreed with them three times out of three** — the seeder exists and is
unreachable, the ID decode failure is the string `"projects"`, and there is no error boundary
anywhere. The fourth check disagreed with them, and that is the toast finding above.

**Line numbers.** The export I read is from 4 September 04:25; the agents swept `bug-test/v3` on
5 September. `reports.ts` has drifted by one line between them — the agent's `:312` is my `:311`.
Everything above is stated against my export. Hercules should confirm against the branch.
