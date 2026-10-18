"""Real Chromium checks and unedited screenshots of the local read-only portfolio.

Starts/stops a loopback server. Requires optional Playwright plus an installed browser.
No external page requests are permitted. These are portfolio UI tests, not SAP UAT.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from datetime import datetime,timezone
from urllib.parse import urlparse
import argparse,csv,hashlib,json,shutil,traceback
from playwright.sync_api import sync_playwright,expect

ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        # Emulate GitHub project-site subpaths using the same project root.
        if self.path.startswith('/northstar-otc/'):
            self.path=self.path[len('/northstar-otc'):]
        super().do_GET()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--browser-path',default=shutil.which('chromium') or shutil.which('google-chrome'))
    args=p.parse_args()
    if not args.browser_path:p.error('Provide --browser-path for an installed Chromium/Chrome executable.')
    shots=ROOT/'screenshots';shots.mkdir(exist_ok=True)
    checks=[];screens=[];errors=[];remote=[]
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}'
    catalog=json.loads((ROOT/'quality/catalog.json').read_text())
    def record(name,detail=''):
        checks.append(dict(id=f'UI-{len(checks)+1:03}',check=name,status='Passed',detail=detail))
    def capture(page,name,title,detail,full=False):
        page.evaluate('window.scrollTo(0,0)');page.wait_for_timeout(200)
        path=shots/name;page.screenshot(path=str(path),full_page=full,animations='disabled')
        screens.append(dict(file=str(path.relative_to(ROOT)),title=title,description=detail,kind='Actual local Chromium screenshot; no image generation',viewport=page.viewport_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    try:
        with sync_playwright() as w:
            browser=w.chromium.launch(executable_path=args.browser_path,headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
            context=browser.new_context(viewport={'width':1440,'height':1050},device_scale_factor=1,accept_downloads=True)
            def route(req):
                if req.request.url.startswith(base+'/'):req.continue_()
                else:remote.append(req.request.url);req.abort()
            context.route('**/*',route)
            page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
            response=page.goto(base+'/',wait_until='load');assert response.status==200
            expect(page.locator('h1')).to_have_text('Order-to-Cash overview')
            record('Root entry opens over local HTTP','200 response and rendered overview heading')
            expect(page.locator('.metrics .metric')).to_have_count(6)
            values=page.locator('.metrics .metric strong').all_text_contents()
            assert any('49.07' in x for x in values) and any('84.89' in x for x in values)
            record('Six KPI cards render expected synthetic values','49.07% on-time; 84.89% quantity fulfilment; fixed snapshot')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            record('Desktop overview fits viewport','1440 CSS pixels; no document-wide horizontal overflow')
            capture(page,'01-overview.png','Overview and KPIs','Full-cohort synthetic values and denominator limitations.',True)
            page.locator('nav [data-view="orders"]').click()
            page.locator('#order-search').fill('NS-ORD-1001')
            expect(page.locator('#order-count')).to_contain_text('1 of 300')
            page.locator('#order-table [data-order="NS-ORD-1001"]').click()
            expect(page.locator('#detail')).to_contain_text('No shipment records.')
            expect(page.locator('#detail')).to_contain_text('£2,500.00')
            record('Representative order search and detail','100 ordered; unresolved availability; no invented shipment')
            page.locator('#order-search').fill('no-such-order')
            expect(page.locator('#order-count')).to_contain_text('0 of 300')
            expect(page.locator('#order-table tbody tr')).to_have_count(0)
            record('No-result search state','Zero records without runtime exception')
            page.locator('#order-search').fill('')
            page.locator('#order-status').select_option('Cancelled')
            expect(page.locator('#order-count')).to_contain_text('17 of 300')
            with page.expect_download() as info:page.locator('#export-orders').click()
            downloaded=info.value;path=downloaded.path()
            with open(path,newline='') as f:rows=list(csv.DictReader(f))
            assert len(rows)==17 and 'order_id' in rows[0]
            record('Status filter and actual CSV download','17 cancelled orders exported, with header and expected ID column')
            page.locator('#order-status').select_option('all')
            # Select an actual synthetic invoice with at least one allocation.
            with (ROOT/'phase-08/data/allocations.csv').open() as f:a=next(csv.DictReader(f))
            with (ROOT/'phase-08/data/invoices.csv').open() as f:inv=next(x for x in csv.DictReader(f) if x['invoice_id']==a['invoice_id'])
            with (ROOT/'phase-08/data/deliveries.csv').open() as f:d=next(x for x in csv.DictReader(f) if x['delivery_id']==inv['delivery_id'])
            page.locator('#order-search').fill(d['order_id']);page.locator(f'#order-table [data-order="{d["order_id"]}"]').click()
            expect(page.locator('#detail')).to_contain_text(inv['invoice_id'])
            expect(page.locator('#detail')).to_contain_text(d['delivery_id'])
            record('Shipment/invoice/allocation drill-down','Linked synthetic records rendered for '+d['order_id'])
            capture(page,'02-order-details.png','Order drill-down','Actual synthetic '+d['order_id']+' with linked shipment, invoice and analytical payment amounts.',True)
            page.locator('nav [data-view="requirements"]').click();page.locator('#req-search').fill('FR-004')
            expect(page.locator('#req-table tbody tr')).to_have_count(1)
            page.locator('#req-table [data-req="FR-004"]').click()
            expect(page.locator('#req-detail')).to_contain_text('TC-005;TC-006')
            expect(page.locator('#req-detail')).to_contain_text('US-004')
            record('Requirement search and traceability','FR-004 → US-004 → TC-005/006 shown')
            capture(page,'03-requirements.png','Requirements and traceability','Partial-delivery requirement, acceptance criteria and linked evidence.',True)
            page.locator('nav [data-view="uat"]').click()
            expect(page.locator('details')).to_have_count(22)
            assert all(x=='Not executed' for x in page.locator('details summary .badge').all_text_contents())
            page.locator('details').filter(has=page.locator('summary',has_text='TC-005')).locator('summary').click()
            expect(page.locator('details[open]')).to_contain_text('60 fulfilled and 40 open')
            record('UAT details and honest statuses','22 cases displayed; all Not executed; actual steps/expected results expandable')
            capture(page,'04-uat.png','UAT design','Test cases are readable; status remains Not executed in SAP.')
            page.locator('nav [data-view="process"]').click()
            expect(page.locator('#process-map svg')).to_have_count(1)
            before=page.locator('#process-map').inner_text();page.locator('[data-map="tobe"]').click()
            expect(page.locator('[data-map="tobe"]')).to_have_attribute('aria-pressed','true')
            assert page.locator('#process-map').inner_text()!=before
            record('AS-IS / TO-BE flowchart switching','Two SVG process flowcharts; not BPMN or SAP screenshots')
            capture(page,'05-process.png','Proposed process flow','Actual process screen. This viewport shows the top of a scrollable full flowchart.')
            page.locator('nav [data-view="analysis"]').click()
            expect(page.locator('.chart svg')).to_have_count(1)
            expect(page.locator('#content')).to_contain_text('initial_confirmed_receipt_date')
            record('Data analysis screen','Chart, formulas and date/exclusion definitions present')
            capture(page,'06-analysis.png','Data and KPI definitions','Separate day/percentage chart and the KPI calculation contract.')
            page.locator('nav [data-view="evidence"]').click()
            expect(page.locator('#content article.panel')).to_have_count(9)
            expect(page.locator('#content')).to_contain_text('Unverified; do not use as proof')
            record('Evidence register','Nine entries including two explicitly unverified pages; external sources not opened during UI check')
            capture(page,'07-evidence.png','SAP evidence register','Reviewed documentation claims and scope limitations; no tenant execution.')
            page.locator('nav [data-view="library"]').click()
            options=page.locator('#doc-select option').all_text_contents()
            idx=options.index('phase-10/business-case.md');page.locator('#doc-select').select_option(str(idx))
            expect(page.locator('#doc-body')).to_contain_text('capacity equivalent')
            record('Document library selection','Embedded business-case document loads without network calls')
            capture(page,'08-library.png','Document library and downloads','Choose phase documents and open the full repository download assets.')
            pdf_checks=0
            for href in page.locator('#content a').evaluate_all('(xs)=>xs.map(x=>x.href)'):
                if href.startswith(base+'/'):
                    result=context.request.get(href)
                    assert result.status==200,(href,result.status)
                    pdf_checks+=href.endswith('.pdf')
            record('Library download links resolve','Local workbook, presentation, setup files and '+str(pdf_checks)+' PDFs return HTTP 200')
            # The root copy must work at GitHub Pages' repository prefix, including downloads.
            response=page.goto(base+'/northstar-otc/',wait_until='load');assert response.status==200
            expect(page.locator('h1')).to_have_text('Order-to-Cash overview')
            page.locator('nav [data-view="library"]').click()
            for link in page.locator('#content a').evaluate_all('(xs)=>xs.map(x=>x.href)'):
                if link.startswith(base+'/'):assert context.request.get(link).status==200,link
            record('GitHub-style repository subpath','/northstar-otc/ entry and relative assets tested locally; not a live GitHub deployment')
            for entry in ['/viewer/index.html','/downloads/NorthStar_Offline_Portfolio.html']:
                page.goto(base+entry,wait_until='load');expect(page.locator('h1')).to_have_text('Order-to-Cash overview')
            record('Alternative prebuilt entry points','Viewer and downloadable HTML both render over HTTP')
            page.locator('nav [data-view="orders"]').focus();page.keyboard.press('Enter')
            expect(page.locator('h1')).to_have_text('Orders & exceptions')
            record('Keyboard navigation sample','Focused native navigation button activated with Enter; not a full accessibility audit')
            page.set_viewport_size({'width':390,'height':1000})
            for view in ['overview','orders','requirements','uat','evidence','library']:
                page.locator(f'nav [data-view="{view}"]').click()
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),view+' overflows mobile viewport'
            record('Mobile layout sample','390px viewport: six screens have no document-wide horizontal overflow; wide tables scroll internally')
            page.locator('nav [data-view="overview"]').click()
            capture(page,'09-mobile.png','Mobile overview','Actual 390px Chromium viewport; not a physical-device test.')
            assert not errors,errors;record('JavaScript runtime errors','No pageerror events across the exercised paths')
            assert not remote,remote;record('Self-contained runtime','No external rendering/data requests attempted during the exercised paths')
            report=dict(executed_at_utc=datetime.now(timezone.utc).isoformat(),execution_type='Actual Playwright/Chromium local HTTP portfolio UI tests — not SAP UAT',browser=browser.version,checks=checks,screenshots=screens,passed=True,local_only=True,github_deployed=False,file_url='Not tested successfully: managed browser policy blocks file URLs; HTTP route verified',runtime_errors=errors,external_requests=remote,index_sha256=hashlib.sha256((ROOT/'index.html').read_bytes()).hexdigest(),source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['viewer/app.js','viewer/style.css']})
            (ROOT/'quality/browser-checks.json').write_text(json.dumps(report,indent=2))
            (shots/'manifest.json').write_text(json.dumps(screens,indent=2))
            browser.close()
            print(f'{len(checks)} real Chromium checks passed; {len(screens)} actual screenshots saved.')
    finally:server.shutdown();server.server_close()

if __name__=='__main__':main()
