# Final messaging fix — implement all of this, then publish

Your diagnosis was correct. `hidden group-hover:flex` and the hover-gated message
toolbar are the cause: there is no hover on a touch screen, and most of Magnus
works from a phone. Everything below follows from that plus four decisions the
Chief Executive Officer has now made.

Do not come back with another plan. Build it, publish it, and report.

---

## 1. Group ownership and control — decided, and it changes the model

The Chief Executive Officer has decided, overriding section A3 of the earlier
instruction:

- **Any member may rename a group or space.** Not only the owner.
- **A group may have more than one owner.**
- **Every console holder is automatically an owner of every group**, including
  groups they did not create and were not invited to.

The reasoning is that this is a company platform, not a private messaging
service, and the company must retain control of its own conversations.

**Implement it this way.** `channels.ownerId` is a single optional field and
cannot express multiple owners. Add `isOwner: v.optional(v.boolean())` to
`channel_members` and treat that as the authority. Keep `channels.ownerId` as the
record of who created the group; do not delete it. Every console holder resolves
as an owner whether or not a membership row exists.

**Then correct what the panel tells people.** The Group rules text currently
reads: *"A console holder may access a group for review only through a logged
action that requires a reason and notifies the owner."* After this change that is
no longer true, and leaving a privacy promise on screen that the platform does not
keep is worse than making no promise. Replace it with an accurate statement —
that console holders have full access to every group as owners, and that groups
are closed rather than deleted. Every member should be able to read what is
actually the case.

## 2. Make the controls visible without hover

`GroupInfoPanel.tsx` line 233 wraps remove and hand-over in
`hidden group-hover:flex`. Line 164 gates rename on `isOwner`.

- Remove member, and add or remove an owner: **always visible** on each member
  row, at touch-target size. No hover.
- Rename: always visible beside the group name, for any member.
- All of it must remain reachable on a phone-width screen in a panel that already
  scrolls.

Every one of these mutations already exists in
`convex/communication/channels.ts` at lines 355, 381, 425 and 460. This is
wiring and gating, not new backend work.

## 3. Sweep the whole interface for hover-hidden actions

This is the highest-value item in the list. The two instances above were found by
accident; there will be more, and every one is invisible to the people who work
from a phone.

Search every file under `src/` for `group-hover`, for `hover:` used to reveal
rather than to style, and for any control gated on a `hovering` or `isHovered`
state. **Report the complete list**, saying for each whether it hides an action
or only changes an appearance. Fix all of the first kind.

## 4. Departed people must disappear from every picker

`invitableCandidates` in `GroupInfoPanel.tsx` line 57 does not filter on status,
so people marked `departed` are offered as invitable and shown as members.

Filter them everywhere, not only here: the invite search, task assignment,
project party, approval routing, mention autocomplete, and every other person
picker in the codebase. A departed person who already holds a membership is shown
as departed rather than hidden, so existing records stay readable.

Report which pickers you swept.

## 5. Project names on old threads

Your proposed fix is approved: in `listRecentThreads`, when `projectId` is
undefined and `subjectType === "project"`, use `subjectId` directly — a project
thread's `subjectId` **is** the project's identifier. For a site report thread,
look up the report's parent project.

**Keep `threads.projectId` as the primary path.** This is a compatibility route
for threads created before that field existed. New threads must still store it.
Do not remove the field or stop populating it.

## 6. Reply — three separate defects, all confirmed

**6a.** `ChannelMessageBubble` line 399: `onClick={() => { /* set reply */ }}` —
an empty placeholder. Add an `onReply` prop, wire it to `setReplyToId` in
`ChannelPanel`.

**6b.** `ChannelPanel` line 827 passes `quotedMessage={null}` as a hardcoded
literal. The bubble already renders a quoted message at lines 332 to 336 and is
never given one. Fetch the parent and pass it through. Tapping the quote scrolls
to the original.

**6c.** `ThreadPanel.tsx` has no reply at all, although
`thread_messages.replyToMessageId` exists in the schema and
`convex/communication/threads.ts` accepts it at line 158. Add reply to threads,
matching the channel behaviour. Record threads are where most conversation will
happen.

The message action toolbar is itself hover-gated, so on a phone none of pin,
bookmark or reply can be reached. Fix that as part of item 3.

## 7. Not a defect — leave it alone

Record threads are named by their record and are not renameable. This is
intended. Do not add a rename control to them. Only groups and spaces are
renameable.

---

## Report back with

1. The complete list from the hover sweep, with the count.
2. The list of person pickers you filtered for departed status.
3. Tap-by-tap navigation, on a phone-width screen, for each of: rename a group ·
   remove a member · add an owner · reply to a message in a space · reply to a
   message in a record thread.
4. The exact text now shown in the Group rules panel.
5. The exact sidebar label for one project thread and one site report thread.
6. Confirmation that you published, and the published URL.

Navigation steps and quoted on-screen text are the evidence. A clean build is
not.
