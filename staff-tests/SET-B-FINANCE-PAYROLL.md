# Set B — Finance and Payroll, done the way you do it today

**For:** the Head of Finance, with the payroll officer for Part 4. One or two people.
**Where:** office, on a laptop. Have your current Excel files open beside the platform.
**Time:** about 3 hours.
**Projects to use:** P1 — Calamba Agro Industrial Corporation (contract ₱28,800,000, three billing milestones already exist) and P5 — Dasmariñas Plastics Manufacturing Corporation (₱1,900,000).
**Prefix:** every record you create starts with `HT-B`.

## Why a human has to do this

The browser agent checks that buttons work. It cannot say whether the progress claim screen has the fields you actually need, whether the payroll figure matches what you compute today, or whether a step takes you longer than your spreadsheet. Only you can.

## Rules

1. Write down exactly what the screen says when something is refused. Screenshot and number it (B-01, B-02, ...).
2. Do not invent a result. "Could not find" is a valid answer.
3. Never delete anything. Never edit a record you did not create unless the step says so.
4. Use **real figures from one real past transaction** where the step says so, but change the client and supplier names. Do not enter real salaries; use the test rates the step gives.
5. Karl approves what you cannot approve yourself. Message him on the platform, not on Viber, so the notification path is also tested.

## Part 1 — What you see, what you must not see

| Step | Do this | Expected | Record |
|---|---|---|---|
| 1.1 | Sign in. Read the sidebar. | Finance, Payroll and Human Resource are visible. | Write the sidebar as you see it. |
| 1.2 | Open P1. Find contract value, cost, and margin. | As Head of Finance you see money. Note which of the three you see. | Which figures. |
| 1.3 | Open Human Resource, open your own person record, then another person's record. | Whether you can see salary, ratings or disciplinary records depends on your role. Record what you see; do not change anything. | What was visible on each. |
| 1.4 | Open Administration. | Either not in your sidebar, or open but the audit chain, gates and hard blocks are read-only to you. | What you could open. |
| 1.5 | Open Reports. Look for any report that ranks people by output or shows login times or activity. | There must be **none**. | Anything found. |

## Part 2 — Progress claim and retention (Head of Finance)

| Step | Do this | Expected | Record |
|---|---|---|---|
| 2.1 | Open P1 Finance. Look at the three billing milestones. Compare them with how a real Magnus contract's billing schedule is written. | The screen holds every field your real schedule has. | Fields that are **missing**, and fields you never use. |
| 2.2 | Raise a progress claim `HT-B claim 1` on P1. Look at the percent complete. | It is the **derived** figure from the site reports. You cannot type it. | The figure. Could you type over it? |
| 2.3 | Try to approve your own claim. | Refused: you raised it. Even though gate 11 names the Head of Finance as primary, a person cannot approve their own request. | Exact text. |
| 2.4 | Ask Karl to raise `HT-B claim 2` on P1. When it reaches you, approve it. | Gate 11 shows primary Head of Finance, alternate Chief Operating Officer, window 2 days recorded but **not enforced**. | Was the window shown? Did anything threaten to escalate? |
| 2.5 | Enter a **certified amount lower** than claimed on claim 2. | Both figures are kept; neither overwrites the other. | Screenshot. |
| 2.6 | Raise a **retention invoice** on P5 before its retention date. | Refused or warned; the retention date comes from the turnover date the agent entered. | Text. |
| 2.7 | Compute retention by hand from P1 (10 percent of the certified amount) and compare with what the platform shows. | Equal to the peso. | Your figure, the platform's figure. |
| 2.8 | Take one **real past progress billing** (client name changed). Enter it as `HT-B real billing` on P5. Time yourself. | You can enter everything you needed for the real one. | Minutes taken. Anything you could not enter. How long the same billing takes you today in Excel. |

## Part 3 — Write-offs, fund requests and refusal 3 (Head of Finance)

| Step | Do this | Expected | Record |
|---|---|---|---|
| 3.1 | Ask Karl to raise three write-offs on P1: ₱45,000, ₱75,000 and ₱150,000, each named `HT-B write-off [amount]`. | ₱45,000 → gate 1, primary Head of Finance. ₱75,000 → gate 2, primary Chief Operating Officer, alternate Chief Executive Officer. ₱150,000 → gate 3, Chief Executive Officer only, **no alternate**. | Which gate appeared on each, and who it named. |
| 3.2 | Approve the ₱45,000 one. Try to approve the ₱75,000 one. | First succeeds. Second refuses: you are neither primary nor alternate. | Text. |
| 3.3 | Raise a **fund request** `HT-B advance 1` on P1 for ₱20,000. Ask Karl to approve and release it. Look at the liquidation due date. | Fifteen days from release, computed, not typed. | The date. |
| 3.4 | Without liquidating, raise `HT-B advance 2`. | **Refused**: unliquidated advance. Finance and Human Resource are informed. | Text. Did a notification reach you as Finance? |
| 3.5 | Liquidate advance 1 with a document. Raise advance 2 again. | Allowed. | Result. |
| 3.6 | Try to raise a fund request on a project with **no contract**. Ask Karl which pipeline customer has none. | Refused, naming the missing contract, never "no permission". | Text. |

## Part 4 — Payroll, "no report, no payroll" (payroll officer with the Head of Finance)

The browser agent filed site reports on P1 for three consecutive workdays with toolbox attendance of five, six and four crew. Use those days.

| Step | Do this | Expected | Record |
|---|---|---|---|
| 4.1 | Open Payroll. Create a period `HT-B period 1` that covers the three reported days **and at least one working day with no site report** on P1. | Created. Period state shows **blocked, incomplete reports** and lists the missing site day. | State shown. Missing day shown? |
| 4.2 | Try to generate the register. | **Refused.** The whole run is blocked. **No individual worker is dropped.** | Text. Does it say who to chase (Person In Charge and their manager)? |
| 4.3 | Ask Karl or the Person In Charge to file the missing report. Generate again. | Register produced. | Time between the report being filed and the register being available. |
| 4.4 | Open the crew lines. Compare **days worked** with the toolbox attendance: a crew member present on all three days shows 3; one present on two days shows 2. | Days come from toolbox attendance, not from any clock. | A table: name, days you expect, days shown. |
| 4.5 | Look for a clock-in, clock-out, time or location field anywhere in Payroll or Human Resource. | There must be **none**. | Anything found. |
| 4.6 | Take one real crew rate structure (use test rates: basic ₱610 per day, overtime 25 percent, allowance ₱100). Compute one worker's Social Security System, PhilHealth, Pag-IBIG and withholding in your own Excel. Compare with the platform line. | Equal, at the rates in force for that period. | Your figures beside the platform's, item by item. Which one is wrong, if any. |
| 4.7 | Try to type a **net pay**. | Impossible; it is computed. | Result. |
| 4.8 | Change one contribution table row **effective next month**. Reopen `HT-B period 1`. | Its figures are **unchanged**. | Before and after figures. |
| 4.9 | Try to **close** the period while the acknowledgement sheet is outstanding. | **Refused**: refusal 2. | Text. |
| 4.10 | Release payroll. | Gate 23, Head of Finance primary, Chief Operating Officer alternate, one-day window recorded only. | Who it named. |
| 4.11 | Open the **headcount variance** query for the three days. | Every day where people paid differs from attendees recorded is listed. If the agent's data is consistent, the list is empty; note that. | What it showed. |
| 4.12 | Ask Karl (console holder) to open the register, a payslip and a rate table from his account. | All **refused** for a console holder. | What Karl reports. |

## Part 5 — Two people, one record (with Karl, ten minutes)

| Step | Do this | Expected | Record |
|---|---|---|---|
| 5.1 | You and Karl open `HT-B claim 2` at the same time. Karl posts a message on its thread. Do **not** refresh. | The message appears on your screen by itself within seconds. | Seconds taken, or "did not appear". |
| 5.2 | Both of you edit the claim's notes at the same moment and save. | The platform tells one of you the record changed, or shows both edits; it does **not** silently lose one. | What each of you saw. |
| 5.3 | Karl mentions you in the message. | You receive **exactly one** notification, category Response, that opens the claim. | Count and category. |

## Part 6 — Fit to real work (write answers)

1. Take your last month-end close. List the steps. Beside each, write whether the platform has a place for it, and where.
2. Which report do you produce weekly that you could not produce from Reports today?
3. Which figures did the platform compute differently from your Excel? Which one is right?
4. Which words on screen did you not understand, and any abbreviations? Write them exactly.
5. If Magnus ran payroll on this next period, what would stop you?

## Report — send to Karl within two days

Word or Google document, `HT-B finance report — [name] — [date]`.

1. Tester names and roles.
2. **Step table:** every step, result (**pass** / **fail** / **could not find** / **blocked, needed Karl** / **not tested**), what happened, screenshot numbers.
3. **Figure comparison tables** from steps 2.7, 4.4 and 4.6.
4. **Things you could see that your role should not**, and things you could not see that you need.
5. **Things that happened by themselves** (escalations, reminders, status changes you did not make).
6. **Fit to real work** answers (Part 6).
7. **Records you created**, by name.
8. **Top three problems**, in order, one sentence each.

Attach all screenshots, numbered.
