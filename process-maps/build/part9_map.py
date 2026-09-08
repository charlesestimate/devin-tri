from swimlane import Map
m=Map("Part 9 — Govern",
      "Level-1 cross-functional map · as specified · configuration, authority, documents and proof · gates 22, 24, 31, 32, 33 · 8 September 2026",
      [("console","Console Holders"),("exec","Executive"),("dept","Department Heads"),("doc","Document Control"),("mcp","Model Context Protocol"),("platform","The Platform")])
s=m.step
# --- stand the console up ---
s("9.1","console","First console holder is created at sign-up",rec="console_holders",col=0,dev="the bootstrap writes holderRank second for the first holder; the live first row says second and the live second row says nothing at all")
s("9.2","console","Add the second console holder",rec="console_holders",col=1,dev="addConsoleHolder never checks that the caller is a console holder. While fewer than two exist, any signed-in person can add themselves")
s("9.3","platform","Thirty gate rows are seeded",kind="auto",rec="gates",col=2,dev="the seeder skips a gate that already exists, so a wrong label is permanent — see Part 5")
# --- configure ---
s("9.4","exec","Change a gate's approver and window",rec="gates",gate=("31","COO","2nd console holder",None),col=3,dev="updateGateConfig takes no approval reference at all. It can rewrite the approver on gate 31 itself — the guard can move its own guard")
s("9.5","platform","All five govern gates have no approver",kind="auto",rec="gates 22, 24, 31, 32, 33",col=4,dev="live: primaryRoleName and primaryPersonId are both empty on every one of the five. The roles they name all exist and are marked approver")
s("9.6","exec","Change a system constant",rec="system_constants",state="new version, old one closed",gate=("22","COO",None,None),col=5,dev="the approval reference is an optional argument, stored unverified. Nine constant rows live, four with a change history, and not one carries a gate reference")
s("9.7","mcp","Change the same constant by tool call",rec="system_constants",col=6,dev="update_system_constant patches the number in place instead of closing the version and opening a new one. Two writers, two different meanings of change")
s("9.8","platform","The constant timeline",kind="auto",rec="system_constants",col=7,dev="live: markup_major_equipment has a version that begins 1 January 2030 and ends 7 September 2026. From 2030 the dated lookup for that key throws instead of returning a number")
# --- grant authority ---
s("9.9","dept","Assign a role to a person",rec="person_roles + approval_requests",state="pending",gate=("24","Director","COO",None),col=0,dev="the request is raised and the role is inserted live in the same transaction. Nothing anywhere treats a pending gate as not yet effective, and a refusal never revokes it")
s("9.10","platform","The screen path refuses today",kind="auto",rec="foundation/identity.ts",col=1,dev="assignRole throws when gate 24 has no primary approver, and it has none. Role assignment through the Administration screen cannot succeed until someone configures the gate")
s("9.11","mcp","Assign a role by tool call",rec="person_roles",col=2,dev="create_person_role raises no gate, checks no duplicate and checks no console holder. Fifty-five of the fifty-six role grants in the company arrived this way or by direct assignment")
s("9.12","console","Direct assignment, gate bypassed",rec="person_roles",col=3,dev="the honest path: console holders only, and the audit entry records bypassedGate 24 in as many words. This is the one place the bypass is written down")
s("9.13","exec","Change what a role may do",rec="permissions",gate=("32","CEO","COO",None),col=4,dev="the comment above the mutation says requires gate 32 approval — but for now records it directly. Gate 32 is a note in a comment")
s("9.14","platform","Permissions paint the sidebar",kind="auto",rec="permissions",col=5,dev="one consumer in the whole product: the query behind the navigation menu. No mutation anywhere asks whether the caller holds a permission before writing")
# --- documents ---
s("9.15","doc","Register a document and classify it",rec="documents",state="active",gate=("33","Document Controller",None,None),col=0,dev="the class is set at creation and there is no reclassification path anywhere — the gate is named for an act the platform cannot perform")
s("9.16","doc","Publish a revision in force",rec="document_revisions",state="draft → in_force",col=1,dev="supersedes cleanly and moves the pointer — good code, no gate, no approver check, and the effective date is a free argument, so a revision can be made to have been in force before it existed")
s("9.17","mcp","Set a revision in force by tool call",rec="document_revisions",col=2,dev="update_document_revision takes status as free text. It skips the unclassified refusal and the supersede step; two revisions in force then break the screen path for that document permanently")
s("9.18","doc","Put a document under legal hold",rec="documents",state="legalHold",col=3,dev="the strongest control in the module — blocks revisions, voiding and retention — is a boolean any signed-in person can set and any signed-in person can clear, with no reason and no gate")
# --- prove it ---
s("9.19","platform","Every write appends to the audit chain",kind="auto",rec="audit_entries",col=4,dev="hash-linked, sequence-numbered, and there is a working verifier on the Administration screen. This is the second thing in the platform that is completely right")
s("9.20","exec","Erase a person cryptographically",rec="erasure_records",state="key destroyed",col=5,dev="permanent and irreversible, it makes that person's audit entries unreadable for ever, and it requires a reason string that is not blank. No gate, no role check, no second signature, no console holder")
s("9.21","exec","Export the tenant and attest it",rec="export_records",col=6,dev="human-initiated and human-attested, exactly as the principles ask. Ninety-eight names for one hundred and sixteen tables, three of them phantom, and fourteen fall back to a read that is not filtered by tenant")
for a,b in [("9.1","9.2"),("9.2","9.3"),("9.3","9.4"),("9.4","9.5"),("9.5","9.6"),("9.6","9.7"),("9.7","9.8"),
            ("9.9","9.10"),("9.10","9.11"),("9.11","9.12"),("9.12","9.13"),("9.13","9.14"),
            ("9.15","9.16"),("9.16","9.17"),("9.17","9.18"),("9.18","9.19"),("9.19","9.20"),("9.20","9.21")]: m.edge(a,b)
m.edge("9.4","9.9","a reconfigured gate changes who may grant authority",kind="return")
m.edge("9.12","9.2","a console holder can make another console holder",kind="return")
m.banner="Fifty-six role grants are live and exactly one carries a gate 24 approval — raised and approved by the same person · all five governing gates have no approver configured, so the screen path for role assignment refuses outright · cryptographic erasure is permanent, ungated and needs only a non-blank reason · the audit chain is correct, and the compliance export reads fourteen tables without a tenant filter"
info=m.render("part9.svg"); print(info)
import re
svg=open("part9.svg").read()
open("part9.min.svg","w").write(re.sub(r'>\n\s*<','><',svg))
w,h=re.search(r'width="(\d+)" height="(\d+)"',svg).groups()
open("part9.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:A3 landscape;margin:5mm}} html,body{{margin:0;background:#fff}} svg{{width:{w}px;height:{h}px;display:block}}</style></head><body>'+svg+'</body></html>')
print("canvas",w,"x",h)
