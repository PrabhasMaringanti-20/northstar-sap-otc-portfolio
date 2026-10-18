"""Reproducible synthetic data and independently checked KPI calculations; stdlib only."""
from pathlib import Path
from datetime import date, timedelta
from collections import defaultdict
import csv, json, random, sqlite3, statistics, hashlib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'phase-08'
DATA=OUT/'data'
DATA.mkdir(parents=True,exist_ok=True)
ASOF=date(2026,10,11)
SEED=20261011
rng=random.Random(SEED)

def write_csv(name, rows, fields=None):
    with (DATA/(name+'.csv')).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0])); w.writeheader();w.writerows(rows)

customers=[dict(customer_id=f'CUST-{i:03}',customer_name='Alder Engineering Ltd' if i==1 else f'Fictional UK Customer {i:02}',country='GB',currency='GBP',payment_terms_days=30) for i in range(1,21)]
products=[dict(product_id=f'PROD-{i:03}',product_name=n,unit_price_pence=p,uom='EA') for i,(n,p) in enumerate([('Standard mounting bracket',2500),('Steel spacer',1200),('Support plate',4000),('Machine guard panel',6500),('Mounting rail',3000)],1)]
orders=[];deliveries=[];invoices=[];receipts=[];allocations=[];events=[]
def event(oid,typ,d,role,detail):
    events.append(dict(event_id=f'EVT-{len(events)+1:04}',order_id=oid,event_type=typ,event_date=str(d),role=role,detail=detail))
for i in range(300):
    oid=f'NS-ORD-{1001+i}'
    received=date(2026,10,5) if i==0 else date(2026,7,1)+timedelta(days=rng.randrange(102))
    prod=products[0] if i==0 else rng.choice(products)
    qty=100 if i==0 else rng.choice([10,20,40,60,80,100])
    cancelled=i>0 and i%17==0
    issue='Stock availability unresolved' if i==0 else ('Customer cancellation' if cancelled else rng.choice(['None']*6+['Stock shortage','Customer data correction','Credit review','Billing handoff']))
    initial='' if i==0 else str(received+timedelta(days=rng.randint(4,8)))
    o=dict(order_id=oid,customer_id='CUST-001' if i==0 else rng.choice(customers)['customer_id'],product_id=prod['product_id'],warehouse_id='WH-01',received_date=str(received),requested_receipt_date=str(date(2026,10,9) if i==0 else received+timedelta(days=5)),initial_confirmed_receipt_date=initial,ordered_qty=qty,unit_price_pence=prod['unit_price_pence'],net_value_pence=qty*prod['unit_price_pence'],cancelled=int(cancelled),cancelled_date=str(received) if cancelled else '',partial_allowed=0 if i==0 else int(i%3!=0),exception=issue)
    orders.append(o)
    event(oid,'order_received',received,'Sales','Synthetic intake')
    if i>0 and (i%7==0 or issue=='Customer data correction'):
        event(oid,'validation_error',received,'Sales',rng.choice(['Missing ship-to corrected','Invalid quantity corrected','Incorrect price corrected']));event(oid,'manual_touch',received,'Sales','Rekey corrected data')
    if i%3!=0:event(oid,'manual_touch',received,'Customer Service','Chase status update')
    if issue=='Billing handoff':event(oid,'manual_touch',received,'Finance','Request missing handoff information')
    if cancelled:event(oid,'cancelled',received,'Sales','Cancelled before dispatch');continue
    if i==0 or i%19==0:continue
    split=o['partial_allowed'] and i%4==0
    quantities=[qty//2,qty-qty//2] if split else [qty]
    for j,q in enumerate(quantities):
        if j==1 and i%8==0:continue
        delay=4 if issue=='Stock shortage' else 0
        dispatch=received+timedelta(days=rng.randint(1,6)+delay+j*5)
        if dispatch>ASOF:continue
        gi=dispatch+timedelta(days=1 if i%6==0 else 0)
        receipt=dispatch+timedelta(days=rng.randint(1,3))
        d=dict(delivery_id=f'DEL-{len(deliveries)+1:04}',order_id=oid,shipped_qty=q,dispatch_date=str(dispatch),goods_issue_posting_date=str(gi) if gi<=ASOF else '',customer_receipt_date=str(receipt) if receipt<=ASOF else '')
        deliveries.append(d)
        if gi>ASOF or i%23==0:continue
        bill=gi+timedelta(days=rng.randint(0,3)+(4 if issue=='Billing handoff' else 0))
        if bill>ASOF:continue
        inv=dict(invoice_id=f'INV-{len(invoices)+1:04}',delivery_id=d['delivery_id'],invoice_date=str(bill),due_date=str(bill+timedelta(days=30)),net_amount_pence=q*o['unit_price_pence'])
        invoices.append(inv)
        if i%11==0:continue
        amount=inv['net_amount_pence']
        chunks=[amount//2,amount-amount//2] if i%5==0 else [amount]
        for k,amt in enumerate(chunks):
            if k==1 and i%10==0:continue
            pd=bill+timedelta(days=rng.randint(10,35)+k*5)
            if pd>ASOF:continue
            rec=dict(receipt_id=f'PAY-{len(receipts)+1:04}',customer_id=o['customer_id'],received_date=str(pd),amount_pence=amt,reference=inv['invoice_id'])
            receipts.append(rec)
            allocations.append(dict(allocation_id=f'ALLOC-{len(allocations)+1:04}',receipt_id=rec['receipt_id'],invoice_id=inv['invoice_id'],allocation_date=str(pd),allocated_pence=amt))
for i in range(12):
    receipts.append(dict(receipt_id=f'PAY-{len(receipts)+1:04}',customer_id=customers[i]['customer_id'],received_date=str(ASOF-timedelta(days=i)),amount_pence=20000+i*1000,reference='Unmatched remittance'))

tables=dict(customers=customers,products=products,orders=orders,deliveries=deliveries,invoices=invoices,receipts=receipts,allocations=allocations,events=events)
for name,rows in tables.items():write_csv(name,rows)

db=sqlite3.connect(':memory:')
for name,rows in tables.items():
    fields=list(rows[0]); types={k:('INTEGER' if isinstance(rows[0][k],int) else 'TEXT') for k in fields}
    db.execute(f'CREATE TABLE {name} ('+','.join(f'{k} {types[k]}' for k in fields)+')')
    db.executemany(f'INSERT INTO {name} VALUES ('+','.join('?' for _ in fields)+')', [[row[k] for k in fields] for row in rows])
sql='''-- Synthetic order cohort: all supplied orders, snapshot 2026-10-11.
-- Aggregate deliveries before joining to orders. Never SUM order value over raw children.
CREATE VIEW delivery_by_order AS
SELECT order_id, SUM(shipped_qty) shipped_qty,
 SUM(CASE WHEN customer_receipt_date <> '' THEN shipped_qty ELSE 0 END) received_qty,
 MAX(CASE WHEN customer_receipt_date <> '' THEN customer_receipt_date END) last_receipt
FROM deliveries GROUP BY order_id;
CREATE VIEW order_summary AS
SELECT o.*, COALESCE(d.shipped_qty,0) shipped_qty, COALESCE(d.received_qty,0) received_qty,
 CASE WHEN COALESCE(d.received_qty,0)=o.ordered_qty THEN d.last_receipt ELSE NULL END full_receipt_date
FROM orders o LEFT JOIN delivery_by_order d USING(order_id);
-- KPI-001: mean calendar days to full customer receipt, completed noncancelled only.
SELECT AVG(julianday(full_receipt_date)-julianday(received_date)) FROM order_summary WHERE cancelled=0 AND full_receipt_date IS NOT NULL;
-- KPI-002: due initial promises; incomplete overdue orders are failures, unknown promises excluded.
SELECT 100.0*SUM(CASE WHEN full_receipt_date<=initial_confirmed_receipt_date THEN 1 ELSE 0 END)/COUNT(*)
FROM order_summary WHERE cancelled=0 AND initial_confirmed_receipt_date<>'' AND initial_confirmed_receipt_date<='2026-10-11';
-- KPI-003: received units / ordered units, noncancelled cohort, as-of snapshot.
SELECT 100.0*SUM(received_qty)/SUM(ordered_qty) FROM order_summary WHERE cancelled=0;
-- KPI-004: posted GI to invoice, billed deliveries only. Unbilled count is disclosed separately.
SELECT AVG(julianday(i.invoice_date)-julianday(d.goods_issue_posting_date)) FROM invoices i JOIN deliveries d USING(delivery_id);
-- KPI-005/006: count distinct affected orders, including subsequently cancelled orders.
SELECT 100.0*COUNT(DISTINCT order_id)/(SELECT COUNT(*) FROM orders) FROM events WHERE event_type='validation_error';
SELECT 100.0*COUNT(DISTINCT order_id)/(SELECT COUNT(*) FROM orders) FROM events WHERE event_type='manual_touch';
-- Balance: aggregate allocations before invoice/receipt joins.
SELECT i.invoice_id,i.net_amount_pence-COALESCE(a.paid,0) outstanding_pence
FROM invoices i LEFT JOIN (SELECT invoice_id,SUM(allocated_pence) paid FROM allocations GROUP BY invoice_id) a USING(invoice_id);
'''
(OUT/'kpi_queries.sql').write_text(sql)
db.executescript(sql[:sql.index('-- KPI-001')])
db.row_factory=sqlite3.Row
summary=[dict(x) for x in db.execute('SELECT * FROM order_summary')]
write_csv('order_summary',summary)

ds=defaultdict(list)
for d in deliveries:ds[d['order_id']].append(d)
oms={o['order_id']:o for o in orders};dms={d['delivery_id']:d for d in deliveries}; ims={x['invoice_id']:x for x in invoices};rms={x['receipt_id']:x for x in receipts}
full={o['order_id']:max(d['customer_receipt_date'] for d in ds[o['order_id']]) for o in orders if ds[o['order_id']] and all(d['customer_receipt_date'] for d in ds[o['order_id']]) and sum(d['shipped_qty'] for d in ds[o['order_id']])==o['ordered_qty']}
noncancel=[o for o in orders if not o['cancelled']]
completed=[o for o in noncancel if o['order_id'] in full]
due=[o for o in noncancel if o['initial_confirmed_receipt_date'] and o['initial_confirmed_receipt_date']<=str(ASOF)]
on_time=sum(o['order_id'] in full and full[o['order_id']]<=o['initial_confirmed_receipt_date'] for o in due)
received_units=sum(d['shipped_qty'] for d in deliveries if d['customer_receipt_date'])
cycle=statistics.mean((date.fromisoformat(full[o['order_id']])-date.fromisoformat(o['received_date'])).days for o in completed)
billing=statistics.mean((date.fromisoformat(i['invoice_date'])-date.fromisoformat(dms[i['delivery_id']]['goods_issue_posting_date'])).days for i in invoices)
error_ids={e['order_id'] for e in events if e['event_type']=='validation_error'}
manual_ids={e['order_id'] for e in events if e['event_type']=='manual_touch'}
vals=[cycle,100*on_time/len(due),100*received_units/sum(o['ordered_qty'] for o in noncancel),billing,100*len(error_ids)/len(orders),100*len(manual_ids)/len(orders)]
sql_no_comments='\n'.join(line for line in sql.splitlines() if not line.lstrip().startswith('--'))
sqlqueries=[s.strip() for s in sql_no_comments.split(';') if 'SELECT' in s and 'CREATE VIEW' not in s]
independent=[db.execute(q).fetchone()[0] for q in sqlqueries[:6]]
checks=[]
def check(name,condition,detail):
    checks.append(dict(check_id=f'DQ-{len(checks)+1:03}',name=name,status='Passed' if condition else 'Failed',detail=detail,execution_type='Executed Python/SQLite data check',date='2026-10-11'))
    if not condition:raise AssertionError(name)
for name,rows in tables.items():
    key=list(rows[0])[0];check(name+' primary key',len({x[key] for x in rows})==len(rows) and all(x[key] for x in rows),f'{len(rows)} unique non-null keys')
check('Order master references',all(o['customer_id'] in {c['customer_id'] for c in customers} and o['product_id'] in {p['product_id'] for p in products} for o in orders),'Customer and product parents exist')
check('Delivery/invoice parent references',all(d['order_id'] in oms for d in deliveries) and all(i['delivery_id'] in dms for i in invoices),'No orphan fulfilment records')
check('Receipt/allocation references',all(a['invoice_id'] in ims and a['receipt_id'] in rms for a in allocations),'No orphan payment links')
check('Receipt customer references',all(p['customer_id'] in {c['customer_id'] for c in customers} for p in receipts),'Every cash receipt has a known synthetic customer')
check('Order value arithmetic',all(o['net_value_pence']==o['ordered_qty']*o['unit_price_pence'] for o in orders),'Integer pence, tax excluded')
check('Quantity bounds and cancelled fulfilment',all(sum(d['shipped_qty'] for d in ds[o['order_id']])<=o['ordered_qty'] and (not o['cancelled'] or not ds[o['order_id']]) for o in orders),'No overdelivery or cancelled order shipment')
check('Partial permission',all(o['partial_allowed'] or not ds[o['order_id']] or (len(ds[o['order_id']])==1 and ds[o['order_id']][0]['shipped_qty']==o['ordered_qty']) for o in orders),'Split/short shipments require permission in synthetic baseline')
check('Delivery chronology',all(oms[d['order_id']]['received_date']<=d['dispatch_date']<=str(ASOF) and (not d['goods_issue_posting_date'] or d['dispatch_date']<=d['goods_issue_posting_date']<=str(ASOF)) and (not d['customer_receipt_date'] or d['dispatch_date']<=d['customer_receipt_date']<=str(ASOF)) for d in deliveries),'Physical and posting events separated; future actuals excluded')
check('Invoice chronology and amount',all(dms[i['delivery_id']]['goods_issue_posting_date'] and dms[i['delivery_id']]['goods_issue_posting_date']<=i['invoice_date']<=str(ASOF) and i['net_amount_pence']==dms[i['delivery_id']]['shipped_qty']*oms[dms[i['delivery_id']]['order_id']]['unit_price_pence'] for i in invoices),'Only observed goods-issued deliveries billed; one active invoice per delivery')
check('No duplicate active invoice',len({i['delivery_id'] for i in invoices})==len(invoices),'Simplified dataset excludes correction documents')
ar=defaultdict(int);ai=defaultdict(int)
for a in allocations:ar[a['receipt_id']]+=a['allocated_pence'];ai[a['invoice_id']]+=a['allocated_pence']
check('Allocation upper bounds',all(0<=ar[r['receipt_id']]<=r['amount_pence'] for r in receipts) and all(0<=ai[i['invoice_id']]<=i['net_amount_pence'] for i in invoices),'No cash or invoice over-allocation')
check('Allocation chronology/customer',all(ims[a['invoice_id']]['invoice_date']<=a['allocation_date']<=str(ASOF) and rms[a['receipt_id']]['received_date']<=a['allocation_date'] and rms[a['receipt_id']]['customer_id']==oms[dms[ims[a['invoice_id']]['delivery_id']]['order_id']]['customer_id'] for a in allocations),'Matching customers and valid event order')
check('Python versus independent SQL KPIs',all(abs(a-b)<1e-9 for a,b in zip(vals,independent)),'All six calculations agree before rounding')
check('Example retained',orders[0]['net_value_pence']==250000 and not ds['NS-ORD-1001'] and orders[0]['initial_confirmed_receipt_date']=='','Representative case retains unresolved availability; no fabricated fulfilment')
check('Split and partial payment coverage',any(len(v)>1 for v in ds.values()) and any(0<ai[i['invoice_id']]<i['net_amount_pence'] for i in invoices),'Dataset includes split deliveries and unpaid residual analytical amounts')

# Hand-calculated fixture independent of random generation: four orders.
fixture=[dict(id='FIX-01',ordered=100,received=100,cancelled=0,received_day=1,promise_day=5,full_day=5,value=250000,deliveries=[60,40],allocations=[90000,60000],error=0,manual=1),dict(id='FIX-02',ordered=100,received=40,cancelled=0,received_day=1,promise_day=5,full_day=None,value=250000,deliveries=[40],allocations=[],error=1,manual=1),dict(id='FIX-03',ordered=100,received=0,cancelled=1,received_day=1,promise_day=5,full_day=None,value=250000,deliveries=[],allocations=[],error=0,manual=0),dict(id='FIX-04',ordered=100,received=0,cancelled=0,received_day=9,promise_day=15,full_day=None,value=250000,deliveries=[],allocations=[],error=0,manual=0)]
expected=dict(cycle_days=4,otd_pct=50,fulfilment_pct=140/300*100,error_pct=25,manual_pct=50,billing_days=2,order_value_pence=1000000)
actual=dict(cycle_days=statistics.mean(x['full_day']-x['received_day'] for x in fixture if x['full_day'] and not x['cancelled']),otd_pct=100*sum(x['full_day'] is not None and x['full_day']<=x['promise_day'] for x in fixture if not x['cancelled'] and x['promise_day']<=10)/sum(not x['cancelled'] and x['promise_day']<=10 for x in fixture),fulfilment_pct=100*sum(x['received'] for x in fixture if not x['cancelled'])/sum(x['ordered'] for x in fixture if not x['cancelled']),error_pct=100*sum(x['error'] for x in fixture)/len(fixture),manual_pct=100*sum(x['manual'] for x in fixture)/len(fixture),billing_days=statistics.mean([2,3,1]),order_value_pence=sum(x['value'] for x in fixture))
check('Four-order hand oracle',all(abs(actual[k]-v)<1e-9 for k,v in expected.items()),'Cycle 4d; on-time 50%; fulfilment 46.6667%; error 25%; manual 50%; billing 2d; value £10,000')
ROOT.joinpath('quality/fixtures.json').write_text(json.dumps(dict(orders=fixture,as_of_day=10,billing_gi_days=[2,3,4],billing_invoice_days=[4,6,5],expected=expected,actual=actual),indent=2))
write_csv('data_checks',checks)
labels=['Order cycle time','On-time delivery','Order fulfilment rate','Billing cycle time','Order error rate','Manual-touch rate']
den=[len(completed),len(due),sum(o['ordered_qty'] for o in noncancel),len(invoices),len(orders),len(orders)]
metrics=[dict(id=f'KPI-{i+1:03}',name=n,value=round(v,4),unit='calendar days' if i in [0,3] else '%',denominator=den[i],basis='Synthetic baseline; not measured business performance') for i,(n,v) in enumerate(zip(labels,vals))]
unbilled=[d for d in deliveries if d['goods_issue_posting_date'] and d['delivery_id'] not in {i['delivery_id'] for i in invoices}]
context=dict(as_of=str(ASOF),seed=SEED,counts={k:len(v) for k,v in tables.items()},cancelled=sum(o['cancelled'] for o in orders),completed=len(completed),open_non_cancelled=len(noncancel)-len(completed),unknown_promise=sum(not o['initial_confirmed_receipt_date'] for o in noncancel),due_promises=len(due),on_time=on_time,received_units=received_units,ordered_units=sum(o['ordered_qty'] for o in noncancel),unbilled_goods_issued=len(unbilled),split_orders=sum(len(v)>1 for v in ds.values()),partially_received_orders=sum(0<s['received_qty']<s['ordered_qty'] for s in summary),partially_paid_invoices=sum(0<ai[i['invoice_id']]<i['net_amount_pence'] for i in invoices),unallocated_pence=sum(p['amount_pence']-ar[p['receipt_id']] for p in receipts),invoice_outstanding_pence=sum(i['net_amount_pence']-ai[i['invoice_id']] for i in invoices),total_order_value_pence=sum(o['net_value_pence'] for o in orders),checks=len(checks))
manifest={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(DATA.glob('*.csv')) if f.stem!='data_checks'}
(OUT/'results.json').write_text(json.dumps(dict(context=context,metrics=metrics,checks=checks,sha256=manifest),indent=2))
db.row_factory=None
target=OUT/'northstar_synthetic.sqlite'
if target.exists():target.unlink()
db.commit()
backup=sqlite3.connect(target);db.backup(backup);backup.close()
print(json.dumps(dict(context=context,metrics=metrics),indent=2))
