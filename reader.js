/* ==========================================================
   PAWGRAM · Reader enhancements
   Sticky coral progress · reactions bar · tap-to-hide UI
   ========================================================== */
(function(){
  'use strict';

  var body=document.body, doc=document.documentElement;

  /* ---------- reduced motion ---------- */
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){
    body.classList.add('reduced-motion');
  }

  /* ---------- reactions bar ---------- */
  var reactions = document.createElement('div');
  reactions.className='reader-reactions';
  reactions.innerHTML =
    '<button class="reaction" data-heart title="Save thread">💾</button>'+
    '<button class="reaction" title="Coral hug">🌸</button>'+
    '<button class="reaction" title="Midnight paw">🐾</button>'+
    '<button class="reaction" title="Sakura sigh">🌙</button>';
  body.appendChild(reactions);

  reactions.querySelectorAll('.reaction').forEach(function(btn){
    btn.addEventListener('click',function(){
      reactions.querySelectorAll('.reaction').forEach(function(b){b.classList.remove('active');});
      btn.classList.add('active');
      var key='pg-reaction-'+location.pathname.split('/').pop();
      try{localStorage.setItem(key,btn.title);}catch(e){}
    });
    // restore saved reaction
    var key='pg-reaction-'+location.pathname.split('/').pop();
    try{
      var saved=localStorage.getItem(key);
      if(saved){
        reactions.querySelectorAll('.reaction').forEach(function(b){
          if(b.title===saved)b.classList.add('active');
        });
      }catch(e){}
  });

  /* ---------- reader nav (prev/next) ---------- */
  var nav = document.createElement('div');
  nav.className='reader-nav';
  var links = body.querySelectorAll('.tbtn, .btn[href]');
  var next = null, prev = null;
  links.forEach(function(a){
    var h = a.getAttribute('href')||'';
    if(h.match(/Chapter_\d+_Reader/)){
      if(h>location.pathname.split('/').pop()){next=a;}
      else if(h<location.pathname.split('/').pop()){prev=a;}
    }
  });
  var html = '';
  if(prev){html+='<a class="btn" href="'+prev.getAttribute('href')+'">← '+prev.textContent.trim()+'</a>';}
  if(next){html+='<a class="btn" href="'+next.getAttribute('href')+'">'+next.textContent.trim()+' →</a>';}
  if(html){nav.innerHTML=html;body.appendChild(nav);}

  /* ---------- tap to hide topbar ---------- */
  var topbar = document.querySelector('.topbar');
  var hideTimer;
  function showUI(){if(topbar)topbar.classList.remove('hide');reactions.classList.add('show');}
  function hideUI(){if(topbar)topbar.classList.add('hide');reactions.classList.remove('show');}
  body.addEventListener('click',function(){
    showUI();
    clearTimeout(hideTimer);
    hideTimer=setTimeout(hideUI,3500);
  });
  body.addEventListener('scroll',showUI,{passive:true});
  showUI();

  /* ---------- panel entrance ---------- */
  if(window.gsap){
    window.gsap.utils.toArray('figure.pg').forEach(function(fig){
      window.gsap.from(fig,{y:30,opacity:0,duration:.6,scrollTrigger:{
        trigger:fig,start:'top 85%',toggleActions:'play none none none'
      }});
    });
  }

  /* ---------- scroll progress (enhance existing #rp) ---------- */
  var rp=document.getElementById('rp');
  if(rp){
    rp.style.background='linear-gradient(90deg,var(--coral,#ffb25e))';
    rp.style.height='3px';
  }
})();
