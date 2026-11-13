(() => {
  'use strict';
  const P = window.AGRIVA_PRODUCTS || [];
  const USES = window.AGRIVA_USES || [];
  const CFG = window.AGRIVA_CONFIG || {};
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const byId = id => P.find(p => p.id === id);
  const store = {
    get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} }
  };
  const priceText = p => p.price ? esc(p.price) : 'Price on enquiry';

  /* ---------- Toast ---------- */
  function toast(msg) {
    let el = $('#toast');
    if (!el) { el = document.createElement('div'); el.id = 'toast'; el.className = 'toast'; el.setAttribute('role', 'status'); document.body.append(el); }
    el.textContent = msg; el.classList.add('show');
    clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove('show'), 2600);
  }

  /* ---------- Image with graceful fallback ---------- */
  function media(p, size = 'card') {
    return `<div class="media media-${size}" style="--tone:${p.tone}"><span class="media-fallback"><b>${esc(p.short)}</b><i>${esc(p.catLabel)}</i></span><img data-slot="${p.id}" data-local="assets/products/${p.id}.jpg" alt="${esc(p.name)}" loading="lazy" decoding="async" referrerpolicy="no-referrer"></div>`;
  }
  /* Every <img data-slot> tries the URL in images.js first, then the local file, then hides itself. */
  function wireImages(root = document) {
    const map = window.AGRIVA_IMAGES || {};
    $$('img[data-slot]', root).forEach(img => {
      if (img.dataset.wired) return; img.dataset.wired = '1';
      const remote = map[img.dataset.slot], local = img.dataset.local;
      let usedLocal = !remote;
      img.addEventListener('load', () => img.classList.add('is-loaded'));
      img.addEventListener('error', () => { if (!usedLocal && local) { usedLocal = true; img.src = local; } else img.remove(); });
      img.src = remote || local;
    });
  }

  /* ---------- Product card ---------- */
  function card(p) {
    const href = `product.html?product=${encodeURIComponent(p.id)}`;
    return `<article class="pcard reveal"><a class="pcard-media" href="${href}" aria-label="${esc(p.name)}">${media(p)}</a>
      <div class="pcard-body"><span class="kicker">${esc(p.catLabel)}</span>
      <h3><a href="${href}">${esc(p.name)}</a></h3><p>${esc(p.blurb)}</p>
      <div class="pcard-foot"><span class="price">${priceText(p)}</span>
      <button class="add" data-quick="${p.id}" aria-label="Add ${esc(p.name)} to basket"><span>Add</span><svg viewBox="0 0 20 20" width="16" height="16" aria-hidden="true"><path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></button></div></div></article>`;
  }

  /* ---------- Basket ---------- */
  const KEY = 'agriva_basket_v2';
  let basket = store.get(KEY, []).filter(i => byId(i.id));
  const save = () => { store.set(KEY, basket); renderBasket(); };
  const count = () => basket.reduce((n, i) => n + i.qty, 0);
  function addToBasket(id, pack, qty = 1) {
    const p = byId(id); if (!p) return;
    pack = pack || p.packs[0];
    const found = basket.find(i => i.id === id && i.pack === pack);
    if (found) found.qty = Math.min(found.qty + qty, 99); else basket.push({ id, pack, qty });
    save(); bump(); toast(`${p.short} · ${pack} added to basket`);
  }
  function bump() { const b = $('.basket-btn'); if (!b) return; b.classList.remove('bump'); void b.offsetWidth; b.classList.add('bump'); }
  function basketMessage() {
    const lines = basket.map((i, n) => `${n + 1}. ${byId(i.id).name} — ${i.pack} × ${i.qty}`);
    return `Hello AGRIVA, I'd like to order:\n\n${lines.join('\n')}\n\nPlease confirm availability, price and delivery to my location.`;
  }
  function openWhatsApp(message) {
    const n = String(CFG.whatsappNumber || '').replace(/\D/g, '');
    if (!n) {
      (navigator.clipboard ? navigator.clipboard.writeText(message) : Promise.reject()).then(
        () => toast('WhatsApp number not set yet. Message copied instead.'),
        () => toast('WhatsApp number not set yet. See site-config.js.'));
      return;
    }
    window.open(`https://wa.me/${n}?text=${encodeURIComponent(message)}`, '_blank', 'noopener');
  }
  function renderBasket() {
    const n = count();
    $$('.basket-count').forEach(el => { el.textContent = n; el.hidden = n === 0; });
    const list = $('#basketList'), foot = $('#basketFoot');
    if (!list) return;
    if (!basket.length) {
      list.innerHTML = `<div class="basket-empty"><p class="display">Your basket is empty.</p><p>Browse the range and add what you'd like to ask about.</p><a class="btn" href="shop.html">Browse the shop</a></div>`;
      foot.hidden = true; return;
    }
    foot.hidden = false;
    list.innerHTML = basket.map((i, idx) => { const p = byId(i.id); return `<div class="bline">
      <a class="bline-media" href="product.html?product=${p.id}">${media(p, 'thumb')}</a>
      <div class="bline-info"><a href="product.html?product=${p.id}">${esc(p.name)}</a><span>${esc(i.pack)}</span>
      <div class="stepper sm"><button data-dec="${idx}" aria-label="Decrease">−</button><output>${i.qty}</output><button data-inc="${idx}" aria-label="Increase">+</button></div></div>
      <button class="bline-x" data-rm="${idx}" aria-label="Remove ${esc(p.name)}">×</button></div>`; }).join('');
    wireImages(list);
  }
  function setDrawer(open) {
    const d = $('#drawer'); if (!d) return;
    const wasOpen = d.classList.contains('open');
    d.classList.toggle('open', open); d.setAttribute('aria-hidden', String(!open));
    document.body.classList.toggle('lock', open);
    if (open) $('#drawerClose').focus();
    else if (wasOpen) $('.basket-btn')?.focus();
  }

  /* ---------- Global wiring ---------- */
  function wireGlobal() {
    const header = $('.site-header');
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 8);
    onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

    const nav = $('#nav'), tgl = $('#menuToggle');
    const closeNav = () => { nav.classList.remove('open'); tgl.setAttribute('aria-expanded', 'false'); document.body.classList.remove('lock'); };
    tgl.addEventListener('click', () => { const o = nav.classList.toggle('open'); tgl.setAttribute('aria-expanded', String(o)); document.body.classList.toggle('lock', o); });
    $$('#nav a').forEach(a => a.addEventListener('click', closeNav));

    document.addEventListener('click', e => {
      const t = e.target.closest('button, a'); if (!t) return;
      if (t.matches('.basket-btn')) setDrawer(true);
      else if (t.id === 'drawerClose' || t.id === 'drawerScrim') setDrawer(false);
      else if (t.dataset.quick) addToBasket(t.dataset.quick);
      else if (t.dataset.inc !== undefined) { basket[+t.dataset.inc].qty = Math.min(99, basket[+t.dataset.inc].qty + 1); save(); }
      else if (t.dataset.dec !== undefined) { const i = basket[+t.dataset.dec]; i.qty--; if (i.qty < 1) basket.splice(+t.dataset.dec, 1); save(); }
      else if (t.dataset.rm !== undefined) { basket.splice(+t.dataset.rm, 1); save(); }
      else if (t.id === 'basketSend') openWhatsApp(basketMessage());
      else if (t.id === 'basketCopy') navigator.clipboard?.writeText(basketMessage()).then(() => toast('Basket copied'));
      else if (t.id === 'basketClear') { basket = []; save(); }
    });
    document.addEventListener('keydown', e => {
      if (e.key !== 'Escape') return;
      if ($('#drawer')?.classList.contains('open')) setDrawer(false);
      if (nav.classList.contains('open')) { closeNav(); tgl.focus(); }
    });
    $$('[data-wa]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); openWhatsApp(a.dataset.wa); }));

    const yr = $('#year'); if (yr) yr.textContent = new Date().getFullYear();
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }), { threshold: .12 });
      window.observeReveals = (root = document) => $$('.reveal:not(.in)', root).forEach(el => io.observe(el));
    } else window.observeReveals = (root = document) => $$('.reveal', root).forEach(el => el.classList.add('in'));
    window.observeReveals();
    renderBasket(); wireImages();
  }

  /* ---------- Pages ---------- */
  const pages = {
    home() {
      const grid = $('#featuredGrid');
      grid.innerHTML = P.filter(p => p.featured).slice(0, 6).map(card).join('');
      wireImages(grid); window.observeReveals(grid);

      const chips = $('#finderChips'), out = $('#finderOut'), note = $('#finderNote');
      chips.innerHTML = USES.map((u, i) => `<button class="chip" role="tab" aria-selected="${i === 0}" data-use="${u.key}">${esc(u.label)}</button>`).join('');
      const show = key => {
        const u = USES.find(x => x.key === key);
        note.textContent = u.note;
        const list = P.filter(p => p.uses.includes(key));
        out.innerHTML = list.map(p => `<a class="pick" href="product.html?product=${p.id}" style="--tone:${p.tone}"><i></i><span>${esc(p.short)}</span><em>${esc(p.catLabel)}</em></a>`).join('');
        $$('#finderChips .chip').forEach(c => c.setAttribute('aria-selected', c.dataset.use === key));
      };
      chips.addEventListener('click', e => { const c = e.target.closest('.chip'); if (c) show(c.dataset.use); });
      show(USES[0].key);
    },

    shop() {
      const q = new URLSearchParams(location.search);
      let state = { cat: q.get('category') || 'all', term: '', sort: 'featured' };
      const cats = [['all', 'All'], ['oils', 'Cold pressed oils'], ['dry-fruits', 'Dry fruits'], ['seeds', 'Seeds']];
      if (!cats.some(c => c[0] === state.cat)) state.cat = 'all';
      const bar = $('#shopChips'), grid = $('#shopGrid'), meta = $('#shopCount'), empty = $('#shopEmpty');
      bar.innerHTML = cats.map(c => `<button class="chip" data-cat="${c[0]}" aria-pressed="${c[0] === state.cat}">${c[1]}<sup>${c[0] === 'all' ? P.length : P.filter(p => p.cat === c[0]).length}</sup></button>`).join('');
      const draw = () => {
        let list = P.filter(p => (state.cat === 'all' || p.cat === state.cat) && (`${p.name} ${p.blurb} ${p.catLabel}`).toLowerCase().includes(state.term));
        if (state.sort === 'az') list = [...list].sort((a, b) => a.name.localeCompare(b.name));
        else if (state.sort === 'featured') list = [...list].sort((a, b) => !!b.featured - !!a.featured);
        grid.innerHTML = list.map(card).join('');
        empty.hidden = list.length > 0;
        meta.textContent = `${list.length} ${list.length === 1 ? 'product' : 'products'}`;
        $$('#shopChips .chip').forEach(c => c.setAttribute('aria-pressed', c.dataset.cat === state.cat));
        wireImages(grid); window.observeReveals(grid);
      };
      bar.addEventListener('click', e => { const c = e.target.closest('.chip'); if (!c) return; state.cat = c.dataset.cat; history.replaceState(null, '', state.cat === 'all' ? 'shop.html' : `shop.html?category=${state.cat}`); draw(); });
      $('#shopSearch').addEventListener('input', e => { state.term = e.target.value.trim().toLowerCase(); draw(); });
      $('#shopSort').addEventListener('change', e => { state.sort = e.target.value; draw(); });
      $('#shopReset').addEventListener('click', () => { state = { cat: 'all', term: '', sort: 'featured' }; $('#shopSearch').value = ''; $('#shopSort').value = 'featured'; draw(); });
      draw();
    },

    product() {
      const id = new URLSearchParams(location.search).get('product');
      const p = byId(id), root = $('#productRoot');
      if (!p) { root.innerHTML = `<div class="container narrow center"><h1 class="display">That product isn't in the catalogue.</h1><p>It may have been renamed or removed.</p><a class="btn" href="shop.html">Back to the shop</a></div>`; return; }
      document.title = `${p.name} | AGRIVA`;
      const md = $('meta[name="description"]'); if (md) md.content = `${p.name} from AGRIVA. ${p.desc}`;
      let pack = p.packs[0], qty = 1;
      const related = P.filter(x => x.cat === p.cat && x.id !== p.id).slice(0, 4);
      root.innerHTML = `<div class="container pd">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><a href="shop.html?category=${p.cat}">${esc(p.catLabel)}</a><span>/</span><b>${esc(p.short)}</b></nav>
        <div class="pd-grid">
          <div class="pd-media">${media(p, 'hero')}</div>
          <div class="pd-info">
            <span class="kicker">${esc(p.catLabel)}</span>
            <h1 class="display">${esc(p.name)}</h1>
            <p class="lede">${esc(p.desc)}</p>
            <div class="pd-price"><span class="price big">${priceText(p)}</span><small>Final price confirmed by our team before you pay.</small></div>
            <fieldset class="packs"><legend>Pack size</legend>${p.packs.map((k, i) => `<label class="pack"><input type="radio" name="pack" value="${esc(k)}" ${i ? '' : 'checked'}><span>${esc(k)}</span></label>`).join('')}</fieldset>
            <div class="buy-row"><div class="stepper"><button id="qDec" aria-label="Decrease quantity">−</button><output id="qVal">1</output><button id="qInc" aria-label="Increase quantity">+</button></div>
              <button class="btn grow" id="addBtn">Add to basket</button></div>
            <button class="btn btn-ghost block" id="askBtn">Ask about this on WhatsApp ↗</button>
            <div class="acc">
              <details open><summary>Before you order</summary><p>Current price, availability and pack formats are confirmed by AGRIVA at enquiry. Always check the label of the pack you receive for ingredients, allergens, storage and best-before information.</p></details>
              <details><summary>Delivery</summary><p>Serviceability and charges depend on your location. Share your pincode when you enquire and we'll confirm.</p></details>
              <details><summary>Storage</summary><p>Follow the storage instructions printed on the pack. As a general rule, keep oils and dry fruits sealed, away from heat and direct sun.</p></details>
            </div>
          </div>
        </div></div>
        <section class="section tight"><div class="container"><div class="section-head"><h2 class="display">More from ${p.cat === 'oils' ? 'the oil range' : 'the pantry'}</h2><a class="text-link" href="shop.html?category=${p.cat}">See all →</a></div><div class="grid">${related.map(card).join('')}</div></div></section>`;
      wireImages(root); window.observeReveals(root);
      $$('input[name=pack]').forEach(r => r.addEventListener('change', e => pack = e.target.value));
      const qv = $('#qVal');
      $('#qInc').addEventListener('click', () => { qty = Math.min(99, qty + 1); qv.textContent = qty; });
      $('#qDec').addEventListener('click', () => { qty = Math.max(1, qty - 1); qv.textContent = qty; });
      $('#addBtn').addEventListener('click', () => addToBasket(p.id, pack, qty));
      $('#askBtn').addEventListener('click', () => openWhatsApp(`Hello AGRIVA, I'd like to know more about ${p.name} (${pack}). Could you share the current price, availability and delivery to my location?`));
    },

    contact() {
      const rows = [['phoneDisplay', 'Phone', v => v], ['email', 'Email', v => `<a href="mailto:${esc(v)}">${esc(v)}</a>`], ['address', 'Address', v => v], ['hours', 'Hours', v => v]]
        .filter(r => CFG[r[0]]).map(r => `<div><dt>${r[1]}</dt><dd>${r[2](esc(CFG[r[0]]))}</dd></div>`).join('');
      if (rows) { $('#contactDetails').innerHTML = rows; $('#contactDetails').hidden = false; }
      $('#enquiryForm').addEventListener('submit', e => {
        e.preventDefault();
        const f = new FormData(e.target);
        const msg = `Hello AGRIVA,\n\n${f.get('message')}\n\nName: ${f.get('name')}\nPhone: ${f.get('phone')}${f.get('email') ? '\nEmail: ' + f.get('email') : ''}${f.get('topic') ? '\nTopic: ' + f.get('topic') : ''}`;
        openWhatsApp(msg);
      });
      $$('.topic').forEach(b => b.addEventListener('click', () => { $('#topic').value = b.dataset.topic; $$('.topic').forEach(x => x.setAttribute('aria-pressed', x === b)); $('#message').focus(); }));
    },

    policies() {
      const tabs = $$('.ptab'), secs = $$('.psec');
      const pick = id => { tabs.forEach(t => t.setAttribute('aria-selected', t.dataset.t === id)); secs.forEach(s => s.hidden = s.id !== id); };
      tabs.forEach(t => t.addEventListener('click', () => { pick(t.dataset.t); history.replaceState(null, '', '#' + t.dataset.t); }));
      pick(secs.some(s => s.id === location.hash.slice(1)) ? location.hash.slice(1) : secs[0].id);
      fetch('assets/credits.json').then(r => r.ok ? r.json() : null).then(c => {
        if (!c || !Object.keys(c).length) return;
        $('#creditList').innerHTML = Object.entries(c).map(([k, v]) => `<li><b>${esc(k)}</b> — <a href="${esc(v.source)}" rel="noopener" target="_blank">${esc(v.title)}</a> by ${esc(v.author)} · ${esc(v.license)}</li>`).join('');
        $('#creditEmpty').hidden = true;
      }).catch(() => {});
    }
  };

  document.addEventListener('DOMContentLoaded', () => {
    wireGlobal();
    const run = pages[document.body.dataset.page]; if (run) run();
  });
})();
