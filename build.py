#!/usr/bin/env python3
"""Build the ADA static site from the 2025 week definitions + Simon's
material corpus. Vendors linked files into materials/week-NN/, converts
notebooks to HTML, generates index/assessment/resources + week pages."""
import re, shutil, subprocess, html, os, glob, datetime as dt
from pathlib import Path
import yaml

ROOT = Path(__file__).parent
SRC  = Path.home()/'Projects/research/AP2025/ada-course-materials'
DEFS = sorted((SRC/'content/week-definitions').glob('week*.md'))
SUB  = SRC/'docs/advanced_data_analytics_2025'
PREFIX = '/ada-course-materials/advanced_data_analytics_2025/'
NBC = str(Path.home()/'.local/bin/jupyter-nbconvert')
MAT = ROOT/'materials'
DATA_EXT = {'.gz','.zip','.tar','.pkl','.ubyte','.npz','.h5','.parquet','.7z'}

# ---- 2026 provisional Mondays: Sep 14 start, Sep 21 holiday, 14 rows
d0 = dt.date(2026,9,14)
DATES = [d0 + dt.timedelta(weeks=i) for i in range(14)]

def fm(path):
    t = path.read_text()
    m = re.match(r'---\n(.*?)\n---', t, re.S)
    return yaml.safe_load(m.group(1)) if m else {}

def vendor(link, wk):
    """Copy a linked file/dir into materials/week-NN/; return (href, kind)."""
    if not link or not link.startswith(PREFIX): return None
    rel = link[len(PREFIX):]
    src = SUB/rel
    if not src.exists(): return None
    dest_dir = MAT/f'week-{wk:02d}'
    dest_dir.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        d = dest_dir/src.name
        def _ignore(dirpath, names):
            skip = set()
            for n in names:
                p = Path(dirpath)/n
                if n in ('.ipynb_checkpoints','__pycache__','FashionMNIST','data','.DS_Store'): skip.add(n); continue
                if p.is_file() and (p.suffix.lower() in DATA_EXT or p.stat().st_size > 8_000_000): skip.add(n)
            return skip
        shutil.copytree(src, d, dirs_exist_ok=True, ignore=_ignore)
        items = []
        for nb in sorted(d.glob('*.ipynb')):
            out = convert(nb)
            items.append(out.name)
        # folder listing page
        listing = ''.join(f'<li><a href="{src.name}/{html.escape(n)}">{html.escape(n)}</a></li>'
                          for n in sorted(os.listdir(d)) if not n.startswith('.'))
        (dest_dir/f'{src.name}.html').write_text(page(f'{src.name}/', f'<ul>{listing}</ul>', crumb=f'Week {wk}'))
        return (f'{src.name}.html', 'folder')
    dest = dest_dir/src.name
    shutil.copy2(src, dest)
    if dest.suffix == '.ipynb':
        out = convert(dest)
        return (out.name, 'notebook')
    return (dest.name, dest.suffix.lstrip('.'))

def convert(nb: Path):
    out = nb.with_suffix('.html')
    if not out.exists() or out.stat().st_mtime < nb.stat().st_mtime:
        subprocess.run([NBC,'--to','html','--embed-images','--log-level','ERROR',str(nb)],
                       check=False)
    return out

# ---- page shell
def shell(title, body, cur='', depth=0):
    p = '../'*depth
    nav = lambda k,h,t: f'<a href="{p}{h}"{" aria-current=\"page\"" if cur==k else ""}>{t}</a>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — Advanced Data Analytics, UNIL HEC</title>
<link rel="stylesheet" href="{p}styles.css"></head><body>
<header class="sig"><div class="wrap">
<img src="{p}assets/logos/unil-logo-blue.svg" alt="UNIL"><span class="fac">HEC Lausanne</span>
<span class="sem">Autumn semester 2026</span></div></header>
<nav class="nav"><div class="wrap">{nav('index','index.html','Schedule')}{nav('assessment','assessment.html','Assessment')}{nav('resources','resources.html','Python refresher &amp; resources')}</div></nav>
{body}
<footer><div class="wrap"><img src="{p}assets/logos/unil-logo-white.svg" alt="UNIL">
<span>HEC Lausanne · Autumn 2026</span><a href="mailto:anna.smirnova@unil.ch">Contact the team</a>
<span class="nuv"><!-- Nuvolos branding required (free compute credits) — do not remove -->Compute by <a href="https://nuvolos.cloud">Nuvolos</a></span></div></footer>
<script src="{p}site.js"></script></body></html>'''

def page(title, inner, crumb=''):
    body = f'''<div class="wk-mast"><div class="wrap"><p class="crumb"><a href="../../index.html">Advanced Data Analytics</a> · {html.escape(crumb)}</p>
<h1>{html.escape(title)}</h1></div></div><main><div class="wrap">{inner}
<nav class="pager"><a href="../../index.html"><span class="lbl">← Back</span><b>Schedule</b></a></nav></div></main>'''
    return shell(title, body, depth=2)

# ---- build weeks
rows = []
for i, path in enumerate(DEFS):
    wk = i+1
    f = fm(path)
    title = re.sub(r'^Week \d+:\s*','', f.get('title',''))
    date = DATES[i]
    noclass = 'no class' in title.lower()
    groups = []
    for key,label in [('lecture_slides','Lecture'),('ta_slides','With the TA'),('examples','Demos & notebooks'),('references','References')]:
        items = f.get(key) or []
        got = []
        for it in items:
            if not isinstance(it, dict): continue
            v = vendor(it.get('link'), wk)
            if v: got.append((it.get('title',''), v[0], it.get('description','')))
        if got: groups.append((label, got))
    a = f.get('assignment')
    if isinstance(a, dict) and a.get('link'):
        v = vendor(a['link'], wk)
        if v: groups.append(('Exercise sheet', [(a.get('title',''), v[0], a.get('description',''))]))
    # week page
    if groups:
        inner = f'<p class="cando" style="font-style:normal;font-size:1rem;color:var(--ink-2)">{html.escape(f.get("description",""))}</p>'
        for label, got in groups:
            inner += f'<h2 class="sect" style="margin-top:1.6rem">{label}</h2><dl class="mats">'
            for t,h,dsc in got:
                inner += f'<div class="row"><dt></dt><dd><a href="{html.escape(h)}">{html.escape(t)}</a>'
                if dsc: inner += f'<span class="ms">{html.escape(dsc)}</span>'
                inner += '</dd></div>'
            inner += '</dl>'
        (MAT/f'week-{wk:02d}'/'index.html').write_text(page(f'Week {wk}: {title}', inner, crumb=f'Week {wk}'))
    mat_cell = (f'<a href="materials/week-{wk:02d}/index.html">Materials</a>' if groups
                else '<span class="tba">—</span>')
    cls = 'session exam' if ('wrap-up' in title.lower() or 'presentation' in title.lower()) else 'session'
    q = html.escape(title) if not noclass else 'No class — Swiss federal fast (holiday)'
    skip = ' data-skip="1"' if noclass else ''
    rows.append(f'<tr class="{cls}" id="s{wk:02d}" data-date="{date.isoformat()}"{skip}><td class="wk">{wk:02d}</td><td class="wk">{date.strftime("%b %-d")}</td>'
                f'<td class="q">{q}</td><td class="mat">{mat_cell}</td></tr>')
    # detail row: week body (objectives/topics) via pandoc + materials mirror
    body_md = re.sub(r'^---\n.*?\n---\n', '', path.read_text(), flags=re.S)
    body_md = re.sub(r'^## .*\n', '', body_md, count=1, flags=re.M)
    body_html = subprocess.run(['pandoc','-f','markdown','-t','html'], input=body_md, capture_output=True, text=True).stdout
    body_html = body_html.replace('<h3', '<h4').replace('</h3>', '</h4>')
    body_html = re.sub(r'<h4[^>]*>Schedule</h4>\s*<ul>.*?</ul>', '', body_html, flags=re.S)  # 2025 dates
    if not noclass:
        rows.append(f'<tr class="detail"><td colspan="4"><div class="d-wrap"><div class="d-in"><div class="d-body">{body_html}<h4>Materials</h4><div class="d-mat"></div></div></div></div></td></tr>')

# ---- refresher page (Simon's 12 notebooks → HTML)
ref = ROOT/'refresher'; ref.mkdir(exist_ok=True)
ref_items = []
def _num(p):
    m = re.search(r'python_basics_(\d+)', p.stem)
    return int(m.group(1)) if m else 0
for nb in sorted((SUB/'python_refresher').glob('*.ipynb'), key=_num):
    dest = ref/nb.name; shutil.copy2(nb, dest); out = convert(dest)
    n = _num(nb)
    nice = re.sub(r'^python_basics_\d+_', '', nb.stem).replace('_',' ')
    label = f'{n:02d}' if n else 'start'
    ref_items.append(f'<div class="row"><dt>{label}</dt><dd><a href="refresher/{out.name}">{html.escape(nice)}</a></dd></div>')

# ---- top pages
index_body = f'''<div class="mast"><div class="wrap"><h1>Advanced Data Analytics</h1>
<p class="sub">Machine learning for economics and finance — from regression to reinforcement learning.</p></div></div>
<div class="facts"><div class="wrap">
<section><h2>Meets</h2><p>Mondays, from Sep 14</p><p class="note">2026 dates provisional · lecture + practice</p></section>
<section><h2>Grading</h2><p>Final project</p><p class="note">Details confirmed at semester start</p></section>
<section><h2>Prerequisites</h2><p>Python basics</p><p class="note"><a href="resources.html">Refresher notebooks</a> if you need them</p></section>
<section><h2>Compute</h2><p><a href="https://nuvolos.cloud">Nuvolos</a> cloud workspaces</p><p class="note">Free for enrolled students</p></section>
</div></div>
<main><div class="wrap"><h2 class="sect">Schedule</h2>
<p style="margin-bottom:0.9rem;color:var(--ink-2);font-size:0.93rem">Dates are the provisional 2026 calendar; materials are the current course corpus and may be updated week by week.</p>
<table class="sched"><thead><tr><th>#</th><th>Date</th><th>Topic</th><th>Materials</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table></div></main>'''
(ROOT/'index.html').write_text(shell('Schedule', index_body, cur='index'))

assess_body = '''<div class="wk-mast"><div class="wrap"><p class="crumb"><a href="index.html">Advanced Data Analytics</a> · Assessment</p>
<h1>Assessment</h1><p class="q">Provisional — confirmed at semester start.</p></div></div>
<main><div class="wrap"><dl class="mats">
<div class="row"><dt>Project</dt><dd>Final project, presented in the last session<span class="ms">A GitHub repository is required. Deadline and format announced at semester start.</span></dd></div>
<div class="row"><dt>Exercises</dt><dd>Exercise sheets and finger exercises with the TA<span class="ms">Practice, discussed in the practice sessions.</span></dd></div>
<div class="row"><dt>Binding terms</dt><dd>The study plan<span class="ms">In the event of an appeal, only the study plan (plan d'études) is binding. This page summarizes the intended terms.</span></dd></div>
</dl><nav class="pager"><a href="index.html"><span class="lbl">← Back</span><b>Schedule</b></a></nav></div></main>'''
(ROOT/'assessment.html').write_text(shell('Assessment', assess_body, cur='assessment'))

res_body = f'''<div class="wk-mast"><div class="wrap"><p class="crumb"><a href="index.html">Advanced Data Analytics</a> · Resources</p>
<h1>Python refresher &amp; resources</h1><p class="q">Twelve short notebooks, readable in the browser — from calculator to pandas.</p></div></div>
<main><div class="wrap"><h2 class="sect">Python refresher</h2><dl class="mats">{''.join(ref_items)}</dl>
<h2 class="sect" style="margin-top:2rem">Reference shelf</h2><dl class="mats">
<div class="row"><dt>pandas</dt><dd><a href="https://wesmckinney.com/book/">Python for Data Analysis, 3rd ed.</a> — McKinney<span class="ms">Free online; the pandas book by pandas' author.</span></dd></div>
<div class="row"><dt>Visualize</dt><dd><a href="https://pythontutor.com">Python Tutor</a><span class="ms">Watch code run step by step.</span></dd></div>
<div class="row"><dt>Help</dt><dd><a href="mailto:anna.smirnova@unil.ch">anna.smirnova@unil.ch</a><span class="ms">Anna Smirnova, teaching assistant — for personal matters; course questions go to the Moodle forum.</span></dd></div>
</dl><nav class="pager"><a href="index.html"><span class="lbl">← Back</span><b>Schedule</b></a></nav></div></main>'''
(ROOT/'resources.html').write_text(shell('Resources', res_body, cur='resources'))
print('built:', len(rows), 'weeks;', len(ref_items), 'refresher notebooks')
