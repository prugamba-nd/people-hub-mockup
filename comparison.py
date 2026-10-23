"""Build isolated, interactive People hub alternatives using the existing NDT3 shell."""
from pathlib import Path
import json
import shutil

def build(ns):
    root=ns['ROOT']; out=ns['SITE']/'compare';out.mkdir(exist_ok=True)
    for filename in ['compare.css','compare.js']:
        shutil.copyfile(root/'comparison-assets'/filename,out/filename)
    first=['Alex','Amara','Anika','Ben','Clara','Daniel','Elena','Farah','Gabriel','Hana','Isabel','James','Kai','Leila','Maya','Noah','Omar','Priya','Ravi','Sofia','Tariq','Uma','Victor','Yara']
    last=['Adams','Bennett','Chen','Diaz','Evans','Flores','Garcia','Hassan','Ito','Jones','Khan','Lee','Martin','Nguyen','Okafor','Patel','Quinn','Reyes','Singh','Taylor','Usman','Vega','Wong','Young','Zhang']
    roles=[('governance','Leadership'),('governance','Advisory'),('faculty','Core Affiliated Faculty'),('faculty','Faculty Fellows'),('faculty','Associated Faculty'),('faculty','Emeriti'),('staff','Staff'),('scholars-fellows','Visiting Scholars'),('scholars-fellows','Fellows'),('scholars-fellows','Postdoctoral Researchers'),('scholars-fellows','Affiliates'),('scholars-fellows','Past Scholars & Fellows'),('students','Graduate'),('students','Undergraduate'),('students','PhD')]
    disciplines=['Political Science','Sociology','History','Economics','Anthropology','Theology']
    regions=['Africa','Asia','Europe','Latin America','Middle East','North America']
    interests=['Migration and citizenship','Democracy and institutions','Peace and conflict','Climate and development','Religion and public life','Education and inequality','Trade and livelihoods']
    people=[]
    for i in range(2040):
        # Weight faculty heavily to make the large-category prototype meaningful.
        group,role=roles[(i//3)%len(roles)] if i%3==0 else ('faculty','Core Affiliated Faculty')
        name=f'{first[i%len(first)]} {chr(65+(i//600)%26)}. {last[(i//len(first))%len(last)]}'
        people.append(dict(id=f'person-{i+1}',name=name,group=group,role=role,discipline=disciplines[(i//3)%6],region=regions[(i//19)%6],interest=interests[i%7],status='past' if role in ['Emeriti','Past Scholars & Fellows'] or i%11==0 else 'current'))
    people.sort(key=lambda p:(p['name'].split()[-1],p['name'],p['id']))
    sample=[]
    for i,(_,name,title,group) in enumerate(ns['PEOPLE']):
        role=next((r for g,r in roles if g==group),group)
        if name=='Isabel Fontaine':role='Advisory'
        if group=='students':role='PhD' if 'Ph.D.' in title else 'Undergraduate' if 'Undergraduate' in title else 'Graduate'
        sample.append(dict(id=f'sample-{i}',name=name,group=group,role=role,discipline=disciplines[i%6],region=regions[i%6],interest=interests[i%7],status='current'))
    sample.sort(key=lambda p:p['name'].split()[-1])
    featured=[next(p['id'] for p in people if p['group']==g and p['status']=='current') for g in ns['LABELS']]
    featured.append(next(p['id'] for p in people if p['role']=='Postdoctoral Researchers' and p['status']=='current'))
    (out/'data.js').write_text('window.directoryPeople='+json.dumps(people)+';\nwindow.samplePeople='+json.dumps(sample)+';\nwindow.featuredIds='+json.dumps(featured)+';')
    modes=[('small','A · Complete small directory','All 13 profiles, with category navigation.'),('directory','B · Searchable full directory','Alphabetical, paginated results; current affiliations by default. Search across 2,040 current and past profiles.'),('gateway','C · Search and browse hub','No initial profiles. Search everyone or choose a category.'),('featured','D · Featured selection','Six explicitly featured profiles, plus access to the complete directory.'),('category','E · Large category with filters','Faculty starts with a large result set. Search, discipline, region, and affiliation narrow this group.')]
    def page(title,body,prefix='../'):
        html=ns['ndt3_shell'](title,body,prefix=prefix)
        return html
    for slug,label,description in modes:
        folder=out/slug;folder.mkdir(exist_ok=True)
        html=page('People','<div id="directory-app"></div><noscript>This interactive comparison requires JavaScript. <a href="../../ndt3/index.html">Open the static directory</a>.</noscript>','../../')
        # Existing theme assets and header retained; own links keep people within this option.
        html=html.replace('href="../../index.html"','href="index.html"')
        html=html.replace('<body vocab=',f'<body data-prototype="{slug}" vocab=')
        bar=f'<div class="prototype-bar"><a href="../index.html">Compare options</a><strong>{label}</strong> — {description}<br>Usability prototype: fictional profiles; no real directory records.</div>'
        html=html.replace('<div class="wrapper" id="wrapper">',bar+'<div class="wrapper" id="wrapper">')
        html=html.replace('</head>','<link rel="stylesheet" href="../compare.css"></head>')
        html=html.replace('</body>','<script src="../data.js"></script><script src="../compare.js"></script></body>')
        (folder/'index.html').write_text(html)
    body='<p>Try each option with the same tasks. The current published hub is unchanged.</p><ol><li>Find Amara A. Adams.</li><li>Find current faculty whose work involves migration.</li><li>Find someone in Political Science with Latin America expertise.</li><li>Find a past affiliate.</li><li>Move from Faculty to Advisory.</li></ol><p>Search/filter tasks apply to the large-directory options. The small directory uses the original 13 sample profiles.</p><ul class="category-links">'+''.join(f'<li><a href="{slug}/index.html"><strong>{label}</strong><br>{description}</a></li>' for slug,label,description in modes)+'</ul><p>While testing, note where you expect to start, whether the result scope is clear, and which controls feel repetitive.</p>'
    html=page('People hub options',body)
    html=html.replace('</head>','<link rel="stylesheet" href="compare.css"></head>')
    (out/'index.html').write_text(html)
    print(json.dumps({'comparison_options':len(modes),'fictional_profiles':len(people)}))
