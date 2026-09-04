# Fix — "Account not associated with a tenant" on every fresh deployment

Signing in to a new branch fails with **"Account not associated with a tenant"**.
It has happened on the original deployment and again on `bug-test/v2`, and each
time it has been worked around by editing the `users` table by hand. Fix it
properly.

---

## Why it happens

`maybeBootstrapConsoleHolder` in `convex/users.ts` has **three preconditions, and
every one of them fails by returning silently**:

| Line | Condition | On failure |
|---|---|---|
| ~47 | `BOOTSTRAP_CONSOLE_HOLDER_EMAILS` is set | `return` |
| ~55 | the signing-in email is on that allowlist | `return` |
| ~66 | `BOOTSTRAP_TENANT_SHORT_CODE` is set | `return` |
| ~72 | a tenant with that short code already exists | `return` — comment says *"seed not yet run — nothing to bootstrap"* |

On a fresh branch the deployment is new, so **no tenant exists yet** and the
environment variables may not have been carried over. The bootstrap returns
without doing anything, the `users` row is written with no `tenantId`, and the
next call hits `requireTenantContext` in `convex/lib/tenantEnforcement.ts` line 35
and throws.

**The person signing in is told none of this.** They get one sentence naming a
condition they cannot see and cannot act on. That is the real defect — not the
missing tenant, but that four different causes produce one useless message.

## What to change

### 1. Say which precondition failed

Replace every silent `return` with a recorded reason, and surface it. When
sign-in cannot complete, the screen must say which of these is true:

- *"No bootstrap allowlist is configured on this deployment."*
- *"This email is not on the bootstrap allowlist."*
- *"No bootstrap tenant short code is configured."*
- *"No tenant exists yet on this deployment."*
- *"This account is not linked to a person. An administrator must grant sign-in."*

Each one tells somebody what to do next. `Account not associated with a tenant`
tells nobody anything.

### 2. Create the tenant on first run

The bootstrap currently gives up when no tenant exists, on the assumption that a
seed has already run. On a fresh deployment nothing has run, which is exactly
when a bootstrap is needed.

When the signing-in email is on the allowlist **and there are no tenants at all**,
create one, using `BOOTSTRAP_TENANT_SHORT_CODE` for the short code and a sensible
default name. Then continue as it already does: create the person, link the
`users` row, make them a console holder, write the audit entry.

This is the whole fix. A first sign-in on an empty deployment should produce a
working console holder with no manual editing.

### 3. Make it work with no environment variables at all

Both variables have to be set by hand on every new branch, which is the step that
keeps being missed. Add a fallback: **if the deployment has no tenants and no
users, the first person to sign in becomes the console holder**, allowlist or
not.

That is safe. It can only fire once, on a database with nothing in it and nobody
in it — there is no one to escalate above. Every later sign-in follows the normal
path. Write an audit entry saying the bootstrap ran under the empty-deployment
rule, so it is visible afterwards.

### 4. Give an administrator a way to link an account

There is no screen for it. `grant_sign_in` exists over the Model Context
Protocol, so a console holder can only fix a colleague's access by asking
somebody with a protocol token.

Add it to Administration → Persons: select a person, enter their email address,
grant sign-in. This is how every one of your 45 staff gets access, and it
currently cannot be done through the interface at all.

## Prove it

1. On `bug-test/v2`, sign out and sign in. Report the exact text shown.
2. Say plainly whether a person can now sign in to a fresh deployment with no
   manual database editing and no environment variables set.
3. Show the audit entry the bootstrap wrote.
4. Give the tap-by-tap path for granting sign-in to a colleague from
   Administration.

Then publish to the branch.
