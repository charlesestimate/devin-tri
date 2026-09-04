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

## 1. Group rename and member removal are still not reachable

You replaced the unlabelled ⓘ with a `Users [N members]` label in
`ChannelPanel.tsx` and published. It is still not usable.

Establish which of these is true, and say which:

- The label is not rendering at all.
- It renders but does not open `GroupInfoPanel`.
- The panel opens but the rename and remove controls are not in it, or are
  disabled.
- It only renders for the group owner, and the person testing is not the owner.
- It renders on a wide screen and not on a phone. **The Chief Executive Officer
  is testing on a phone.** Check the mobile layout specifically — a header
  control that fits on a laptop is frequently pushed out of view on a narrow
  screen, and that alone would explain both rounds of this.

Then fix it, and report the navigation as steps:

> Messages → tap a group under SPACES → header shows … → tap … → panel shows …
> → Rename is at … → Remove member is at …

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

1. Which of the five causes in item 1 was true, and the tap-by-tap navigation for
   rename and for remove member, on a phone-width screen.
2. The file and line of the Reply action, of the quoted-parent rendering, and of
   the thread reply.
3. The same tap-by-tap navigation for: replying to a message in a space, and
   replying to a message in a record thread.
4. Confirmation that you published, and the published URL.

Screenshots of the group header and of a rendered reply if you can produce them.
