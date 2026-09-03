This message rebuilds module 14, Communication, to a standard that replaces Facebook Messenger and Google Chat for Magnus staff, and moves every file the platform stores onto a connected Google Drive. **Both are critical path for cutover. Build A first, then B, then run C.** Everything here follows the original rules: no scheduler, no timer, nothing acts by itself, every write under a person's name, everything through the tenant wrapper, no abbreviations on any label.

Section 8.13 of the original instruction stands in full. This message adds to it and, where it says so, changes it. Where the current build has any of this already, keep it and report what exists.

---

# A. COMMUNICATION — WHAT MAGNUS ACTUALLY NEEDS

## A1 · The Messages screen is one place for every conversation

One screen, reached from the sidebar item *Messages*, laid out like Google Chat: a left panel and a conversation pane.

Left panel, in this order, each with an unread count:

1. **Direct** — one-to-one conversations with people in the company.
2. **Spaces** — account spaces (A2), project channels, department channels, and invite-only groups (A3).
3. **Threads** — record threads the person has posted on or been mentioned in, newest activity first, each showing the record it belongs to.

An unread count is a display state per person per conversation. **It is not a notification.** Notifications are still created only by a mention or a direct message, section 8.13. A person clears an unread count by opening the conversation. There is no mark-all-read that touches notifications.

The conversation pane shows messages newest at the bottom, the composer, attachments, reactions, pin, bookmark, quote, reply, and **convert to task in one tap**. Every message shows author, sent time and, where different, the device time it was composed. A hidden message shows that a message was hidden, who hid it and why.

**Speed rule, from section 8.13 and measured in test 244:** from opening the application on a phone, a message on a project channel or a record thread takes no more taps than posting in a Messenger group. If it does, the screen is wrong.

## A2 · The account space: one conversation per customer, for the life of the customer

**`channel.channel_type` gains `account`.** An account space is created in the same transaction as the account in Pipeline, linked to the account, and lives as long as the account. It is internal only. Client contacts never see it and cannot be members.

**What it shows.** Its own messages, plus every record thread under the account rolled up in one view: the opportunities and proposals in Pipeline, the site assessment, the design package and its deliverables, the project, its blocks, site reports, permits, purchase orders, non-conformance reports, variation orders, progress claims, and after turnover the service agreements, serviced assets and work orders on that account's sites. Each rolled-up message shows which record it was posted on and opens that record. **A message posted from the account space view onto a record thread is stored on that record thread**, not on the space; the composer shows which thread it will post to, and the default when nothing is selected is the space itself.

**Membership is automatic and logged.** A person joins the account space when assigned to anything under the account: sales owner on the opportunity, Director on the project, Project Manager, design engineer on a deliverable, Person In Charge on a site report, procurement officer on a purchase order, assigned owner on a work order. A person leaves the space when no assignment under the account remains, except Directors and console holders, who remain. A person may also be invited by a current member, logged, and removed by the inviter or a Director, logged. Membership changes never delete history.

**Record scope still governs.** A person who may not see the project's money sees the messages but not the figures the record carries; the roll-up shows message text, never a monetary field.

## A3 · Invite-only groups

**`channel.channel_type` gains `group`.** Any person creates a group, names it, and invites members. **Only members see that the group exists, its membership and its messages.** The creator is the owner; the owner may hand ownership to another member. Members may leave; the owner may remove a member, logged. A group with no owner passes to its longest-standing member. A group is closed, never deleted; a closed group is read-only to its members and searchable by them.

**Groups are not secret from the record.** Two rules keep them answerable years later, and both are visible to every member on the group's information panel so nobody is surprised:

- A console holder may open a group they are not a member of only through a logged *access for review* action that requires a reason and notifies the owner. Hiding a message inside a group follows the same path.
- Legal hold applies to a group like any thread.

Department channels and project channels stay as specified: membership follows roles and assignment automatically, and no invitation is needed.

## A4 · Direct messages

Internal only. Two people, or one person and themselves as notes. A direct message notifies without a mention, section 8.13. Searchable by its two participants only. No group direct message: three people is a group.

## A5 · Everything else in section 8.13 stands

Mention as the only attention mechanism · exactly one person per mention · no subscription, no watch, no mute · append-only, hide only by an administrator with reason · search across message text, attachment filenames and the owning record, scoped by record scope and, for groups and direct messages, by membership · convert to task in one tap, output type required · the site-report prompt when a photograph is offered on a block thread · offline compose queue, composition order, de-duplication by `client_message_key`, text before attachments · reactions, pin, bookmark, quote, reply · legal hold.

## A6 · Read tool for reports

Add to the protocol's read scope: `get_account_activity(account_id, from, to)` returning every record and every message under the account in the window, with sources, respecting record scope and money visibility and excluding groups and direct messages the caller is not a member of. This is what an agent uses to draft a client report; the report itself is written outside the platform and stored under Documents when a person files it.

---

# B. GOOGLE DRIVE AS THE FILE STORE

**Principle: Drive is the disk. The platform is the index.** The platform is the only writer to the folder tree. People open files through the platform. Nobody browses, renames, moves or replaces a file in Drive, because the revision-in-force rule of section 8.14 and the toolbox photograph's place in the payroll chain both depend on the file being exactly what the record says it is.

## B1 · Connection

In Administration, under Integrations, a console holder connects one Google account by OAuth. **It is a dedicated Google account owned by Magnus for this purpose, not a person's own account.** Request only the scope that limits access to files the application created. The connection stores the refresh token encrypted, the account's email, the root folder identifier, when it was connected and by whom. Disconnecting is logged and does not delete anything in Drive. The connection state, quota used and the count of files pending upload are shown on the same screen.

## B2 · The `file` record

Every stored file has one record: `file_id` · `drive_file_id` · `drive_folder_path` · `original_name` · `mime_type` · `size_bytes` · **`sha256` computed at upload, before Drive** · `uploaded_by` · `uploaded_on_device` · `received_by_server` · `capture_source` (`in_app_camera` / `file`) · `attached_to_object` · `storage_state` (`staged` / `in_drive` / `verified` / `erased`) · `legal_hold`. Attachments, document revisions, toolbox photographs, site photographs, contract documents, insurance certificates, evidence documents and every other stored file reference a `file` record. Existing code that references a Convex storage identifier directly is changed to reference `file_id`.

## B3 · Upload path

1. A phone or browser uploads to the platform exactly as today. Field uploads still go through the offline queue. **A device never talks to Drive.**
2. The server computes `sha256`, writes the `file` record as `staged` with the bytes in platform storage, and in the same request attempts the Drive upload into the derived folder.
3. On success the record becomes `in_drive` with `drive_file_id`, and the staged bytes are removed.
4. On failure the record stays `staged`. **Nothing retries by itself**, section 1 of the original instruction. The Integrations screen shows the pending count, the protocol exposes `list_files_pending_drive` and `push_pending_files_to_drive`, and any later successful upload by any person also pushes up to twenty pending files in the same request. A staged file is fully usable inside the platform meanwhile.
5. `verify_file(file_id)` re-reads the bytes from Drive, recomputes the hash and sets `verified` or raises a discrepancy naming the file. `verify_audit_chain` gains an option to verify every file referenced by the entries in its range.

## B4 · Reading path

Files are served through the platform, which fetches from Drive using the connection and streams to the person after the same permission check the record carries. **No Drive sharing link is ever issued to a person.** Thumbnails for photographs are generated once at upload and stored beside the file in the same folder.

## B5 · Folder tree, derived from the record, never typed

Root: **Magnus Platform**. Second level: the module name exactly as it appears in the sidebar. Third level: the object, as its number and name. Below that, the sub-object. Examples:

| Record | Folder |
|---|---|
| Toolbox photograph, site report workday 63 on PRJ-2026-0001 | Magnus Platform / Projects / PRJ-2026-0001 Calamba Agro Industrial Corporation / Site Reports / 2026-09-03 workday 63 / |
| Signed contract | Magnus Platform / Projects / PRJ-2026-0001 Calamba Agro Industrial Corporation / Contract / |
| Drawing revision 3 | Magnus Platform / Documents / DWG-0412 Single line diagram / Revision 3 / |
| Goods receipt photograph | Magnus Platform / Procurement / PO-2026-044 Nordwind Energy GmbH / Goods Receipts / 2026-10-05 / |
| Incident evidence | Magnus Platform / Safety / INC-2026-007 / |
| Work order evidence | Magnus Platform / Operations and Maintenance / OM-2024-003 Lipa Cold Storage and Logistics Inc. / Work Orders / WO-2026-018 / |
| Message attachment on a block thread | Magnus Platform / Projects / PRJ-2026-0001 Calamba Agro Industrial Corporation / Messages / B1 / |
| Message attachment in a group | Magnus Platform / Messages / Groups / Bicol procurement / |
| Proposal PDF | Magnus Platform / Pipeline / ACC-0012 Calamba Agro Industrial Corporation / OPP-2026-031 / |

Folder names are created on first use. A renamed project renames its folder; Drive file identifiers do not change, so no record breaks. A file name inside a folder is the platform's `file_id` plus the original extension, with the original name kept on the record, so two uploads named `photo.jpg` never collide.

## B6 · Retention and erasure

A retention schedule or a cryptographic erasure request executed by a person under the existing rules deletes the Drive file permanently through the connection, sets `storage_state` to `erased`, keeps the record with its hash, and writes the audit entry. Legal hold refuses it. Nothing deletes on a timer.

## B7 · Moving what is already stored

A one-time action on the Integrations screen, run by a console holder, moves every file currently in platform storage into Drive under the derived folder tree, one batch at a time, showing progress and the count remaining. Each moved file is hashed before and verified after. The action stops on the first discrepancy and reports it. It may be run again to continue.

## B8 · Later move to Google Workspace

The connection is designed so the root folder can be transferred to a Workspace shared drive later with file identifiers intact. Store nothing that depends on the owning account's email.

---

# C. ACCEPTANCE TESTS — APPEND TO SECTION 14 AS TESTS 237 TO 258

## Communication

237. **One screen.** Messages shows Direct, Spaces and Threads with unread counts; opening a conversation clears its count and creates no notification.
238. **Account space is born with the account.** Creating an account creates its space in the same transaction; no separate action.
239. **Roll-up reads across the lifecycle.** Post on the opportunity thread, the project thread, a block thread, a site report thread and a work order thread under one account; the account space shows all five in order, each opening its record.
240. **Post from the roll-up lands on the record.** From the account space, post onto the block thread; the message is stored on the block, not the space.
241. **Automatic membership.** Assign a person as Person In Charge on a site report under the account; they are in the space. Remove the assignment; they are out, and their past messages remain.
242. **Money never rolls up.** A Person In Charge reads the account space; no monetary figure appears in any rolled-up message or record preview.
243. **Invite-only is invisible.** Create a group with two members. A third person cannot find it by search, by list, or by identifier. A console holder cannot read it without *access for review*, which requires a reason and notifies the owner.
244. **Speed.** On a phone, from the home screen to a sent message on a project channel: count the taps. Record it against a Messenger group post. It must not be more.
245. **Convert to task in one tap.** From a message, one tap opens the task with the message quoted; output type required.
246. **No mute anywhere.** Search every screen for mute, watch, subscribe, follow. None exists.
247. **Append-only.** Edit and delete do not exist; hide by an administrator is logged and visible in the thread.
248. **Offline order.** Text, photograph, text composed offline arrive in that order; the photograph never delays the third message; no duplicate after three reconnects.
249. **Direct message notifies without a mention.** Exactly one notification, opening the conversation.
250. **Group ownership passes.** Owner leaves; longest-standing member becomes owner; logged.
251. **Account activity read tool.** `get_account_activity` returns records and messages under the account with sources and excludes a group the caller is not in.

## Drive

252. **Device never touches Drive.** Inspect the client bundle and network calls: no Drive endpoint, no Drive token.
253. **Hash before Drive.** Upload a file; the record carries `sha256` before `drive_file_id`. Replace the file in Drive by hand; `verify_file` reports the discrepancy.
254. **Folder derived.** Upload a toolbox photograph on workday 63 of PRJ-2026-0001; it lands in the folder in B5 exactly. Rename the project; the folder renames; the file still opens from the site report.
255. **Staged survives Drive failure.** Disconnect Drive; upload; the file is `staged`, usable in the platform, counted on Integrations; nothing retries by itself. Reconnect; the next upload pushes it; `push_pending_files_to_drive` pushes the rest.
256. **No sharing links.** Open a file as a person; the network shows the platform serving it; no Drive link is issued.
257. **Legal hold refuses erasure.** Place a hold; execute erasure; refused. Release; execute; the Drive file is gone, the record remains with hash and state `erased`.
258. **Move existing files.** Run B7 on the current store; every file moves, verifies, and every record still opens its file.

---

# D. THEN CONTINUE

Report what existed of module 14 before this message, then the results of tests 237 to 258, then resume remaining milestones without waiting to be prompted.
