# Full platform sweep — for Claude in Chrome

**Your job is to find and document defects. You are not here to fix anything.**

Open every screen in the Magnus Workspace Platform, use every control on it, and
write down what does not work. When you find a defect, record it and move on —
do not investigate the cause, do not read code, do not propose a fix. Someone
else does that afterwards with the source in front of them.

We are paying for discovery, not repair. A defect found and clearly described is
a complete result.

---

## The platform

**https://magnus-solar-workspace-platform-446354.onhercules.app/**

You are signed in as **Karl Ivan Estadola, Chief Executive Officer** — a console
holder with full access. Remember this: a control you can see may be invisible to
a Solar Installer. Note anywhere that seems likely.

### Where you are working — read this first

You are working inside the **Hercules workspace**, not the plain platform. The
screen has three parts and only one of them is yours.

**Yours to use:**

- The **Preview pane** on the right — the platform itself. Everything in the
  sweep happens here.
- The preview's own **back, forward and reload** arrows.
- The two small **device icons** beside the word Preview — a monitor and a phone.
  These switch the preview between desktop and phone width. Use them to change
  between passes.
- The **Console** strip along the bottom. Read it. Errors appearing there while
  you click are valuable — include them in your defect reports.

**Never touch, under any circumstance:**

- The **chat panel** on the left, or anything that says "Type your message". Do
  not type into it, do not press its send arrow. Every message there spends money
  and starts a build. This is the single most important rule in this brief.
- **Publish.**
- The **version selector** — the box reading `v68` or similar. Changing it rolls
  the application back.
- **Debug Mode / Build mode**, or any toggle between them.
- The entire **left navigation rail** of Hercules — AI Editor, Visual Editor,
  Branding, Users and Access, Files and Media, Email, Audits, Commerce, Domains,
  Mobile, Showcase, Analytics, Chat Integrations, Roadmap, Personalize, Skills,
  Versions, Secrets, Database, Backend, Tests, Push Notifications, Codebase,
  Settings. None of it is part of the platform under test.

If you are ever unsure whether a control belongs to Hercules or to the platform,
do not click it. Ask.

### Two passes, desktop first

**Pass 1 — desktop.** With the preview set to the monitor icon, go through every
screen and build the inventory: every button, tab, menu, filter and form field
that exists, and whether each one works. This pass establishes what the platform
is supposed to have.

**Pass 2 — phone.** Switch the preview to the phone icon. Go through the same
screens again with the Pass 1 inventory in hand, and check each control is still
reachable and still works. Anything present in Pass 1 and missing or unusable in
Pass 2 is a defect, recorded as `WIDTH: phone only`.

The order matters. You cannot notice that a control is unreachable on a phone
unless you already know it exists.

Say which device icon is selected at the start of each pass, so the record is
unambiguous.

Most of this company works from a phone, and nearly every defect found so far has
been mobile-only, so Pass 2 is where the valuable findings are.

### During Pass 2, build the gap table

The difference between the two views is not a scatter of unrelated bugs — it is
one systematic problem, and it needs its own document. As you repeat each screen
on the phone, record every control from Pass 1 against one of five states:

| State | Meaning |
|---|---|
| **same** | Reachable and works exactly as on desktop |
| **absent** | Does not render on the phone at all |
| **hidden** | Renders but cannot be reached — off screen, clipped, behind a hover, under another element, needs a scroll that does not scroll |
| **unusable** | Visible but cannot be operated — too small to tap, overlapped, keyboard covers it, tap does nothing |
| **degraded** | Works, but takes materially more steps than on desktop — say how many more |

**hidden** is the important one and the easiest to miss. A control that exists in
the page but is invisible on a phone looks identical to one that was never built.
If you can see it on desktop and cannot reach it on the phone, it is `hidden`,
and that is a defect even though nothing is broken in the ordinary sense.

Only `same` is acceptable. Everything else goes in the table.

---

## Step zero — establish whether this is real data

You are testing a **branch preview**, not the live platform. The code is
isolated. Whether the **data** is isolated is the thing to establish before you
touch anything, and it takes a minute.

The preview will show a **Sign In** button. Sign in, then go to **Messages** and
look at the member lists and the spaces.

- **If you see around 45 people with real Filipino names, and spaces called
  General, GROUP CHAT 1, Platform Bugs and Tutorials** — this branch shares the
  live database. **Stop and say so.** Do not send messages, do not remove anyone,
  do not delete anything. Wait for instructions.
- **If the platform is empty, or holds only a handful of obviously seeded
  records** — the data is isolated. Proceed with the full sweep below and hold
  nothing back.

Report which of the two you found before doing anything else.

---

## Rules

Assuming step zero showed isolated data:

**Use everything. Break things.** Create records, submit forms, send messages,
start conversations, upload files, rename spaces, add and remove members, convert
messages to tasks, approve things, cancel things, delete things. A control you do
not press is a control nobody has tested. Half-testing produces a half-finished
document, which is worth very little.

Try the awkward cases too, because that is where platforms fail:

- Submit a form with every field empty.
- Put text in a number field, and a negative number in an amount.
- Enter a date in the past where a future one is expected.
- Paste something very long into a short field.
- Press a save button twice quickly.
- Navigate away mid-form and come back.
- Open the same record in two tabs.

**Two things remain off limits, and only two:**

1. **Stay inside the preview pane.** Never touch the Hercules chat panel, Merge,
   the branch selector, the mode toggle, or the Hercules navigation rail. Those
   spend money and change the deployment. The preview pane and its own controls
   are yours; nothing outside it is.
2. **Do not upload anything confidential.** A small test image or document is
   fine.

Everything else is permitted. If a control looks destructive, press it and write
down what happened.

---

## Method

Work one screen at a time, left navigation top to bottom. For each screen:

1. **Does it open at all?**
2. **List every control on it** — buttons, tabs, links, menus, filters, search
   boxes, form fields, table row actions, icons.
3. **Use each one.** Click it. Does something happen? Is what happens what the
   label promised?
4. **Open one record.** Does the detail view load, and do its own controls work?
5. **Submit one small form**, where one exists. Does the record appear
   afterwards in the list it should appear in?
6. **Record every defect** in the format below, then continue. Do not stop to
   investigate.

Four kinds of defect are worth as much as a crash, and are easier to miss:

- A control that does nothing at all when clicked.
- A control that reports success while nothing changed.
- A control that is present on desktop and unreachable on a phone.
- A number that disagrees with the list it summarises.

---

## How to write up a defect

One block per defect. Keep them uniform — they will be sorted and turned into
work.

```
DEFECT ##
SCREEN:        Finance → Write-offs tab
WIDTH:         phone / desktop / both
CONTROL:       "New write-off" button, top right
WHAT I DID:    Tapped it, filled amount 5000, category other, saved
WHAT I EXPECTED: A write-off row appears in the list
WHAT HAPPENED: Dialog closed, no row appeared, no error shown
REPEATABLE:    yes — 2 of 2 attempts
SEVERITY:      blocks work / wrong result / annoying / cosmetic
```

**Severity, plainly:**

- **blocks work** — a person cannot do their job. A screen that will not open, a
  form that will not save, a record that cannot be found.
- **wrong result** — it works but produces something incorrect. Wrong figure,
  wrong name, wrong permission, a summary that disagrees with its own list.
- **annoying** — works, but takes more steps than it should or is hard to find.
- **cosmetic** — spelling, spacing, alignment, a truncated label.

Screenshot anything visual. Quote error text exactly.

---

## Coverage — every screen must be visited

Tick each one. If a screen is empty because there is no data, say so — that is a
result, not a gap.

| # | Screen | Look especially at |
|---|---|---|
| 1 | Dashboard | Do the figures match the lists they summarise |
| 2 | My Day / Today | Does it show anything at all |
| 3 | Tasks | Create, assign, complete, filter |
| 4 | Pipeline | Accounts, Sites, Opportunities tabs; account and opportunity detail panels; the account, contact, site, opportunity, assessment and proposal forms |
| 5 | Projects | Project list, project detail, contract form |
| 6 | Design and Engineering | Package list and detail, create package, create deliverable, add bill of materials line, record seal |
| 7 | Procurement | Purchase order list, create purchase order, purchase order detail |
| 8 | Construction | Site reports, create a report, report detail |
| 9 | Permits | Permit list, permit to work, permit detail |
| 10 | Inventory | Stock positions, transfers, adjustments, counts |
| 11 | Manpower and Equipment | Trades, deployments, equipment, resource requests |
| 12 | Safety | Incidents, near misses, safety stops, inspections, corrective actions, toolbox meetings |
| 13 | Operations and Maintenance | Schedules, visits, readings, defects |
| 14 | Documents | Document list, revisions, acknowledgements |
| 15 | Messages | See the separate list below |
| 16 | Finance | Billing milestones, progress claims, fund requests, write-offs, cash forecast, the summary cards |
| 17 | Human Resource | Employees, recruitment, performance, engagement and regularization |
| 18 | Payroll | Periods, payroll lines, statutory rate tables |
| 19 | Reports | Every report offered — do they render, are they empty |
| 20 | Administration | Roles, permissions, console holders, configuration, integrations, the seed and backfill buttons |
| 21 | Migration and Cutover | What it offers and whether it runs |
| 22 | Notifications | Opens, lists, marks read |

### Messages — the most used screen, test it hardest

- Start a direct message with a colleague. Does the person search work?
- Does the direct conversation show the other person's name?
- Open a space. Rename it. Add a person. Remove a person. Hand over ownership.
- Reply to a message. Does the quoted original appear above your reply?
- Reply inside a record thread under THREADS.
- Pin a message. Where do pinned messages appear? Can you filter to them?
- Bookmark a message. Where do bookmarks appear?
- Search for a word you know is in an older message, one not currently on screen.
- Send a photograph. Does a thumbnail render? Click it — does it open?
- Send a non-image file. Does it download and open?
- Convert a message into a task. Does the task appear under Tasks?
- Mention a person with @. Does the list of people appear, and is it correct?
- Do unread counts appear beside spaces, and do they clear when you open one?
- Read the labels of the record threads. Do they read
  `480_kW_Customer Name_PRJ-2026-0004`, or a bare number?

---

## Already known — confirm in one line each, do not investigate

These are recorded. Say only whether each is still present. Do not spend time on
them.

1. **Mobile navigation.** A staff member reported that on a phone only
   Notifications opens and no other tab does. Confirm or deny at phone width —
   this one matters more than anything else on the list.
2. Images and files return `Missing auth token` when opened.
3. People named `[TEST RECORD]` appear in invite lists and member lists.
4. Group rename and member removal not reachable, particularly on a phone.
5. Reply produces no quoted original.
6. Search finds only what is already on screen.

---

## Optional — verifying that writes actually landed

If a Model Context Protocol token is provided with this brief, use it to check
that what the interface said it did, it actually did.

Endpoint `https://elegant-cormorant-29.convex.site/mcp`, JSON-RPC 2.0, with
`Authorization: Bearer <token>`.

The pattern: create a record in the interface, then call the matching `list_` or
`get_` tool and confirm the record is really there. This catches the most
expensive class of defect — a control that reports success and writes nothing.
A button on the Administration page has already done exactly that.

If no token is provided, skip this entirely and test through the interface only.

---

## What finishing looks like

You are done when every one of the 22 screens has been visited in **both passes**,
every control on each has been used, and every defect is written up in the format
above.

Report at the end of Pass 1 before starting Pass 2, so the window can be resized
and so the desktop findings are safe if the session is interrupted.

Finish with:

1. **The defect list**, numbered, ordered with "blocks work" first.
2. **The desktop-versus-phone gap table.** One row per control that is not
   `same`, grouped by screen:

   ```
   | Screen | Control | Desktop | Phone | Notes |
   |--------|---------|---------|-------|-------|
   | Messages → group header | Rename group | works | hidden | only appears on hover |
   | Finance → Write-offs | New write-off | works | absent | button not rendered |
   ```

   End it with a count per state — how many `absent`, how many `hidden`, how many
   `unusable`, how many `degraded` — and name the screens where the phone view is
   worst.

3. **A coverage table** — each of the 22 screens marked complete for both passes,
   or not reached with the reason.
4. **A count**: how many defects, split by severity.
5. **The three worst things you found**, in your own words.

Do not summarise your findings as "mostly working". Give the counts.

Report only. Change nothing beyond the test records you create, and name those.
