# Truthful resume and interview preparation

Independent simulated portfolio · 2026-10-11 · AI-assisted draft; learner review pending.


## Contribution check — required before using personal claims
The artifacts and automated analyses were produced with AI assistance. The learner has not yet supplied review answers or demonstrated independent reproduction. Therefore the statements below are **project-description drafts**, not approved personal achievement claims. Use “I analysed/designed/tested” only after personally performing and explaining the relevant work.

## Four evidence-supported project-description bullets
- Independent simulated SAP S/4HANA Order-to-Cash portfolio covering a fictional UK manufacturer, with current/future process flows and a source-labelled SAP reference assessment.
- Portfolio includes 23 requirements, 15 user stories and 22 planned UAT cases linked through traceability; SAP test cases are labelled Not executed.
- Reproducible analysis covers 300 synthetic orders and six KPIs, with separate order, delivery, invoice and payment-allocation grains and Python/SQLite reconciliation.
- Compares manual-control, process-standardisation and SAP-aligned options using illustrative costs and capacity assumptions, without claiming achieved savings.

## 60-second overview to adapt truthfully
“My portfolio is an independent simulation of Order-to-Cash at a fictional UK manufacturer. It focuses on order visibility, stock delays and billing handoffs. The pack connects discovery assumptions to process changes, requirements, stories and planned tests. It uses official SAP Public Edition sources as a reference, not a live implementation. A 300-order synthetic dataset demonstrates six KPIs and the importance of avoiding duplicate values across shipments and payments. AI helped draft and generate the artifacts; my personal contribution so far is [state only work actually completed]. I am working through the decisions and checks so I can explain them independently. All SAP UAT cases remain unexecuted.”

## Five-minute walkthrough
0:00–0:45: scenario, supplied problems and evidence boundary. 0:45–1:30: NS-ORD-1001 and on-hand versus available stock. 1:30–2:15: AS-IS hypothesis and TO-BE ownership. 2:15–3:00: FR-004 → US-004 → TC-005/006 → KPI-003. 3:00–4:00: dataset grains, original-promise denominator and executed checks. 4:00–4:40: desk-based SAP fit, unexecuted UAT and option comparison. 4:40–5:00: personal contribution, limitations and next validation step.

## Interview questions and challenges
1. BA: How would you turn “poor visibility” into a requirement? Follow-up: which role, fields and freshness matter? Strong answer names observable outcomes and evidence.
2. Discovery: Sales wants Friday delivery, Warehouse cannot confirm. What do you do? Follow-up: how do you distinguish request, estimate and commitment?
3. Process: What proves the customer received the goods? Follow-up: what if dispatch and posting occur on different dates?
4. SAP: Why choose Public Edition as a reference? Follow-up: which exact claims still require tenant verification?
5. Controls: Who can release credit and why? Follow-up: what if a separate order block remains?
6. Requirements: Give a negative acceptance criterion for partial delivery. Follow-up: what happens to the remaining quantity?
7. Data: How can a join inflate order value? Follow-up: show the grain before and after aggregation.
8. KPI: Should an open overdue order be excluded from on-time delivery? Follow-up: why retain the original promise date?
9. UAT: Can TC-018 be Passed because Python checks passed? Follow-up: what evidence would a system test require?
10. Finance: Does a partial payment clear the original invoice? Follow-up: contrast partial and residual treatment using SAP-006.
11. Business case: Are 500 saved hours £12,500 cash savings? Follow-up: what decision would make cash benefits real?
12. Integrity: What did you do and what did AI do? Follow-up: reproduce one calculation without relying on the generated explanation.

## Coaching rubric
For each answer record 0 = incorrect/no explanation, 1 = partial, 2 = correct with example and limitation. Do not assign scores before answers exist. Re-teach stock availability, event dates, grain or test status if confused. Readiness requires explaining the main decisions without a script, not memorizing every file. Employment is not guaranteed.
