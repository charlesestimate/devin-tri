# Coverage table accepted — decisions on all twelve points

The table is accepted. It is the first report in this build that states what is missing without rounding up, and the notes column is genuinely useful. Two of your findings matter more than the tooling gap itself; they are at the end.

Answers below. Each cites the section that already defines the object, so none of these is a new decision — they are readings of the original instruction. Where I say "own table", the object is already specified with fields and you should build it to that specification, not invent one.

## 1. gate_trigger — own table, referenced by gate

Section 8.1 defines it: `trigger_type` (`always` / `value_above` / `value_below` / `percentage_below` / `condition`) · `threshold_value` · `threshold_basis` (`absolute_peso` / `percentage_of_policy` / `percentage_of_block_budget`) · `condition_expression`.

You have conflated two different things. `gate_trigger` is the **rule** that decides which gate applies: above ₱100,000 goes to gate 5. `approval_request.triggerValue` is the **evidence** on one request: this purchase order was ₱250,000. Both must exist. The rule is configuration, changed under gate 31; the evidence is a fact about a record and never changes.

This is not cosmetic. Requirement F3.5 says the gate that applies is derived from the amount, never chosen from a dropdown, and section 6 says that if a gate value appears in a source file, it is wrong. Without `gate_trigger` as rows, those thresholds are living in code.

## 2. resource_availability — computed read, no table

Section 8.10 settles it in its first words: "computed, never entered." Fields are `resource_id` · `resource_class` · `current_assignment` · `available_from` · `status` (`available` / `assigned` / `in_transit` / `maintenance` / `unavailable`), derived from deployments and equipment. Expose list, get and search as computed reads; create and update do not exist for it.

## 3. transmittal — own table, and you already have the data

Section 8.9 defines it fully: `transmittal_number` · `job_order_number` · `from_location` · `to_location` · `purpose` · `system_reference_number` · `date` · `time_of_release` · line items with quantity, unit and item description including brand, size, colour and capacity · `prepared_by`, `confirmed_by`, `received_by`, each a signature and a date · state (`draft` / `awaiting_approval` / `issued` / `in_transit` / `received`).

This is not a document with a class of "transmittal". It is the inter-warehouse movement record — the object that appeared as TRF-0001 and TRF-0002 in September testing, moving 200 panels from the Laguna warehouse to Dumaguete and raising a discrepancy when 180 arrived. That table exists under some name already. Map `transmittal` to it, and if the fields above are missing, add them.

## 4. mention — read tools only

Section 8.13 defines it: `message_id` · `mentioned_person`, exactly one per row · `notification_id`. Build list, get and search. Do not build create or update: a mention comes into existence only inside `post_message`, in the same transaction, and mentioning three people creates three rows. Mark create and update in the table as "created only within post_message".

## 5. site_photograph — own table, referencing the file record

Section 8.7 defines it: `site_photograph_id` · `site_report_id` · `project_block_id` · `image` · `created_on_device` · `caption`.

It carries a block and a caption, which a generic file record does not have, so it is a real record rather than a filtered view. It must not become a second upload path. The bytes, hash, Drive folder path and storage state stay in the `files` record built last week; `site_photograph` holds a `file_id` plus the block, the device time and the caption. One upload path, one file table, domain meaning on top.

## 6 to 11. The operations and maintenance objects — all specified, none optional

`service_agreement`, `service_level_term`, `serviced_asset`, `serviced_asset_equipment`, `service_charge`, `warranty_claim` and `work_order` are specified in full in section 8.23, each with its fields, its state machine and its gates. Build all seven tables to that specification. Two mappings you proposed must not be made:

**`service_agreement` is not a contract with a type of "service".** Section 8.23 is explicit: a service relationship attaches to a **site**, never to a project, and outlives every project on that site. A contract attaches to a project. They are different objects with different lifetimes. The agreement also carries `agreement_document_id` as a hard requirement — an agreement whose signed document is not loaded stays `draft` and produces no charge — plus commencement date, term, derived expiry, renewal notice days, scope of service, charge basis, charge amount, charge period, escalation percentage and month, and predecessor and successor references.

**`serviced_asset` is not a project in a late status.** The same section: this module covers assets that may have no project record, no block structure, no as-built drawings and no bill of materials, because Magnus did not necessarily build them. A serviced asset exists for a site Magnus never touched until the service contract was signed.

`maintenance_plan` and `generation_reading` you already have as `om_schedules` and `om_readings`; confirm their fields match 8.23 and rename if the mapping is loose.

## 12. report_register and measure_register — both own tables

Section 8.18 defines both. `measure_register`: measure · source records · owner, a named person · cadence · **the decision it informs, required — the platform refuses to save a measure without one**. That refusal is acceptance test 155. `report_register`: every standing report, by module, with its owner and cadence, on the principle that a standing report nobody reads is removed.

## The two findings that matter more than the tooling

**First: operations and maintenance was never built.** Seven of that module's nine objects have no table. That module was specified in a follow-up instruction in September, confirmed as Milestone 6, and reported at various points as covered. It is not. Correct the milestone record to show it as not started, and do not report it otherwise again. Build it as Milestone 6 in the existing order — not as part of this work.

**Second: `homeRegion` is an unconstrained string.** You noted this in passing. It means the four-value constraint in section 8.1 was never enforced, so any typo creates a region that exists only in one row and matches nothing. Make it a real enumeration with five values: `Luzon`, `Bicol`, `Visayas`, `Mindanao`, `overseas`. Check the existing 19 person rows for values outside that set and report anything you find rather than silently correcting it.

Also: `list_persons` returns only identifier, display name and status. A person's population, employment basis, home region, sign-in state and roles are all invisible over the protocol, which is why the tool cannot answer the simplest question about staffing. Fix that as part of the person group.

## Order of work — unchanged

Build group one first — person with `grant_sign_in`, party, account, site, contact, item, location — then publish before starting group two. Update the coverage table with each publish so the count of remaining rows is always visible.
