# Prompt for Hercules — project naming and group chat membership

Two changes, both about people not being confused when the team starts next week.
Item 2 is a defect: the backend was built to specification and the interface
never calls it.

---

# 1. Projects need a name, not only a number

Today a project has `projectNumber` and nothing else to call it. `projects` in
`convex/schema/projects.ts` carries no name field at all, so every screen shows
`PRJ-2026-0041`. Nobody at Magnus talks about a project that way, and with sixty
staff across three regions a number tells you nothing about which job it is.

**Show a name in this shape:**

```
{capacity}_kW_{Customer}_{Location}
```

For example: `480_kW_Calamba Agro Industrial Corporation_Calamba, Laguna`

## Where each part comes from

| Part | Source |
|---|---|
| capacity | `proposals.systemSizeKwp` on the project's `proposalId` — this is peak capacity in kilowatt-peak; show the number as it is stored, do not convert it |
| Customer | `parties.legalName`, reached through the project's `opportunityId` → `opportunity.partyId` |
| Location | `sites.local_government_unit` and `sites.province` on the project's `siteId` |

## Derive it, do not store it

Compute the name when the project is read. Do not add a `name` column that a
person types and then has to keep correct.

Two reasons. Locked principle L5 — accumulate, do not maintain — and the
practical one: when a variation order changes the capacity, or a customer's legal
name is corrected, a stored name silently goes stale while a derived one is right
the next time anyone opens the screen. That is what "renaming only shall change"
should mean: the name follows the data, and nothing else moves.

## `projectNumber` does not change, ever

It is structural. `nextDocNumber` in `convex/finance/finance.ts` uses it as the
prefix for progress claim numbers, billing milestone numbers and write-off
numbers, so changing it would break document numbering on existing records.

Keep it, show it as secondary text under the name, and keep it searchable. The
name is what a person reads; the number is what the documents carry.

## Blocking dependency: the site has no local government unit field

Section 8.3 specifies `site` as: *"site_id · account_id · address · **region
(derived from province, never typed)** · **local_government_unit** ·
distribution_utility · host_party."*

The built `sites` table has `address`, `province` and `region` and **no
`local_government_unit`**. One of the existing site records even carries the note
*"Local government unit: Calamba (no field)"* — someone hit this and wrote it into
free text.

Add `local_government_unit` to `sites`, expose it on the site form and on the
protocol's site tools, and use it as the first part of the location. It is needed
beyond naming: permits are filed per local government unit, and section 8 asks for
permit duration, requirement and fee accumulation *per office*, which cannot be
grouped without this field.

Until it is populated on a given site, fall back to `province` alone.

## Where the name must appear

Everywhere the project is currently shown as a number: the project list, the
project record header, search results, the project picker on any form, the
Messages channel for the project, notifications, the board pack and every
exception report. If a screen shows `PRJ-2026-0041` today, it shows the name with
the number underneath after this change.

The Drive folder follows the name — that is already specified and already true:
*"A renamed project renames its folder; Drive file identifiers do not change, so
no record breaks."*

---

# 2. Group chat membership — built, and unreachable

**This is a defect, not a new request.** The instruction was given, the backend
was built to it, and the interface was never wired to it.

## What was specified

> **A3 · Invite-only groups.** Any person creates a group, names it, and invites
> members. Only members see that the group exists, its membership and its
> messages. The creator is the owner; the owner may hand ownership to another
> member. Members may leave; the owner may remove a member, logged.

## What exists in the backend

`convex/communication/channels.ts` already has all of it:

| Line | Mutation |
|---|---|
| 355 | `inviteMember` |
| 381 | `removeMember` |
| 425 | `leaveChannel` |
| 460 | `handoverGroupOwnership` |
| 495 | `closeGroupChannel` |
| 1085 | `listChannelMembers` (query) |

## What the interface calls

**One of them.** `src/pages/messages/_components/ChannelPanel.tsx` line 604 calls
`listChannelMembers`. Nothing in `src/pages/messages/` calls `inviteMember`,
`removeMember`, `leaveChannel` or `handoverGroupOwnership` — a search of the whole
`src/` tree returns no hit for any of the four.

So a person can create a group and then never add anybody to it. The mutation that
would do it is written, tested by the compiler, deployed, and reachable by nothing.

## What to build

An information panel on every group, opened from the group header, holding:

1. **The member list** — every member by name and role, the owner marked. The
   query already exists; put it on screen.
2. **Add people** — a person search, multi-select, calling `inviteMember`. This is
   the one people will use most. It must be reachable in one tap from the group,
   the way it is in Google Chat and Messenger, not buried in a settings screen.
3. **Remove a member** — owner only, calling `removeMember`, logged as the
   specification requires.
4. **Leave group** — any member, calling `leaveChannel`.
5. **Hand over ownership** — owner only, calling `handoverGroupOwnership`.
6. **Rename the group** — see below; this one needs backend work first.
7. The two answerability rules already specified must be visible on this panel, so
   no member is surprised by them: that a group is closed and never deleted, and
   that a console holder may open a group they are not a member of only through a
   logged access-for-review action that requires a reason and notifies the owner.

## Rename is genuinely new

Unlike the five above, **rename was never specified and no mutation exists.**
There is no `renameChannel` or `updateChannel` anywhere in
`convex/communication/channels.ts`.

Build it: the owner may rename a group; the change is logged with the old and new
name; the rename is announced in the group as a system message, the way Google
Chat and Messenger do, so members are not confused by a group that changed name
overnight.

Project channels and department channels are **not** renameable by hand — their
names follow the project or department, and after item 1 a project channel's name
follows the derived project name automatically.

## Also missing: no way to manage membership over the protocol

`create_group` exists among the 400 tools. There is no `list_channel_members`, no
`invite_member` and no `remove_member`. Adding one person to five groups is
currently five manual operations in the browser; onboarding sixty staff is not
practical that way. Add the three tools, honouring the same ownership rules as the
interface.

---

## Report back with

1. An example of the derived project name as it appears on the project list, for
   a real project.
2. Confirmation that `projectNumber` is unchanged on every existing record and
   that document numbering still works.
3. The file and line of each of the six controls on the group information panel.
4. The rename mutation, and the system message it posts.
5. The three new protocol tools, with one call of each.
