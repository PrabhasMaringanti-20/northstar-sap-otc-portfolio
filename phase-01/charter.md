# Phase 1 — Project charter

> Supersession note — 11 October 2026: the user authorized building all phases. This Phase 1 draft is retained as the starting charter. Current status and decisions are in ../registers/progress.md and ../registers/decisions.md. Public Edition 2602 is now the research reference. Initial “not started” and evidence-pending statements below describe 8 October, not the current artifact set.

Version 0.1 | 8 October 2026 | Independent simulation | Draft; learner review pending

## Executive summary

NorthStar Manufacturing UK is a fictional company selling stocked manufactured products to domestic business customers. The project examines poor order visibility, stock-related fulfilment delays and late billing caused by manual handoffs.

The work will describe the current process, investigate potential causes, define requirements and propose a future process informed by official SAP sources. Synthetic analysis and honest validation records will support a portfolio for junior Business Analyst, ERP Business Analyst and Process Analyst roles. The primary target role is unresolved.

Order-to-Cash means the journey from receiving a customer order through collecting and matching its payment. The project demonstrates analysis, not production readiness or an implemented transformation.

## Business problems

Problems are supplied scenario facts. Consequences and causes below are hypotheses, not observed findings.

| ID | Problem | Potential operational consequences | Evidence needed in a real business |
|---|---|---|---|
| PROB-001 | Poor order visibility | Repeated status enquiries; delayed orders overlooked; unclear ownership | Enquiry logs, order histories, ageing reports |
| PROB-002 | Stock-related fulfilment delays | Missed promises; partial deliveries; replanning effort | Stock commitments, promised dates, delivered quantities |
| PROB-003 | Late billing caused by manual handoffs | Dispatched orders wait for billing; payment period starts later | Dispatch evidence, posting timestamps, invoice dates, handoff records |

An overdue invoice is a symptom. Unclear billing ownership is a possible cause requiring evidence. Simulated discovery will not be presented as actual stakeholder research.

## Objectives and proposed business measures

| Objective | Candidate measures | Business target |
|---|---|---|
| Make order progress and exception ownership visible | Manual-touch rate; ability to identify open order status and owner | Unresolved |
| Improve stock-related fulfilment decisions | On-time delivery percentage; order fulfilment rate | Unresolved |
| Reduce avoidable billing delays | Billing cycle time | Unresolved |
| Improve order quality and flow | Order error rate; order cycle time | Unresolved |

KPI formulas, date bases, denominators and exclusions will be agreed before analysis. Targets require a baseline, customer commitments, capacity and cost assumptions. Synthetic results can inform illustrative targets but cannot establish real performance or achieved improvements.

## Scope

- One fictional company and one warehouse; GBP reporting currency.
- Domestic business customers buying stocked manufactured products.
- Customer order → sales order validation → availability check → fulfilment → delivery and goods issue → billing → payment allocation → reporting.
- Sales, Warehouse, Finance, Customer Service and IT stakeholders.
- Data quality, access permissions, auditability, reporting timeliness, usability and process ownership where relevant.
- Exceptions: missing/incorrect customer data; insufficient stock; partial delivery; credit/order block; order cancellation; incorrect invoice; partial/unmatched payment.

Excluded initially: manufacturing planning, procurement redesign, international trade, complex tax configuration, full migration and production deployment. Record dependencies rather than silently expanding scope. Basic invoice/tax-data needs remain relevant.

## Physical events and system postings

A physical event happens in the operation. A system posting records an event or its accounting consequences. Picking removes goods from storage; dispatch sends goods out of the warehouse; customer receipt occurs when the customer receives them. A goods-issue posting records an outbound stock movement in the system. Billing creates an invoice; payment allocation matches received money to an invoice or account.

These events can occur at different times. A goods-issue record alone does not prove customer receipt. Later KPI definitions must distinguish dispatch from receipt. These are introductory business definitions; exact SAP behaviour requires edition-specific verification.

## Stakeholder overview

These are proposed fictional responsibilities, not interviewed people or recorded approvals.

| Role | Proposed responsibility | Interest |
|---|---|---|
| Sales | Validate commercial order information; communicate delivery commitments | Reliable promises and straightforward processing |
| Warehouse | Pick, pack, dispatch and record fulfilment information | Clear priorities and accurate quantities |
| Finance | Credit-control policy, billing oversight and payment allocation | Correct invoices, controlled exposure and traceable payments |
| Customer Service | Status communication and coordination of customer exceptions | Consistent information and escalation routes |
| IT | Access, feasibility, integration and support assessment | Maintainable solutions |
| Learner as portfolio analyst | Produce, review and explain analysis and validation designs | Credible evidence of understanding |

Detailed billing ownership and handoff rules remain unresolved. No sponsor approval is claimed.

## Reference model and choices

Provisionally select SAP S/4HANA Cloud Public Edition to keep standard-process research within a defined product boundary. An edition identifies a product offering/operating model; a release identifies its version. The reference release is unresolved. If learner access uses another edition, assess whether to change the reference before making capability claims.

This selection is a learning decision, not an investment recommendation. No edition-specific capability has yet been verified or demonstrated. Record official SAP source URLs and actual access dates before using claims in the future-state design. Do not substitute another edition's documentation without flagging the difference.

Alternatives to assess later include improving manual controls, standardising the process, and an SAP-aligned future state. Prefer standard processes when they meet needs; justify any extension and its maintenance cost.

## Constraints, dependencies and unresolved choices

The user requires a free working route. No paid SAP environment, Office licence, course, domain or hosting is required. Use documentation and synthetic analysis, with free editing and analysis tools. See free-working-route.md for cost boundaries and evidence limitations.

See the linked [register](../registers/assumptions.md). SAP access, study time and primary target role are pending. Baselines, business targets, current tools, partial-delivery policy, delivery promises, billing ownership and payment exception rules remain provisional or unresolved.

## Portfolio completion criteria

- All three problems trace to relevant requirements, process changes and validation evidence.
- Normal flow and all seven exceptions are covered consistently across maps, stories and tests.
- SAP claims have official sources and access dates or explicit uncertainty; documentation and demonstrations are distinguished.
- Synthetic data relationships and KPI calculations are reproducible and checked.
- SAP test cases remain Not executed unless run; walkthrough issues are design issues, not executed SAP defects.
- Benefits and financial scenarios are labelled; capacity released is distinguished from cash savings.
- Resume claims match actual completed work; learner can explain key decisions and AI use.

These are portfolio criteria, separate from unachieved fictional business targets. Production readiness would require real discovery, configuration, integration, security assessment, system testing, business acceptance and operational preparation beyond this scope.

Deliverables and phase checkpoints appear in the [delivery plan](delivery-plan.md).
