#!/usr/bin/env python3
"""ADA importer: week-definitions + Simon's 2025 corpus → course.yaml +
vendored materials (notebooks → HTML), then the shared coursesite generator."""
import re, shutil, subprocess, html, os, datetime as dt, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).parent
SRC  = Path.home()/'Projects/research/AP2025/ada-course-materials'
DEFS = sorted((SRC/'content/week-definitions').glob('week*.md'))
SUB  = SRC/'docs/advanced_data_analytics_2025'
PREFIX = '/ada-course-materials/advanced_data_analytics_2025/'
NBC = str(Path.home()/'.local/bin/jupyter-nbconvert')
GEN = Path.home()/'Projects/research/AP2025/dsap-materials/tools/coursesite/build.py'
MAT = ROOT/'materials'
DATA_EXT = {'.gz','.zip','.tar','.pkl','.ubyte','.npz','.h5','.parquet','.7z'}
d0 = dt.date(2026,9,14); DATES = [d0 + dt.timedelta(weeks=i) for i in range(14)]
E = html.escape

def fm(path):
    m = re.match(r'---\n(.*?)\n---', path.read_text(), re.S)
    return yaml.safe_load(m.group(1)) if m else {}

def convert(nb):
    out = nb.with_suffix('.html')
    if not out.exists() or out.stat().st_mtime < nb.stat().st_mtime:
        subprocess.run([NBC,'--to','html','--embed-images','--log-level','ERROR',str(nb)], check=False)
    return out

def vendor(link, wk):
    if not link or not link.startswith(PREFIX): return None
    src = SUB/link[len(PREFIX):]
    if not src.exists(): return None
    dd = MAT/f'week-{wk:02d}'; dd.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        def _ignore(dirpath, names):
            skip=set()
            for n in names:
                p=Path(dirpath)/n
                if n in ('.ipynb_checkpoints','__pycache__','FashionMNIST','data','.DS_Store'): skip.add(n); continue
                if p.is_file() and (p.suffix.lower() in DATA_EXT or p.stat().st_size > 8_000_000): skip.add(n)
            return skip
        d = dd/src.name; shutil.copytree(src, d, dirs_exist_ok=True, ignore=_ignore)
        for nb in sorted(d.glob('*.ipynb')): convert(nb)
        listing = ''.join(f'<li><a href="{src.name}/{E(n)}">{E(n)}</a></li>' for n in sorted(os.listdir(d)) if not n.startswith('.'))
        (dd/f'{src.name}.html').write_text(f'<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="../../styles.css"><main class="wrap" style="padding:2rem"><h1>{E(src.name)}/</h1><ul>{listing}</ul><p><a href="index.html">← Week {wk}</a></p></main>')
        return f'{src.name}.html'
    dest = dd/src.name; shutil.copy2(src, dest)
    return convert(dest).name if dest.suffix == '.ipynb' else dest.name

sessions = []
for i, path in enumerate(DEFS):
    wk = i+1; f = fm(path)
    title = re.sub(r'^Week \d+:\s*','', f.get('title',''))
    noclass = 'no class' in title.lower()
    groups = []
    for key,label in [('lecture_slides','Lecture'),('ta_slides','With the TA'),('examples','Demos & notebooks'),('references','References')]:
        got=[]
        for it in (f.get(key) or []):
            if not isinstance(it, dict): continue
            v = vendor(it.get('link'), wk)
            if v: got.append({'title':it.get('title',''),'href':v,'desc':it.get('description','')})
        if got: groups.append({'label':label,'items':got})
    a = f.get('assignment')
    if isinstance(a, dict) and a.get('link'):
        v = vendor(a['link'], wk)
        if v: groups.append({'label':'Exercise sheet','items':[{'title':a.get('title',''),'href':v,'desc':a.get('description','')}]})
    body_md = re.sub(r'^---\n.*?\n---\n', '', path.read_text(), flags=re.S)
    body_md = re.sub(r'^## .*\n', '', body_md, count=1, flags=re.M)
    body_html = subprocess.run(['pandoc','-f','markdown','-t','html'], input=body_md, capture_output=True, text=True).stdout
    body_html = body_html.replace('<h3','<h4').replace('</h3>','</h4>')
    body_html = re.sub(r'<h4[^>]*>Schedule</h4>\s*<ul>.*?</ul>', '', body_html, flags=re.S)
    s = {'n':wk,'date':DATES[i].isoformat(),'title':title if not noclass else 'No class — Swiss federal fast (holiday)',
         'revealed':True,'description':f.get('description','')}
    if noclass: s['skip']=True
    else:
        s['detail']=body_html
        if 'wrap-up' in title.lower() or 'presentation' in title.lower(): s['exam']=True
    if groups:
        s['groups']=groups; s['materials']=[{'label':'Materials','href':f'materials/week-{wk:02d}/index.html'}]
    sessions.append(s)

# project documents: copy the built PDFs into the site
_pdir = ROOT/'project'
for _pdf in ('project-requirements.pdf','project-shipping-guidelines.pdf'):
    _src = _pdir/_pdf
    if _src.exists():
        (ROOT/'materials'/'project').mkdir(parents=True, exist_ok=True)
        shutil.copy2(_src, ROOT/'materials'/'project'/_pdf)
    else:
        print(f'  note: {_pdf} not built yet — run project/build.sh')

# refresher notebooks → resources fragment
ref = ROOT/'refresher'; ref.mkdir(exist_ok=True)
def _num(p):
    m = re.search(r'python_basics_(\d+)', p.stem); return int(m.group(1)) if m else 0
items=[]
for nb in sorted((SUB/'python_refresher').glob('*.ipynb'), key=_num):
    dest = ref/nb.name; shutil.copy2(nb, dest); out = convert(dest); n=_num(nb)
    nice = re.sub(r'^python_basics_\d+_','',nb.stem).replace('_',' ')
    items.append(f'<div class="row"><dt>{f"{n:02d}" if n else "start"}</dt><dd><a href="refresher/{out.name}">{E(nice)}</a></dd></div>')
(ROOT/'resources.html.frag').write_text(f'''<h2 class="sect">Python refresher</h2><dl class="mats">{''.join(items)}</dl>
<h2 class="sect" style="margin-top:2rem">Reference shelf</h2><dl class="mats">
<div class="row"><dt>pandas</dt><dd><a href="https://wesmckinney.com/book/">Python for Data Analysis, 3rd ed.</a> — McKinney<span class="ms">Free online; the pandas book by pandas' author.</span></dd></div>
<div class="row"><dt>Visualize</dt><dd><a href="https://pythontutor.com">Python Tutor</a><span class="ms">Watch code run step by step.</span></dd></div>
<div class="row"><dt>Help</dt><dd><a href="mailto:anna.smirnova@unil.ch">anna.smirnova@unil.ch</a><span class="ms">Anna Smirnova, teaching assistant — for personal matters; course questions go to the Moodle forum.</span></dd></div></dl>''')
(ROOT/'assessment.html.frag').write_text('''<dl class="mats">
<div class="row"><dt>Project</dt><dd>Final project, presented in the last session<span class="ms">A GitHub repository is required. Deadline and format announced at semester start.</span></dd></div>
<div class="row"><dt>Exercises</dt><dd>Exercise sheets and finger exercises with the TA<span class="ms">Practice, discussed in the practice sessions.</span></dd></div>
<div class="row"><dt>Also on Moodle</dt><dd>Everything on this page is posted on the course Moodle as well<span class="ms">Exam and project announcements are published on Moodle and here at the same time. If the two ever differ, Moodle is the official channel.</span></dd></div>
<div class="row"><dt>Binding terms</dt><dd>The study plan<span class="ms">In the event of an appeal, only the study plan (plan d'études) is binding. This page summarizes the intended terms.</span></dd></div></dl>''')

cfg = {'id':'ada','title':'Advanced Data Analytics','tagline':'Machine learning for economics and finance — from regression to reinforcement learning.',
 'semester':'Autumn semester 2026','semester_short':'Autumn 2026','contact_email':'anna.smirnova@unil.ch','accent':'#317e43','show_part':False,
 'moodle_url':'https://moodle.unil.ch','resources_label':'Python refresher &amp; resources','resources_title':'Python refresher &amp; resources',
 'resources_tagline':'Twelve short notebooks, readable in the browser — from calculator to pandas.','assessment_tagline':'Provisional — confirmed at semester start.',
 'schedule_note':'Dates are the provisional 2026 calendar; materials are the current course corpus and may be updated week by week.',
 'facts':[{'h':'Meets','p':'Mondays, from Sep 14','note':'2026 dates provisional · lecture + practice'},
          {'h':'Grading','p':'Final project','note':'Details confirmed at semester start'},
          {'h':'Prerequisites','p':'Python basics','note':'<a href="resources.html">Refresher notebooks</a> if you need them'},
          {'h':'Compute','p':'<a href="https://nuvolos.cloud">Nuvolos</a> cloud workspaces','note':'Free for enrolled students'}],
 'nuvolos':{'enroll_url':'https://app.nuvolos.cloud','login_url':'https://app.nuvolos.cloud','blurb':'VS Code and JupyterLab in the browser — nothing to install. Enroll with your UNIL email once; then log in from any computer.'},
 'assessment_html':'assessment.html.frag','resources_html':'resources.html.frag',
 'pages':[{'slug':'project','label':'Project','title':'The semester project',
           'tagline':'One project, carried out individually — the whole assessment for this course.',
           'html':'project.html.frag'}],
 'sessions':sessions}
yaml.safe_dump(cfg, open(ROOT/'course.yaml','w'), allow_unicode=True, sort_keys=False, width=100)
subprocess.run([sys.executable, str(GEN), str(ROOT/'course.yaml'), str(ROOT)], check=True)
