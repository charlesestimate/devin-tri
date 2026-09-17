# Magnus Workspace Platform — Hercules build specification, round 3

## Part 2 of 4 · Sign-in and access · The logged-out screen · The dashboard · Global search · The task indicator · Full configuration

**Prepared for Karl Ivan Estadola, Chief Executive Officer, Magnus Renewable Tech Corp · 17 September 2026**

Second of four parts. **Build after Part 1, in its own thread.** Section B1 is the most important item in the whole round: people Karl has granted access to cannot get in, and the cause is now known to the line. Line numbers are from the source exported on 8 September 2026 — no build has run since 5 September — verify each before editing.

### How to use this document with Hercules

Build mode, new thread, paste the whole part. Hercules reads the cited file and line, fixes the root cause, and pastes the evidence asked for in section G. One part, one thread, one report.

### Standing rules that still apply

No scheduler, timer or automation. Every write carries a human's name through the tenant wrapper. A record with no current role has no access — never default access. No presence, location or login-time tracking. No abbreviations or ampersands. Where silent, ask.

---

# A. WHAT WAS FOUND ON THE LIVE PLATFORM — 17 SEPTEMBER 2026

Checked over the protocol, read-only. Of 69 persons, **48 are flagged `signsIn = true`**. Their identity links:

| State | Count | Who |
|---|---|---|
| Linked and active | 20 | Alma Codog · Kidron Magnus · Christianah Alake · Alfie Jie Villalon · Beda Escobedo · Cristy Jasareno · Erika Arjona · Amy O. Calintig · Michael Bryan L. Cataquiz · John Rex Cabrela · Reymund Reola · Shairra Macuha · Caroline B. Pinero · Austin · Al Jay Mabansag · Jmrosvil Seguisa · Sheina Mae Avenido · Jiemma Seguisa · Candice Kate D. Velasco — plus Karl (bootstrap, no link row needed) |
| **Link `pending` — granted, never completed a sign-in** | **5** | **Jennifer Morante (`Jennifer.magnuscorp@gmail.com` — capital J)** · Felicidad P. Rubio (`fhel.magnuscorp@gmail.com`) · Felicity C. Abordo (`felicitymagnuscorp@gmail.com`) · Dexter P. Broce (`dexterbroce.magnuscorp@gmail.com`) · Procurement Department (`procurement.magnuscorp@gmail.com`) |
| **Flagged `signsIn` but no identity link at all — cannot sign in, ever** | **23** | Jefferson Quicay · Erline Mae Diaz · Vivien-Vick Jebulan · Nino Javier · James Fullon · Kimberly A. Josol · Mark Joseph S. Castro · Henry Pepito · Denbert Estrada · Carlito Pilapil · Adrian Glenn Obra · Reynan Balucan · Rose Dianne M. Torres · Jeanille Ariane Tamayo · Nolianne Jhon · Xydric Gonzales · Alejandro Oso · Jubert A. Perez · Christine Mae C. Dingding · Jhoniver Bantaya · Joey A. Leonardo Jr. · Jessie Carinola Jr. · Jones Pedrina |

The General channel has 69 members — every person — so once a person is linked, Messages works for them.

---

# B. DEFECTS AND FIXES

## B1 · "Granting access to people is not working" — the most important item

**How access is meant to work.** A console holder grants sign-in on Administration → Persons (`convex/foundation/identity.ts` `grantSignIn`, line 111), which writes an `identity_links` row with the email and state `pending`. When the person signs in with Google, `convex/users.ts` `updateCurrentUser` (line 172) looks up the pending link by the email on the sign-in identity, activates it, stamps `identitySubject` on the person, and links the `users` row to the tenant and person. From then on every query resolves the tenant.

**Why it fails — four causes, all in the code, one confirmed on live data:**

1. **The email match is exact and case-sensitive.** `users.ts` lines 226 and 286: `.withIndex("by_email", (q) => q.eq("email", identity.email!))`. `grantSignIn` (identity.ts line 138) and the protocol's `toolGrantSignIn` (`convex/mcp/group1Internals.ts` line 253) store the address **exactly as typed**, with no trimming and no lowercasing. Google returns the address in lowercase. **Jennifer Morante's link is stored as `Jennifer.magnuscorp@gmail.com` and can never match** — that is the live defect behind "I granted access and it did not work."
2. **`signsIn` is a flag, not a grant.** Twenty-three persons carry `signsIn = true` with no link row. The flag was set (on the person form or through the protocol's `update_person`) without `grantSignIn` ever being called, and nothing on the People list shows the difference. Those people were told they had access; the platform has never heard of their addresses.
3. **A wrong grant cannot be corrected.** `grantSignIn` refuses when a non-revoked link exists for that email (line 128) and there is no `revoke_sign_in` protocol tool; on screen, `revokeSignIn` (line 174) exists but is not reachable from the Persons list. A mistyped address is permanent from the protocol's side.
4. **The person sees the wrong message.** An unlinked account gets `FORBIDDEN — Account not associated with a tenant` from `requireTenantContext` (`convex/lib/tenantEnforcement.ts` line 33) as a crash on screen, and empty lists everywhere `tryGetTenantContext` is used. Nothing tells them, or the console holder, which address they signed in with.

**Fix.**

1. **Normalise every email at both ends:** `trim().toLowerCase()` in `grantSignIn`, `toolGrantSignIn`, the migration import, and in both lookups in `updateCurrentUser`. Add a one-time data correction that lowercases every existing `identity_links.email` and `persons.pendingSignInEmail` (Jennifer's link then matches on her next sign-in).
2. **`signsIn` becomes derived, never set by hand.** Remove it from the person form and from `update_person`. Show on the People list, per person: *Sign-in: not granted · granted, waiting for first sign-in (address) · active (address) · revoked.* Derived from `identity_links`. For the 23 flagged persons with no link, the list shows *not granted* and the Grant control — Karl then grants each one from the screen with the correct address.
3. **Grant, correct and revoke from the Persons list and the protocol:** `grant_sign_in(personId, email)` · `revoke_sign_in(personId, reason)` · **`correct_sign_in_email(personId, email)`** which revokes the pending link and grants the new address in one mutation, logged. A person with an *active* link cannot be re-granted without revoking first.
4. **When a signed-in account has no link, the platform says so and records the address.** `updateCurrentUser` writes an audit entry `sign_in.unlinked` carrying the identity email; every page that hits an unlinked account renders one screen — *Your sign-in ([address]) is not yet linked to a person record. Ask a console holder to grant sign-in for this address.* — with no module content. Administration → Persons shows a panel **Unlinked sign-ins** listing every `users` row without a `personId` (name, email, first seen) with a one-tap *Link to person* that calls `grant_sign_in` with that exact address. This turns the failure Karl saw in the office into a two-click fix.
5. **Sign-in email absent.** Where the identity carries no `email`, refuse with *Your account has no email address; sign in with a Google account that has one* — do not leave the person on an empty screen.
6. **A record with no current role has no access.** `getMyVisibleObjectTypes` (identity.ts line 831) returns `[]` for a person with no roles, and `AppLayout.tsx` lines 120–131 then **shows every module** (`permissionsSeeded` false → all visible). Reverse it: no roles, or roles with no permission rows, means an empty sidebar and the sentence *No role has been assigned to you yet. Ask your department head.* Until the permission rows are seeded for every role (Part 3 §C6), seed a `view` permission on every module for every existing role so nobody loses what they have today — then the rule can hold.

## B2 · "If you are not logged out, an outsider can view the modules"

**Root cause.** `src/components/layout/AppLayout.tsx` lines 236–241 render `<StaticNav>` — the full eighteen-item module list — under both `<AuthLoading>` and `<Unauthenticated>`; the header (search bar, theme picker) renders regardless; `src/pages/Index.tsx` renders the four feature cards to an unauthenticated visitor; and `src/App.tsx` line 71 leaves `/om/*` outside the `<Authenticated>` wrapper the other routes have. The routes themselves render nothing to a visitor, but the shell tells them what the platform contains.

**Fix.** Unauthenticated: one full-screen sign-in page — the company name, one Sign in button, nothing else; no sidebar, no header, no module names, no search, no theme control. AuthLoading: a spinner on a blank page. Wrap `/om/*` like every other route and remove the page-level `<Authenticated>` inside it. Every deep link followed while signed out lands on the sign-in page and returns to the requested path after sign-in. **After session expiry the same page appears** — a stale tab must not keep showing the shell.

## B3 · "The dashboard shall have my tasks, awaiting my approvals, and notifications"

**Root cause.** `src/pages/Index.tsx` is a greeting and four marketing cards (*Pipeline & Projects* — with an ampersand — *29 configured gates*, and so on). It reads nothing but the person's name.

**Fix — the Dashboard becomes the person's landing screen, in this order, computed on read:**

1. **Overdue** — tasks assigned to me past their current date; approvals waiting on me past the gate's recorded window.
2. **Awaiting my approval** — every pending `approval_requests` row where I am the current approver or the alternate, from a new query `listMyPendingApprovals` (request, gate name, what is being approved, value, who raised it, age in working days, window) — each row opening the approval detail with the full object. This is *My Approvals* from section 13; the same list is the `/approvals` screen.
3. **Due today** — tasks with current date today.
4. **Blocked, waiting on someone else** — my tasks in `blocked`, with the named blocker and expected clear date; and tasks blocked on me.
5. **Coming** — due this week.
6. **Three counters at the top, all live and all opening their list:** **Task (X)** (§B5) · **Awaiting my approval (X)** · **Notifications (X)** (uncleared `action_required`) · plus **Message (X)** from Part 1. No ranking, no cap, no summary: if there are forty, show forty.
7. Landing screen per role stays configurable (Person In Charge → Today; the rest → Dashboard by default). Remove the four cards and the ampersand.

## B4 · "The general search box in the upper right corner is not functioning"

**Root cause.** `AppLayout.tsx` line 400 `GlobalSearchBar` is a `<Button>` with the text *Search…* and a ⌘K label. It has no handler, no input and no query. The only search backends are `searchMessages` (channels.ts 1429), `searchThreadMessages` (threads.ts 604) and `searchParties` (pipeline/parties.ts 52).

**Fix.** One server query `globalSearch(query)` returning up to ten results per type, **permission-scoped at the query — a result the person may not open does not appear**: projects (derived name and number) · blocks · people (display name, aliases, nicknames — the pilot ground rules ask for nickname search) · documents (number and title) · purchase orders · items · permits · messages (text and attachment names, membership-scoped) · tasks · accounts and sites. The bar opens a command palette on click or ⌘K / Ctrl-K, searches after two characters, groups results by type, and every result is a deep link. Recent items shown when empty. Works on the phone.

## B5 · "There is a task indicator on the profile, but opening it does not show the specified task"

**Root cause.** `src/pages/today/page.tsx` lines 117–125: the *Open Tasks* card shows `myTasks.length` — **every task ever assigned, including `done` and `cancelled`** — and links to `/tasks`, whose list is filtered. The number and the list are two different questions.

**Fix.** One query `myOwedTasks`: `assignedPersonId = me` and status not in (`done`, `cancelled`). It drives the Today card, the sidebar **Task (X)**, the dashboard counter and the default view of `/tasks`. The number opens exactly the list it counted. Overdue tasks stay in the count until delivered or cancelled.

## B6 · "I cannot access the full configuration of the platform"

**Root cause.** Administration (`src/pages/admin/page.tsx` lines 44–57) has twelve tabs: System Constants, Gates, Hard Blocks, Roles, Persons, Console Holders, Tenants, Audit Chain, Agent Sessions, Integrations, Compliance, Setup and Migration. Karl is a console holder, so nothing is hidden from him — **the missing configuration screens do not exist.** Section 8.19 and section 13 require the following and none is built:

| Missing screen | What it configures | Gate |
|---|---|---|
| **Thresholds by domain** | The approximately thirty operational thresholds in `configuration_values` — overdue receivable days, uncertified claim days, waiting thresholds for sealing engineer and client, transit days per route class, liquidation days, insurance threshold for hard block 1, priority limit per requester, renewal notice days, plan intervals | 31 |
| **Labels and terminology** | Every interface label as a controlled set; the place a wrong word is corrected once | 31 |
| **Controlled lists** | Weather, loss reasons, decline reasons, closing reasons, blocked reasons, capability list, permit types | 31 |
| **Push list** | The categories that send a device push; the three carve-outs shown as non-removable | 31 |
| **Landing screen per role** | Defaults per section 8.2 | 31 |
| **Working calendar** | Holidays; every window in working days uses it | 31 |
| **Roles and permissions with money visibility** | Per role: object type, action, record scope, money visibility — today the Roles tab lists roles and `setRolePermission` exists (identity.ts line 717) but there is no grid | 32 |
| **Statutory rate tables** | Human Resource enters, Finance approves; today only reachable inside Payroll and the live tables are the fake ones (Part 3 §C8) | dual control |
| **Retention schedules and legal holds** | `[CONFIGURED]` pending counsel; holds set only by a console holder with a reason | — |
| **Change log with arrival channel** | Every configuration change: what, previous, new, who, when, reason, channel | — |
| **Access review** | Per person: current roles, permissions granted, what they used in the period | 32 |

Also on the existing tabs: the **Gates** tab must show primary and alternate on every row, refuse an alternate with a lower limit at save (R3), and refuse reconfiguration by anyone but a console holder under gate 31 (Part 3 §C3); the **Hard Blocks** tab must show six read-only rows with only the value editable and no enable, disable or delete control; the **Persons** tab gains the sign-in state column, the Grant, Correct and Revoke controls, and the Unlinked sign-ins panel (§B1).

**Fix.** Build the eleven screens above, each writing through the same mutations the protocol's configuration tools call, each change logged with a reason where the field requires one. No bulk import.

---

# C. THE ACCESS LIFECYCLE — RULES THAT HOLD AFTER THIS PART

- Onboarding: Human Resource creates the person · a console holder grants sign-in with the address · the department head assigns roles under gate 24 (Part 3 §C2 — the grant takes effect on approval) · the person appears with access only after a role is approved.
- The identity provider is a property of the tenant; the only field that knows the provider's user identifier is `persons.identitySubject`.
- Disabling the provider account ends the session and moves the person to `suspended` with no administrator action.
- Departure: identity disabled → `suspended` · Human Resource sets `departed` · every open task, approval and deliverable owned by the person is listed and must be reassigned before offboarding completes (refusal 4) · console seat removed with a replacement named first · agent sessions revoked · record retained.
- Quarterly access review under gate 32.

---

# D. DATA CORRECTIONS KARL CAN MAKE THE DAY THE FIX SHIPS

1. Jennifer Morante — after the lowercase correction, ask her to sign in again; the pending link activates.
2. Felicidad P. Rubio, Felicity C. Abordo, Dexter P. Broce, Procurement Department — ask each which Google address they used; if it differs from the link, use *Correct sign-in email*; then they sign in.
3. The 23 with no link — grant sign-in from the Persons list with each person's `@gmail.com` address as they appear in Karl's staff table; field crew who never open the platform (solar installers) get no grant and `signsIn` derives to false.

---

# E. TESTS THAT DECIDE THIS PART

- **A1 Grant and sign in.** Grant `Test.Person@Gmail.com`; sign in as `test.person@gmail.com` — linked on first sign-in; the audit shows the normalised address.
- **A2 Flag is derived.** Search the schema and every form for a writable `signsIn`; none. The People list shows the four sign-in states from `identity_links`.
- **A3 Correct.** Grant a wrong address; correct it; the old link is `revoked`, the new is `pending`; one audit entry.
- **A4 Unlinked screen.** Sign in with an ungranted account — the sentence with the address, no module content; Administration shows the account under Unlinked sign-ins; one tap links it.
- **A5 No role, no access.** A linked person with no approved role sees an empty sidebar and the sentence; grant a role under gate 24 and approve — the modules the role may view appear.
- **A6 Logged out.** Open every route signed out — the sign-in page only; no module names in the DOM; `/om/*` behaves like the rest; a stale tab after expiry shows the sign-in page.
- **A7 Dashboard.** Assign two tasks, raise one approval to me, mention me once: the three counters read 2, 1, 1; each opens the list it counted; the sections appear in the specified order; nothing is ranked or capped.
- **A8 Search.** Type a nickname, a project number, a purchase order number and a word from a group message: results appear grouped, each opening its record; a person outside the group sees no message result; a person with `money_visibility` `none` sees no monetary value in any result.
- **A9 Task (X).** Three open, one done, one cancelled — the indicator reads 3 and the list it opens shows the same three.
- **A10 Configuration.** Each of the eleven screens exists; change one value on each; the change log shows what, previous, new, who, when, reason and channel; an alternate with a lower limit on a gate is refused at save.

---

# F. WHAT NOT TO DO IN THIS PART

Do not add password sign-in, a recovery flow, a "user" concept separate from `person`, a default role, default access for a person with no role, any presence or login-time metric, an email invitation (no outbound mail exists), or a self-service "request access" form that creates a person — persons are created by Human Resource, and sign-in is granted by a console holder.

---

# G. REPORT BACK — PASTE THE EVIDENCE

1. The `identity_links` rows for Jennifer Morante before and after the correction; her `users` row after her next sign-in.
2. The People list rendered for Administration, showing the sign-in state column for every one of the 48 flagged persons.
3. The Unlinked sign-ins panel with at least one real row and the audit entry from linking it.
4. The DOM of `/projects` while signed out (no module names) and the same after sign-in.
5. The dashboard for Karl with the three counters and the five sections, with the queries behind each.
6. Search results for `Kidron`, `PRJ-2026-0001`, `PO-`, and a word from a group message, as two different people.
7. The `myOwedTasks` query and the Today card, sidebar and `/tasks` default list all reading it.
8. A screenshot or rendered list of every Administration tab after this part, and one change-log row per new screen.
9. Tests A1 to A10 above — results pasted.
