const mode=document.body.dataset.prototype;
const params=new URLSearchParams(location.search);
const groups={governance:'Leadership',faculty:'Faculty',staff:'Staff','scholars-fellows':'Scholars & Fellows',students:'Students'};
const children={governance:['Advisory'],faculty:['Faculty Fellows','Associated Faculty','Emeriti'],staff:[], 'scholars-fellows':['Postdoctoral Researchers','Affiliates','Past Scholars & Fellows'],students:['PhD']};
const defaults={governance:['Leadership'],faculty:['Core Affiliated Faculty'],staff:['Staff'],'scholars-fellows':['Visiting Scholars','Fellows'],students:['Graduate','Undergraduate']};
const requestedGroup=params.get('group');
const group=requestedGroup==='all'?'':(requestedGroup || (mode==='category'?'faculty':''));
const sub=params.get('sub')||'';
const e=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const app=document.querySelector('#directory-app');
const currentPath=location.pathname;
function url(g='',s=''){const q=new URLSearchParams();if(g)q.set('group',g);if(s)q.set('sub',s);return currentPath+(q.size?'?'+q:'');}
const screenshot=mode==='screenshot';
const small=mode==='small';
const data=screenshot?window.screenshotPeople:small?window.samplePeople:window.directoryPeople;
const scopeName=sub||groups[group]||'everyone';
const activeTitle=sub||groups[group]||(screenshot?'People Directory':'People');
document.querySelector('.page-title').textContent=activeTitle;
document.title=activeTitle+' | People hub comparison';
const sidebar=document.querySelector('.page-sidebar');
sidebar.innerHTML='<nav id="nav" class="nav-site nav-section" aria-label="People categories"><ul>'+Object.entries(groups).map(([g,label])=>`<li class="${g===group?'active':''}"><a href="${url(g)}" ${g===group&&!sub?'aria-current="page"':''}>${e(label)}</a>${g===group&&children[g].length?'<ul>'+children[g].map(s=>`<li><a href="${url(g,s)}" ${sub===s?'aria-current="page"':''}>${e(s)}</a></li>`).join('')+'</ul>':''}</li>`).join('')+'</ul></nav>';
sidebar.insertAdjacentHTML('beforeend',sidebar.firstElementChild.outerHTML.replace('id="nav"','id="nav-mobile"').replace('nav-section','nav-full'));
document.querySelector('.nav-menu').href='#nav-mobile';
let q=params.get('q')||'',discipline=params.get('discipline')||'',region=params.get('region')||'',status=params.get('status')||(['Emeriti','Past Scholars & Fellows'].includes(sub)?'past':'current'),page=Math.max(1,Number(params.get('page'))||1);
let searched=!!q||params.has('search');
const pageSize=24;
const scoped=()=>data.filter(p=>!group||(p.group===group&&(sub?p.role===sub:defaults[group].includes(p.role))));
const options=(key,value)=>[...new Set(scoped().map(p=>p[key]))].sort().map(v=>`<option ${value===v?'selected':''}>${e(v)}</option>`).join('');
const gateway=mode==='gateway'&&!group&&!searched;
const featured=mode==='featured'&&!group&&!searched;
const controls=screenshot?scoped().length>40:!small;
app.innerHTML=`${group?`<p><a href="${url()+(mode==='category'?'?group=all':'')}">Search all people</a></p>`:''}
${screenshot?'':gateway?'<h2>Find someone</h2><p>Search by name or research interest, or choose a group below.</p>':featured?'<h2>Find someone</h2>':'<h2>Directory</h2>'}
${controls?`<form class="directory-controls" id="search-form"><label>Search ${group?e(scopeName):'all people'}<input name="q" type="search" value="${e(q)}" placeholder="Name or research interest"></label><button type="submit">Search</button></form>
<div class="directory-controls" ${gateway||featured?'hidden':''} id="filters"><label>Discipline<select id="discipline"><option value="">All disciplines</option>${options('discipline',discipline)}</select></label><label>Region of expertise<select id="region"><option value="">All regions</option>${options('region',region)}</select></label><label>Affiliation<select id="status"><option value="current" ${status==='current'?'selected':''}>Current</option><option value="past" ${status==='past'?'selected':''}>Past</option><option value="all" ${status==='all'?'selected':''}>Current and past</option></select></label><button id="reset" type="button">Clear search and filters</button></div>`:''}
${gateway?'<ul class="category-links">'+Object.entries(groups).map(([g,label])=>`<li><a href="${url(g)}"><strong>${label}</strong><br>${e({governance:'Institute leadership and advisory council',faculty:'Core affiliates and faculty groups',staff:'The team supporting the institute','scholars-fellows':'Visiting scholars, fellows, and postdocs',students:'Undergraduate, graduate, and PhD groups'}[g])}</a></li>`).join('')+'</ul>':''}
${featured?'<h2>Featured community members</h2><p>A curated selection across institute roles. This is not the complete directory.</p><p><a href="?search=1">Browse the full directory</a></p>':''}
<p id="result-count" role="status" aria-live="polite"></p>${screenshot?'<nav class="pagination" aria-label="Directory pages above results" id="pagination-top"></nav>':''}<ul id="results" class="grid grid-sm-2 grid-md-4"></ul><nav class="pagination" aria-label="Directory pages" id="pagination"></nav>
<dialog class="prototype-dialog" aria-labelledby="profile-name"><button id="close-profile" autofocus>Close profile</button><h2 id="profile-name"></h2><div id="profile-detail"></div></dialog>`;
function save(){const s=new URLSearchParams(location.search);for(const [k,v] of Object.entries({q,discipline,region,status,page:String(page)})){if(v)s.set(k,v);else s.delete(k);}if(searched)s.set('search','1');history.replaceState(null,'',currentPath+'?'+s);}
function render(){
 let list=scoped().filter(p=>(small||status==='all'||p.status===status)&&(!discipline||p.discipline===discipline)&&(!region||p.region===region)&&(!q||[p.name,p.role,p.discipline,p.region,p.interest].join(' ').toLowerCase().includes(q.toLowerCase())));
 if(screenshot&&!group)list.sort((a,b)=>(a.role==='Leadership'?0:1)-(b.role==='Leadership'?0:1)||a.name.split(' ').at(-1).localeCompare(b.name.split(' ').at(-1))||a.name.localeCompare(b.name));
 if(gateway)return;
 if(featured)list=window.featuredIds.map(id=>data.find(p=>p.id===id)).filter(Boolean);
 const pages=Math.max(1,Math.ceil(list.length/pageSize));page=Math.min(page,pages);
 const visible=small||featured?list:list.slice((page-1)*pageSize,page*pageSize);
 document.querySelector('#result-count').textContent=featured?'':list.length?`${small?'Showing all '+list.length:`Showing ${(page-1)*pageSize+1}–${Math.min(page*pageSize,list.length)} of ${list.length}`} profiles${!small?' · '+(status==='all'?'Current and past':status==='past'?'Past affiliates':'Current affiliates'):''}${screenshot&&!group?' · Leadership first, then surname A–Z':' · Last name A–Z'}`:'No matching profiles. Try a different search or clear the filters.';
 document.querySelector('#results').innerHTML=visible.map(p=>`<li class="card card-person"><figure class="card-image"><img class="image-circle" src="../../assets/avatar-placeholder.svg" width="600" height="600" alt="" loading="lazy"></figure><div class="card-body"><h3 class="card-title"><button class="profile-link" data-profile="${p.id}">${e(p.name)}</button></h3><p>${e(p.role)}</p><p>${e(p.discipline)} · ${e(p.region)}</p></div></li>`).join('');
 document.querySelector('#pagination').innerHTML=small||featured||!list.length||(screenshot&&list.length<=24)?'':`<button data-page="${page-1}" ${page===1?'disabled':''}>Previous</button><span>Page ${page} of ${pages}</span><button data-page="${page+1}" ${page===pages?'disabled':''}>Next</button>`;
 if(screenshot)document.querySelector('#pagination-top').innerHTML=document.querySelector('#pagination').innerHTML;
}
app.addEventListener('submit',ev=>{ev.preventDefault();q=new FormData(ev.target).get('q').trim();page=1;searched=true;save();if(gateway||featured)location.reload();else render();});
for(const key of ['discipline','region','status'])document.getElementById(key)?.addEventListener('change',ev=>{if(key==='discipline')discipline=ev.target.value;if(key==='region')region=ev.target.value;if(key==='status')status=ev.target.value;page=1;save();render();});
document.querySelector('#reset')?.addEventListener('click',()=>{q='';discipline='';region='';status='current';page=1;searched=true;save();location.reload();});
app.addEventListener('click',ev=>{const b=ev.target.closest('[data-page]');if(b){page=Number(b.dataset.page);save();render();document.querySelector('#result-count').scrollIntoView({block:'center'});}const a=ev.target.closest('[data-profile]');if(a){const p=data.find(p=>p.id===a.dataset.profile);document.querySelector('#profile-name').textContent=p.name;document.querySelector('#profile-detail').innerHTML=`<p>${e(p.role)} · ${e(groups[p.group])}</p><p>${e(p.discipline)} · ${e(p.region)}</p><p>Research interest: ${e(p.interest)}</p><p>${p.status==='past'?'Past affiliate':'Current affiliate'}</p><p>Fictional profile for usability testing.</p>`;document.querySelector('dialog').showModal();}});
document.querySelector('#close-profile').onclick=()=>document.querySelector('dialog').close();
render();
