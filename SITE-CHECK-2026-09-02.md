# Published site check — 2 September 2026

**Site:** https://magnus-solar-workspace-platform-446354.onhercules.app/
**Checked from outside, before sign-in.** What could be verified: the served HTML, the progressive web application manifest, the service worker, the client bundle, and every route it declares. What could not: anything behind sign-in, the Convex functions, the wrapper, the audit chain, the exempt list. Those need the code.

---

## 1. Status

**Up and serving.** HTTP 200, the manifest is a real manifest, the service worker is a real worker, the client connects to one Convex deployment (`elegant-cormorant-29`). No second deployment is referenced — the other Convex hostname in the bundle is Convex's own library example text, not a configuration.

**Built so far, from the routes the bundle declares:** pipeline · projects · design · procurement · permits · inventory · manpower · safety · documents · messages · finance · payroll · reports · admin · my-day · auth/callback. Most are placeholders; Pipeline is the only module reported complete, Project and Contract is in progress.

---

## 2. Issues, in order of consequence

### 2.1 Sign-in is Hercules Auth, not Google Workspace — check this first

The bundle wires `HerculesAuthProviderContext` into `ConvexProviderWithAuth` and points at `https://01m1fwvwx09tmpmkraqwcm2wz0.hercules-auth.com`. The specification requires each tenant to configure its own identity provider, the Magnus tenant's being Google Workspace, with the platform holding no password of any kind and a disabled Workspace account ending platform access at the same moment.

**Two things to establish in Hercules → Users & Access before anyone signs in:**
1. Is Google the sign-in method, restricted to the Magnus Workspace domain — and is email-and-password sign-up **off**? If a password path exists, the platform is storing credentials, which the specification forbids outright.
2. Does disabling a Workspace account end the Hercules Auth session? If Hercules Auth caches identity independently, the leaver control the specification relies on does not hold.

If Hercules Auth cannot be made Google-only and domain-restricted, this is the single most important prompt to send, because every later module inherits it.

### 2.2 The application does not open offline — the field path is not met

The service worker deliberately never caches the application shell, only an `offline.html` page and the icons. A navigation with no signal falls back to `offline.html`. **A Person In Charge on a rooftop with no signal cannot open the application at all**, let alone file a report — the exact failure the specification says sends people back to Messenger permanently.

Hercules' comment explains why: the shell embeds hashed asset names that change on every publish, so a cached shell would point at dead chunks. That is true, and the standard answer is a build-time precache list (a Workbox or `vite-plugin-pwa` generated manifest) so each publish caches its own shell and chunks. **The IndexedDB offline queue required by section 9 cannot be verified from outside; nothing in the bundle is conclusive either way.** Raise both together when the site-report screen is built — before, not after, the field test.

### 2.3 Manifest `start_url` points at a route that does not exist

`site.webmanifest` sets `start_url: "/today"` and a shortcut to `/today`, but no `/today` route is declared in the bundle. An installed app icon would open a non-existent page. Either the Today landing screen (the Person In Charge's landing page under section 8.2) has not been built yet, or the route is named differently. Low effort, high visibility.

### 2.4 Abbreviations in user-facing text

The manifest description reads *"Solar EPC operations management platform"* and a shortcut reads *"active PTWs"*. Both violate the no-abbreviation rule, and both appear on the home screen of every installed phone. Ampersands in the sidebar labels are already queued for correction.

### 2.5 Not yet visible, expected later

- No no-login near-miss or stop-work route exists yet (the per-site Quick Response form). The Safety module is not built; check for it then.
- No `/operations-and-maintenance`, `/human-resource` or `/administration` route yet — placeholders may be under other names; the sidebar shows them.
- Push-notification handling exists in the service worker. Fine, but confirm nothing schedules a push server-side.

---

## 3. Recommendations

| # | Do | Why |
|---|---|---|
| 1 | **Connect the Hercules app to a GitHub repository now** | Everything that matters in this build — the wrapper, the exempt list, the audit chain, the scheduler ban — is invisible from the browser. A repository lets it be read, tested and, if needed, fixed directly |
| 2 | **Settle sign-in before the first real user** — Google-only, domain-restricted, no password path | Identity is the one foundation choice the specification says forces a rebuild if wrong |
| 3 | **Queue the offline-shell fix alongside the site report screen** | Fixing it later means re-testing the field path |
| 4 | **Treat the current URL as the development preview, not production** | It is served from a Convex dev deployment under Hercules' own domain. Production needs a custom domain and, in Convex, a production deployment — and the backup-and-restore test the specification requires before go-live |
| 5 | **Open the Convex dashboard and count the seed rows** | 30 gate rows, 6 hard block rows, 5 system constants, 2 tenants. This is the one check that does not need code access and it verifies the foundation was seeded as specified |

---

## 4. How to start it

There is no "start" button — the first sign-in is the start, and the order matters because the specification says a person with no role has no access at all.

**Before signing in**

1. In Hercules → Users & Access, confirm the sign-in method per 2.1. Do not proceed on email-and-password.
2. In the Convex dashboard (Hercules → the app's backend), open the `tenants`, `gates`, `hard_blocks` and `system_constants` tables and confirm the counts above. If `tenants` has one row, the invented second test tenant is missing and should be seeded before anything else — it is the cheapest multi-tenancy test that exists.

**First sign-in — Karl**

3. Sign in with the Magnus Workspace account. The identity-link path creates or links the person record. Confirm Karl appears as the **second console holder** — the specification names the Chief Executive Officer in that seat.
4. In Administration, **name the primary console holder** — open item 3. Until there are two, the platform is one unreachable person away from being unconfigurable.

**The next five people, in this order**

5. Human Resource — creates person records for everyone else.
6. Department heads — assign roles under gate 24; nobody appears in the platform until this is done.
7. The Procurement Head, the Head of Finance and the Safety Officer of record — they are primaries on gates that fire early.
8. Persons In Charge last, and only after the site-report screen exists and has been field-tested; there is nothing for them to do before that.

**Data — what to load now and what to wait for**

9. Load now: parties (clients, suppliers, subcontractors, with insurance exclusions as a field), accounts, sites, contacts, and the five system constants with their effective date. These are the objects Pipeline needs and the only module that is complete.
10. **Do not load live projects yet.** Project and Contract is not finished; a project loaded before `site_id`, `warranty_months` and the risk-term rows exist is a migration later. Wait for the module, then load with signed contracts attached — hard block 6 will refuse them otherwise, which is correct.

**Roles today, working through the Hercules preview** — every person using the preview is working on a development deployment. Anything entered is real data on a database that may be reset when Hercules republishes or when the production deployment is created. Enter configuration and master data; do not enter operational records until the deployment is production.
