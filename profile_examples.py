"""NDT4 profile destination examples. Uses unmodified NDT4 components."""
def build(ns):
    root=ns['SITE']/'profile-examples';root.mkdir(exist_ok=True)
    school='https://keough.nd.edu/about/faculty-staff-directory/scott-appleby/'
    host='https://politicalscience.nd.edu/people/daniel-philpott/'
    def page(slug,title,body,profile=False,note='',role='',category='',subcategory=''):
        folder=root/slug;folder.mkdir(exist_ok=True)
        html=ns['shell'](title,body,prefix='../../',category=category or ('faculty' if profile else ''),profile=profile,subcategory=subcategory)
        if role:
            html=html.replace(f'<h1 class="page-title">{title}</h1>',f'<h1 class="page-title person-name">{title}</h1><p class="person-title">{role}</p>')
        html=html.replace('<p class="site-link">Institute Title</p>','<p class="site-link">Institute Title</p><p><a href="../index.html">Compare profile examples</a></p>'+ (f'<p>{note}</p>' if note else ''))
        (folder/'index.html').write_text(html)
    body=f'''<ul class="grid grid-md-2 grid-lg-4"><li class="card-container"><article class="card card--person">
<figure class="avatar avatar--lg card-image"><img src="../assets/scott-appleby.jpg" width="600" height="600" alt="Scott Appleby"></figure>
<div class="card-body"><h2 class="card-title"><a class="card-link" href="{school}" aria-label="Scott Appleby — profile on the Keough School website">Scott Appleby</a></h2><p class="person-title">Keough-Hesburgh Professor of Global Affairs</p></div></article></li></ul>'''
    page('external-profile','People Directory',body,note='Directory example: this profile is maintained on the Keough School website.')
    body='''<div class="grid grid-lg-3">
<div class="person-photo order-lg-2"><figure class="avatar"><img src="../../assets/avatar-placeholder.svg" width="600" height="600" alt=""></figure>
<dl class="list--grid"><dt>Office</dt><dd>Institute Title<br>Notre Dame, IN 46556</dd><dt>Email</dt><dd><a href="mailto:maren.okafor@example.org">maren.okafor@example.org</a></dd></dl></div>
<div class="person-content span-md-2">
<p>Maren Okafor studies how institutions respond to the needs of the communities they serve. Her research examines the relationship between public participation, local governance, and access to essential services.</p>
<p>As director of Institute Title, she leads its research and educational programs, supports faculty collaboration, and builds partnerships with community organizations. Her work brings together researchers and practitioners to understand how public decisions are made and whose perspectives inform them.</p>
<p>Okafor combines comparative policy analysis with interviews and collaborative field research. She is particularly interested in how local knowledge can inform the design and evaluation of public programs. Her research spans participatory governance, public accountability, and community-led policy evaluation.</p>
<p>Her current project examines how community organizations and local governments work together to identify priorities and evaluate public services. The project produces comparative case studies and practical resources for research partners.</p>
<p>Okafor teaches courses on governance, research methods, and public policy. She advises graduate students and mentors undergraduate researchers working with community partners.</p>
<p>She holds a doctorate in political science, a master’s degree in public policy, and a bachelor’s degree in political science.</p>
</div></div>'''
    page('full-bio','Maren Okafor',body,True,'Full institute-hosted biography example. Person, biography, and contact details are fictional.',role='Director; Professor of Global Affairs')
    body=f'''<div class="grid grid-lg-3">
<div class="person-photo order-lg-2"><figure class="avatar"><img src="../assets/daniel-philpott.jpg" width="600" height="600" alt="Daniel Philpott"></figure><dl class="list--grid"><dt>Office</dt><dd>2034 Jenkins and Nanovic Halls<br>Notre Dame, IN 46556</dd><dt>Email</dt><dd><a href="mailto:philpott.1@nd.edu">philpott.1@nd.edu</a></dd></dl></div>
<div class="person-content span-md-2">
<p>Daniel Philpott is affiliated with the Kroc Institute for International Peace Studies. His research on reconciliation, religious freedom, and religion in global politics connects with the institute’s focus on peacebuilding.</p>
<p>His full biography, publications, and contact information are maintained by Notre Dame’s Department of Political Science.</p>
<p><a class="btn" href="{host}" aria-label="Read Daniel Philpott’s full biography on the Department of Political Science website">Read full biography</a></p>
</div></div>'''
    page('abridged-bio','Daniel Philpott',body,True,f'Abridged institute biography example. Public profile information: <a href="{host}">Department of Political Science</a>.',role='Professor of Political Science')
    from html import escape
    past=sorted(ns['PEOPLE'][:8],key=lambda person:person[1].split()[-1])
    names='<ul class="no-bullets">'+''.join(f'<li>{escape(person[1])}</li>' for person in past)+'</ul>'
    images='<ul class="grid grid-md-2 grid-lg-4 no-bullets">'+''.join(f'<li><figure class="avatar"><img src="../../assets/avatar-placeholder.svg" width="600" height="600" alt="" loading="lazy"></figure><p>{escape(person[1])}</p></li>' for person in past)+'</ul>'
    for slug,body in [('names-only',names),('images-and-names',images)]:
        page(slug,'Past Scholars & Fellows',body,note='Historical listing example. All names are fictional; entries do not open biography pages.',category='scholars-fellows',subcategory='past-scholars-fellows')
    body='''<p>NDT4 examples of full and abridged biographies, external profile destinations, and simple historical listings.</p>
<ol><li><h2><a href="external-profile/">Directory entry linking directly offsite</a></h2><p>The external-link arrow appears automatically on the native People Card. Clicking the card opens the full profile on the Keough School website.</p></li>
<li><h2><a href="full-bio/">Full institute biography</a></h2><p>A locally maintained profile with biography, research, teaching, and education. This example uses a fictional person.</p></li>
<li><h2><a href="abridged-bio/">Abridged institute biography</a></h2><p>A short institute-focused biography with a button to the full profile maintained outside the Keough School website.</p></li>
<li><h2><a href="names-only/">Simple historical list: names only</a></h2><p>Alphabetical names without profile links, roles, or biographies.</p></li>
<li><h2><a href="images-and-names/">Simple historical list: images and names</a></h2><p>Four columns of images and names, without clickable profile cards.</p></li></ol>'''
    html=ns['shell']('Profile page examples',body,prefix='../')
    (root/'index.html').write_text(html)
