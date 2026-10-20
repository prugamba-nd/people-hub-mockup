#!/usr/bin/env python3
"""Build the static NDT4 People hub. Python standard library only."""
from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SITE = ROOT / 'site'
CATEGORIES = [
    ('governance', 'Governance', 'The leadership and advisory community guiding our work.'),
    ('faculty', 'Faculty', 'Scholars connecting disciplines, research, and teaching.'),
    ('staff', 'Staff', 'The team supporting our people, programs, and partnerships.'),
    ('postdocs-visiting-scholars', 'Postdocs & Visiting Scholars', 'Researchers bringing new ideas and perspectives to our community.'),
    ('students', 'Students', 'Emerging scholars and practitioners working toward a better world.'),
]
PEOPLE = [
    ('maren-okafor', 'Maren Okafor', 'Director; Professor of Global Affairs', 'governance'),
    ('isabel-fontaine', 'Isabel Fontaine', 'Chair, Advisory Council', 'governance'),
    ('priya-raghunathan', 'Priya Raghunathan', 'Associate Professor of Anthropology and Peace Studies', 'faculty'),
    ('daniel-achterberg', 'Daniel Achterberg', 'Professor of Theology and Peace Studies', 'faculty'),
    ('yusra-haddad', 'Yusra Haddad', 'Assistant Professor of Sociology', 'faculty'),
    ('amara-osei', 'Amara Osei', 'Academic Program Manager', 'staff'),
    ('sofia-reyes', 'Sofía Reyes', 'Senior Administrative Coordinator', 'staff'),
    ('declan-murphy', 'Declan Murphy', 'Communications Specialist', 'staff'),
    ('naledi-dlamini', 'Naledi Dlamini', 'Postdoctoral Research Associate', 'postdocs-visiting-scholars'),
    ('linnea-bergstrom', 'Linnea Bergström', 'Visiting Research Fellow', 'postdocs-visiting-scholars'),
    ('ravi-menon', 'Ravi Menon', 'Ph.D. Student, Peace Studies and Sociology', 'students'),
    ('clara-nowak', 'Clara Nowak', 'Master of Global Affairs Student', 'students'),
]
LABELS = {slug: label for slug, label, _ in CATEGORIES}


def sidebar(prefix, current=''):
    current_attribute = ' class="current" aria-current="page"'
    items = ''.join(
        f'<li class="{"active" if current == slug else ""}"><a href="{prefix}{slug}/index.html"'
        f'{current_attribute if current == slug else ""}>{escape(label)}</a></li>'
        for slug, label, _ in CATEGORIES
    )
    hub_current = ' class="current" aria-current="page"' if not current else ''
    return f'''<aside class="page-sidebar"><nav class="nav-site nav-site--section" aria-label="People categories"><div id="nav_sub">
<ul class="nav-level-1 depth_1"><li class="first last li-has-children active"><a href="{prefix}index.html"{hub_current}>People</a>
<ul class="nav-level-2 depth_2">{items}</ul></li></ul></div></nav></aside>'''


def card(person, prefix):
    slug, name, title, _ = person
    return f'''<li class="card-container"><article class="card card--person">
<figure class="avatar avatar--lg card-image"><img src="{prefix}assets/avatar-placeholder.svg" alt="" width="600" height="600" loading="lazy"></figure>
<div class="card-body"><h3 class="card-title"><a class="card-link" href="{prefix}profiles/{slug}.html">{escape(name)}</a></h3>
<p class="person-title">{escape(title)}</p></div></article></li>'''


def grid(people, prefix):
    return '<ul class="no-bullets grid grid-md-2 grid-lg-3 people-grid">' + ''.join(card(p, prefix) for p in people) + '</ul>'


def shell(title, body, prefix='', category='', profile=False):
    extra_crumb = ''
    if category:
        category_link = f'<a href="{prefix}{category}/index.html">{escape(LABELS[category])}</a>' if profile else escape(title)
        crumb_current = ' aria-current="page"' if not profile else ''
        extra_crumb = f'<li{crumb_current}>{category_link}</li>'
    if profile:
        extra_crumb += f'<li aria-current="page">{escape(title)}</li>'
    people_crumb = f'<a href="{prefix}index.html">People</a>' if category else 'People'
    return f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="A static People hub mockup for the Keough School of Global Affairs.">
<title>{escape(title)} | Keough School of Global Affairs | University of Notre Dame</title>
<link id="theme-fallback" rel="stylesheet" href="{prefix}assets/fallback.css" media="not all">
<link rel="stylesheet" href="https://conductor.nd.edu/stylesheets/themes/ndt/4.0/ndt.css" onerror="document.getElementById('theme-fallback').media='all'">
<link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body class="people-mockup">
<a class="skip-link" href="#content">Skip to content</a>
<div class="mockup-note">People hub mockup <span aria-hidden="true">·</span> Sample profiles</div>
<div class="wrapper nav-top--false" id="wrapper">
<header class="site-header" id="header">
  <a class="header-mark-mobile" href="https://www.nd.edu/"><img src="{prefix}assets/mobile_mark_s.svg" width="512" height="86" alt="University of Notre Dame"></a>
  <div class="header-group">
    <div class="header-title">
      <a href="https://www.nd.edu/"><img class="header-mark" src="{prefix}assets/academic_mark_s.svg" width="250" height="60" alt="University of Notre Dame"></a>
      <div class="header-title-name"><p class="site-title" id="site-title"><a href="{prefix}index.html">Keough School of Global Affairs</a></p></div>
    </div>
    <div class="header-nav">
      <nav class="nav-primary" id="nav-primary" aria-label="Primary"><div id="primary"><ul>
        <li><a href="https://keough.nd.edu/about/">About</a></li>
        <li class="active"><a href="{prefix}index.html"{'' if category else ' aria-current="page"'}>People</a></li>
        <li><a href="https://keough.nd.edu/research/">Research</a></li>
        <li><a href="https://keough.nd.edu/academics/">Academics</a></li>
        <li><a href="https://keough.nd.edu/news-and-events/">News &amp; Events</a></li>
      </ul></div></nav>
    </div>
  </div>
</header>
<main class="site-content" id="content" tabindex="-1">
  <div class="page-header"><div class="page-title-wrapper">
    <nav class="breadcrumbs" aria-label="Breadcrumbs"><ol><li><a href="https://keough.nd.edu/">Home</a></li><li{'' if category else ' aria-current="page"'}>{people_crumb}</li>{extra_crumb}</ol></nav>
    <h1 class="page-title">{escape(title)}</h1>
  </div></div>
  <div class="page-primary">{body}</div>
  {sidebar(prefix, category)}
</main>
<footer class="site-footer" id="footer">
  <div class="footer-org"><p class="site-link">Keough School of Global Affairs</p><p>University of Notre Dame</p></div>
  <div class="footer-nd"><a href="https://www.nd.edu/"><img src="{prefix}assets/academic_mark_s.svg" width="250" height="60" alt="University of Notre Dame"></a></div>
  <div class="footer-global"><p><a href="https://www.nd.edu/copyright/">© 2026 University of Notre Dame</a> <span aria-hidden="true">·</span> <a href="https://www.nd.edu/about/accessibility/">Accessibility</a></p><p class="mockup-footer">Static design mockup. Names, roles, and profiles are fictional; portraits are placeholders.</p></div>
</footer>
</div>
</body>
</html>
'''


def write(relative, content):
    output = SITE / relative
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding='utf-8')


intro = '''<p class="lede">Our people bring a world of perspectives to a shared purpose: advancing human dignity through research, education, and engagement.</p>
<p>Meet the faculty, staff, scholars, and students who make up the Keough School community.</p>
<figure class="people-photo"><img src="assets/people-wide.jpg" width="800" height="400" alt="Three scholars speaking and exchanging ideas in academic settings." fetchpriority="high"></figure>'''
sections = []
for slug, label, description in CATEGORIES:
    sections.append(f'''<section class="people-section" aria-labelledby="{slug}-heading">
<div class="section-heading"><h2 id="{slug}-heading">{escape(label)}</h2><a class="category-link" href="{slug}/index.html">View all<span class="visually-hidden"> {escape(label)}</span> <span aria-hidden="true">→</span></a></div>
<p>{escape(description)}</p>{grid([p for p in PEOPLE if p[3] == slug], '')}</section>''')
write('index.html', shell('People', intro + ''.join(sections)))

for slug, label, description in CATEGORIES:
    write(f'{slug}/index.html', shell(label, f'<p class="lede">{escape(description)}</p>' + grid([p for p in PEOPLE if p[3] == slug], '../'), '../', slug))

for person in PEOPLE:
    slug, name, title, category = person
    body = f'''<div class="sample-profile">
<figure class="avatar avatar--xl"><img src="../assets/avatar-placeholder.svg" width="600" height="600" alt=""></figure>
<div><p class="lede">{escape(title)}</p><p>Keough School of Global Affairs</p><p class="sample-label">Sample profile</p></div></div>
<h2>Biography</h2><p>This fictional profile illustrates the destination of a People listing. A published profile would introduce the person’s work, expertise, and role in the community.</p>
<p><a class="btn" href="../{category}/index.html">Back to {escape(LABELS[category])}</a></p>'''
    write(f'profiles/{slug}.html', shell(name, body, '../', category, profile=True))

write('.nojekyll', '')
print(json.dumps({'pages': 1 + len(CATEGORIES) + len(PEOPLE), 'profiles': len(PEOPLE), 'categories': [label for _, label, _ in CATEGORIES]}))
