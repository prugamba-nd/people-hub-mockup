const records=window.screenshotPeople;
const query=new URLSearchParams(location.search);
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const app=document.querySelector('#directory-app');
let term=query.get('q')||'',discipline=query.get('discipline')||'',region=query.get('region')||'',page=Math.max(1,Number(query.get('page'))||1);
const options=(field,selected)=>[...new Set(records.map(p=>p[field]))].sort().map(v=>`<option value="${escapeHTML(v)}" ${v===selected?'selected':''}>${escapeHTML(v)}</option>`).join('');
app.innerHTML=`${records.length>40?`<form id="directory-search"><div class="form-field"><label for="search-name">Search the directory</label><input class="field" type="search" id="search-name" name="q" value="${escapeHTML(term)}" placeholder="Name or research interest"></div><div class="grid grid-md-2"><div class="form-field"><label for="discipline">Discipline</label><select class="field" id="discipline"><option value="">All disciplines</option>${options('discipline',discipline)}</select></div><div class="form-field"><label for="region">Region of expertise</label><select class="field" id="region"><option value="">All regions</option>${options('region',region)}</select></div></div><p><button class="btn" type="submit">Search</button> <button class="btn btn--secondary" type="button" id="clear-filters">Clear search and filters</button></p></form>`:''}<p id="result-message" role="status" aria-live="polite" hidden></p><ul id="results" class="grid grid-md-2 grid-lg-4"></ul><div class="pagination" role="navigation" aria-label="Pagination" id="pagination"></div><dialog class="dialog" id="profile-dialog" aria-labelledby="profile-heading"><div class="dialog-header"><h2 class="dialog-heading" id="profile-heading"></h2><form method="dialog" class="dialog-close"><button type="submit" aria-label="Close profile">×</button></form></div><div class="dialog-content" id="profile-content"></div></dialog>`;
function url(n){const p=new URLSearchParams();if(term)p.set('q',term);if(discipline)p.set('discipline',discipline);if(region)p.set('region',region);p.set('page',n);return location.pathname+'?'+p;}
function render(){
 const matches=records.filter(p=>(!term||[p.name,p.role,p.interest,p.discipline,p.region].join(' ').toLowerCase().includes(term.toLowerCase()))&&(!discipline||p.discipline===discipline)&&(!region||p.region===region)).sort((a,b)=>(a.role==='Leadership'?0:1)-(b.role==='Leadership'?0:1)||a.name.split(' ').at(-1).localeCompare(b.name.split(' ').at(-1))||a.name.localeCompare(b.name));
 const pages=Math.ceil(matches.length/24);page=Math.min(page,Math.max(1,pages));
 document.querySelector('#result-message').hidden=Boolean(matches.length);
 document.querySelector('#result-message').textContent=matches.length?'':'No matching profiles. Try another search or clear the filters.';
 document.querySelector('#results').innerHTML=matches.slice((page-1)*24,page*24).map(p=>`<li class="card-container"><article class="card card--person"><figure class="avatar avatar--lg card-image"><img src="../../assets/avatar-placeholder.svg" width="600" height="600" loading="lazy" alt=""></figure><div class="card-body"><h2 class="card-title"><a class="card-link" href="#profile-dialog" data-profile="${p.id}">${escapeHTML(p.name)}</a></h2><p class="person-title">${escapeHTML(p.role)}</p></div></article></li>`).join('');
 const link=(n,label,attrs)=>`<a href="${escapeHTML(url(n))}" ${attrs}>${label}</a>`;
 document.querySelector('#pagination').hidden=pages<=1;
 document.querySelector('#pagination').innerHTML=pages<=1?'':[
 page>1?link(page-1,'Previous','class="previous_page" aria-label="Previous page" rel="prev"'):'<span class="previous_page disabled" aria-label="Previous page">Previous</span>',
 ...Array.from({length:pages},(_,i)=>i+1).map(n=>n===page?`<span class="current" aria-current="page">${n}</span>`:link(n,n,`aria-label="Page ${n}"`)),
 page<pages?link(page+1,'Next','class="next_page" aria-label="Next page" rel="next"'):'<span class="next_page disabled" aria-label="Next page">Next</span>'
 ].join(' ');
}
function update(){page=1;history.replaceState(null,'',url(page));render();}
document.querySelector('#directory-search')?.addEventListener('submit',ev=>{ev.preventDefault();term=document.querySelector('#search-name').value.trim();update();});
document.querySelector('#discipline')?.addEventListener('change',ev=>{discipline=ev.target.value;update();});
document.querySelector('#region')?.addEventListener('change',ev=>{region=ev.target.value;update();});
document.querySelector('#clear-filters')?.addEventListener('click',()=>{term=discipline=region='';document.querySelector('#directory-search').reset();document.querySelector('#search-name').value='';document.querySelector('#discipline').value='';document.querySelector('#region').value='';update();});
app.addEventListener('click',ev=>{const a=ev.target.closest('[data-profile]');if(!a)return;ev.preventDefault();const person=records.find(p=>p.id===a.dataset.profile);document.querySelector('#profile-heading').textContent=person.name;document.querySelector('#profile-content').innerHTML=`<p>${escapeHTML(person.role)}</p><p>${escapeHTML(person.discipline)} · ${escapeHTML(person.region)}</p><p>${escapeHTML(person.interest)}</p><p>Fictional profile for illustration.</p>`;document.querySelector('#profile-dialog').showModal();});
render();
