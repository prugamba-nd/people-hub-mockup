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
    ('scholars-fellows', 'Scholars & Fellows', 'Postdoctoral researchers, visiting scholars, and fellows in our community.'),
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
    ('naledi-dlamini', 'Naledi Dlamini', 'Postdoctoral Research Associate', 'scholars-fellows'),
    ('linnea-bergstrom', 'Linnea Bergström', 'Visiting Research Fellow', 'scholars-fellows'),
    ('ravi-menon', 'Ravi Menon', 'Ph.D. Student, Peace Studies and Sociology', 'students'),
    ('clara-nowak', 'Clara Nowak', 'Master of Global Affairs Student', 'students'),
    ('malia-brooks', 'Malia Brooks', 'Undergraduate Student, Political Science and Peace Studies', 'students'),
]
LABELS = {slug: label for slug, label, _ in CATEGORIES}
SUBCATEGORIES = {
    'governance': [
        ('advisory', 'Advisory', ('isabel-fontaine',)),
    ],
    'faculty': [
        ('faculty-fellows', 'Faculty Fellows', ('daniel-achterberg',)),
        ('associated-faculty', 'Associated Faculty', ()),
        ('emeriti', 'Emeriti', ()),
    ],
    'staff': [],
    'scholars-fellows': [
        ('postdoctoral-researchers', 'Postdoctoral Researchers', ('naledi-dlamini',)),
        ('affiliates', 'Affiliates', ()),
        ('past-scholars-fellows', 'Past Scholars & Fellows', ()),
    ],
    'students': [
        ('phd', 'PhD', ('ravi-menon',)),
    ],
}
LANDING_GROUPS = {
    'governance': ('maren-okafor',),
    'faculty': ('priya-raghunathan', 'yusra-haddad'),
    'staff': ('amara-osei', 'sofia-reyes', 'declan-murphy'),
    'scholars-fellows': ('linnea-bergstrom',),
    'students': ('clara-nowak', 'malia-brooks'),
}
LANDING_LABELS = {
    'governance': 'Leadership',
    'faculty': 'Core Affiliated Faculty',
    'scholars-fellows': 'Visiting Scholars & Fellows',
    'students': 'Undergraduate and Graduate Students',
}


def sidebar(prefix, current='', child='', profile=False, embedded=False):
    current_attribute = ' class="current" aria-current="page"'
    nav_id = 'nav_menu' if embedded else 'nav_sub'
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
        expanded = current == slug
        child_id = f'{nav_id}-{slug}'
        hidden = '' if expanded else ' hidden'
        if children:
            items.append(f'<li class="li-has-children{active}"><a href="{prefix}{slug}/index.html"'
                         f'{current_attribute if selected else ""} aria-expanded="{str(expanded).lower()}" aria-controls="{child_id}">{escape(label)}</a>'
                         f'<ul class="nav-level-2 depth_2 no-bullets" id="{child_id}"{hidden}>{"".join(children)}</ul></li>')
        else:
            list_class = f' class="{active.strip()}"' if active else ''
            items.append(f'<li{list_class}><a href="{prefix}{slug}/index.html"'
                         f'{current_attribute if selected else ""}>{escape(label)}</a></li>')
    items = ''.join(items)
    nav_label = 'People menu' if embedded else 'People categories'
    navigation = f'''<nav class="nav-site" aria-label="{nav_label}"><div id="{nav_id}">
<ul class="nav-level-1 depth_1 no-bullets">{items}</ul></div></nav>'''
    return navigation if embedded else f'<aside class="page-sidebar">{navigation}</aside>'


def card(person, prefix):
    slug, name, title, _ = person
    return f'''<li class="card-container"><article class="card card--person">
<figure class="avatar avatar--lg card-image"><img src="{prefix}assets/avatar-placeholder.svg" alt="" width="600" height="600" loading="lazy"></figure>
<div class="card-body"><h3 class="card-title"><a class="card-link" href="{prefix}profiles/{slug}.html">{escape(name)}</a></h3>
<p class="person-title">{escape(title)}</p></div></article></li>'''


def grid(people, prefix):
    return '<ul class="grid grid-md-2 grid-lg-3">' + ''.join(card(p, prefix) for p in people) + '</ul>'


def category_people(category):
    members = set(LANDING_GROUPS[category])
    return [p for p in PEOPLE if p[0] in members]


def shell(title, body, prefix='', category='', profile=False, subcategory='', hero=False, lede=''):
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
    menu_button = f'''<div class="header-util"><div class="header-nav-toggle"><button type="button" class="btn btn--action global-menu-toggle" aria-label="Open site menu" aria-controls="global-menu" aria-haspopup="dialog"><svg class="icon" aria-hidden="true" focusable="false"><use href="{prefix}assets/ndt4-v1.svg#icon-menu"></use></svg></button></div></div>'''
    extra_crumb = ''
    if category:
        is_parent = not profile and not subcategory
        category_link = escape(LABELS[category]) if is_parent else f'<a href="{prefix}{category}/index.html">{escape(LABELS[category])}</a>'
        crumb_current = ' aria-current="page"' if is_parent else ''
        extra_crumb = f'<li{crumb_current}>{category_link}</li>'
    if profile or subcategory:
        extra_crumb += f'<li aria-current="page">{escape(title)}</li>'
    people_crumb = f'<a href="{prefix}index.html">People</a>' if category else 'People'
    header_class = 'page-header page-header--inset' if hero else 'page-header'
    hero_image = f'''<figure class="page-image"><img src="{prefix}assets/people-wide.jpg" width="800" height="400" alt="Three scholars speaking and exchanging ideas in academic settings." fetchpriority="high"></figure>''' if hero else ''
    header_lede = f'\n    <p class="page-lede">{escape(lede)}</p>' if lede else ''
    return f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="A static People hub mockup for {escape(SITE_NAME)}.">
<title>{escape(title)} | {escape(SITE_NAME)} | University of Notre Dame</title>
<link rel="stylesheet" href="https://conductor.nd.edu/stylesheets/themes/ndt/4.0/ndt.css">
</head>
<body>
<ul class="skip-links"><li><a href="#content">Skip to content</a></li></ul>
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
    <h1 class="page-title">{escape(title)}</h1>{header_lede}
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
  <a class="ndshield" href="{prefix}index.html" aria-label="{escape(SITE_NAME)} home"><svg aria-hidden="true" focusable="false"><use href="{prefix}assets/ndt4-v1.svg#shield"></use></svg></a>
  <nav class="nav-primary" aria-label="Fixed primary"><ul>{primary_links}</ul></nav>
  {menu_button}
</div></div>
<dialog class="dialog" id="global-menu" aria-labelledby="menu-title">
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


intro_lede = 'Our people bring a world of perspectives to a shared purpose: advancing human dignity through research, education, and engagement.'
hub_intro = '<h2>Directory</h2><p>Meet the faculty, staff, scholars, and students who make up our institute community.</p>'
write('index.html', shell('People', hub_intro + grid(PEOPLE, ''), hero=True, lede=intro_lede))

for slug, label, description in CATEGORIES:
    landing_heading = f'<h2>{escape(LANDING_LABELS[slug])}</h2>' if slug in LANDING_LABELS else ''
    body = f'<p class="lede">{escape(description)}</p>{landing_heading}{grid(category_people(slug), "../")}'
    write(f'{slug}/index.html', shell(label, body, '../', slug))
    for subslug, sublabel, members in SUBCATEGORIES[slug]:
        people = [p for p in PEOPLE if p[0] in members]
        listing = grid(people, '../../') if people else '<p>Profiles coming soon.</p>'
        body = f'<p class="lede">{escape(sublabel)} at {escape(SITE_NAME)}.</p>{listing}'
        write(f'{slug}/{subslug}/index.html', shell(sublabel, body, '../../', slug, subcategory=subslug))

for person in PEOPLE:
    slug, name, title, category = person
    body = f'''<div class="card-container mbe-3"><div class="card card--person card--horizontal">
<figure class="avatar avatar--lg card-image"><img src="../assets/avatar-placeholder.svg" width="600" height="600" alt=""></figure>
<div class="card-body"><p class="lede">{escape(title)}</p><p>{escape(SITE_NAME)}</p><p>Sample profile</p></div></div></div>
<h2>Biography</h2><p>This fictional profile illustrates the destination of a People listing. A published profile would introduce the person’s work, expertise, and role in the community.</p>
<p><a class="btn" href="../{category}/index.html">Back to {escape(LABELS[category])}</a></p>'''
    write(f'profiles/{slug}.html', shell(name, body, '../', category, profile=True))

write('.nojekyll', '')
print(json.dumps({'pages': 1 + len(CATEGORIES) + sum(map(len, SUBCATEGORIES.values())) + len(PEOPLE), 'profiles': len(PEOPLE), 'categories': [label for _, label, _ in CATEGORIES]}))


NDT3_SITE = SITE / 'ndt3'


def write_ndt3(relative, content):
    output = NDT3_SITE / relative
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding='utf-8')


def ndt3_sidebar(prefix, current='', child='', profile=False):
    items = []
    for slug, label, _ in CATEGORIES:
        active = current == slug
        selected = active and not child and not profile
        parent_class = ' class="active"' if active else ''
        children = []
        if active:
            for subslug, sublabel, _ in SUBCATEGORIES[slug]:
                selected_child = child == subslug
                child_class = ' class="active"' if selected_child else ''
                current_attr = ' class="current" aria-current="page"' if selected_child else ''
                children.append(f'<li{child_class}><a href="{prefix}{slug}/{subslug}/index.html"{current_attr}>{escape(sublabel)}</a></li>')
        parent_current = ' class="current" aria-current="page"' if selected else ''
        nested = f'<ul class="nav-level-2 depth_2">{"".join(children)}</ul>' if children else ''
        items.append(f'<li{parent_class}><a href="{prefix}{slug}/index.html"{parent_current}>{escape(label)}</a>{nested}</li>')
    return '<nav id="nav" class="nav-site nav-section" aria-label="People categories"><ul class="nav-level-1 depth_1">' + ''.join(items) + '</ul></nav>'


def ndt3_card(person, prefix):
    slug, name, title, _ = person
    return f'''<li class="card card-person hover-bg hover-grow">
<figure class="card-image"><img class="image-circle" src="{prefix}../assets/avatar-placeholder.svg" width="600" height="600" alt="" loading="lazy"></figure>
<div class="card-body"><p class="card-title"><a class="card-link" href="{prefix}profiles/{slug}.html">{escape(name)}</a></p>
<p class="person-title">{escape(title)}</p></div></li>'''


def ndt3_grid(people, prefix):
    return '<ul class="grid grid-sm-2 grid-md-4">' + ''.join(ndt3_card(person, prefix) for person in people) + '</ul>'


def ndt3_shell(title, body, prefix='', category='', profile=False, subcategory='', hero=False, lede=''):
    if subcategory:
        crumbs = f'<li><a href="{prefix}{category}/index.html">{escape(LABELS[category])}</a> &rsaquo;</li><li aria-current="page">{escape(title)}</li>'
    elif category and profile:
        crumbs = f'<li><a href="{prefix}{category}/index.html">{escape(LABELS[category])}</a> &rsaquo;</li><li aria-current="page">{escape(title)}</li>'
    elif category:
        crumbs = f'<li aria-current="page">{escape(title)}</li>'
    else:
        crumbs = '<li aria-current="page">People</li>'
    hero_image = f'<figure class="page-image inset"><img src="{prefix}../assets/people-wide.jpg" alt="Scholars gathered in conversation" width="1600" height="700"></figure>' if hero else ''
    page_lede = f'<p class="lede">{escape(lede)}</p>' if lede else ''
    page_header = (f'<div class="page-header has-title has-image"><h1 class="page-title">{escape(title)}</h1>'
                   f'<p class="page-lede">{escape(lede)}</p>{hero_image}</div>' if hero else '<div class="page-header"></div>')
    main_title = f'<h1 class="page-title">{escape(title)}</h1>{page_lede}'
    navigation = ndt3_sidebar(prefix, category, subcategory, profile)
    primary = f'''<nav id="nav-top" class="nav-top" role="navigation" aria-label="Primary navigation"><div id="primary"><ul>
<li><a href="https://keough.nd.edu/about/">About</a></li><li><a class="active" href="{prefix}index.html">People</a></li><li><a href="https://keough.nd.edu/research/">Research</a></li><li><a href="https://keough.nd.edu/academics/">Academics</a></li><li><a href="https://keough.nd.edu/news-and-events/">News &amp; Events</a></li>
</ul></div></nav>'''
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<meta name="description" content="A static NDT3 People hub mockup for Institute Title.">
<title>{escape(title)} | Institute Title | University of Notre Dame</title>
<link rel="stylesheet" type="text/css" href="https://conductor.nd.edu/stylesheets/themes/ndt/3.0/ndt.css">
</head><body vocab="https://schema.org/" class="nav-top-true">
<nav class="skip-links" aria-label="Skip links"><ul><li><a href="#content">Skip To Content</a></li><li><a href="#nav-top">Skip To Navigation</a></li></ul></nav>
<div class="wrapper" id="wrapper">
<header id="header" class="site-header"><p class="mark-header"><a href="https://www.nd.edu/">University of Notre Dame</a></p>
<div class="site-title-group"><p id="site-title" class="site-title"><a href="{prefix}index.html">Institute Title</a></p></div>
<div class="nav-header">{primary}</div><div class="nav-mobile-util"><ul class="no-bullets"><li><a href="{prefix}index.html">People</a></li><li><a class="nav-menu nav-skip" href="#nav">Menu</a></li></ul></div></header>
<div id="content" class="site-content">
{page_header}
<main class="page-main" role="main"><ol class="breadcrumbs"><li><a href="https://keough.nd.edu/">Home</a> &rsaquo;</li>{f'<li><a href="{prefix}index.html">People</a> &rsaquo;</li>' if category or profile or subcategory else ''}{crumbs}</ol>
{main_title}
{body}</main>
<aside class="page-sidebar">{navigation}</aside>
</div>
<footer id="footer" class="site-footer" role="contentinfo"><div class="footer-org" typeof="Organization"><p><a href="{prefix}index.html" class="site-link">Institute Title</a></p><p>University of Notre Dame</p><p class="copyright"><a href="https://www.nd.edu/copyright/">&copy; 2026 University of Notre Dame</a></p></div><div class="footer-parent"><a href="https://www.nd.edu/" class="mark-footer">University of Notre Dame</a></div></footer>
</div><script src="https://conductor.nd.edu/javascripts/themes/ndt/3.0/ndt.js"></script></body></html>'''


ndt3_intro = '<h2>Directory</h2><p>Meet the faculty, staff, scholars, and students who make up our institute community.</p>'
write_ndt3('index.html', ndt3_shell('People', ndt3_intro + ndt3_grid(PEOPLE, ''), hero=True, lede=intro_lede))
for slug, label, description in CATEGORIES:
    landing_heading = f'<h2>{escape(LANDING_LABELS[slug])}</h2>' if slug in LANDING_LABELS else ''
    body = f'<p class="lede">{escape(description)}</p>{landing_heading}{ndt3_grid(category_people(slug), "../")}'
    write_ndt3(f'{slug}/index.html', ndt3_shell(label, body, '../', slug))
    for subslug, sublabel, members in SUBCATEGORIES[slug]:
        people = [p for p in PEOPLE if p[0] in members]
        listing = ndt3_grid(people, '../../') if people else '<p>Profiles coming soon.</p>'
        body = f'<p class="lede">{escape(sublabel)} at {escape(SITE_NAME)}.</p>{listing}'
        write_ndt3(f'{slug}/{subslug}/index.html', ndt3_shell(sublabel, body, '../../', slug, subcategory=subslug))
for slug, name, title, category in PEOPLE:
    body = f'''<div class="card-container"><article class="card"><figure class="card-image"><img src="../../assets/avatar-placeholder.svg" width="600" height="600" alt=""></figure><div class="card-body"><p class="lede">{escape(title)}</p><p>Institute Title</p><p>Sample profile</p></div></article></div><h2>Biography</h2><p>This fictional profile illustrates the destination of a People listing. A published profile would introduce the person’s work, expertise, and role in the community.</p><p><a class="btn" href="../{category}/index.html">Back to {escape(LABELS[category])}</a></p>'''
    write_ndt3(f'profiles/{slug}.html', ndt3_shell(name, body, '../', category, profile=True))

print(json.dumps({'ndt3_pages': 1 + len(CATEGORIES) + sum(map(len, SUBCATEGORIES.values())) + len(PEOPLE)}))


NDT24_SITE = SITE / 'ndt24'


def write_ndt24(relative, content):
    output = NDT24_SITE / relative
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding='utf-8')


# Ansari's saved theme and site overrides are vendored in assets/reference.
# Only replace the institute-specific image logo with our placeholder title.
NDT24_NAV_CSS = '''.site-title a {
  background: none;
  text-indent: 0;
  display: flex;
  align-items: center;
  color: #0c2340;
  font-family: Georgia, serif;
  font-size: 2rem;
  white-space: normal;
  max-width: calc(100vw - 5rem);
}
'''


def ndt24_sidebar(prefix, current='', child='', profile=False):
    items = []
    for slug, label, _ in CATEGORIES:
        active = current == slug
        selected = active and not child and not profile
        current_attr = ' class="current-last" aria-current="page"' if selected else ''
        children = []
        if active:
            for subslug, sublabel, _ in SUBCATEGORIES[slug]:
                selected_child = child == subslug
                child_attr = ' class="current-last" aria-current="page"' if selected_child else ''
                children.append(f'<li><a href="{prefix}{slug}/{subslug}/index.html"{child_attr}>{escape(sublabel)}</a></li>')
        nested = f'<ul class="no-bullets">{"".join(children)}</ul>' if children else ''
        active_class = ' class="active"' if active else ''
        items.append(f'<li{active_class}><a href="{prefix}{slug}/index.html"{current_attr}>{escape(label)}</a>{nested}</li>')
    return f'<nav class="nav-section nav-site" aria-label="People categories"><ul class="no-bullets">{"".join(items)}</ul></nav><nav id="nav" class="nav-full nav-site" aria-label="Mobile navigation"><ul>{"".join(items)}</ul></nav>'


def ndt24_grid(people, prefix):
    cards = []
    for slug, name, title, _category in people:
        cards.append(f'''<li class="column small-12 medium-6 large-3">
<article><p><img src="{prefix}../assets/avatar-placeholder.svg" width="600" height="600" alt="" loading="lazy"></p>
<h2 class="entry-title"><a href="{prefix}profiles/{slug}.html">{escape(name)}</a></h2><p>{escape(title)}</p></article></li>''')
    return '<ul class="row no-bullets">' + ''.join(cards) + '</ul>'


def ndt24_shell(title, body, prefix='', category='', profile=False, subcategory='', lede='', hero=False):
    if subcategory:
        crumbs = f'<li><a href="{prefix}{category}/index.html">{escape(LABELS[category])}</a> &rsaquo; </li><li>{escape(title)}</li>'
    elif category and profile:
        crumbs = f'<li><a href="{prefix}{category}/index.html">{escape(LABELS[category])}</a> &rsaquo; </li><li>{escape(title)}</li>'
    elif category:
        crumbs = f'<li>{escape(title)}</li>'
    else:
        crumbs = '<li>Directory</li>'
    navigation = ndt24_sidebar(prefix, category, subcategory, profile)
    people_state = ' class="active li-has-children"'
    people_current = '' if category or profile or subcategory else ' aria-current="page" class="current current-last"'
    primary = f'''<nav id="nav-top" class="nav-top" role="navigation" aria-label="Primary navigation"><div class="row"><div class="column"><div id="primary"><ul class="nav-level-1 depth_1">
<li id="primary_97992" class="first"><a href="https://ansari.nd.edu/" aria-label="Home"><svg class="icon" aria-label="Home"><use xlink:href="#icon-home"></use></svg></a></li>
<li id="primary_97994" class="li-has-children"><a href="https://ansari.nd.edu/about/">About</a></li>
<li id="primary_97996"{people_state}><a href="{prefix}index.html"{people_current}>People</a></li>
<li id="primary_113027" class="li-has-children"><a href="https://ansari.nd.edu/student-opportunities/">Student Opportunities</a></li>
<li id="primary_98005" class="li-has-children"><a href="https://ansari.nd.edu/conference/">Programs</a></li>
<li id="primary_98654" class="last li-has-children"><a href="https://ansari.nd.edu/news-events/">News &amp; Events</a></li>
</ul></div></div></div></nav>'''
    primary = primary.replace('\n', '')
    page_lede = f'<p class="lede">{escape(lede)}</p>' if lede else ''
    hero_image = f'<p class="image-default"><img src="{prefix}../assets/people-wide.jpg" alt="Scholars gathered in conversation" width="1600" height="700"></p>' if hero else ''
    return f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A static NDT 2.4 People directory mockup for Institute Title.">
<title>{escape(title)} | Institute Title | University of Notre Dame</title>
<link rel="stylesheet" href="{prefix}assets/reference/styles/ndt.css">
<link rel="stylesheet" href="{prefix}assets/reference/styles/site.1737718680.css">
<link rel="stylesheet" href="{prefix}assets/ndt24-nav.css">
</head><body class="nav-top-true">
<nav class="skip-links" aria-label="Skip links"><ul><li><a href="#content">Skip To Content</a></li><li><a href="#nav-top">Skip To Navigation</a></li></ul></nav>
<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="display:none"><symbol id="icon-home" viewBox="0 0 950.8578853607178 1024">
	<path class="path1" d="M804.571 566.857v274.286q0 14.857-10.857 25.714t-25.714 10.857h-219.429v-219.429h-146.286v219.429h-219.429q-14.857 0-25.714-10.857t-10.857-25.714v-274.286q0-0.571 0.286-1.714t0.286-1.714l328.571-270.857 328.571 270.857q0.571 1.143 0.571 3.429zM932 527.429l-35.429 42.286q-4.571 5.143-12 6.286h-1.714q-7.429 0-12-4l-395.429-329.714-395.429 329.714q-6.857 4.571-13.714 4-7.429-1.143-12-6.286l-35.429-42.286q-4.571-5.714-4-13.429t6.286-12.286l410.857-342.286q18.286-14.857 43.429-14.857t43.429 14.857l139.429 116.571v-111.429q0-8 5.143-13.143t13.143-5.143h109.714q8 0 13.143 5.143t5.143 13.143v233.143l125.143 104q5.714 4.571 6.286 12.286t-4 13.429z" />
</symbol><symbol id="icon-search" viewBox="0 0 950.8563512165565 1024">
	<path class="path1" d="M658.286 475.429q0-105.714-75.143-180.857t-180.857-75.143-180.857 75.143-75.143 180.857 75.143 180.857 180.857 75.143 180.857-75.143 75.143-180.857zM950.857 950.857q0 29.714-21.714 51.429t-51.429 21.714q-30.857 0-51.429-21.714l-196-195.429q-102.286 70.857-228 70.857-81.714 0-156.286-31.714t-128.571-85.714-85.714-128.571-31.714-156.286 31.714-156.286 85.714-128.571 128.571-85.714 156.286-31.714 156.286 31.714 128.571 85.714 85.714 128.571 31.714 156.286q0 125.714-70.857 228l196 196q21.143 21.143 21.143 51.429z" />
</symbol></svg>
<div class="wrapper" id="wrapper">
<header id="header" role="banner" class="site-header">
    <nav class="brandbar theme-bb-blue" aria-label="Department navigation">
      <div class="row row-container">
        <ul class="column">
          <li class="dept-nd"><a href="https://www.nd.edu/">University of Notre Dame</a></li>
          <li class="dept dept-ksga"><a href="https://keough.nd.edu/">Keough School of Global Affairs</a></li>
        </ul>
      </div>
    </nav>
    <div class="titlebar">
      <div class="row row-container">

        <div class="column large-5">
            <p class="site-title"><a href="{prefix}index.html" accesskey="H">Institute Title</a></p>
          <a href="#nav" class="btn-nav-mobile" aria-label="Menu">
            <svg version="1.1" class="icon-menu" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 20 20" xml:space="preserve">
              <line class="ni ni1" stroke-width="2" stroke-linecap="square" stroke-miterlimit="10" x1="0.98" y1="2" x2="18.94" y2="2" />
              <line class="ni ni2" stroke-width="2" stroke-linecap="square" stroke-miterlimit="10" x1="0.98" y1="8.69" x2="18.94" y2="8.69" />
              <g class="ni ni3">
                <path d="M2.18,19.91l-0.95-2.58l-0.28-0.81l0.01,1.42v1.97H0.04v-5.17h1.08l1.07,2.81l0.35,0.97l0.35-0.97 l1.07-2.81h1.08v5.17H4.12v-1.97l0.01-1.42l-0.28,0.81l-0.95,2.58H2.18z" />
                <path d="M9.7,14.74v0.86H6.96v1.23h2.42v0.86H6.96v1.35h2.86v0.86H6.04v-5.17H9.7z" />
                <path d="M12.15,17.25l-0.51-0.79l0.01,1.24v2.22h-0.93v-5.17h0.85l1.78,2.66l0.51,0.79l-0.01-1.24v-2.22h0.93v5.17 h-0.85L12.15,17.25z" />
                <path d="M15.74,18.02v-3.28h0.93v3.28c0,0.63,0.2,1.12,1.18,1.12c0.98,0,1.18-0.49,1.18-1.12v-3.28h0.93v3.28 c0,1.13-0.5,1.98-2.11,1.98C16.23,20,15.74,19.15,15.74,18.02z" />
              </g>
            </svg>
            <span class="visibility-hidden">Menu</span>
          </a>
        </div>

        <div class="column align-right">
          <div class="header-util">
            <form method="get" action="https://ansari.nd.edu/search/" role="search" id="search" class="search-form" aria-label="Site search"><input type="hidden" name="as_sitesearch" value="ansari.nd.edu"><input type="hidden" name="entqr" value="3"><label for="search-input">Search</label><input type="search" name="q" id="search-input" class="search-input" placeholder="Search"><button type="submit" class="search-button"><svg data-icon="search" class="icon"><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#icon-search" /></svg> <span>Search</span></button></form>
          </div><!-- .header-util -->
          {primary}
        </div>

      </div>
    </div><!-- .titlebar -->
  </header>
<div class="site-hero" aria-hidden="true"></div>
<div id="content" class="site-content cf"><div class="row row-container">
<main class="alpha small-12 medium-8 medium-push-4 large-9 large-push-3 xlarge-10 xlarge-push-2 medium-order-2 columns" role="main">
<div class="site-content-inner">
<ol class="breadcrumbs"><li><a href="https://keough.nd.edu/">Home</a> &rsaquo; </li>{f'<li><a href="{prefix}index.html">Directory</a> &rsaquo; </li>' if category or profile or subcategory else ''}{crumbs}</ol>
<h1 class="page-title">{escape(title)}</h1>{page_lede}{hero_image}{body}</div></main>
<aside class="beta small-12 medium-4 medium-pull-8 large-3 large-pull-9 xlarge-2 xlarge-pull-10 medium-order-1 columns">{navigation}</aside>
</div></div>
<footer id="footer" class="site-footer vcard" role="contentinfo"><div class="row row-container"><div class="column"><div class="footer-inner"><p class="copyright org"><a href="https://www.nd.edu/copyright/">Copyright</a> &copy; 2026 <a href="https://www.nd.edu/" class="org">University of Notre Dame</a></p><p class="contact-info adr"><a href="{prefix}index.html" class="site-link url fn">Institute Title</a><span class="address"><span class="locality">Notre Dame</span>, <span class="region">IN</span> <span class="postal-code">46556</span> <span class="country-name">USA</span></span></p><a href="https://www.nd.edu/" class="ndmark"><img src="https://static.nd.edu/images/marks/blue/ndmark300.png" alt="University of Notre Dame"></a></div></div></div></footer>
</div><script src="https://conductor.nd.edu/javascripts/themes/ndt/2.4/ndt.js"></script></body></html>'''


write_ndt24('assets/ndt24-nav.css', NDT24_NAV_CSS)

ndt24_intro = '<h2>Directory</h2><p>Meet the faculty, staff, scholars, and students who make up our institute community.</p>'
write_ndt24('index.html', ndt24_shell('People', ndt24_intro + ndt24_grid(PEOPLE, ''), lede=intro_lede, hero=True))
for slug, label, description in CATEGORIES:
    landing_heading = f'<h2>{escape(LANDING_LABELS[slug])}</h2>' if slug in LANDING_LABELS else ''
    body = f'<p>{escape(description)}</p>{landing_heading}{ndt24_grid(category_people(slug), "../")}'
    write_ndt24(f'{slug}/index.html', ndt24_shell(label, body, '../', slug))
    for subslug, sublabel, members in SUBCATEGORIES[slug]:
        people = [p for p in PEOPLE if p[0] in members]
        listing = ndt24_grid(people, '../../') if people else '<p>Profiles coming soon.</p>'
        body = f'<p>{escape(sublabel)} at {escape(SITE_NAME)}.</p>{listing}'
        write_ndt24(f'{slug}/{subslug}/index.html', ndt24_shell(sublabel, body, '../../', slug, subcategory=subslug))
for slug, name, title, category in PEOPLE:
    body = f'<p><img src="../../assets/avatar-placeholder.svg" width="600" height="600" alt=""></p><p><strong>{escape(title)}</strong></p><p>Institute Title</p><p>Sample profile</p><h2>Biography</h2><p>This fictional profile illustrates the destination of a directory listing. A published profile would introduce the person’s work, expertise, and role in the community.</p><p><a class="btn" href="../{category}/index.html">Back to {escape(LABELS[category])}</a></p>'
    write_ndt24(f'profiles/{slug}.html', ndt24_shell(name, body, '../', category, profile=True))

print(json.dumps({'ndt24_pages': 1 + len(CATEGORIES) + sum(map(len, SUBCATEGORIES.values())) + len(PEOPLE)}))
