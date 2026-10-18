"""Build readable PDF explanations and a detailed portfolio reference using free ReportLab.

Screenshots are included only when an actual browser-check manifest exists.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import csv,json,re,subprocess,shutil
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image,Preformatted,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from browser_evidence import current_browser_evidence

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'downloads';OUT.mkdir(exist_ok=True)
FONT=Path('/usr/share/fonts/truetype/dejavu')
if (FONT/'DejaVuSans.ttf').exists():
    pdfmetrics.registerFont(TTFont('NorthStar',str(FONT/'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('NorthStar-Bold',str(FONT/'DejaVuSans-Bold.ttf')))
    pdfmetrics.registerFontFamily('NorthStar',normal='NorthStar',bold='NorthStar-Bold',italic='NorthStar',boldItalic='NorthStar-Bold')
    regular,bold='NorthStar','NorthStar-Bold'
else:regular,bold='Helvetica','Helvetica-Bold'
styles=getSampleStyleSheet()
for name in styles.byName:styles[name].fontName=regular
styles.add(ParagraphStyle(name='NSBody',fontName=regular,fontSize=9,leading=14,spaceAfter=7,textColor=colors.HexColor('#213547'),splitLongWords=True))
styles.add(ParagraphStyle(name='NSH1',fontName=bold,fontSize=20,leading=26,spaceBefore=10,spaceAfter=12,keepWithNext=True,textColor=colors.HexColor('#112b42')))
styles.add(ParagraphStyle(name='NSH2',fontName=bold,fontSize=13,leading=18,spaceBefore=13,spaceAfter=8,keepWithNext=True,textColor=colors.HexColor('#087e8b')))
styles.add(ParagraphStyle(name='NSH3',fontName=bold,fontSize=10,leading=15,spaceBefore=9,spaceAfter=6,keepWithNext=True))
styles.add(ParagraphStyle(name='NSTitle',fontName=bold,fontSize=29,leading=37,spaceAfter=20,textColor=colors.HexColor('#112b42')))
styles.add(ParagraphStyle(name='NSCaption',fontName=regular,fontSize=8,leading=12,spaceAfter=10,textColor=colors.HexColor('#526476')))
styles.add(ParagraphStyle(name='NSCell',fontName=regular,fontSize=7.5,leading=11,spaceAfter=2,splitLongWords=True))
styles.add(ParagraphStyle(name='NSCode',fontName='Courier',fontSize=7.5,leading=11,spaceAfter=9))
WIDTH=A4[0]-84
def inline(text):
    text=escape(text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'`([^`]+)`',r'<font name="Courier">\1</font>',text)
    text=re.sub(r'\[([^]]+)\]\(([^)]+)\)',lambda m: '<link href="'+m[2]+'" color="#087e8b">'+m[1]+'</link>' if m[2].startswith('http') else m[1]+' ('+m[2]+')',text)
    return text
def para(text,sty='NSBody'):return Paragraph(inline(text),styles[sty])
def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#dce4eb'));canvas.line(42,37,A4[0]-42,37)
    canvas.setFont(regular,7);canvas.setFillColor(colors.HexColor('#526476'))
    canvas.drawString(42,25,'NorthStar · Independent simulated portfolio · No SAP UAT executed')
    canvas.drawRightString(A4[0]-42,25,str(doc.page))
def imageflow(path,maxheight=590):
    w,h=ImageReader(str(path)).getSize();scale=min(WIDTH/w,maxheight/h)
    return Image(str(path),width=w*scale,height=h*scale)
def istable_sep(line):return all(re.fullmatch(':?-+:?',x.strip()) for x in line.strip().strip('|').split('|'))
def table(rows):
    data=[[para(c,'NSCell') for c in row] for row in rows]
    widths=[WIDTH/len(rows[0])]*len(rows[0])
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8eff5')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#cad5df')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t
def markdown(path):
    out=[];lines=path.read_text().splitlines();i=0
    while i<len(lines):
        line=lines[i]
        if line.startswith('```'):
            language=line[3:];block=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
            if language=='mermaid':out.append(para('Full process flowchart is provided in the diagram appendix and as editable .mmd/.dot and zoomable .svg files. This is not BPMN.','NSCaption'))
            else:
                out.append(Preformatted('\n'.join(block),styles['NSCode']))
        elif line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                if not istable_sep(lines[i]):rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i+=1
            if len(rows[0])<=4:out.append(table(rows));out.append(Spacer(1,10))
            else:
                for row in rows[1:]:
                    out.append(para(row[0],'NSH3'))
                    for key,value in zip(rows[0][1:],row[1:]):out.append(para('**'+key+':** '+value))
            continue
        elif line.startswith('#'):
            level=len(line)-len(line.lstrip('#'));out.append(para(line.lstrip('# '),'NSH1' if level==1 else 'NSH2' if level==2 else 'NSH3'))
        elif line.strip():out.append(para(line.lstrip('> ')))
        i+=1
    return out
def title(text,sub):return [Spacer(1,40),para('NORTHSTAR MANUFACTURING UK','NSCaption'),para(text,'NSTitle'),para(sub),para('Handover: 12 October 2026 · Synthetic baseline: 11 October 2026\nIndependent simulated portfolio · Free-tool route'),Spacer(1,20)]
class BookmarkedDoc(SimpleDocTemplate):
    def afterFlowable(self,flowable):
        if isinstance(flowable,Paragraph) and flowable.style.name in ['NSTitle','NSH1','NSH2']:
            self._bookmark_count=getattr(self,'_bookmark_count',0)+1
            key='section-'+str(self._bookmark_count)
            level=1 if flowable.style.name=='NSH2' else 0
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(),key,level=level,closed=False)
def build(name,story):
    doc=BookmarkedDoc(str(OUT/name),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=48,title=name.replace('_',' ').replace('.pdf',''),author='AI-assisted independent portfolio',subject='Simulated business analysis and local application handover')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)

browser=current_browser_evidence()
guide=title('Project guide &\nreal UI screenshots','What was built, what runs locally, what is simulated, and how to put the whole project on GitHub.')
guide += [para('**Built:** a read-only interactive portfolio plus all twelve phases of draft analysis artifacts.'),para('**Not built:** a live SAP implementation or a transactional ERP backend. Learning review and real business acceptance remain open.'),para('Start with the overview, then follow the local and GitHub steps. The companion Full Portfolio PDF contains the detailed catalogues; editable sources and raw data stay in the repository.'),PageBreak()]
guide+=markdown(ROOT/'PROJECT_GUIDE.md')
guide+=[PageBreak(),para('Real browser verification','NSH1')]
if browser:
    guide += [para(f'{len(browser["checks"])} real Chromium checks passed. Browser {browser["browser"]}. Execution timestamp (UTC): {browser["executed_at_utc"]}.'),para('Tests exercised the portfolio over HTTP on a temporary loopback server. No GitHub deployment or SAP UAT occurred. Screenshots are direct browser captures; they are not generated concept artwork.'),table([['Check','Result']]+[[x['check'],x['status']] for x in browser['checks']])]
    for shot in browser['screenshots']:
        guide += [PageBreak(),para(shot['title'],'NSH1'),para(shot['description'],'NSCaption'),imageflow(ROOT/shot['file']),Spacer(1,8),para('Actual local Chromium UI · '+shot['file']+' · Read-only simulated portfolio, not SAP software. Open the PNG or zoom the PDF for fine text.','NSCaption')]
else:guide += [para('A full current-source browser-check record is not yet available. This preliminary PDF does not claim completed screenshot verification. Run browser_check.py and regenerate this PDF to include actual captures.')]
guide += [PageBreak()]+markdown(ROOT/'RUN_LOCALLY.md')+[PageBreak()]+markdown(ROOT/'GITHUB_SETUP.md')
build('NorthStar_Project_Guide.pdf',guide)

full=title('Full portfolio\nreference','Twelve-phase narrative and learning pack, followed by detailed requirements, stories, tests, evidence, data definitions and control catalogues.')
full += [para('This PDF is a reading reference. The repository contains the executable scripts, complete raw synthetic records and editable formats. CSVs are authoritative tabular artifacts; no real records, stakeholder approvals or SAP test results are fabricated.'),para('Contents: project orientation; phases 1–12 and learning reviews; maintained registers; quality gate; process diagrams; catalogue appendices. Use your PDF reader’s bookmarks sidebar to jump to a section. Root README gives the file index.'),PageBreak()]
paths=[ROOT/'PROJECT_GUIDE.md']+sorted(ROOT.glob('phase-*/*.md'))+sorted(ROOT.glob('registers/*.md'))+[ROOT/'quality/final-quality-gate.md']
for i,path in enumerate(paths):
    if i:full.append(PageBreak())
    full.append(para(str(path.relative_to(ROOT)),'NSCaption'));full+=markdown(path)
for folder,name in [('phase-03','as-is'),('phase-05','to-be')]:
    dot=ROOT/f'{folder}/{name}.dot';png=ROOT/f'{folder}/{name}.png'
    if shutil.which('dot'):subprocess.run(['dot','-Tpng','-Gdpi=120',str(dot),'-o',str(png)],check=True)
    if png.exists():full += [PageBreak(),para(name.upper()+' process flowchart','NSH1'),para('Entire diagram for orientation. Use the supplied SVG for readable zoom. This is a flowchart, not BPMN.','NSCaption'),imageflow(png,640)]
appendices=[('Business requirements and acceptance','phase-04/requirements.csv'),('Rules','phase-04/business-rules.csv'),('Traceability','phase-04/traceability.csv'),('Non-functional test links','phase-04/nonfunctional-trace.csv'),('Access matrix','phase-04/access-matrix.csv'),('Discovery findings','phase-02/discovery-findings.csv'),('Responsibilities','phase-02/responsibility-matrix.csv'),('AS-IS step register','phase-03/as-is-step-register.csv'),('SAP evidence','phase-05/sap-evidence.csv'),('Fit-gap','phase-06/fit-gap.csv'),('User stories','phase-07/backlog.csv'),('UAT case designs','phase-09/uat-cases.csv'),('KPI definitions','phase-08/kpi-contract.csv'),('Data model','phase-08/data-model.csv'),('Data dictionary','phase-08/data-dictionary.csv'),('Risks','phase-10/risks.csv'),('Change and training','phase-10/change-impact.csv'),('Business-case options','phase-10/business-case-options.csv'),('Sensitivity','phase-10/sensitivity.csv'),('Executed data checks','phase-08/data/data_checks.csv'),('Executed catalogue checks','quality/consistency-checks.csv')]
for heading,path in appendices:
    with (ROOT/path).open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
    full += [PageBreak(),para('Appendix — '+heading,'NSH1'),para('Editable source: '+path,'NSCaption')]
    for idx,row in enumerate(rows):
        key=next(iter(row));full.append(para(f'{idx+1}. {row[key]}','NSH3'))
        for k,v in row.items():
            if v:full.append(para('**'+k.replace('_',' ')+':** '+v))
build('NorthStar_Full_Portfolio.pdf',full)
print('Built explanatory/screenshots PDF and detailed full-portfolio PDF.')
