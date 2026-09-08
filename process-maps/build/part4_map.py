from swimlane import Map
m=Map("Part 4 — Buy and Store",
      "Level-1 cross-functional map · as specified · purchase order to goods receipt, and the warehouse chain · gates 4, 5, 25a, 25b, 26, 27 · hard blocks 5 and 6 · 8 September 2026",
      [("supp","External Suppliers"),("exec","Executive"),("proc","Procurement"),("wh","Warehouse and Logistics"),("proj","Projects and Site"),("platform","The Platform")])
s=m.step
# --- the buy chain ---
s("4.1","proc","Create purchase order",rec="purchase_orders",state="draft",col=0)
s("4.2","proc","Add order lines against the bill of materials",rec="purchase_order_lines",state="open",col=1)
s("4.3","proc","Submit for approval",rec="purchase_orders",state="pending_approval",col=2,dev="refused unless the order has at least one line")
s("4.4","exec","Approve the order",rec="purchase_orders",state="approved",gate=("4 or 5","set by amount",None,None),col=3,dev="the browser invents the reference manual-<timestamp>; no approval request, no approver, no amount band")
s("4.5","proc","Issue the order to the supplier",rec="purchase_orders",state="issued",col=4,hb=("HB6","checks only that a reference string exists"))
s("4.6","supp","Supplier delivers",kind="external",col=5)
s("4.7","wh","Record goods receipt",rec="goods_receipts",state="pending",col=6,dev="nothing enters stock; over-receipt accepted; the three inspection statuses are unreachable")
s("4.8","platform","Delivery status recomputed",kind="auto",rec="purchase_orders",state="partially_delivered | fully_delivered",col=7)
s("4.9","platform","Material readiness — computed on read, never stored",kind="auto",col=8,dev="counts only order lines linked to a bill of materials line")
s("4.10","proc","Amend an issued order",col=9,dev="the schema reserves gate5ApprovalId; no mutation writes it — an issued order cannot be changed at all")
s("4.11","proc","Add supplier bank account",rec="supplier_bank_accounts",state="confirmed = false",col=10)
s("4.12","proc","A second person confirms the account",rec="supplier_bank_accounts",state="confirmed = true",col=11,dev="enforced — the person who added it cannot confirm it")
# --- the store chain ---
s("4.13","wh","Maintain locations and item catalogue",rec="locations · items",col=0)
s("4.14","wh","Create stock transfer",rec="stock_transfers",state="draft",col=1)
s("4.15","wh","Dispatch",rec="stock_transfers",state="dispatched",col=2,dev="no stock check — on hand goes negative; G25a and G25b are never raised")
s("4.16","proj","Receive at destination",rec="stock_transfers",state="received | discrepancy",col=3)
s("4.17","platform","Discrepancy flagged",kind="auto",rec="stock_positions",col=4,dev="the shortfall simply vanishes — no quarantine, no write-off, no variance record")
s("4.18","wh","Raise stock adjustment",rec="stock_adjustments",state="pending_approval",col=5)
s("4.19","exec","Approve the adjustment",rec="stock_adjustments",state="approved",gate=("26","Warehouse Custodian","PM",None),col=6,dev="the only same-person refusal in the platform; stock moves on approval")
s("4.20","wh","Open a physical count — stock snapshotted",rec="physical_counts",state="open",col=7,dev="lockDate is stored but locks nothing")
s("4.21","wh","Submit counted quantities",rec="physical_counts",state="submitted",col=8)
s("4.22","wh","Close the count",rec="physical_counts",state="closed",col=9,dev="every variance written to stock with no approval; G26 belongs here in the specification; G27 opening stock lock has no code")
s("4.23","proj","Issue material to site",rec="stock_transfers [warehouse_to_site]",col=10,hb=("HB5","quarantined material — the quarantined quantity is never set by any code, so the block can never fire"))
for a,b in [("4.1","4.2"),("4.2","4.3"),("4.3","4.4"),("4.4","4.5"),("4.5","4.6"),("4.6","4.7"),("4.7","4.8"),("4.8","4.9"),("4.9","4.10"),("4.10","4.11"),("4.11","4.12"),
            ("4.13","4.14"),("4.14","4.15"),("4.15","4.16"),("4.16","4.17"),("4.17","4.18"),("4.18","4.19"),("4.19","4.20"),("4.20","4.21"),("4.21","4.22"),("4.22","4.23")]: m.edge(a,b)
m.edge("4.7","4.5","partial delivery: the order stays open",kind="return")
m.edge("4.19","4.18","rejected: the adjustment is closed, stock unchanged",kind="return")
m.banner="Hard block 6 is enforced against a reference the browser invents, so it always passes · gates 4 and 5 are collapsed into one field, so the amount band is never applied · closing a physical count rewrites stock with no approval at all · the quarantined quantity is never set, so hard block 5 can never fire"
info=m.render("part4.svg"); print(info)
import re
svg=open("part4.svg").read()
open("part4.min.svg","w").write(re.sub(r'>\n\s*<','><',svg)); w,h=re.search(r'width="(\d+)" height="(\d+)"',svg).groups()
open("part4.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:A3 landscape;margin:5mm}} html,body{{margin:0;background:#fff}} svg{{width:{w}px;height:{h}px;display:block}}</style></head><body>'+svg+'</body></html>')
print("canvas",w,"x",h)
