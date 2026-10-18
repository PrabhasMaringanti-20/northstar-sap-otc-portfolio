"""Generate portfolio documents and catalogues from authored simulation content."""
from pathlib import Path
import csv,json
from project_catalog import DATE,EVIDENCE,SPECS,RULES,NF,TESTS,RISKS,MENTOR
ROOT=Path(__file__).resolve().parents[1]
def write(path,text):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def table(rows):
    if not rows:return ''
    keys=list(rows[0]);return '\n'.join(['| '+' | '.join(keys)+' |','| '+' | '.join('---' for _ in keys)+' |']+['| '+' | '.join(str(r[k]).replace('|','/').replace('\n','; ') for k in keys)+' |' for r in rows])
def catalog(path,rows):
    with (ROOT/path).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def doc(path,title,body):write(path,f'# {title}\n\nIndependent simulated portfolio · {DATE} · AI-assisted draft; learner review pending.\n\n{body}')

stakeholders=[
dict(Role='Sales',Responsibility='Order capture, validation, commercial promise',Interest='Fast acceptance and customer retention',Influence='High: controls promises',Concern='Checks may slow response',Engagement='Review incomplete/short-stock examples and promise rules'),
dict(Role='Warehouse',Responsibility='Stock accuracy, picking, dispatch and posting evidence',Interest='Feasible priorities and correct quantities',Influence='High: controls fulfilment',Concern='Sales promises exceed usable stock',Engagement='Walk shortages, split deliveries and event recording'),
dict(Role='Finance',Responsibility='Credit, billing, receivables and controls',Interest='Accurate charges and supported clearing',Influence='High: financial control owner',Concern='Pressure to bypass blocks; late handoffs',Engagement='Review authorization, billing and payment scenarios'),
dict(Role='Customer Service',Responsibility='Status communication and exception coordination',Interest='Reliable answers and named owner',Influence='Medium: customer voice',Concern='Conflicting statuses and partial shipments',Engagement='Walk customer enquiry and delivery-agreement cases'),
dict(Role='IT',Responsibility='Feasibility, roles, integration and reporting support',Interest='Standard, maintainable design',Influence='High: technical feasibility',Concern='Custom dashboard scope and unverified integrations',Engagement='Evidence-led fit review and data contract checks'),
]
catalog('phase-02/stakeholders.csv',stakeholders)
findings=[
('SIM-SALES-01','Sales','We sometimes learn about missing delivery details only when Warehouse asks.','Validation responsibility and required fields need definition.','PROB-001'),
('SIM-SALES-02','Sales','Customers cancel, but we cannot always tell whether the order has already shipped.','Cancellation must check downstream state.','PROB-001'),
('SIM-WH-01','Warehouse','A shelf quantity is not a reliable promise if stock is already committed.','Availability and lead times must precede confirmation.','PROB-002'),
('SIM-WH-02','Warehouse','Dispatch paperwork and the recorded stock movement do not always happen together.','Keep physical and posting dates separate.','PROB-002'),
('SIM-CS-01','Customer Service','I ask several teams before I can explain a delay.','An order view and accountable exception owner are needed.','PROB-001'),
('SIM-CS-02','Customer Service','Some customers need part of an order urgently; others reject split shipments.','Record partial-delivery agreement; do not assume one rule for everyone.','PROB-002'),
('SIM-FIN-01','Finance','Sales wants to release held orders, but Finance must own credit decisions.','Separate request and approval responsibilities.','PROB-002'),
('SIM-FIN-02','Finance','We wait for dispatch emails before reviewing what should be billed.','Reconcile goods-issued deliveries with billing queue daily.','PROB-003'),
('SIM-FIN-03','Finance','We need to explain price corrections without losing the first invoice.','Linked correction records are needed.','PROB-003'),
('SIM-FIN-04','Finance','A receipt can be short or lack a usable invoice reference.','Retain partial and unallocated amounts.','PROB-001'),
('SIM-IT-01','IT','Joining several document lists may duplicate values; custom screens need a clear purpose.','Agree grains, freshness and standard-first fit.','PROB-001'),
]
catalog('phase-02/discovery-findings.csv',[dict(Source=s,Role=r,Role_play_statement=q,Finding=f,Problem=p,Evidence_status='Invented role-play; no interview conducted') for s,r,q,f,p in findings])
doc('phase-02/discovery.md','Stakeholders and simulated discovery',f'''
## Purpose and boundary
Find the business need behind each complaint and identify whose policy decisions conflict. All dialogue below is invented role-play, created to practise discovery. There were no stakeholder interviews, workshops, attendance records or approvals.

{table(stakeholders)}

## Interview guide to use in a real discovery

Sales: Walk through the last incomplete order. Which fields were missing, where were they captured and what proved correction? What evidence supports your delivery promise? How do you recognize a duplicate customer purchase order? When can cancellation safely stop fulfilment?

Warehouse: Show how usable stock differs from shelf quantity. What happens when picking finds fewer units? How do you authorize split shipments? Who records dispatch, goods issue and receipt evidence, and how are timing differences reconciled?

Finance: What triggers a credit block and who may release it? What proves a delivery is billable? How do you identify missed or duplicate charges? What distinguishes invoice creation, accounting posting and successful customer output? How do you handle short or unidentified receipts?

Customer Service: What information is needed to answer an order enquiry? Which status is authoritative? How is consent to split shipment recorded? How do you escalate an overdue response and notify the customer without promising an unsupported date?

For every answer ask for an example, record, frequency and contrary case. Do not turn an opinion into a quantified baseline.

## Role-play workshop — proposed 60-minute agenda
10 minutes: agree boundaries and terminology. 20: walk NS-ORD-1001. 15: debate policy conflicts. 10: agree provisional requirements. 5: list evidence gaps. This agenda has not been run with people.

Sales: “Can we promise all 100 for Friday so the customer stays with us?” Warehouse: “Only 60 are on hand; we have not checked commitments.” Customer Service: “I could ask whether 60 helps, but I need a defensible date for the rest.” Finance: “Agreement to split does not remove a credit hold.” IT: “First confirm the rules; do not commission a custom promise engine.”

Later, Warehouse says billing belongs to Finance once goods leave. Finance says a dispatch email is still needed. The analyst proposes that Warehouse owns accurate dispatch/posting evidence and Finance owns a daily billable/unbilled review. Neither team can treat the handoff as complete solely because an email was sent. This is a proposed resolution, not approval.

## Conflicts and proposed resolutions
| Conflict | Proposed resolution | Alternative and trade-off | Decision owner |
|---|---|---|---|
| Fast promise vs feasible supply | Confirm only supported quantity/date; explain shortfall | Provisional estimate can be communicated if clearly unconfirmed | Sales with Warehouse |
| Urgent partial vs single complete shipment | Explicit agreement and cost awareness; retain remainder | Wait for all stock: lower handling effort, potentially worse service | Customer Service with Sales |
| Sales urgency vs credit control | Finance decides credit release; Sales requests review | Blanket override is rejected because it removes control | Finance |
| Billing ownership ambiguity | Warehouse owns fulfilment evidence; Finance owns billing queue and reconciliation | Email checklist is a low-cost interim control | Finance |

## Findings
See discovery-findings.csv for the 11 linked simulated sources. None establish actual frequency or impact. Validate proposed policies with real role owners before implementation.
''')
raci=[]
for task,owner,consult in [('Customer/order validation','Sales','Customer Service;Finance'),('Promise and partial agreement','Sales','Warehouse;Customer Service'),('Credit release','Finance','Sales'),('Dispatch and goods issue','Warehouse','Sales;Finance'),('Billing and corrections','Finance','Warehouse;Customer Service'),('Payment allocation','Finance','Customer Service'),('Customer exception communication','Customer Service','Sales;Warehouse;Finance'),('Role/report configuration','IT','Finance;Sales;Warehouse;Customer Service')]:
    raci.append(dict(Activity=task,**{r:('A/R' if r==owner else 'C' if r in consult.split(';') else 'I') for r in ['Sales','Warehouse','Finance','Customer Service','IT']}))
catalog('phase-02/responsibility-matrix.csv',raci)
doc('phase-02/responsibilities.md','Proposed responsibility matrix','A = accountable for the outcome; R = performs work; C = consulted; I = informed. One accountable role per activity. A/R combines responsibility for this small-company simulation, not every named employee. Credit request and release must remain separated.\n\n'+table(raci))

steps=[
('AS-01','Sales','Customer email/order','Recorded request','Email and order spreadsheet','Check customer reference manually','Details rekeyed','No agreed required-field checklist','Original request vs entered fields','Corrections and repeated contact'),
('AS-02','Sales / Finance','Recorded request','Validated or held order','Spreadsheet and messages','Check customer, price and credit by request','Hold reason not shared','Different teams keep separate lists','Rejected orders and hold logs','Unclear release ownership'),
('AS-03','Sales / Warehouse','Validated demand','Informal promise or shortage query','Stock sheet and calls','Ask about stock before picking','Shelf count mistaken for available stock','Commitments and lead times not visible','Stock snapshot and concurrent commitments','Unreliable date promise'),
('AS-04','Warehouse / Customer Service','Pick request','Picked goods or partial decision','Paper pick list and email','Seek agreement for short shipment','Partial permission hard to find','Agreement not attached to order','Customer correspondence and pick quantities','Repeat handling or customer rejection'),
('AS-05','Warehouse','Picked goods','Dispatch note and stock movement entry','Paper note and stock workbook','Record actual quantity and movement','Physical event and entry occur at different times','Batch updates or missing owner','Dispatch log vs entry timestamps','Status/stock mismatch'),
('AS-06','Finance','Dispatch email','Invoice or unresolved item','Standalone billing spreadsheet/tool','Check price/quantity before sending','Dispatch email awaited','No complete billable population reconciliation','Dispatched vs invoiced lists','Late billing'),
('AS-07','Finance','Bank receipt and remittance','Allocation or unmatched balance','Bank file and receivables sheet','Match customer/reference/amount','Short payment handling inconsistent','No agreed partial/unmatched policy','Bank records and allocation history','Misstated open balances'),
('AS-08','Customer Service / IT','Departmental lists','Order/KPI report','Excel consolidation','Reconcile lists manually','Different totals and stale status','One-to-many joins and inconsistent dates','Source extracts and formula review','Poor operational decisions'),
]
catalog('phase-03/as-is-step-register.csv',[dict(Step=a,Owner=b,Input=c,Output=d,Tool=e,Rule_control=f,Pain_point=g,Potential_cause=h,Evidence_required=i,Consequence=j,Evidence_status='Fictional process assumption; not observed') for a,b,c,d,e,f,g,h,i,j in steps])
asis='''flowchart TD
 A[Sales: receive customer order] --> B{Data and price correct?}
 B -- No --> C[Sales: request correction / retain draft]
 C --> B
 B -- Yes --> D{Finance: credit or order block?}
 D -- Yes --> E[Responsible owner reviews / no dispatch]
 E --> D
 D -- No --> F[Sales asks Warehouse about stock]
 F --> G{Enough stock?}
 G -- No --> H{Customer agrees partial?}
 H -- No --> I[Sales: wait / revise promise]
 I --> F
 H -- Yes --> J[Warehouse: pick permitted quantity / remainder open]
 G -- Yes --> J
 J --> K[Warehouse: dispatch physically]
 K --> L[Warehouse: enter stock movement and email Finance]
 L --> M[Finance waits for handoff and creates invoice]
 M --> N{Invoice correct?}
 N -- No --> O[Finance: review linked correction]
 O --> M
 N -- Yes --> P[Finance receives payment]
 P --> Q{Full supported match?}
 Q -- No --> R[Finance: partial or unmatched balance review]
 R --> S[Customer Service / IT consolidate reporting]
 Q -- Yes --> S
 A -. Cancellation request .-> T{Already dispatched?}
 T -- No --> U[Sales checks dependencies and stops demand]
 T -- Yes --> V[Finance / Warehouse: return or reversal review]
 U --> S
 V --> S
'''
write('phase-03/as-is.mmd',asis)
doc('phase-03/current-state.md','AS-IS process and root-cause hypotheses',f'''
This is a **process flowchart, not BPMN**. Tools and responsibilities are fictional current-state assumptions. Shared owner labels show uncertain handoffs that the TO-BE must resolve.

```mermaid
{asis}```

The full eight-step register is in as-is-step-register.csv. Cancellation after dispatch is an exception routed to controlled review, not a full returns redesign. Unmatched and partial payments remain visible rather than pretending the order is financially complete.

## Five Whys — late billing hypothesis
1. Why is billing late? A dispatched delivery is absent from the billing review list.
2. Why absent? Finance has not received or located the handoff email.
3. Why does that matter? The email is treated as the trigger instead of reconciling all eligible deliveries.
4. Why is reconciliation absent? Ownership of the complete billable population is unclear.
5. Why unclear? The cross-team procedure defines individual tasks but no accountable handoff outcome.

This chain is a hypothesis, not a root cause proven by five repetitions. Alternative explanations include pricing incompleteness, goods-issue timing, invoice schedules or accounting blocks. Compare dispatch, posting, invoice and output dates plus exception reasons before attributing delay. A missing receipt timestamp can be an evidence gap rather than a late physical delivery.

## Root-cause test plan
| Hypothesis | Evidence that supports it | Evidence that could refute it | Proposed response |
|---|---|---|---|
| Fragmented status causes enquiries | Enquiry timestamps coincide with inconsistent team records | Accurate shared records exist but users cannot locate them | Shared definitions or usability training depending on evidence |
| Promise ignores commitments | Orders promised beyond usable stock at confirmation | Stock was sufficient but damaged during picking | Availability review or warehouse control depending on cause |
| Email handoff delays billing | Eligible items wait until email arrives | Items were blocked for pricing despite timely email | Queue ownership or pricing correction depending on cause |
''')

business=[
dict(ID='BR-001',Type='Business',Statement='Enable accountable, traceable order and payment status from intake through allocation and reporting.',Rationale='Reduce uncertainty and prevent lost exceptions.',Source='PROB-001; SIM-CS-01; SIM-FIN-04',Priority='Must',Priority_reason='Core visibility problem',Acceptance='Representative normal, blocked, cancelled and partially paid cases expose current stage, owner, remaining quantity/balance and evidence gaps.',Dependencies='Master data; linked documents; agreed role access',Validation='Trace review and planned UAT TC-001;TC-014;TC-017'),
dict(ID='BR-002',Type='Business',Statement='Base fulfilment commitments and release on feasible supply, customer agreement and financial controls.',Rationale='Avoid unsupported promises and unauthorized shipments.',Source='PROB-002; SIM-WH-01; SIM-FIN-01',Priority='Must',Priority_reason='Core fulfilment/control problem',Acceptance='Stock shortage, partial permission and block cases follow rules; measures KPI-001/002/003 use the agreed definitions; no achieved improvement claimed.',Dependencies='Stock accuracy; credit policy; transit assumptions',Validation='Planned UAT TC-004 through TC-008; synthetic KPI checks'),
dict(ID='BR-003',Type='Business',Statement='Make eligible fulfilled deliveries visible to Finance for timely, accurate and traceable billing.',Rationale='Remove avoidable handoff waiting without billing incorrectly.',Source='PROB-003; SIM-FIN-02; SIM-FIN-03',Priority='Must',Priority_reason='Core billing problem',Acceptance='Eligible delivery appears in review population without an email; correction/duplicate/error paths retain links and owner; KPI-004 includes unbilled context.',Dependencies='Posting accuracy; billing relevance; Finance ownership',Validation='Planned UAT TC-012;TC-013;TC-022'),
]
requirements=list(business);stories=[];trace=[];fits=[]
for n,cap,role,br,prob,pc,kpi,rule,source,need,ac,dep,exc,fit,sap in SPECS:
    fr=f'FR-{n:03}';us=f'US-{n:03}'
    tests=';'.join(f'TC-{t[0]:03}' for t in TESTS if n in t[1])
    priority='Should' if n in [12,15] else 'Must'
    requirements.append(dict(ID=fr,Type='Functional',Statement=f'The proposed process/solution shall {need}.',Rationale=f'{cap} addresses {prob} and supports {br}.',Source=source+' (role-play)',Priority=priority,Priority_reason='Control or essential end-to-end capability' if priority=='Must' else 'Supports operation; interim documented control possible',Acceptance=ac,Dependencies=dep+'; '+rule,Validation='Design walkthrough; planned SAP tests '+tests))
    case=next((t for t in TESTS if n in t[1] and t[0]!=1),next(t for t in TESTS if n in t[1]))
    stories.append(dict(ID=us,Capability=cap,Requirement=fr,Role=role,Story=f'As {role}, I need to {need}, so that {br} is supported.',Business_value=next(b['Rationale'] for b in business if b['ID']==br),Given=case[3]+'; authorized role and relevant policy available.',When=case[4],Then=ac,Additional_exception_outcome=case[5],Priority=priority,Dependencies=dep,Exceptions=exc,Tests=tests,Status='Proposed; not implemented in SAP'))
    trace.append(dict(Problem=prob,Business_requirement=br,Requirement=fr,Process_change=pc,Process_change_description=cap,Story=us,Tests=tests,KPI=kpi or 'Control evidence; no direct KPI',Rule=rule))
    resolution={'Supported in principle':'Use documented standard approach; demonstrate exact policy in a configured practice tenant before acceptance.', 'Process/configuration change':'Define policy and demonstrate standard configuration first; do not assume default settings meet acceptance criteria.', 'Integration/extension candidate':'Try standard capture/export first; assess an integration only if the needed evidence cannot be captured reliably.', 'Unresolved':'Run a focused standard-process demonstration against acceptance criteria; retain controlled manual procedure pending evidence.'}[fit]
    fits.append(dict(Requirement=fr,Required_capability=need,Standard_evidence=sap or 'No verified exact capability source',Assessment=fit,Business_impact=cap+' affects '+prob,Proposed_resolution=resolution,Alternative='Documented manual control; standard view/export before custom development',Dependencies=dep,Validation_remaining=ac,Assessment_type='Desk-based; no system demonstration'))
for ident,cap,ac,source,priority,reason,dep,val in NF:
    requirements.append(dict(ID=ident,Type='Non-functional',Statement=cap+' shall meet the stated acceptance condition.',Rationale=reason,Source=source+' role-play/control analysis',Priority=priority,Priority_reason=reason,Acceptance=ac,Dependencies=dep,Validation=val))
catalog('phase-04/requirements.csv',requirements)
catalog('phase-04/business-rules.csv',[dict(ID=i,Rule=r,Owner=o,Rationale=s,Status='Proposed simulation policy') for i,r,o,s in RULES])
catalog('phase-07/backlog.csv',stories);catalog('phase-04/traceability.csv',trace);catalog('phase-06/fit-gap.csv',fits)
nonfunc_links=[('NFR-001','FR-014','TC-007;TC-008;TC-019'),('NFR-002','FR-015','TC-020'),('NFR-003','FR-015','TC-020'),('NFR-004','FR-015','TC-021'),('NFR-005','FR-013','TC-018')]
catalog('phase-04/nonfunctional-trace.csv',[dict(Requirement=n,Functional_anchor=f,Story='US-'+f[3:],Tests=t,Validation_status='SAP not executed; NFR-005 synthetic subset executed') for n,f,t in nonfunc_links])
access=[]
for action,allowed in [('View operational status',['Sales','Warehouse','Finance','Customer Service']),('Confirm commercial promise',['Sales']),('Request credit release',['Sales','Customer Service']),('Approve credit release',['Finance']),('Post goods issue',['Warehouse']),('Create/correct invoice',['Finance']),('Allocate payment',['Finance']),('Change access configuration',['IT'])]:
    access.append(dict(Action=action,**{r:'Allow' if r in allowed else 'Deny' for r in ['Sales','Warehouse','Finance','Customer Service','IT']}))
catalog('phase-04/access-matrix.csv',access)
doc('phase-04/brd.md','Concise business requirements document',f'''
## Business need
PROB-001: unclear order status. PROB-002: stock-related delays. PROB-003: billing handoff delays. The goal is controlled, visible processing, not buying SAP by default. Scope, exclusions and NS-ORD-1001 remain as in Phase 1. The source-labelled discovery is simulated; no real stakeholder acceptance exists.

## Business requirements
{table(business)}

## Functional and non-functional scope
requirements.csv contains 3 business, 15 functional and 5 non-functional requirements with rationale, priority, acceptance, dependencies and validation. business-rules.csv defines 12 stable rules. traceability.csv connects every FR to problem → BR → process change → story → tests → KPI/control. nonfunctional-trace.csv adds NFR coverage. Access permissions are proposed in access-matrix.csv; the offline viewer has no production authorization enforcement.

Must = essential to a core flow/control; Should = useful with a controlled interim process. These priorities do not imply a committed sprint. Thresholds follow business need: exact key/balance reconciliation, zero unauthorized releases in a test set, daily management review freshness, and formative usability by role. No arbitrary speed or improvement target is treated as agreed.

## Requirement review decisions
“Real-time visibility” was narrowed to named status fields and a stated refresh time; real-time integration lacks evidence of need. “Automatic billing” was narrowed to complete billable-population review and controlled invoice creation, including failures. “All stock is available” was rejected because commitments and restrictions matter. “Clear every payment automatically” was rejected because unidentified cash needs investigation.

## Unresolved items and change control
Retention period, exact SAP role restrictions, carrier receipt capture, correction method, duplicate customer PO policy and refresh architecture need validation. A duplicate customer-PO control is a discovery question, not silently added to the approved scope. Proposed changes must record source, rationale and impacts on process, rules, stories, tests and KPI definitions. No actual approval has been recorded.
''')

tobe='''flowchart TD
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
'''
write('phase-05/to-be.mmd',tobe)
evidence=[dict(ID=e['id'],Title=e['title'],URL=e['url'],Access_date=DATE,Edition='SAP S/4HANA Cloud Public Edition',Release='2602 reference; learning pages unpinned' if e['id']!='SAP-007' else '2602, document v5.0 / 2026-06-11',Claim=e['claim'],Locator=e['locator'],Verification=e['status'],Limit=e['limit'],System_demonstration='None') for e in EVIDENCE]
catalog('phase-05/sap-evidence.csv',evidence)
doc('phase-05/future-state.md','SAP reference and proposed TO-BE',f'''
## Reference boundary
Select SAP S/4HANA Cloud Public Edition **2602**, using the official release-specific feature scope document version 5.0 dated 11 June 2026. This is a stable research reference, not a claim to use the newest release or a live tenant. Public Edition suits a standard-first learning exercise; it is not free SAP hosting. Learning pages support concepts but are not pinned to 2602. Feature entitlement, country scope, activation and exact configuration require validation.

## Essential concepts
A business partner is the common customer identity with role-specific information (SAP-005). A sales order records the requested commercial transaction. Availability and scheduling help establish a feasible quantity/date; shelf stock alone is insufficient (SAP-002). An outbound delivery organizes shipping; partial-delivery rules need agreement (SAP-003). Goods issue records the outbound stock event, while physical dispatch and receipt are separately evidenced. Billing charges the customer and connects to receivables, the amount owed (SAP-001). Finance then handles payment matching and differences (SAP-006). No step has been demonstrated in an SAP system.

## Proposed process flowchart — not BPMN
```mermaid
{tobe}```

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
''')
doc('phase-06/assessment.md','Desk-based fit-to-standard assessment','''
fit-gap.csv covers all 15 functional requirements. Supported in principle means relevant standard concepts exist, not that all acceptance criteria are satisfied. Process/configuration change means policy and settings must be demonstrated. Integration/extension candidate means investigate standard capture first. Unresolved means evidence is insufficient.

NFR assessment: NFR-001 uses broad role capability SAP-007 but exact segregation is unvalidated; NFR-002 audit field coverage/retention unresolved; NFR-003 refresh architecture unresolved; NFR-004 requires real users; NFR-005 is demonstrated only on the synthetic data subset. No SAP system acceptance is claimed.

Prioritise demos for blocked release, partial delivery, invoice retries/corrections and event-level receipt capture. An external receipt feed could require interface monitoring, retries, security, data mapping and release regression testing. A custom exception view also creates maintenance and access-control obligations. Prefer a standard report plus a controlled exception register until an evidenced gap justifies more.

The locally built portfolio viewer is a learning presentation, not a proposed SAP production extension or proof of FR implementation.
''')
doc('phase-07/backlog.md','Focused product backlog','''
backlog.csv contains 15 substantive proposed stories grouped by capability. Each names a role, business value, linked requirement, Given/When/Then criteria, priority, dependencies and exception coverage. Specific fixtures and actions are in the linked UAT cases rather than duplicating long steps in each story.

Suggested sequencing: US-001/003/005/014 establish input and controls; US-004/006/007 handle fulfilment and cancellation; US-008/009/010 handle billing; US-011 covers receipts; US-002/012/013/015 depend on reliable linked information. This is dependency reasoning, not a sprint commitment. No velocity or delivered SAP increment is claimed.

Analysis tasks are separate: AT-001 verify exact credit-release roles; AT-002 define correction route; AT-003 validate receipt capture; AT-004 test reporting extraction/grain; AT-005 conduct actual usability review. They are evidence-gathering tasks, not user-facing product stories.
''')

tests=[]
for num,frs,title,data,actions,expected in TESTS:
    linked=[f'FR-{n:03}' for n in frs]+[n for n,_,ts in nonfunc_links if f'TC-{num:03}' in ts.split(';')]
    pre='Configured non-production Public Edition reference process; valid synthetic customer/product and named role; relevant rules/authorizations and resettable test state available.'
    if num in [18,21]:pre='Agreed KPI definitions and fixture data available.' if num==18 else 'Five consenting role representatives and a usable practice system available; no participants recruited.'
    tests.append(dict(ID=f'TC-{num:03}',Requirements=';'.join(linked),Scenario=title,Purpose='Validate '+', '.join(f'FR-{n:03}' for n in frs)+' including negative/exception behaviour',Preconditions=pre,Test_data=data,Steps='; '.join(f'{i+1}. {s.strip()}' for i,s in enumerate(actions.split(';'))),Expected_results=expected,Actual_results='Not run in SAP',Status='Not executed',Evidence_reference='None — design only',Defect_reference='None',Execution_type='Planned SAP UAT / business acceptance'))
catalog('phase-09/uat-cases.csv',tests)
doc('phase-09/uat-plan.md','UAT plan and honest validation status','''
## Purpose
User acceptance testing checks whether business users can meet agreed needs in the configured solution. A requirements walkthrough checks the design. Executing a spreadsheet or data script does not execute SAP UAT.

## Entry criteria
Reviewed requirements/rules and traceability; known release/configuration and scope; non-production tenant; authorized test roles; controlled synthetic master/transaction data; reset approach; approved expected results; evidence storage and agreed severity. These entry conditions have not been met for SAP execution.

## Exit criteria for a future SAP test cycle
All Must scenarios executed with evidence; no open critical/high issue preventing safe order, financial or access processing; medium/low residual issues explicitly accepted by accountable owners with workarounds; regression/coverage reviewed; actual business acceptance recorded. No fabricated approval or acceptance is supplied here.

## Severity
Critical: unauthorized financial release, severe data corruption or widespread inability to operate safely. High: core flow blocked or materially wrong quantity/value without safe workaround. Medium: restricted scenario affected with a controlled workaround. Low: cosmetic/help issue without material processing impact. Priority is how soon to fix, based on business timing and impact; it is not automatically identical to severity.

## Execution records
All 22 cases in uat-cases.csv remain **Not executed**. No SAP defects or screenshots exist. Synthetic data and KPI checks are separately recorded in phase-08/data/data_checks.csv. The fixture oracle exercises analytical logic related to TC-018 but does not change its SAP status. Document reviews are recorded in walkthrough.md as design issues.

For later execution, save actual inputs, time, user role, relevant document IDs, observed result and evidence path. If blocked before the action, mark Blocked with reason—not Passed. Do not use generated concept artwork as evidence.
''')
doc('phase-09/walkthrough.md','Executed desk-based design walkthrough','''
Execution type: AI-assisted document/data walkthrough, 11 October 2026. No SAP interaction and no stakeholder participation.

| Walkthrough | Design observation | Resolution / status |
|---|---|---|
| TC-004/005: 100 ordered, 60 available | On-hand vs available wording can lead to unsupported promise | Base scenario stays unresolved; test variant explicitly assumes availability and permission |
| TC-011: dispatch Monday, posting Tuesday, receipt Wednesday | One delivery date would obscure service and posting lag | RULE-006 and dataset separate all three events |
| TC-014: £900 toward £1,500 | Analytical remaining balance could be mistaken for SAP invoice clearing | SAP-006 distinction and net-only model limitation added |
| TC-018: multiple deliveries and payments | Raw child joins multiply order values | Aggregate to order/invoice grain; independent SQL and fixture checks executed |
| TC-020/021: audit and usability | Offline viewer cannot prove production permissions or user task success | System controls and actual user review remain pending |

DI-001 (resolved design issue): date semantics needed separation. DI-002 (resolved design issue): payment model needed explicit distinction from SAP open-item postings. DI-003 (open design issue): full receipt-data capture and audit retention need tenant/policy validation. These are not executed SAP defects.
''')

results=json.loads((ROOT/'phase-08/results.json').read_text());ctx=results['context']
kpis=[
('KPI-001','Order cycle time','Mean(full_customer_receipt_date − order_received_date)','Fully received noncancelled orders in intake cohort','received_date; customer_receipt_date; shipped_qty; ordered_qty','Warehouse','End-to-end physical fulfilment speed','Cancelled and incomplete orders excluded; final partial receipt completes order. Survivorship bias: disclose 51 open noncancelled orders.'),
('KPI-002','On-time delivery %','100 × orders fully received by initial confirmed receipt date / orders with initial promise due by as-of','Noncancelled orders with nonblank initial_confirmed_receipt_date ≤ as-of','initial_confirmed_receipt_date; customer_receipt_date; shipped_qty; ordered_qty','Sales','Reliability of original promise','Open overdue and partially fulfilled overdue orders fail; future promises excluded; unknown promise excluded and counted separately. Do not substitute requested date.'),
('KPI-003','Order fulfilment rate %','100 × received units / ordered units','All noncancelled orders in intake cohort, including open and future-due','ordered_qty; shipped_qty; customer_receipt_date','Warehouse','Quantity fulfilment as of snapshot','Cancelled excluded; partial contributes received units only; dispatched but not received does not count. Mixed products all use EA but units have unequal value.'),
('KPI-004','Billing cycle time','Mean(invoice_date − goods_issue_posting_date)','Invoiced deliveries with goods issue by as-of','invoice_date; goods_issue_posting_date; delivery_id','Finance','Posting-to-billing delay','Unbilled deliveries excluded from mean but disclosed separately; partial deliveries measured individually; net cancellations/reversals absent from data. Not dispatch-to-billing time.'),
('KPI-005','Order error rate %','100 × distinct orders with validation_error event / received orders','All 300 orders in intake cohort including later cancellations','events.event_type; events.order_id; orders.received_date','Sales','First-pass validation quality','Corrected errors still count once; open/partial/cancelled included. Does not measure undetected or invoice errors.'),
('KPI-006','Manual-touch rate %','100 × distinct orders with manual_touch event / received orders','All 300 orders in intake cohort including later cancellations','events.event_type; events.order_id; orders.received_date','Customer Service','Avoidable intervention prevalence','Includes chase, rekey and handoff enquiry, excludes routine physical picks; multiple touches count once. Logging completeness and process stage affect rate.'),
]
catalog('phase-08/kpi-contract.csv',[dict(ID=i,Name=n,Formula=f,Denominator=d,Source_fields=s,Owner=o,Purpose=p,Exclusions_and_limitations=l,Date_basis='Intake cohort 2026-07-01 through 2026-10-11; snapshot 2026-10-11; calendar days; dates interpreted as UK business-local dates',Business_target='Unresolved; synthetic baseline is not a target') for i,n,f,d,s,o,p,l in kpis])
grain=[('customers','One fictional customer','customer_id','None'),('products','One stocked product','product_id','None'),('orders','One single-line order','order_id','customer_id → customers; product_id → products'),('deliveries','One shipment for an order','delivery_id','order_id → orders'),('invoices','One active net-only invoice per delivery','invoice_id','delivery_id → deliveries'),('receipts','One incoming net-only receipt','receipt_id','customer_id → customers'),('allocations','One receipt-to-invoice allocation','allocation_id','receipt_id → receipts; invoice_id → invoices'),('events','One intake/quality/manual/cancellation event','event_id','order_id → orders')]
catalog('phase-08/data-model.csv',[dict(Table=t,Grain=g,Primary_key=k,Foreign_keys=f) for t,g,k,f in grain])
dictionary=[]
definitions={'received_date':'Order/customer cash receipt date according to table; actual, not future','requested_receipt_date':'Customer request; not a confirmed promise','initial_confirmed_receipt_date':'Original supported receipt promise; blank means unknown','ordered_qty':'Positive ordered units in EA','unit_price_pence':'Net GBP unit price in integer pence','net_value_pence':'Ordered quantity × net unit price','cancelled':'1 if cancelled before dispatch, else 0','cancelled_date':'Cancellation date; blank if not cancelled','partial_allowed':'1 if partial permission exists in this synthetic baseline; else 0','exception':'Synthetic explanatory label, not a measured root cause','shipped_qty':'Actual dispatched units for this shipment','dispatch_date':'Physical departure date','goods_issue_posting_date':'System posting date; blank if not posted by snapshot','customer_receipt_date':'Physical receipt evidence date; blank means unknown/not yet observed','invoice_date':'Invoice creation date in simplified net-only model','due_date':'Invoice date + 30 calendar days; may lie after snapshot','net_amount_pence':'Net-only invoice amount; VAT and accounting corrections omitted','amount_pence':'Net-only cash simulation amount, not actual VAT-inclusive customer cash','reference':'Synthetic remittance reference; unmatched text retained','allocation_date':'Date receipt assigned analytically to invoice','allocated_pence':'Positive net-only amount assigned; not SAP clearing journal','event_type':'order_received, validation_error, manual_touch or cancelled','event_date':'Observed synthetic event date','role':'Fictional role performing event','detail':'Synthetic event explanation','warehouse_id':'WH-01 only','payment_terms_days':'30 calendar days assumed','currency':'GBP only','country':'GB only','uom':'EA, each','shipped_qty':'Dispatched quantity in EA','received_qty':'Sum of shipments with receipt evidence','full_receipt_date':'Last receipt only when full ordered quantity has been received'}
for t,g,key,fk in grain:
    with (ROOT/f'phase-08/data/{t}.csv').open() as f:rows=list(csv.DictReader(f))
    for field in rows[0]:
        typ='integer' if field.endswith('_pence') or field.endswith('_qty') or field in ['cancelled','partial_allowed','payment_terms_days'] else 'ISO date' if field.endswith('_date') else 'text'
        nullable=field in ['initial_confirmed_receipt_date','cancelled_date','goods_issue_posting_date','customer_receipt_date']
        dictionary.append(dict(Table=t,Field=field,Type=typ,Nullable='Yes' if nullable else 'No',Definition=definitions.get(field,'Stable synthetic identifier' if field.endswith('_id') else 'Fictional descriptive name'),Example=rows[0][field],Rule='Unique non-null primary key' if field==key else 'Referential integrity' if field.endswith('_id') and field!='warehouse_id' else 'See generation assumptions and KPI contract'))
catalog('phase-08/data-dictionary.csv',dictionary)
doc('phase-08/analysis.md','Synthetic data model, analysis and reproducibility',f'''
## Model before generation
{table([dict(Table=t,Grain=g,Key=k,Relationship=f) for t,g,k,f in grain])}

All records are synthetic, generated with Python random seed {ctx['seed']}. 300 orders, 20 customers, five products and one warehouse; single line per order is a deliberate simplification. A future multi-line model needs order_items and line-level delivery/invoice links. Receipts and invoices can have multiple allocation rows structurally, although this generator mainly demonstrates split payments per invoice plus unmatched receipts rather than every possible many-to-many pattern.

Generation uses an intake cohort from 1 July through 11 October 2026, snapshot 11 October 2026. Orders received near the cutoff have less time to finish; open and future-due counts must be shown. Dates are UK business-local calendar dates; weekends are not excluded. NS-ORD-1001 preserves the Phase 1 facts and remains unconfirmed/unfulfilled. Other distributions are designed teaching examples, not calibrated observations. All financial amounts are **net-only integer pence**, with VAT deliberately excluded from invoices and receipts; this is not a complete UK receivables ledger.

## Generation assumptions
Every seventeenth non-base order is cancelled before dispatch. Every nineteenth is left without fulfilment. Some permitted orders split into two shipments; some remain partial. Stock-shortage labels add delay. Billing-handoff labels add billing delay. Errors and manual touches are explicit event records. Pending future events are omitted, not recorded as actuals. No returns, invoice corrections, overpayments, discounts, tax or bad debt are generated; those scenarios remain in design/UAT. This bias intentionally illustrates the problems and cannot prove causation.

## Relationships and double-counting
orders 1:N deliveries; deliveries 1:1 invoices in this simplified dataset; invoices 1:N allocations and receipts 1:N allocations. Aggregate delivery quantity to order, allocations to invoice/receipt, and event flags to order before joining. Never SUM order value after joining raw deliveries and allocations. The four-order fixture demonstrates that £10,000 remains £10,000 regardless of child-row count.

## Executed baseline results — not achieved improvements
{table(results['metrics'])}

Context: {ctx['cancelled']} cancelled; {ctx['completed']} fully received; {ctx['open_non_cancelled']} open noncancelled; {ctx['unknown_promise']} unknown initial promise; {ctx['split_orders']} orders with multiple deliveries; {ctx['partially_received_orders']} partially received; {ctx['partially_paid_invoices']} partially paid invoices; {ctx['unbilled_goods_issued']} goods-issued deliveries still unbilled. These exclusions matter: completed-only cycle and billed-only billing means can look better while unfinished work grows. On-time performance is {ctx['on_time']}/{ctx['due_promises']} due promises, with overdue open orders counted as failures.

Synthetic invoice balances outstanding total £{ctx['invoice_outstanding_pence']/100:,.2f}; unmatched cash totals £{ctx['unallocated_pence']/100:,.2f}. These are model balances, not real cash or savings. Total order value includes cancelled demand; do not call it revenue. Results describe the generator, not NorthStar operations.

## Reproduce and inspect
Run `python scripts/build_data.py` from the project folder; it uses only Python's standard library. CSVs, SQLite database, results JSON, checks and SQL are generated. kpi_queries.sql independently computes the six measures in SQLite. {ctx['checks']} checks passed, including keys, references, date/quantity/amount bounds, known fixture and Python/SQL agreement. SHA-256 hashes in results.json make deterministic reruns comparable. These are executed data checks, not SAP UAT.

LibreOffice route: import each CSV with comma delimiter and UTF-8; retain identifiers as text. Use order_summary.csv as the order-grain table for pivots. It is an exported derived table; source CSV changes require regenerating it. For on-time calculations filter noncancelled known promises due by snapshot; count full receipt by original promise. For billing join invoices to deliveries once at delivery ID. Power BI is optional, not required.

## Dashboard design and implementation
The offline viewer shows six cohort-wide KPI cards, denominator/exclusion context, searchable orders with linked shipment/invoice/payment details, requirement traceability, tests and source evidence. Order-list search filters the list only; KPI cards stay clearly labelled as the full snapshot. No role permissions or transactional SAP behaviours are simulated by the viewer.

## Future-state scenario boundary
No future-state KPI uplift is presented. Phase 10 models illustrative handling-time capacity separately; it is not subtracted from this baseline or claimed as achieved.
''')

risks=[dict(ID=i,Risk=r,Owner=o,Likelihood=l,Impact=im,Score=l*im,Mitigation=m,Trigger=t,Contingency=c,Status='Open; illustrative assessment') for i,r,o,l,im,m,t,c in RISKS]
catalog('phase-10/risks.csv',risks)
changes=[dict(Role=r,Change=c,Training=t,Communication=co,Support=s) for r,c,t,co,s in [
('Sales','Promise only checked quantity/date; retain original promise; correction queue','45-minute NS-ORD-1001 and missing-data exercise','Before trial: explain why checks protect promise quality','Sales key user → process owner → IT if technical'),
('Warehouse','Separate physical dispatch from posting; resolve quantity mismatch','45-minute partial pick and delayed-posting exercise','Daily handoff checklist and unresolved stock review','Warehouse key user → Warehouse owner → IT'),
('Finance','Own billable population; controlled correction and payment handling','60-minute billing retry, credit release and partial-payment cases','Daily unbilled/credit/payment review; weekly control issues','Finance key user → Finance owner → IT'),
('Customer Service','Use authoritative status; capture partial agreement and next action','30-minute status enquiry and customer agreement role-play','Short quick guide; weekly feedback session in pilot','Customer Service key user → relevant process owner'),
('IT','Support role matrix, data contracts, refresh and evidence retention','60-minute access, failed-refresh and reconciliation exercise','Release notes and change-impact review before changes','IT support → authorized platform support where applicable')]]
catalog('phase-10/change-impact.csv',changes)
doc('phase-10/change-and-risk.md','Risks, change and support',f'''
Risk scoring uses illustrative 1–5 likelihood and impact scales; 1 is low, 5 high, score is their product. Scores guide discussion, not quantified loss forecasts. Ten risks are in risks.csv. RISK-007 and RISK-010 remain particularly important because desk research is not system evidence or learner mastery.

{table(changes)}

Training durations are proposed session lengths based on a few concrete scenarios, not measured learning requirements. Use job aids, a practice task, observation and feedback; attendance alone does not establish competence. Communications should explain the changed rule, why it matters, who owns the next step and where to get help. No training has been delivered.

Suggested support: role key user triages process questions; business owner decides policy; IT handles access/integration/report failures; specialist/vendor support is a possible later dependency, not a purchased service. Critical access/financial integrity problems require immediate containment and Finance/IT escalation; other issues enter a daily triage queue. Actual service levels and support coverage require agreement.
''')
options=[dict(Option='A: Improve manual controls',One_off_GBP=2000,Annual_running_GBP=500,Minutes_saved_per_order=2),dict(Option='B: Standardise process and shared reporting',One_off_GBP=8000,Annual_running_GBP=1500,Minutes_saved_per_order=5),dict(Option='C: SAP-aligned future state',One_off_GBP=60000,Annual_running_GBP=18000,Minutes_saved_per_order=8)]
for o in options:
    o['Annual_orders_assumed']=6000;o['Loaded_hourly_rate_GBP']=25
    o['Annual_capacity_hours']=6000*o['Minutes_saved_per_order']/60
    o['Capacity_equivalent_GBP']=o['Annual_capacity_hours']*25
    o['Cash_savings_GBP']='Unproven'
    o['Cost_basis']='Illustrative planning placeholder, not supplier quote or SAP price'
catalog('phase-10/business-case-options.csv',options)
sensitivity=[]
for minutes in [2,5,8]:
    for rate in [20,25,30]:
        sensitivity.append(dict(Option='B sensitivity',Annual_orders=6000,Minutes_saved=minutes,Hourly_rate_GBP=rate,Capacity_hours=6000*minutes/60,Capacity_equivalent_GBP=6000*minutes/60*rate,Annual_running_GBP=1500,Interpretation='Capacity valuation only; not cash ROI'))
catalog('phase-10/sensitivity.csv',sensitivity)
doc('phase-10/business-case.md','Illustrative business case — no achieved savings',f'''
## Decision question
What is the proportionate next step for the three process problems? A free portfolio does not imply a real ERP implementation is free. All implementation costs below are hypothetical business planning placeholders, distinct from the learner's £0 required software-purchase route.

{table(options)}

One-off categories include discovery, design, data cleansing, configuration or spreadsheet setup, integration, testing, training and contingency. Annual categories include administration, support, subscriptions if applicable, monitoring and regression. Option C is a broad allowance, not a SAP licence quote; commercial discovery would be mandatory. These estimates do not come from our synthetic dataset.

At 6,000 assumed annual orders, 5 minutes saved each equals 500 hours/year. At £25/hour, this is £12,500 of **capacity equivalent**, not cash savings. Staff can use time for other work; payroll falls only if a specific cost-removal decision exists. Do not also count the same minutes as fewer errors, faster billing or headcount savings. Earlier billing might affect working capital, but no cash-flow benefit is calculated without actual payment behaviour and financing assumptions.

## Sensitivity and investment caution
For Option B, 2–8 minutes saved and £20–£30/hour gives 200–800 hours and £4,000–£24,000 capacity equivalent per year. At the central assumptions, dividing £8,000 by (£12,500−£1,500) would look attractive, but calling that cash payback would be misleading because salary spending has not been shown to fall. No cash ROI or payback is claimed. To calculate one meaningfully, establish incremental cash benefits, costs, timing and a defensible horizon first.

## Recommendation
Start with Option A's ownership and reconciliation controls, then validate Option B against genuine baseline evidence. Keep the SAP-aligned design as a reference option requiring system fit, entitlements, costs and business readiness assessment. This sequence does not presume SAP is the best investment. Benefits depend on adoption, clean data, operating discipline and actual opportunities to redeploy capacity.
''')

# Phase-specific mentoring remains reviewable even though the user authorized building all phases.
for phase,(title,purpose,task,questions) in enumerate(MENTOR,2):
    doc(f'phase-{phase:02}/learning-review.md',f'Phase {phase} learning review — {title}',f'## Purpose and essential concept\n{purpose}\n\n## Practical task\n{task}\n\n## Three understanding questions\n'+ '\n'.join(f'{i+1}. {q}' for i,q in enumerate(questions))+'\n\nStatus: answers not supplied; understanding not assessed. Review before claiming mastery. Building all phases was authorized; this does not substitute for your learning review.')

doc('phase-11/case-study.md','Case study and lessons learned',f'''
## Context
Independent simulated analysis of NorthStar Manufacturing UK, a one-company, one-warehouse domestic stock seller. Supplied problems: poor visibility, stock delays and manual billing handoffs. The learner's quality-review and error-analysis background motivates attention to controls and evidence; no real client engagement is claimed.

## Analysis and decisions
The pack uses explicitly invented discovery to explore conflicting promises, partial deliveries, credit and billing ownership. AS-IS and TO-BE flowcharts distinguish physical events from postings. Three business requirements decompose into 15 functional and five non-functional requirements, 15 stories and 22 planned UAT cases. Traceability links problems, process changes, tests and measures. Official SAP references support broad standard-process fit; exact configuration and several controls remain unresolved.

The main decisions were to preserve the original promise date, require partial-delivery agreement, assign Finance the billable-population review, distinguish partial payment from clearing, and aggregate child records before combining measures. Standard processes and manual controls were considered before extensions.

## Evidence produced
The reproducible dataset contains 300 synthetic orders, {ctx['counts']['deliveries']} shipments, {ctx['counts']['invoices']} invoices and {ctx['counts']['allocations']} allocations. Six KPI calculations agree between Python and SQLite; {ctx['checks']} data checks passed. The offline viewer exposes results and records but is not an SAP application. All 22 SAP UAT cases remain Not executed.

## Limitations and next steps
No real stakeholder research, tenant demonstration, implementation or measured savings. Data is simplified to one line per order and net-only finances; it omits corrections, VAT and returns. A real project needs agreed policies, broader representative data, configuration/integration/security testing and business acceptance. Learner understanding and personal contribution still need review before resume use.

## Lessons from building the pack
An attractive dashboard is not evidence of a sound denominator. Posted goods issue is not proof of receipt. A plausible root cause is still a hypothesis. A linked analytical payment amount is not the same as an SAP clearing document. A generated test list is not executed UAT. These are artifact-development observations, not retrospective lessons from a live implementation.
''')
doc('phase-12/interview-and-resume.md','Truthful resume and interview preparation','''
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
''')

write('quality/catalog.json',json.dumps(dict(requirements=requirements,stories=stories,trace=trace,tests=tests,evidence=evidence,risks=risks,rules=[dict(id=i,rule=r,owner=o,rationale=s) for i,r,o,s in RULES],fits=fits),indent=2))
print(f'Generated catalogues: {len(requirements)} requirements, {len(stories)} stories, {len(tests)} unexecuted UAT cases, {len(evidence)} evidence entries.')
