# Sections 12.2 and 12.3 were not built as written

Read this whole message before writing any code. It does not add a new feature. It completes a requirement that was in the original instruction and was built only in part.

## What sections 12.2 and 12.3 actually say

I am restating them in full here so there is no ambiguity about what was asked, whatever remains in your context:

**Section 12.2, read tools.** "Expose list, get and search for **every object in section 8**, plus these computed reads, evaluated on request and each returning its own evaluation timestamp and rule count." Then a list of about twenty computed queries — percentage complete per block and project against the planned curve, material readiness by block, blocks not startable with mobilisation planned, projects with no site report in the last two working days, approval requests pending with age in working days, blocked activities with reason, non-conformance reports open with ageing, design deliverables waiting split by party waited on, the twelve-month cash forecast, and the rest.

**Section 12.3, write tools.** "Create and update for **every object**; submit an approval decision on any pending request — always as the authenticated person and always subject to that person's permissions."

## What was actually built

Twenty-six tools. Section 8 defines ninety-seven objects.

What happened is that I named `create_notification` and `post_message` as examples of the rule in 12.3, and you built exactly those two and treated the rule they were examples of as decoration. The same happened in 12.2: a handful of list tools exist, and "every object in section 8" was not implemented. This is the same pattern as the six hard blocks being given different meanings from section 5, and as tests being reported complete on the strength of reading code rather than running it.

`create_person` is not a new request. It was covered by "create and update for every object" from the first protocol instruction. So was `create_party`, `create_site`, `create_item`, and ninety-odd others.

## The ninety-seven objects in section 8

So that "every object" cannot be read loosely, here they are:

account · approval_request · attachment · audit_entry · bill_of_materials_line · billing_milestone · candidate · capability_tag · cash_forecast_line · channel · configuration_value · console_holder · contact · contract · corrective_action · deployment · design_deliverable · design_package · document · document_acknowledgement · document_revision · employee · engagement_response · equipment · fund_request · gate · gate_trigger · generation_reading · goods_receipt · hard_block · hard_block_attempt · incident · inspection · interview_record · item · location · maintenance_plan · measure_register · mention · message · non_conformance_report · notification · objective · offer · opportunity · party · payroll_line · payroll_period · permission · permit_duration_observation · permit_requirement · permit_to_work · permit_type · person · person_role · physical_count · professional_seal · progress_claim · project · project_block · project_party · project_permit · proposal · purchase_order · purchase_order_line · report_register · required_document · requisition · resource_availability · resource_request · review · risk_term · role · safety_stop · service_agreement · service_charge · service_level_term · serviced_asset · serviced_asset_equipment · site · site_assessment · site_photograph · site_report · site_report_activity · statutory_rate_table · stock_adjustment · stock_position · system_constant · task · tenant · thread · toolbox_meeting · transmittal · variation_order · warranty_claim · work_order · write_off

## Deliverable one, before any code

Post a table with one row per object above and these columns: object · list · get · search · create · update · notes.

Mark each cell as **exists**, **missing**, or **not writable by rule**. That last value applies only where section 12.5 forbids it: the audit log, statutory calculation results, tenant isolation, and the existence of any hard block. Hard block *values* remain configurable under gate 31; their existence is not. Anything you believe should not be writable for a reason other than 12.5, put the reason in the notes column and I will decide, rather than omitting the row.

Post the table in full. Do not begin building until it is posted.

## Deliverable two, the tools

Then build every cell marked missing, so that every row is complete. Each tool obeys the rules already in section 12.1, without exception:

- It runs as the authenticated person and has that person's permissions, never more.
- Record scope and money visibility are applied at the query layer, never by filtering an answer after it is computed.
- It applies the same validation, the same gates and the same refusal messages as the equivalent screen. A refusal a person would see on screen is the refusal the tool returns, word for word.
- Every call is written to the audit log with arrival channel `model_context_protocol`, the agent session identifier and the session scope.
- No tool deletes anything. Records are archived, voided, withdrawn or superseded.
- Every figure returned cites the records it came from.

## Order of work

Build in this order, publishing after each group:

1. **Blocking work right now:** person, with a `grant_sign_in` tool alongside it; party; account; site; contact; item; location.
2. **Pipeline and projects:** opportunity, site_assessment, proposal, project, contract, project_party, project_block, risk_term, variation_order.
3. **Everything else in the table**, module by module, in the order the modules appear in section 8.

## One separate change

Add `overseas` to the home region options on `person`. The company now has staff working from outside the Philippines and the four existing values cannot describe them.

## What I will check when you publish

I will call `tools/list` on the published deployment and count the tools against your table. I will then create one record of each of the seven priority objects over the protocol and confirm each appears on its screen, carries its audit entry with the arrival channel and session identifier, and refuses correctly when the gate or the permission says it should.
