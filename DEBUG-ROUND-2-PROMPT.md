# Debug round 2 — controls that are still unreachable

You reported items 3 and 4 delivered and published. The Chief Executive Officer
opened a group space afterwards and still cannot rename it and still cannot
remove a member. Reply has also been found broken.

**Before anything else, read this.** You wrote: *"The dev machine can't click."*
That is the whole problem. You have now twice reported a control fixed that a
person then could not find. Reading the code and getting a clean build tells you
the function exists; it does not tell you a human can reach it. From now on,
every interface fix in this round must come back with **exact tap-by-tap
navigation** a person can follow in thirty seconds. If a step cannot be
described, the control is not reachable.

---

## 1. Rename, remove member and hand over ownership are missing from the panel

**Do not investigate this. The cause is confirmed by screenshot.**

The panel opens correctly. One tap from the group header shows: the heading
"Group info", the group name, the group rules, **MEMBERS · 6** with a search box
and the member list, **ADD PEOPLE** with an invite search, and **Leave group**.

So `GroupInfoPanel` renders, and invite and leave work. What is not there:

- **Rename.** The group name is static text with no edit control beside it.
- **Remove member.** Each member row shows an avatar and a name and nothing
  else — no remove action, no row menu.
- **Hand over ownership.** Not present anywhere in the panel.

The owner is marked with a crown, so the panel already knows who the owner is.

Add all three to the panel:

- The name becomes editable in place for the owner and for a console holder,
  calling `renameChannel`. Log the change with the old and new name and announce
  it in the group as a system message.
- Each member row gains a remove action, visible to the owner and to a console
  holder, calling `removeMember`. It is logged, as specified.
- An action to hand ownership to another member, owner only, calling
  `handoverGroupOwnership`.

All four mutations already exist in `convex/communication/channels.ts` at lines
355, 381, 425 and 460. This is wiring, not new backend work.

**Check the phone layout.** The Chief Executive Officer tests on a phone. Three
new controls in a panel that already scrolls must remain reachable on a narrow
screen.

## 1b. Departed people still appear as members and as invitable

The member list shows four people whose `status` is `departed`, each named
`[TEST RECORD] …`, and more are offered under ADD PEOPLE.

A person marked `departed` must not appear in the invite search anywhere in the
platform, and must be shown as departed wherever they still hold an existing
membership. Sweep every person picker for the same defect — task assignment,
project party, approvals, mentions.

## 1c. The project name still has not been applied

The Messages sidebar shows `Site Report 001 — PRJ-20…` and `PRJ-2026-0004`. If
the backfill had run these would read
`Site Report 001 — 480_kW_Calamba Agro Industrial Corporation_PRJ-2026-0004`.

The "Seed Project Names" button was pressed and nothing changed. Establish why
and say which it was: the button did not call the mutation, the mutation ran and
wrote nothing, it wrote `derivedName` but the thread label does not read it, or
the format change was never applied.

Then make it work, and confirm by quoting the exact sidebar text for one project
thread and one site report thread after running it.

## 2. Reply and quote do not work — three separate defects

All three are in `src/pages/messages/_components/ChannelPanel.tsx`.

**2a. There is no Reply action on any message.** `setReplyToId` is called exactly
once in the entire `src/` tree, at line 699, and the value it passes is
`undefined` — the clear-reply action. Nothing anywhere sets it *to* a message. So
`replyToId` can never hold a value and the reply composer can never open.

Add a Reply action on each message, reachable the way a person expects it — the
message's own menu, or a control that appears on the message.

**2b. The quoted message is never rendered.** `replyToMessageId` appears once, at
line 525, where it is sent. It is never read back when messages are displayed. So
a reply, if one could be created, would render as an ordinary message with no
sign of what it answers.

Render the quoted parent above the reply: author and a truncated line of the
original, tapping it scrolls to the original. This is the entire point of the
feature — a reply that does not show what it replies to is not a reply.

**2c. Threads have no reply at all.** `ThreadPanel.tsx` contains no reference to
reply of any kind, although `thread_messages.replyToMessageId` exists in the
schema and `convex/communication/threads.ts` accepts it at line 158. Record
threads are where most conversation will happen. Add reply there too, matching
the channel behaviour.

## 3. Not a defect — do not change it

Thread names are not editable, and that is correct. A record thread is named by
the record it belongs to. The Chief Executive Officer has confirmed this is
intended. **Do not add a rename control to record threads.** Only group spaces
are renameable.

---

## Report back with

1. The tap-by-tap navigation for rename, for remove member and for hand over
   ownership, on a phone-width screen.
2. Confirmation that departed people no longer appear in any invite search, and
   the list of pickers you swept.
3. Which of the four causes in item 1c was true, and the exact sidebar text for
   one project thread and one site report thread afterwards.
4. The file and line of the Reply action, of the quoted-parent rendering, and of
   the thread reply.
5. The same tap-by-tap navigation for: replying to a message in a space, and
   replying to a message in a record thread.
6. Confirmation that you published, and the published URL.

Screenshots of the group header and of a rendered reply if you can produce them.
