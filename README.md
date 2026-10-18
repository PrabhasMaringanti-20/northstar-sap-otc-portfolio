# NorthStar Manufacturing UK — Order-to-Cash portfolio

**Independent simulated portfolio · AI-assisted · 11 October 2026**

A complete artifact pack for learning business analysis through a fictional one-company, one-warehouse domestic stock-sales process. No real client engagement, production configuration, measured savings or SAP implementation experience is claimed.

## Start here

1. Download and extract the supplied GitHub-ready ZIP, or use GitHub's Code → Download ZIP when viewing the repository.
2. Run `python scripts/serve.py --open` and visit `http://127.0.0.1:8000/`. The app includes document reading, synthetic KPI cards, order details, requirements, UAT and evidence. Root index.html is also self-contained for browsers allowing file URLs. No account, API key or paid service is required.
3. Open [the editable workbook](downloads/NorthStar_Complete_Workbook.xlsx) in LibreOffice Calc, [the report](downloads/NorthStar_Portfolio_Report.docx) in Writer and [the ten-slide presentation](downloads/NorthStar_Executive_Presentation.pptx) in Impress. Microsoft Office is optional. Rendering may vary; Office files were programmatically checked, not visually verified in LibreOffice. Real portfolio UI browser checks and screenshots are separately recorded in quality/browser-checks.json.
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
