"""Package the current repository; no build, network, Git push or deployment."""
from pathlib import Path
import zipfile,hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'downloads'
from browser_evidence import current_browser_evidence
browser=current_browser_evidence()
if browser:
    artifact_path=ROOT/'quality/artifact-checks.json'
    artifact=json.loads(artifact_path.read_text()) if artifact_path.exists() else {}
    artifact['handover_updated']='2026-10-12'
    artifact['browser_evidence']='quality/browser-checks.json'
    artifact['browser_checks_passed']=len(browser['checks'])
    artifact['actual_screenshots']=len(browser['screenshots'])
    artifact['tested_html_matches_release']=hashlib.sha256((ROOT/'index.html').read_bytes()).hexdigest()==browser['index_sha256']
    artifact['visual_limit']='Actual local Chromium checked; other browsers, physical devices, comprehensive accessibility and LibreOffice visual rendering not verified.'
    artifact_path.write_text(json.dumps(artifact,indent=2))
files=[]
for f in sorted(ROOT.rglob('*')):
    if not f.is_file() or f.suffix in ['.zip','.sha256','.pyc'] or any(p in f.parts for p in ['__pycache__','.git','.venv']):continue
    if f.parent==OUT and f.name.startswith('NorthStar_Phase_1'):continue
    if 'downloads/csv/' in str(f) or f.name=='initial-overview.png':continue
    files.append(f)
for name in ['NorthStar_Complete_Portfolio.zip','NorthStar_GitHub_Ready.zip']:
    archive=OUT/name
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for f in files:z.write(f,Path('northstar-otc')/f.relative_to(ROOT))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert 'northstar-otc/index.html' in z.namelist()
        assert 'northstar-otc/.nojekyll' in z.namelist()
    archive.with_suffix('.sha256').write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
print(f'Packaged {len(files)} files in complete and GitHub-ready ZIPs; integrity verified.')
