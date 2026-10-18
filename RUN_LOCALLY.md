# Run the project locally

The portfolio application is prebuilt. Viewing it does not require SAP, a database server, an account, npm packages or paid software. The editable workbook is a snapshot; it does not recalculate the browser data when changed.

## Recommended: local web server

1. Extract the repository ZIP and open the `northstar-otc` folder. Keep the entire folder together.
2. Open a terminal inside that folder.
3. Run `python scripts/serve.py --open` (on Windows you may use `py scripts/serve.py --open`; on macOS/Linux, `python3 scripts/serve.py --open`).
4. If the browser does not open automatically, visit `http://127.0.0.1:8000/`.
5. Press Ctrl+C in the terminal when finished. If the port is occupied, run with `--port 8001`.

Python's standard library is enough for this server. Internet is unnecessary for the application itself; official SAP source links open external sites when selected. No records are written by the application. CSV export saves a file in your browser's download location.

## Without Python

Double-click `index.html` in a modern browser. All interactive data and documents are embedded; no fetch calls or backend are required. Some managed browsers block file URLs. If that happens, use the local-server option or GitHub Pages. File-URL execution was blocked by this environment's browser policy; actual Chromium verification used HTTP on loopback. Do not interpret that policy restriction as a passed file-URL test.

## Five-minute tour

1. Overview: read the six KPI cards and the denominator context.
2. Orders: search `NS-ORD-1001`; open it and notice that 60 on hand is not a confirmed promise. Filter other orders by fulfilment status and export the filtered CSV.
3. Requirements: search `FR-004`; inspect the story/test/KPI chain for partial delivery.
4. UAT: expand `TC-005` and `TC-006`; both remain Not executed in SAP.
5. Process maps: switch AS-IS and TO-BE.
6. Data & KPIs: inspect formulas and limitations; the cards remain full-cohort when the order list is filtered.
7. SAP evidence: distinguish reviewed sources from two unverified pages.
8. Document library: read each phase and download the PDF/workbook/presentation.

## Rebuild instead of just viewing

Only contributors regenerating the data, charts and editable reports need the build tools. Install Python 3.11+ and Node.js 18+, then `python -m pip install -r requirements.txt` and `python scripts/build_all.py`. Graphviz is optional if the supplied rendered maps are retained. The Python data-only command is `python scripts/build_data.py`.

Optional real-browser checks and screenshot refresh require `python -m pip install -r requirements-browser.txt` plus an installed Chromium browser. Run `python scripts/browser_check.py --browser-path /path/to/chromium`. That script creates a temporary local server, tests the app and closes both server and browser. It does not run SAP UAT. Windows Chrome is usually inside Program Files; provide its executable path if using it. Browser automation is optional for viewing or GitHub hosting.

After capturing screenshots, `python scripts/build_handover.py` regenerates the explanatory and full-reference PDFs. Run `python scripts/package_release.py` last to update the ZIPs. Regeneration overwrites generated files; reconcile direct Word/Excel edits with source Markdown/CSV/Python first.

## Troubleshooting

- A blank page: use a current browser with JavaScript enabled; try the local server. Inspect the browser console and compare quality/browser-checks.json.
- Opening README shows text, not the app: open root `index.html` or the local URL.
- PDF link unavailable: confirm the full repository's downloads folder was extracted. A lone HTML copy keeps the app data but cannot carry separate downloadable files.
- Data edits do not appear: rebuild the viewer; it contains a generated snapshot rather than reading live CSVs.
- Changes disappear on rebuild: edit the source scripts, Markdown or CSV generation inputs, not only generated HTML/Office copies.
