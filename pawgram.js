/* ==========================================================
   PAWGRAM · Gen-Z Motion Engine v2
   GSAP + ScrollTrigger · Custom cursor · Loader · Nav
   ========================================================== */
(function(){
  'use strict';

  var doc = document.documentElement;
  var body = document.body;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var touch = matchMedia('(hover: none)').matches;
  var small = innerWidth < 760;

  /* ---------- helpers ---------- */
  function el(s){return document.querySelector(s);}
  function els(s){return document.querySelectorAll(s);}
  function clamp(v,min,max){return Math.min(max,Math.max(min,v));}

  /* ---------- reduced motion body class ---------- */
  if(reduce) body.classList.add('reduced-motion');
  matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',function(e){
    body.classList.toggle('reduced-motion', e.matches);
  });

  /* ---------- touch device detection ---------- */
  if(touch) body.classList.add('touch-device');

  /* ---------- GSAP via CDN (async self-loader fallback) ---------- */
  // GSAP is expected as <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  // plus ScrollTrigger. If missing, we define a tiny stub so the rest of the file won't crash.
  window._gsapReady = false;

  function loadGSAP(cb){
    if(window.gsap && window.ScrollTrigger){
      window._gsapReady = true;
      cb(); return;
    }
    var s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js';
    s.onload = function(){
      var st = document.createElement('script');
      st.src = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js';
      st.onload = function(){
        window._gsapReady = true;
        cb();
      };
      doc.head.appendChild(st);
    };
    doc.head.appendChild(s);
  }

  loadGSAP(init);

  /* ---------- init ---------- */
  function init(){
    var gsap = window.gsap;
    var ScrollTrigger = window.ScrollTrigger;
    if(!gsap) return;

    gsap.registerPlugin(ScrollTrigger);

    /* ---------- cursor ---------- */
    var cursor = el('#paw-cursor');
    var trail  = el('.cursor-trail');
    if(cursor && !touch && !reduce){
      var tx=0,ty=0,x=0,y=0,scale=1;
      var state = 'idle';
      var states = {};

      function setState(s){
        if(state===s) return;
        state=s;
        cursor.className = '';
        cursor.classList.add('visible');
        if(s==='read') cursor.classList.add('state-read');
        if(s==='play') cursor.classList.add('state-play');
        if(s==='drag') cursor.classList.add('state-drag');
        if(s==='heart') cursor.classList.add('state-heart');
      }
      function clearState(){state='idle';cursor.className='';cursor.classList.remove('visible');}

      document.addEventListener('mousemove',function(e){
        tx=e.clientX;ty=e.clientY;
        cursor.classList.add('visible');
      },{passive:true});
      document.addEventListener('mouseenter',function(){cursor.classList.add('visible');});
      document.addEventListener('mouseleave',function(){cursor.classList.remove('visible');});

      // state zones
      els('a.btn,.btn,button,.gitem,a.motif,.chapter-card').forEach(function(b){
        b.addEventListener('mouseenter',function(){setState('play');});
        b.addEventListener('mouseleave',function(){setState('idle');});
      });
      els('[data-heart]').forEach(function(b){
        b.addEventListener('mouseenter',function(){setState('heart');});
        b.addEventListener('mouseleave',function(){setState('idle');});
      });

      (function loop(){
        x += (tx-x)*0.14;
        y += (ty-y)*0.14;
        if(cursor.classList.contains('visible')){
          cursor.style.transform = 'translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px) translate(-50%,-50%)';
        }
        requestAnimationFrame(loop);
      })();
    }

    /* ---------- loader ---------- */
    var loader = el('#loader');
    if(loader){
      var lbar = el('#lbar');
      var lpct = el('#lpct');
      var lring = el('#lring');
      var msgs = el('.battery-msg');
      var p = 0;
      var msgIdx = 0;
      var messages = [
        'threading needle…','0010 0100','loading thread','sakura bloom','neon on',
        'coral thread →','midnight purple','almost…','99%','ready.'
      ];
      var tick = setInterval(function(){
        p = Math.min(p + (p<70 ? 9 : p<92 ? 4 : 1.4), 96);
        paint(p);
        if(msgs && Math.random()>.75){
          msgs.textContent = messages[msgIdx++ % messages.length];
        }
      },90);
      function paint(v){
        v=Math.round(v);
        if(lbar) lbar.style.width = v+'%';
        if(lpct) lpct.textContent = v+'%';
        if(lring) lring.style.strokeDashoffset = 502-(502*v/100);
      }
      function finish(){
        if(lbar){lbar.style.width='100%';}
        if(lpct){lpct.textContent='100%';}
        if(lring){lring.style.strokeDashoffset=0;}
        if(msgs){msgs.textContent='connect…';}
        gsap.to(loader,{opacity:0,visibility:'hidden',duration:.7,ease:varEase('ease'),delay:.4,
          onComplete:function(){
            loader.remove();
            body.style.overflow='';
          }});
      }
      document.body.style.overflow='hidden';
      if(document.readyState==='complete'){setTimeout(finish,1400);}
      else{addEventListener('load',function(){setTimeout(finish,1400);});}
      setTimeout(finish,4600);
    }

    /* ---------- nav hide/show on scroll ---------- */
    var nav = el('header.nav');
    if(nav){
      var lastY=0,ticking=false;
      function onScroll(){
        var y = doc.scrollTop || body.scrollTop;
        if(y>lastY && y>60){nav.classList.add('hidden');}
        else if(y<lastY || y<60){nav.classList.remove('hidden');}
        lastY = y>0?y:0;
        ticking=false;
      }
      addEventListener('scroll',function(){
        if(!ticking){requestAnimationFrame(onScroll);ticking=true;}
      },{passive:true});
    }

    /* ---------- thread SVG draw on scroll ---------- */
    var thread = el('.thread-svg path');
    if(thread && ScrollTrigger){
      var len = thread.getTotalLength();
      thread.style.strokeDasharray = len;
      thread.style.strokeDashoffset = len;
      ScrollTrigger.create({
        trigger: 'body',
        start: 'top top',
        end: 'bottom bottom',
        scrub: true,
        onUpdate: function(self){
          var offset = len * (1 - self.progress);
          thread.style.strokeDashoffset = offset;
        }
      });
    }

    /* ---------- reveal entries ---------- */
    if(ScrollTrigger){
      els('.rv,.reveal').forEach(function(el){
        gsap.from(el,{
          scrollTrigger:{trigger:el,start:'top 85%',toggleActions:'play none none reverse'},
          y:40,opacity:0,duration:.8,ease:'power3.out',
          clearProps:'all'
        });
      });
    }

    /* ---------- counters ---------- */
    els('[data-count]').forEach(function(c){
      var target = parseFloat(c.dataset.count);
      gsap.to(c,{textContent:target,duration:1.2,ease:'power2.out',scrollTrigger:{
        trigger:c,start:'top 80%',toggleActions:'play none none none'
      }});
    });

    /* ---------- hero entrance ---------- */
    var hero = el('.hero');
    if(hero && gsap){
      var tl = gsap.timeline({defaults:{ease:'power3.out'}});

      // per-letter bounce on title spans
      els('h1 span').forEach(function(s,i){
        tl.from(s,{y:40,opacity:0,scale:1.4,duration:.7,ease:'back.out(1.7)'},i*0.08);
      },0);

      tl.from('.kicker',{y:20,opacity:0,duration:.6},'-=0.5')
        .from('.badge',{y:20,opacity:0,duration:.6},'-=0.4')
        .from('.jp',{y:15,opacity:0,duration:.6},'-=0.4')
        .from('.logline',{y:25,opacity:0,duration:.7},'-=0.3')
        .from('.hero-cta .btn',{y:20,opacity:0,duration:.6,stagger:.15},'-=0.4')
        .from('.hero-stats',{y:20,opacity:0,duration:.7},'-=0.5')
        .from('.phonestage',{y:30,opacity:0,duration:.8,ease:'back.out(1.4)'},'-=0.6')
        .from('.scrollcue',{y:20,opacity:0,duration:.6},'-=0.4');

      // neon flicker on badge
      gsap.to('.badge',{
        duration:0.15,repeat:-1,yoyo:true,ease:'power1.inOut',
        opacity:function(){return 0.85+Math.random()*0.15;},
        textShadow:function(){return '0 0 '+(10+Math.random()*10)+'px var(--coral)';}
      });
    }

    /* ---------- chat typing in phone ---------- */
    var chatlog = el('#chatlog');
    if(chatlog && gsap){
      var lines = [
        'u up?',
        'saw this sakura and thought of you',
        'it was 2:47 AM',
        'you replied in 3 seconds',
        'i saved that message',
        'now we\u2019re here'
      ];
      var li = 0;
      function typeLine(){
        if(li>=lines.length) return;
        var text = lines[li++];
        var div = document.createElement('div');
        div.className='bub mine';
        div.textContent='';
        chatlog.appendChild(div);
        var k=0;
        (function step(){
          div.textContent = text.slice(0,k+1);
          k++;
          if(k<text.length){setTimeout(step,60+Math.random()*40);}
          else{
            chatlog.scrollTop = chatlog.scrollHeight;
            setTimeout(typeLine,700+Math.random()*800);
          }
        })();
      }
      setTimeout(typeLine,1200);
    }
  }

  function varEase(n){
    // fallback for CSS var inside GSAP string ease
    var map={'ease':'power3.out','bounce':'back.out(1.7)'};
    return map[n]||'power3.out';
  }

})();
