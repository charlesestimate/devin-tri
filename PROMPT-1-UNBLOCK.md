# Unblock an empty tenant — seven changes, then publish

Two independent testers swept the whole platform on `bug-test` overnight and raised
63 findings. Almost all of them are downstream of a small number of causes. This
prompt is **only the seven that unblock the platform**. Everything else is being
held deliberately, because the testers are going back in after you publish this and
unrelated changes would invalidate their second sweep.

**Build all seven. Do not redesign anything. Do not fix anything not listed here.
Do not come back with a plan — build it, publish it, and report against section 8.**

---

## 1. Seed every tenant when it is created

This is the largest problem on the platform and it is not missing code.

`convex/foundation/seed.ts` already contains `seedFoundation`, which creates the
**thirty gates**, the hard blocks, the system constants (`specific_yield` is at
line 451), the roles and the Philippine public holidays. It is complete and it is
correct. **Nothing calls it when a tenant is created, and nothing in the interface
exposes it.**

The consequence, verified by both testers on a fresh tenant: Create Proposal fails
with `System constant specific_yield is not configured`. No proposal means no won
opportunity, no project, no contract — so **Projects, Tasks, Design and
Engineering, Procurement, Construction, Operations and Maintenance and Finance are
all permanently empty**, and Raise Safety Stop cannot be used because it demands a
project. Eight screens, one cause.

### What to change

**1a.** The five seeding sections of `seedFoundation` are already written as
per-tenant loops — gates (line 331), hard blocks (414), system constants (483),
roles (667) and public holidays (714) — and each already checks for an existing row
before inserting (see lines 334–340). **Extract the body of those loops into one
exported internal helper:**

```
seedTenantFoundation(ctx, tenantId, { now, goLiveDate })
```

It must remain idempotent: running it twice must insert nothing the second time.
Keep every existing check.

**1b.** Call it from `seedFoundation` once per tenant. This is a refactor with no
behaviour change — the seed must still produce identical results.

**1c.** Call it from **both** places a tenant is inserted:
`convex/foundation/tenants.ts:25` (`createTenant`) and
`convex/foundation/tenants.ts:102` (`ensureOrCreateTenant`). Those are the only two
inserts into `tenants` in the codebase. After this, no tenant can exist unseeded.

**1d.** Fold **trades** into `seedTenantFoundation` as well. `manpower.ts:67
seedTrades` seeds eight trades that every tenant needs and is currently a button a
tester had to press twice before it worked. Seeding them at creation removes the
button and the bug together. Leave `seedLocations` as a button — warehouses are
specific to each company.

**1e.** Add one operation, **"Seed System Constants"**, to Administration → Setup
and Migration, calling `seedTenantFoundation` for the current tenant, for tenants
that already exist. Because it is idempotent this is safe to run on production.

**1f.** Surface the check you already have. `convex/foundation/tenants.ts:117`
defines `isSeedComplete`, which reports whether a tenant has its gates. **Nothing in
`src/` calls it.** Call it on Administration → Setup and Migration and show the
result plainly — *"This workspace is fully configured"* or *"This workspace is
missing its system constants, roles and gates. Run Seed System Constants."*

**1g.** When a mutation fails on a missing constant, say what to do. Replace
`System constant specific_yield is not configured` with a sentence naming the
screen: *"This workspace has not been configured yet. An administrator must run
Seed System Constants on the Administration screen, under Setup and Migration."*

---

## 2. Two unguarded reads that take the whole application down

Reports → Exception Report **white-screens the entire application** — sidebar,
header and every control. The only way out is a browser reload. Reproduced twice.

The console text was:

```
[CONVEX Q(reports/reports:safetyExceptions)] Server Error
Uncaught Error: Invalid argument id for db.get: Unable to decode ID: Invalid ID length 8
  at async get (../../convex/lib/tenantDb.ts:97:11)
  at async handler (../../convex/reports/reports.ts:312:14)
```

**The cause is exact.** `convex/schema/safety.ts:73` declares
`projectId: v.optional(v.id("projects"))`. Two lines in `reports.ts` read it as if
it were required:

```ts
const project = await db.get("projects",
  (incident as Record<string, unknown>)["projectId"] as Id<"projects">);
```

That is at **line 311 (rule S2) and line 342 (rule S3)** in my copy of the file;
confirm against the branch, it may have drifted by a line. Two casts in one
expression — the first discards the type, the second asserts that a missing value
is present. TypeScript would have caught this and was told twice not to.

`"projects"` is **eight characters**. When `projectId` is `undefined`, the table
name itself reaches the ID decoder — which is precisely the error message above.
One incident filed without a project takes the report down, and Incidents correctly
make the project optional.

### What to change

**2a.** Guard both lines. Do not fabricate a project; a safety exception on an
incident with no project is still a valid exception. Show the project number when
there is one and leave it blank when there is not.

**2b.** Remove the `as Record<string, unknown>` and `as Id<"projects">` casts on
those two reads and let the schema's own optional type flow through.

**2c.** Then search `convex/` for the same shape — a `db.get` whose id argument is
a field the schema declares `v.optional`. There are 411 `as Id<…>` casts in
`convex/`; most are harmless. **Report how many sit on optional fields and fix
them.** Do not change casts that are not this pattern.

---

## 3. There is no error boundary anywhere in the application

I searched `src/` for `ErrorBoundary`, `componentDidCatch` and `errorElement`.
**There are none.** That is why item 2 is an outage rather than a broken panel, and
it is why a route change shows a blank pane for up to five seconds and a cold load
shows a dark screen for eight to twelve seconds with nothing on it.

### What to change

**3a.** One error boundary at the route level, so a failing screen never takes the
navigation and header with it. It must show what failed, and offer a control that
returns to the previous screen without a browser reload.

**3b.** One boundary around each tab panel, so a failing tab leaves the other tabs
usable — the Exception Report should have failed while Board Pack kept working.

**3c.** A loading state for the initial application mount and for route changes.
Anything is better than a dark screen: a skeleton, a spinner, the Magnus mark.

This is the highest-value item in the prompt. It does not fix a bug — it converts
every future bug of this class from an outage into a panel that says something went
wrong.

---

## 4. The platform is on Coordinated Universal Time, not Philippine time

At 01:16 on Saturday 5 September, My Day said 5 September and Reports evaluated at
5 September — but the Site Assessment saved as **4 September** and New Permit to
Work defaulted its Issue Date to **04/09/2026**. The code stamps and defaults dates
with `new Date().toISOString()` (for example `convex/safety/safety.ts:322`).
Philippine Standard Time is Coordinated Universal Time plus eight hours.

**Between midnight and 8 a.m. Philippine time, every date default on this platform
is yesterday.** A permit to work is same-day and expires at the end of its issue
date, so a permit raised at 6 a.m. — which is when site crews raise them — is born
expired. Every site report and assessment filed before 8 a.m. is dated the day
before.

### What to change

**4a.** One date helper that returns today's date in Philippine time, and use it
for every date default and every date-only stamp across the platform. Sweep for
`new Date().toISOString()` and for date defaults computed in the browser.

**4b.** Timestamps that record a precise moment stay in Coordinated Universal Time.
This is about **date-only** fields — issue dates, incident dates, assessment dates,
period dates — not about `createdAt`.

**4c.** Say which one you are showing. Anywhere a date is displayed to a person, it
is Philippine time.

---

## 5. A safety stop cannot be raised at all

Safety → Raise Stop opens a dialog that states **"Any person may raise a safety
stop"** and then requires a Project. This is the first Quick Action on My Day and
the one control on the platform that exists for an emergency.

Incidents already make the project optional and work correctly. Make Raise Safety
Stop match: **Project optional, everything else unchanged.** A safety stop raised
with no project is still a safety stop.

This is not made redundant by item 1. Projects will exist after item 1, but a
person stopping work does not always know which project they are standing on, and
must never be blocked by a dropdown.

---

## 6. Separate Clear All Test Data from the seeding operations

**Correction to what a tester reported.** One tester described Clear All Test Data
as "one click, irreversible". That is what the screen looks like, but it is not what
the control does — the tester never pressed it. **The confirmation already exists and
is well built:** `src/pages/admin/page.tsx:2110` requires the person to type
`CLEAR ALL TEST DATA` exactly, the button stays disabled until it matches (line 2122),
and `convex/foundation/clearTestData.ts:28` re-validates the phrase on the server.
**Do not build a confirmation. It is already there.**

Two smaller things are worth changing.

**6a.** It sits in the same scrolling list as Seed Roles, Backfill General Channel and
Seed Project Names. Move it out of that list, to the foot of the screen, visually
separated and plainly marked as destructive. Presentation only — do not touch the
confirmation logic.

**6b. `trades` is in the wrong list.** `convex/foundation/clearTestDataInternal.ts`
clears `trades` along with the operational data. Trades are reference data, like roles
and gates, and the header comment of `clearTestData.ts` says reference data is
preserved. **Move `trades` out of `TABLES_TO_CLEAR` and into the preserved set**, so
that clearing test data does not leave a workspace unable to add a worker.

## 7. The landing page says twenty-nine gates. There are thirty.

`src/pages/Index.tsx:12` contains a hardcoded string:
`"29 configured gates, full audit trail"`. It is not a live count.

The specification is exactly thirty — 1 to 12, 18 to 24, 25a, 25b, and 26 to 34.
`seed.ts` says *"Exact 30 rows per F3.1"*, and your own health check at
`tenants.ts:117` treats a tenant as configured when `gateCount >= 30`. Administration
is right; this string is wrong.

While you are in those three lines: they also ship **"EPC"** and **"PTWs"** on the
front page of a platform whose specification forbids abbreviations. Write them out —
"engineering, procurement and construction", "permits to work".

Change nothing else on that page. The four cards being decorative rather than
clickable is known and is being handled separately.

---

## 8. What to report back

Do not report that these are done. Report each one with its proof.

1. **Seeding.** Create a brand-new tenant. Without pressing any seed control, say
   how many gates, hard blocks, system constants, roles, trades and public holidays
   it has. Then create a proposal on it and paste what happened.
2. **The refactor is safe.** Confirm `seedFoundation` still produces identical
   results, and that running `seedTenantFoundation` twice inserts nothing the second
   time.
3. **Exception Report.** File an incident with **no project**, then open Reports →
   Exception Report and say what you see. Then say how many `as Id<…>` casts you
   found sitting on optional fields, and which you changed.
4. **Error boundary.** Force a query to throw on one tab and confirm the sidebar,
   the header and the other tabs still work.
5. **Time.** State the current Philippine date and time, then open New Permit to
   Work and say what date it defaults to.
6. **Safety stop.** Raise one with no project and say whether it saved.
7. **Clear All Test Data.** Confirm you did **not** change the confirmation logic,
   and that `trades` is now preserved rather than cleared.
8. **Gates.** Say what the landing page reads now.

If any item cannot be built as written, say which and why **before** publishing the
rest. Do not substitute a different fix for one of these without saying so.
