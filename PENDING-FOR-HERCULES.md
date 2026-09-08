# Pending for Hercules — what is still owed

**8 September 2026 · Magnus Workspace Platform**
Not a prompt. This is the outstanding list: yours first, then mine, each checked against the
`convex/` source of 8 September and the live platform the same day.

---

# Part A — Karl's five

These are the things Magnus will actually use every day. Where the platform is already half
way there I have said so, because it changes the size of the job.

## A1. Archive a thread or space

**Wanted:** move an inactive thread or space into a folder so it stops cluttering the list.

**Today:** there is no archive of any kind. The only two things that come close are
`closeGroupChannel` — owner-only, group channels only, and closed for everybody at once — and
`leaveChannel`, which refuses anything that is not a group ("You can only leave group
channels"). Neither is what you asked for. You cannot tidy a direct message, an account space,
or General out of your own list, and closing a group hides it from the whole company rather
than from you.

**What is needed:** a per-person archive flag on the membership row — `archived`,
`archivedAt` — with the archived rows excluded from `listMyChannels` by default and reachable
under an "Archived" heading. It must be per person: your archive should not touch anyone
else's list, and it must never delete or close the space. Archiving must not suppress the
unread count when a new message arrives — a live thread should surface again.

## A2. Unread counts as numbers — General (5), and Message (X) on the dashboard

**Wanted:** `General (5)` in the list, and `Message (X)` on the dashboard where X is the total
unread.

**Today: most of this already works and is not being shown.** `unreadCount` is maintained on
the membership row on every send, cleared on read, returned per channel by `listMyChannels`,
and summed by `myUnreadCounts` into direct, spaces and mentions. The Messages page already
renders those badges.

**What is missing is only the surfacing:**
- **The left navigation has no badge at all.** `myUnreadCounts` is called by the Messages page
  and nowhere else. `AppLayout` never reads it. So you have to be inside Messages to see that
  you have anything.
- **The dashboard has no Message tile.** The Today page shows Open Tasks and Priority; it does
  not show messages.
- Give the nav item **Messages (X)** and the dashboard a **Message (X)** tile, both from the
  same `myUnreadCounts` query, with X = direct + spaces (mentions is a subset, do not double
  count).

This one is small and worth doing first — the data is already correct.

## A3. Task (X) on the dashboard that persists until the task is delivered

**Wanted:** `Task (X)` on the dashboard, X = tasks that person owes, and the number does not
clear until they are delivered.

**Today:** the Today page has an "Open Tasks" stat card driven by `listMyTasks`, and a
"Priority" card. Two problems:
- The nav item has no badge, same as messages.
- "Open" is a status filter. What you asked for is **owed** — assigned to me and not yet at a
  delivered state. That needs the count to be defined against the task's terminal states and
  to keep counting an overdue task, not to drop it when someone changes its status to
  something that is not "open".

**What is needed:** one query — tasks where `assigneeId` is me and status is not delivered or
cancelled — surfaced as **Task (X)** on both the dashboard and the nav, and unchanged by
anything except delivery or cancellation.

## A4. More than one company channel — Announcement, FAQ, Q&A

**Wanted:** several General-type channels for company-wide information.

**Today: the platform allows exactly one.** `ensureCompanyChannel` looks for an existing
channel of type `company` and returns it if it finds one, so a second can never be created
through that path, and there is no other mutation that creates one. `autoJoinCompanyChannel`
finds the company channel the same way and joins people to that one only — so even if a second
row were inserted directly, nobody would be a member of it.

**What is needed:** allow multiple company channels, each with its own name; auto-join every
person to all of them on first sign-in and on creation; and add a **post permission** on the
company channel, because Announcement and FAQ should be read-only for most of the company
while Q&A is open to everyone. That permission does not exist today — any member of a company
channel can post. This is the one item of your five that needs a real design decision, and it
is the one I would ask you to settle before Hercules starts: **who may post in each company
channel.**

## A5. A person card on People — number, email, photograph, how else to reach them

**Wanted:** click a person, see their number, email, picture and a note such as an alternative
way to contact them.

**Today: none of that data exists.** The `persons` table holds full name, display name,
aliases, population, employment basis, home region, sign-in email and status. **There is no
telephone number, no photograph and no notes field anywhere on a person.** The email that
exists is the sign-in address, which is not always the address you would use to reach someone.

**What is needed:**
- Add to `persons`: `mobileNumber`, `alternateNumber`, `contactEmail` (separate from the
  sign-in address), `photographFileId`, `contactNote`.
- A person card that opens from the People list and from a name anywhere else — a message
  author, a task assignee, an approver.
- **The photograph needs file storage.** There is no working file upload in the product except
  the chat composer, so this item carries the attachment work with it (see B14).
- Decide who may see a mobile number. My recommendation: everyone signed in can see it, and
  the change is audited — the point of the field is that people can be reached.

---

# Part B — My pending list

Ordered by what it costs the company if it stays broken. The numbers behind each are in the
Part 10 register in the Drive folder.

## B1. No gate anywhere has an approver — all thirty

**Corrected today, and it is worse than Part 9 said.** Part 9 reported that the five governing
gates had no approver. Checking every row this afternoon: the `primaryRoleName` and
`primaryPersonId` fields are **absent from all thirty gate rows**. Not one gate in the platform
knows who is allowed to approve it.

This is why `assignRole` refuses on the Administration screen, and every other screen that
tried to raise a gate properly would refuse the same way. It needs no code — the screen and the
roles both exist. It is still the single highest-value hour available.

## B2. Route every approval through `convex/foundation/gates.ts`

The engine is complete and correct: the R6 self-approval refusal in the specification's own
words, primary and alternate role checks, no-alternate respected. **A scan of every backend
file returns zero callers outside the file itself.** Seventeen approval points across six
modules take an approval reference as a plain string and never check anything. Twelve of them
were reported as separate defects; they are one decision made twelve times.

## B3. A role must take effect when the gate is answered, not before

`assignRole` raises a gate 24 request and inserts the `person_roles` row live in the same
transaction. Nothing treats a pending gate as not-yet-effective, and a refusal never revokes
the row. Because the grant is live immediately and R6 refuses the *requester* rather than the
*subject*, a newly granted Chief Operating Officer can approve the request that granted them
the role. One filter in `checkGateAuthorisation` and the two role-listing queries closes it.

## B4. Cryptographic erasure is ungated

`performErasure` destroys a person's encryption key permanently and makes their audit entries
unreadable for ever. It requires a reason string that is not blank. No gate, no role check, no
console holder, no second signature. It is the only irreversible operation in the platform.
Gate it, or remove the button until it is gated.

## B5. The compliance export leaks across tenants and is incomplete

Each table is read through its `by_tenant` index; when that index does not exist the code
catches the error and re-reads the table **unfiltered**, up to 1,000 rows. Fourteen exported
tables have no such index, including `audit_entries`, `encryption_keys` and
`supplier_bank_accounts`. Harmless on one tenant; on the day there are two, the artefact whose
purpose is to be handed to an outsider carries another company's data.

Separately: the export names 98 tables against a schema of 116. Three of the 98 do not exist.
Twenty-one real tables are missing, including every operations-and-maintenance table and
`payroll_lines` — the actual pay amounts.

## B6. Settle the register — `seed.ts` is the specification

Twenty-five of the thirty live gate labels differ from `seed.ts`. Eleven gate numbers mean
something different in the module that uses them than in the specification. Gate 24 means Role
Assignment in one place and Employment Offer in another; gate 32 has three claimants. State the
rule once — *the thirty rows in `seed.ts` are the register* — and thirteen open questions become
mechanical corrections.

## B7. A project can never leave design

The only stage mutation in the platform is setup → design. Nothing sets a project to
procurement, construction, commissioning or handover. Everything in Parts 5 to 8 is downstream
of a stage that cannot advance.

## B8. A goods receipt does not move stock

Procurement and inventory share no data at all. Material is received, and somebody has to
notice and type it in again as an adjustment or a count. This is the largest single gap in the
daily work of the warehouses.

## B9. There is no accounts payable

The platform cannot record or pay a supplier bill. Committed cost is computed from issued
orders; nothing records what is actually owed.

## B10. Four of the six hard blocks have no code

Hard blocks 1, 2, 3 and 4 exist as rows and as helper functions that nothing calls. All six
live rows carry a different label and a different meaning from the six the specification names,
and the specification's block 3 depends on a block B0 that does not exist in the construction
spine.

## B11. Two data corrections on the live platform

- **`markup_major_equipment` has a version that begins 1 January 2030 and ends 7 September
  2026.** From 2030 the dated lookup for that key throws instead of returning a number. Caused
  by the protocol tool patching values in place instead of versioning them.
- **The four statutory rate tables in the live database are the deliberately fake ones** from
  the first agent's testing, and they are approved and therefore immutable. Payroll is computing
  against invented brackets.

## B12. The protocol surface must call the same mutations the screens call

Not reimplement them. Today: `update_system_constant` overwrites history instead of versioning;
`update_document_revision` takes status as free text and can set a revision in force without
the unclassified refusal or the supersede step, permanently breaking that document;
`create_person_role` raises no gate and checks no duplicate; `create_role` has no uniqueness
check on the machine name while the screen path does — and gate authority resolves by that
name; `update_person_role` accepts `revoked: false`, ignores it, and reports success.

## B13. Nobody is notified at any hand-off

Every one of the eight process parts ends with the same line. A proposal, an order, a site
report, a payroll period, a service visit — all sit waiting for an approver who is never told.
This is the defect that makes every other approval slow.

## B14. Nothing can be attached, sent or printed

The only working upload in the product is the chat composer. There is no way to send a purchase
order to a supplier, to give a worker a payslip, to send a client an invoice or a signed-off
service report, to attach a design deliverable, a permit, or the toolbox photograph the schema
already has a field for. Karl's A5 photograph sits on top of this.

## B15. Console holder add and remove check nothing

Neither `addConsoleHolder` nor `removeConsoleHolder` checks that the caller is a console holder.
While fewer than two exist, any signed-in person can add themselves — and a console holder may
then use `directAssignRole`, which bypasses gate 24 by design.

## B16. Smaller, still real

- No document reclassification path exists; gate 33 is named for an act the platform cannot
  perform.
- Legal hold is a free boolean any signed-in person can set or clear, with no reason.
- `revokeRole` needs nothing at all — taking authority away is easier than granting it.
- The progress claim screen passes a project id where a contract id is required, so a claim
  cannot be created from the interface.
- Purchase order numbers are counted per project, so two projects in the same month both
  produce `PO-202609-001`.
- Seven of the thirty-two roles are held by nobody.

---

# What I would put in front of Hercules first

1. **B1** — configure the thirty gates. No code. One afternoon. It unblocks every approval
   screen in the product.
2. **A2** — surface the unread counts. The data is already right; this is display only.
3. **B4** — gate the erasure, or hide it.
4. **B5** — delete the unfiltered fallback in the export.
5. **B2** — then the seventeen approval points, as one change.

A1, A3, A4 and A5 are the daily-use work and should run alongside, because they are what
Magnus will actually touch. A5 needs the attachment work (B14) for the photograph, and A4 needs
your decision on who may post in each company channel.
