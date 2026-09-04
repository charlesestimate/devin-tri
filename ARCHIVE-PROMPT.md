# Prompt for Hercules — archive, not delete

Archiving is the everyday action for a conversation that is finished. Deleting
stays what it is: rare, console-holder only, for records that should never have
existed. Build archive so deleting almost never gets used.

---

## 1. What already exists — reuse it, do not rebuild it

`channels` already carries `closed`, `closedAt` and `closedBy`, and
`closeGroupChannel` in `convex/communication/channels.ts` line 495 already sets
them with an audit entry. That is archiving for group channels and it works.

Two things are missing from it: there is no way to reopen a closed group, and a
closed group appears nowhere in the interface. Fix both below.

`threads` has no equivalent field at all.

## 2. Threads gain the same three fields

Add to `threads`: `archived`, `archivedAt`, `archivedBy`, and
`archivedReason` (optional). Add an index that lets archived and unarchived be
listed separately without scanning.

## 3. Who may archive

| Object | Who |
|---|---|
| Group channel | The owner, as `closeGroupChannel` already enforces — **or** a console holder |
| Account channel | A console holder |
| Record thread — project, site report, purchase order, permit and the rest | A console holder |
| **Company General channel** | **Nobody. It cannot be archived.** |

Not everyone, deliberately. Section 8.13 has no subscription, no watch and no
mute, because a person who can silence a conversation can silence the mechanism
by which the company calls their attention. A per-person hide would be a mute
under another name. Archiving is therefore a shared state with an owner, not a
personal preference.

## 4. What archiving does

- The item leaves the main Messages lists and appears under **Archived**.
- It becomes read-only. No new messages, no reactions, no attachments.
- **It stays searchable.** Section 8.13 requires it: a closed group is read-only
  to its members and searchable by them. The same holds for an archived thread.
- Members and viewers do not change. Archiving is not removal from a group.
- An audit entry is written: `thread.archived` or `channel.archived`, with the
  actor, the timestamp and the reason if one was given.
- A reason is optional here. Deleting requires one; archiving does not, because
  archiving destroys nothing.

## 5. Restore

Anyone who may archive an item may restore it. Restoring writes its own audit
entry and returns the item to the main list with its messages intact.

**One automatic case:** if a person posts on the record an archived thread
belongs to — files a new site report on an archived project, say — the thread
restores itself in that same mutation. A conversation must never continue
somewhere invisible. Log the automatic restore the same way.

## 6. The Archived section

In the Messages sidebar, below Threads, add a collapsed section headed
**Archived**, showing the count. Opening it lists archived threads and closed
spaces together, most recently archived first, each showing what it is, when it
was archived and by whom.

Selecting one opens it read-only, with a banner saying it is archived, who
archived it and when, and a Restore control for those permitted to use it.

Archived items must not appear in the main lists, in unread counts, or in any
mention notification. They must still appear in search results, marked as
archived.

## 7. Over the protocol

Add `archive_thread`, `restore_thread`, `archive_channel`, `restore_channel`,
and a filter on `list_threads` and `list_channels` for archived state — default
excluding archived. Same authority rules as the interface.

---

## Report back with

1. The schema change and the index.
2. The file and line of the archive and restore controls, and of the Archived
   section.
3. Confirmation of each: an archived thread is read-only; it still appears in
   search; it does not appear in unread counts; posting on the underlying record
   restores it automatically; the company General channel refuses to archive.
4. The audit entries for one archive, one manual restore and one automatic
   restore.
