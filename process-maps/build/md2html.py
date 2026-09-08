import re,html,sys
def inline(t):
    t=html.escape(t,quote=False)
    t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
    t=re.sub(r'(?<![\w*])\*(?!\*)([^*]+?)\*(?!\*)',r'<i>\1</i>',t)
    t=re.sub(r'`([^`]+)`',r'<code>\1</code>',t)
    return t
def convert(md):
    lines=md.split("\n"); out=[]; i=0
    def take_block(pred):
        nonlocal i
        buf=[]
        while i<len(lines) and pred(lines[i]): buf.append(lines[i]); i+=1
        return buf
    while i<len(lines):
        l=lines[i]
        if l.startswith("|"):
            rows=[r for r in take_block(lambda x:x.startswith("|")) if not re.match(r'^\|[\s\-:|]+\|$',r)]
            out.append("<table border='1' cellpadding='4' style='border-collapse:collapse;font-size:9pt'>")
            for ri,r in enumerate(rows):
                cells=[c.strip() for c in r.strip().strip("|").split("|")]; tag="th" if ri==0 else "td"
                out.append("<tr>"+"".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells)+"</tr>")
            out.append("</table>"); continue
        m=re.match(r'^(#{1,4}) (.*)',l)
        if m: out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>"); i+=1; continue
        if l.strip()=="---": out.append("<hr/>"); i+=1; continue
        if re.match(r'^\s*[-*] ',l) or re.match(r'^\s*\d+\. ',l):
            ordered=bool(re.match(r'^\s*\d+\. ',l)); items=[]
            while i<len(lines) and (re.match(r'^\s*[-*] ',lines[i]) or re.match(r'^\s*\d+\. ',lines[i])):
                item=re.sub(r'^\s*(?:[-*]|\d+\.) ','',lines[i]); i+=1
                while i<len(lines) and lines[i].startswith("  ") and lines[i].strip() and not re.match(r'^\s*(?:[-*]|\d+\.) ',lines[i]):
                    item+=" "+lines[i].strip(); i+=1
                items.append(item)
            tag="ol" if ordered else "ul"
            out.append(f"<{tag}>"+"".join(f"<li>{inline(x)}</li>" for x in items)+f"</{tag}>"); continue
        if l.strip()=="": i+=1; continue
        para=[l]; i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(("|","#")) and not re.match(r'^\s*(?:[-*]|\d+\.) ',lines[i]) and lines[i].strip()!="---":
            para.append(lines[i]); i+=1
        out.append(f"<p>{inline(' '.join(x.strip() for x in para))}</p>")
    return "<html><body style='font-family:Arial;font-size:10.5pt'>"+"\n".join(out)+"</body></html>"
if __name__=="__main__":
    src,dst=sys.argv[1],sys.argv[2]; open(dst,"w").write(convert(open(src).read())); print(dst,len(open(dst).read()),"bytes")
