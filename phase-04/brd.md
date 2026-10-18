# Concise business requirements document

Independent simulated portfolio · 2026-10-11 · AI-assisted draft; learner review pending.


## Business need
PROB-001: unclear order status. PROB-002: stock-related delays. PROB-003: billing handoff delays. The goal is controlled, visible processing, not buying SAP by default. Scope, exclusions and NS-ORD-1001 remain as in Phase 1. The source-labelled discovery is simulated; no real stakeholder acceptance exists.

## Business requirements
| ID | Type | Statement | Rationale | Source | Priority | Priority_reason | Acceptance | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BR-001 | Business | Enable accountable, traceable order and payment status from intake through allocation and reporting. | Reduce uncertainty and prevent lost exceptions. | PROB-001; SIM-CS-01; SIM-FIN-04 | Must | Core visibility problem | Representative normal, blocked, cancelled and partially paid cases expose current stage, owner, remaining quantity/balance and evidence gaps. | Master data; linked documents; agreed role access | Trace review and planned UAT TC-001;TC-014;TC-017 |
| BR-002 | Business | Base fulfilment commitments and release on feasible supply, customer agreement and financial controls. | Avoid unsupported promises and unauthorized shipments. | PROB-002; SIM-WH-01; SIM-FIN-01 | Must | Core fulfilment/control problem | Stock shortage, partial permission and block cases follow rules; measures KPI-001/002/003 use the agreed definitions; no achieved improvement claimed. | Stock accuracy; credit policy; transit assumptions | Planned UAT TC-004 through TC-008; synthetic KPI checks |
| BR-003 | Business | Make eligible fulfilled deliveries visible to Finance for timely, accurate and traceable billing. | Remove avoidable handoff waiting without billing incorrectly. | PROB-003; SIM-FIN-02; SIM-FIN-03 | Must | Core billing problem | Eligible delivery appears in review population without an email; correction/duplicate/error paths retain links and owner; KPI-004 includes unbilled context. | Posting accuracy; billing relevance; Finance ownership | Planned UAT TC-012;TC-013;TC-022 |

## Functional and non-functional scope
requirements.csv contains 3 business, 15 functional and 5 non-functional requirements with rationale, priority, acceptance, dependencies and validation. business-rules.csv defines 12 stable rules. traceability.csv connects every FR to problem → BR → process change → story → tests → KPI/control. nonfunctional-trace.csv adds NFR coverage. Access permissions are proposed in access-matrix.csv; the offline viewer has no production authorization enforcement.

Must = essential to a core flow/control; Should = useful with a controlled interim process. These priorities do not imply a committed sprint. Thresholds follow business need: exact key/balance reconciliation, zero unauthorized releases in a test set, daily management review freshness, and formative usability by role. No arbitrary speed or improvement target is treated as agreed.

## Requirement review decisions
“Real-time visibility” was narrowed to named status fields and a stated refresh time; real-time integration lacks evidence of need. “Automatic billing” was narrowed to complete billable-population review and controlled invoice creation, including failures. “All stock is available” was rejected because commitments and restrictions matter. “Clear every payment automatically” was rejected because unidentified cash needs investigation.

## Unresolved items and change control
Retention period, exact SAP role restrictions, carrier receipt capture, correction method, duplicate customer PO policy and refresh architecture need validation. A duplicate customer-PO control is a discovery question, not silently added to the approved scope. Proposed changes must record source, rationale and impacts on process, rules, stories, tests and KPI definitions. No actual approval has been recorded.
