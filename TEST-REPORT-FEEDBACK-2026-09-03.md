# Feedback on the Phase 1 browser test report

Report read in full: 20 module sections, 10 top findings, 40-item abbreviation list, 12 usability items, data inventory. It is a good report: nothing rounded up, refusals by absence called out as such, reproduction steps on every failure.

## 1. What the report actually says

The build is not a buggy version of the specification. It is a different, generic platform that borrows the specification's vocabulary. The evidence:

| Specification says | Build does |
|---|---|
| Six hard blocks, closed list, section 5: insurance, safety program, B0 sign-off, prerequisite permit, quarantine, signed contract | Six hard blocks with different meanings: "Daily Report Required for Payroll", "Toolbox Meeting Required", "Open Permit Blocks Closeout", "Fund Release Requires Approved Request". Two of the six are the payroll refusals, not hard blocks |
| Gates are rows with primary and alternate roles; self-approval refused everywhere (R6) | Every gate "Primary: Unassigned"; the raiser approves their own item on gates 1 to 7, 19, 20, 28, 29, 32; only gate 26 and bank confirmation refuse |
| Gate chosen by amount (write-off 1/2/3, purchase order 4/5) | Gate chosen from a dropdown by the user; ₱8,550,000 went to gate 4 |
| Block spine B0 to B11 plus General Requirements and Battery Energy Storage System, value weights, percent derived | Nine generic blocks "Mobilization … Snagging", typed cumulative percent, project percent is an unweighted mean |
| Roles, permissions, record scope, money visibility, sign-in grant, exactly two console holders | No roles, no permissions, no way to grant sign-in, one console holder |
| Signed document is a file; toolbox photograph is in-app capture; evidence is a file | No file upload anywhere; every document is a typed reference string |
| Operations and Maintenance, section 8.23, delivered in the second prompt | Placeholder "on the roadmap" |
| Communication module 14 | Read-only Messages screen with no compose |
| Hard block 6 blocks fund requests | Fund request created on a project with no contract |
| Stock cannot go negative; goods receipt posts to stock; inter-island transfer is gate 25a | Dispatched 200 from a warehouse holding 0; receipt never posted; no gate |

Add the outright bugs: progress claims throw a server error, purchase order numbers repeat across projects, audit entries carry no actor name, the board pack shows zero pending approvals with nine pending, permit duration counts calendar days, times render in UTC, an unclassified document can be registered as usable.

## 2. Why this happened

Hercules reads the beginning of a long prompt well and drifts as it goes, then fills gaps from a generic template. The sidebar drift, the renamed hard blocks and the ignored Operations and Maintenance prompt are the same failure. A single long corrective prompt will meet the same reader, so its structure matters more than its length.

## 3. Recommendation: one prompt, built as a conformance pass

Agree with one prompt. It should not be a list of 200 fixes. It should be a conformance instruction with four properties:

1. **The specification is the authority, restated in the prompt where the build deviates.** Each section names the original section, states what exists, states what must exist, and says "replace" or "add". Hercules is told that where the build and the specification differ, the specification wins, without exception.
2. **Foundation first, in a fixed order, with a stop after each milestone to report.** Roles and permissions → sign-in grant and second console holder → gate rows with role check and universal self-approval refusal → gate selection by amount → the six hard blocks exactly as section 5 → file store on Google Drive → then the data model corrections module by module → then the missing modules (Operations and Maintenance, Communication, protocol scopes and migration) → then labels, sidebar, abbreviations, dates and times → then usability.
3. **A conformance checklist Hercules must fill before building.** One row per requirement in the prompt: exists / deviates / missing. This forces the whole prompt to be read and gives Karl a document to check against.
4. **Tests are the exit.** The acceptance tests from section 14 and the appended tests 190 to 258 are rerun at the end of each milestone. The report says "pass by absence" is not a pass.

The three prompts already written, protocol and migration (MCP), Communication and Drive, and the earlier Operations and Maintenance prompt, become sections of the one prompt rather than separate messages.

## 4. Size of the work

This is a second build pass, not a patch. Roughly: foundation and file store two to three Hercules milestones; data model corrections across nine modules four to six; the three missing modules three to four; labels, dates and usability one to two. Expect several days of Hercules time and two or three rounds of retest. The fast alternative, exporting the code and correcting it directly with Claude Code, depends on whether Hercules can export the repository; that question still stands.

## 5. Three things in the report that are not defects

- The "Claude Code review" agent session and the HT-MCP task are mine, from the protocol check at 12:45.
- The "test2" and "This is a test" accounts and audit entries 1 to 8 predate the test; they are Karl's own trial entries.
- Gate 26 and the supplier bank confirmation refusing the raiser prove that the refusal mechanism exists in the code and was simply not applied elsewhere. That makes the fix a matter of applying one rule everywhere, not inventing it.

## 6. One thing in the report that needs an answer

Audit entries 263 and 264: an agent session named "Unnamed session" was created and revoked at 14:26, during the test. I created only one session, at 12:45. If Karl did not create the second one while looking at the Agent Sessions tab, it needs to be explained before any real data enters the platform.

## 7. Decisions needed before the one prompt is written

1. Google Drive account: dedicated with its own storage plan, or personal for now. File upload underpins hard blocks 1 and 6, toolbox photographs, document control and evidence, so the prompt cannot leave the file store open.
2. The second console holder: who. The specification requires exactly two; the platform's own rule says a second holder cannot be removed. Gate 32's alternate is that person.
3. Whether this deployment goes to production. If yes, the prompt includes a test-data wipe step before migration; if it is a copy, it does not.
4. Confirmation that the future-dated system constant (Markup, Major Equipment 116 percent, effective 1 January 2030) is to be superseded in the prompt.
