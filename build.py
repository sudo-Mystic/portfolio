#!/usr/bin/env python3
"""Build Rishabh's portfolio from the reference template. Output -> dist/"""
import re, os, shutil, subprocess

HOME = os.path.expanduser('~')
REF = f'{HOME}/workspace/portfolio-site/ref'
BUILD = f'{HOME}/workspace/portfolio-site/build'
DIST = f'{HOME}/workspace/portfolio-site/dist'

GITHUB = 'https://github.com/sudo-Mystic'
LINKEDIN = 'https://www.linkedin.com/in/rishabh-b-90303b245'
EMAIL = 'mrmysticuniverse@gmail.com'
SIM_URL = 'https://sudo-mystic.github.io/Scoot-releases/sim/'
CANONICAL = 'https://sudo-mystic.github.io/portfolio/'

try:
    COMMIT = subprocess.check_output(
        ['git', '-C', f'{HOME}/workspace/portfolio-site', 'rev-parse', '--short', 'HEAD'],
        text=True).strip()
except Exception:
    COMMIT = 'main'

# ---------- assets ----------
shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(f'{DIST}/assets', exist_ok=True)
for f in ['2zq26fv-w3ylr.css', '3197uc4c-hv2_.css', '2ircu5rqc450t.css']:
    shutil.copy(f'{REF}/{f}', f'{DIST}/assets/{f}')
shutil.copy(f'{REF}/70bc3e132a0a741e-s.p.269kn9uafm0ti.woff2', f'{DIST}/assets/font.woff2')

# logo: resize generated art to 256 and 64
from PIL import Image
logo_src = None
for f in os.listdir(BUILD):
    if f.startswith('media-generation-mystic-logo') and f.endswith('.webp'):
        logo_src = f'{BUILD}/{f}'
        break
assert logo_src, 'logo not found'
im = Image.open(logo_src).convert('RGB')
im.resize((256, 256), Image.LANCZOS).save(f'{DIST}/logo-256.webp', 'WEBP', quality=90)
im.resize((64, 64), Image.LANCZOS).save(f'{DIST}/logo-64.webp', 'WEBP', quality=90)
shutil.copy(f'{DIST}/logo-256.webp', f'{DIST}/apple-touch-icon.webp')

# ---------- base template ----------
html = open(f'{REF}/main.html').read()

def sub(old, new, count=1):
    global html
    assert old in html, f'NOT FOUND: {old[:70]}'
    html = html.replace(old, new, count)

def resub(pat, new):
    global html
    html, n = re.subn(pat, new, html, flags=re.S)
    return n

# strip ALL their scripts (their JS is React flight data + chunks; we ship our own site.js)
resub(r'<script[^>]*>.*?</script>\s*', '')
resub(r'<link rel="preload" as="script"[^>]*>\s*', '')

# ---- head ----
sub('<title>Mohd Maaz Khan · maaz.code</title>', '<title>Rishabh Bohra · mystic.code</title>')
sub('<meta name="author" content="Mohd Maaz Khan"/>', '<meta name="author" content="Rishabh Bohra"/>')
sub('<link rel="author" href="https://github.com/maaz7409"/>', f'<link rel="author" href="{GITHUB}"/>')
sub('<link rel="canonical" href="https://maaza-codes.vercel.app"/>', f'<link rel="canonical" href="{CANONICAL}"/>')
m = re.search(r'<meta name="description" content="[^"]*"', html)
html = html.replace(m.group(0), '<meta name="description" content="Rishabh Bohra — embedded systems, mobile apps, security research."')
for css in ['2zq26fv-w3ylr.css', '3197uc4c-hv2_.css', '2ircu5rqc450t.css']:
    sub(f'href="/_next/static/chunks/{css}"', f'href="@root/assets/{css}"')
sub('href="/_next/static/media/70bc3e132a0a741e-s.p.269kn9uafm0ti.woff2"', 'href="@root/assets/font.woff2"')
sub('<link rel="preload" as="image" href="/logo-64.webp"/>', '')
sub('<link rel="preload" href="/logo-256.webp" as="image"/>', '')
m = re.search(r'<link rel="icon"[^>]*>', html)
if m: html = html.replace(m.group(0), '<link rel="icon" href="@root/logo-64.webp" type="image/webp"/>')
m = re.search(r'<link rel="apple-touch-icon"[^>]*>', html)
if m: html = html.replace(m.group(0), '<link rel="apple-touch-icon" href="@root/apple-touch-icon.webp"/>')
sub('</head>', '<script src="@root/assets/site.js" defer></script>\n</head>')

# ---- chrome ----
sub('src="/logo-64.webp" width="18" height="18" alt="maaz.code logo"', 'src="@root/logo-64.webp" width="18" height="18" alt="mystic.code logo"')
sub('src="/logo-256.webp" width="56" height="56" alt="maaz.code logo"', 'src="@root/logo-256.webp" width="56" height="56" alt="mystic.code logo"')
sub('<h1 class="text-4xl font-light tracking-tight text-tab-active-fg max-md:text-3xl">Mohd Maaz Khan</h1>',
    '<h1 class="text-4xl font-light tracking-tight text-tab-active-fg max-md:text-3xl">Rishabh Bohra</h1>')
sub('B.Tech Chemical Engineering · ML / Scientific Computing',
    'B.Tech undergrad at IET DAVV · Embedded / Mobile / Security')
sub('Chemical Engineering undergrad at IIT (ISM) Dhanbad working on Machine Learning and Scientific Computing.',
    'I build things and break things to understand them. Microcontrollers, Flutter apps shipped to real users, and Android apps taken apart for security research.')

# ---- boot lines ----
sub('maaz.code: booting', 'mystic.code: booting')
sub('Mounted /home/maaz (18 files)', 'Mounted /home/rishabh (12 files)')
sub('Indexed 5 projects and 5 notebooks', 'Indexed 4 projects, shipped 2')
sub('Linked 16 merged pull requests', 'Linked 1 merged pull request')
sub('Started lorenz.service (σ=10, ρ=28, β=8/3)', 'Paired with Jupiter cluster over BLE')

# ---- start section ----
sub('href="/README.md"', 'href="@root/readme/"')
sub('href="/simple"', 'href="@root/simple/"')
# churn_predictor.py appears 3x: Start "Run a simulation", Recent list, Walkthrough card.
# For Rishabh: Start + Walkthrough -> sim URL; Recent -> detroit-jev page.
occ = [m.start() for m in re.finditer(r'href="/projects/churn_predictor\.py"', html)]
assert len(occ) == 3, f'expected 3 churn hrefs, found {len(occ)}'
# replace from last to first to keep indices valid
html = html[:occ[2]] + f'href="{SIM_URL}" target="_blank" rel="noreferrer"' + html[occ[2]+len('href="/projects/churn_predictor.py"'):]
html = html[:occ[1]] + 'href="@root/projects/detroit-jev/"' + html[occ[1]+len('href="/projects/churn_predictor.py"'):]
html = html[:occ[0]] + f'href="{SIM_URL}" target="_blank" rel="noreferrer"' + html[occ[0]+len('href="/projects/churn_predictor.py"'):]
sub('>Run a simulation<', '>Run the sim<')
# View open-source contributions button -> GitHub link
sub('View open-source contributions', 'View open-source contributions')
# Download resume row: remove the whole <li>
m = re.search(r'<li>\s*<a[^>]*href="/resume"[^>]*>.*?</a>\s*</li>', html, re.S)
assert m, 'resume row not found'
html = html.replace(m.group(0), '')
sub(f'href="mailto:kmaaz7256@gmail.com"', f'href="mailto:{EMAIL}"')
sub('>kmaaz7256@gmail.com<', f'>{EMAIL}<')
sub('href="https://github.com/maaz7409"', f'href="{GITHUB}"')
sub('https://www.linkedin.com/in/maaz-khan-63100b313', LINKEDIN)

# ---- recent ----
recent = [
    ('enterprise_rag.py', 'Enterprise RAG System with LLM-as-a-Judge', '/projects/enterprise_rag.py',
     'scoot.dart', 'Flutter companion app for TVS smart scooters', '@root/projects/scoot/'),
    ('heat_pinn.ipynb', 'Inverse Heat Transfer with PINNs', '/research/heat_pinn.ipynb',
     'esp_reddit.cpp', 'Reddit API wrapper for ESP32', '@root/projects/esp-reddit/'),
    ('email_classifier.py', 'Automated Email Classification Engine', '/projects/email_classifier.py',
     'exam_eval.md', 'AI examination evaluation platform', '@root/projects/exam-eval/'),
]
# churn_predictor name/desc handled separately (href done positionally above)
sub('>churn_predictor.py<', '>detroit_jev.py<')
sub('E-Commerce Customer Churn Prediction', 'AI plays Detroit: Become Human, all 226 decisions')
for old_name, old_desc, old_href, new_name, new_desc, new_href in recent:
    sub(f'>{old_name}<', f'>{new_name}<')
    sub(old_desc, new_desc)
    sub(f'href="{old_href}"', f'href="{new_href}"')
# notebook icon for heat_pinn -> keep as file-code (cpp); swap icon class
sub('codicon-notebook text-syntax-string " aria-hidden="true"></span><span class="truncate ">esp_reddit.cpp',
    'codicon-file-code text-syntax-function " aria-hidden="true"></span><span class="truncate ">esp_reddit.cpp')

# ---- walkthroughs ----
sub('Run the research', 'Run the sim')
sub('Notebooks marked ▶ launch live physics simulations in your browser.',
    'The Jupiter cluster simulator runs live in your browser. No hardware needed.')
sub('href="/vscode/settings.json"', 'href="@root/settings/"')

# ---- footer ----
sub('>8830acc<', f'>{COMMIT}<')
sub('↑ <!-- -->16<!-- --> <!-- -->PRs<!-- --> merged', '↑ 1 PR merged')
sub('Open to research &amp; internships', 'Open to work &amp; research')
sub('title="Open-source pull requests merged upstream"', 'title="Merged pull requests"')
# structured data -> his
m = re.search(r'<script type="application/ld\+json">.*?</script>', html, re.S)
if m:
    ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Person",'
          '"name":"Rishabh Bohra","url":"https://sudo-mystic.github.io/portfolio/",'
          '"sameAs":["https://github.com/sudo-Mystic","https://www.linkedin.com/in/rishabh-b-90303b245"]}</script>')
    html = html.replace(m.group(0), ld)
# og tags -> his
for prop, val in [('og:title', 'Rishabh Bohra · mystic.code'),
                  ('og:site_name', 'Rishabh Bohra · mystic.code'),
                  ('twitter:title', 'Rishabh Bohra · mystic.code')]:
    m = re.search(r'<meta (?:property|name)="' + prop + r'" content="[^"]*"', html)
    if m:
        html = html.replace(m.group(0), m.group(0).split('content="')[0] + f'content="{val}"')
m = re.search(r'<meta property="og:url" content="[^"]*"', html)
if m:
    html = html.replace(m.group(0), '<meta property="og:url" content="https://sudo-mystic.github.io/portfolio/"')
for prop in ['og:image', 'twitter:image']:
    m = re.search(r'<meta (?:property|name)="' + prop + r'" content="[^"]*"', html)
    if m:
        html = html.replace(m.group(0), m.group(0).split('content="')[0] + 'content="https://sudo-mystic.github.io/portfolio/logo-256.webp"')
m = re.search(r'<meta property="og:image:alt" content="[^"]*"', html)
if m:
    html = html.replace(m.group(0), '<meta property="og:image:alt" content="Rishabh Bohra"/>')
# explorer workspace root label
sub('>MAAZ</button>', '>MYSTIC</button>')
# verify no leftover flight data / personal strings
for bad in ['maaz7409', 'Mohd Maaz', 'kmaaz7256', '__next_f', 'maaza-codes']:
    assert bad not in html, f'LEFTOVER: {bad}'

# ---- sidebar explorer tree ----
TREE = [
    ('file', 'codicon-markdown text-syntax-keyword', 'README.md', '@root/readme/', None),
    ('folder', None, 'projects', None, None),
    ('file', 'codicon-file-code text-syntax-function', 'scoot.dart', '@root/projects/scoot/', 'shipped'),
    ('file', 'codicon-file-code text-syntax-function', 'detroit_jev.py', '@root/projects/detroit-jev/', 'wip'),
    ('file', 'codicon-file-code text-syntax-function', 'esp_reddit.cpp', '@root/projects/esp-reddit/', None),
    ('file', 'codicon-markdown text-syntax-keyword', 'exam_eval.md', '@root/projects/exam-eval/', None),
    ('folder', None, '.vscode', None, None),
    ('file', 'codicon-json text-syntax-function', 'settings.json', '@root/settings/', None),
]

def tree_html():
    out = []
    for kind, icon, name, href, badge in TREE:
        if kind == 'folder':
            out.append(
                '<li class="flex h-6 w-full cursor-pointer items-center gap-1.5 pr-2 outline-offset-[-1px] '
                'select-none hover:bg-list-hover max-md:h-11 ">'
                '<span class="codicon codicon-chevron-down " aria-hidden="true"></span>'
                f'<span class="truncate ">{name}</span></li>')
        else:
            badge_html = f'<span class="ml-auto text-[11px] text-muted">{badge}</span>' if badge else ''
            out.append(
                '<li class="flex h-6 w-full cursor-pointer items-center gap-1.5 pr-2 outline-offset-[-1px] '
                'select-none hover:bg-list-hover max-md:h-11 ">'
                f'<a href="{href}" class="flex h-full min-w-0 flex-1 items-center gap-1.5">'
                f'<span class="codicon {icon} " aria-hidden="true"></span>'
                f'<span class="truncate ">{name}</span>{badge_html}</a></li>')
    return ''.join(out)

m = re.search(r'(<h2[^>]*>\s*EXPLORER\s*</h2>.*?<ul[^>]*>)(.*?)(</ul>)', html, re.S | re.I)
assert m, 'explorer ul not found'
html = html[:m.start(2)] + tree_html() + html[m.end(2):]

# ---- mobile drawer ("Open Editors") -> file tree links ----
m = re.search(r'(<section class="absolute inset-x-0 bottom-0 z-30.*?<ul[^>]*>)(.*?)(</ul>)', html, re.S)
if m:
    items = []
    for kind, icon, name, href, badge in TREE:
        if kind == 'folder' or not href:
            continue
        items.append(
            '<li class="flex items-center">'
            f'<a href="{href}" class="flex h-11 min-w-0 flex-1 items-center gap-2 px-4 text-left text-[13px]">'
            f'<span class="codicon {icon} " aria-hidden="true"></span>'
            f'<span class="truncate ">{name}</span></a></li>')
    html = html[:m.start(2)] + ''.join(items) + html[m.end(2):]
    html = html.replace('>Open Editors<', '>Explorer<', 1)

INDEX_HTML = html  # home page template (with @root/ placeholders)

# ---------- page content blocks ----------
def article(title, status, desc, chips, repo_url, body_html):
    chips_html = ''.join(
        f'<li class="rounded-full border border-border bg-sidebar px-2.5 py-0.5 font-mono text-xs text-syntax-variable">{c}</li>'
        for c in chips)
    repo_html = (f'<ul aria-label="Links" class="flex flex-wrap gap-2"><li><a href="{repo_url}" target="_blank" '
                 'rel="noreferrer" class="flex h-8 items-center gap-1.5 rounded-[5px] px-3 text-[13px] max-md:h-11 '
                 'bg-button text-button-fg hover:bg-button-hover"><span class="codicon codicon-github " '
                 'aria-hidden="true"></span>Repository</a></li></ul>') if repo_url else ''
    status_html = (f'<p class="flex items-center gap-2 text-xs text-muted"><span aria-hidden="true" '
                   f'class="text-syntax-function">●</span>{status}</p>') if status else ''
    return (f'<div><article class="mx-auto max-w-3xl px-8 py-8 max-md:px-5"><header class="space-y-4">'
            f'<div class="space-y-2">{status_html}'
            f'<h1 class="text-[1.75rem] leading-tight font-semibold text-tab-active-fg">{title}</h1>'
            f'<p class="text-[15px] text-muted">{desc}</p></div>'
            f'{repo_html}<ul aria-label="Tech stack" class="flex flex-wrap gap-1.5">{chips_html}</ul>'
            f'</header><hr class="my-6 border-border"/><div class="markdown-body ">{body_html}</div>'
            f'</article></div>')

PAGES = {}

PAGES['readme/'] = ('README.md', 'README.md', article(
    'README.md', None, 'The short version.',
    [], None,
    '''<h2>Hi, I am Rishabh.</h2>
<p>B.Tech undergrad at IET DAVV. I work across embedded systems, mobile apps, and security research.</p>
<h2>What I am building</h2>
<ul>
<li><strong>Scoot</strong> — Flutter companion app for TVS smart scooters. Live telemetry, trip history, turn-by-turn navigation on the cluster, all over BLE. Protocol reverse-engineered from the official app.</li>
<li><strong>detroit-jev</strong> — an engine that plays Detroit: Become Human start to finish, with an AI making all 226 story decisions live.</li>
<li><strong>esp-reddit</strong> — Reddit API wrapper for ESP32. OAuth2, rate limiting, 39 unit tests.</li>
<li><strong>exam-eval-platform</strong> — AI examination evaluation with a Gemini-powered grading pipeline.</li>
<li><strong>Security research</strong> — static and dynamic teardown of Indian consumer Android apps, disclosed through proper channels.</li>
</ul>
<h2>Elsewhere</h2>
<ul>
<li>home-assistant/core contributor (heater-cooler fix, HomeKit controller).</li>
<li>Preparing for FDE / Applied AI roles: LLM foundations, RAG + evals, agents.</li>
</ul>
<blockquote><p>If it runs code, it can be understood. If it can be understood, it can be improved. Or broken.</p></blockquote>'''))

PAGES['projects/scoot/'] = ('scoot.dart', 'scoot.dart', article(
    'Scoot', 'Shipped', 'Flutter companion app for TVS smart scooters. Live telemetry, trips, and cluster navigation over BLE.',
    ['Flutter', 'Dart', 'BLE', 'Reverse engineering'], f'{GITHUB}/Scoot',
    '''<h2>What it does</h2>
<p>Turns a phone into a full dashboard for the scooter: live telemetry, trip history, turn-by-turn navigation mirrored to the instrument cluster, media and call controls, all over Bluetooth Low Energy.</p>
<ul>
<li><strong>Reverse-engineered protocol</strong> — the entire cluster frame format decoded from the official app and JRC docs.</li>
<li><strong>Audited every release</strong> — APK hash and signer cert verified against the manifest before anything ships.</li>
<li><strong>Real users</strong> — on the road, not a demo.</li>
</ul>'''))

PAGES['projects/detroit-jev/'] = ('detroit_jev.py', 'detroit_jev.py', article(
    'detroit-jev', 'In progress', 'An engine that plays Detroit: Become Human start to finish, with an AI making all 226 story decisions live.',
    ['Python', 'LLM agents', 'Game automation'], f'{GITHUB}/detroit-jev',
    '''<h2>What it does</h2>
<p>Hooks a real game backend and lets an AI play the entire game — every dialogue choice, every quick-time event, every branching consequence, no human hands.</p>
<ul>
<li><strong>226 story decisions</strong> made live by the model.</li>
<li>Full playthroughs with consistent character reasoning.</li>
</ul>'''))

PAGES['projects/esp-reddit/'] = ('esp_reddit.cpp', 'esp_reddit.cpp', article(
    'esp-reddit', 'Shipped', 'Reddit API wrapper for the ESP32, built from scratch.',
    ['C++', 'ESP32', 'ArduinoJson', 'TLS'], f'{GITHUB}/esp-reddit',
    '''<h2>What it does</h2>
<p>Brings Reddit to microcontrollers: OAuth2 with auto re-auth, listings with pagination, comments, voting, posting, client-side rate limiting, and a curated TLS root set.</p>
<ul>
<li><strong>39 unit tests</strong> passing on the host-testable core.</li>
<li>Every example compiles for real ESP32 hardware.</li>
<li>Usable today via <code>lib_deps</code> in PlatformIO.</li>
</ul>'''))

PAGES['projects/exam-eval/'] = ('exam_eval.md', 'exam_eval.md', article(
    'exam-eval-platform', 'Shipped', 'AI examination evaluation platform with a Gemini-powered grading pipeline.',
    ['Next.js', 'TypeScript', 'Postgres', 'Gemini'], f'{GITHUB}/exam-eval-platform',
    '''<h2>What it does</h2>
<p>Paper ingestion, rubric workflows, and an AI grading pipeline with deterministic checks, wrapped in a Next.js app with Postgres job queues.</p>
<ul>
<li>Multi-stage evaluation pipeline with parked jobs when no key is configured.</li>
<li>24 unit + 8 DB-gated tests passing.</li>
</ul>'''))

PAGES['settings/'] = ('settings.json', 'settings.json', '''<div><article class="mx-auto max-w-3xl px-8 py-8 max-md:px-5">
<h1 class="text-[1.75rem] leading-tight font-semibold text-tab-active-fg">Settings</h1>
<p class="mt-2 text-[15px] text-muted">4 dark themes. Pick one — it sticks around for your next visit.</p>
<div id="theme-cards" class="mt-6 grid gap-3 sm:grid-cols-2"></div>
<script>
window.__THEMES = [
  {id:'dark-modern', name:'Dark Modern', base:'#181818', desc:'The default. Balanced contrast.'},
  {id:'dark-plus', name:'Dark Plus', base:'#3c3c3c', desc:'Softer, lighter chrome.'},
  {id:'oled', name:'OLED', base:'#0a0a0a', desc:'True black. Easy on battery.'},
  {id:'dreamscape', name:'Dreamscape', base:'#00225c', desc:'Deep blue midnight.'}
];
</script>
</article></div>''')

PAGES['simple/'] = ('Simple view', 'Simple view', f'''<div><article class="mx-auto max-w-3xl px-8 py-8 max-md:px-5">
<h1 class="text-[1.75rem] leading-tight font-semibold text-tab-active-fg">Rishabh Bohra</h1>
<p class="mt-1 text-[15px] text-muted">B.Tech undergrad at IET DAVV · Embedded / Mobile / Security</p>
<p class="mt-4 text-[15px] leading-relaxed">I build things and break things to understand them. Microcontrollers, Flutter apps shipped to real users, and Android apps taken apart for security research.</p>
<h2 class="mt-8 mb-2 text-[15px] text-tab-active-fg">Contact</h2>
<ul class="space-y-1 text-[13px]">
<li><a class="text-link hover:underline" href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><a class="text-link hover:underline" href="{GITHUB}" target="_blank" rel="noreferrer">github.com/sudo-Mystic</a></li>
<li><a class="text-link hover:underline" href="{LINKEDIN}" target="_blank" rel="noreferrer">LinkedIn</a></li>
</ul>
<h2 class="mt-8 mb-2 text-[15px] text-tab-active-fg">Projects</h2>
<ul class="space-y-3 text-[13px]">
<li><strong class="text-tab-active-fg">Scoot</strong> <span class="text-muted">— Flutter companion app for TVS smart scooters. Live telemetry, trips, cluster navigation over BLE. Protocol reverse-engineered.</span> <a class="text-link hover:underline" href="{GITHUB}/Scoot" target="_blank" rel="noreferrer">repo</a></li>
<li><strong class="text-tab-active-fg">detroit-jev</strong> <span class="text-muted">— AI plays Detroit: Become Human, all 226 decisions live.</span> <a class="text-link hover:underline" href="{GITHUB}/detroit-jev" target="_blank" rel="noreferrer">repo</a></li>
<li><strong class="text-tab-active-fg">esp-reddit</strong> <span class="text-muted">— Reddit API wrapper for ESP32. OAuth2, rate limiting, 39 tests.</span> <a class="text-link hover:underline" href="{GITHUB}/esp-reddit" target="_blank" rel="noreferrer">repo</a></li>
<li><strong class="text-tab-active-fg">exam-eval-platform</strong> <span class="text-muted">— AI examination evaluation with a Gemini grading pipeline.</span> <a class="text-link hover:underline" href="{GITHUB}/exam-eval-platform" target="_blank" rel="noreferrer">repo</a></li>
<li><strong class="text-tab-active-fg">Android security research</strong> <span class="text-muted">— teardown of Indian consumer apps, disclosed properly.</span></li>
</ul>
<h2 class="mt-8 mb-2 text-[15px] text-tab-active-fg">Elsewhere</h2>
<ul class="space-y-1 text-[13px] text-muted">
<li>home-assistant/core contributor.</li>
<li>Try the <a class="text-link hover:underline" href="{SIM_URL}" target="_blank" rel="noreferrer">Jupiter cluster simulator</a> in your browser.</li>
</ul>
<p class="mt-8 border-l-2 border-[var(--color-accent,#4ec9b0)] pl-3 text-[13px] text-muted italic">If it runs code, it can be understood. If it can be understood, it can be improved. Or broken.</p>
</article></div>''')

# ---------- page generator ----------
def find_main_content(h):
    start = h.find('<div class="mx-auto max-w-5xl px-8 py-12 max-md:px-5 max-md:py-8">')
    assert start > 0, 'main content div not found'
    i = start
    depth = 0
    while True:
        nxt_open = h.find('<div', i)
        nxt_close = h.find('</div>', i)
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            i = nxt_open + 4
        else:
            depth -= 1
            i = nxt_close + 6
            if depth == 0:
                return start, i

C_START, C_END = find_main_content(INDEX_HTML)

TERMINAL_HTML = '''<div id="mterm" class="fixed inset-x-0 bottom-0 z-50 hidden border-t border-border bg-panel shadow-widget" style="height:min(46vh,380px)">
<div class="flex h-[35px] items-center justify-between border-b border-border px-3">
<span class="text-[11px] uppercase tracking-wide text-muted">Terminal — mystic.code</span>
<button id="mterm-close" class="flex size-[22px] items-center justify-center rounded-[5px] hover:bg-toolbar-hover" aria-label="Close terminal"><span class="codicon codicon-close"></span></button>
</div>
<div id="mterm-out" class="h-[calc(100%-75px)] overflow-y-auto px-3 py-2 font-mono text-[13px]"></div>
<div class="flex h-10 items-center gap-2 border-t border-border px-3">
<span class="font-mono text-[13px] text-ansi-green">rishabh@mystic:~$</span>
<input id="mterm-in" class="min-w-0 flex-1 bg-transparent font-mono text-[13px] text-editor-fg outline-none" autocomplete="off" spellcheck="false" aria-label="Terminal input"/>
</div></div>'''

def build_page(path, tab_label, title, content):
    h = INDEX_HTML
    h = h[:C_START] + content + h[C_END:]
    # tab label
    h = re.sub(r'(bg-tab-active-top.*?<span class="whitespace-nowrap ">)(.*?)(</span>)',
               r'\g<1>' + tab_label + r'\g<3>', h, count=1, flags=re.S)
    h = h.replace('<title>Rishabh Bohra · mystic.code</title>', f'<title>{title} · Rishabh Bohra</title>')
    # terminal overlay
    h = h.replace('</body>', TERMINAL_HTML + '\n</body>')
    # resolve @root/ per depth (index.html sits one level below the page dir)
    segs = [s for s in path.strip('/').split('/') if s]
    prefix = './' if not segs else '../' * len(segs)
    h = h.replace('@root/', prefix)
    # terminal walkthrough button -> open terminal
    h = h.replace('<button type="button" class="walkthrough', '<button type="button" data-open-terminal class="walkthrough', 1)
    out_dir = f'{DIST}/{path}'
    os.makedirs(out_dir, exist_ok=True)
    open(f'{out_dir}index.html', 'w').write(h)
    print('wrote', path or '/', '->', tab_label)

# home
h = INDEX_HTML
h = h.replace('</body>', TERMINAL_HTML + '\n</body>')
h = h.replace('<button type="button" class="walkthrough', '<button type="button" data-open-terminal class="walkthrough', 1)
h = h.replace('@root/', './')
open(f'{DIST}/index.html', 'w').write(h)
print('wrote / (home)')

for path, (tab_label, title, content) in PAGES.items():
    build_page(path, tab_label, title, content)

# ---------- site.js ----------
SITE_JS = r'''
(function(){
  var root = document.documentElement;
  try {
    var t = localStorage.getItem('mystic-theme');
    if (t) root.setAttribute('data-theme', t);
  } catch(e){}
  window.mysticSetTheme = function(id){
    root.setAttribute('data-theme', id);
    try { localStorage.setItem('mystic-theme', id); } catch(e){}
    renderThemeCards();
  };
  window.mysticTheme = function(){ return root.getAttribute('data-theme'); };

  function renderThemeCards(){
    var wrap = document.getElementById('theme-cards');
    if (!wrap || !window.__THEMES) return;
    var cur = window.mysticTheme();
    wrap.innerHTML = '';
    window.__THEMES.forEach(function(th){
      var card = document.createElement('button');
      card.type = 'button';
      card.className = 'rounded-[8px] border p-4 text-left transition-colors ' +
        (th.id === cur ? 'border-[var(--vscode-focusBorder,#4ec9b0)]' : 'border-border hover:border-muted');
      card.style.borderColor = th.id === cur ? '#4ec9b0' : '';
      card.innerHTML =
        '<div class="flex gap-1.5 mb-3">' +
        '<span class="h-8 flex-1 rounded" style="background:' + th.base + ';border:1px solid rgba(255,255,255,.12)"></span>' +
        '<span class="h-8 w-8 rounded" style="background:#4ec9b0"></span>' +
        '<span class="h-8 w-8 rounded" style="background:#4fc1ff"></span>' +
        '<span class="h-8 w-8 rounded" style="background:#c586c0"></span></div>' +
        '<div class="text-[13px] text-tab-active-fg font-medium">' + th.name + '</div>' +
        '<div class="text-[12px] text-muted mt-0.5">' + th.desc + '</div>' +
        (th.id === cur ? '<div class="text-[12px] mt-2" style="color:#4ec9b0">● active</div>' : '');
      card.addEventListener('click', function(){ window.mysticSetTheme(th.id); });
      wrap.appendChild(card);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', renderThemeCards);
  else renderThemeCards();

  // mobile drawer (Open Editors sheet)
  var drawer = document.querySelector('section.absolute.inset-x-0.bottom-0.z-30');
  var backdrop = document.querySelector('div.absolute.inset-0.z-20.bg-backdrop');
  function setDrawer(open){
    if (!drawer) return;
    drawer.classList.toggle('invisible', !open);
    drawer.classList.toggle('translate-y-full', !open);
    if (backdrop) {
      backdrop.classList.toggle('invisible', !open);
      backdrop.classList.toggle('opacity-0', !open);
    }
  }
  if (backdrop) backdrop.addEventListener('click', function(){ setDrawer(false); });
  var drawerClose = drawer ? drawer.querySelector('button[aria-label^="Close"]') : null;
  if (drawerClose) drawerClose.addEventListener('click', function(){ setDrawer(false); });
  // bottom nav (mobile): first button = files, last = terminal
  var bottomNav = document.querySelector('nav.relative.z-40');
  if (bottomNav) {
    var btns = bottomNav.querySelectorAll('button');
    if (btns[0]) btns[0].addEventListener('click', function(){
      var isOpen = drawer && !drawer.classList.contains('invisible');
      setDrawer(!isOpen);
    });
    if (btns[btns.length-1]) btns[btns.length-1].addEventListener('click', openTerm);
  }
  // activity bar (desktop): last icon opens terminal too
  var actBar = document.querySelector('nav.flex.w-12');
  if (actBar) {
    var ab = actBar.querySelectorAll('button');
    if (ab[ab.length-1]) ab[ab.length-1].addEventListener('click', openTerm);
  }

  // ---------- terminal ----------
  var term = document.getElementById('mterm'),
      out = document.getElementById('mterm-out'),
      inp = document.getElementById('mterm-in');
  function print(html){ if(out){ out.insertAdjacentHTML('beforeend', html); out.scrollTop = out.scrollHeight; } }
  function esc(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;'); }
  var FILES = {
    'README.md': 'Rishabh Bohra — B.Tech undergrad at IET DAVV.\nEmbedded / Mobile / Security.\n\n"If it runs code, it can be understood."',
    'scoot.dart': 'Flutter companion app for TVS smart scooters.\nBLE telemetry, trips, cluster nav. Shipped to real users.',
    'detroit_jev.py': 'AI plays Detroit: Become Human. All 226 decisions, live.',
    'esp_reddit.cpp': 'Reddit API wrapper for ESP32. OAuth2, rate limiting, 39 tests.',
    'exam_eval.md': 'AI examination evaluation platform. Next.js + Gemini pipeline.',
    'settings.json': '{ "theme": "' + (window.mysticTheme && window.mysticTheme() || 'dark-modern') + '" }'
  };
  function openTerm(){
    if (!term) return;
    term.classList.remove('hidden');
    if (!term.dataset.booted){
      term.dataset.booted = '1';
      print('<div class="text-muted">mystic.code shell — type <span class="text-editor-fg">help</span></div>');
    }
    setTimeout(function(){ inp && inp.focus(); }, 50);
  }
  window.mysticOpenTerm = openTerm;
  document.querySelectorAll('[data-open-terminal]').forEach(function(b){
    b.addEventListener('click', openTerm);
  });
  var closeBtn = document.getElementById('mterm-close');
  if (closeBtn) closeBtn.addEventListener('click', function(){ term.classList.add('hidden'); });
  if (inp) inp.addEventListener('keydown', function(e){
    if (e.key !== 'Enter') return;
    var raw = inp.value; inp.value = '';
    print('<div><span class="text-ansi-green">rishabh@mystic:~$</span> <span>' + esc(raw) + '</span></div>');
    var parts = raw.trim().split(/\s+/), cmd = parts[0] || '', arg = parts.slice(1).join(' ');
    switch(cmd){
      case '': break;
      case 'help':
        print('<div class="text-muted">help · ls · cat &lt;file&gt; · whoami · neofetch · themes · open &lt;file&gt; · clear · exit</div>'); break;
      case 'ls':
        print('<div class="text-editor-fg">README.md&nbsp;&nbsp;projects/&nbsp;&nbsp;.vscode/</div><div class="text-muted">projects/: scoot.dart detroit_jev.py esp_reddit.cpp exam_eval.md</div>'); break;
      case 'cat':
        if (FILES[arg]) print('<div class="whitespace-pre-wrap text-editor-fg">' + esc(FILES[arg]) + '</div>');
        else print('<div class="text-muted">cat: ' + esc(arg || '') + ': no such file. Try ls.</div>');
        break;
      case 'whoami': print('<div class="text-editor-fg">rishabh — builder, breaker, shipper</div>'); break;
      case 'neofetch':
        print('<div class="text-editor-fg">mystic.code</div><div class="text-muted">user: rishabh bohra<br>stack: embedded / flutter / security<br>editor: this website<br>uptime: always building</div>'); break;
      case 'themes': print('<div class="text-muted">dark-modern · dark-plus · oled · dreamscape — change them on the <span class="text-editor-fg">settings</span> page</div>'); break;
      case 'open':
        if (FILES[arg]) print('<div class="text-muted">opening ' + esc(arg) + '… (it is already open in the editor above)</div>');
        else print('<div class="text-muted">open: unknown file. Try ls.</div>');
        break;
      case 'clear': out.innerHTML = ''; break;
      case 'exit': term.classList.add('hidden'); break;
      default: print('<div class="text-muted">command not found: ' + esc(cmd) + ' — try help</div>');
    }
  });
})();
'''
open(f'{DIST}/assets/site.js', 'w').write(SITE_JS)
print('wrote assets/site.js')

# .nojekyll so GitHub Pages serves files as-is
open(f'{DIST}/.nojekyll', 'w').write('')
print('done')
