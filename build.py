#!/usr/bin/env python3
"""Render the HTML published by GitHub Pages, using only the standard library."""

import argparse
import json
from html import escape
from pathlib import Path

from source.projects import EMAIL, GITHUB, HOME_ASSISTANT_PR, LINKEDIN, PROJECTS, SCOOT_SITE

ROOT = Path(__file__).resolve().parent
SITE = "https://sudo-mystic.github.io/portfolio/"
NAME = "Rishabh Bohra"
DESCRIPTION = "Rishabh Bohra builds software for connected devices, the web and applied AI. Explore his projects and open-source work."
BIO = ("I’m a B.Tech student at IET DAVV. I work on mobile apps and embedded systems, "
       "and I’m exploring where AI fits into tools people actually use.")
THEMES = (
    ("dark-modern", "Graphite", "Warm charcoal with a red-orange accent."),
    ("dark-plus", "Slate", "Cooler surfaces with a mint accent."),
    ("oled", "Black", "Black surfaces with a gold accent."),
    ("dreamscape", "Midnight", "Deep blue surfaces with a lavender accent."),
)


def project_path(project):
    return f"projects/{project['slug']}/"


def button(url, label, primary=False):
    style = "button button-primary" if primary else "button"
    return f'<a class="{style}" href="{escape(url, quote=True)}">{escape(label)}</a>'


def project_links(project):
    return "".join(button(url, label, primary=(index == 0))
                   for index, (label, url) in enumerate(project["links"]))


def tags(project):
    return '<ul class="tags" aria-label="Technologies">' + "".join(
        f"<li>{escape(tag)}</li>" for tag in project["tags"]
    ) + "</ul>"


def picture(root, name, alt, width, height):
    return (f'<img src="{root}assets/{name}.webp" alt="{escape(alt, quote=True)}" '
            f'width="{width}" height="{height}" decoding="async" fetchpriority="high">')


def scoot_display():
    return """
<div class="cluster-art" aria-hidden="true">
  <div class="cluster">
    <div class="cluster-top"><span>SCOOT</span><span class="cluster-mode">RIDE MODE</span></div>
    <div class="cluster-data">
      <div class="cluster-speed"><span>42</span><small>km/h</small></div>
      <div class="cluster-turn"><span class="turn-icon"></span><div><strong>300 m</strong><small>Next turn</small></div></div>
    </div>
    <div class="cluster-meter"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
    <div class="cluster-bottom"><span>TRIP <b>12.4 km</b></span><span>ODO <b>2,068 km</b></span></div>
  </div>
</div>"""


def featured(project, root):
    return f"""
<article class="featured">
  <div class="featured-copy">
    <p class="eyebrow"><span class="indicator"></span>{project['status']}</p>
    <h3><a href="{root}{project_path(project)}">{project['name']}</a></h3>
    <p>{project['intro']}</p>
    {tags(project)}
    <div class="actions">
      {button(root + project_path(project), "Read the case study", True)}
      {button(SCOOT_SITE + "sim/", "Try the simulator")}
    </div>
  </div>
  <figure class="featured-figure">
{scoot_display()}
    <figcaption>Illustrative Scoot telemetry</figcaption>
  </figure>
</article>"""


def project_cards(projects, root):
    return "\n".join(f"""
    <li>
      <article class="project-card">
        <p class="eyebrow">{project['category']}</p>
        <h3><a href="{root}{project_path(project)}">{project['name']}</a></h3>
        <p>{project['intro']}</p>
        {tags(project)}
      </article>
    </li>""" for project in projects)


def homepage(root):
    scoot, *others = PROJECTS
    return f"""
<section class="hero wrap" aria-labelledby="hero-title">
  <div class="hero-copy">
    <p class="eyebrow hero-kicker"><span></span> Independent developer <span class="kicker-place">/ India</span></p>
    <h1 id="hero-title">Rishabh<br>Bohra<span class="name-period">.</span></h1>
    <p class="hero-intro">I build mobile apps, embedded systems and applied AI tools.</p>
    <div class="actions">
      {button("#work", "Explore work", True)}
      <a class="quiet-link" href="mailto:{EMAIL}">Get in touch</a>
    </div>
  </div>
  <figure class="signal">
    <div class="signal-image">{picture(root, "signal", "", 1000, 840)}</div>
    <figcaption><span>Signal study</span></figcaption>
  </figure>
</section>
<section class="work wrap" id="work" aria-labelledby="work-title">
  <header class="section-heading">
    <h2 id="work-title">Selected work<span class="name-period">.</span></h2>
    <a class="quiet-link" href="{GITHUB}">GitHub</a>
  </header>
{featured(scoot, root)}
  <ul class="project-list">{project_cards(others, root)}</ul>
</section>
<section class="contribution wrap" aria-labelledby="oss-title">
  <div>
    <p class="eyebrow">Open source</p>
    <h2 id="oss-title">Home Assistant</h2>
  </div>
  <div>
    <p>I proposed a fix for the temperature range Home Assistant shows for HomeKit heater-cooler devices in Auto mode.</p>
    <a class="quiet-link" href="{HOME_ASSISTANT_PR}">Read the pull request</a>
  </div>
</section>
<section class="about-band wrap" id="about" aria-labelledby="about-title">
  <div><p class="eyebrow">About me</p><h2 id="about-title">From boards<br>to browsers<span class="name-period">.</span></h2></div>
  <div><p>{BIO}</p>
  <p>I like working where the hard part is figuring out how two systems should talk to each other.</p>
  <a class="quiet-link" href="{root}readme/">More about me</a></div>
</section>"""


PROJECT_VISUALS = {
    "scoot": f'<figure class="case-visual">{scoot_display()}<figcaption>Illustrative Scoot telemetry</figcaption></figure>',
    "esp-reddit": """
<figure class="case-board">
  <figcaption>How the client keeps memory use down</figcaption>
  <ol class="pipeline">
    <li><strong>Request</strong><span>Cap the page size</span></li>
    <li><strong>Parse</strong><span>Stream the JSON response</span></li>
    <li><strong>Return</strong><span>Keep the requested fields</span></li>
  </ol>
</figure>""",
    "exam-eval": """
<figure class="case-board">
  <figcaption>From answer sheet to a reviewed grade</figcaption>
  <ol class="pipeline">
    <li><strong>Capture</strong><span>Collect the handwritten answer</span></li>
    <li><strong>Evaluate</strong><span>Draft marks against the rubric</span></li>
    <li><strong>Review</strong><span>Faculty verify evidence and marks</span></li>
  </ol>
</figure>""",
    "detroit-jev": """
<figure class="case-board">
  <figcaption>Explore a fictional decision trace</figcaption>
  <p class="trace-prompt">The radio goes quiet just before a supply drop.</p>
  <div class="trace-choices">
    <details>
      <summary>Investigate the signal</summary>
      <p>You find the damaged relay. The drop has to wait while you restore contact.</p>
    </details>
    <details>
      <summary>Keep watch at the drop zone</summary>
      <p>The supplies arrive on time. The next call comes from an unknown sender.</p>
    </details>
  </div>
</figure>""",
}


def project_page(project, root, next_project):
    sections = "".join(
        f'<section><h2>{escape(heading)}</h2><p>{escape(content)}</p></section>'
        for heading, content in project["sections"]
    )
    links = project_links(project)
    actions = f'<div class="actions">{links}</div>' if links else ""
    return f"""
<article class="wrap article">
  <a class="back-link" href="{root}#work">Back to selected work</a>
  <header class="article-header">
    <p class="eyebrow">{project['category']} <span class="separator">/</span> {project['status']}</p>
    <h1>{project['name']}<span class="name-period">.</span></h1>
    <p class="article-intro">{project['intro']}</p>
    {tags(project)}
{actions}
  </header>
{PROJECT_VISUALS[project["slug"]]}
  <div class="article-body">{sections}</div>
  <a class="next-project" href="{root}{project_path(next_project)}">
    <span class="eyebrow">Next project</span>
    <strong>{next_project['name']}</strong>
  </a>
</article>"""


def about_page(root):
    return f"""
<article class="wrap article">
  <header class="article-header">
    <p class="eyebrow">About me</p>
    <h1>{NAME}<span class="name-period">.</span></h1>
    <p class="article-intro">{BIO}</p>
  </header>
  <div class="article-body">
    <section><h2>Connected devices</h2>
      <p><a href="{root}projects/scoot/">Scoot</a> started with a question about what a phone and a scooter could share over Bluetooth. With <a href="{root}projects/esp-reddit/">esp-reddit</a>, the challenge was fitting an API client into the resources of an ESP32.</p>
    </section>
    <section><h2>Applied AI</h2>
      <p>In <a href="{root}projects/exam-eval/">Exam Evaluation</a>, I worked on bringing rubric-based grading and faculty review into one flow. <a href="{root}projects/detroit-jev/">detroit-jev</a> explores a different question: how a model’s decisions hold together over a long story.</p>
    </section>
    <section><h2>Open source</h2>
      <p>I’ve also worked on a <a href="{HOME_ASSISTANT_PR}">Home Assistant HomeKit integration fix</a>. You can find my public projects and contributions on <a href="{GITHUB}">GitHub</a>.</p>
    </section>
  </div>
</article>"""


def settings_page():
    switches = "".join(f"""
      <label class="theme-option theme-{identity}">
        <input type="radio" name="theme" value="{identity}"{' checked' if index == 0 else ''} disabled>
        <span class="swatch" aria-hidden="true"></span>
        <span><strong>{name}</strong><small>{description}</small></span>
      </label>""" for index, (identity, name, description) in enumerate(THEMES))
    return f"""
<article class="wrap article">
  <header class="article-header">
    <p class="eyebrow">Settings</p>
    <h1>Appearance<span class="name-period">.</span></h1>
    <p class="article-intro">Your theme choice is saved in this browser.</p>
  </header>
  <fieldset class="theme-options"><legend class="sr-only">Site theme</legend>{switches}</fieldset>
  <noscript><p>Enable JavaScript to change the theme.</p></noscript>
</article>"""


def command_menu(root):
    destinations = (
        ("Home", root, "index portfolio rishabh"),
        *((project["name"], root + project_path(project), f"project {project['category']} {' '.join(project['tags'])}")
          for project in PROJECTS),
        ("About Rishabh", root + "readme/", "bio"),
        ("Email Rishabh", f"mailto:{EMAIL}", "contact"),
        ("Appearance", root + "settings/", "preferences theme settings"),
        ("Simple view", root + "simple/", "text compact"),
    )
    rows = "\n".join(
        f'<li data-search="{escape(keywords, quote=True)}"><a href="{url}">{label}</a></li>'
        for label, url, keywords in destinations
    )
    return f"""
<dialog class="jump-dialog" id="jump-dialog" aria-labelledby="jump-title">
  <div class="jump-header">
    <label id="jump-title" for="jump-input">Jump to a page</label>
    <form method="dialog"><button class="jump-close" type="submit" aria-label="Close search">Esc</button></form>
  </div>
  <input type="search" id="jump-input" placeholder="Search projects and pages" autocomplete="off" autofocus>
  <ul class="jump-results">{rows}</ul>
  <p class="jump-empty" hidden>No matching pages.</p>
  <p class="sr-only" role="status" id="jump-status"></p>
</dialog>"""


def footer(root):
    return f"""
<footer class="site-footer" id="contact">
  <div class="wrap">
    <div class="footer-main">
      <div><h2>Get in touch<span class="name-period">.</span></h2>
      <a class="footer-email" href="mailto:{EMAIL}">{EMAIL}</a></div>
      <ul class="footer-profiles"><li><a href="{GITHUB}">GitHub</a></li><li><a href="{LINKEDIN}">LinkedIn</a></li></ul>
    </div>
    <div class="footer-bottom"><span>© {NAME}</span>
      <ul><li><a href="{root}simple/">Simple view</a></li><li><a href="{root}settings/">Appearance</a></li></ul>
    </div>
  </div>
</footer>"""


def metadata(title, description, path, root, indexable):
    url = SITE + path
    social_image = SITE + "assets/share.jpg"
    title = escape(title, quote=True)
    description = escape(description, quote=True)
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
<meta property="og:image" content="{social_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Rishabh Bohra, independent developer">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{social_image}">"""


def page(title, description, path, root, content, active="", indexable=True, not_found=False):
    body_class = " class=\"home\"" if active == "home" else ""
    about_current = ' aria-current="page"' if active == "about" else ""
    brand_current = ' aria-current="page"' if active == "home" else ""
    schema = ""
    if active == "home":
        person = {"@context": "https://schema.org", "@type": "Person", "name": NAME,
                  "url": SITE, "sameAs": [GITHUB, LINKEDIN]}
        schema = f'<script type="application/ld+json">{json.dumps(person)}</script>\n'
    return f"""<!doctype html>
<html lang="en" data-theme="dark-modern">
<head>
{metadata(title, description, path, root, indexable)}
<script src="{root}assets/theme.js"></script>
<link rel="stylesheet" href="{root}assets/site.css">
<script src="{root}assets/site.js" defer></script>
{schema}</head>
<body{body_class}>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{root}" aria-label="{NAME}, home"{brand_current}><span class="brand-mark" aria-hidden="true">rb<span>.</span></span><span>{NAME}</span></a>
    <nav aria-label="Main navigation">
      <a href="{root}#work">Work</a>
      <a href="{root}readme/"{about_current}>About</a>
      <a href="#contact">Contact</a>
    </nav>
    <button class="jump-trigger" type="button" aria-haspopup="dialog" aria-controls="jump-dialog" hidden>
      <span class="search-icon" aria-hidden="true"></span><span class="jump-label">Jump to</span><kbd aria-hidden="true">⌘ K</kbd>
    </button>
  </div>
</header>
<main id="main" tabindex="-1">
{content}
</main>
{footer(root)}
{"" if not_found else command_menu(root)}
</body>
</html>
"""


def simple_page():
    projects = "".join(f'<li><a href="../{project_path(p)}">{p["name"]}</a> — {p["intro"]}</li>'
                       for p in PROJECTS)
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
<header><a href="../">Full portfolio</a></header>
<main><h1>{NAME}</h1><p>{BIO}</p>
<h2>Projects</h2><ul>{projects}</ul>
<h2>Open source</h2><p><a href="{HOME_ASSISTANT_PR}">Home Assistant HomeKit integration contribution</a></p>
<h2>Contact</h2><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><a href="{GITHUB}">GitHub</a></li><li><a href="{LINKEDIN}">LinkedIn</a></li></ul>
</main>
</body>
</html>
"""


def site_files():
    files = {
        "index.html": page(NAME + " · Independent Developer", DESCRIPTION, "", "./", homepage("./"), "home"),
        "readme/index.html": page("About · " + NAME, BIO, "readme/", "../", about_page("../"), "about"),
        "settings/index.html": page("Appearance · " + NAME, "Choose the portfolio’s color theme.",
                                    "settings/", "../", settings_page(), indexable=False),
        "simple/index.html": simple_page(),
        "404.html": page("Page not found · " + NAME, "This page could not be found.", "404.html",
                         "/portfolio/", f"""
<section class="wrap article error-page">
  <p class="eyebrow">404</p><h1>Page not found<span class="name-period">.</span></h1>
  <p class="article-intro">Find the current projects on the portfolio homepage.</p>
  {button("/portfolio/", "Go to the homepage", True)}
</section>""", indexable=False, not_found=True),
    }
    for i, project in enumerate(PROJECTS):
        path = project_path(project)
        next_project = PROJECTS[(i + 1) % len(PROJECTS)]
        files[f"{path}index.html"] = page(f"{project['name']} · {NAME}", project["intro"],
                                          path, "../../", project_page(project, "../../", next_project))
    site_paths = ("", "readme/", *(project_path(project) for project in PROJECTS))
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
