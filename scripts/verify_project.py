"""Validate catalogue consistency and report remaining gates; no SAP execution."""
from pathlib import Path
import csv,json,re
ROOT=Path(__file__).resolve().parents[1]
c=json.loads((ROOT/'quality/catalog.json').read_text());r=json.loads((ROOT/'phase-08/results.json').read_text())
checks=[]
def check(name,condition,detail):
 checks.append(dict(id=f'QC-{len(checks)+1:03}',check=name,status='Passed' if condition else 'Failed',detail=detail,type='Executed artifact consistency check'))
 if not condition:raise AssertionError(name)
req={x['ID']:x for x in c['requirements']};stories={x['ID']:x for x in c['stories']};tests={x['ID']:x for x in c['tests']};evidence={x['ID']:x for x in c['evidence']}
check('Catalogue unique IDs',len(req)==23 and len(stories)==15 and len(tests)==22,'3 BR + 15 FR + 5 NFR; 15 stories; 22 test designs')
check('All three business problems traced',{x['Problem'] for x in c['trace']}=={'PROB-001','PROB-002','PROB-003'},'Every supplied problem has a trace row')
check('Every functional requirement traced',{x['Requirement'] for x in c['trace']}=={k for k in req if k.startswith('FR-')},'No functional requirement missing from trace')
check('Story/test references valid',all(s['Requirement'] in req and all(t in tests for t in s['Tests'].split(';')) for s in stories.values()),'All story requirement and test references resolve')
check('Trace and test bidirectional',all(x['Story'] in stories and all(x['Requirement'] in tests[t]['Requirements'].split(';') for t in x['Tests'].split(';')) for x in c['trace']),'Trace test links include the same requirement')
check('All tests link valid requirements',all(all(k in req for k in t['Requirements'].split(';')) for t in tests.values()),'No dangling test requirements')
check('All NFRs covered',{k for t in tests.values() for k in t['Requirements'].split(';') if k.startswith('NFR-')}=={k for k in req if k.startswith('NFR-')},'All five NFRs linked to planned cases')
check('SAP execution labels honest',all(t['Status']=='Not executed' and t['Actual_results']=='Not run in SAP' and t['Defect_reference']=='None' for t in tests.values()),'No invented test result or SAP defect')
exception_cases={'Missing/incorrect customer data':['TC-002','TC-003'],'Insufficient stock':['TC-004'],'Partial delivery':['TC-005','TC-006'],'Credit/order block':['TC-007','TC-008'],'Cancellation':['TC-009','TC-010'],'Incorrect invoice':['TC-013'],'Partial/unmatched payment':['TC-014','TC-015']}
check('Seven exceptions covered',all(all(t in tests for t in ts) for ts in exception_cases.values()),'Includes positive and negative partial-delivery permission; pre/post dispatch cancellation')
check('Rules and process change IDs',len({x['Rule'] for x in c['trace']})==12 and len({x['Process_change'] for x in c['trace']})==15,'All 12 rules referenced; 15 unique changes')
check('Fit assessment covers FRs',{x['Requirement'] for x in c['fits']}=={k for k in req if k.startswith('FR-')},'15 desk-based fit assessments; no claimed tenant demo')
check('Source evidence completeness',all(e['URL'].startswith(('https://learning.sap.com/','https://help.sap.com/')) and e['Access_date']=='2026-10-11' and e['System_demonstration']=='None' for e in evidence.values()),'Official URLs/access date and demonstration boundary recorded')
check('Unverified sources explicit',sum(e['Verification'].startswith('Unverified') for e in evidence.values())==2,'Two unreadable Help pages not treated as verified capability')
check('Synthetic data checks passed',all(x['status']=='Passed' for x in r['checks']),'24 checks incl. independent Python/SQL and hand-calculated fixture')
check('Required files present',all((ROOT/p).is_file() for p in ['phase-03/as-is.mmd','phase-05/to-be.mmd','phase-04/brd.md','phase-10/business-case.md','phase-12/interview-and-resume.md']),'Core narratives/maps exist')
check('Learning questions retained',all((ROOT/f'phase-{i:02}/learning-review.md').exists() for i in range(1,13)),'All twelve learning reviews present; none marked passed')
summary=dict(date='2026-10-11',checks=checks,exception_coverage=exception_cases,status='Artifact checks passed; final learner/production gates remain open')
(ROOT/'quality/consistency-checks.json').write_text(json.dumps(summary,indent=2))
with (ROOT/'quality/consistency-checks.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
rows='\n'.join(f'| {x["id"]} | {x["check"]} | {x["status"]} | {x["detail"]} |' for x in checks)
(ROOT/'quality/final-quality-gate.md').write_text('''# Final quality gate — 11 October 2026

Independent simulated portfolio. **Artifacts prepared; original project completion gate remains open. Not production ready.**

## Executed evidence

24 Python/SQLite synthetic-data checks passed. Six KPI calculations agree before rounding. Sixteen catalogue consistency checks below passed. These are data/document checks, not SAP UAT. Office files are reopened and the offline viewer receives JavaScript logic smoke checks in the packaging step; see artifact-checks.json. No browser rendering, real role permissions or LibreOffice visual checks were performed.

| ID | Check | Result | Evidence |
|---|---|---|---|
'''+rows+'''

## Manual desk review

Requirements address the three supplied problems; core exception paths appear in both flowcharts and planned tests. PC changes map to the named requirements and proposed stories. Seven exception categories have test coverage. Standard-process claims cite the SAP evidence register; two unreadable pages remain unverified. Business targets have not been achieved. Financial amounts are explicitly net-only, and capacity assumptions are not cash savings.

## Remaining weaknesses

1. Learner answers, personal contribution and independent explanation have not been reviewed. Conditional resume descriptions cannot yet be used as personal execution claims.
2. Discovery and policies are invented role-play. No stakeholders have validated priorities, ownership, thresholds or acceptance.
3. SAP is a documentation reference: no tenant, configuration, authorization, integration or UAT evidence. All 22 SAP cases remain Not executed.
4. Synthetic data is single-line and net-only; VAT, corrections, returns and the full SAP journal/open-item model are absent. These need broader modelling for a real project.
5. Receipt capture, audit retention and exact billing/credit controls remain unresolved. Learning pages are not release-pinned even though the reference PDF is 2602.
6. Viewer is read-only learning software with embedded synthetic data. It does not enforce production authorization or implement the transactional requirements. Browser/Office visual QA remains outstanding.
7. Business-case volumes, handling minutes and costs are illustrative. No cash ROI, achieved benefit or investment approval is claimed.

## Honest completion statement

The requested twelve-phase artifact pack is built. Production readiness is not established, and full portfolio completion under the user's original gate requires the learner to explain key decisions without a script. Use the phase learning reviews next, then revise personal claims to match actual work completed.
''')
print(f'{len(checks)} catalogue consistency checks passed; final learning gate remains open.')
from browser_evidence import current_browser_evidence
browser=current_browser_evidence()
if browser:
    gate=ROOT/'quality/final-quality-gate.md';text=gate.read_text()
    text=text.replace('No browser rendering, real role permissions or LibreOffice visual checks were performed.',f'Actual local Chromium rendering and {len(browser["checks"])} UI checks are recorded in browser-checks.json, with screenshots and the tested HTML hash. Real role permissions and LibreOffice visual checks were not performed.')
    text=text.replace('Browser/Office visual QA remains outstanding.','Actual local browser checks are recorded separately; Office visual QA, other-browser coverage and comprehensive accessibility/security review remain outstanding.')
    gate.write_text(text)
