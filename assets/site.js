(()=>{
 const nav=document.querySelector('.nav');
 const onS=()=>nav.classList.toggle('scrolled',scrollY>8);onS();addEventListener('scroll',onS,{passive:true});
 const els=document.querySelectorAll('.rv');
 if('IntersectionObserver' in window){
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -8% 0px'});
  els.forEach(el=>io.observe(el));
 }else els.forEach(el=>el.classList.add('in'));
 const rm=matchMedia('(prefers-reduced-motion: reduce)');
 const hv=document.querySelector('.hero video');
 const vb=document.querySelector('.vbtn');
 const setB=p=>{if(!vb)return;vb.classList.toggle('paused',p);vb.setAttribute('aria-label',p?vb.dataset.play:vb.dataset.pause)};
 if(hv&&rm.matches){hv.removeAttribute('autoplay');hv.pause();setB(true);}
 if(vb&&hv)vb.addEventListener('click',()=>{if(hv.paused){hv.play();setB(false)}else{hv.pause();setB(true)}});
})();
