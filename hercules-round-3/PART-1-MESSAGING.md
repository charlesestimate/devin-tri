# Magnus Workspace Platform — Hercules build specification, round 3

## Part 1 of 4 · Messaging — defects found on 17 September 2026, and the messaging deliverables still owed

**Prepared for Karl Ivan Estadola, Chief Executive Officer, Magnus Renewable Tech Corp · 17 September 2026**

This is the first of four parts. **Build this part first.** It is the module Magnus uses every hour, and every defect below was traced to a file and a line in the source exported on 8 September 2026 (no build has run since 5 September, so the lines still hold — verify each before editing). Part 2 covers sign-in, access, the dashboard, search and configuration. Part 3 covers governance. Part 4 covers the remaining module deliverables and the acceptance tests.

### How to use this document with Hercules

1. Open the app in **Build mode**, start a new thread, and paste this whole part as one message.
2. Hercules must **read the cited file and line before editing**, fix the root cause named here — not a symptom — and **paste the evidence** asked for in section E: the query output, the search output, the refusal text. A sentence saying it is done is not evidence.
3. Do not start Part 2 in the same thread. One part, one thread, one report.

### Standing rules that still apply

The platform is a record, a permission boundary and a Model Context Protocol server. No scheduler, timer, automation or digest. Every write carries a human's name and goes through the tenant wrapper. Messages are append-only. No abbreviations or ampersands on any label. Nothing is deleted. Where this document is silent, ask; do not decide.

---

# A. WHAT KARL'S OFFICE TEST FOUND, AND WHY — EIGHT MESSAGING DEFECTS

Karl tested with several staff in the office on the week of 14 September. Each report below is followed by the root cause in the code and the exact fix.

## A1 · "Message notifications are not being sent. Some received my message, others did not."

**What actually happens.** A message in General or a group creates a notification **only for the people mentioned** and, in a direct conversation, **for the other participant** (`convex/communication/channels.ts` lines 852–880 and 883–935). Everyone else is meant to see an **unread number** on the conversation — and that number is kept correctly but never drawn (A2). So the people who "received" the message were the ones Karl mentioned or messaged directly; everyone else received exactly what the code gives them: nothing visible.

Two further faults hide the notifications that *are* created:

- **The bell badge never counts them.** `getMyNotifications` in `convex/foundation/notifications.ts` (lines 59 and 71) counts a badge only for category `action_required`. The mention notification (line 869) and the direct-message notification (line 921) are written with category `information`. Information never badges — that rule is correct — but a mention and a direct message are not information: they require the person. They are written in the wrong category.
- **Clicking the bell opens nothing** (A4).

**Fix.**

1. In `sendChannelMessage`, write the mention notification and the direct-message notification with category **`action_required`** (the platform's badging category), title *You were mentioned in [channel name]* or *New direct message from [author display name]*, and `subjectType: "channel"`, `subjectId: channelId` so that opening it opens the conversation (A4). Keep `information` for nothing in this path.
2. Do the same in `threads.ts` for thread mentions (lines 1847–1860 of `channels.ts` handle account-channel record threads; `convex/communication/threads.ts` has its own fan-out — align both).
3. Clearing: a mention or direct-message notification is cleared **when the person opens that conversation** (`markChannelRead` and `markDirectChannelRead`), in the same mutation — the work is reading it. It is never cleared by dismissing the bell.
4. **Do not add a notification for every channel message.** Section 8.13 stands: a thread nobody is mentioned on notifies nobody. The unread number (A2) is the signal for unmentioned messages.

## A2 · Unread numbers do not appear — General (5), Messages (X)

**Root cause — five small defects, all confirmed in the code:**

| # | Where | Defect |
|---|---|---|
| 1 | `src/pages/messages/page.tsx` line 771 | The Company (General) row renders `<ChannelItem>` **without the `unread` prop**. The component draws an amber badge when `unread > 0`; it is never given the value |
| 2 | `page.tsx` line 805 | The Direct rows omit `unread` the same way |
| 3 | `page.tsx` lines 838–845 | Only the Spaces rows pass `unread={ch.unreadCount}` — which is why a badge has only ever appeared on a group |
| 4 | `page.tsx` line 760 | The Company section header passes `count={companyChannels.length}` (the number of company channels, which is 1) and no `unread` |
| 5 | `convex/communication/channels.ts` lines 1416–1421 | `myUnreadCounts` sums `unreadCount` only where the channel type is `group` or `account`. **A company channel is neither, so General never contributes to any total** |

Also: `listMyChannels` (line 1198) accepts a `channelType` filter of `direct`, `account` or `group` — `company` is not an accepted value.

**Fix.**

1. Pass `unread={ch.unreadCount}` on the Company rows (line 771) and the Direct rows (line 805).
2. Company section header: `unread={sum of companyChannels[*].unreadCount}`; keep the count as secondary text or drop it.
3. `myUnreadCounts`: add `company` to the summed channel types and return a fourth field `company`, plus `total = direct + spaces + company`.
4. `listMyChannels`: accept `company` in the `channelType` union.
5. **Messages (X)** on the sidebar item and **Message (X)** on the dashboard, both reading `myUnreadCounts().total`, computed on read — no stored total anywhere.
6. Verify against the database, not the screen: for one person, compare every drawn number with `channel_members.unreadCount` and `direct_message_receipts.unreadCount`. If a row-level count is wrong, that is a second defect — name it separately.

## A3 · "Messages are not accessible to new users, even the General chatbox"

**Root cause.** Two things, and the first is not a messaging defect at all.

1. **The person is not linked to the tenant.** Every messaging query starts with `tryGetTenantContext` (`convex/lib/tenantEnforcement.ts` line 51) and returns an empty list when the signed-in account has no `tenantId` and `personId`. A new user whose sign-in grant did not link (Part 2 §B1 explains why grants fail) sees an empty Messages screen with no explanation. On the live platform today **23 of the 48 people flagged `signsIn` have no identity link at all** and five more have links still `pending` — none of them can reach General.
2. **General itself is fine.** Live check on 17 September: the General channel has **69 members — every person on the platform** — so membership is not the cause. `autoJoinCompanyChannel` runs from `src/pages/auth/Callback.tsx` line 18 inside a `try { } catch { }` that swallows every error, so a failed join is invisible; keep the call but log the failure to the audit trail.

**Fix.**

1. Part 2 §B1 (linking). Nothing in Messages can work until the person is linked.
2. On the Messages screen, when `getCurrentPerson` returns `null`, render one message instead of empty lists: *Your sign-in is not yet linked to a person record. Ask a console holder to grant sign-in for your address [the email the person signed in with].* Show the address — it is what the console holder needs to fix the grant.
3. Remove the silent `catch` in `Callback.tsx`; write an audit entry `person.company_channel_join_failed` with the reason.

## A4 · "Clicking the notification icon does not open the desired notification"

**Root cause.** `src/components/layout/NotificationPanel.tsx` renders each notification as a list item with no click handler and no link — the only control is the × that calls `clearNotification` (line 94). The record has `subjectType` and `subjectId` but nothing maps them to a route.

**Fix.** Every notification opens its record — section 8.2: the notification opens the object, not the message. Build one `routeForNotification(subjectType, subjectId)` map: `channel` → `/messages?channel=…` · `channel_message` → the message's channel · `thread` → the record the thread belongs to, with the thread open · `task` → `/tasks/…` · `approval_request` → `/approvals/…` (My Approvals, Part 2) · `site_report`, `purchase_order`, `work_order`, `document_revision` and every other object type → its record page. Clicking the row navigates, closes the popover, and — only where the work is reading it (a message) — clears it in the same mutation as `markChannelRead`. A notification for a task or an approval is cleared by the task closing or the decision being made, never by the click.

## A5 · "Reactions cannot be undone"

**Root cause.** `ChannelPanel.tsx` lines 507–533 call `addReaction` for both the reaction chips and the smile button. `removeReaction` exists in `channels.ts` line 1029 and nothing in `src/` calls it. `addReaction` (line 1004) is itself idempotent — it removes and re-adds — so a second click on your own reaction changes nothing.

**Fix.** Replace both calls with one `toggleReaction` on the server: if a reaction row with this emoji and this `personId` exists, remove it; otherwise add it. The chip for a reaction the current person has made is drawn highlighted. The panel needs the current person identifier — `page.tsx` line 598 hard-codes `currentPersonId = null` with the comment *resolved server-side*; resolve it once from `getCurrentPerson` and pass it down.

## A6 · "The list of users who reacted to a message is not visible"

**Root cause.** The reaction array on `channel_messages` already stores `{ emoji, personId, reactedAt }` per reaction (`channels.ts` lines 1017–1018). The panel reduces it to a count per emoji (line 510) and throws the names away.

**Fix.** On tap or hover of a reaction chip, show the display names of everyone who reacted with that emoji, resolved from the `persons` list already loaded on the page, each name opening the person card (Part 4 §D4). No new backend.

## A7 · "Sending direct messages requires two attempts"

**Root cause — confirmed.** `page.tsx` lines 1148–1152: after `getOrCreateDirectChannel` returns the new channel identifier, `onCreated` looks the channel up in the `channels` array, which comes from the reactive `listMyChannels` query. That query has not refreshed yet in the same tick, so `find` returns `undefined`, `handleSelectChannel` is never called, and nothing is selected. The person clicks again; by then the channel is in the list, and the second attempt works. The New Group dialog (lines 1136–1140) has the identical fault.

**Fix.** `getOrCreateDirectChannel` and `createGroupChannel` return the full channel document (or the page fetches it with a `getChannel(channelId)` query), and `onCreated` selects it directly rather than searching a list that has not yet updated. Test: one attempt, every time, on a slow connection.

## A8 · A thread can be deleted — this must become archive

Not on Karl's list, found while tracing A2. `convex/communication/threads.ts` line 516 `deleteThread` and the delete dialog on `page.tsx` (state at lines 587–594, handler at 665–668) let a console holder **delete a record thread with a reason**. Section 8.13: messages are append-only, nothing is deleted, and a conversation that can be removed is not evidence of anything. Replace deletion with archive (section C). Keep the reason field for archive; remove the delete path and its dialog entirely.

---

# B. UNREAD, BADGES AND NOTIFICATIONS — THE RULES, RESTATED

- **Unread numbers are display state** per person per conversation: `channel_members.unreadCount` (channels), `direct_message_receipts.unreadCount` (direct), `thread_readers.unreadCount` (record threads — add this table; today threads have no per-person unread). Incremented on send for every active member except the author; cleared by opening the conversation. Never a notification.
- **Notifications** are created only by a mention or a direct message, in category `action_required`, one recipient each, pointing at the conversation. They badge the bell. They clear when the conversation is opened.
- **Badges are computed on read.** `myUnreadCounts` and `getMyNotifications().badge` are queries; nothing stores a running total.
- **Archived conversations count nowhere** — not in unread totals, not in Messages (X), not in mention notifications (section C).
- **No mute, watch, subscribe or per-person hide exists.** Search every screen for those words after this part; none may appear.

---

# C. MESSAGING DELIVERABLES STILL OWED — DECIDED 8 SEPTEMBER 2026

## C1 · Archive, not delete

`channels` already carries `closed`, `closedAt`, `closedBy` and `closeGroupChannel` (`channels.ts` line 571) sets them with an audit entry. Two things are missing: no way to reopen, and a closed group appears nowhere. `threads` has no equivalent field.

1. Add to `threads`: `archived`, `archivedAt`, `archivedBy`, `archivedReason` (optional), with an index so archived and unarchived list without scanning. Rename the channel fields to the same four names or map them; one vocabulary.
2. **Who may archive and restore:** a group — its owner or a console holder · an account space — a console holder · a record thread — a console holder · a direct conversation — either participant, for both · **General and Announcement — nobody; refused.**
3. **What archiving does:** the item leaves the main lists and appears under **Archived** · read-only (no messages, reactions, attachments) · still searchable, marked archived · members unchanged · excluded from unread counts and mention notifications · audit entry `thread.archived` / `channel.archived` with actor, time and optional reason.
4. **Restore:** anyone who may archive; logged. **Automatic restore:** posting on the record an archived thread belongs to (a new site report on an archived project, a message on an archived purchase order) restores the thread in the same mutation, logged as `thread.restored_automatically`.
5. **Archived section** in the Messages sidebar below Threads, collapsed, showing the count; opening lists archived threads and channels together, most recent first, each showing what it is, when, by whom; selecting opens read-only with a banner and a Restore control for those permitted.
6. Protocol: `archive_thread`, `restore_thread`, `archive_channel`, `restore_channel`; `list_threads` and `list_channels` gain an `archived` filter defaulting to excluded.
7. Remove `deleteThread` (A8).

## C2 · The Announcement channel beside General — administrators post, everyone reads, posts are editable

Today the platform allows exactly one company channel: `ensureCompanyChannel` (line 1579) returns the first `company` channel and `autoJoinCompanyChannel` (line 1629) joins people to that one only; any member may post; no message anywhere can be edited.

1. **Allow more than one company channel**, each with a `name`, each auto-joined by every person on creation and on first sign-in. `ensureCompanyChannel` becomes `ensureCompanyChannels` seeding **General** and **Announcement**; `autoJoinCompanyChannel` joins every company channel.
2. **Post permission on the channel row:** `postRestrictedTo` — a list of role machine names or person identifiers; empty means everyone. General: empty. Announcement: `chief_executive_officer`, `chief_operating_officer` (Karl and Beda by role, so a successor inherits it). `sendChannelMessage` refuses a post from anyone outside the list with *Only administrators post in Announcement.* The composer is replaced by that sentence for everyone else.
3. **Edit — Announcement only.** New mutation `editChannelMessage(messageId, body)`: author only, still within `postRestrictedTo`, channel must have a non-empty `postRestrictedTo`. Stores the previous body in a new `channel_message_revisions` table (messageId · revisionNumber · body · replacedAt · replacedBy), updates the message body, sets `editedAt`, increments `editCount`, writes an audit entry. The message shows *edited [time]* and opens its revision history. **No other message anywhere becomes editable**; a correction elsewhere is a new message.
4. The two channels sit side by side at the top of the Company section: General open, Announcement read-only for non-administrators. FAQ and Q&A later on the same mechanism.

## C3 · Messages (X) and Task (X)

- Sidebar item **Messages (X)** and dashboard **Message (X)**, X = `myUnreadCounts().total` (A2).
- Sidebar item **Task (X)** and dashboard **Task (X)**, X = tasks assigned to me whose status is not `done` or `cancelled` — one query `myOwedTasks`, used by the indicator and by the list it opens (Part 2 §B5). Unchanged by anything except delivery or cancellation.

## C4 · The person card from any author name

Every author name in a channel or thread, every reactor name (A6), every member row in the group panel opens the person card of Part 4 §D4 — photograph, mobile number, contact email, contact note, current roles. The card is built in Part 4; the click target belongs to this part.

## C5 · Group information panel — verify, do not rebuild

`src/pages/messages/_components/GroupInfoPanel.tsx` now calls `inviteMember`, `removeMember`, `leaveChannel`, `setMemberIsOwner` and `renameChannel` (lines 38–42) — the panel that was missing on 8 September exists. Verify on screen: member list with the owner marked · Add people in one tap from the group header · Remove (owner) · Leave · Hand over ownership · Rename posting a system message with old and new name · the two answerability rules visible on the panel (a group is archived and never deleted; a console holder may open a group they are not a member of only through a logged *access for review* with a reason that notifies the owner). **`access_for_review` does not exist in `channels.ts`** — build it: a console holder opening a group they are not in must supply a reason, an audit entry is written, and the owner receives a notification in the same mutation.

## C6 · Protocol tools

`list_channel_members`, `invite_member`, `remove_member` (same ownership rules as the screen), `archive_*` / `restore_*` (C1), `edit_announcement(messageId, body)` under the same restriction as C2, `get_account_activity` (already specified; confirm it exists and excludes groups the caller is not in).

---

# D. RULES FROM SECTION 8.13 THAT MUST SURVIVE THIS PART

Mention is the only attention mechanism; one person per mention; the notification opens the object. A direct message notifies without a mention. No subscription, watch or mute. Append-only, except the Announcement edit path; hide by an administrator with a reason, logged and visible. Search covers message text, attachment filenames and the owning record, scoped by record scope and, for groups and direct messages, by membership; archived items appear marked. Convert a message to a task in one tap with output type required. A photograph offered on a block thread prompts *attach to today's site report instead?* Offline: composition order, de-duplication by `clientMessageKey`, text before attachments. Reactions, pin, bookmark, quote, reply exist. Legal hold by a console holder with a reason.

---

# E. REPORT BACK — PASTE THE EVIDENCE, NOT A SENTENCE

1. **A2.** Sign in as two people. Person B sends five messages to General. Paste `channel_members` rows for person A on General (`unreadCount` = 5), then a screenshot or the rendered values of: the General row (5), the Company header (5), the sidebar *Messages (5)*, the dashboard *Message (5)*. Person A opens General; paste the same four values (0).
2. **A1.** Person B mentions person A in a group and sends a direct message. Paste the two `notifications` rows: category `action_required`, `subjectType` `channel`, `subjectId` the channel. Paste the bell badge value (2). Person A opens each conversation; paste the rows as cleared with `clearedBy` naming the mutation.
3. **A4.** Click each notification type once; paste the route it navigated to.
4. **A5, A6.** Person A reacts 👍, clicks again — paste the `reactions` array before and after (present, then absent). Hover the chip on a message with two reactors — paste the names shown.
5. **A7.** Start a new direct message on a throttled connection; paste the audit entries showing one `channel.create_direct` and one `channel.message_sent` from a single attempt.
6. **A8, C1.** Paste the search of `src/` and `convex/` for `deleteThread` (empty). Archive a group, an account space, a record thread and a direct conversation; attempt General and Announcement (refused — paste the message). Paste one `thread.archived`, one `thread.restored`, one `thread.restored_automatically` audit entry. Paste a search result that returns an archived thread marked archived, and `myUnreadCounts` showing it excluded.
7. **C2.** Paste the two company channel rows with `postRestrictedTo`. A non-administrator posts to Announcement — paste the refusal. Karl edits an announcement — paste the `channel_message_revisions` row, the message's `editedAt` and `editCount`, and the audit entry. Attempt `editChannelMessage` on a General message — paste the refusal.
8. **A3.** Sign in as a person with no identity link; paste the exact text the Messages screen shows, including the email address.
9. **C5.** Paste the file and line of each of the six controls on the group panel and of `access_for_review`, with one audit entry and one owner notification from a review access.
10. Paste the search of every screen for `mute`, `watch`, `subscribe`, `follow` — none.
11. Acceptance tests 237 to 251 from the chat specification and tests M1 to M12 in Part 4 §F — paste the results.
