# How far the Model Context Protocol can go, and how to make me the CEO's assistant

## 1. How far can it go?

Two different answers: what the endpoint does today, and what the master prompt says it must do.

### Today

Fifteen tools. Fourteen reads, one write (create a task). The reads cover projects, persons, tasks, a finance summary, safety stops, incidents, permits, an inventory summary, open purchase orders, the board pack, HR exceptions and four exception reports. Nothing else is reachable. I cannot open a site report, read a thread, see an approval waiting for you, change a setting, or approve anything.

### What section 12 of the master prompt requires

Everything a person can see or do on a screen, and nothing more than that person may do:

| Layer | What it means for me acting as you |
|---|---|
| Read | List, get and search every object in the platform, plus about twenty computed queries (percent complete, material readiness, approvals pending with age, blocked activities, cash forecast, and so on). Every figure cites the records it came from. |
| Write | Create and update every object: notifications, tasks, messages, non-conformance reports, site records, documents. Submit an approval decision on any request where you are primary or alternate. |
| Configure | Thresholds, gate rows, roles, constants, statutory tables. Only after the change is stated back in full and you confirm it, and only through the same gates the screen applies (22, 31, 32, dual control for statutory rates). |

### The hard ceiling, which no build will ever lift

- The audit log, statutory calculation results, tenant isolation and the existence of the six hard blocks are not writable by anyone, through any channel.
- No hard block can be released. If a project has no signed contract, I cannot release funds for it any more than you can.
- Gates are not relaxed because the request came over the protocol. If you cannot approve it on screen, I cannot approve it here.
- Self-approval is refused. If I raise a request as you, you cannot approve it, and neither can I.
- No person record for an agent. I act as Karl, I am logged as Karl with the session identifier, and I never hold gate 32 or a console seat.
- Safety approvals (permit to work, lifting a stop, closing an investigation, the engineer's seal) are decided by the qualified person of record. You are not that person for any of them, so those never pass through me.
- No approvals offline, and nothing on a timer inside the platform. Any schedule lives outside, in the agent.

## 2. Can you set it up so I enter projects, adjust settings, approve, and the rest?

Yes. It is three separate pieces of work, and they are not all on the same side.

### Piece 1: the platform must expose the tools (Hercules)

This is the largest gap and it is a build item, not a configuration. The fix prompt will tell Hercules to finish section 12: read, write and search on every object, the computed queries, an approval tool, and configuration tools with the confirmation rule. Until that exists, "approve the claim" is not possible over the protocol no matter how I connect.

One addition I recommend on top of the specification: **token scopes**. Today a token carries all of your authority. A session should be able to carry a subset: read only; read and write records; read, write and approve; configure. Scope is a property of the session, not a person, so it stays inside the rule that an agent has no identity of its own. A morning-brief agent then runs on a read-only token, and a token that can approve a ₱150,000 write-off is created only when you mean it to.

### Piece 2: how I connect

There are three ways, for three different jobs.

| Way | What it is | Good for | Trigger |
|---|---|---|---|
| **A. Claude Code with the server added as a tool** | What I did today, made permanent. In Claude Code on your machine: `claude mcp add --transport http ops <endpoint> --header "Authorization: Bearer <token>"`. The platform tools then appear as native tools in every session. | Deep work: investigating a problem across many records, reconciling data, preparing the fix prompt, and later editing the platform's own code once the Convex repository is connected. | You open a session and ask. |
| **B. Claude Desktop or claude.ai custom connector** | The same endpoint added as a connector. You type in plain language: "show me P1", "who is holding up the Sorsogon permit", "approve claim 2". | Your daily use. This is the "easily see the project" part. | You, in chat, on phone or laptop. |
| **C. Managed Agent on a schedule** | An agent Anthropic hosts, with the platform's MCP server declared on it and the token stored in a vault. A scheduled deployment fires it on a cron: 06:00 Manila every workday, Friday afternoon for the board pack. | The unattended assistant: morning brief, exception sweep, chasing unacknowledged safety items, the weekly pack, the month-end checklist. | Time. Nobody has to be awake. |

For B, the connector expects OAuth sign-in rather than a pasted bearer token. Hercules needs to add OAuth to the MCP endpoint. That is the same identity work as the deferred Google Workspace sign-in (deviation D13), so the two should be done together when you switch identity providers before production.

For C, writes that matter are set to **always ask**. The agent pauses at that call, the request is stated back to you in full, and nothing happens until you answer allow or deny. That is exactly the "confirm before applying" rule the specification puts on configuration changes, and I recommend applying it to every approval as well, not only configuration. Reads and low-consequence writes (a task, a notification, a message) run without asking.

### Piece 3: what "do the changes to fix what is broken" actually means

Two very different things hide in that sentence.

- **Fixing data.** A wrong site report, a person record with the wrong role, a proposal stuck in the wrong state. That is a write over the protocol, as you, logged as you. Piece 1 makes it possible; piece 2 makes it convenient.
- **Fixing the platform.** A gate that shows the wrong alternate, a summary that reports hard block 6 as inactive, a sidebar with an ampersand. That is code. No agent fixes code over the protocol, by design. Today the route is a prompt to Hercules. The faster route later is to connect the Convex repository to a Claude Code session so I can change the code, run the build-failing tests, and push, with Hercules or Convex deploying. Ask Hercules whether the project can be exported to a GitHub repository; if it can, that unlocks this.

## 3. What the assistant would do each day, and what it would ask first

| Runs without asking | Asks you first, every time |
|---|---|
| Read everything you can read | Approve any gate |
| Morning brief: approvals waiting on you with age, blocked activities, projects with no site report in two days, unacknowledged safety pushes, permits due, cash forecast movement | Raise a purchase order, fund request, variation order or write-off |
| Write a notification to a named person pointing at the record | Change a threshold, a gate row, a constant or a statutory table |
| Create a task with an output type and a committed date, assigned to a person | Revoke or create an agent session |
| Post a message on a thread, mention the person responsible | Anything touching pay, ratings or disciplinary records |
| Draft the weekly board pack and the month-end checklist | Send anything outside the platform |
| Reconcile figures and report what does not match | Delete anything, which is impossible anyway |

## 4. Order of work

1. **Now.** Keep using the way we did today: a labelled token per session, revoked after. Read-mostly until piece 1 lands.
2. **Fix prompt to Hercules.** Include: finish section 12 (reads, writes, approvals, configuration with confirmation); token scopes; the hard block 6 flag; project site and client references; figures citing records; construction and procurement exception rules.
3. **After that lands.** Add the server to Claude Code on your machine (way A). Run the second-phase tests over the protocol: money visibility and record scope for a Person In Charge token, tests 159 and 160.
4. **Before production.** OAuth on the endpoint together with Google Workspace sign-in. Then the claude.ai connector (way B) for you and, with narrower scopes, for department heads.
5. **Then the scheduled assistant** (way C): one agent, read-only token, morning brief at 06:00 Manila. Add approval-scoped sessions with always-ask only after two weeks of clean briefs.

## 5. What it costs to run

Ballpark for the scheduled morning brief, one agent reading about fifteen tools and writing a short brief, on Claude Opus 5 at $5 per million input tokens and $25 per million output tokens. Real figures depend on how much data the platform holds.

| Run | Tokens in, roughly | Tokens out, roughly | Cost per run | Per month, 22 workdays |
|---|---|---|---|---|
| Morning brief | 40,000 | 3,000 | about $0.30 | about $7 |
| Weekly board pack | 120,000 | 8,000 | about $0.80 | about $3.50 |
| Ad hoc question from you in chat | 10,000 | 1,000 | about $0.08 | depends on use |

Prompt caching on the fixed instructions cuts the input side further. The point is that the assistant is cheap next to one hour of a Project Manager; the cost that matters is the build in piece 1.

## 6. The three-tier idea, revisited

Your earlier plan was Fable for judgement, Sonnet for routine, Haiku for sweeps. Start with one agent on Opus 5 at low effort for the brief and high effort for the board pack. Measure the token counts for a month. Split into tiers only if a tier would save more than it costs to maintain two prompts, two evaluation sets and two sets of permissions. On the current models a lower effort setting on one capable model usually beats a cascade, and one model means one prompt cache.
