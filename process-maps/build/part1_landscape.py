# Part 1 — The Company on One Page. Level-0 cross-functional landscape, A3 landscape.
import html
W,H=1600,1130
GREEN="#1F6F3F"; GREEN_D="#154D2C"; ORANGE="#E4702A"; RED="#B3261E"; INK="#1F2A24"; MUTED="#5B6B62"
LANE_A="#FFFFFF"; LANE_B="#F3F6F4"; GRID="#D6DED9"; PLAT="#EAF1EC"; AMBER="#FFF4E5"; AMBER_B="#E4702A"

phases=[("P1","Win the Work",1.0),("P2","Design and Permit",0.95),("P3","Buy and Store",1.35),("P4","Build Safely",1.75),("P5","Commission and Hand Over",0.8),("P6","Operate and Maintain",0.8),("P7","Govern (continuous)",0.85)]
lanes=[("L1","Client and External Parties",0.72),("L2","Executive",0.9),("L3","Sales and Pipeline",0.68),("L4","Engineering",0.88),
       ("L5","Procurement and Inventory",1.55),("L6","Projects and Site",1.72),("L7","Safety",1.75),("L8","Finance and Payroll",1.55),
       ("L9","Human Resources",0.74),("L10","Administration and Permits",0.84),("L11","Operations and Maintenance",0.62),("L12","The Platform",0.78)]

# cells: (lane, phase) -> list of items. item = ("step", text) | ("gate", "G6", "Director", "alt COO", "—"|"3d") | ("hb","HB6","short") | ("note", text)
C={}
def add(l,p,*items): C.setdefault((l,p),[]).extend(items)

add("L1","P1",("step","Enquiry · site access · receives and accepts proposal · signs agreement"))
add("L1","P2",("step","Utility and local government issue permits · licensed engineer seals drawings"))
add("L1","P3",("step","Suppliers quote, deliver, and are paid"))
add("L1","P5",("step","Accepts turnover and handover"))
add("L1","P6",("step","Reports faults · warranty claims"))

add("L2","P1",("gate","G6","Director","COO","—"),("gate","G7","Director","—","—"),("gate","G9","CEO","—","—"),("gate","G10","Director","COO","—"))
add("L2","P2",("gate","G20","COO","Director","—"))
add("L2","P3",("gate","G5","Director","COO","2d"),("gate","G25a","Director","COO","—"))
add("L2","P4",("gate","G3","COO","—","—"),("gate","G8","Director","COO","3d"),("gate","G30","COO","—","—"))
add("L2","P5",("gate","G21","Director","COO","—"))
add("L2","P7",("gate","G22","COO","—","—"),("gate","G24","Director","COO","—"),("gate","G31","COO","—","—"),("gate","G32","CEO","COO","—"))

add("L3","P1",("step","Account → site → opportunity → site assessment → proposal → won"))

add("L4","P2",("step","Design package → deliverables → professional seal → approval → bill of materials"),("gate","G18","Design Engineer","—","—"))
add("L4","P4",("step","Issued-for-construction revisions"))
add("L4","P5",("step","As-built package"))

add("L5","P3",("step","Purchase order from the bill of materials → approved by amount → issued → received"),("gate","G4","Procurement Head","Director","2d"),
    ("step","Stock: locations · items · transfers · adjustments · physical counts · equipment"),("gate","G25b","PM","Director","—"),("gate","G26","Custodian","PM","—"),("gate","G27","Custodian","—","—"))
add("L5","P4",("step","Issue material and equipment to site"),("hb","HB5","quarantined material"))

add("L6","P1",("step","Project created on won · contract · risk terms · project parties"),("hb","HB6","signed contract to leave setup"))
add("L6","P4",("step","Mobilise → deploy workforce → nine construction blocks → daily site report"),("hb","HB1","insurance certificate"),("hb","HB4","prerequisite permit"),("hb","HB3","block B0 before electrical"),
    ("step","Non-conformance → closure"),("gate","G19","PM","Director","3d"))
add("L6","P5",("step","Commissioning → turnover date → handover"))

add("L7","P4",("step","Safety and health program"),("hb","HB2","program before construction"),
    ("step","Daily toolbox meeting — precondition of every site report"),
    ("step","Permit to work · safety stop"),("gate","G28","Safety Officer","—","—"),("gate","G29","Safety Officer","—","—"),
    ("step","Incident → corrective action → closure · near miss · inspections"))

add("L8","P3",("step","Fund request → release → liquidation"),("gate","G23","Head of Finance","COO","2d"),("hb","HB6","signed contract for orders and funds"))
add("L8","P4",("step","Milestones → progress claims → certification · write-offs by band · cash forecast"),("gate","G11","Head of Finance","COO","3d"),("gate","G1","Person In Charge","PM","3d"),("gate","G2","PM","Director","3d"),
    ("step","Payroll: period → statutory tables → runs → approve → disburse"),("note","● no payroll gate in specification (live: \"Gate 30\")"))
add("L8","P5",("step","Retention invoice"),("gate","G12","Head of Finance","COO","—"))
add("L8","P6",("step","Warranty claim"),("gate","G34","Head of Finance","COO","3d"))

add("L9","P4",("step","Requisition → candidate → offer → hire → regularisation · leave · performance"),("note","● no hiring gate in specification (live: \"Gate 24\")"))

add("L10","P2",("step","Permit types → project permits → requirements → submission · consultant"))
add("L10","P7",("step","Document register → revision → classification → in force → acknowledged"),("gate","G33","Document Controller","—","—"))

add("L11","P6",("step","Schedules → visits → readings → defects → sign-off"))

add("L12","P1",("step","Every write appended to the hash-chained audit trail · numbers assigned"))
add("L12","P3",("step","Order and fund request refused without a signed contract"))
add("L12","P4",("step","HB1–HB5 enforced at the step they guard · toolbox meeting before any site report"))
add("L12","P6",("note","⚠ RC-H nothing notifies anyone today"))
add("L12","P7",("step","Protocol reads, writes, decides under scoped tokens · Administration browser-only"))

# ---- layout ----
title_h=50; chev_h=30; banner_h=34; legend_h=64; pad=8
label_w=138; left=pad+label_w; right=W-pad
ptot=sum(w for *_,w in phases); col_x=[left]
for *_,w in phases: col_x.append(col_x[-1]+(right-left)*w/ptot)
tot=sum(w for _,_,w in lanes)
body_top=title_h+chev_h+6; body_h=H-body_top-banner_h-legend_h-pad*2
def esc(s): return html.escape(s)

def wrap(text,maxc):
    words=text.split(); lines=[]; cur=""
    for w in words:
        if len(cur)+len(w)+1>maxc and cur: lines.append(cur); cur=w
        else: cur=(cur+" "+w).strip()
    if cur: lines.append(cur)
    return lines

svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">']
svg.append(f'<rect width="{W}" height="{H}" fill="#fff"/>')
# title block
svg.append(f'<text x="{pad+4}" y="21" font-size="17" font-weight="bold" fill="{INK}">Magnus Renewable Tech Corp — The Company on One Page</text>')
svg.append(f'<text x="{pad+4}" y="39" font-size="10" fill="{MUTED}">Part 1 of 10 · Level-0 cross-functional process landscape · as specified · every gate (G) and hard block (HB) placed on the step it governs · 8 September 2026</text>')
svg.append(f'<text x="{right-4}" y="21" font-size="10" text-anchor="end" fill="{MUTED}">Magnus Workspace Platform · Process Maps and RACI</text>')
svg.append(f'<text x="{right-4}" y="39" font-size="10" text-anchor="end" fill="{MUTED}">Lanes = departments the platform defines · Columns = the order value moves</text>')
# chevrons
cy=title_h; 
for i,(pid,pname,_w) in enumerate(phases):
    x0=col_x[i]; x1=col_x[i+1]; col_w=x1-x0; n=12
    pts=f"{x0},{cy} {x1-n},{cy} {x1},{cy+chev_h/2} {x1-n},{cy+chev_h} {x0},{cy+chev_h} {x0+n if i>0 else x0},{cy+chev_h/2}"
    fill=GREEN if pid!="P7" else GREEN_D
    svg.append(f'<polygon points="{pts}" fill="{fill}"/>')
    pl=wrap(pname,14) if len(pname)>18 else [pname]
    for k,l in enumerate(pl):
        svg.append(f'<text x="{x0+col_w/2+4}" y="{cy+chev_h/2+4-(len(pl)-1)*5.5+k*11}" font-size="{11.5 if len(pl)==1 else 10}" font-weight="bold" text-anchor="middle" fill="#fff">{esc(l)}</text>')
# lanes
y=body_top
lane_y={}
for i,(lid,lname,wt) in enumerate(lanes):
    h=body_h*wt/tot; lane_y[lid]=(y,h)
    fill=PLAT if lid=="L12" else (LANE_A if i%2==0 else LANE_B)
    svg.append(f'<rect x="{pad}" y="{y}" width="{right-pad}" height="{h}" fill="{fill}" stroke="{GRID}"/>')
    svg.append(f'<rect x="{pad}" y="{y}" width="{label_w}" height="{h}" fill="{GREEN_D if lid!="L12" else "#3C5A48"}"/>')
    ls=wrap(lname,16)
    for k,l in enumerate(ls):
        svg.append(f'<text x="{pad+label_w/2}" y="{y+h/2-(len(ls)-1)*7+k*14+4}" font-size="11.5" font-weight="bold" text-anchor="middle" fill="#fff">{esc(l)}</text>')
    y+=h
for i in range(1,len(phases)):
    x=col_x[i]; svg.append(f'<line x1="{x}" y1="{body_top}" x2="{x}" y2="{y}" stroke="{GRID}" stroke-dasharray="3,3"/>')

# cell contents
def draw_cell(lid,pid,items):
    ly,lh=lane_y[lid]; ci=[p[0] for p in phases].index(pid); x0=col_x[ci]+6; cw=col_x[ci+1]-col_x[ci]-12
    cy=ly+5; gx=x0  # gx = running x for flowing gate badges
    def flush_gates():
        nonlocal cy,gx
        if gx>x0: cy+=17; gx=x0
    for it in items:
        kind=it[0]
        if kind=="step":
            flush_gates()
            lines=wrap(it[1],int(cw/5.3)); bh=len(lines)*10.5+7
            svg.append(f'<rect x="{x0}" y="{cy}" width="{cw}" height="{bh}" rx="5" fill="#fff" stroke="{GREEN}" stroke-width="1.2"/>')
            for k,l in enumerate(lines): svg.append(f'<text x="{x0+6}" y="{cy+12.5+k*10.5}" font-size="8.9" fill="{INK}">{esc(l)}</text>')
            cy+=bh+3
        elif kind=="gate":
            g,prim,alt,win=it[1],it[2],it[3],it[4]
            txt=f"{g} {prim}"+(f"·{alt}" if alt!="—" else "")+(f"·{win}" if win!="—" else "")
            tw=5.1*len(txt)+11
            if gx+tw>x0+cw and gx>x0: cy+=17; gx=x0
            svg.append(f'<rect x="{gx}" y="{cy}" width="{tw}" height="14" rx="7" fill="{GREEN}"/>')
            svg.append(f'<text x="{gx+6}" y="{cy+10.2}" font-size="8" font-weight="bold" fill="#fff">{esc(txt)}</text>')
            gx+=tw+4
        elif kind=="hb":
            flush_gates()
            lines=wrap(f"{it[1]} — {it[2]}",int(cw/5.0)); bh=len(lines)*10+6
            svg.append(f'<rect x="{x0}" y="{cy}" width="{cw}" height="{bh}" rx="3" fill="#FDECEA" stroke="{RED}" stroke-width="1.4"/>')
            svg.append(f'<polygon points="{x0+6},{cy+bh/2-5} {x0+11},{cy+bh/2-7} {x0+16},{cy+bh/2-5} {x0+16},{cy+bh/2+1} {x0+11},{cy+bh/2+3} {x0+6},{cy+bh/2+1}" fill="{RED}"/>')
            for k,l in enumerate(lines): svg.append(f'<text x="{x0+20}" y="{cy+11.5+k*10}" font-size="8.4" font-weight="bold" fill="{RED}">{esc(l)}</text>')
            cy+=bh+3
        elif kind=="note":
            flush_gates()
            lines=wrap(it[1],int(cw/4.9))
            for k,l in enumerate(lines): svg.append(f'<text x="{x0+2}" y="{cy+10+k*10.5}" font-size="8.4" font-style="italic" fill="{ORANGE}">{esc(l)}</text>')
            cy+=len(lines)*10.5+3
    flush_gates()
    return cy-ly
overflow=[]
for (lid,pid),items in C.items():
    used=draw_cell(lid,pid,items)
    if used>lane_y[lid][1]-2: overflow.append((lid,pid,round(used),round(lane_y[lid][1])))

# banner + legend
by=H-legend_h-banner_h-pad
svg.append(f'<rect x="{pad}" y="{by}" width="{right-pad}" height="{banner_h}" fill="{AMBER}" stroke="{AMBER_B}"/>')
svg.append(f'<text x="{pad+8}" y="{by+14}" font-size="9.2" fill="{INK}"><tspan font-weight="bold" fill="{ORANGE}">⚠ Where the live build deviates from this map today (each is detailed in Parts 2–9):</tspan>  RC-A one same-person check in sixteen approval controls · RC-B the write-off gate is chosen from a dropdown, not derived from the amount</text>')
svg.append(f'<text x="{pad+8}" y="{by+27}" font-size="9.2" fill="{INK}">Register: 25 of 30 gate labels and all 6 hard blocks on the live rows predate this specification, so no approver is ever named on screen · RC-H nothing notifies anyone · RC-N the live "Hard Block 6" blocks fund requests, not purchase orders</text>')
gy=H-legend_h-pad+2
svg.append(f'<text x="{pad+4}" y="{gy+12}" font-size="10" font-weight="bold" fill="{INK}">How to read</text>')
lx=pad+90
svg.append(f'<rect x="{lx}" y="{gy+2}" width="60" height="15" rx="5" fill="#fff" stroke="{GREEN}" stroke-width="1.2"/><text x="{lx+66}" y="{gy+13}" font-size="9.4" fill="{INK}">A step, or a chain of steps, performed by that lane. Arrows are implied left to right; each column hands to the next.</text>')
svg.append(f'<rect x="{lx}" y="{gy+22}" width="92" height="15" rx="7.5" fill="{GREEN}"/><text x="{lx+6}" y="{gy+33}" font-size="8" font-weight="bold" fill="#fff">G6 Director·COO·3d</text><text x="{lx+98}" y="{gy+33}" font-size="9.4" fill="{INK}">An approval gate: number · primary approver (Accountable) · alternate (Consulted) · working-day window where set. Thirty gates; 13–17 reserved.</text>')
svg.append(f'<rect x="{lx}" y="{gy+42}" width="60" height="15" rx="3" fill="#FDECEA" stroke="{RED}" stroke-width="1.4"/><text x="{lx+6}" y="{gy+53}" font-size="8.4" font-weight="bold" fill="{RED}">HB6</text><text x="{lx+66}" y="{gy+53}" font-size="9.4" fill="{INK}">A hard block: nobody can waive it — the step cannot happen until the precondition exists. Six, closed list.   <tspan fill="{ORANGE}" font-style="italic">● specification gap</tspan>   <tspan fill="{ORANGE}">⚠ live deviation</tspan>   <tspan fill="{MUTED}">Key: CEO Chief Executive Officer · COO Chief Operating Officer · PM Project Manager · Custodian Warehouse Custodian · 2d/3d working-day window</tspan></text>')
svg.append('</svg>')

page=f'''<!doctype html><html><head><meta charset="utf-8"><title>Part 1 — The Company on One Page</title>
<style>@page{{size:A3 landscape;margin:5mm}} html,body{{margin:0;padding:0;background:#fff}} svg{{width:404mm;height:auto;display:block}}</style></head><body>{"".join(svg)}</body></html>'''
open("part1.html","w").write(page)
open("part1_screen.html","w").write(page.replace("svg{{width:404mm;height:auto;display:block}}","svg{{width:1600px;height:1130px;display:block}}").replace("svg{width:404mm;height:auto;display:block}","svg{width:1600px;height:1130px;display:block}"))
print("overflow cells:",overflow if overflow else "none")
