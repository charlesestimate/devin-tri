# Set A — Field test on a real phone

**For:** one Person In Charge and one Safety Officer. Two people, two phones.
**Where:** a real site, or any place where signal is weak. You will also switch airplane mode on and off.
**Time:** about 3 hours, spread over one working day.
**Project to use:** P2 — Lipa Cold Storage and Logistics Inc. Karl has prepared it. Do not use any other project.
**Prefix:** every record you create starts with `HT-A`. Example: `HT-A toolbox day 1`.

## Why a human has to do this

The platform is built for the Person In Charge on their own phone, on a rooftop, with bad signal. A browser on a desk cannot test a camera, airplane mode, a printed Quick Response code, a push notification arriving on someone else's phone, or whether the app is usable with one hand in the sun. You can.

## Rules

1. Write down exactly what the screen says when something is refused. Take a screenshot and number it (A-01, A-02, and so on).
2. Do not invent a result. If you cannot find a button, write "could not find", not "does not exist".
3. Never delete anything. Never edit a record you did not create.
4. Note the time of everything you do offline. You will compare it with what the platform shows after it syncs.
5. Do not photograph anything private. Toolbox photographs of the test crew are fine.

## Part 1 — Installing (Person In Charge, then Safety Officer, each on their own phone)

| Step | Do this | Expected | Record |
|---|---|---|---|
| 1.1 | Open the platform address Karl gave you in Chrome on your phone. Sign in with your own account. | You see the Magnus workspace, not "pending tenant assignment". | Screenshot of the first screen. |
| 1.2 | Look for "Install app" or "Add to Home screen" in the Chrome menu. Install it. Open it from the home screen. | It opens full screen, like an app. | Did it install? Did it open full screen? |
| 1.3 | When asked, **allow notifications**. If never asked, look in the app for a notification setting. | Notifications allowed. | Were you asked? Where? |
| 1.4 | Note whether the app ever asks for your **location**. | It must **never** ask. | Yes or no. |
| 1.5 | Open Projects, open P2. Find the sidebar. | The sidebar reads: Dashboard · My Day · Pipeline · Projects · Design and Engineering · Procurement · Permits · Inventory · Manpower and Equipment · Safety · Operations and Maintenance · Documents · Messages · Finance · Human Resource · Payroll · Reports · Administration. As Person In Charge you may see fewer items. | Write down what you actually see. |

## Part 2 — A full site day offline (Person In Charge)

Do Parts 2.1 to 2.6 with **airplane mode on**. Switch it on before you start and leave it on until Part 3.

| Step | Do this | Expected | Record |
|---|---|---|---|
| 2.1 | With airplane mode on, open the app from the home screen. | It opens and shows P2 with yesterday's information cached. | Did it open? What did it show? Screenshot. |
| 2.2 | Open the **site emergency card** for the P2 site. | Nearest hospital, ambulance, evacuation point, first aiders, client contact are all readable with no signal. | Screenshot. Anything missing? |
| 2.3 | Start today's **site report** on P2. Fill weather, working hours, look-ahead. | The form opens offline. | Time you started. |
| 2.4 | Add the **toolbox meeting**: topic, photograph, attendees. Take the photograph with the app's own camera control. Then **try to pick a photograph from your gallery instead**. Add five named attendees from the crew list. | The camera opens inside the app. Picking from the gallery must **not** be possible. Attendees are chosen by name, not typed as a number. | Could you pick from the gallery? Did the photograph appear in your phone's gallery afterwards (check the Photos app)? It must not. |
| 2.5 | Add three **activities**: B0 lifelines 30 percent, B0 catwalk 20 percent, and one activity where you deliberately leave the block empty. | The two B0 activities save. The one with no block is **refused**. | Exact refusal text. Screenshot. |
| 2.6 | Try to **submit a second site report** for today on P2. | Refused: one report per project per workday. | Exact text. |
| 2.7 | Open Messages, open the P2 project thread. Post a text message `HT-A offline message 1`, then a message with a photograph `HT-A offline photo`, then a text `HT-A offline message 3`. | All three sit in a **visible queue** marked as waiting to send. | Screenshot of the queue. Can you see it without searching for it? |
| 2.8 | Open Safety. Try to **approve** anything, or open any approval waiting for you, while still offline. | Refused with a clear reason: no approvals offline. | Exact text. |
| 2.9 | Leave airplane mode on for **at least 30 minutes**. Lock the phone. Use other apps. Then come back to the app. | Everything you entered is still there. | Anything lost? |

## Part 3 — Reconnect (Person In Charge)

| Step | Do this | Expected | Record |
|---|---|---|---|
| 3.1 | Switch airplane mode off. Watch the queue. | Messages send in the order you wrote them: message 1, photo, message 3. The photo's **text** must not hold up message 3. | Order in which they appeared in the thread. Time to fully sync. |
| 3.2 | Open the site report you filed. Look for two times: when you **recorded** it and when it **synced**. | Both are shown. Recorded time is the offline time from step 2.3, not the sync time. | Both times as shown. |
| 3.3 | Check the P2 thread and the site report on the Safety Officer's phone. | One copy of each message, one site report. No duplicates. | Count. |
| 3.4 | Switch airplane mode on and off three times quickly while opening the report. | Nothing duplicates, nothing is lost. | Anything odd. |
| 3.5 | Sign out on the Person In Charge phone, then switch airplane mode on and open the app. | The cached data is **not** readable after sign-out. | What did you see? |

Sign back in before Part 4.

## Part 4 — Safety (both phones)

| Step | Who | Do this | Expected | Record |
|---|---|---|---|---|
| 4.1 | Anyone with a phone that is **not signed in** (borrow a crew member's phone, or use an incognito tab) | Scan the printed **Quick Response code** for the P2 site. Submit a near miss: one sentence and a photograph. | The form opens with **no login**, no app install, and never asks who you are. | Did it ask for a name, phone number or email at any point? It must not. Screenshot. |
| 4.2 | Same phone, same form | Submit again, this time choosing the **stop work** option. | Submitted. | Time submitted. |
| 4.3 | Safety Officer | Wait, phone locked. | A **push notification** arrives about the stop work, and it demands acknowledgement; it must not simply disappear. | Time received. Screenshot of the notification. Could you dismiss it without acknowledging? |
| 4.4 | Person In Charge | Same check on your phone. | Push arrives, acknowledgement demanded. | Time received. |
| 4.5 | Safety Officer | Open Safety, find the stop. Try to lift it on **Karl's** behalf or delegate it. Then lift it yourself with a reason. | Only the Safety Officer of record can lift it. No delegate option anywhere. Gate 29 shows **no alternate**. | Screenshots of the lift screen and of anything that offered delegation. |
| 4.6 | Safety Officer | Raise a **permit to work, working at height** on P2 B0 naming two crew. Set validity to tomorrow. | Refused or warned: the window must be same day. Gate 28 shows no alternate. | Text. |
| 4.7 | Safety Officer | Approve the permit for today. Then look for any setting that auto-approves permits. | Approved. No such setting exists. | Where did you look? |
| 4.8 | Person In Charge | Raise an **incident** on P2 from the block with a photograph. Try to delete it. | Cannot delete. Can only close, void or supersede. | Text. |
| 4.9 | Both | Open Safety and look at the near miss you submitted in 4.1. | The near miss is there. **Nowhere** does it show who submitted it, and there is no ranking or count of who reports the most. | What you see. |

## Part 5 — Day 2 and the things the platform should do by itself (Person In Charge)

Do this the next morning, or later the same day if Karl allows a second report date.

| Step | Do this | Expected | Record |
|---|---|---|---|
| 5.1 | Start the next site report. | It opens **pre-populated** from yesterday: incomplete activities and look-ahead carried forward. | Was it? What was carried? |
| 5.2 | Toolbox meeting again, six attendees. Add one name **twice**. | The duplicate is refused or collapsed. | Text. |
| 5.3 | Open block B0 on P2. Look for its percent complete. | It shows a number you never typed, equal to the sum of your activities. Look for **any field where a person can type a percent complete**. There must be none. | The number. Any typed-percent field found. |
| 5.4 | Open My Day. | Today's site report task is gone because you filed the report; you did not have to tick it. | What My Day shows. |
| 5.5 | Watch for anything that **happened by itself**: a task appearing that nobody created, a reminder, an escalation, a status that changed while you watched. | Nothing happens by itself in this version. | List every one, with a screenshot. |

## Part 6 — Usability (both, ten minutes)

Answer in writing:

1. Which screen would you open first in the morning on site? How many taps to reach it?
2. Can you fill a toolbox meeting with one hand while holding a phone in sunlight? What was hardest?
3. Which words on screen did you not understand? Any abbreviations? Write them down exactly.
4. What did you do today on site that the app gave you no place to record?
5. If Magnus switched to this app on Monday, what would stop you using it?

## Report — send to Karl within two days

Word or Google document, named `HT-A field report — [your names] — [date]`.

1. **Testers, phones, Android versions, signal condition** (one line each).
2. **Step table:** every step number above, result (**pass** / **fail** / **could not find** / **not tested**), what happened in your words, screenshot numbers.
3. **Offline timings:** the times from steps 2.3, 3.1, 3.2 side by side.
4. **Push notification timings:** steps 4.2, 4.3, 4.4.
5. **Things that happened by themselves** (step 5.5).
6. **Things you could see that a Person In Charge or Safety Officer should not see** (any cost, salary, other people's pay, other projects' money).
7. **Usability answers** (Part 6).
8. **Records you created**, listed by name.
9. **Your top three problems**, in order, one sentence each.

Attach all screenshots, numbered.
