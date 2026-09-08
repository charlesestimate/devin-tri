# Level-1 swimlane engine for Parts 2-9. Steps placed left->right in sequence, one box per step in its lane,
# orthogonal connectors between consecutive steps, gate badges and hard-block stops attached to steps.
import html
GREEN="#1F6F3F"; GREEN_D="#154D2C"; ORANGE="#E4702A"; RED="#B3261E"; INK="#1F2A24"; MUTED="#5B6B62"
LANE_A="#FFFFFF"; LANE_B="#F3F6F4"; GRID="#D6DED9"; PLAT="#EAF1EC"; AMBER="#FFF4E5"; ARROW="#3C5A48"
def esc(s): return html.escape(str(s))
def wrap(text,maxc):
    words=str(text).split(); lines=[]; cur=""
    for w in words:
        if len(cur)+len(w)+1>maxc and cur: lines.append(cur); cur=w
        else: cur=(cur+" "+w).strip()
    if cur: lines.append(cur)
    return lines
class Map:
    def __init__(self,title,subtitle,lanes,W=2200,H=1556,col_w=150,box_w=132):
        self.title=title; self.subtitle=subtitle; self.lanes=lanes  # list of (id,label)
        self.W=W; self.H=H; self.col_w=col_w; self.box_w=box_w
        self.steps=[]; self.edges=[]; self.notes=[]; self.banner=None; self.legend_extra=""
    def step(self,id,lane,label,rec=None,state=None,gate=None,hb=None,dev=None,kind="step",col=None):
        # gate=(num,primary,alt,window) ; hb=(id,text) ; dev="RC-A note" ; kind: step|decision|auto|external
        self.steps.append(dict(id=id,lane=lane,label=label,rec=rec,state=state,gate=gate,hb=hb,dev=dev,kind=kind,col=col)); return id
    def edge(self,a,b,label=None,kind="flow"): self.edges.append((a,b,label,kind))
    def render(self,path):
        W=self.W; pad=8; title_h=44; legend_h=52; banner_h=26 if self.banner else 0
        label_w=124; left=pad+label_w; right=W-pad
        # assign columns: sequential unless explicit
        col=0; cols={}
        for s in self.steps:
            if s["col"] is None: s["col"]=col; col+=1
            else: col=max(col,s["col"]+1)
        ncol=max(s["col"] for s in self.steps)+1
        col_w=min(self.col_w,(right-left-6)/ncol); box_w=min(self.box_w,col_w-10)
        nret=sum(1 for e in self.edges if e[3]=="return")
        body_top=title_h+6+(9*nret+10 if nret else 0)
        # lane heights: proportional to max stack in lane
        def parts(s):
            lab=wrap(s["label"],max(10,int(box_w/5.4)))
            rec=[]
            if s["rec"]:
                rt=s["rec"]+(" ["+s["state"]+"]" if s["state"] else "")
                rec=wrap(rt,max(12,int(box_w/4.4)))
            return lab,rec
        def stack_h(s):
            lab,rec=parts(s)
            h=9+len(lab)*11+(len(rec)*8.6+3 if rec else 0)
            if s["gate"]: h+=16
            if s["hb"]: h+=len(wrap(s["hb"][1],max(12,int(box_w/4.9))))*9.6+7
            if s["dev"]: h+=len(wrap("! "+s["dev"],max(12,int(box_w/4.6))))*9.4+3
            return h+12
        need={l[0]:max([stack_h(s) for s in self.steps if s["lane"]==l[0]] or [34])+10 for l in self.lanes}
        need={k:max(v,46) for k,v in need.items()}
        H=self.H=int(body_top+sum(need.values())+banner_h+legend_h+pad+6); scale=1.0
        svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">',f'<rect width="{W}" height="{H}" fill="#fff"/>']
        svg.append(f'<text x="{pad+4}" y="20" font-size="16" font-weight="bold" fill="{INK}">{esc(self.title)}</text>')
        svg.append(f'<text x="{pad+4}" y="36" font-size="9.6" fill="{MUTED}">{esc(self.subtitle)}</text>')
        svg.append(f'<text x="{right-4}" y="20" font-size="9.6" text-anchor="end" fill="{MUTED}">Magnus Workspace Platform · Process Maps and RACI</text>')
        # lanes
        y=body_top; lane_y={}
        for i,(lid,lname) in enumerate(self.lanes):
            h=need[lid]; lane_y[lid]=(y,h)
            fill=PLAT if lid=="platform" else (LANE_A if i%2==0 else LANE_B)
            svg.append(f'<rect x="{pad}" y="{y:.1f}" width="{right-pad}" height="{h:.1f}" fill="{fill}" stroke="{GRID}"/>')
            svg.append(f'<rect x="{pad}" y="{y:.1f}" width="{label_w}" height="{h:.1f}" fill="{GREEN_D if lid!="platform" else "#3C5A48"}"/>')
            ls=wrap(lname,15)
            for k,l in enumerate(ls): svg.append(f'<text x="{pad+label_w/2}" y="{y+h/2-(len(ls)-1)*6.5+k*13+4:.1f}" font-size="11" font-weight="bold" text-anchor="middle" fill="#fff">{esc(l)}</text>')
            y+=h
        # steps
        pos={}
        for s in self.steps:
            ly,lh=lane_y[s["lane"]]; x=left+6+s["col"]*col_w+(col_w-box_w)/2
            lab,rec=parts(s); bh=9+len(lab)*11+(len(rec)*8.6+3 if rec else 0)
            # vertical centre the whole stack
            sh=stack_h(s)-10; y0=ly+max(4,(lh-sh)/2)
            kind=s["kind"]
            if kind=="decision":
                cx,cy=x+box_w/2,y0+bh/2; hw,hh=box_w/2+4,bh/2+7
                svg.append(f'<polygon points="{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}" fill="#fff" stroke="{ORANGE}" stroke-width="1.4"/>')
            else:
                stroke=GREEN if kind=="step" else (MUTED if kind=="auto" else "#8A6D3B")
                dash=' stroke-dasharray="4,3"' if kind=="external" else ''
                fillc="#fff" if kind!="auto" else "#F6F8F6"
                svg.append(f'<rect x="{x:.1f}" y="{y0:.1f}" width="{box_w}" height="{bh:.1f}" rx="5" fill="{fillc}" stroke="{stroke}" stroke-width="1.3"{dash}/>')
            for k,l in enumerate(lab): svg.append(f'<text x="{x+box_w/2:.1f}" y="{y0+12.5+k*11:.1f}" font-size="9" text-anchor="middle" fill="{INK}">{esc(l)}</text>')
            ry=y0+12.5+len(lab)*11
            for k,l in enumerate(rec): svg.append(f'<text x="{x+box_w/2:.1f}" y="{ry+k*8.6:.1f}" font-size="7.4" text-anchor="middle" fill="{MUTED}">{esc(l)}</text>')
            yy=y0+bh+3
            if s["gate"]:
                g,p,a,w=s["gate"]; txt=f"G{g} {p}"+(f"·{a}" if a else "")+(f"·{w}" if w else "")
                tw=min(box_w,4.9*len(txt)+10); gx=x+(box_w-tw)/2
                svg.append(f'<rect x="{gx:.1f}" y="{yy:.1f}" width="{tw:.1f}" height="13" rx="6.5" fill="{GREEN}"/>')
                svg.append(f'<text x="{x+box_w/2:.1f}" y="{yy+9.6:.1f}" font-size="7.6" font-weight="bold" text-anchor="middle" fill="#fff">{esc(txt)}</text>'); yy+=16
            if s["hb"]:
                hl=wrap(f"{s['hb'][0]} — {s['hb'][1]}",max(12,int(box_w/4.9))); hh=len(hl)*9.6+6
                svg.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{box_w}" height="{hh}" rx="3" fill="#FDECEA" stroke="{RED}" stroke-width="1.3"/>')
                for k,l in enumerate(hl): svg.append(f'<text x="{x+box_w/2:.1f}" y="{yy+10.6+k*9.6:.1f}" font-size="7.8" font-weight="bold" text-anchor="middle" fill="{RED}">{esc(l)}</text>')
                yy+=hh+3
            if s["dev"]:
                dl=wrap("⚠ "+s["dev"],max(12,int(box_w/4.6)))
                for k,l in enumerate(dl): svg.append(f'<text x="{x+box_w/2:.1f}" y="{yy+8.8+k*9.4:.1f}" font-size="7.6" font-style="italic" text-anchor="middle" fill="{ORANGE}">{esc(l)}</text>')
            pos[s["id"]]=(x,y0,box_w,bh,s["lane"])
        # edges (orthogonal): right-mid of a -> left-mid of b; if same column/backwards, route above
        for a,b,label,kind in self.edges:
            xa,ya,wa,ha,la=pos[a]; xb,yb,wb,hb_,lb=pos[b]
            x1,y1=xa+wa,ya+ha/2; x2,y2=xb,yb+hb_/2
            dash=' stroke-dasharray="4,3"' if kind=="return" else ''
            colr=ORANGE if kind=="return" else ARROW
            if x2>x1:
                midx=x1+(x2-x1)/2
                d=f'M{x1:.1f},{y1:.1f} L{midx:.1f},{y1:.1f} L{midx:.1f},{y2:.1f} L{x2-5:.1f},{y2:.1f}'
                svg.append(f'<path d="{d}" fill="none" stroke="{colr}" stroke-width="1.2"{dash}/>')
                svg.append(f'<polygon points="{x2-6:.1f},{y2-3.5:.1f} {x2:.1f},{y2:.1f} {x2-6:.1f},{y2+3.5:.1f}" fill="{colr}"/>')
                if label:
                    svg.append(f'<text x="{midx+3:.1f}" y="{(y1+y2)/2-3:.1f}" font-size="7.4" fill="{colr}">{esc(label)}</text>')
            else:  # backward / return: dedicated channel above every lane
                self._retn=getattr(self,"_retn",0)+1
                top=body_top-6-self._retn*9
                d=f'M{xa+wa/2:.1f},{ya:.1f} L{xa+wa/2:.1f},{top:.1f} L{xb+wb/2:.1f},{top:.1f} L{xb+wb/2:.1f},{yb-5:.1f}'
                svg.append(f'<path d="{d}" fill="none" stroke="{colr}" stroke-width="1.2"{dash}/>')
                svg.append(f'<polygon points="{xb+wb/2-3.5:.1f},{yb-6:.1f} {xb+wb/2:.1f},{yb:.1f} {xb+wb/2+3.5:.1f},{yb-6:.1f}" fill="{colr}"/>')
                if label: svg.append(f'<text x="{(xa+xb)/2+wa/2:.1f}" y="{top-3:.1f}" font-size="7.4" text-anchor="middle" fill="{colr}">{esc(label)}</text>')
        # banner
        by=H-legend_h-banner_h-pad
        if self.banner:
            svg.append(f'<rect x="{pad}" y="{by}" width="{right-pad}" height="{banner_h}" fill="{AMBER}" stroke="{ORANGE}"/>')
            svg.append(f'<text x="{pad+8}" y="{by+16}" font-size="9" fill="{INK}"><tspan font-weight="bold" fill="{ORANGE}">⚠ Live build deviates here today:</tspan> {esc(self.banner)}</text>')
        gy=H-legend_h-pad+2; lx=pad+84
        svg.append(f'<text x="{pad+4}" y="{gy+11}" font-size="9.6" font-weight="bold" fill="{INK}">How to read</text>')
        svg.append(f'<rect x="{lx}" y="{gy+1}" width="46" height="13" rx="5" fill="#fff" stroke="{GREEN}" stroke-width="1.3"/><text x="{lx+52}" y="{gy+11}" font-size="8.8" fill="{INK}">A step by a person, with the record and its new state beneath.</text>')
        svg.append(f'<polygon points="{lx+23},{gy+17} {lx+46},{gy+25} {lx+23},{gy+33} {lx},{gy+25}" fill="#fff" stroke="{ORANGE}" stroke-width="1.3"/><text x="{lx+52}" y="{gy+28}" font-size="8.8" fill="{INK}">A decision the process branches on.   </text>')
        svg.append(f'<rect x="{lx+330}" y="{gy+1}" width="46" height="13" rx="5" fill="#F6F8F6" stroke="{MUTED}" stroke-width="1.3"/><text x="{lx+382}" y="{gy+11}" font-size="8.8" fill="{INK}">Automatic — the platform acts, nobody is Responsible.</text>')
        svg.append(f'<rect x="{lx+330}" y="{gy+18}" width="46" height="13" rx="5" fill="#fff" stroke="#8A6D3B" stroke-width="1.3" stroke-dasharray="4,3"/><text x="{lx+382}" y="{gy+28}" font-size="8.8" fill="{INK}">Outside the company — client, supplier, authority.</text>')
        svg.append(f'<rect x="{lx+700}" y="{gy+1}" width="72" height="13" rx="6.5" fill="{GREEN}"/><text x="{lx+704}" y="{gy+10.5}" font-size="7.4" font-weight="bold" fill="#fff">G6 Director·COO</text><text x="{lx+778}" y="{gy+11}" font-size="8.8" fill="{INK}">Gate: number · primary (Accountable) · alternate (Consulted) · window.</text>')
        svg.append(f'<rect x="{lx+700}" y="{gy+18}" width="46" height="13" rx="3" fill="#FDECEA" stroke="{RED}" stroke-width="1.3"/><text x="{lx+706}" y="{gy+28}" font-size="7.8" font-weight="bold" fill="{RED}">HB6</text><text x="{lx+778}" y="{gy+28}" font-size="8.8" fill="{INK}">Hard block: cannot proceed until the precondition exists.  <tspan fill="{ORANGE}">⚠ live deviation</tspan>  <tspan fill="{ORANGE}" stroke-dasharray="4,3">- - orange: return path</tspan>{self.legend_extra}</text>')
        svg.append(f'<text x="{right-4}" y="{gy+42}" font-size="8" text-anchor="end" fill="{MUTED}">Key: CEO Chief Executive Officer · COO Chief Operating Officer · PM Project Manager · PIC Person In Charge · 2d/3d working-day window · [state] from the schema</text>')
        svg.append('</svg>')
        open(path,"w").write("\n".join(svg))
        return dict(cols=ncol,col_w=round(col_w,1),box_w=round(box_w,1))
