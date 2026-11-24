#!/usr/bin/env python3
"""Render the portfolio pages for GitHub Pages."""

import argparse
import hashlib
import json
from functools import lru_cache
from html import escape
from pathlib import Path

from source.projects import EMAIL, GITHUB, HOME_ASSISTANT_PR, LINKEDIN, PROJECTS

ROOT = Path(__file__).resolve().parent
SITE = "https://sudo-mystic.github.io/portfolio/"
REPO = f"{GITHUB}/portfolio"
NAME = "Rishabh Bohra"
DESCRIPTION = "Rishabh Bohra builds mobile apps, embedded systems and applied AI tools."
BIO = "B.Tech student at IET DAVV"
FOCUS = "Mobile apps, embedded systems and applied AI."
THEMES = (
    ("dark-modern", "Dark Modern"),
    ("dark-plus", "Slate"),
    ("oled", "Black"),
    ("dreamscape", "Midnight"),
)
ICONS = {
    "source": "ea68", "search": "ea6d", "close": "ea76", "file": "ea7b", "folder": "ea83",
    "github": "ea84", "terminal": "ea85", "chevron": "eab6", "code": "eae9",
    "files": "eaf0", "home": "eb06", "json": "eb0f", "external": "eb14",
    "mail": "eb1c", "markdown": "eb1d", "settings": "eb51", "branch": "ec6f",
}

WELCOME = {"id": "welcome", "path": "", "file": "Welcome", "icon": "home",
           "intro": FOCUS, "name": "Welcome", "language": "Portfolio"}
ABOUT = {"id": "readme", "path": "readme/", "file": "README.md", "icon": "markdown",
         "intro": f"{NAME} · {BIO}. {FOCUS}", "name": "About", "language": "Markdown"}
SETTINGS = {"id": "settings", "path": "settings/", "file": "settings.json", "icon": "json",
            "intro": "Choose a color theme for the editor.", "name": "Settings", "language": "JSON"}
PROJECT_FILES = tuple({
    **project, "id": project["slug"], "path": f"projects/{project['slug']}/",
    "icon": "markdown" if project["language"] == "Markdown" else "code",
} for project in PROJECTS)


def icon(name, extra=""):
    return f'<span class="icon{extra}" aria-hidden="true">&#x{ICONS[name]};</span>'


@lru_cache(maxsize=None)
def asset(name):
    path = f"assets/{name}"
    digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:12]
    return f"{path}?v={digest}"


def current_attr(item, current):
    return ' aria-current="page"' if item["id"] == current.get("id") else ""


def file_link(item, root, current):
    return (f'<a class="file-link" href="{root}{item["path"]}"{current_attr(item, current)} '
            f'data-file-id="{item["id"]}" data-file-name="{item["file"]}" '
            f'data-file-intro="{escape(item["intro"], quote=True)}">'
            f'{icon(item["icon"], " file-" + item["icon"])}<span>{item["file"]}</span></a>')


def explorer(root, current):
    projects = "\n".join(f'<li>{file_link(item, root, current)}</li>' for item in PROJECT_FILES)
    return f"""
<aside class="explorer" id="explorer" aria-labelledby="explorer-title">
  <div class="explorer-heading"><h2 id="explorer-title">Explorer</h2></div>
  <details class="folder workspace-folder" open>
    <summary>{icon("chevron", " disclosure")}<strong>MYSTIC.CODE</strong></summary>
    <nav aria-label="Files">
      <ul class="file-tree">
        <li>{file_link(WELCOME, root, current)}</li>
        <li>{file_link(ABOUT, root, current)}</li>
        <li>
          <details class="folder" open>
            <summary>{icon("chevron", " disclosure")}{icon("folder", " folder-icon")}projects</summary>
            <ul>{projects}</ul>
          </details>
        </li>
        <li>
          <details class="folder"{" open" if current["id"] == "settings" else ""}>
            <summary>{icon("chevron", " disclosure")}{icon("folder", " folder-icon")}.vscode</summary>
            <ul><li>{file_link(SETTINGS, root, current)}</li></ul>
          </details>
        </li>
      </ul>
    </nav>
  </details>
</aside>"""


def titlebar(root):
    return f"""
<header class="titlebar">
  <a class="brand" href="{root}" aria-label="mystic.code, home">
    <img src="{root}logo-64.webp" width="24" height="24" alt="">
    <span>mystic<span class="brand-period">.</span>code</span>
  </a>
  <button class="quick-open" type="button" data-jump aria-label="Search files" aria-haspopup="dialog" aria-controls="jump-dialog" hidden>
    {icon("search")}<span>Search files</span><kbd aria-hidden="true">Ctrl K</kbd>
  </button>
  <a class="title-github" aria-label="GitHub" href="{GITHUB}">{icon("github")}<span>GitHub</span></a>
</header>"""


def activitybar(root, current):
    return f"""
<nav class="activitybar" aria-label="Editor tools">
  <button class="activity-item" type="button" data-explorer aria-label="Toggle Explorer" aria-expanded="true" aria-controls="explorer" title="Explorer" hidden>{icon("files")}</button>
  <button class="activity-item" type="button" data-jump aria-label="Search files" aria-haspopup="dialog" aria-controls="jump-dialog" title="Search files" hidden>{icon("search")}</button>
  <a class="activity-item" href="{REPO}" aria-label="Portfolio source" title="Portfolio source">{icon("source")}</a>
  <a class="activity-item activity-settings" href="{root}settings/" aria-label="Settings"{current_attr(SETTINGS, current)} title="Settings">{icon("settings")}</a>
</nav>"""


def editor_tab(item, root, current):
    return (f'<div class="editor-tab"><a href="{root}{item["path"]}"{current_attr(item, current)}>'
            f'{icon(item["icon"], " file-" + item["icon"])}{item["file"]}</a></div>')


def editor_header(root, current):
    initial_tabs = (WELCOME, current) if current["id"] != "welcome" else (WELCOME, ABOUT)
    tabs = "".join(editor_tab(item, root, current) for item in initial_tabs)
    project = f'<a href="{root}#work">projects</a>{icon("chevron")}' if current["path"].startswith("projects/") else ""
    settings = f'<span>.vscode</span>{icon("chevron")}' if current["id"] == "settings" else ""
    return f"""
<div class="editor-tabs">
  <button class="mobile-explorer" type="button" data-explorer aria-label="Toggle Explorer" aria-expanded="false" aria-controls="explorer" hidden>{icon("files")}</button>
  <nav class="open-tabs" aria-label="Open editors" id="open-tabs">{tabs}</nav>
</div>
<nav class="breadcrumbs" aria-label="Breadcrumb">
  <a href="{root}">mystic.code</a>{icon("chevron")}{project}{settings}
  <span aria-current="page">{icon(current["icon"], " file-" + current["icon"])}{current["file"]}</span>
</nav>"""


def terminal():
    return f"""
<section class="terminal" id="terminal" aria-labelledby="terminal-title" hidden>
  <header>
    <h2 id="terminal-title">Terminal</h2>
    <button class="icon-button" type="button" data-terminal-close aria-label="Close terminal">{icon("close")}</button>
  </header>
  <div class="terminal-log" role="log" aria-label="Terminal output"><p>Type <code>help</code> for commands.</p></div>
  <form>
    <span aria-hidden="true">mystic:~$</span>
    <input type="text" aria-label="Terminal command" autocomplete="off" spellcheck="false" maxlength="150">
  </form>
</section>"""


def statusbar(current):
    return f"""
<footer class="statusbar" aria-label="Status bar">
  <a href="{REPO}/tree/main" title="View the main branch">{icon("branch")}<span>main</span></a>
  <button type="button" data-terminal aria-expanded="false" aria-controls="terminal" hidden>{icon("terminal")}<span>Terminal</span></button>
  <span class="status-language"><span>UTF-8</span><span>{current["language"]}</span></span>
</footer>"""


def quick_open(root):
    rows = []
    for item in (WELCOME, ABOUT, *PROJECT_FILES, SETTINGS):
        keywords = " ".join((item["name"], item["language"], *item.get("tags", ()), item["intro"]))
        rows.append(f'<li data-search="{escape(keywords, quote=True)}">{file_link(item, root, {})}</li>')
    return f"""
<dialog id="jump-dialog" aria-labelledby="jump-title">
  <div class="jump-header">
    <label id="jump-title" for="jump-input">Search files</label>
    <form method="dialog"><button class="icon-button" type="submit" aria-label="Close search">{icon("close")}</button></form>
  </div>
  <input type="search" id="jump-input" placeholder="Type a filename or project" autocomplete="off" autofocus>
  <ul class="jump-results">{"".join(rows)}</ul>
  <p class="jump-empty" hidden>No matching files.</p>
  <p class="sr-only" role="status" id="jump-status"></p>
</dialog>"""


def contact():
    return f"""<ul class="link-row">
      <li><a href="mailto:{EMAIL}">{icon("mail")}Email</a></li>
      <li><a href="{GITHUB}">{icon("github")}GitHub</a></li>
      <li><a href="{LINKEDIN}">{icon("external")}LinkedIn</a></li>
    </ul>"""


def open_source():
    return f'<p><a href="{HOME_ASSISTANT_PR}">Home Assistant</a> · HomeKit heater-cooler temperature range fix.</p>'


def motion_graphic(scene):
    return f"""
<div class="motion-study" data-scene="{scene}" hidden>
  <canvas width="560" height="280" aria-hidden="true"></canvas>
  <button class="replay-study" type="button" aria-label="Replay motion graphic" title="Replay motion graphic" hidden>
    <span aria-hidden="true"></span>
  </button>
</div>"""


def homepage(root):
    projects = "\n".join(
        f'<li><a href="{root}{item["path"]}" data-preview="{item["id"]}">{icon(item["icon"], " file-" + item["icon"])}'
        f'<span><strong>{item["file"]}</strong><small>{item["intro"]}</small></span></a></li>'
        for item in PROJECT_FILES
    )
    return f"""
<div class="editor-document welcome-document">
  <div class="document-hero">
    <div>
      <header class="welcome-intro" id="about">
        <img src="{root}logo-256.webp" width="58" height="58" alt="">
        <div><h1>{NAME}</h1><p>{BIO}</p></div>
      </header>
      <p class="document-intro">{FOCUS}</p>
    </div>
    {motion_graphic("welcome")}
  </div>
  <div class="welcome-grid">
    <section aria-labelledby="start-title">
      <h2 id="start-title">Start</h2>
      <ul class="start-list">
        <li><a href="{root}readme/">{icon("markdown")}README.md</a></li>
        <li><button type="button" data-terminal aria-expanded="false" aria-controls="terminal" hidden>{icon("terminal")}<span data-terminal-label>Open terminal</span></button></li>
        <li><a href="{root}settings/">{icon("settings")}Color themes</a></li>
        <li><a href="{root}simple/">{icon("file")}Simple view</a></li>
      </ul>
    </section>
    <section id="work" aria-labelledby="work-title">
      <h2 id="work-title">Projects</h2>
      <ul class="project-list">{projects}</ul>
    </section>
  </div>
  <div class="welcome-bottom">
    <section><h2>Open source</h2>{open_source()}</section>
    <section id="contact"><h2>Contact</h2>{contact()}</section>
  </div>
</div>"""


def project_page(item):
    links = "".join(f'<a class="document-button" href="{url}">{icon("external")}{label}</a>'
                    for label, url in item["links"])
    tools = "".join(f"<li>{escape(tag)}</li>" for tag in item["tags"])
    details = "".join(f"<li><strong>{escape(label)}</strong> {escape(value)}</li>"
                      for label, value in item["details"])
    return f"""
<article class="editor-document project-document">
  <div class="document-hero">
  <header>
    <h1>{item["name"]}</h1>
    <p class="document-intro">{item["intro"]}</p>
    <ul class="stack" aria-label="Technologies">{tools}</ul>
    {links}
  </header>
  {motion_graphic(item["id"])}
  </div>
  <section class="document-section"><h2>Details</h2><ul class="details-list">{details}</ul></section>
</article>"""


def about_page():
    return f"""
<article class="editor-document">
  <h1>{NAME}</h1>
  <p class="document-intro">{BIO}. {FOCUS}</p>
  <section class="document-section"><h2>Open source</h2>{open_source()}</section>
  <section class="document-section" id="contact"><h2>Contact</h2>{contact()}</section>
</article>"""


def settings_page():
    switches = "\n".join(f"""
    <label class="theme-option theme-{identity}">
      <input type="radio" name="theme" value="{identity}"{' checked' if index == 0 else ''} disabled>
      <span class="swatch" aria-hidden="true"></span><span>{name}</span>
    </label>""" for index, (identity, name) in enumerate(THEMES))
    return f"""
<article class="editor-document">
  <h1>Settings</h1>
  <fieldset class="theme-options"><legend>Color theme</legend>{switches}</fieldset>
  <fieldset class="motion-options" hidden>
    <legend>Motion</legend>
    <label><input type="checkbox" id="reduce-motion"> Reduce animations</label>
  </fieldset>
  <noscript><p>Enable JavaScript to change the editor theme.</p></noscript>
</article>"""


def metadata(title, description, path, root, indexable):
    url = SITE + path
    image = SITE + "assets/share.jpg"
    title, description = escape(title, quote=True), escape(description, quote=True)
    robots = "" if indexable else '<meta name="robots" content="noindex">\n'
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="{NAME}">
{robots}<link rel="canonical" href="{url}">
<link rel="icon" href="{root}logo-64.webp" type="image/webp">
<link rel="apple-touch-icon" href="{root}apple-touch-icon.webp">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Rishabh Bohra’s mystic.code portfolio">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image}">"""


def page(item, root, content, indexable=True):
    title = f"{item['name']} · {NAME}"
    description = item["intro"]
    study_script = ""
    if item == WELCOME or item in PROJECT_FILES:
        study_script = f'<script src="{root}{asset("studies.js")}" defer></script>'
    schema = ""
    if item["id"] == "welcome":
        title, description = f"{NAME} · mystic.code", DESCRIPTION
        person = {"@context": "https://schema.org", "@type": "Person", "name": NAME,
                  "url": SITE, "sameAs": [GITHUB, LINKEDIN]}
        schema = f'<script type="application/ld+json">{json.dumps(person)}</script>\n'
    return f"""<!doctype html>
<html lang="en" data-theme="dark-modern">
<head>
{metadata(title, description, item["path"], root, indexable)}
<script src="{root}{asset("theme.js")}"></script>
<link rel="stylesheet" href="{root}{asset("site.css")}">
<link rel="stylesheet" href="{root}{asset("motion.css")}">
<script src="{root}{asset("site.js")}" defer></script>
{study_script}
{schema}</head>
<body data-current-file="{item["id"]}">
<a class="skip-link" href="#main">Skip to editor</a>
{titlebar(root)}
<div class="workspace">
  {activitybar(root, item)}
  {explorer(root, item)}
  <div class="explorer-resizer" role="separator" aria-label="Explorer width" aria-controls="explorer"
       aria-orientation="vertical" aria-valuemin="170" aria-valuemax="360" aria-valuenow="232" tabindex="0" hidden></div>
  <section class="editor" aria-label="Editor">
    {editor_header(root, item)}
    <main id="main" tabindex="-1">{content}</main>
    {terminal()}
  </section>
</div>
{statusbar(item)}
{quick_open(root)}
</body>
</html>
"""


def simple_page():
    projects = "".join(f'<li><a href="../{p["path"]}">{p["name"]}</a> · {p["intro"]}</li>'
                       for p in PROJECT_FILES)
    return f"""<!doctype html>
<html lang="en">
<head>
{metadata("Simple view · " + NAME, DESCRIPTION, "simple/", "../", False)}
<meta name="color-scheme" content="light dark">
<style>
  body {{ font: 1.0625rem/1.65 system-ui, sans-serif; max-width: 43rem; margin: 3rem auto; padding: 0 1.25rem; }}
  li + li {{ margin-block-start: .65rem; }}
  a {{ overflow-wrap: anywhere; }}
</style>
</head>
<body>
<header><a href="../">Editor view</a></header>
<main><h1>{NAME}</h1><p>{BIO}. {FOCUS}</p>
<h2>Projects</h2><ul>{projects}</ul>
<h2>Open source</h2>{open_source()}
<h2>Contact</h2><ul><li><a href="mailto:{EMAIL}">Email</a></li>
<li><a href="{GITHUB}">GitHub</a></li><li><a href="{LINKEDIN}">LinkedIn</a></li></ul>
</main>
</body>
</html>
"""


def site_files():
    missing = {"id": "missing", "path": "404.html", "file": "404",
               "icon": "file", "intro": "Page not found.", "name": "Page not found", "language": "Portfolio"}
    files = {
        "index.html": page(WELCOME, "./", homepage("./")),
        "readme/index.html": page(ABOUT, "../", about_page()),
        "settings/index.html": page(SETTINGS, "../", settings_page(), indexable=False),
        "simple/index.html": simple_page(),
        "404.html": page(missing, "/portfolio/", """
<div class="editor-document">
  <h1>Page not found</h1>
  <p class="document-intro"><a href="/portfolio/">Return to Welcome</a></p>
</div>""", indexable=False),
    }
    for item in PROJECT_FILES:
        files[f'{item["path"]}index.html'] = page(item, "../../", project_page(item))
    site_paths = ("", "readme/", *(item["path"] for item in PROJECT_FILES))
    urls = "\n".join(f"  <url><loc>{SITE}{path}</loc></url>" for path in site_paths)
    files["sitemap.xml"] = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check the published files for drift")
    args = parser.parse_args()
    stale = []
    for name, contents in site_files().items():
        path = ROOT / name
        contents = "\n".join(line.rstrip() for line in contents.split("\n"))
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != contents:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
    if stale:
        parser.exit(1, "Regenerate with python3 build.py: " + ", ".join(stale) + "\n")


if __name__ == "__main__":
    main()
