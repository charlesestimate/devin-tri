import json,re,glob,os,collections
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter

SP="/tmp/claude-0/-home-user-devin-tri/b7b98c67-52eb-53f7-b3a1-2f2eb30499cf/scratchpad"
MD="/home/user/devin-tri/process-maps"
J=lambda n: json.load(open(os.path.join(SP,n)))

GREEN="1F6F3F"; DARK="154D2C"; INK="1F2A24"; MUT="5B6B62"; ORANGE="E4702A"; RED="B3261E"
HDR=PatternFill("solid",fgColor=DARK); SUB=PatternFill("solid",fgColor="EAF1EC")
AMB=PatternFill("solid",fgColor="FFF4E5"); ROSE=PatternFill("solid",fgColor="FDECEA")
WHITE=Font(color="FFFFFF",bold=True,size=10)
B=Font(bold=True,size=10); N=Font(size=10); SM=Font(size=9); MUTF=Font(size=9,color=MUT)
WRAP=Alignment(wrap_text=True,vertical="top"); TOP=Alignment(vertical="top")
CTR=Alignment(horizontal="center",vertical="center")
thin=Side(style="thin",color="D6DED9"); BOX=Border(left=thin,right=thin,top=thin,bottom=thin)

def strip_md(s):
    s=re.sub(r'\*\*(.+?)\*\*',r'\1',s); s=re.sub(r'`([^`]+)`',r'\1',s)
    s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'\1',s)
    return s.strip()

def md_tables(path):
    out=[];cur=[]
    for l in open(path).read().split("\n"):
        if l.startswith("|"): cur.append(l)
        elif cur: out.append(cur);cur=[]
    if cur: out.append(cur)
    res=[]
    for t in out:
        rows=[[c.strip() for c in r.strip().strip("|").split("|")] for r in t if not re.match(r'^\|[\s\-:|]+\|$',r)]
        res.append(rows)
    return res

def header(ws,cols,widths,row=1):
    for i,(c,w) in enumerate(zip(cols,widths),1):
        cell=ws.cell(row=row,column=i,value=c); cell.fill=HDR; cell.font=WHITE
        cell.alignment=Alignment(wrap_text=True,vertical="center"); cell.border=BOX
        ws.column_dimensions[get_column_letter(i)].width=w
    ws.row_dimensions[row].height=30
    ws.freeze_panes=ws.cell(row=row+1,column=1)

def put(ws,r,vals,font=None,fill=None,wrap=True):
    for i,v in enumerate(vals,1):
        c=ws.cell(row=r,column=i,value=v)
        c.font=font or N; c.alignment=WRAP if wrap else TOP; c.border=BOX
        if fill: c.fill=fill
    return r+1

wb=Workbook(); wb.remove(wb.active)
wbB=Workbook(); wbB.remove(wbB.active)
wbC=Workbook(); wbC.remove(wbC.active)

# ─────────────────────────────── 1. Read me
ws=wb.create_sheet("Read me")
ws.column_dimensions['A'].width=22; ws.column_dimensions['B'].width=118
ws['A1']="Magnus Workspace Platform"; ws['A1'].font=Font(bold=True,size=16,color=DARK)
ws['A2']="Part 10 of 10 — the consolidated register"; ws['A2'].font=Font(size=12,color=MUT)
r=4
lines=[
 ("What this is","Every process step, every RACI assignment, every gate, every hard block and every deviation from Parts 1 to 9, in one workbook. Parts 2 to 9 are the narrative; this is the register they were building towards."),
 ("Date","8 September 2026. The live columns are a reading of the platform on that date, not a specification."),
 ("Three registers","Throughout, the same three columns recur: what seed.ts specifies, what the live row says, and what the module that uses the number believes. Where they disagree the disagreement is the finding, not an error in this sheet."),
 ("How to read RACI","R = does the work. A = accountable, and where a gate exists this is the gate's primary approver. C = consulted before. I = informed after. Blank = not involved. 'R today' in the Part 9 rows means the live build lets anyone signed in do it."),
 ("Tabs","Gate register · Hard blocks · Process steps · Consolidated RACI · Deviations · Hand-offs · Roles live · People live"),
 ("Sources","convex/ source export of 8 September 2026, and the live platform read over the Model Context Protocol on the same day. Nothing here is inferred from memory."),
 ("Companion files","Parts 1 to 9 as Google Docs, A3 landscape PDFs and SVGs, in this same folder."),
]
for k,v in lines:
    ws.cell(row=r,column=1,value=k).font=B
    c=ws.cell(row=r,column=2,value=v); c.font=N; c.alignment=WRAP
    ws.row_dimensions[r].height=max(15,13*(len(v)//110+1)); r+=1
r+=1
ws.cell(row=r,column=1,value="The one number").font=Font(bold=True,size=11,color=ORANGE)
c=ws.cell(row=r,column=2,value="Thirty gates are specified. Five raise an approval request in code (6, 7, 18, 24, 34). Nothing outside convex/foundation/gates.ts ever calls the approval engine — not once, in any module. The live approval_requests table contains gates 6, 7, 24 and 34 and nothing else, which is exactly what the code predicts.")
c.font=Font(size=10,bold=True); c.alignment=WRAP; c.fill=AMB; ws.row_dimensions[r].height=45

# ─────────────────────────────── 2. Gate register
seed=J("seed_gates.json"); live=J("gates_live.json"); claims=J("gate_claims.json")
livemap={str(g["gateId"]):g for g in live}
RAISES={"6","7","18","24","34"}
ws=wb.create_sheet("Gate register")
header(ws,["Gate","Specified label (seed.ts)","Live label","Specified primary","Specified alternate","Live primary","Live alternate","No alternate","Window (working days)","Modules that name this gate","In code","Agrees?"],
       [7,34,28,22,22,16,16,10,12,44,26,26])
r=2; agree=0
for g in sorted(seed,key=lambda x:(int(re.sub(r'\D','',x["gateId"])), x["gateId"])):
    gid=g["gateId"]; L=livemap.get(gid,{})
    mods=[m for m in claims.get(gid,[]) if not m.startswith("foundation/seed")]
    # finance derives gates 1-3 through gateIdForSeverity rather than a literal, so the
    # mechanical scan misses them. Verified by reading convex/finance/finance.ts.
    if gid in ("1","2","3") and "finance/finance.ts (computed)" not in mods:
        mods.append("finance/finance.ts (computed)")
    # gates with no gate reference anywhere, but where the action itself is implemented —
    # verified by reading the named mutation in each module.
    UNNAMED={"21":"Action exists (recordTurnoverDate), gate never named",
             "28":"Action exists (issuePermitToWork), gate never named",
             "29":"Action exists (clearSafetyStop), gate never named",
             "10":"Action exists (risk review), gate never named",
             "11":"Action exists (progress claim), gate never named"}
    if gid in RAISES: incode="Raises an approval request"
    elif any(not m.startswith("schema/") for m in mods): incode="Approval recorded without the engine"
    elif gid in UNNAMED: incode=UNNAMED[gid]
    else: incode="No code — no record of this act at all"
    same = (L.get("label","")==g["label"])
    if same: agree+=1
    fill=None if same else AMB
    r=put(ws,r,[gid,g["label"],L.get("label","(missing)"),g["primary"],g["alternate"] or "—",
                L.get("primaryRoleName") or "none set",L.get("alternateRoleName") or "none set",
                "yes" if g["noAlternate"] else "no", "—" if g["window"]=="undefined" else g["window"],
                ", ".join(mods) or "—", incode,
                "labels agree" if same else "labels differ"],fill=fill)
r+=1
put(ws,r,[f"{agree} of 30 live labels match the specification; {30-agree} differ. Five gates raise an approval request (6, 7, 18, 24, 34). Seventeen record an approval without the engine. Three have no record of the act at all. Nothing outside convex/foundation/gates.ts ever calls approveRequest, rejectRequest or checkGateAuthorisation — the scan returns zero callers."],font=Font(bold=True,color=ORANGE))

# ─────────────────────────────── 3. Hard blocks
ws=wb.create_sheet("Hard blocks")
header(ws,["Block","Specified label (seed.ts)","Specified blocked action","Released by","Live label","Live description","Agrees?"],
       [7,42,32,44,34,52,14])
shb={h["blockId"]:h for h in J("seed_hb.json")}
lhb={h["blockId"]:h for h in J("hb_live.json")}
r=2
for i in range(1,7):
    s=shb.get(i,{}); l=lhb.get(i,{})
    same=s.get("label","")==l.get("label","")
    r=put(ws,r,[i,s.get("label",""),s.get("blockedAction",""),s.get("releasedBy",""),
                l.get("label","(missing)"),l.get("description",""),"agrees" if same else "differs"],
          fill=None if same else AMB)
r+=1
put(ws,r,["All six live hard blocks carry a different label and a different meaning from the six the specification names. The specification's block 3 refers to a block B0 that does not exist in the construction spine."],font=Font(bold=True,color=ORANGE))

# ─────────────────────────────── steps + RACI + deviations + handoffs
PARTS=[("2","Win the Work"),("3","Design and Permit"),("4","Buy and Store"),("5","Build Safely"),
       ("6","Get Paid"),("7","People and Pay"),("8","Operate and Maintain"),("9","Govern")]
files={p:glob.glob(os.path.join(MD,f"PART-{p}-*.md"))[0] for p,_ in PARTS}
steps=[]; raci_rows=[]; devs=[]; hands=[]
role_alias={"Sales role":"Sales","COO":"Chief Operating Officer","CEO":"Chief Executive Officer",
 "HR Head":"Human Resource Head","Doc Controller":"Document Controller","O&M Lead":"Operations and Maintenance Lead",
 "PIC":"Person In Charge","Procurement Head":"Procurement Head","VP Sales":"Vice President for Sales",
 "Manager":"Line Manager","Everyone signed in":"Anyone signed in (live build)"}
for p,title in PARTS:
    ts=md_tables(files[p])
    for t in ts:
        h=t[0]
        if h[0]=="#" and "Lane" in h and "Action" in h:
            gi=h.index("Gate") if "Gate" in h else (h.index("Gate or block") if "Gate or block" in h else None)
            di=len(h)-1
            for row in t[1:]:
                if len(row)<len(h): continue
                steps.append({"part":p,"title":title,"step":strip_md(row[0]),"lane":strip_md(row[1]),
                    "action":strip_md(row[2]),"record":strip_md(row[3]),
                    "gate":strip_md(row[gi]) if gi is not None else "",
                    "dev":strip_md(row[di])})
        elif h[0]=="Step" and len(h)>3:
            roles=[role_alias.get(x,x) for x in h[1:]]
            for row in t[1:]:
                if len(row)<len(h): continue
                raci_rows.append({"part":p,"title":title,"label":strip_md(row[0]),
                    "cells":{roles[i]:strip_md(v) for i,v in enumerate(row[1:]) if strip_md(v)}})
        elif h[0]=="From → To":
            for row in t[1:]:
                if len(row)<4: continue
                hands.append([p,title]+[strip_md(x) for x in row[:4]])
        elif (h[0] in ("","#")) and ("Deviation" in h or "The map says" in h):
            sev = "Severity" in h
            for row in t[1:]:
                if len(row)<4: continue
                if sev: devs.append([p,title,strip_md(row[0]),strip_md(row[1])+" — "+strip_md(row[2]),"",strip_md(row[3])])
                else:   devs.append([p,title,strip_md(row[0]),strip_md(row[1]),strip_md(row[2]),strip_md(row[3])])

ws=wbB.create_sheet("Process steps")
header(ws,["Part","Process","Step","Lane","Action","Record → state","Gate or block"],[6,22,7,20,46,32,18])
r=2
for s in steps:
    r=put(ws,r,[s["part"],s["title"],s["step"],s["lane"],s["action"],s["record"],s["gate"] or "—"],
          fill=AMB if s["dev"] and s["dev"]!="—" else None)

# consolidated RACI
order=["Chief Executive Officer","Chief Operating Officer","Director","Vice President for Sales","Sales",
 "Project Manager","Person In Charge","Design Manager","Design Engineer","Permit Liaison","Document Controller",
 "Procurement Head","Procurement Officer","Warehouse Custodian","Safety Officer","Service Technician",
 "Operations and Maintenance Lead","Human Resource Head","Line Manager","Payroll Officer","Head of Finance",
 "Finance Officer","Console Holder","Employee","Anyone signed in (live build)",
 "Client","Candidate","Supplier","Authority","Department of Labor and Employment"]
seen=set()
for rr in raci_rows: seen|=set(rr["cells"])
cols=[c for c in order if c in seen]+[c for c in sorted(seen) if c not in order]
ws=wbC.create_sheet("Consolidated RACI")
header(ws,["Part","Step"]+cols,[6,42]+[11]*len(cols))
r=2
for rr in raci_rows:
    ws.cell(row=r,column=1,value=rr["part"]).font=N
    c=ws.cell(row=r,column=2,value=rr["label"]); c.font=N; c.alignment=TOP
    for i,cn in enumerate(cols,3):
        v=rr["cells"].get(cn,"")
        if not v: continue
        cell=ws.cell(row=r,column=i,value=v); cell.alignment=CTR
        cell.font=Font(size=9,bold=("R" in v or "A" in v))
        if v.startswith("R today"): cell.fill=ROSE
        elif "A" in v: cell.fill=SUB
    r+=1
ws.freeze_panes="C2"

ws=wbB.create_sheet("Deviations")
header(ws,["Part","Process","#","What is wrong","Step","Reference or severity"],[6,22,7,96,10,20])
r=2
for d in devs: r=put(ws,r,d)
r+=1
put(ws,r,[f"{len(devs)} numbered deviations across Parts 2 to 9."],font=Font(bold=True,color=ORANGE))

ws=wbB.create_sheet("Hand-offs")
header(ws,["Part","Process","From → To","At step","What crosses","What stalls it"],[6,22,32,14,42,62])
r=2
for h in hands: r=put(ws,r,h)

# ─────────────────────────────── roles + people (live)
roles=J("roles_now.json"); roles=roles if isinstance(roles,list) else roles.get("page",[])
prs=[]
txt=open(os.path.join(SP,"pr_all.json")).read(); dec=json.JSONDecoder(); i=0
while i<len(txt):
    while i<len(txt) and txt[i] in " \n\t": i+=1
    if i>=len(txt): break
    o,i=dec.raw_decode(txt,i); prs+= o if isinstance(o,list) else []
cnt=collections.Counter(p["roleId"] for p in prs if not p.get("revoked"))
rolemap={r["_id"]:r for r in roles}
ws=wb.create_sheet("Roles live")
header(ws,["Role label","Machine name","Department","Approver","Record scope","Money visibility","Active","People holding it"],
       [34,30,18,10,14,16,8,16])
r=2
for ro in sorted(roles,key=lambda x:(x.get("department") or "zz",x["label"])):
    r=put(ws,r,[ro["label"],ro["name"],ro.get("department") or "—","yes" if ro.get("isApprover") else "no",
                ro.get("recordScope"),ro.get("moneyVisibility"),"yes" if ro.get("active") else "no",cnt.get(ro["_id"],0)],
          fill=AMB if cnt.get(ro["_id"],0)==0 else None)
r+=1
put(ws,r,[f"{len(roles)} roles. {sum(1 for ro in roles if cnt.get(ro['_id'],0)==0)} are held by nobody."],font=Font(bold=True,color=ORANGE))

persons=J("persons_now.json"); persons=persons if isinstance(persons,list) else persons.get("page",[])
byperson=collections.defaultdict(list)
for p in prs:
    if not p.get("revoked"): byperson[p["personId"]].append(rolemap.get(p["roleId"],{}).get("label","(unknown role)"))
ws=wb.create_sheet("People live")
header(ws,["Name","Population","Employment basis","Home region","Status","Roles held","Gate 24 approval on any role"],
       [30,14,18,14,10,52,26])
r=2
gated={p["personId"] for p in prs if p.get("gateRequestId")}
for p in sorted(persons,key=lambda x:x.get("displayName","")):
    rl=byperson.get(p["_id"],[])
    r=put(ws,r,[p.get("displayName"),p.get("population") or "—",p.get("employmentBasis") or "—",
                p.get("homeRegion") or "—",p.get("status") or "—",", ".join(sorted(rl)) or "no role",
                "yes" if p["_id"] in gated else "no"],
          fill=AMB if not rl else None)
r+=1
put(ws,r,[f"{len(persons)} people. {sum(1 for p in persons if not byperson.get(p['_id']))} hold no role. "
          f"{len(prs)} role grants, {sum(1 for p in prs if p.get('gateRequestId'))} carrying a gate 24 approval."],
    font=Font(bold=True,color=ORANGE))

# Read me pointer on workbook B
wsB=wbB.create_sheet("Read me",0)
wsB.column_dimensions['A'].width=22; wsB.column_dimensions['B'].width=110
wsB['A1']="Part 10 of 10 — Consolidated RACI and process register"; wsB['A1'].font=Font(bold=True,size=14,color=DARK)
for i,(k,v) in enumerate([("What this is","Every process step and every RACI assignment from Parts 2 to 9, plus the numbered deviations and the hand-offs between lanes."),
  ("Companion","The gate register, the hard blocks and the live roles and people are in the companion workbook, Part 10 — Registers."),
  ("Reading RACI","R does the work. A is accountable, and where a gate exists this is the gate's primary approver. C is consulted before. I is informed after. Blank means not involved. 'R today' means the live build lets anyone signed in do it."),
  ("Deviation notes","The full note for each step is in the Deviations tab and in the Part 2 to 9 documents."),
  ("Date","8 September 2026.")],start=3):
    wsB.cell(row=i,column=1,value=k).font=B
    c=wsB.cell(row=i,column=2,value=v); c.font=N; c.alignment=WRAP
    wsB.row_dimensions[i].height=max(15,13*(len(v)//105+1))
outA="/home/user/devin-tri/process-maps/build/part10a.xlsx"; wb.save(outA)
outB="/home/user/devin-tri/process-maps/build/part10b.xlsx"; wbB.save(outB)
wsC=wbC.create_sheet("Read me",0)
wsC.column_dimensions['A'].width=22; wsC.column_dimensions['B'].width=110
wsC['A1']="Part 10 of 10 — Consolidated RACI"; wsC['A1'].font=Font(bold=True,size=14,color=DARK)
for i,(k,v) in enumerate([("What this is","Every RACI assignment from Parts 2 to 9 in one matrix: 172 steps against 30 roles."),
  ("Reading it","R does the work. A is accountable, and where a gate exists this is the gate's primary approver. C is consulted before. I is informed after. Blank means not involved."),
  ("R today","In the Part 9 rows, 'R today' means the live build lets anyone signed in do it, where the specification names a specific officer."),
  ("Companions","Part 10 — Registers holds the gate register, the hard blocks and the live roles and people. Part 10 — Process register holds the steps, the deviations and the hand-offs."),
  ("Date","8 September 2026.")],start=3):
    wsC.cell(row=i,column=1,value=k).font=B
    c=wsC.cell(row=i,column=2,value=v); c.font=N; c.alignment=WRAP
    wsC.row_dimensions[i].height=max(15,13*(len(v)//105+1))
outC="/home/user/devin-tri/process-maps/build/part10c.xlsx"; wbC.save(outC)
import base64
for f in (outA,outB,outC):
    b=base64.b64encode(open(f,'rb').read()).decode()
    open(f+'.b64','w').write(b)
    print(os.path.basename(f), os.path.getsize(f), "bytes ->", len(b), "b64 chars")
print("steps",len(steps),"raci",len(raci_rows),"devs",len(devs),"handoffs",len(hands),"roles",len(roles),"persons",len(persons),"raci cols",len(cols))
