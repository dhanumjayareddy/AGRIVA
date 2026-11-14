/* AGRIVA motion layer: scroll progress, hero depth, word reveal, card tilt, parallax, magnetic buttons. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (reduce) return;
  document.documentElement.classList.add('fx');

  document.addEventListener('DOMContentLoaded', () => {
    /* Scroll progress line in the header */
    const hdr = $('.site-header');
    const bar = document.createElement('div'); bar.className = 'progress'; hdr.append(bar);

    /* Headline: word-by-word rise */
    const h1 = $('.hero h1'); let wi = 0;
    if (h1) {
      const wrap = node => {
        [...node.childNodes].forEach(n => {
          if (n.nodeType === 3) {
            const frag = document.createDocumentFragment();
            n.textContent.split(/(\s+)/).forEach(t => {
              if (!t.trim()) { frag.append(t); return; }
              const o = document.createElement('span'); o.className = 'w'; o.textContent = t; o.style.setProperty('--i', wi++); frag.append(o);
            });
            n.replaceWith(frag);
          } else if (n.nodeType === 1) wrap(n);
        });
      };
      wrap(h1); h1.classList.add('wsplit');
    }

    /* Scroll loop: progress, parallax, ticker speed */
    const par = $$('[data-parallax]'), track = $('.ticker-track');
    let lastY = scrollY, vel = 0, ticking = false, decaying = false;
    const frame = () => {
      ticking = false;
      const max = document.documentElement.scrollHeight - innerHeight;
      bar.style.transform = `scaleX(${max > 0 ? scrollY / max : 0})`;
      if (fine) {
        par.forEach(el => {
          if (!el.parentElement) return;
          const host = el.parentElement.getBoundingClientRect();
          if (host.bottom < -100 || host.top > innerHeight + 100) return;
          const p = (host.top + host.height / 2 - innerHeight / 2) / innerHeight; // -1 .. 1
          el.style.translate = `0 ${(p * -42).toFixed(1)}px`;
        });
      }
      vel = vel * .85 + (scrollY - lastY) * .15; lastY = scrollY;
      if (track && track.getAnimations) { const a = track.getAnimations()[0]; if (a) a.playbackRate = 1 + Math.min(Math.abs(vel) * .35, 6); }
    };
    const decay = () => {
      vel *= .9;
      if (Math.abs(vel) <= .05) {
        vel = 0; decaying = false;
        if (!ticking) { ticking = true; requestAnimationFrame(frame); }
        return;
      }
      if (!ticking) { ticking = true; requestAnimationFrame(frame); }
      requestAnimationFrame(decay);
    };
    const kick = () => {
      if (!ticking) { ticking = true; requestAnimationFrame(frame); }
      if (!decaying) { decaying = true; requestAnimationFrame(decay); }
    };
    addEventListener('scroll', kick, { passive: true }); addEventListener('resize', kick); frame();

    if (!fine) return;

    /* Hero: 3D tilt of the photo + floating note */
    const hv = $('.hero-visual');
    if (hv) {
      hv.addEventListener('pointermove', e => {
        const r = hv.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        hv.style.setProperty('--ry', (x * 12).toFixed(2) + 'deg'); hv.style.setProperty('--rx', (-y * 10).toFixed(2) + 'deg');
      });
      hv.addEventListener('pointerleave', () => { hv.style.setProperty('--ry', '0deg'); hv.style.setProperty('--rx', '0deg'); });
    }

    /* Product cards: tilt with moving glare */
    let raf = 0;
    document.addEventListener('pointermove', e => {
      const m = e.target.closest && e.target.closest('.pcard-media');
      if (!m) return;
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const r = m.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        m.style.setProperty('--ry', ((x - .5) * 14).toFixed(2) + 'deg'); m.style.setProperty('--rx', ((.5 - y) * 12).toFixed(2) + 'deg');
        m.style.setProperty('--gx', (x * 100).toFixed(0) + '%'); m.style.setProperty('--gy', (y * 100).toFixed(0) + '%');
        m.classList.add('tilting');
      });
    });
    document.addEventListener('pointerout', e => {
      const m = e.target.closest && e.target.closest('.pcard-media');
      if (m && !m.contains(e.relatedTarget)) { m.classList.remove('tilting'); m.style.setProperty('--rx', '0deg'); m.style.setProperty('--ry', '0deg'); }
    });

    /* Magnetic buttons */
    document.addEventListener('pointermove', e => {
      const b = e.target.closest && e.target.closest('.btn:not(.block)');
      $$('.btn.mag').forEach(x => { if (x !== b) { x.style.translate = ''; x.classList.remove('mag'); } });
      if (!b) return;
      const r = b.getBoundingClientRect();
      b.classList.add('mag');
      b.style.translate = `${((e.clientX - r.left - r.width / 2) * .18).toFixed(1)}px ${((e.clientY - r.top - r.height / 2) * .3).toFixed(1)}px`;
    });
  });
})();
