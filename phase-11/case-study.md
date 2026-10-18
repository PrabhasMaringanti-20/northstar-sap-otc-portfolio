# Case study and lessons learned

Independent simulated portfolio · 2026-10-11 · AI-assisted draft; learner review pending.


## Context
Independent simulated analysis of NorthStar Manufacturing UK, a one-company, one-warehouse domestic stock seller. Supplied problems: poor visibility, stock delays and manual billing handoffs. The learner's quality-review and error-analysis background motivates attention to controls and evidence; no real client engagement is claimed.

## Analysis and decisions
The pack uses explicitly invented discovery to explore conflicting promises, partial deliveries, credit and billing ownership. AS-IS and TO-BE flowcharts distinguish physical events from postings. Three business requirements decompose into 15 functional and five non-functional requirements, 15 stories and 22 planned UAT cases. Traceability links problems, process changes, tests and measures. Official SAP references support broad standard-process fit; exact configuration and several controls remain unresolved.

The main decisions were to preserve the original promise date, require partial-delivery agreement, assign Finance the billable-population review, distinguish partial payment from clearing, and aggregate child records before combining measures. Standard processes and manual controls were considered before extensions.

## Evidence produced
The reproducible dataset contains 300 synthetic orders, 285 shipments, 262 invoices and 197 allocations. Six KPI calculations agree between Python and SQLite; 24 data checks passed. The offline viewer exposes results and records but is not an SAP application. All 22 SAP UAT cases remain Not executed.

## Limitations and next steps
No real stakeholder research, tenant demonstration, implementation or measured savings. Data is simplified to one line per order and net-only finances; it omits corrections, VAT and returns. A real project needs agreed policies, broader representative data, configuration/integration/security testing and business acceptance. Learner understanding and personal contribution still need review before resume use.

## Lessons from building the pack
An attractive dashboard is not evidence of a sound denominator. Posted goods issue is not proof of receipt. A plausible root cause is still a hypothesis. A linked analytical payment amount is not the same as an SAP clearing document. A generated test list is not executed UAT. These are artifact-development observations, not retrospective lessons from a live implementation.
