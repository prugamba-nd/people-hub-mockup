"""NDT4 profile destination examples. Uses unmodified NDT4 components."""
def build(ns):
    root=ns['SITE']/'profile-examples';root.mkdir(exist_ok=True)
    school='https://keough.nd.edu/about/faculty-staff-directory/scott-appleby/'
    host='https://politicalscience.nd.edu/people/daniel-philpott/'
    def page(slug,title,body,profile=False,note=''):
        folder=root/slug;folder.mkdir(exist_ok=True)
        html=ns['shell'](title,body,prefix='../../',category='faculty' if profile else '',profile=profile)
        html=html.replace('<p class="site-link">Institute Title</p>','<p class="site-link">Institute Title</p><p><a href="../index.html">Compare profile examples</a></p>'+ (f'<p>{note}</p>' if note else ''))
        (folder/'index.html').write_text(html)
    body=f'''<ul class="grid grid-md-2 grid-lg-4"><li class="card-container"><article class="card card--person">
<figure class="avatar avatar--lg card-image"><img src="../assets/scott-appleby.jpg" width="600" height="600" alt="Scott Appleby"></figure>
<div class="card-body"><h2 class="card-title"><a class="card-link" href="{school}" aria-label="Scott Appleby — profile on the Keough School website">Scott Appleby</a></h2><p class="person-title">Keough-Hesburgh Professor of Global Affairs</p></div></article></li></ul>'''
    page('external-profile','People Directory',body,note='Directory example: this profile is maintained on the Keough School website.')
    body='''<div class="card-container"><article class="card card--person card--horizontal">
<figure class="avatar avatar--lg card-image"><img src="../../assets/avatar-placeholder.svg" width="600" height="600" alt=""></figure>
<div class="card-body"><p class="person-title">Director; Professor of Global Affairs</p><p>Institute Title</p><p>Research: governance, civic participation, and public policy</p></div></article></div>
<h2>Biography</h2>
<p>Maren Okafor studies how institutions respond to the needs of the communities they serve. Her research examines the relationship between public participation, local governance, and access to essential services.</p>
<p>As director of Institute Title, she leads its research and educational programs, supports faculty collaboration, and builds partnerships with community organizations. Her work brings together researchers and practitioners to understand how public decisions are made and whose perspectives inform them.</p>
<p>Okafor combines comparative policy analysis with interviews and collaborative field research. She is particularly interested in how local knowledge can inform the design and evaluation of public programs.</p>
<h2>Research interests</h2><ul><li>Participatory governance and public accountability</li><li>Community-led research and policy evaluation</li><li>Access to public services</li></ul>
<h2>Current work</h2><p>Her current project examines how community organizations and local governments work together to identify priorities and evaluate public services. The project produces comparative case studies and practical resources for research partners.</p>
<h2>Teaching and mentoring</h2><p>Okafor teaches courses on governance, research methods, and public policy. She advises graduate students and mentors undergraduate researchers working with community partners.</p>
<h2>Education</h2><ul><li>Ph.D., Political Science</li><li>M.A., Public Policy</li><li>B.A., Political Science</li></ul>
<p><a href="../../faculty/index.html">Back to Faculty</a></p>'''
    page('full-bio','Maren Okafor',body,True,'Full institute-hosted biography example. Maren Okafor and this biography are fictional.')
    body=f'''<div class="card-container"><article class="card card--person card--horizontal"><figure class="avatar avatar--lg card-image"><img src="../assets/daniel-philpott.jpg" width="600" height="600" alt="Daniel Philpott"></figure><div class="card-body"><p class="person-title">Professor of Political Science</p><p>University of Notre Dame</p></div></article></div>
<h2>Institute affiliation</h2><p>Daniel Philpott is affiliated with the Kroc Institute for International Peace Studies. His research on reconciliation, religious freedom, and religion in global politics connects with the institute’s focus on peacebuilding.</p>
<p>His full biography, publications, and contact information are maintained by Notre Dame’s Department of Political Science.</p>
<p><a class="btn" href="{host}" aria-label="Read Daniel Philpott’s full biography on the Department of Political Science website">Read full biography</a></p>
<p><a href="../../faculty/index.html">Back to Faculty</a></p>'''
    page('abridged-bio','Daniel Philpott',body,True,f'Abridged institute biography example. Public profile information: <a href="{host}">Department of Political Science</a>.')
    body='''<p>Three NDT4 examples showing where a person’s directory entry leads.</p>
<ol><li><h2><a href="external-profile/">Directory entry linking directly offsite</a></h2><p>The external-link arrow appears automatically on the native People Card. Clicking the card opens the full profile on the Keough School website.</p></li>
<li><h2><a href="full-bio/">Full institute biography</a></h2><p>A locally maintained profile with biography, research, teaching, and education. This example uses a fictional person.</p></li>
<li><h2><a href="abridged-bio/">Abridged institute biography</a></h2><p>A short institute-focused biography with a button to the full profile maintained outside the Keough School website.</p></li></ol>'''
    html=ns['shell']('Profile page examples',body,prefix='../')
    (root/'index.html').write_text(html)
