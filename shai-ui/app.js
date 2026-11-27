(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
const small=matchMedia('(max-width:900px)').matches;
const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
const hasGsap=!!window.gsap&&!!window.ScrollTrigger;
if(hasGsap)gsap.registerPlugin(ScrollTrigger);
window.__cupP=0;

/* ---------- data ---------- */
const MENU=[
 {k:'Чёрные',v:0,items:[
  ['Дянь Хун «Золотые почки»','Юньнань','Мёд, сухофрукты и тёплая карамель в послевкусии.',3200],
  ['Лапсанг Сушонг','Фуцзянь','Дымный, с сосновой смолой. Для тех, кто любит характер.',3400],
  ['Ассам Мангалам','Индия','Солодовый и крепкий, отлично держит молоко.',2400],
  ['Кимун','Аньхой','Какао, орех и тонкая дымка. Мягкий, как шёлк.',3800]]},
 {k:'Зелёные',v:1,items:[
  ['Сенча «Утро»','Япония','Свежая трава, морской бриз, лёгкая сладость.',2800],
  ['Лун Цзин «Колодец дракона»','Чжэцзян','Жареный каштан и чистая свежесть.',4800],
  ['Билочунь','Цзянсу','Цветы и персиковая кожура. Нежный, почти сладкий.',4200],
  ['Генмайча','Япония','Зелёный чай с жареным рисом, тёплый и ореховый.',2600]]},
 {k:'Улуны',v:2,items:[
  ['Те Гуань Инь','Фуцзянь','Орхидея и сливки. Раскрывается до семи проливов.',3600],
  ['Да Хун Пао','Уишань','Минералы, жар углей и кора корицы.',5200],
  ['Молочный улун','Тайвань','Сливочный аромат без капли молока.',3800],
  ['Габа','Тайвань','Спелая слива и мёд. Успокаивает лучше любого слова.',5800]]},
 {k:'Пуэры и белые',v:3,items:[
  ['Шу пуэр 5 лет','Юньнань','Земля, какао, плотное тело. Согревает до вечера.',3200],
  ['Шэн пуэр 2019','Бунян','Горчинка, цветы и мёд. Чай с историей.',4600],
  ['Лао Ча Тоу','Юньнань','Старые почки: тёмный, сладкий, с нотой сухофруктов.',3900],
  ['Шоу Мэй','Фудин','Белый чай: сено, абрикос и тихая сладость.',4000]]},
 {k:'Травы · Қазақша',v:4,items:[
  ['Сүт шай','Қазақша','Крепкий чай, молоко и сливочное масло, как у бабушки. С баурсаками +900 ₸.',1600],
  ['Иван-чай с чабрецом','Алтай','Луговые травы, мёд на дне, без кофеина.',2200],
  ['Облепиха и имбирь','Наш сбор','Горячий, острый и яркий. Лучшее от простуды.',2600],
  ['Фруктовый чайник 800 мл','Наш сбор','Ягоды, цитрус и яблоко над свечой.',4800]]}
];
const PICK={
 focus:[['Сенча «Утро»','Японская свежесть собирает мысли в одну точку.',2800],['Те Гуань Инь','Ясная орхидея: бодрит мягко, без суеты.',3600],['Да Хун Пао','Жар углей и минералы. Чай для серьёзного дела.',5200]],
 calm:[['Шоу Мэй','Белый чай как тихий вечер: сено, абрикос, пауза.',4000],['Молочный улун','Сливочный и спокойный. Плечи опускаются сами.',3800],['Габа','Спелая слива и мёд. Успокаивает лучше любого слова.',5800]],
 warm:[['Иван-чай с чабрецом','Луговые травы и мёд. Согревает и не взбадривает.',2200],['Дянь Хун «Золотые почки»','Карамель и сухофрукты. Тепло изнутри.',3200],['Шу пуэр 5 лет','Земля и какао. Выдерживает зимний вечер.',3200]],
 talk:[['Жасминовая жемчужина','Раскрывается в стекле, а разговор раскрывается вместе с ней.',2900],['Сүт шай','Казахский чай с молоком и маслом. Лучший повод задержаться.',1600],['Лапсанг Сушонг','Дымный, с характером. Будет о чём поговорить.',3400]]
};
const fmt=n=>n.toLocaleString('ru-RU').replace(/ /g,' ')+' ₸';
const WA='77000000000';

/* ---------- smooth scroll ---------- */
let lenis=null;
if(window.Lenis&&!reduce){
 lenis=new Lenis({duration:1.15,easing:t=>Math.min(1,1.001-Math.pow(2,-10*t))});
 if(hasGsap){lenis.on('scroll',ScrollTrigger.update);gsap.ticker.add(t=>lenis.raf(t*1000));gsap.ticker.lagSmoothing(0)}
 else{const f=t=>{lenis.raf(t);requestAnimationFrame(f)};requestAnimationFrame(f)}
}
const goTo=(h)=>{const el=$(h);if(!el)return;lenis?lenis.scrollTo(el,{offset:0,duration:1.6}):el.scrollIntoView({behavior:'smooth'})};
$$('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{const h=a.getAttribute('href');if(h.length>1&&$(h)){e.preventDefault();closeSheet();goTo(h)}}));

/* ---------- split words ---------- */
function split(el){const txt=el.textContent.trim();el.setAttribute('aria-label',txt);el.innerHTML=txt.split(/\s+/).map(w=>`<span class="w" aria-hidden="true"><span>${w}</span></span>`).join(' ');return $$('.w>span',el)}
const heroW=split($('.hero-h'));
const otherSplits=$$('.h2.split').map(split);

/* ---------- hero video ---------- */
const hv=$('#heroV');const startHero=()=>{hv.src=small?'assets/hero-m.mp4':'assets/hero.mp4';hv.play().catch(()=>{})};document.readyState==='complete'?startHero():addEventListener('load',startHero,{once:true});

/* ---------- menu ---------- */
const tabs=$('#tabs'),list=$('#list'),pvs=$$('#pv video'),cap=$('#pvCap');
function loadVid(v){if(!v.src&&v.dataset.src){v.src=v.dataset.src+(small?'-m':'')+'.mp4';v.poster=v.dataset.poster}}
function showCat(i){
 $$('.tab',tabs).forEach((t,j)=>t.setAttribute('aria-selected',j===i));
 const c=MENU[i];cap.textContent=c.k;
 pvs.forEach((v,j)=>{if(j===c.v){loadVid(v);v.classList.add('on');v.play().catch(()=>{})}else{v.classList.remove('on');setTimeout(()=>{if(!v.classList.contains('on'))v.pause()},800)}});
 list.innerHTML=c.items.map(it=>`<div class="it"><h3>${it[0]}</h3><span class="pr">${fmt(it[3])}</span><p><span class="o">${it[1]}</span>${it[2]}</p></div>`).join('');
 if(hasGsap&&!reduce)gsap.from($$('.it',list),{y:30,opacity:0,duration:.8,stagger:.07,ease:'power3.out',clearProps:'all'});
 else{}
}
MENU.forEach((c,i)=>{const b=document.createElement('button');b.className='tab';b.role='tab';b.textContent=c.k;b.addEventListener('click',()=>showCat(i));b.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){const n=(i+(e.key==='ArrowRight'?1:MENU.length-1))%MENU.length;showCat(n);$$('.tab',tabs)[n].focus()}});tabs.appendChild(b)});
showCat(0);

/* ---------- lazy videos (cards, mist) ---------- */
const io=new IntersectionObserver(es=>es.forEach(e=>{const v=e.target;if(e.isIntersecting){loadVid(v);v.play().catch(()=>{})}else v.pause()}),{rootMargin:'200px'});
$$('.card video').forEach(v=>io.observe(v));
const mv=$('#mistV');mv.dataset.src='assets/mist';mv.dataset.poster='assets/mist-poster.webp';io.observe(mv);
const hio=new IntersectionObserver(es=>es.forEach(e=>e.isIntersecting?hv.play().catch(()=>{}):hv.pause()));hio.observe(hv);

/* ---------- quiz ---------- */
const st={mood:null,power:null};
function showRes(){
 const r=$('#res');if(st.mood==null||st.power==null)return;
 const t=PICK[st.mood][st.power],msg=encodeURIComponent(`Здравствуйте! Хочу заказать к столу в «Алтын шай»: ${t[0]}.`);
 r.innerHTML=`<div class="in"><span class="o">Ваш чай на сегодня</span><h3>${t[0]}</h3><p>${t[1]}</p><div class="rf"><b>${fmt(t[2])}</b><a class="btn btn-sm" href="https://wa.me/${WA}?text=${msg}" target="_blank" rel="noopener">Заказать к столу</a></div></div>`;
}
$$('.chips').forEach(g=>g.addEventListener('click',e=>{const b=e.target.closest('.chip');if(!b)return;$$('.chip',g).forEach(c=>c.classList.toggle('on',c===b));st[g.dataset.q]=b.dataset.v;showRes()}));

/* ---------- booking ---------- */
const form=$('#form'),gn=$('#gn');let guests=2;
$('#gm').onclick=()=>{guests=Math.max(1,guests-1);gn.textContent=guests};$('#gp').onclick=()=>{guests=Math.min(12,guests+1);gn.textContent=guests};
const d=new Date(),iso=x=>x.toISOString().slice(0,10);form.date.min=iso(d);d.setDate(d.getDate()+1);form.date.value=iso(d);
$$('[data-set]').forEach(a=>a.addEventListener('click',()=>{$('#setSel').value=a.dataset.set}));
form.addEventListener('submit',e=>{e.preventDefault();let ok=true;
 [form.name,form.phone].forEach(i=>{const bad=i.value.trim().length<(i===form.phone?6:2);i.classList.toggle('err',bad);if(bad)ok=false});
 if(!ok){$('#formN').textContent='Заполните имя и телефон, и мы всё подтвердим.';return}
 const m=`Здравствуйте! Хочу забронировать стол в «Алтын шай».\nДата: ${form.date.value}, ${form.time.value}\nГостей: ${guests}\nСет: ${form.set.value}\nИмя: ${form.name.value.trim()}, тел.: ${form.phone.value.trim()}`;
 $('#formN').textContent='Открываем WhatsApp. Если окно не открылось, нажмите кнопку ещё раз.';
 window.open(`https://wa.me/${WA}?text=${encodeURIComponent(m)}`,'_blank','noopener')});

/* ---------- nav / sheet ---------- */
const nav=$('#nav'),burger=$('#burger'),sheet=$('#sheet');
function closeSheet(){sheet.classList.remove('open');burger.setAttribute('aria-expanded','false');lenis&&lenis.start()}
burger.addEventListener('click',()=>{const o=!sheet.classList.contains('open');sheet.classList.toggle('open',o);burger.setAttribute('aria-expanded',o);o?lenis&&lenis.stop():lenis&&lenis.start()});
let ly=0;addEventListener('scroll',()=>{const y=scrollY;nav.classList.toggle('solid',y>40);nav.classList.toggle('hide',y>ly&&y>500&&!sheet.classList.contains('open'));ly=y},{passive:true});

/* ---------- cursor + magnetic ---------- */
if(fine&&!reduce&&hasGsap){
 const cur=$('.cur'),xT=gsap.quickTo(cur,'x',{duration:.35,ease:'power3'}),yT=gsap.quickTo(cur,'y',{duration:.35,ease:'power3'});
 addEventListener('pointermove',e=>{xT(e.clientX);yT(e.clientY)});
 document.addEventListener('pointerover',e=>cur.classList.toggle('big',!!e.target.closest('a,button,.chip,.card')));
 $$('.mag').forEach(b=>{const bx=gsap.quickTo(b,'x',{duration:.5,ease:'power3'}),by=gsap.quickTo(b,'y',{duration:.5,ease:'power3'});
  b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();bx((e.clientX-r.left-r.width/2)*.25);by((e.clientY-r.top-r.height/2)*.35)});
  b.addEventListener('pointerleave',()=>{bx(0);by(0)})});
}

/* ---------- scroll choreography ---------- */
function setup(){
 if(!hasGsap||reduce){document.body.classList.remove('is-loading');return}
 otherSplits.forEach(sp=>gsap.from(sp,{yPercent:110,duration:1.2,stagger:.07,ease:'power4.out',scrollTrigger:{trigger:sp[0].closest('h2'),start:'top 85%'}}));
 $$('.eyebrow').forEach(e=>gsap.from(e,{opacity:0,y:14,duration:.9,ease:'power3.out',scrollTrigger:{trigger:e,start:'top 92%'}}));
 // hero parallax
 gsap.to('.hero-v',{yPercent:12,scale:1.14,ease:'none',scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:true}});
 gsap.to('.hero-in',{yPercent:-8,opacity:.2,ease:'none',scrollTrigger:{trigger:'.hero',start:'center top',end:'bottom top',scrub:true}});
 // cup progress
 const steps=$$('.step'),railF=$('#railF'),no=$('#stepNo');let cur=-1;
 ScrollTrigger.create({trigger:'.cup',start:'top top',end:'bottom bottom',scrub:true,onUpdate:s=>{
  const p=s.progress;window.__cupP=p;railF.style.width=(p*100)+'%';
  const i=Math.min(3,Math.floor(p*4));if(i!==cur){cur=i;steps.forEach((x,j)=>x.classList.toggle('on',j===i));no.textContent='0'+(i+1)+' / 04'}}});
 gsap.from('.cup-bg',{xPercent:20,opacity:0,duration:1.6,ease:'power3.out',scrollTrigger:{trigger:'.cup',start:'top 60%'}});
 // mist text + parallax
 const mt=$('#mistT'),t=mt.textContent.trim();mt.innerHTML='<span class="sr-only">'+t+'</span>'+t.split(/(\s+)/).map(w=>/^\s+$/.test(w)?' ':`<span aria-hidden="true">${[...w].map(c=>`<i class="ch" style="font-style:normal">${c}</i>`).join('')}</span>`).join('');
 const chs=$$('.ch',mt);
 ScrollTrigger.create({trigger:'.mist',start:'top 60%',end:'center 40%',scrub:true,onUpdate:s=>{const n=Math.round(s.progress*chs.length);chs.forEach((c,i)=>c.classList.toggle('on',i<n))}});
 gsap.fromTo('.mist-v',{yPercent:-7},{yPercent:7,ease:'none',scrollTrigger:{trigger:'.mist',start:'top bottom',end:'bottom top',scrub:true}});
 // horizontal sets (desktop only)
 ScrollTrigger.matchMedia({'(min-width:901px)':()=>{
  const tr=$('#track'),dist=()=>tr.scrollWidth-innerWidth+parseFloat(getComputedStyle(tr).paddingRight||0);
  gsap.to(tr,{x:()=>-dist(),ease:'none',scrollTrigger:{trigger:'.sets-pin',start:'top 8%',end:()=>'+='+dist(),pin:true,scrub:.6,invalidateOnRefresh:true,anticipatePin:1}});
 }});
 gsap.from('.res-hint',{opacity:0,duration:1,scrollTrigger:{trigger:'.pick',start:'top 70%'}});
 gsap.from('.form > *',{y:30,opacity:0,duration:.9,stagger:.08,ease:'power3.out',scrollTrigger:{trigger:'.form',start:'top 85%'}});
 gsap.from('.info li',{x:-30,opacity:0,duration:.9,stagger:.1,ease:'power3.out',scrollTrigger:{trigger:'.info',start:'top 88%'}});
 gsap.from('.foot-big',{yPercent:40,opacity:0,duration:1.4,ease:'power3.out',scrollTrigger:{trigger:'.foot',start:'top 85%'}});
}

/* ---------- preloader ---------- */
const pre=$('.pre'),pn=$('#preN'),pb=$('#preBar');let shown=false;
function intro(){
 if(shown)return;shown=true;
 const done=()=>{pre.remove();document.body.classList.remove('is-loading');setup();window.ScrollTrigger&&ScrollTrigger.refresh()};
 if(!hasGsap||reduce){done();return}
 gsap.set(heroW,{yPercent:115});gsap.set(['.hero .eyebrow','.hero-p','.hero-cta','.hero-foot','.nav'],{opacity:0,y:20});
 gsap.timeline({defaults:{ease:'power4.inOut'}})
  .to('.pre-in',{y:-30,opacity:0,duration:.6,ease:'power2.in'})
  .to(pre,{yPercent:-100,duration:1,onComplete:()=>{pre.remove();document.body.classList.remove('is-loading');setup()}},'-=.1')
  .to(heroW,{yPercent:0,duration:1.3,stagger:.1,ease:'power4.out'},'-=.55')
  .to(['.hero .eyebrow','.hero-p','.hero-cta','.hero-foot','.nav'],{opacity:1,y:0,duration:1,stagger:.08,ease:'power3.out'},'-=.9');
}
let pv=0;const target=()=>{let t=40;if(document.fonts&&document.fonts.status==='loaded')t+=20;if(hv.readyState>=3)t+=40;return t};
const tick=setInterval(()=>{const t=target();pv+=Math.max(1,(t-pv)*.12);if(pv>=99.5||(t>=100&&pv>=98)){pv=100}
 pn.textContent=Math.round(pv);pb.style.width=pv+'%';if(pv>=100){clearInterval(tick);setTimeout(intro,250)}},40);
setTimeout(()=>{pv=100;intro()},4500);
})();
