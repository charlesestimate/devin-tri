# Decisions: Model Context Protocol scopes and migration loading

Agreed 3 September 2026. These go into the Hercules fix prompt as written.

## Four session scopes, no bypass

| Scope | May do | May never do | Who creates | Expires |
|---|---|---|---|---|
| **Read** | Every list, get and search in section 8; every computed query in section 12.2; audit chain verification | Any write | Any account holder, for themselves | 90 days |
| **Write** | Create and update records the person may create on screen: tasks, notifications, messages, non-conformance reports, site records, documents, data corrections with a reason | Approve any gate; raise a purchase order, fund request, variation order or write-off; any configuration | Any account holder, for themselves | 14 days |
| **Decide** | Submit an approval decision on any request where the person is primary or alternate; configuration under gates 22 and 31 and the push list; hard block **values** under gate 31 | Gate 32; console holders; single-handed statutory rates; the existence of a hard block; self-approval; gates 18, 28, 29 and 30 unless the person is the officer of record | Console holders only; second console holder notified | 12 hours |
| **Migrate** | The one-time import tools in section 8.21 and the reverse-import tool; the opening stock lock request routed to gate 27 | Anything outside import; any approval; any configuration | Console holders only; second console holder notified | The cutover date, then the scope cannot be created again |

Rules that apply to all four:

1. Scope is fixed at creation, stored on the session record and stamped on every audit entry with the session identifier. Raising scope means a new token.
2. Every Decide and Migrate tool is two calls: `propose` returns the full statement of the change and a one-time confirmation code; `confirm` applies it. A client that skips the second call changes nothing.
3. Self-approval is refused across scopes. Two tokens held by the same person are the same person.
4. Nothing in any scope can disable a hard block. The enumerate-every-tool test in section 12.5 covers all four scopes.
5. A break-glass fifth scope is **not** built now. If needed later: both console holders present, one-hour expiry, `break_glass` on every entry, push with mandatory acknowledgement to the second console holder and the Head of Finance, alternate authority only on gates that have an alternate, never 18, 28, 29, 30, 32, never a hard block, never self-approval, still propose-then-confirm.

## Migrate scope: import tools to build

One tool per sheet of the migration workbook, each taking a batch of rows and returning a batch identifier, per-row result, and the list of rows refused with reasons:

`import_roles` · `import_persons` (with aliases; three spellings become one record) · `import_parties` · `import_accounts` · `import_sites` · `import_contacts` · `import_items` · `import_equipment` · `import_locations` · `import_opening_stock` · `import_projects` · `import_contracts` (document required for active) · `import_project_parties` · `import_project_blocks` (value weights computed from loaded block cost; percent complete seeded from the loaded position and derived afterwards) · `import_bill_of_materials` · `import_open_purchase_orders` · `import_project_permits` · `import_billing_milestones` · `import_service_agreements` (document required for active; no document loads as draft and produces no charge) · `import_service_level_terms` · `import_serviced_assets` · `import_asset_equipment` · `import_maintenance_plans` · `import_open_work_orders` (device timestamps where known, server otherwise, marked migrated) · `import_open_warranty_claims`.

Plus: `reverse_import(batch_id)` allowed until the opening stock lock for that batch's warehouse or, for non-stock batches, the cutover date; `list_import_batches`; `validate_import` which runs every check without writing.

Every imported record carries `migrated = true`, `import_batch_id` and `source_reference`. Every import writes one audit entry per row under the importing person with arrival channel Model Context Protocol and the session identifier. Gates are not replayed on migrated state; the gate outcome as it happened is stored where the sheet captures it (counsel review state, approver and date on open purchase orders).

## Loading workflow

1. Karl fills the workbook, or points at the existing spreadsheets and Drive folders it should be filled from.
2. Claude validates offline: duplicates and aliases, links between sheets, missing contract and agreement documents, projects with no site, items with no unit, agreements with no service level term, open purchase orders on projects with no contract.
3. Load in the README order, one sheet per batch, on a Migrate token. Karl checks each on screen.
4. A wrong batch is reversed and reloaded.
5. Jay, Bernie and Paul count; Cristy spot-checks; gate 27 locks each warehouse. The Migrate scope ends on the cutover date.

## Open question before any real data is loaded

Whether the current Convex deployment becomes production or is a development copy. Real contracts, people and stock are loaded once, into the deployment that will go live.
