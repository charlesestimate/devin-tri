# Minimal SVG -> PDF for the process-map drawings: rect (rx), polygon, line, text/tspan.
# Uses base-14 Helvetica (never embedded) -> small files. A3 landscape.
import sys,re,zlib,xml.etree.ElementTree as ET
NS='{http://www.w3.org/2000/svg}'
# Helvetica AFM widths for chars 32..126 (per 1000 em)
_W=[278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584]
_WB=[278,333,474,556,556,889,722,238,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,333,333,584,584,584,611,975,722,722,722,722,667,611,778,722,278,556,722,611,833,722,778,667,778,722,667,611,722,667,944,667,667,611,333,278,333,584,556,333,556,611,556,611,556,333,611,611,278,278,556,278,889,611,611,611,611,389,556,333,611,556,778,556,556,500,389,280,389,584]
EXTRA={'·':278,'—':1000,'–':556,'×':584,'≤':584,'₱':556,'→':700,'⚠':760,'●':600,'≥':584}
WINANSI={'·':0xB7,'—':0x97,'–':0x96,'×':0xD7,'’':0x92,'‘':0x91,'“':0x93,'”':0x94}
def width(s,bold):
    t=_WB if bold else _W; w=0
    for c in s:
        o=ord(c)
        if 32<=o<=126: w+=t[o-32]
        else: w+=EXTRA.get(c,556)
    return w/1000.0
def hexrgb(h):
    h=h.strip()
    if h.startswith('#'):
        h=h[1:]; 
        if len(h)==3: h=''.join(c*2 for c in h)
        return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
    return None
def esc(s):
    out=[]
    for c in s:
        o=ord(c)
        if c in '()\\': out.append('\\'+c)
        elif 32<=o<=126: out.append(c)
        elif c in WINANSI: out.append('\\%03o'%WINANSI[c])
        else: out.append('?')
    return ''.join(out)
def convert(svg_path,pdf_path,page=(1190.55,841.89),margin=14.2):
    root=ET.parse(svg_path).getroot()
    vb=[float(v) for v in root.get('viewBox').split()]; sw,sh=vb[2],vb[3]
    PW,PH=page; s=min((PW-2*margin)/sw,(PH-2*margin)/sh); ox=margin; oy=PH-margin
    def X(x): return ox+x*s
    def Y(y): return oy-y*s
    ops=[]; fonts_used=set()
    def col(c,stroke=False):
        r=hexrgb(c) if c else None
        if r is None: return None
        ops.append('%.3f %.3f %.3f %s'%(r[0],r[1],r[2],'RG' if stroke else 'rg')); return True
    def rrect(x,y,w,h,rx):
        x0,y0,x1,y1=X(x),Y(y+h),X(x+w),Y(y); r=min(rx*s,(x1-x0)/2,(y1-y0)/2); k=0.5523*r
        if r<=0.01:
            ops.append('%.2f %.2f %.2f %.2f re'%(x0,y0,x1-x0,y1-y0)); return
        ops.append('%.2f %.2f m'%(x0+r,y0))
        ops.append('%.2f %.2f l %.2f %.2f %.2f %.2f %.2f %.2f c'%(x1-r,y0, x1-r+k,y0, x1,y0+r-k, x1,y0+r))
        ops.append('%.2f %.2f l %.2f %.2f %.2f %.2f %.2f %.2f c'%(x1,y1-r, x1,y1-r+k, x1-r+k,y1, x1-r,y1))
        ops.append('%.2f %.2f l %.2f %.2f %.2f %.2f %.2f %.2f c'%(x0+r,y1, x0+r-k,y1, x0,y1-r+k, x0,y1-r))
        ops.append('%.2f %.2f l %.2f %.2f %.2f %.2f %.2f %.2f c h'%(x0,y0+r, x0,y0+r-k, x0+r-k,y0, x0+r,y0))
    def paint(fill,stroke,sw_):
        f=col(fill) if fill and fill!='none' else None
        st=col(stroke,True) if stroke and stroke!='none' else None
        if st: ops.append('%.2f w'%(float(sw_ or 1)*s))
        ops.append('B' if (f and st) else ('f' if f else ('S' if st else 'n')))
    def glyph(ch,x,y,size,color):
        # draw substitutes for glyphs Helvetica lacks; x,y in svg units at baseline; returns advance (svg units)
        adv=EXTRA.get(ch,556)/1000*size
        r=hexrgb(color) or (0,0,0)
        ops.append('q %.3f %.3f %.3f rg %.3f %.3f %.3f RG'%(r+r))
        if ch=='→':
            y0=y-size*0.33; x0=x+size*0.08; x1=x+adv-size*0.1
            ops.append('%.2f w %.2f %.2f m %.2f %.2f l S'%(max(0.6,size*0.09*s),X(x0),Y(y0),X(x1),Y(y0)))
            ops.append('%.2f %.2f m %.2f %.2f l %.2f %.2f l h f'%(X(x1),Y(y0),X(x1-size*0.28),Y(y0-size*0.22),X(x1-size*0.28),Y(y0+size*0.22)))
        elif ch=='⚠':
            cx=x+adv/2; top=y-size*0.78; bot=y+size*0.02; hw=size*0.36
            ops.append('%.2f %.2f m %.2f %.2f l %.2f %.2f l h f'%(X(cx),Y(top),X(cx-hw),Y(bot),X(cx+hw),Y(bot)))
            ops.append('1 1 1 rg %.2f %.2f %.2f %.2f re f %.2f %.2f %.2f %.2f re f'%(X(cx-size*0.05),Y(y-size*0.2),size*0.1*s,size*0.35*s, X(cx-size*0.05),Y(y-size*0.06),size*0.1*s,size*0.1*s))
        elif ch=='●':
            cx,cy,rr=X(x+adv/2),Y(y-size*0.3),size*0.28*s; k=0.5523*rr
            ops.append('%.2f %.2f m %.2f %.2f %.2f %.2f %.2f %.2f c %.2f %.2f %.2f %.2f %.2f %.2f c %.2f %.2f %.2f %.2f %.2f %.2f c %.2f %.2f %.2f %.2f %.2f %.2f c f'%(cx+rr,cy, cx+rr,cy+k,cx+k,cy+rr,cx,cy+rr, cx-k,cy+rr,cx-rr,cy+k,cx-rr,cy, cx-rr,cy-k,cx-k,cy-rr,cx,cy-rr, cx+k,cy-rr,cx+rr,cy-k,cx+rr,cy))
        elif ch=='₱':
            ops.append('BT /F%s %.2f Tf %.2f %.2f Td (P) Tj ET'%('B' if False else 'R',size*s,X(x),Y(y)))
            ops.append('%.2f w %.2f %.2f m %.2f %.2f l %.2f %.2f m %.2f %.2f l S'%(max(0.5,size*0.06*s),X(x-size*0.02),Y(y-size*0.52),X(x+size*0.62),Y(y-size*0.52),X(x-size*0.02),Y(y-size*0.40),X(x+size*0.62),Y(y-size*0.40)))
        elif ch=='≤':
            ops.append('BT /FR %.2f Tf %.2f %.2f Td (<) Tj ET'%(size*s,X(x),Y(y)))
            ops.append('%.2f w %.2f %.2f m %.2f %.2f l S'%(max(0.5,size*0.06*s),X(x+size*0.05),Y(y+size*0.12),X(x+size*0.5),Y(y+size*0.12)))
        ops.append('Q'); return adv
    def run_text(txt,x,y,size,bold,italic,color):
        # writes a run starting at x; returns advance in svg units
        fk='B' if bold else ('I' if italic else 'R'); fonts_used.add(fk)
        r=hexrgb(color) or (0,0,0); cur=x; buf=''
        def flush():
            nonlocal buf,cur
            if buf:
                ops.append('BT /F%s %.2f Tf %.3f %.3f %.3f rg %.2f %.2f Td (%s) Tj ET'%(fk,size*s,r[0],r[1],r[2],X(cur),Y(y),esc(buf)))
                cur+=width(buf,bold)*size; buf=''
        for ch in txt:
            o=ord(ch)
            if 32<=o<=126 or ch in WINANSI: buf+=ch
            else: flush(); cur+=glyph(ch,cur,y,size,color)
        flush(); return cur-x
    def text_width(txt,size,bold):
        return sum((width(c,bold)*size if (32<=ord(c)<=126 or c in WINANSI) else EXTRA.get(c,556)/1000*size) for c in txt)
    for el in root.iter():
        tag=el.tag.replace(NS,'')
        if tag=='rect':
            x,y,w,h=[float(el.get(k,0)) for k in ('x','y','width','height')]; rx=float(el.get('rx',0))
            rrect(x,y,w,h,rx); paint(el.get('fill','#000'),el.get('stroke'),el.get('stroke-width'))
        elif tag=='polygon':
            pts=[tuple(map(float,p.split(','))) for p in el.get('points').split()]
            ops.append('%.2f %.2f m '%(X(pts[0][0]),Y(pts[0][1]))+' '.join('%.2f %.2f l'%(X(a),Y(b)) for a,b in pts[1:])+' h')
            paint(el.get('fill','#000'),el.get('stroke'),el.get('stroke-width'))
        elif tag=='line':
            da=el.get('stroke-dasharray')
            ops.append('q'); 
            if da: ops.append('[%s] 0 d'%' '.join('%.2f'%(float(v)*s) for v in re.split('[ ,]+',da.strip())))
            col(el.get('stroke','#000'),True); ops.append('%.2f w %.2f %.2f m %.2f %.2f l S Q'%(float(el.get('stroke-width',1))*s,X(float(el.get('x1'))),Y(float(el.get('y1'))),X(float(el.get('x2'))),Y(float(el.get('y2')))))
        elif tag=='text':
            size=float(el.get('font-size',10)); bold=(el.get('font-weight')=='bold'); italic=(el.get('font-style')=='italic')
            color=el.get('fill','#000'); anchor=el.get('text-anchor','start'); x=float(el.get('x',0)); y=float(el.get('y',0))
            runs=[]
            if el.text: runs.append((el.text,bold,italic,color))
            for ts in el:
                if ts.tag.replace(NS,'')=='tspan':
                    runs.append((ts.text or '',ts.get('font-weight','bold' if bold else '')=='bold',ts.get('font-style','italic' if italic else '')=='italic',ts.get('fill',color)))
                    if ts.tail: runs.append((ts.tail,bold,italic,color))
            total=sum(text_width(t,size,b) for t,b,i,c in runs)
            if anchor=='middle': x-=total/2
            elif anchor=='end': x-=total
            cur=x
            for t,b,i,c in runs: cur+=run_text(t,cur,y,size,b,i,c)
    content=zlib.compress(('\n'.join(ops)).encode('latin-1'),9)
    fonts={'R':'Helvetica','B':'Helvetica-Bold','I':'Helvetica-Oblique'}
    objs=[]
    def add(o): objs.append(o); return len(objs)
    fobj={k:add('<< /Type /Font /Subtype /Type1 /BaseFont /%s /Encoding /WinAnsiEncoding >>'%v) for k,v in fonts.items()}
    cobj=add(('<< /Length %d /Filter /FlateDecode >>\nstream\n'%len(content)).encode()+content+b'\nendstream')
    res='<< /Font << '+' '.join('/F%s %d 0 R'%(k,v) for k,v in fobj.items())+' >> >>'
    pobj=add('<< /Type /Page /Parent %%PAGES%% /MediaBox [0 0 %.2f %.2f] /Contents %d 0 R /Resources %s >>'%(PW,PH,cobj,res))
    pages=add('<< /Type /Pages /Kids [%d 0 R] /Count 1 >>'%pobj)
    objs[pobj-1]=objs[pobj-1].replace('%PAGES%','%d 0 R'%pages)
    cat=add('<< /Type /Catalog /Pages %d 0 R >>'%pages)
    out=bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n'); offs=[]
    for i,o in enumerate(objs,1):
        offs.append(len(out)); out+=('%d 0 obj\n'%i).encode(); out+=(o.encode('latin-1') if isinstance(o,str) else o); out+=b'\nendobj\n'
    xref=len(out); out+=('xref\n0 %d\n0000000000 65535 f \n'%(len(objs)+1)).encode()
    for o in offs: out+=('%010d 00000 n \n'%o).encode()
    out+=('trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n'%(len(objs)+1,cat,xref)).encode()
    open(pdf_path,'wb').write(out); return len(out)
if __name__=='__main__':
    n=convert(sys.argv[1],sys.argv[2]); print(sys.argv[2],n,'bytes')
