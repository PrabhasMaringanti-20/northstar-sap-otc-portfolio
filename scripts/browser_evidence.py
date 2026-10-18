"""Read browser evidence only when it matches the current UI source files."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def current_browser_evidence():
    file=ROOT/'quality/browser-checks.json'
    if not file.exists():return None
    evidence=json.loads(file.read_text())
    if not evidence.get('passed'):return None
    for name,expected in evidence.get('source_sha256',{}).items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected:return None
    if not evidence.get('source_sha256'):return None
    return evidence
