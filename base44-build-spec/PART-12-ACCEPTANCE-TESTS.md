# Magnus Workspace Platform — Base44 build specification

## Part 12 · Acceptance tests — 1 to 258, plus 259 to 280 from the first build's defects

**The build is not done until all of these pass. None is visible in a demonstration and none is revealed by clicking through screens. Turn them into a suite that runs, not prose that is read.** Each part names which tests it makes runnable; run them then, and run the whole suite before reporting complete. Report the output, never a sentence saying it passed.

---

## The seven that decide whether the platform is fit for use

1. **The audit log is genuinely immutable.** Alter an entry through the builder's data console. Verification reports a broken chain with the true last sequence. Attempt update and delete from any backend function — refused.
2. **Tenant isolation is enforced at the chokepoint.** Call every read and write as a person of one tenant with a record identifier of another. Nothing returned, nothing written. The build-failing test for client-side writes to governed tables passes.
3. **Offline capture preserves creation time and survives reconnection.** Create records offline, reconnect after a delay; both timestamps present; nothing lost or duplicated.
4. **Percentage-of-completion and payroll calculations are correct** against manually computed cases.
5. **Cryptographic erasure works over the immutable log.** Erase a data subject under gate 35; content unrecoverable; chain verifies; Drive files gone; legal hold refuses it.
6. **Effective dating on system constants.** Build a record, change a constant, reopen — the old value; a new record — the new value.
7. **A hard block cannot be disabled.** Attempt each of the six from Administration, from the data console, by permission escalation, and through the protocol. All fail, all logged.

## The test of this entire specification

8. **Nothing runs unattended.** Deploy, leave twenty-four hours with no user and no agent. Nothing changed: no notification, no state advanced, no approval moved, no invoice, no task, no escalation. The audit log for the period is empty. **If anything happened, automation was built and must be removed.** Also: the builder's automation list is empty.

## Governance

9. **No auto-approval.** Every gate sits indefinitely; nothing reaches `approved`.
10. **Alternate authority refusal.** Save an alternate with a lower limit than the primary — save fails.
11. **Self-approval.** One person as requester and approver — offered to the alternate, logged.
12. **Block precedes gate.** An action both blocked and gated raises no approval request.
13. **Gate 10 distinguishes two outcomes.** `proceeded_without_review` is never `approved` and appears in the counsel query.
14. **Gate 25 splits.** ₱30,000 inter-island requires approval; ₱30,000 within-island does not.
15. **No module implements its own approval.** Code review: no approval logic outside the engine; every approval point calls it.
16. **Hard block table has no `active` column**; no enable, disable or delete control on any screen.
17. **Blocked-action message** names the block, the unmet condition, what releases it and who can supply it — never *you do not have permission*.
18. **Gate 18 has no alternate.** A seal sits indefinitely.

## Identity and permissions

19. **Multi-role union**; approval limit is the higher, never the sum.
20. **Money visibility is independent.** `project` scope with `none` sees the full material list and no cost anywhere, including exports and printed views.
21. **Identity revocation.** Disable the provider account — the session ends and cannot resume, no administrator action.
22. **Console holder count.** A third holder and removal of the second both fail.
23. **Crew are not users.** `signs_in` false — no `identity_subject`, appears in deployment and payroll, cannot be granted a session.
24. **Offboarding blocks on open work** — refuses and lists the item.
25. **Console holder is excluded from Human Resource and payroll data.**
26. **Role history survives.** Deactivate a role referenced by a historical approval — the name still displays.

## Pipeline and contract

27. **Site is separate from account.** One account, eleven sites, each with its own assessment and permit history.
28. **Sizing references the constant.** New proposals use the new value; existing retain theirs; the version is retrievable.
29. **Contingency never leaves.** Export and print in every format — contingency in none.
30. **Winning version is frozen.** Edit after win — fails.
31. **Gate 6 applies to every quotation.** A ₱50,000 quotation requires Director approval.
32. **Gate 7 band.** 112% major — Director; 108% — Chief Executive Officer only, no pass-down.
33. **Loss reason above ₱10,000,000** required; *did not proceed* reported separately.
34. **Won does not mean active.** Project in `setup`; cannot activate without the signed contract.
35. **Hard block 6 blocks purchase orders.** Raise one on a contractless project — fails.
36. **A tick-box does not satisfy a document block.** Every contract field set except the document — still blocked. Same for the insurance certificate.
37. **Unread is not absent.** Unpopulated risk terms report `not_yet_read`.
38. **No stored phase.** No `phase` column; a project in three stages displays a distribution.
39. **Variation does not overwrite.** Contract intact; weights re-base only on `accepted`.
40. **One date, three clocks.** Turnover date sets retention, warranty and operations dates with no second entry.
41. **Portfolio total crosses record scope**, subject only to money visibility.

## Design, procurement and site

42. **One bill of materials, two views.** No second procurement table.
43. **Every bill of materials line has a block.**
44. **Seal attaches to a revision.** Revision 4 after sealing 3 is unsealed.
45. **Retrospective licence check.** A licence expiry earlier than an existing seal flags every affected design.
46. **Waiting is never anonymous.** Both `waiting_on` and `waiting_since`; cumulative client days sum correctly.
47. **Ordered lines are not silently changed.** A revision altering an `ordered` line flags and requires a decision.
48. **Reinforcement raises a variation, not a task.**
49. **Weights exclude General Requirements** and re-base only on an accepted variation.
50. **Capacity difference is visible**, neither overwritten.
51. **Expected arrival is required** on `ordered`.
52. **Block readiness is computed**; `partially_ready` carries the outstanding line's date.
53. **Committed cost begins at issue.**
54. **Overrun states its kind** — price or additional items.
55. **Partial delivery** keeps the line open with its own date.
56. **Off-design is recorded, not absorbed** — reason and block required; appears in the query.
57. **Bank change control** — second person confirms; previous values retained; next payment flagged.
58. **No manual supplier score screen.**
59. **Foreign exchange variance** appears outside the margin.
60. **Non-conformance quarantines.** A damaged receipt lands in quarantine; hard block 5 prevents issue.
61. **No typed percentage.** Search the platform — none.
62. **Every activity has a block.**
63. **General Requirements has no weight** — the curve reads 100 with permits open.
64. **Hard block 3.** B1 with B0 unsigned — fails and is logged.
65. **Toolbox meeting required, attendees named** as person references, not an integer.
66. **Headcount variance is reported.** Pay eight, record six — visible to the Project Manager and Finance.
67. **Variation shows before and after** percentages.
68. **The spine is not configurable** by a console holder.
69. **Blocked material carries a date** from the outstanding line automatically.
70. **Weather stoppage is retained** as dated evidence attributed to the recorder.

## Permits, inventory and safety

71. **One permitting route.** Six cases, one permit set, no branch logic.
72. **Permits and permits to work are separate tables** with no shared code.
73. **Expected date required on filing**; 90-working-day default with no history.
74. **Accumulation overrides the default.** Three at 60 days — the fourth forecasts 60.
75. **Requirement library accumulates**, appears at filing with `times_observed`, no editing screen.
76. **Additional requirement is not a delay** — task raised, library written, date re-based and shown as re-based.
77. **Prerequisite blocks mobilisation** and is an exception from day one.
78. **Closeout exposure is valued.**
79. **Gate 20 has no threshold.** ₱2,000 still requires approval.
80. **Stock moves on receipt.** Origin decreases, in transit increases, destination unchanged until signature; total conserved.
81. **Discrepancy raises immediately** to both custodians and the Procurement Head.
82. **Route class derives from the form.** Laguna → Dumaguete inter-island, 10 days; a Bicol site from Laguna is inter-island.
83. **All four directions.** Site → warehouse accepted.
84. **Hard block 5** at every permission level — fails and is logged.
85. **Zero tolerance** — one unit short requires investigation; closing reason in the distribution.
86. **Every issue names a block.**
87. **Surplus returns at cost.**
88. **Site stock is stock.**
89. **Opening balance records both dates.**
90. **Reorder points do not apply to project material.**
91. **Gate 28 cannot be automated** — auto-approve, delegate or window at every level fails.
92. **Competency gating** — a lapsed worker cannot be named.
93. **Permit validity is enforced** as a live finding.
94. **Near-miss needs no login.**
95. **No reporter identity anywhere** outside the safety function.
96. **Push acknowledgement cannot be disabled** on the three; adding a fourth category succeeds.
97. **Safety indicators are derived** — no entry screen.
98. **Corrective actions closed without evidence are permitted and reported.**
99. **Emergency card works offline.**
100. **Subcontractor exclusions are held** and reported.

## Work, money and people

101. **No duration fields** — no `hours`, `time_spent`, `started_at`, clock, location or duration anywhere; the site-level hours are attached to no person.
102. **Output type required.**
103. **Automatic closure** — filing a site report closes its task.
104. **One owner.**
105. **Blocked requires a name** and appears on the blocker's screen.
106. **Carry-forward** — an unfinished task is on tomorrow's screen.
107. **Committed date is permanent**; `recommit_count` reads 4 after four moves.
108. **Priority is scarce** — a fourth from one requester fails.
109. **No aggregate per-person score** anywhere.
110. **No ranking of people** on any screen, query or export.
111. **No-task flag routes correctly** — manager and director; never the person; count across managers on the executive view; none for approved leave.
112. **Load is a band** — no numeric load anywhere.
113. **Self-registration counts identically.**
114. **Mention governs notification.** Ten unmentioned messages — none; no mute, watch or subscription.
115. **Message de-duplication and ordering.** Retries post once; composition order; text before attachment.
116. **Messages are append-only.** Edit and delete as console holder fail outside the Announcement path; hide is logged.
117. **One-tap conversion** to a task with output type and link back.
118. **Photograph prompt** on a block thread offers the site report.
119. **Records link to revisions, not documents.** Revision 3 remains on the report after 4 and 5.
120. **One revision in force**; a superseded revision announces itself and links to the governing one.
121. **Unclassified is visible but unusable** for a work instruction.
122. **Acknowledgement is per revision.**
123. **Required-document register is derived** — no hand-built checklist.
124. **Form revision is recorded on records.**
125. **Permanent classes never expire**; legal hold overrides retention.
126. **No general ledger** — no chart of accounts, no journal, no write to accounting.
127. **Fund release blocked** on a contractless project, logged.
128. **Claimed and certified are separate.**
129. **Uncertified escalation carries the client baseline.**
130. **Three confidence bands**; every gated line names gate, owner and age.
131. **Gap detection** valued with the gated cash that would close it.
132. **Over- and under-billing** compute correctly.
133. **Reconciliation reports variance**, not absorbed.
134. **Unliquidated advance blocks the next request.**
135. **No computed rating**; a rating with no reasons fails.
136. **Engagement responses are not identifiable** — no `person_id`.
137. **Buddy is not the manager.**
138. **Regularization is diarised** ahead of the date.
139. **Source effectiveness is twelve-month.**
140. **Self-service works without Human Resource.**
141. **Attrition by manager is a Check**, not a score.
142. **Payroll: the block lands on the run** — register not generated; no worker dropped.
143. **Historical reproducibility** — March reproduces exactly after a June rate change; each line names its version.
144. **Unapproved rates do not compute.**
145. **Statutory figures cannot be overridden** at any level.
146. **Brackets, not percentages** — a boundary salary to the peso.
147. **Attendance has no clock**; `days_worked` derives from toolbox attendance.
148. **Separation of duties** — compute and release as one person fails.
149. **Acknowledgement gates the period.**
150. **Three-cycle parallel run** — cutover after one cycle refused.
151. **Overtime only where worked.**

## Reporting and the protocol

152. **Silence states what was checked** — time and rule count; a blank panel is a failure; no domain evaluates zero rules.
153. **Every exception names a person** with a valued so-what.
154. **Drill reaches the log.**
155. **Measure register enforces a decision.**
156. **Gaming guards hold** — no per-person load score, grade aggregate, reporter identity or safety score anywhere.
157. **Role scoping** — a Project Manager sees own-project exceptions only.
158. **Board pack generates** with no manual step.
159. **Money visibility respected over the protocol** — no answer, and the query never reads the value.
160. **Record scope respected over the protocol** — no acknowledgement the project exists.
161. **Configuration carries a human name** and the arrival channel.
162. **Same authority** over the protocol as the screen.
163. **Confirmation before applying** — stated back in full.
164. **Gates apply** — a constant change fires gate 22 with no alternate.
165. **Statutory rates writable, results not.**
166. **Tenant scoping** over the protocol.
167. **Every call audited** — reads and writes.
168. **No tool can disable a hard block** — every tool and parameter enumerated and attempted.

## Field, product and migration

169. **Full offline day** captured and synchronised.
170. **Offline day attribution** — created Monday, synced Thursday, it is Monday's.
171. **No approvals offline** — refused with a reason.
172. **No silent loss** — failed uploads retained and shown as unsent.
173. **Queue is visible** with retry.
174. **Resumable upload** survives interruption; original retained.
175. **Gallery prohibition** — none written, no route to attach from it.
176. **Compression** — about 300 kilobytes.
177. **Revocation kills the device cache.**
178. **Pre-population** of tomorrow's report.
179. **No Magnus literals in code** — search for the values and brand names.
180. **Second tenant profile runs.**
181. **Full export works** — complete, schema-enumerated, documented, re-importable, logged, permission-scoped, tenant-filtered.
182. **Tested restore** recorded.
183. **No outbound email** — no transport configured; nothing leaves by mail.
184. **The platform does not file** to any government channel.
185. **Aliases prevent duplicates.**
186. **Workday seeding** — 84 loads, next is 85.
187. **Import reversible before lock**, refused after.
188. **Old stores are read-only.**
189. **Accumulated figures carry sample size.**

## Operations and maintenance

190. **An agreement attaches to a site, not a project.**
191. **A signed document is required** to activate.
192. **Service level terms are required** to activate.
193. **No charge without an active agreement**; activation is the only path, in the same mutation.
194. **Expiring is derived, not fired.**
195. **Lapse is derived, not fired.**
196. **Renewal links both ways.**
197. **Dual timestamps on field capture.**
198. **Response is measured in elapsed device hours** — 65, not one working hour.
199. **Severity selects the promise.**
200. **A preventive visit does not pass through `restored`**; the plan advances in the same mutation.
201. **Service level breaches are never scored against a person.**
202. **A maintenance plan holds the cadence and creates nothing.**
203. **A supplier claim needs a purchase order, not a client clause.**
204. **An asset works with no project.**
205. **Warranty expiry with open work is queryable.**
206. **A service charge is generated, never typed.**
207. **Recurring revenue reaches the forecast** under `secured`.
208. **A service charge cannot be written off outside the ladder.**
209. **Lost generation values at site tariff.**
210. **Yield uses the effective-dated constant.**
211. **Nothing dispatches** — no code path creates, assigns, closes or prioritises a work order except a person's call.
212. **Every operations query returns its evaluation timestamp** with no agent connected.
213. **Gate 34 fires**; the gate table holds thirty-one rows and no row 13 to 17.
214. **Offline transitions are owner-only.**

## Protocol scopes

215. **Read scope cannot write.**
216. **Write scope cannot decide**; `create_task` and `post_message` succeed.
217. **Decide requires a console holder**; the second holder is notified.
218. **Propose writes nothing.**
219. **Confirm applies once** — a reused, expired or foreign code refuses.
220. **Self-approval across sessions** refused.
221. **Money visibility over the protocol** on a Person In Charge token.
222. **Record scope over the protocol** on a Project Manager token.
223. **No path to a hard block** — the enumeration exists and the build-failing test passes.
224. **Statutory rates need the second person** on screen.
225. **Expiry** refused with the reason.
226. **Every figure has sources.**
227. **Hard block 6 flag** — `funds_blocked_no_contract` true without a contract, false after.

## Migration

228. **Aliases collapse** across two batches.
229. **Active needs the document** — refused naming hard block 6; loads with it.
230. **Position is derived, not typed** — 55 percent from the migration activity.
231. **Workday counter seeds** — 62 loads, next report is 63.
232. **Draft agreement produces no charge.**
233. **Reverse before lock**; refused after gate 27.
234. **Migrate scope ends** on the cutover date.
235. **Migrated is visible** — `migrated`, `import_batch_id`, `source_reference`; a report filters on it.
236. **Nothing decides** — role assignments arrive as pending gate 24 requests.

## Communication

237. **One screen.** Company, Direct, Spaces, Threads and Archived with unread numbers; opening clears the number and creates no notification.
238. **Account space is born with the account** in the same transaction.
239. **Roll-up reads across the lifecycle** — five record threads under one account shown in order, each opening its record.
240. **Post from the roll-up lands on the record.**
241. **Automatic membership** follows assignment; past messages remain after removal.
242. **Money never rolls up.**
243. **Invite-only is invisible**; *access for review* requires a reason and notifies the owner.
244. **Speed.** Phone home screen to a sent message on a project channel — no more taps than a Messenger group post; record both counts.
245. **Convert to task in one tap** with the message quoted.
246. **No mute anywhere** — search every screen for mute, watch, subscribe, follow.
247. **Append-only** — hide by an administrator is logged and visible; Announcement edits keep every previous body.
248. **Offline order** — text, photograph, text; no duplicate after three reconnects.
249. **Direct message notifies without a mention** — exactly one.
250. **Group ownership passes** to the longest-standing member, logged.
251. **Account activity read tool** returns records and messages with sources and excludes a group the caller is not in.

## Drive

252. **Device never touches Drive** — no endpoint, no token in the client bundle or network.
253. **Hash before Drive**; a hand-replaced file is reported by `verify_file`.
254. **Folder derived** exactly per the tree; a renamed project renames its folder and the file still opens.
255. **Staged survives Drive failure**; nothing retries by itself; the next upload pushes it.
256. **No sharing links** issued.
257. **Legal hold refuses erasure**; after release, the Drive file is gone and the record remains `erased` with its hash.
258. **Move existing files** — every file moves, verifies, every record still opens.

## From the first build's defects — 259 to 280

259. **Every gate has a primary at seed.** Query the gate table on a fresh deploy — thirty-one rows, none with an empty primary role and empty primary person.
260. **A grant follows the decision.** Assign a role — the `person_role` row is `pending_approval`; the person's permissions and approval authority are unchanged; approve — `current` and effective; refuse — `refused` and never effective.
261. **A granted role cannot approve its own grant.** Assign Chief Operating Officer to a person; that person cannot approve the gate 24 request that grants it.
262. **No duplicate current grant.** Assign the same role twice — the second refuses.
263. **Gate reconfiguration is governed.** As a non-console-holder, change gate 24's primary — refused; as a console holder, it raises gate 31 and applies on approval.
264. **Erasure is gated.** Attempt erasure with a reason but no gate 35 approval — refused; under legal hold — refused.
265. **Export enumerates the schema.** Add a new table; the next export includes it with no code change to a list; no table is read without the tenant filter; a tenant-two row appears in no tenant-one export.
266. **Constants are versioned, never patched.** Through the protocol and the screen, change a constant — a new row, the old row closed, no row where `effective_from` is after `effective_to`.
267. **Revisions cannot be set in force from free text.** The protocol's revision tool refuses `in_force` on an unclassified document and refuses a typed `in_force_from`.
268. **Role creation is unique on both paths.** Create a role with an existing machine name through the screen and through the protocol — both refuse.
269. **One registry.** A script checks every gate number, hard block number and constant name appearing in code and tests against the seed registry and returns clean.
270. **Every hard block is wired.** Trigger each of the six by its action — all six refuse and log; none is a row with no caller.
271. **A goods receipt moves stock** at the receiving location in the same transaction; a damaged line lands in quarantine.
272. **Accounts payable exists** — a supplier invoice is recorded against a purchase order, paid, and the payment after a bank change is flagged.
273. **Every hand-off notifies.** Raise an approval, assign a task, block a task on a person, receive short, assign a work order, activate an agreement — the right person holds a notification in the same transaction as each.
274. **Attach, send and print.** A purchase order, a progress claim, a service charge, a payslip and a distribution sheet each produce a `file` record under the object's folder; a contract, a certificate, a deliverable and a person photograph each upload from their own screen.
275. **Console holder changes are guarded.** As a non-console-holder, add a console holder — refused; remove one without naming a replacement — refused.
276. **Legal hold needs a console holder and a reason.**
277. **Purchase order numbers are per tenant.** Two projects in the same month never produce the same number.
278. **A progress claim is created from the screen** against a contract.
279. **Unread numbers match the database.** Compare every drawn number with the membership row; send to General — the Company header and the sidebar total both move; open — both clear.
280. **A role with no permission rows sees nothing**, not everything. A person with zero rows sees an empty sidebar and a message naming who can grant access.
