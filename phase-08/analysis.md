# Synthetic data model, analysis and reproducibility

Independent simulated portfolio · 2026-10-11 · AI-assisted draft; learner review pending.


## Model before generation
| Table | Grain | Key | Relationship |
| --- | --- | --- | --- |
| customers | One fictional customer | customer_id | None |
| products | One stocked product | product_id | None |
| orders | One single-line order | order_id | customer_id → customers; product_id → products |
| deliveries | One shipment for an order | delivery_id | order_id → orders |
| invoices | One active net-only invoice per delivery | invoice_id | delivery_id → deliveries |
| receipts | One incoming net-only receipt | receipt_id | customer_id → customers |
| allocations | One receipt-to-invoice allocation | allocation_id | receipt_id → receipts; invoice_id → invoices |
| events | One intake/quality/manual/cancellation event | event_id | order_id → orders |

All records are synthetic, generated with Python random seed 20261011. 300 orders, 20 customers, five products and one warehouse; single line per order is a deliberate simplification. A future multi-line model needs order_items and line-level delivery/invoice links. Receipts and invoices can have multiple allocation rows structurally, although this generator mainly demonstrates split payments per invoice plus unmatched receipts rather than every possible many-to-many pattern.

Generation uses an intake cohort from 1 July through 11 October 2026, snapshot 11 October 2026. Orders received near the cutoff have less time to finish; open and future-due counts must be shown. Dates are UK business-local calendar dates; weekends are not excluded. NS-ORD-1001 preserves the Phase 1 facts and remains unconfirmed/unfulfilled. Other distributions are designed teaching examples, not calibrated observations. All financial amounts are **net-only integer pence**, with VAT deliberately excluded from invoices and receipts; this is not a complete UK receivables ledger.

## Generation assumptions
Every seventeenth non-base order is cancelled before dispatch. Every nineteenth is left without fulfilment. Some permitted orders split into two shipments; some remain partial. Stock-shortage labels add delay. Billing-handoff labels add billing delay. Errors and manual touches are explicit event records. Pending future events are omitted, not recorded as actuals. No returns, invoice corrections, overpayments, discounts, tax or bad debt are generated; those scenarios remain in design/UAT. This bias intentionally illustrates the problems and cannot prove causation.

## Relationships and double-counting
orders 1:N deliveries; deliveries 1:1 invoices in this simplified dataset; invoices 1:N allocations and receipts 1:N allocations. Aggregate delivery quantity to order, allocations to invoice/receipt, and event flags to order before joining. Never SUM order value after joining raw deliveries and allocations. The four-order fixture demonstrates that £10,000 remains £10,000 regardless of child-row count.

## Executed baseline results — not achieved improvements
| id | name | value | unit | denominator | basis |
| --- | --- | --- | --- | --- | --- |
| KPI-001 | Order cycle time | 6.1595 | calendar days | 232 | Synthetic baseline; not measured business performance |
| KPI-002 | On-time delivery | 49.0706 | % | 269 | Synthetic baseline; not measured business performance |
| KPI-003 | Order fulfilment rate | 84.8933 | % | 14530 | Synthetic baseline; not measured business performance |
| KPI-004 | Billing cycle time | 1.9504 | calendar days | 262 | Synthetic baseline; not measured business performance |
| KPI-005 | Order error rate | 22.3333 | % | 300 | Synthetic baseline; not measured business performance |
| KPI-006 | Manual-touch rate | 76.3333 | % | 300 | Synthetic baseline; not measured business performance |

Context: 17 cancelled; 232 fully received; 51 open noncancelled; 1 unknown initial promise; 21 orders with multiple deliveries; 21 partially received; 20 partially paid invoices; 22 goods-issued deliveries still unbilled. These exclusions matter: completed-only cycle and billed-only billing means can look better while unfinished work grows. On-time performance is 132/269 due promises, with overdue open orders counted as failures.

Synthetic invoice balances outstanding total £142,705.00; unmatched cash totals £3,060.00. These are model balances, not real cash or savings. Total order value includes cancelled demand; do not call it revenue. Results describe the generator, not NorthStar operations.

## Reproduce and inspect
Run `python scripts/build_data.py` from the project folder; it uses only Python's standard library. CSVs, SQLite database, results JSON, checks and SQL are generated. kpi_queries.sql independently computes the six measures in SQLite. 24 checks passed, including keys, references, date/quantity/amount bounds, known fixture and Python/SQL agreement. SHA-256 hashes in results.json make deterministic reruns comparable. These are executed data checks, not SAP UAT.

LibreOffice route: import each CSV with comma delimiter and UTF-8; retain identifiers as text. Use order_summary.csv as the order-grain table for pivots. It is an exported derived table; source CSV changes require regenerating it. For on-time calculations filter noncancelled known promises due by snapshot; count full receipt by original promise. For billing join invoices to deliveries once at delivery ID. Power BI is optional, not required.

## Dashboard design and implementation
The offline viewer shows six cohort-wide KPI cards, denominator/exclusion context, searchable orders with linked shipment/invoice/payment details, requirement traceability, tests and source evidence. Order-list search filters the list only; KPI cards stay clearly labelled as the full snapshot. No role permissions or transactional SAP behaviours are simulated by the viewer.

## Future-state scenario boundary
No future-state KPI uplift is presented. Phase 10 models illustrative handling-time capacity separately; it is not subtracted from this baseline or claimed as achieved.
