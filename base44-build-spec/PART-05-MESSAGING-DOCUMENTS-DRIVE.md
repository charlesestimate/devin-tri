# Magnus Workspace Platform — Base44 build specification

## Part 05 · Communication (Messages), Document control, Google Drive as the file store

**Prerequisite: Part 01 complete; `project_id`, `project_block_id` and `account_id` from Part 02.** This part carries the Messenger switch-off, which is the reason the platform exists for most of its users, and the file pipe every other part's upload control reuses. **Build D (the file store) first, then A (Messages), then B (Documents).** Section A folds in every decision taken on 8 September 2026: archive, unread numbers, the Announcement channel, editable announcements, the person card photograph on Drive.

---

## 0. Standing rules — repeated at the top of every part

1. The platform is a record, a permission boundary and a Model Context Protocol server. **No scheduler, automation, timer, workflow, rules engine, notification engine, ranking or digest.** The only exception is the same-transaction safety push (Part 01 §2.1).
2. Four permitted computations: derived on read · hard block and gate evaluation at the instant of the attempt · permission resolution at the instant of the request · same-transaction derivation from fields the human action supplied.
3. Every table carries `tenant_id`; every read and write goes through the one server-side data-access layer; the client never writes a governed table directly.
4. The audit log is append-only and hash-chained; nothing edits or deletes an entry.
5. Gates and hard blocks are data rows; one approval engine serves every gate; nothing is auto-approved.
6. Every write carries a human's name; no service account; no agent identity.
7. No abbreviations or ampersands anywhere in the interface, field names, statuses or messages.
8. No Magnus-specific literal in code; all values are configuration rows.
9. Presence is never tracked, for anybody, at any level.
10. Where the specification is silent, ask; do not decide.

---

# A. COMMUNICATION — MESSAGES

**This module replaces something that works.** Magnus runs on Facebook Messenger group chats. The only thing this offers that Messenger cannot is **the conversation happening on the record it is about**, with a permanent link, findable years later. **If a discussion about a purchase order takes more taps than posting in a group chat, people will post in the group chat.**

## A1. The Messages screen — one place for every conversation

One screen, reached from the sidebar item *Messages*, laid out like Google Chat: a left panel and a conversation pane.

**Left panel, in this order, each section header and each row showing an unread number:**

1. **Company** — the company channels: **General** (open to everyone) and **Announcement** (read by everyone, posted by administrators only — section A5). Both auto-joined by every person on creation and on first sign-in. More company channels may be created later on the same mechanism (FAQ, Q&A).
2. **Direct** — one-to-one conversations, and a person's notes to themselves.
3. **Spaces** — account spaces (A3), project channels, department channels, invite-only groups (A4).
4. **Threads** — record threads the person has posted on or been mentioned in, newest activity first, each showing the record it belongs to.
5. **Archived** — collapsed, showing the count (A7).

**Unread numbers are a display state per person per conversation — `channel_member.unread_count` and `thread_reader.unread_count` — maintained on send (incremented for every active member except the author) and cleared by opening the conversation.** They are not notifications. **Every row in every section passes its unread number to the row component, and every section header shows the sum of its rows** — General (5) means five unread in General. The Company header shows the unread sum, never the number of channels. The sidebar item and the dashboard show **Messages (X)** where X = Company + Direct + Spaces unread (Part 01 §10). The first build kept these counters correctly and drew none of them; wire every row.

**The conversation pane:** messages newest at the bottom · the composer · attachments · reactions · pin · bookmark · quote · reply · **convert to task in one tap**. Every message shows author (opening the person card), sent time and, where different, the device time it was composed. A hidden message shows that a message was hidden, who hid it and why. An edited announcement shows *edited* with the time and opens its revision history.

**Speed rule, measured in test 244:** from opening the application on a phone, a message on a project channel or a record thread takes no more taps than posting in a Messenger group.

## A2. Objects

**`thread`** — thread_id · object_type · object_id · account_id (derived from the object, for the roll-up) · **archived · archived_at · archived_by · archived_reason (optional)** · last_activity_at. Created lazily on first message. **Every object carries a thread, without exception and without configuration:** project · block · task · site report · transmittal · permit · purchase order · bill of materials line · goods receipt · progress claim · fund request · write-off · stock adjustment · variation order · non-conformance report · safety stop · document · person · design deliverable · opportunity · proposal · site assessment · service agreement · serviced asset · work order · warranty claim · service charge. No screen decides which objects have threads.

**`channel`** — channel_id · channel_type (`company`/`project`/`department`/`account`/`group`/`direct`) · name · linked_object_type · linked_object_id · owner_person_id (groups) · **post_restricted_to (list of role machine names or person identifiers; empty means every member may post)** · **archived · archived_at · archived_by · archived_reason** · created_by. **One company channel per name.** Project channel names follow the derived project name; department channel names follow the department; neither is renameable by hand.

**`channel_member`** — channel_id · person_id · joined_at · joined_how (`automatic`/`invited`/`creator`) · invited_by · left_at · removed_by · **unread_count** · last_read_at · is_owner.

**`thread_reader`** — thread_id · person_id · unread_count · last_read_at (created on first post or mention).

**`message`** — message_id · thread_id or channel_id · author · body · created_on_device · received_by_server · **client_message_key (generated on the device before the first attempt; duplicates refused)** · reply_to · quote_of · pinned · hidden_by · hidden_at · hidden_reason · **edited_at · edit_count** · is_system_message.

**`message_revision`** — message_id · revision_number · body · replaced_at · replaced_by. Written only by the edit path in A5; the current body stays on `message`, every previous body is here.

**`mention`** — message_id · **mentioned_person (exactly one per row)** · notification_id.

**`attachment`** — message_id · file_id (a `file` record in section D) · capture_source (`in_app_camera`/`file`).

**`reaction`** — message_id · person_id · emoji. **`bookmark`** — message_id · person_id.

## A3. The account space — one conversation per customer, for the life of the customer

Created in the same transaction as the account in Pipeline, linked to it, internal only. It shows its own messages plus **every record thread under the account rolled up in one view**: opportunities, proposals, site assessment, design package and deliverables, project, blocks, site reports, permits, purchase orders, non-conformance reports, variation orders, progress claims, and after turnover the service agreements, serviced assets and work orders on that account's sites. Each rolled-up message shows which record it was posted on and opens it. **A message posted from the roll-up onto a record thread is stored on that record thread**; the composer shows which thread it will post to; the default is the space itself.

**Membership is automatic and logged:** a person joins when assigned to anything under the account (opportunity owner, Director, Project Manager, deliverable owner, Person In Charge on a site report, procurement officer on a purchase order, work order assignee) and leaves when no assignment remains, except Directors and console holders. A current member may invite; the inviter or a Director may remove; logged. History is never deleted by membership change. **Money never rolls up** — the roll-up shows message text, never a monetary field.

## A4. Invite-only groups

Any person creates a group, names it, invites members. **Only members see that the group exists, its membership and its messages** — not by search, list or identifier. The creator is the owner; the owner may hand ownership to another member; members may leave; the owner may remove a member (logged); a group with no owner passes to its longest-standing member (logged). A group is archived, never deleted.

**The group information panel**, opened from the group header in one tap, holds: the member list with the owner marked · **Add people** (person search, multi-select) · Remove a member (owner) · Leave group · Hand over ownership (owner) · **Rename** (owner; logged with old and new name; announced in the group as a system message) · the two answerability rules, visible to every member: a group is archived and never deleted; a console holder may open a group they are not a member of only through a logged **access for review** action that requires a reason and notifies the owner. Hiding a message inside a group follows the same path. Legal hold applies to a group like any thread.

## A5. Company channels: General and Announcement

- **General** — `post_restricted_to` empty; everyone may post.
- **Announcement** — sits directly beside General in the Company section; `post_restricted_to` holds the administrators (configuration; today Karl and Beda by person identifier, or the role `chief_executive_officer` and `chief_operating_officer`). Everyone else sees it read-only, with the composer replaced by *Only administrators post here.*
- **Edit.** A message in a channel with `post_restricted_to` set may be edited by its author (who must still be within the post permission). The edit stores the previous body in `message_revision`, updates the body, sets `edited_at`, increments `edit_count`, shows *edited* with the time, and writes an audit entry. **Nowhere else in the platform can a message be edited.** Messages in General, Direct, Spaces and Threads remain append-only; a correction is a new message.
- Both channels auto-join every person on creation and on first sign-in. Neither can be archived (A7). FAQ and Q&A can be added later on the same mechanism.

## A6. Rules that stand throughout

- **The mention is the attention mechanism.** A thread nobody is mentioned on notifies nobody. A mention names exactly one person; mentioning three creates three notifications; the notification opens the object, not the message. **A direct message is the one message that notifies without a mention.**
- **There is no subscription, no watch and no mute.** No per-person hide of a conversation exists — a personal hide would be a mute under another name.
- **Search is load-bearing:** message text, attachment filenames and the owning record, scoped by record scope and, for groups and direct messages, by membership. Archived items appear in search, marked archived.
- **Convert a message to a task in one tap:** the task opens with the message quoted and `source_message_id` set; output type required; link back retained.
- **A photograph attached to a message is not a site record.** On a block thread the platform prompts: *attach to today's site report instead?*
- **Messages are append-only** except the announcement edit in A5. An administrator may **hide** a message with a reason; the hiding is logged and visible in the thread.
- **Offline:** compose queue · resumable retry · messages send in composition order · de-duplication by `client_message_key` · text sends before attachments.
- **Reactions, pin, bookmark, quote and reply exist.** No presence, typing or read receipts; no voice or video.
- **Membership of project and department channels follows roles and assignment automatically.** A person leaving the company loses every channel on identity provider disablement.
- **Legal hold** on a project, thread, group or person's records — set and released by a console holder with a reason, logged, overriding retention.

## A7. Archive, not delete

Archiving is the everyday action for a finished conversation. Deleting does not exist for messages, threads or channels.

| Object | Who may archive and restore |
|---|---|
| Group | The owner, or a console holder |
| Account space | A console holder |
| Record thread (project, site report, purchase order, permit and the rest) | A console holder |
| Direct conversation | Either participant, for both (it is a shared state, not a personal hide) |
| **General and Announcement** | **Nobody. They cannot be archived.** |

**What archiving does:** the item leaves the main lists and appears under **Archived** · it becomes read-only — no new messages, reactions or attachments · it stays searchable, marked archived · members and viewers do not change · it does not appear in unread counts or in any mention notification · an audit entry `thread.archived` or `channel.archived` records actor, time and optional reason. A reason is optional because archiving destroys nothing.

**Restore:** anyone who may archive may restore; logged. **One automatic case:** when a person posts on the record an archived thread belongs to — files a new site report on an archived project, posts on an archived purchase order — the thread restores itself in that same mutation and the automatic restore is logged. A conversation must never continue somewhere invisible.

**The Archived section** lists archived threads and channels together, most recently archived first, each showing what it is, when it was archived and by whom; selecting one opens it read-only with a banner and a Restore control for those permitted.

## A8. Screens

Messages (A1) · group information panel (A4) · Announcement with edit and revision history (A5) · Archived (A7) · person card from any author name (Part 01 §5).

---

# B. DOCUMENT CONTROL

**So that nobody builds from a superseded drawing, and so that a question asked in year three can be answered by the record made in year one.** This is an authority problem — which copy governs — not a recovery problem.

**`document`** — document_id · document_number · title · **classification (`controlled`/`archive`/`unclassified`)** · classified_by · classified_on · classification_request_id · owner · attached_to_object_type · attached_to_object_id · review_cycle_months · next_review_due · last_reviewed_on · legal_hold · legal_hold_set_by · legal_hold_reason · retention_class · distribution_list (person identifiers for acknowledgement).

**`document_revision`** — revision_id · document_id · revision_number · file_id · status (`draft`/`for_review`/`approved`/**`in_force`**/`superseded`/`withdrawn`) · approver · approved_at · **in_force_from · in_force_to (empty means current)** · superseded_by · seal_id · published_by.

**`document_acknowledgement`** — **revision_id (of a revision, never of a document)** · person_id · acknowledged_at.

**`required_document`** — module · object_type · document_type · mandatory · gates_what. **Derived from module declarations, never maintained.** No screen builds a checklist by hand.

**Rules:**

- **THE REVISION-IN-FORCE RULE. Every historical record references the revision in force at the time of the record. Link to `revision_id`. Never to `document_id`. Anywhere.**
- **Exactly one revision of a controlled document is `in_force` at any moment.** Publishing a revision `in_force` requires the document to be `controlled`, requires the revision to be `approved`, sets the previous in-force revision to `superseded` with `in_force_to` = the day before, and sets `in_force_from` = today in the same mutation. **A revision cannot be set `in_force` with a hand-typed `in_force_from`, on an unclassified document, or while another revision is in force without the supersede step.** The protocol's revision tool calls this same function; it never takes status as free text.
- A superseded revision opened by anyone says so on the face of it and links to the governing revision.
- **Classification is by a person under gate 33, no automatic default, no alternate.** **Reclassification** (controlled ↔ archive) is a distinct action, also under gate 33, logged with before and after; a document with an `in_force` revision cannot become `archive` until that revision is withdrawn.
- **An unclassified document is visible but not usable for construction** — it opens, is discussable, can be attached to a message, carries an unclassified mark, and **cannot be attached to a work instruction or referenced as the governing revision** (refusal 5).
- Controlled: drawings, specifications, procedures, company forms, manuals. Archive: photographs, correspondence, reports, certificates received. **Archive documents are never referenced as governing.**
- **Company forms are controlled documents with revision numbers**: the transmittal form, the daily site report, safety forms, the payroll acknowledgement sheet. The form's revision is recorded on every record created from it.
- **A new revision of an acknowledged document resets acknowledgement for everyone on its distribution list.** A review that confirms no change still records a review.
- **Eight permanent classes, never subject to retention:** site photographs · as-built drawings · test and commissioning records · structural certificates · permits · contracts · service agreements · work-order evidence.
- **Legal hold** is set and released only by a console holder, with a reason, logged. It overrides every retention rule including erasure requests.
- **Retention schedules are `[CONFIGURED]`, pending counsel.** Do not invent periods.
- **Documents are produced elsewhere and controlled here.** No document editing inside the platform.

**Screens:** document library with classification, revisions and the governing revision marked · revision detail with acknowledgements · required-document register per project (derived) · classification queue for Cristy (gate 33) · legal holds.

---

# C. ATTACH, SEND AND PRINT — THE UPLOAD CONTROL EVERY SCREEN REUSES

The first build's only upload was the chat composer. This part delivers one reusable **file control** — upload (camera or file, per the object's rule), preview, download, replace-as-new-revision where the object is a document — and places it on: the person card (photograph) · contract (signed document) · party (insurance certificate) · project (Construction Safety and Health Program document) · purchase order (Send produces the document; supplier quotations attach) · goods receipt (photographs) · design deliverable · permit (filing reference and approval document) · toolbox meeting and site photographs · incident, corrective action and non-conformance evidence · payroll period (acknowledgement sheet photographs) · payslip (Part 06) · progress claim and service charge (the invoice document produced by the platform) · work order and warranty claim evidence.

**Print** produces a document from the record — purchase order, progress claim, service charge, payslip, distribution sheet, transmittal, board pack — stored as a `file` record under the object's folder, with `money_visibility` applied to what appears on it.

---

# D. GOOGLE DRIVE AS THE FILE STORE

**Principle: Drive is the disk. The platform is the index.** The platform is the only writer to the folder tree. Nobody browses, renames, moves or replaces a file in Drive.

## D1. Connection

Administration → Integrations: a console holder connects **one dedicated Google account owned by Magnus** by OAuth, requesting only the scope limited to files the application created. Stored: the refresh token **encrypted, server-side only** · account email · root folder identifier · connected when and by whom. Disconnecting is logged and deletes nothing in Drive. The screen shows connection state, quota used and the count of files pending upload.

## D2. The `file` record

**`file`** — file_id · drive_file_id · drive_folder_path · original_name · mime_type · size_bytes · **sha256 (computed at upload, before Drive)** · uploaded_by · uploaded_on_device · received_by_server · capture_source (`in_app_camera`/`file`) · attached_to_object_type · attached_to_object_id · **storage_state (`staged`/`in_drive`/`verified`/`erased`)** · thumbnail_drive_file_id · legal_hold · erased_at · erased_by. Every stored file anywhere references a `file` record.

## D3. Upload path

1. Phone or browser uploads to the platform. Field uploads go through the offline queue. **A device never talks to Drive.**
2. The server computes `sha256`, writes the record as `staged` with the bytes in platform storage, and in the same request attempts the Drive upload into the derived folder.
3. On success: `in_drive` with `drive_file_id`; staged bytes removed.
4. On failure: stays `staged`. **Nothing retries by itself.** Integrations shows the pending count; the protocol exposes `list_files_pending_drive` and `push_pending_files_to_drive`; any later successful upload by any person also pushes up to twenty pending files in the same request. A staged file is fully usable meanwhile.
5. `verify_file(file_id)` re-reads from Drive, recomputes the hash, sets `verified` or raises a discrepancy naming the file. Audit chain verification gains an option to verify every file referenced by entries in its range.

## D4. Reading path

Files are served through the platform after the same permission check the record carries. **No Drive sharing link is ever issued to a person.** Thumbnails for photographs are generated once at upload and stored beside the file.

## D5. Folder tree — derived from the record, never typed

Root **Magnus Platform** / module name as in the sidebar / object as number and name / sub-object. Examples:

| Record | Folder |
|---|---|
| Toolbox photograph, workday 63 | Magnus Platform / Projects / PRJ-2026-0001 480_kW_Calamba Agro Industrial Corporation / Site Reports / 2026-09-03 workday 63 / |
| Signed contract | … / Projects / PRJ-2026-0001 … / Contract / |
| Drawing revision 3 | Magnus Platform / Documents / DWG-0412 Single line diagram / Revision 3 / |
| Goods receipt photograph | Magnus Platform / Procurement / PO-202610-044 Nordwind Energy GmbH / Goods Receipts / 2026-10-05 / |
| Incident evidence | Magnus Platform / Safety / INC-2026-007 / |
| Work order evidence | Magnus Platform / Operations and Maintenance / OM-2024-003 Lipa Cold Storage and Logistics Inc. / Work Orders / WO-2026-018 / |
| Message attachment on a block thread | … / Projects / PRJ-2026-0001 … / Messages / B1 / |
| Message attachment in a group | Magnus Platform / Messages / Groups / Bicol procurement / |
| Person photograph | Magnus Platform / Human Resource / People / [person_id] / |
| Proposal document | Magnus Platform / Pipeline / ACC-0012 Calamba Agro Industrial Corporation / OPP-2026-031 / |

Folders are created on first use. A renamed project renames its folder; Drive file identifiers do not change. The file name inside a folder is `file_id` plus the original extension; the original name stays on the record.

## D6. Retention and erasure

A retention schedule or an erasure executed by a person under gate 35 deletes the Drive file permanently through the connection, sets `erased`, keeps the record with its hash, and writes the audit entry. Legal hold refuses it. Nothing deletes on a timer.

## D7. Moving what is already stored

A one-time console-holder action on Integrations moves every file in platform storage into Drive under the derived tree, one batch at a time, showing progress; each moved file is hashed before and verified after; the action stops on the first discrepancy and may be re-run to continue.

## D8. Later move to Google Workspace

Store nothing that depends on the owning account's email, so the root folder can be transferred to a Workspace shared drive with identifiers intact.

---

## E. Checks before Part 06 starts

1. Messages shows Company, Direct, Spaces, Threads and Archived; every row and every header shows an unread number; send five messages to General from another account — General (5), the Company header reads 5, the sidebar reads Messages (5); open General — 0. Confirm against the database row, not the screen.
2. Post in Announcement as a non-administrator — refused. As an administrator, edit a posted announcement — previous body in `message_revision`, *edited* shown, audit entry written. Attempt to edit a message in General — no control exists and the backend refuses.
3. Archive a group as its owner: read-only, gone from the main list and unread counts, present in search marked archived, present under Archived with a Restore control. Post a site report on a project whose thread is archived — the thread restores itself, logged as automatic. Attempt to archive General or Announcement — refused.
4. Create a group with two members: a third person cannot find it by search, list or identifier; a console holder cannot read it without *access for review*, which requires a reason and notifies the owner. Owner leaves — longest-standing member becomes owner, logged. Rename — system message posted, old and new name logged.
5. Creating an account creates its space in the same transaction. Post on five record threads under one account — the space shows all five, each opening its record; a Person In Charge reads the space and sees no monetary figure.
6. Ten messages mentioning nobody raise no notification; a direct message raises exactly one. Search every screen for mute, watch, subscribe, follow — none.
7. Text, photograph, text composed offline arrive in that order; no duplicate after three reconnects.
8. Convert a message to a task in one tap — task opens with the message quoted, output type required.
9. Create a site report against revision 3, issue 4 and 5, reopen — it shows revision 3. Attempt to set a revision in force on an unclassified document — refused; with a typed `in_force_from` — refused. Reclassify under gate 33 — logged with before and after. Acknowledge revision 2, issue 3 — not acknowledged.
10. Upload a file: the record carries `sha256` before `drive_file_id`; the folder matches D5 exactly; rename the project — the folder renames and the file still opens. Disconnect Drive; upload — `staged`, usable, counted; reconnect; the next upload pushes it. Inspect the client bundle and network — no Drive endpoint, no Drive token, no sharing link. Place a legal hold; erase — refused; release; erase — Drive file gone, record `erased` with hash.
11. Upload a photograph on the person card — it lands under Human Resource / People and shows on the card, on message authorship and on the People list.
12. Acceptance tests 114 to 125 and 237 to 258 from Part 12 pass, with output pasted.
