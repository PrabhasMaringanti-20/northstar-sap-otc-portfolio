"""Record authorized full-build scope without inventing learner completion."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def put(p,t):(ROOT/p).write_text(t.strip()+'\n')
for p in (ROOT/'phase-01').glob('*.md'):
    text=p.read_text()
    if 'Supersession note' not in text:
        lines=text.splitlines();lines[1:1]=['','> Supersession note — 11 October 2026: the user authorized building all phases. This Phase 1 draft is retained as the starting charter. Current status and decisions are in ../registers/progress.md and ../registers/decisions.md. Public Edition 2602 is now the research reference. Initial “not started” and evidence-pending statements below describe 8 October, not the current artifact set.']
        p.write_text('\n'.join(lines)+'\n')
put('registers/progress.md','''# Current progress — 11 October 2026

Independent simulated portfolio. Full artifact build authorized by the user. Deliverable creation does not establish learner mastery, stakeholder approval or production readiness.

| Phase | Artifact status | Validation / limitation |
|---|---|---|
| 1 Charter and plan | Built; original charter preserved with supersession note | SAP access, actual study hours and target role remain unknown |
| 2 Discovery | Built | Explicit role-play; no people interviewed |
| 3 AS-IS | Built | Hypotheses and fictional tools; process flowchart, not BPMN |
| 4 Requirements | Built | 23 requirements, 12 rules; no stakeholder approval |
| 5 SAP / TO-BE | Built | Public Edition 2602 reference; seven reviewed sources and two unverified pages |
| 6 Fit-gap | Built | Desk-based; no tenant demonstration |
| 7 Backlog | Built | 15 proposed stories; not delivered SAP functionality |
| 8 Data and KPIs | Built and executed | 300 synthetic orders; six Python/SQL KPIs; data-check evidence available |
| 9 UAT | Design built | 22 SAP cases Not executed; separate desk walkthrough/data checks |
| 10 Risks/change/case | Built | Ten open risks; illustrative cost/capacity assumptions |
| 11 Packaging | Built | Offline viewer, editable files, presentation and case study; not published |
| 12 Resume/interview | Conditional drafts built | Actual learner contribution and oral review still pending |

## Outstanding quality gates

- Learner answers and independent explanation have not been reviewed.
- SAP access is unknown; no paid access required or purchased.
- No real discovery, policy agreement, configured system tests or business acceptance.
- Data is single-line, net-only and synthetic; receipt integration and exact audit coverage unresolved.
- Browser/LibreOffice visual rendering not verified in this environment; programmatic checks are recorded separately.

Artifact preparation is complete subject to the recorded checks and limitations. The project must not be labelled fully complete under the original final gate until learner understanding is reviewed. It is not production ready.
''')
dec=ROOT/'registers/decisions.md';t=dec.read_text()
if 'DEC-008' not in t:
 t+='''| DEC-008 | 2026-10-11 | Build all twelve phases now | User explicitly requested the whole project; learning reviews remain pending |
| DEC-009 | 2026-10-11 | Pin SAP reference to Public Edition 2602 | Official feature-scope PDF reviewed; learning sources are unpinned; no tenant access inferred |
| DEC-010 | 2026-10-11 | Use a 300-order single-line, net-only analytical dataset | Keeps reproducibility manageable; not a full UK tax/receivables ledger |
| DEC-011 | 2026-10-11 | Provide an offline portfolio viewer, not hosted production software | Preserves free-tool constraint and original instruction not to publish without request |
| DEC-012 | 2026-10-11 | Keep representative order unresolved in baseline | Design/test variants are separate; do not invent actual fulfilment |
| DEC-013 | 2026-10-11 | Draft resume statements conditionally | Artifacts generated with AI; personal validation and learning review not established |
'''
 dec.write_text(t)
ass=ROOT/'registers/assumptions.md';t=ass.read_text()
if 'ASM-006' not in t:
 t+='''
## Full-build additions — 11 October 2026

| ID | Type | Entry | Status / treatment |
|---|---|---|---|
| ASM-006 | Fictional operating policy | Daily Finance queue review; daily management snapshot before 09:00 Europe/London | Proposed business-local cadence; not a service-level claim |
| ASM-007 | Analytical assumption | One line per order, GBP integer pence, all finance net-only with VAT omitted | Explicit teaching limitation |
| ASM-008 | Analytical assumption | Synthetic snapshot 11 October 2026; dates are UK business-local calendar dates | Actual future events omitted; promises/due dates may be future |
| ASM-009 | Business-case assumption | 6,000 annual orders and £25 loaded hourly cost | Illustrative; independent of synthetic baseline |
| ASM-010 | Learning assumption | Broad junior BA emphasis with ERP/process skills retained | Primary target role still unresolved |
| CON-004 | Evidence constraint | Learner has not personally reproduced or explained artifacts in this conversation | Conditional resume drafts; no competence claim |
| DEP-004 | Integration dependency | Receipt evidence, audit coverage and retention require validation | No automatic carrier integration or retention guarantee |
'''
 ass.write_text(t)
gl=ROOT/'registers/glossary.md';t=gl.read_text()
if '| Grain |' not in t:
 t+='''
## Terms introduced in the full build

| Term | Meaning |
|---|---|
| Grain | What one data row represents |
| Primary / foreign key | Unique row identifier / reference to another table's row |
| Fan-out | Multiplication of parent rows when several child tables are joined |
| Business partner | Common identity and role-specific master information; see SAP-005 |
| ATP | Available to promise: date/quantity confirmation concept; see SAP-002 |
| PGI | Post goods issue; recording an outbound stock movement, not customer receipt |
| Receivable | Amount owed by a customer |
| Partial payment | Payment linked to an invoice while original invoice remains open; see SAP-006 |
| Residual item | Remaining balance item after clearing the original invoice; see SAP-006 |
| On-account payment | Payment recorded without matching a particular invoice |
| RACI | Responsible, Accountable, Consulted and Informed responsibilities |
| Segregation of duties | Separating conflicting actions, such as requesting and approving release |
| Capacity released | Staff time available for other work; not necessarily cash saved |
| Severity / priority | Impact of a defect / urgency of resolving it |
| Configuration / extension | Setting standard behaviour / adding capability beyond the chosen standard |
'''
 gl.write_text(t)
put('README.md','''# NorthStar Manufacturing UK — Order-to-Cash portfolio

**Independent simulated portfolio · AI-assisted · 11 October 2026**

A complete artifact pack for learning business analysis through a fictional one-company, one-warehouse domestic stock-sales process. No real client engagement, production configuration, measured savings or SAP implementation experience is claimed.

## Start here

1. Download and extract the supplied GitHub-ready ZIP, or use GitHub's Code → Download ZIP when viewing the repository.
2. Run `python scripts/serve.py --open` and visit `http://127.0.0.1:8000/`. The app includes document reading, synthetic KPI cards, order details, requirements, UAT and evidence. Root index.html is also self-contained for browsers allowing file URLs. No account, API key or paid service is required.
3. Open [the editable workbook](downloads/NorthStar_Complete_Workbook.xlsx) in LibreOffice Calc, [the report](downloads/NorthStar_Portfolio_Report.docx) in Writer and [the ten-slide presentation](downloads/NorthStar_Executive_Presentation.pptx) in Impress. Microsoft Office is optional. Rendering may vary; these files were programmatically checked, not visually verified in LibreOffice.
4. Read [the project guide with screenshots (PDF)](downloads/NorthStar_Project_Guide.pdf), [full portfolio reference (PDF)](downloads/NorthStar_Full_Portfolio.pdf), [local setup](RUN_LOCALLY.md), [GitHub Pages setup](GITHUB_SETUP.md), [quality gate](quality/final-quality-gate.md) and [contribution limits](phase-12/interview-and-resume.md).

## What is working

This is a read-only portfolio application, not an operational SAP/ERP backend. Search and filter orders, export CSV, inspect linked records, explore requirements and tests, switch process maps and read documents. Creating orders, reserving stock, posting invoices and clearing actual payments are proposed business behaviours documented in the portfolio; they are not implemented transactions in the browser. See [what was built](PROJECT_GUIDE.md).

## GitHub access

Push the extracted folder contents to a public repository with index.html at its root. Then enable Settings → Pages → Deploy from a branch → main → /(root). The root entry and .nojekyll are supplied. Pushing alone does not enable Pages; no live deployment is claimed. This route uses GitHub Pages for public repositories on GitHub Free; official sources and setup steps are in GITHUB_SETUP.md. Generated ZIPs are ignored by Git to keep the repository clean.

## Evidence boundary

- Supplied facts: learner background and fictional scenario scope. Invented business detail is labelled assumption or role-play.
- SAP reference: Public Edition 2602; official URLs/access dates and uncertainties in [SAP evidence](phase-05/sap-evidence.csv). Documentation is not demonstrated capability.
- Executed: synthetic generation, Python/SQLite KPI reconciliation, fixture/data checks and artifact consistency checks.
- Not executed: all 22 SAP UAT cases. No fabricated defects, approvals, interviews or system screenshots.
- Pending: learner understanding and actual personal contribution review; business validation, tenant configuration and testing. Artifact preparation does not equal the original final learning gate or production readiness.

## Contents

| Folder | Contents |
|---|---|
| phase-01 | Starting charter, schedule, base order and free route; original statements carry a supersession note |
| phase-02 | Stakeholders, interview guide, role-play findings and responsibilities |
| phase-03 | AS-IS flowchart, step register and root-cause hypotheses |
| phase-04 | BRD, 23 requirements, 12 rules, access and traceability |
| phase-05 | TO-BE flowchart, SAP evidence and data/control design |
| phase-06 | Desk-based fit-gap assessment |
| phase-07 | 15-story backlog and separate analysis tasks |
| phase-08 | 300-order synthetic dataset, dictionary, model, six KPI contracts, SQL and results |
| phase-09 | 22 unexecuted UAT cases, plan and desk-based design walkthrough |
| phase-10 | Ten risks, role change/training/support and illustrative option/cost analysis |
| phase-11 | Case study and executive presentation source |
| phase-12 | Conditional resume descriptions, interview scripts and coaching rubric |
| registers | Current decisions, assumptions, glossary and progress |
| quality | Executed checks, fixture oracle and remaining gates |
| viewer | Offline browser interface, not SAP software |
| scripts | Reproducible free-tool build scripts |

Each phase has a short practical task and three understanding questions. The user authorized building all phases at once; no learner answers or mastery are inferred.

## Reproduce with free tools

Python 3.11+ and Node.js 18+ are recommended for the full build. Install the packages in requirements.txt if needed, then run `python scripts/build_all.py` from this folder. Node runs local viewer logic checks only; it is not needed to open the viewer. Data generation itself uses the Python standard library: `python scripts/build_data.py`. SQLite queries are in phase-08/kpi_queries.sql. Graphviz `dot` is optional for regenerating process SVGs; supplied SVGs remain usable if unavailable. No network access is needed to rerun the build once tools are installed. Official SAP source links require internet only when opened.

Markdown, CSV and authored Python are the source of truth. Reconcile edits made directly in Office-compatible copies before rebuilding, which overwrites generated outputs. The builder does not publish or deploy anything. The earlier Phase 1 downloads are historical snapshots, not the current full project.

## Free route

Required incremental software purchases: £0 using an existing device and free tools. This is not a promise about charges for this chat/cloud environment or internet access. No paid SAP practice tenant, training, Power BI sharing, domain or hosting is needed. The illustrative business case models a separate fictional organization's potential costs.

## Personal contribution

AI generated the draft artifacts and ran the recorded checks. The learner should review, revise, reproduce and explain them before claiming personal analysis or testing achievements. See phase-12/interview-and-resume.md for conditional wording and an honest AI-use explanation. No employment outcome is guaranteed.
''')
put('requirements.txt','''openpyxl==3.1.5
python-docx==1.2.0
python-pptx==1.0.2
matplotlib==3.10.8
reportlab==4.4.9
''')
put('.gitignore','''__pycache__/
*.pyc
.venv/
downloads/*.zip
downloads/*.sha256
.DS_Store
''')
from browser_evidence import current_browser_evidence
browser=current_browser_evidence()
if browser:
    replacements={
        'registers/progress.md':{
            '- Browser/LibreOffice visual rendering not verified in this environment; programmatic checks are recorded separately.': '- Real local Chromium checks and actual screenshots are recorded in quality/browser-checks.json; LibreOffice visual rendering remains unverified. The browser record identifies the exact tested HTML hash.',
        },
        'README.md':{
            'Rendering may vary; these files were programmatically checked, not visually verified in LibreOffice.': 'Rendering may vary; Office files were programmatically checked, not visually verified in LibreOffice. Real portfolio UI browser checks and screenshots are separately recorded in quality/browser-checks.json.',
        },
    }
    for relative,changes in replacements.items():
        file=ROOT/relative;content=file.read_text()
        for old,new in changes.items():content=content.replace(old,new)
        file.write_text(content)
    file=ROOT/'registers/progress.md'
    file.write_text(file.read_text()+'\n## Handover update — 12 October 2026\n\nActual local Chromium checks and nine UI screenshots completed. Root index.html, local-server script, GitHub Pages guide and PDF handover added. No remote publishing occurred. Exact test timing and current source hashes are in quality/browser-checks.json.\n')
dec=ROOT/'registers/decisions.md';content=dec.read_text()
if 'DEC-014' not in content:
    content+='| DEC-014 | 2026-10-11 | Add real-browser screenshots, explanatory PDFs and GitHub-ready root entry | User requested local run evidence and a repository they can push; no remote publication performed |\n'
    dec.write_text(content)
print('Updated current project status, registers and free-tool README.')
