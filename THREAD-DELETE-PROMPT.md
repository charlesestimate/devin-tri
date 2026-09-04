# Prompt for Hercules — administrator delete for threads

You could not delete the seven test threads. Build the control instead, so this
never needs a console workaround again.

---

## What to build

**A delete action on a thread, available only to a console holder.**

- Reachable from the thread's own header in Messages, and from a selection in the
  thread list so several can be cleared at once.
- Requires a typed reason before it will proceed. No reason, no delete.
- Writes an audit entry: `thread.deleted`, the thread identifier, its subject type
  and subject identifier, the message count destroyed, the actor, the timestamp
  and the reason.
- Deletes the thread and its messages. Attachments already written to Google Drive
  are **not** deleted — the file records are marked orphaned and the audit entry
  says so. Do not make a Drive call from this mutation.
- Anyone who is not a console holder does not see the control at all, and the
  mutation refuses them.

## What this deliberately is not

Not message hiding. Section 8.13 keeps messages append-only, hidden only by an
administrator with a reason, and that stays exactly as it is. This is a different
control for a different job: destroying a whole thread that should not exist —
test data, a thread on a record created in error, a duplicate.

It is a narrow exception to append-only and it is scoped that way on purpose:
console holder, reason required, audit entry, never available to anyone else.
Do not widen it, and do not add a "delete message" control alongside it.

## Then use it

Delete the seven existing test threads with the reason "Pilot test data cleared
before staff onboarding."

## Two things to check while you are in there

**1. Confirm the naming work actually published.** Your last message asked me to
switch back to Build mode. Nothing in the sidebar changed. Tell me plainly
whether the schema and query changes from the previous round are live on the
published deployment, or still sitting in preview.

**2. Confirm the new labels render.** After deleting the seven threads, post one
message on a project and one on a site report, and report the exact text that
appears in the Messages sidebar for each. It should read:

- `480_kW_Calamba Agro Industrial Corporation` for the project thread
- `Site Report 001 — 480_kW_Calamba Agro Industrial Corporation` for the site report

If it does not, the previous round did not take effect and we deal with that
before anything else.

## Report back with

1. The file and line of the delete control and of the mutation.
2. The audit entry as it was written for one of the seven deletions.
3. The two label strings, copied exactly as they appear on screen.
