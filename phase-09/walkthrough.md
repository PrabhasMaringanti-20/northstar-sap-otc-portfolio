# Executed desk-based design walkthrough

Independent simulated portfolio · 2026-10-11 · AI-assisted draft; learner review pending.


Execution type: AI-assisted document/data walkthrough, 11 October 2026. No SAP interaction and no stakeholder participation.

| Walkthrough | Design observation | Resolution / status |
|---|---|---|
| TC-004/005: 100 ordered, 60 available | On-hand vs available wording can lead to unsupported promise | Base scenario stays unresolved; test variant explicitly assumes availability and permission |
| TC-011: dispatch Monday, posting Tuesday, receipt Wednesday | One delivery date would obscure service and posting lag | RULE-006 and dataset separate all three events |
| TC-014: £900 toward £1,500 | Analytical remaining balance could be mistaken for SAP invoice clearing | SAP-006 distinction and net-only model limitation added |
| TC-018: multiple deliveries and payments | Raw child joins multiply order values | Aggregate to order/invoice grain; independent SQL and fixture checks executed |
| TC-020/021: audit and usability | Offline viewer cannot prove production permissions or user task success | System controls and actual user review remain pending |

DI-001 (resolved design issue): date semantics needed separation. DI-002 (resolved design issue): payment model needed explicit distinction from SAP open-item postings. DI-003 (open design issue): full receipt-data capture and audit retention need tenant/policy validation. These are not executed SAP defects.
