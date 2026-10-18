# SAP reference and proposed TO-BE

Independent simulated portfolio · 2026-10-11 · AI-assisted draft; learner review pending.


## Reference boundary
Select SAP S/4HANA Cloud Public Edition **2602**, using the official release-specific feature scope document version 5.0 dated 11 June 2026. This is a stable research reference, not a claim to use the newest release or a live tenant. Public Edition suits a standard-first learning exercise; it is not free SAP hosting. Learning pages support concepts but are not pinned to 2602. Feature entitlement, country scope, activation and exact configuration require validation.

## Essential concepts
A business partner is the common customer identity with role-specific information (SAP-005). A sales order records the requested commercial transaction. Availability and scheduling help establish a feasible quantity/date; shelf stock alone is insufficient (SAP-002). An outbound delivery organizes shipping; partial-delivery rules need agreement (SAP-003). Goods issue records the outbound stock event, while physical dispatch and receipt are separately evidenced. Billing charges the customer and connects to receivables, the amount owed (SAP-001). Finance then handles payment matching and differences (SAP-006). No step has been demonstrated in an SAP system.

## Proposed process flowchart — not BPMN
```mermaid
flowchart TD
 A[Sales: capture draft order] --> B{Required data valid?}
 B -- No --> C[Sales: correct data / retain draft]
 C --> B
 B -- Yes --> D{Credit or order block?}
 D -- Yes --> E[Finance or block owner: review reason and authorization]
 E --> D
 D -- No --> F[Sales: check availability and scheduling]
 F --> G{Full feasible quantity?}
 G -- No --> H[Customer Service: agree partial or revised plan]
 H --> I{Partial permitted?}
 I -- No --> J[Sales: keep open / recheck supply / inform customer]
 J --> F
 I -- Yes --> K[Sales: record agreement and remaining demand]
 G -- Yes --> L[Sales: retain initial confirmed receipt date]
 K --> L
 L --> M[Warehouse: create delivery / pick authorized quantity]
 M --> N{Quantity matches actual pick?}
 N -- No --> O[Warehouse: resolve shortage / return to promise review]
 O --> H
 N -- Yes --> P[Warehouse: physical dispatch and distinct goods-issue posting]
 P --> Q[Customer Service: capture separate customer receipt evidence]
 P --> R[Finance: review billable/unbilled queue daily]
 R --> S{Billing-ready and not already charged?}
 S -- No --> T[Finance: own incomplete or posting/output exception]
 T --> R
 S -- Yes --> U[Finance: create invoice / verify accounting and output]
 U --> V{Invoice correct?}
 V -- No --> W[Finance: approved linked correction]
 W --> U
 V -- Yes --> X[Finance: receive and match payment]
 X --> Y{Full supported match?}
 Y -- No --> Z[Finance: partial/on-account balance and next action]
 Y -- Yes --> AA[Finance: verify clearing]
 Q --> AB[IT / Analyst: reconciled reporting with as-of time]
 Z --> AB
 AA --> AB
 A -. Cancellation request .-> AC{Already dispatched?}
 AC -- No --> AD[Sales: check dependencies / cancel unshipped demand]
 AC -- Yes --> AE[Finance / Warehouse: controlled return/reversal review]
 AD --> AB
 AE --> AB
```

## Ownership, controls and handoffs
Sales owns valid order/promise information; Customer Service records agreement and communication; Warehouse owns quantities and dispatch/posting evidence; Finance owns credit, billable-population reconciliation, corrections and allocation; IT supports roles, interfaces and reporting. A handoff is complete when the receiving role has a linked, actionable record or a named exception—not simply an email. RULE-001 through RULE-012 apply. PC-001 through PC-015 identify changes in traceability.csv.

The base NS-ORD-1001 remains unresolved: 100 ordered at £25, 60 physically on hand, requested receipt 9 October. A **separate design variant** assumes 60 are usable and the customer agrees: deliver/bill 60 (£1,500 net), keep 40 open; a £900 partial payment leaves £600 analytical exposure on that invoice. This is an illustration, not an executed order or the baseline record's actual history.

## Current vs proposed
| Current assumption | Proposed change | Why / alternative |
|---|---|---|
| Fragmented status lists | Linked order view with reason and owner | Standard views first; controlled shared register if fit unresolved |
| Shelf-stock promise | Availability/scheduling review and retained original promise | Manual checked promise can be an interim control |
| Informal split approval | Explicit permission, quantity and remainder | Complete delivery when customer does not agree |
| Dispatch-email billing trigger | Finance queue and daily reconciliation | Daily manual checklist is a credible low-cost option |
| Ad hoc payment matching | Supported allocation and visible unmatched queue | Keep on-account investigation; no forced write-off |

## Data needs beyond the analytical dataset
Customer identity/status and ship-to; product/UOM; quantity and price conditions; requested/initial confirmed dates; check time and block reasons; delivery references and authorized/actual quantities; dispatch/PGI/receipt timestamps; invoice/accounting/output status; corrections; receipt/allocation amounts; actor and change reason. The synthetic dataset is a deliberately smaller analytical model, not an SAP extraction schema or migration mapping.

Receipt capture may need a manual evidence field or carrier integration; this exact fit is unresolved. Returns/reversals, tax settings, replenishment, bank formats and retention policy are dependencies. Do not propose an extension until standard capture and export are tested. Official URLs and actual access date appear in sap-evidence.csv; two inaccessible Help pages are explicitly unverified.
