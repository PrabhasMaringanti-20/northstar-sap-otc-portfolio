-- Synthetic order cohort: all supplied orders, snapshot 2026-10-11.
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
