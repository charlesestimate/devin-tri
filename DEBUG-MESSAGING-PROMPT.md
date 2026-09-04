# Debug — messaging functions that were specified and do not work

Every item below was instructed, and in most cases the backend mutation exists,
compiles and is deployed. **The interface never calls it.** That is the single
pattern behind six of these seven.

Report against the numbered list, naming the file and line you changed and the
call you ran to prove it.

---

## 1. Direct messages cannot be started

`getOrCreateDirectChannel` exists in `convex/communication/channels.ts` line 72.
**Nothing in `src/` calls it.** The Messages sidebar shows a Direct section that
says "No direct messages" and offers no way to begin one.

Section 8.13 defines `direct` as a channel type and states that a direct message
is the one message that notifies without a mention. Wire it: a control that opens
a person search and starts or opens the direct channel with that colleague.

## 2. Pinned messages cannot be seen

`pinMessage` at line 888 is called from the interface, so a message can be
pinned — and then nothing shows it. Pin was instructed alongside reactions,
bookmark, quote and reply.

Add a pinned strip at the top of the thread or channel showing pinned messages,
and a filter to show only pinned. Same for bookmarks: `toggleBookmark` at line
909 is wired, with nowhere to see what has been bookmarked. Add a Bookmarks view
listing the current person's bookmarked messages across every conversation.

## 3. A member cannot be removed from a space

`removeMember` at line 381 exists. **Nothing in `src/` calls it.** So does
`inviteMember` at line 355, `leaveChannel` at 425 and `handoverGroupOwnership` at
460 — none of the four is called anywhere in the interface.

This was already instructed in the previous round. It has not been delivered.
Build the group information panel it asked for: member list, add people, remove
member, leave group, hand over ownership.

## 4. A space cannot be renamed

Also instructed in the previous round, also not delivered. The owner may rename a
group; the change is logged with the old and new name and announced in the group
as a system message. Project and department channels are not renamed by hand.

## 5. Unread counts for spaces are hardcoded to zero

`myUnreadCounts` at line 1164 returns `direct`, `mentions` and `spaces` — and
`spaces` is the literal `0`, with the comment `// display state: not a
notification`.

Compute it properly, per space, for the current person, and show it beside the
space name in the sidebar as `Platform Bugs (3)`. The count clears when the
person opens that space.

**This is a count, not a notification, and the distinction matters.** Section
8.13's rule is that *notification* is governed by the mention and nothing else,
so that a person cannot be notified about everything and then mute the mechanism
by which the company calls their attention. An unread badge on a list the person
has chosen to open breaks none of that. Do not add push notification, email, or
any alert on unread. Do not add subscribe, watch or mute. The badge only.

## 6. Search does not work

`searchMessages` at line 1202 exists and uses the `search_body` index.
**Nothing in `src/` calls it.** The search box in the Messages page filters the
loaded list in the browser and finds nothing that is not already on screen.

Wire the box to `searchMessages`. Search must cover message text, attachment
filenames and the owning record, scoped by record scope and, for groups and
direct messages, by membership.

## 7. The project name still shows as PRJ-2026-0041

Creating a discussion on a project still produces `Project PRJ-2026-0041`.

**First, answer this plainly:** is the naming work from the previous round live on
the published deployment, or still sitting in preview? Nothing visible changed,
and your last message asked me to switch back to Build mode.

**Second, the format changes, by decision of the Chief Executive Officer.** The
project number stays visible, as a suffix rather than a hidden field:

```
480_kW_Calamba Agro Industrial Corporation_PRJ-2026-0041
```

A person reads the capacity and the customer first; the number is still there for
anyone who needs it. Apply the same shape wherever a project is named, and to the
project part of a record thread label:

```
Site Report 001 — 480_kW_Calamba Agro Industrial Corporation_PRJ-2026-0041
```

---

## Report back with

For each of the seven: the file and line, and for items 1, 2, 3, 5 and 6 the
result of actually using the control in the interface — not that the code
compiles. Item 7 needs the published-or-preview answer first, before anything
else.
