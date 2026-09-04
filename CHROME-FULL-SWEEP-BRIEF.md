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

---

## Rules — read before you touch anything

This is a live platform with **45 real employees** in it, real customer records
and real conversations. Some staff are already using it.

**Never:**

- Send a message in **General**, or in any space with real colleagues in it.
  They receive notifications. Use only the space named **Platform Bugs**.
- Remove a person from a group, revoke a role, or change anyone's access.
- Delete a thread, a space, a person, a project or any record you did not create.
- Approve, reject, sign off or release anything.
- Change a system constant, a threshold, or anything under Administration that
  alters how the platform behaves for other people.
- Upload anything confidential. A small test image is fine.

**Always:**

- Prefix anything you create with `ZZTEST` so it can be found and removed later.
- Prefer reading over writing. Where a form must be submitted to test it, submit
  the smallest valid record you can and record its identifier.
- Stop and report if a control looks destructive and its label is unclear.

**One thing to know:** the approval machinery is not connected. Nothing you
approve is authorised, and nothing the platform refuses is necessarily refused
for the right reason. Record what you observe; do not assume the platform's
behaviour reflects a rule.

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
2. **A coverage table** — each of the 22 screens marked complete, or not reached
   with the reason.
3. **A count**: how many defects, split by severity.
4. **The three worst things you found**, in your own words.

Do not summarise your findings as "mostly working". Give the counts.

Report only. Change nothing beyond the test records you create, and name those.
