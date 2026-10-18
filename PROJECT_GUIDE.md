# What was built — NorthStar project guide

Independent simulated portfolio. Initial build 11 October 2026; handover refreshed 12 October 2026. This guide describes actual artifacts and clearly separates the running portfolio application from a future SAP implementation. The synthetic data snapshot remains 11 October 2026.

## 1. The direct answer

Yes: the twelve-phase **artifact pack** and a **read-only, interactive portfolio application** have been built. You can run the application locally, inspect records and analysis, read the documents, and publish the static application using GitHub Pages after uploading the repository and enabling Pages.

No: this is not a working SAP ERP implementation or a transactional order-management backend. Creating orders, reserving stock, enforcing credit approvals, posting goods issue, issuing legally valid invoices and clearing real payments are requirements/design scenarios in the portfolio. They are not executable business transactions in this app.

The earlier phrase “full project built” referred to the artifact pack and viewer. It did not mean a production ERP system, completed SAP UAT or verified learner mastery. Those distinctions are essential to honest portfolio use.

## 2. What you can actually do in the application

| Screen | Implemented behaviour | Boundary |
|---|---|---|
| Overview | Six calculated synthetic KPI cards, exclusions and representative order link | Snapshot, not live business performance |
| Orders | Search by order/customer/issue; status filter; export filtered CSV; open linked delivery/invoice/allocation detail | Read-only records; no order creation or modification |
| Process maps | Switch between AS-IS and TO-BE SVG flowcharts | Proposed process logic, not a workflow execution engine |
| Requirements | Search 23 requirements and inspect acceptance, dependencies and trace links | Proposed requirements, not stakeholder-approved scope |
| Data & KPIs | Inspect a chart, formulas, populations and limitations | Generated snapshot; filters on the order list do not recalculate cards |
| UAT & checks | Expand 22 test designs with prerequisites, steps and expected results | Every SAP case remains Not executed |
| SAP evidence | Read nine source-register entries and open official links | Seven reviewed sources, two unverified pages; no tenant demonstration |
| Document library | Select embedded phase documents and download PDF/workbook/presentation/setup files | Download files require the complete project folder or hosted repository |

There are no logins, roles enforced by the app, live SAP APIs, cloud databases, payment services or secret keys. The role-access matrix describes a proposed business control; it is not implemented authentication. The SQLite database is an analytical output for local inspection, not a backend used by the browser.

## 3. What work was done

- Converted the supplied scope into a charter, representative order, learning plan and maintained registers.
- Created explicitly simulated stakeholder discovery and mapped conflicting needs to proposed policies.
- Built AS-IS and TO-BE flowcharts with ownership, handoffs and exceptions; separated hypotheses from proven causes.
- Authored 3 business, 15 functional and 5 non-functional requirements, 12 business rules, 15 stories and 22 UAT cases; linked them using stable IDs.
- Reviewed official SAP sources and pinned the reference to S/4HANA Cloud Public Edition 2602; recorded access dates and uncertainty.
- Built a reproducible 300-order synthetic dataset with separate customer, product, order, delivery, invoice, receipt, allocation and event tables.
- Implemented six KPI calculations in Python and independently in SQLite; executed 24 data checks and a hand-calculated fixture.
- Built a ten-risk register, role change/training/support plan and illustrative option comparison that separates capacity from cash savings.
- Created an offline HTML/CSS/JavaScript portfolio viewer, editable workbook and report, ten-slide presentation, case study and conditional interview/resume pack.
- Added local serving, root website entry, GitHub Pages preparation, real-browser checks, screenshot evidence and PDF handover materials.

AI performed the drafting, coding and recorded tool execution in this conversation. Your personal contribution so far is supplying the brief, scope, background and preferences. You have not yet demonstrated independent review or reproduction here. Update that statement as you do the practical tasks; do not claim personal implementation/testing work merely because artifacts exist.

## 4. All twelve phases and their outputs

| Phase | What is present | What remains |
|---|---|---|
| 1 Charter | Scope, objectives, assumptions, decisions, schedule, NS-ORD-1001 | Tailoring to actual study time and primary target role |
| 2 Discovery | Stakeholder matrix, questions, role-play, findings and RACI | Real stakeholder engagement |
| 3 AS-IS | Flowchart, eight-step register and root-cause hypotheses | Validate current process and causes with evidence |
| 4 Requirements | BRD, 23 requirements, 12 rules, access and traceability | Business review and policy approval |
| 5 TO-BE/SAP | Future flow, controls, data needs and source register | Tenant-specific feasibility and settings |
| 6 Fit-gap | Fifteen functional desk assessments plus NFR discussion | System demonstrations against criteria |
| 7 Backlog | Fifteen stories with criteria, dependencies and exceptions | Delivery planning and implementation |
| 8 Analysis | 300 orders, dictionary/model, six KPIs, SQL, checks and charts | Broader real data and baseline validation |
| 9 UAT | Twenty-two cases, criteria/severity and design walkthrough | SAP execution and user acceptance |
| 10 Change/case | Ten risks, role impacts, training/support and scenario costs | Agreed operating model and business case |
| 11 Packaging | README, viewer, editable files, deck and case study | Optional GitHub publication by you |
| 12 Coaching | Conditional project descriptions, interview scripts and questions | Your answers, feedback and mastery review |

## 5. How the project works technically

The source files are Markdown documents, CSV catalogues, authored Python, JavaScript and CSS. Python generates deterministic synthetic tables and calculations, then builds the viewer by embedding a JSON snapshot and the documents into HTML. That file runs in the browser without a backend. The same static files can be served locally or by GitHub Pages.

Flow: authored catalogues and generator → CSV / SQLite / calculated results → generated HTML and editable reports → browser exploration. No browser action writes to the original CSVs. Editing the workbook alone does not update the viewer. To change its source data or generated documents consistently, modify source inputs and run the build scripts again.

Root index.html, viewer/index.html and downloads/NorthStar_Offline_Portfolio.html are generated copies of the same app. The root copy makes local and GitHub Pages entry straightforward. Source JavaScript and CSS stay in viewer/app.js and viewer/style.css. This intentional duplication supports a portable single-file app as well as an editable repository.

## 6. Data and KPI interpretation

The dataset contains 300 orders, 285 deliveries, 262 invoices, 209 receipts and 197 allocations. It includes split deliveries, partial payments, open orders and unmatched receipts. Dates are synthetic UK business-local calendar dates with a snapshot of 11 October 2026. Amounts use integer pence; invoices and receipts are net-only and omit VAT. One line per order is a teaching simplification.

The six full-cohort results are: cycle time 6.16 calendar days; on-time delivery 49.07%; quantity fulfilment 84.89%; billing cycle 1.95 calendar days; order error rate 22.33%; manual-touch rate 76.33%. These are properties of generated data, not actual NorthStar results or achieved improvements.

Cycle time includes 232 fully received orders and excludes 51 open noncancelled orders. On-time delivery counts 132 successes among 269 due initial promises, including overdue open failures. One unknown promise is separately disclosed. Billing cycle covers 262 invoiced deliveries and excludes 22 goods-issued unbilled deliveries. Read the KPI contract before interpreting any number.

The model aggregates child records before combining order measures. A delivery × payment join can otherwise multiply values. A partial payment's analytical remaining balance is not proof that an SAP invoice has been cleared.

## 7. How to run it locally

Extract the repository ZIP, open a terminal in the northstar-otc folder and run `python scripts/serve.py --open`. Visit `http://127.0.0.1:8000/` if it does not open. Windows can use `py`; macOS/Linux may use `python3`. The server needs only Python's standard library and stops with Ctrl+C.

Double-clicking index.html is also an intended offline path for browsers allowing file URLs. This environment's browser policy blocks that protocol, so actual verification used local HTTP. Refer to RUN_LOCALLY.md for alternatives, the five-minute tour, rebuild commands and troubleshooting.

## 8. GitHub access and the free route

Push the complete folder contents to a new public repository. Keep index.html at the root. Enable Settings → Pages → Deploy from a branch → main → /(root). After deployment, use the actual URL GitHub displays. A typical project URL has the form https://YOUR_USERNAME.github.io/northstar-otc/; this is a format example, not an existing deployed site.

GitHub Pages can host this static project from a public repository on GitHub Free. The one-time Pages setup is needed; pushing alone is insufficient. GITHUB_SETUP.md includes exact commands, GitHub Desktop guidance and official sources accessed on 11 October 2026. No custom domain or paid service is required for this planned route. Existing device, internet and chat/cloud costs are separate.

Nothing has been pushed to your account or deployed by this handover. GitHub hosting must be checked after your own deployment.

## 9. Verification and screenshot meaning

Python/SQLite data checks and catalogue consistency checks are recorded in quality and phase-08/data. Node smoke checks verify viewer logic. Real Chromium UI checks, when present, are recorded separately in quality/browser-checks.json with the tested HTML hash, browser version and screenshot references. Screenshots in the handover PDF come from that running local portfolio, not the earlier generated concept image and not SAP software.

The browser exercise covers navigation, search, filters, CSV download, record detail, requirement links, UAT expansion, process switching, evidence, document selection, download links, repository-prefix paths and a mobile viewport. It is not a comprehensive security/accessibility certification or real SAP UAT. No real business users were interviewed or tested. LibreOffice visual rendering is not verified.

## 10. What “complete” means here

The twelve-phase artifact pack and defined read-only viewer are built. Their exact execution checks and remaining limits are reported, rather than calling them production ready. The original final learning gate stays open until you can explain the decisions, calculations and your personal contribution independently. The files do not prove a live SAP implementation or guarantee employment.

Turning this into a transactional ERP application would be a separate software-development scope: persistence, authenticated roles, transaction rules, inventory/reservation logic, accounting semantics, integrations, security, operational support and system acceptance. That work is neither required for this BA portfolio nor silently claimed as completed.

## 11. Where to start learning

Read Phase 1 and explain why 60 on hand cannot confirm 100 requested. Follow FR-004 through its story and tests. Recalculate the four-order fixture. Explain physical dispatch versus posting versus receipt. Then work through the short task and three questions in each phase. Resume wording should evolve only as you personally review, change, reproduce and explain the work.

## 12. Handover files

The Project Guide PDF explains the build, real screenshots, local use and GitHub setup. The Full Portfolio PDF supplies the narrative documents and detailed catalogue appendices. Editable originals and raw synthetic data remain in the repository because PDFs are not a suitable replacement for executable scripts or tabular source data. All formats are readable with free tools.
