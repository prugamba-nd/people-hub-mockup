#!/usr/bin/env python3
"""Build the static NDT4 People hub. Python standard library only."""
from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SITE = ROOT / 'site'
SITE_NAME = 'Institute Title'
CATEGORIES = [
    ('governance', 'Governance', 'The leadership and advisory community guiding our work.'),
    ('faculty', 'Faculty', 'Scholars connecting disciplines, research, and teaching.'),
    ('staff', 'Staff', 'The team supporting our people, programs, and partnerships.'),
    ('postdocs-visiting-scholars', 'Visiting Scholars & Fellows', 'Researchers bringing new ideas and perspectives to our community.'),
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
SUBCATEGORIES = {
    'governance': [
        ('leadership', 'Leadership', ('maren-okafor',)),
        ('advisory', 'Advisory', ('isabel-fontaine',)),
    ],
    'faculty': [
        ('core-affiliated-faculty', 'Core Affiliated Faculty', ('priya-raghunathan', 'yusra-haddad')),
        ('faculty-fellows', 'Faculty Fellows', ('daniel-achterberg',)),
        ('associated-faculty', 'Associated Faculty', ()),
        ('emeriti', 'Emeriti', ()),
    ],
    'staff': [
        ('postdoctoral-researchers', 'Postdoctoral Researchers', ('naledi-dlamini',)),
    ],
    'postdocs-visiting-scholars': [
        ('postdocs-visiting-scholars', 'Postdocs & Visiting Scholars', ('naledi-dlamini', 'linnea-bergstrom')),
        ('fellows', 'Fellows', ('linnea-bergstrom',)),
        ('affiliate', 'Affiliate', ()),
        ('past', 'Past', ()),
    ],
    'students': [
        ('graduate', 'Graduate', ('ravi-menon', 'clara-nowak')),
        ('undergraduate', 'Undergraduate', ()),
    ],
}


def sidebar(prefix, current='', child='', profile=False, embedded=False):
    current_attribute = ' class="current" aria-current="page"'
    items = []
    for slug, label, _ in CATEGORIES:
        children = []
        for subslug, sublabel, _ in SUBCATEGORIES[slug]:
            selected = current == slug and child == subslug
            active = ' class="active"' if selected else ''
            children.append(f'<li{active}><a href="{prefix}{slug}/{subslug}/index.html"'
                            f'{current_attribute if selected else ""}>{escape(sublabel)}</a></li>')
        active = ' active' if current == slug else ''
        selected = current == slug and not child and not profile
        items.append(f'<li class="li-has-children{active}"><a href="{prefix}{slug}/index.html"'
                     f'{current_attribute if selected else ""}>{escape(label)}</a>'
                     f'<ul class="nav-level-3 depth_3 no-bullets">{"".join(children)}</ul></li>')
    items = ''.join(items)
    hub_current = ' class="current" aria-current="page"' if not current else ''
    nav_id = 'nav_menu' if embedded else 'nav_sub'
    nav_label = 'People menu' if embedded else 'People categories'
    navigation = f'''<nav class="nav-site nav-site--section" aria-label="{nav_label}"><div id="{nav_id}">
<ul class="nav-level-1 depth_1 no-bullets"><li class="first last li-has-children active"><a href="{prefix}index.html"{hub_current}>People</a>
<ul class="nav-level-2 depth_2 no-bullets">{items}</ul></li></ul></div></nav>'''
    return navigation if embedded else f'<aside class="page-sidebar">{navigation}</aside>'


def card(person, prefix):
    slug, name, title, _ = person
    return f'''<li class="card-container"><article class="card card--person">
<figure class="avatar avatar--lg card-image"><img src="{prefix}assets/avatar-placeholder.svg" alt="" width="600" height="600" loading="lazy"></figure>
<div class="card-body"><h3 class="card-title"><a class="card-link" href="{prefix}profiles/{slug}.html">{escape(name)}</a></h3>
<p class="person-title">{escape(title)}</p></div></article></li>'''


def grid(people, prefix):
    return '<ul class="no-bullets grid grid-md-2 grid-lg-3 people-grid">' + ''.join(card(p, prefix) for p in people) + '</ul>'


def category_people(category):
    members = {slug for _, _, slugs in SUBCATEGORIES[category] for slug in slugs}
    return [p for p in PEOPLE if p[3] == category or p[0] in members]


def shell(title, body, prefix='', category='', profile=False, subcategory='', hero=False):
    primary_links = []
    for label, href in [
        ('About', 'https://keough.nd.edu/about/'),
        ('People', f'{prefix}index.html'),
        ('Research', 'https://keough.nd.edu/research/'),
        ('Academics', 'https://keough.nd.edu/academics/'),
        ('News &amp; Events', 'https://keough.nd.edu/news-and-events/'),
    ]:
        active = ' class="active"' if label == 'People' else ''
        current = ' aria-current="page"' if label == 'People' and not category else ''
        primary_links.append(f'<li{active}><a href="{href}"{current}>{label}</a></li>')
    primary_links = ''.join(primary_links)
    menu_button = '''<div class="header-util"><div class="header-nav-toggle"><button type="button" class="btn btn--action global-menu-toggle" aria-label="Open site menu" aria-controls="global-menu" aria-haspopup="dialog"><svg viewBox="0 0 32 32" width="32" height="32" aria-hidden="true" focusable="false"><path d="M5 8h22M5 16h22M5 24h22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div></div>'''
    extra_crumb = ''
    if category:
        is_parent = not profile and not subcategory
        category_link = escape(LABELS[category]) if is_parent else f'<a href="{prefix}{category}/index.html">{escape(LABELS[category])}</a>'
        crumb_current = ' aria-current="page"' if is_parent else ''
        extra_crumb = f'<li{crumb_current}>{category_link}</li>'
    if profile or subcategory:
        extra_crumb += f'<li aria-current="page">{escape(title)}</li>'
    people_crumb = f'<a href="{prefix}index.html">People</a>' if category else 'People'
    header_class = 'page-header page-header--container contain bg--dark' if hero else 'page-header'
    hero_image = f'''<figure class="page-image bg--gradient bg--dark bg--to-top-right"><img src="{prefix}assets/people-wide.jpg" width="800" height="400" alt="Three scholars speaking and exchanging ideas in academic settings." fetchpriority="high"></figure>''' if hero else ''
    return f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="A static People hub mockup for {escape(SITE_NAME)}.">
<title>{escape(title)} | {escape(SITE_NAME)} | University of Notre Dame</title>
<link id="theme-fallback" rel="stylesheet" href="{prefix}assets/fallback.css" media="not all">
<link rel="stylesheet" href="https://conductor.nd.edu/stylesheets/themes/ndt/4.0/ndt.css" onerror="document.getElementById('theme-fallback').media='all'">
<link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body class="people-mockup">
<a class="skip-link" href="#content">Skip to content</a>
<div class="wrapper nav-top--false" id="wrapper">
<header class="site-header" id="header">
  <a class="header-mark-mobile" href="https://www.nd.edu/"><img src="{prefix}assets/mobile_mark_s.svg" width="512" height="86" alt="University of Notre Dame"></a>
  <div class="header-group header-group--inline-xl">
    <div class="header-title">
      <a href="https://www.nd.edu/"><img class="header-mark" src="{prefix}assets/academic_mark_s.svg" width="250" height="60" alt="University of Notre Dame"></a>
      <div class="header-title-name"><p class="site-title" id="site-title"><a href="{prefix}index.html">{escape(SITE_NAME)}</a></p></div>
    </div>
    <div class="header-nav">
      <nav class="nav-primary" id="nav-primary" aria-label="Primary"><div id="primary"><ul>{primary_links}</ul></div></nav>
      {menu_button}
    </div>
  </div>
</header>
<main class="site-content" id="content" tabindex="-1">
  <div class="{header_class}">{hero_image}<div class="page-title-wrapper">
    <nav class="breadcrumbs" aria-label="Breadcrumbs"><ol><li><a href="https://keough.nd.edu/">Home</a></li><li{'' if category else ' aria-current="page"'}>{people_crumb}</li>{extra_crumb}</ol></nav>
    <h1 class="page-title">{escape(title)}</h1>
  </div></div>
  <div class="page-primary">{body}</div>
  {sidebar(prefix, category, subcategory, profile)}
</main>
<footer class="site-footer" id="footer">
  <div class="footer-org"><p class="site-link">{escape(SITE_NAME)}</p><p>University of Notre Dame</p></div>
  <div class="footer-nd"><a href="https://www.nd.edu/"><img src="{prefix}assets/academic_mark_s.svg" width="250" height="60" alt="University of Notre Dame"></a></div>
  <div class="footer-global"><p><a href="https://www.nd.edu/copyright/">© 2026 University of Notre Dame</a> <span aria-hidden="true">·</span> <a href="https://www.nd.edu/about/accessibility/">Accessibility</a></p></div>
</footer>
</div>
<div class="header-nav-fixed" id="nav-fixed" hidden><div class="nav-fixed-inner">
  <a class="ndshield" href="{prefix}index.html" aria-label="{escape(SITE_NAME)} home"><img src="{prefix}assets/shield.svg" width="32" height="36" alt=""></a>
  <nav class="nav-primary" aria-label="Fixed primary"><ul>{primary_links}</ul></nav>
  {menu_button}
</div></div>
<dialog class="dialog people-site-menu" id="global-menu" aria-labelledby="menu-title">
  <div class="dialog-header"><h2 class="dialog-heading" id="menu-title">{escape(SITE_NAME)}</h2><form method="dialog" class="dialog-close"><button type="submit" aria-label="Close site menu">×</button></form></div>
  <div class="dialog-content"><nav aria-label="Site menu"><ul class="no-bullets">{primary_links}</ul></nav>
    <details><summary>Browse people</summary>{sidebar(prefix, category, subcategory, profile, embedded=True)}</details>
  </div>
</dialog>
<script>window.NDTConductorHost='https://conductor.nd.edu';</script>
<script src="{prefix}assets/ndt.js" defer></script>
</body>
</html>
'''


def write(relative, content):
    output = SITE / relative
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding='utf-8')


intro = '''<p class="lede">Our people bring a world of perspectives to a shared purpose: advancing human dignity through research, education, and engagement.</p>
<p>Meet the faculty, staff, scholars, and students who make up our institute community.</p>'''
sections = []
for slug, label, description in CATEGORIES:
    sections.append(f'''<section class="people-section" aria-labelledby="{slug}-heading">
<div class="section-heading"><h2 id="{slug}-heading">{escape(label)}</h2><a class="category-link" href="{slug}/index.html">View all<span class="visually-hidden"> {escape(label)}</span> <span aria-hidden="true">→</span></a></div>
<p>{escape(description)}</p>{grid(category_people(slug), '')}</section>''')
write('index.html', shell('People', intro + ''.join(sections), hero=True))

for slug, label, description in CATEGORIES:
    write(f'{slug}/index.html', shell(label, f'<p class="lede">{escape(description)}</p>' + grid(category_people(slug), '../'), '../', slug))
    for subslug, sublabel, members in SUBCATEGORIES[slug]:
        people = [p for p in PEOPLE if p[0] in members]
        listing = grid(people, '../../') if people else '<p>Profiles coming soon.</p>'
        body = f'<p class="lede">{escape(sublabel)} at {escape(SITE_NAME)}.</p>{listing}'
        write(f'{slug}/{subslug}/index.html', shell(sublabel, body, '../../', slug, subcategory=subslug))

for person in PEOPLE:
    slug, name, title, category = person
    body = f'''<div class="sample-profile">
<figure class="avatar avatar--xl"><img src="../assets/avatar-placeholder.svg" width="600" height="600" alt=""></figure>
<div><p class="lede">{escape(title)}</p><p>{escape(SITE_NAME)}</p><p class="sample-label">Sample profile</p></div></div>
<h2>Biography</h2><p>This fictional profile illustrates the destination of a People listing. A published profile would introduce the person’s work, expertise, and role in the community.</p>
<p><a class="btn" href="../{category}/index.html">Back to {escape(LABELS[category])}</a></p>'''
    write(f'profiles/{slug}.html', shell(name, body, '../', category, profile=True))

write('.nojekyll', '')
print(json.dumps({'pages': 1 + len(CATEGORIES) + sum(map(len, SUBCATEGORIES.values())) + len(PEOPLE), 'profiles': len(PEOPLE), 'categories': [label for _, label, _ in CATEGORIES]}))
