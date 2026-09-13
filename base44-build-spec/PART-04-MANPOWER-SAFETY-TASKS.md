# Magnus Workspace Platform — Base44 build specification

## Part 04 · Manpower, workforce and equipment · Safety · Tasks and deliverables

**Prerequisite: Part 01 complete; `project_id`, `project_block_id`, `location_id` and `site_report` from Parts 02 and 03.** This part publishes `deployment.labour_rate`, without which Part 06 cannot compute labour cost. **Safety is implemented from Magnus's own manual and is not redesigned.**

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

# A. MANPOWER, WORKFORCE AND EQUIPMENT

**Two objectives: see the resources, and record what was requested and not supplied.** A declined resource request is today a conversation that leaves no trace; recorded, it is the evidence that makes hiring a decision rather than an argument.

**`resource_availability`** — computed on read, never stored: resource_id · resource_class · current_assignment · **available_from (when it frees up)** · status (`available`/`assigned`/`in_transit`/`maintenance`/`unavailable`).

**`resource_request`** — request_id · **project_id and project_block_id (both required)** · resource_class (`manpower`/`equipment`/`vehicle`/`skill`) · what · how_many · skill_or_asset (capability tag) · **needed_from · needed_until** · **why** · requested_by · allocator (routed by class and region — configuration) · state (`requested`/`allocated`/**`partially_allocated`**/`declined`/`fulfilled`/`cancelled`) · **decline_reason (required on decline, controlled list)** · decline_note.

**Decline reasons — never aggregated into a single decline rate:** no one available with this skill · resource committed elsewhere at higher priority · equipment unavailable or under maintenance · request not justified · needed-from date not achievable. **`partially_allocated` is a distinct state.** A request unfulfilled past its needed-from date is valued against the block it was raised for. Raising a request notifies the allocator in the same transaction.

**`deployment`** — deployment_id · person_id · project_id · block_id · **planned_from · planned_to (the plan layer)** · **recorded_days (derived — days the person appears in a toolbox attendance list)** · **verified_days (derived — days carrying both the toolbox photograph and a signed acknowledgement sheet line)** · **labour_rate (money per day, effective-dated, set by Human Resource, changed under gate 31; a rate change never restates a closed period)** · state (`planned`/`active`/`ended`).

**Three layers; the platform reports the variance between them and never overwrites one with another.** Roster continuity: a person in two projects' toolbox lists on the same day is flagged. Scheduling awareness shows approved leave and assignment overlap when a deployment is planned, and **never shows the reason for leave, medical information, or any presence data.**

**`labour_rate`** — person_id or grade · rate_per_day · effective_from · effective_to · set_by · approval_request_id (gate 31).

**`equipment`** — equipment_id · description · serial_number · **custodian (a named person, never a location)** · certification_expiry · maintenance_due · **utilisation (accumulated from deployment, never entered)** · state.

**`equipment_deployment`** — equipment_id · project_id · block_id · from · to.

**Bench depth** — computed on read: any capability held by fewer than two people, where that capability sits on a project critical path, is flagged continuously. Critical-path capabilities are a configured list.

**Permissions:** Project Manager — own projects and the available pool, requests, does not allocate, rates per money visibility · Department head — own department, requests and allocates, sees rates · Chief Operating Officer — all, requests and allocates, sees rates · Person In Charge — own site only, requests, does not allocate, no rates · Human Resource — all people, neither requests nor allocates, sees rates. **No role sees a person's leave reason, medical information or presence data through this module.**

**Screens:** resource availability with release dates · resource requests with decline reasons · deployment with all three layers shown · equipment register · bench depth.

---

# B. SAFETY

**DO NOT REDESIGN SAFETY.** Magnus has a complete occupational safety and health system — manual `MRTC-OSH-GDL-00 Rev 00`, eighteen chapters, six permit-to-work types with a seven-step process, an emergency plan, an eighteen-point incident investigation record, inspection cadences, a corrective action tracker and thirteen named performance indicators. **Implement the manual. Do not improve, simplify or substitute a general safety module for it.**

**⚠ Open dependency, blocking content only:** the item content of the three checklists, the seven permit-to-work steps, the eighteen investigation points and the thirteen indicator definitions come from Alma Codog and the manual itself. **Build the structure to hold checklists and point lists of any length and leave the content slots empty. Do not invent them.**

**`permit_to_work`** — permit_to_work_id · project_id · block_id · type (`working_at_height`/`hot_work`/`electrical_work_on_live_systems`/`confined_space_entry`/`lifting_operations`/`excavation`) · **valid_from · valid_to — same day only** · **named_worker_id list** · steps (the seven, each with a completed flag and who completed it — content slots empty until supplied) · issued_by · issued_on · state (`requested`/`issued`/`closed`/`expired` — `expired` is **derived on read** when the day has passed, never set by a person and never by a timer).

- **Gate 28: the Safety Officer of record issues every permit to work. No alternate, no window, no delegation, and no configuration setting can change this.** Approving authority per type is a configuration row so a future split needs configuration rather than code — but every row today names the Safety Officer and none may name an alternate.
- **Competency-gated: a worker whose capability tag for that permit type is lapsed or absent cannot be named.** Refused at save.
- An open permit past its validity window is a live finding, queryable.
- Working at height carries hard block 3 (B0 signed off).

**`permit_to_work_type_configuration`** — type · approving_role (must resolve to the Safety Officer; save refuses any alternate) · required_capability.

**`incident`** — incident_id · project_id · occurred_on · classification (`near_miss`/`first_aid`/`medical_treatment`/`lost_time`/`disabling`/`fatality`) · **the eighteen investigation points (structure only)** · photograph file list · reported_via (`account`/`site_quick_response_form`) · investigated_by · closed_by · closed_on · state (`reported`/`under_investigation`/`closed`). **Gate 30: the Safety Officer closes, countersigned by the Chief Operating Officer; no alternate.** An incident classified `disabling` or `fatality` stores the statutory deadline (Work Accident/Illness Report by the twentieth of the following month) in `statutory_obligation`; nothing raises the task — an agent does (deviation D7).

**Near-miss reporting: a per-site Quick Response code to a no-login form** — scan, add a photograph and a sentence, submit. Optional stop-work switch on the same form. **No identity captured; no account; no install. Every field added to this form reduces reports.** Submissions arrive as `incident` rows with `reported_via = site_quick_response_form` for the Safety Officer to triage. The form is a public route keyed by an unguessable site token; it writes exactly one table.

**NON-RETALIATION IS A PRODUCT REQUIREMENT, enforced in software.** No reporter identity in any dashboard, report or export. No per-person incident counts outside the safety function.

**`safety_stop`** — safety_stop_id · project_id · block_id · **raised_by — any person on site, or the site form, no minimum role, no approval** · raised_on · reason · photograph_file_id · lifted_by · lifted_on · state (`active`/`lifted`). Raising one stops work on the named block immediately and **fires the mandatory-acknowledgement push in the same transaction** to the Safety Officer and the Person In Charge. **Gate 29: only the Safety Officer lifts it. No alternate, no delegation, no configuration setting. There is no other transition out of `active`.** With an unreachable Safety Officer work halts indefinitely; that is the safe failure direction. Raising a stop is never recorded against the person who raised it.

**`corrective_action`** — corrective_action_id · source (`inspection`/`incident`/`near_miss`/`audit`) · source_id · owner_id · **hierarchy_of_controls_level (`elimination`/`substitution`/`engineering`/`administrative`/`personal_protective_equipment`)** · target_date · state (`open`/`action_taken`/`verified`/`void`) · evidence_file_id. **Closing without evidence is permitted and reported.** `void` requires a reason. Raised by a person or an agent, not automatically from a failed item (deviation D6).

**`inspection`** — inspection_id · type (`daily_walk`/`weekly_checklist`/`monthly_audit`) · project_id · performed_by · performed_on · **item-level answers (checklist_item_id · answer · note)** · state (`scheduled`/`performed`/`actions_raised`).

**`checklist_definition`** — type · items (ordered; **empty until Alma Codog supplies them**) · revision. Keep the daily walk deliberately short.

**`safety_indicator`** — the thirteen from the manual plus two recommended (near-miss to incident ratio · hierarchy of controls distribution). **All computed on read from records the platform holds; no screen exists for entering an indicator value.** Leading indicators are given visual priority over lagging. Indicator definitions are configuration rows with empty formula slots until the manual is supplied.

**`statutory_obligation`** — obligation · deadline · owner · reference · state · source_record. Stored and queryable; nothing raises it on a schedule. Includes the Work Accident/Illness Report, the Annual Medical Report by 31 March, Safety Officer designation, safety committee meetings.

**`site_emergency_card`** — per site: nearest hospital, ambulance, evacuation point, first aiders on duty, client contact. **Held offline on every phone.** A live first-aider roster per site.

**Subcontractor personnel** are persons linked to their employing party and inherit its accreditation and insurance status, exclusions included.

**Nothing in this module is ever deleted.**

**Screens:** permits to work · incidents and near misses · safety stops · corrective actions · inspections with item-level answers · the offline emergency card · the per-site Quick Response near-miss and stop-work form (no login) · indicators (read-only, derived).

---

# C. TASKS AND DELIVERABLES

**A task is a person's guide to their day.** Not a project plan, not a timesheet.

**`task`** — task_id · title · **owner (exactly one person)** · project_id · project_block_id · **output_type (required: `document`/`sales_outcome`/`business_opportunity`/`approval_or_decision_recorded`/`record_or_data_entry`/`physical_work`/`communication_sent`/`verification`)** · output_object_type · output_object_id · source (`derived`/`requested`/`recurring`/`self_registered`/`claimed`) · requested_by · priority (`normal`/`priority`) · **committed_date (set once, permanent)** · current_date · **recommit_count** · state (`draft`/`pending_approval`/`to_do`/`in_progress`/`blocked`/`done`/`graded`/`cancelled`) · blocked_by_person · blocked_expected_clear · blocked_reason · grade (`met`/`partially_met`/`did_not_meet`, optional) · graded_by · source_message_id (when converted from a message) · recurring_definition_id.

**There is no `hours`, `time_spent`, `started_at` or activity field, and there never will be.**

- **Where the output is a platform object, creating that object closes the task in the same transaction.** A site report filed closes the site report task; an approval decided closes the approval task; a work order reaching `in_progress` closes its assignment task. The output is the completion.
- **A task cannot enter `blocked` without a named blocker and, wherever knowable, an expected clear date.** A task blocked on a person appears on that person's daily screen as something they are holding up, with a notification to them in the same transaction.
- **Unfinished work carries forward automatically** — it is simply still open tomorrow; nothing runs at midnight.
- **Priority is scarce: two levels, and a requester may hold at most three priority items at one time across all their requests (configuration).** A fourth is refused until one is released.
- **`committed_date` is kept forever; moving a date increments `recommit_count`.**
- **Grading is per task, never aggregated per person. No code path turns grades into a number describing a person.**
- **Assigning a task raises a Task notification to the owner in the same transaction.**

**`recurring_definition`** — obligation · owner · cadence · next_due (stored) · last_instantiated. A standing obligation stored with its cadence; **an agent instantiates the task; nothing schedules it** (deviation D11).

**The open assignment board** holds work with no owner. A person **claims** it (becomes owner) and may **release** it with a reason. An unclaimed task older than ten working days is queryable.

**The daily screen (My Day) shows, in this order — the order is the specification:** overdue · **blocked (its own section, showing the named blocker and the expected clear date)** · due today · priority · due this week.

**Load is displayed as a band — light, normal, heavy — never a number.** Signals: open commitments · deadline density · spread across projects · ageing · queue depth. Work-in-progress limits per role are set after one quarter of real data.

**A person with no open task for three working days** is a Check computed on read for their manager and their director — never to the person, never on their record. No flag for approved leave, suspension, or roles configured as not task-based.

**Task (X)** on the sidebar and dashboard = tasks owned by the person not in `done`, `graded` or `cancelled`, computed on read (Part 01 §10).

**Screens:** My Day · task record · open assignment board · team load bands (manager view, bands only) · output type by department (report).

---

## D. Gates and notifications this part wires

| Action | Gate | Notification in the same transaction |
|---|---|---|
| Permit to work issue | 28 | Requester (Task) |
| Safety stop raised | — | Safety Officer and Person In Charge — push with mandatory acknowledgement |
| Safety stop lifted | 29 | Person In Charge (Information) |
| Incident closure | 30 | Chief Operating Officer countersignature (Task) |
| Resource request raised | — | Allocator (Task) |
| Task assigned or blocked on a person | — | Owner or blocker (Task) |
| Labour rate change | 31 | — |

---

## E. Checks before Part 05 starts

1. Attempt to auto-approve, delegate or set a window on a permit to work at every level including console holder — all refused. Name a worker with a lapsed capability — refused.
2. Raise a safety stop from the site form with no account — it lands, work on the block is stopped, the push fires with acknowledgement required, and no reporter identity is stored. Attempt to lift it as anyone but the Safety Officer — refused.
3. Search every screen, query and export for reporter identity or per-person incident counts — none outside the safety function. Search for any screen entering an indicator value — none.
4. Emergency card opens with the phone offline.
5. Save a task with no output type — refused. Assign to two people — refused. File a site report — its task closes with no separate action. Move a date four times — original retrievable, `recommit_count` reads 4. A fourth priority item from one requester — refused.
6. Schema review: no `hours`, `time_spent`, `started_at`, clock-in, clock-out, location or duration field on any table. Search every screen, query and export for a per-person load number, aggregate grade or ranking — none.
7. The no-task Check appears for the manager and director; nothing on the person's screen or record; the executive view shows a count across managers, never names.
8. Decline a resource request without a reason from the list — refused; the declined-by-reason query never returns a single combined rate.
9. Acceptance tests 91 to 113 from Part 12 pass, with output pasted.
