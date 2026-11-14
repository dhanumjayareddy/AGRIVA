#!/usr/bin/env python3
"""Generates the static HTML pages. Usage: python3 tools/build.py [--domain https://example.com]"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN = "https://YOUR-AGRIVA-DOMAIN.example"
if "--domain" in sys.argv: DOMAIN = sys.argv[sys.argv.index("--domain") + 1].rstrip("/")

NAV = [("index.html","Home"),("shop.html","Shop"),("about.html","Our Story"),("contact.html","Contact")]
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">'

def page(fname, key, title, desc, body, extra_head=""):
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{cur if h==fname else ""}>{t}</a>' for h,t in NAV)
    hero_preload = '<link rel="preload" as="image" href="assets/img/hero.jpg" fetchpriority="high">' if fname == "index.html" else ""
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta name="theme-color" content="#1f4636">
<link rel="canonical" href="{DOMAIN}/{'' if fname=='index.html' else fname}">
<meta property="og:type" content="website"><meta property="og:site_name" content="AGRIVA"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<link rel="icon" href="assets/agriva-mark.svg" type="image/svg+xml">{hero_preload}{FONTS}<link rel="stylesheet" href="styles.css">{extra_head}
<script defer src="site-config.js"></script><script defer src="images.js"></script><script defer src="catalog.js"></script><script defer src="app.js"></script><script defer src="fx.js"></script></head>
<body data-page="{key}"><a class="skip" href="#main">Skip to content</a>
<div class="bar">Cold pressed oils &amp; dry fruits · Order by WhatsApp</div>
<header class="site-header"><div class="container hd">
<a class="brand" href="index.html" aria-label="AGRIVA home"><img src="assets/agriva-mark.svg" alt="" width="34" height="34">AGRIVA</a>
<nav class="nav" id="nav" aria-label="Main">{nav}</nav>
<div class="hd-actions"><button class="basket-btn" aria-label="Open basket"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 8h14l-1.2 11.2a2 2 0 0 1-2 1.8H8.2a2 2 0 0 1-2-1.8L5 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg><span class="lbl">Basket</span><span class="basket-count" hidden>0</span></button>
<button class="menu-toggle" id="menuToggle" aria-label="Menu" aria-expanded="false"><span></span></button></div></div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="container"><div class="ft">
<div><a class="brand" href="index.html"><img src="assets/agriva-mark.svg" alt="" width="34" height="34">AGRIVA</a><p>Cold pressed oils and dry fruits for the everyday pantry. Details and availability confirmed by our team.</p></div>
<div><h4>Shop</h4><ul><li><a href="shop.html?category=oils">Cold pressed oils</a></li><li><a href="shop.html?category=dry-fruits">Dry fruits</a></li><li><a href="shop.html?category=seeds">Seeds</a></li></ul></div>
<div><h4>AGRIVA</h4><ul><li><a href="about.html">Our story</a></li><li><a href="contact.html">Contact</a></li><li><a href="policies.html">Customer information</a></li></ul></div>
<div><h4>Order</h4><ul><li><a href="contact.html">Ask a question</a></li><li><a href="policies.html#shipping">Delivery</a></li><li><a href="policies.html#credits">Image credits</a></li></ul></div></div>
<div class="legal"><span>© <span id="year">2026</span> AGRIVA. All rights reserved.</span><span>Prices and availability confirmed on enquiry.</span></div></div></footer>
<div class="drawer" id="drawer" aria-hidden="true"><div class="scrim" id="drawerScrim"></div>
<aside class="panel" role="dialog" aria-label="Basket"><div class="panel-head"><h2>Your basket</h2><button id="drawerClose" aria-label="Close basket">×</button></div>
<div id="basketList"></div>
<div id="basketFoot" hidden><p class="mini">No payment is taken on this site. We confirm price, stock and delivery with you first.</p>
<button class="btn" id="basketSend">Send basket on WhatsApp ↗</button>
<div class="foot-row"><button class="btn btn-ghost" id="basketCopy">Copy list</button><button class="btn btn-ghost" id="basketClear">Clear</button></div></div></aside></div>
</body></html>'''
    (ROOT/fname).write_text(html, encoding="utf-8")

# ---------------- Home ----------------
ticker = "".join(f"<span>{w}</span>" for w in ["Groundnut","Sesame","Coconut","Mustard","Almonds","Cashews","Pistachios","Walnuts","Dates","Figs","Apricots","Pumpkin seeds"]*2)
page("index.html","home","AGRIVA | Cold Pressed Oils & Dry Fruits",
 "Cold pressed oils and dry fruits from AGRIVA. Browse the range, build a basket and send it on WhatsApp. Price, stock and delivery confirmed by our team.",
f'''<section class="hero"><div class="container hero-grid">
<div><span class="kicker">Oils · Dry fruits · Seeds</span>
<h1 class="display">Goodness, kept <em>close</em> to its source.</h1>
<p class="lede">Cold pressed oils and everyday dry fruits, chosen for the pantry you actually cook from. Browse, build a basket, and we'll confirm the rest with you.</p>
<div class="hero-cta"><a class="btn" href="shop.html">Shop the range</a><a class="btn btn-ghost" href="about.html">Our story</a></div></div>
<div class="hero-visual"><div class="photo arch"><img src="assets/img/hero.jpg" data-slot="hero" data-local="assets/img/hero.jpg" fetchpriority="high" loading="eager" decoding="async" referrerpolicy="no-referrer" data-parallax alt="Cold pressed oil and dry fruits on a kitchen table"></div>
<div class="hero-stamp"><b>Ask before you order</b>Price, pack and stock confirmed by a real person.</div></div></div></section>
<div class="ticker" aria-hidden="true"><div class="ticker-track">{ticker}</div></div>

<section class="section"><div class="container">
<div class="section-head"><div><span class="kicker">Collections</span><h2 class="display">Two shelves, <em>one</em> kitchen.</h2></div><p>Start with the oils or the dry fruits. Every product page lets you pick a pack size and add it to your basket.</p></div>
<div class="collections">
<a class="coll oils reveal" href="shop.html?category=oils"><img data-slot="oils" data-local="assets/img/oils.jpg" loading="lazy" decoding="async" referrerpolicy="no-referrer" data-parallax alt=""><div class="coll-body"><span class="kicker">Collection 01</span><h3>Cold pressed oils</h3><p>Groundnut, sesame, coconut, mustard and more.</p><span class="go">Explore oils</span></div></a>
<a class="coll dry reveal" href="shop.html?category=dry-fruits"><img data-slot="dryfruits" data-local="assets/img/dryfruits.jpg" loading="lazy" decoding="async" referrerpolicy="no-referrer" data-parallax alt=""><div class="coll-body"><span class="kicker">Collection 02</span><h3>Dry fruits &amp; seeds</h3><p>Almonds, cashews, dates, figs and pumpkin seeds.</p><span class="go">Explore dry fruits</span></div></a>
</div></div></section>

<section class="section tight"><div class="container">
<div class="section-head"><div><span class="kicker">Pantry favourites</span><h2 class="display">Where most people start.</h2></div><a class="text-link" href="shop.html">View all products →</a></div>
<div class="grid" id="featuredGrid"></div></div></section>

<section class="section"><div class="container"><div class="finder">
<div><span class="kicker">Not sure where to begin?</span><h2 class="display">What are you <em>making</em> today?</h2><p>Pick an occasion and we'll point to the products people usually choose for it. A starting point, not a prescription. Ask us and we'll help you decide.</p><p class="fine" id="finderNote"></p></div>
<div><div class="chips" id="finderChips" role="tablist" aria-label="Choose an occasion"></div><div id="finderOut" aria-live="polite"></div></div></div></div></section>

<section class="section alt"><div class="container">
<div class="section-head"><div><span class="kicker">How ordering works</span><h2 class="display">Simple, and <em>human.</em></h2></div></div>
<div class="steps">
<div class="step reveal"><h3>Choose</h3><p>Pick products and pack sizes. Add them to your basket as you browse.</p></div>
<div class="step reveal"><h3>Send</h3><p>One tap sends your basket to us on WhatsApp. No account, no card details on this site.</p></div>
<div class="step reveal"><h3>Confirm</h3><p>We reply with price, availability and delivery to your location, then arrange payment with you directly.</p></div>
</div></div></section>''')

# ---------------- Shop ----------------
page("shop.html","shop","Shop Cold Pressed Oils & Dry Fruits | AGRIVA",
 "Browse AGRIVA's cold pressed oils, dry fruits and seeds. Filter by category, search, and add to your basket.",
'''<section class="page-head"><div class="container"><span class="kicker">The catalogue</span><h1 class="display">Shop the <em>range.</em></h1><p class="lede">Pick a category, search by name, and add what you'd like. Prices are confirmed when you enquire.</p></div></section>
<div class="toolbar"><div class="container"><div class="chips" id="shopChips" role="group" aria-label="Filter by category"></div>
<div class="tools"><input class="field" id="shopSearch" type="search" placeholder="Search products" aria-label="Search products"><select class="field" id="shopSort" aria-label="Sort"><option value="featured">Featured</option><option value="az">A to Z</option></select></div></div></div>
<section class="container" style="padding-bottom:4rem"><p class="count" id="shopCount" aria-live="polite"></p><div class="grid" id="shopGrid"></div>
<div class="empty" id="shopEmpty" hidden><h2 class="display">Nothing matches that.</h2><p>Try a different word, or clear the filters.</p><button class="btn" id="shopReset">Clear filters</button></div></section>''')

# ---------------- Product ----------------
page("product.html","product","Product | AGRIVA","Product details from AGRIVA. Choose a pack size and add it to your basket.",
 '<div id="productRoot"><div class="container" style="padding:5rem 0">Loading…</div></div>')

# ---------------- About ----------------
page("about.html","about","Our Story | AGRIVA","About AGRIVA: a focused catalogue of cold pressed oils and dry fruits for the everyday pantry, with clear answers before you order.",
'''<section class="page-head"><div class="container narrow" style="margin-inline:auto"><span class="kicker">Our story</span><h1 class="display">A smaller shelf, <em>better answered.</em></h1><p class="lede">AGRIVA keeps its catalogue focused on two familiar pantry categories, cold pressed oils and dry fruits, and puts a person behind every order.</p></div></section>
<section class="section"><div class="container split">
<div class="photo reveal"><img data-slot="story" data-local="assets/img/story.jpg" loading="lazy" decoding="async" referrerpolicy="no-referrer" data-parallax alt="Oils and dry fruits arranged on a wooden counter"></div>
<div class="reveal"><span class="kicker">What we do</span><h2 class="display">Clear information. <em>Direct</em> conversations.</h2>
<p>We'd rather you ask a question than guess. For every product, our team can confirm current availability, pack formats, price and batch-specific details before you pay.</p>
<p>Details such as origin, grade, ingredients, allergens and storage always come from the product label and current supplier records, not from a website's guesswork.</p>
<p style="margin-top:1.6rem"><a class="btn" href="shop.html">Browse the range</a></p></div></div></section>
<section class="section alt"><div class="container"><div class="section-head"><div><span class="kicker">How we work</span><h2 class="display">Three habits we keep.</h2></div></div>
<div class="values">
<div class="value reveal"><h3>Say only what's true</h3><p>No borrowed claims. If we can't document it, we don't print it.</p></div>
<div class="value reveal"><h3>Answer before you pay</h3><p>Price, stock and delivery are confirmed with you first, every time.</p></div>
<div class="value reveal"><h3>Keep it simple</h3><p>A focused range, honest pack options, and an ordering flow that fits in one message.</p></div></div></div></section>
<section class="section"><div class="container"><div class="cta-band"><div><h2 class="display">Have a <em>question?</em></h2><p style="opacity:.8;margin-top:.5rem">Ask about a product, a pack size or delivery to your area.</p></div><a class="btn" href="contact.html">Talk to AGRIVA</a></div></div></section>''')

# ---------------- Contact ----------------
page("contact.html","contact","Contact AGRIVA | Orders & Enquiries","Ask AGRIVA about products, pack sizes, pricing, bulk orders and delivery. Your message opens in WhatsApp.",
'''<section class="page-head"><div class="container"><span class="kicker">Contact</span><h1 class="display">Let's <em>talk</em> pantry.</h1><p class="lede">Ask about a product, current pack sizes, pricing, stock or delivery. We'll confirm the details before you order.</p></div></section>
<section class="section tight"><div class="container contact-grid">
<div><div class="topics" role="group" aria-label="Choose a topic">
<button class="topic" type="button" data-topic="Product enquiry" aria-pressed="false"><b>Product enquiry</b><span>Ingredients, pack formats, current availability.</span></button>
<button class="topic" type="button" data-topic="Order & delivery" aria-pressed="false"><b>Orders &amp; delivery</b><span>Share your location and products so we can confirm delivery.</span></button>
<button class="topic" type="button" data-topic="Bulk enquiry" aria-pressed="false"><b>Bulk / business</b><span>Products and approximate quantities you need.</span></button></div>
<dl class="details" id="contactDetails" hidden></dl></div>
<form class="card" id="enquiryForm"><input type="hidden" name="topic" id="topic">
<div class="row2"><label class="f">Your name<input class="field" name="name" required autocomplete="name"></label><label class="f">Phone number<input class="field" name="phone" type="tel" required autocomplete="tel"></label></div>
<label class="f">Email (optional)<input class="field" name="email" type="email" autocomplete="email"></label>
<label class="f">How can we help?<textarea class="field" id="message" name="message" required placeholder="Tell us what you're looking for…"></textarea></label>
<button class="btn" type="submit">Continue on WhatsApp ↗</button>
<p class="note">Your message opens in WhatsApp. This website doesn't store it on a server.</p></form></div></section>
<section class="section"><div class="container faq"><div class="section-head"><h2 class="display">Quick answers.</h2></div><div class="acc">
<details><summary>Do you take payment on the website?</summary><p>No. We confirm your order by message first, then agree payment with you directly.</p></details>
<details><summary>Why is there no price on products?</summary><p>Prices change with batch and pack size. We confirm the current price when you enquire, so you never see an outdated number.</p></details>
<details><summary>Can I order for a business or event?</summary><p>Yes. Choose "Bulk / business" above and tell us the products and rough quantities.</p></details>
<details><summary>How do I know the details of what I'm buying?</summary><p>Ask us before you order, and always check the label on the pack for ingredients, allergens and storage.</p></details></div></div></section>''')

# ---------------- Policies ----------------
page("policies.html","policies","Customer Information | AGRIVA","Ordering, delivery, returns, privacy and website terms for AGRIVA customers.",
'''<section class="page-head"><div class="container"><span class="kicker">Customer information</span><h1 class="display">Ordering with <em>AGRIVA.</em></h1></div></section>
<section class="section tight"><div class="container">
<div class="draft"><b>Draft for owner approval.</b> Replace the notes in each section with AGRIVA's approved legal, shipping, returns and privacy wording before taking public orders.</div>
<div class="ptabs" role="tablist"><button class="ptab" data-t="orders" role="tab">Orders &amp; payment</button><button class="ptab" data-t="shipping" role="tab">Delivery</button><button class="ptab" data-t="returns" role="tab">Returns</button><button class="ptab" data-t="privacy" role="tab">Privacy</button><button class="ptab" data-t="terms" role="tab">Terms</button><button class="ptab" data-t="credits" role="tab">Image credits</button></div>
<div class="psec" id="orders"><h2>Orders &amp; payment</h2><p>An enquiry is not an accepted order. AGRIVA confirms the product, pack size, final price, taxes if applicable, delivery charges, payment method and estimated dispatch before you pay.</p><p><i>To add: accepted payment methods, invoice details, cancellation cut-off.</i></p></div>
<div class="psec" id="shipping" hidden><h2>Delivery</h2><p>Availability, charges and timelines depend on your location and order. Please confirm serviceability and delivery estimates with AGRIVA before ordering.</p><p><i>To add: serviceable pincodes, dispatch timelines, courier partners, charges, process for delayed or damaged parcels.</i></p></div>
<div class="psec" id="returns" hidden><h2>Returns, replacements &amp; refunds</h2><p>Food products may have specific conditions. If a parcel arrives damaged, incorrect or with a quality concern, contact AGRIVA promptly and keep the packaging and batch details until the issue is reviewed.</p><p><i>To add: return window, eligible cases, evidence required, refund method and timeline.</i></p></div>
<div class="psec" id="privacy" hidden><h2>Privacy</h2><p>This website has no customer accounts and doesn't send contact forms to a server. Your basket is kept only in your own browser. Enquiries are handed to WhatsApp, which has its own privacy terms. Fonts are loaded from Google Fonts.</p><p><i>To add: business contact for privacy questions, and a full notice before adding analytics, accounts or marketing.</i></p></div>
<div class="psec" id="terms" hidden><h2>Website terms</h2><p>Product descriptions and pack options are guidance. Current price, stock, pack format, label information and delivery are confirmed by AGRIVA. No product should be described as certified, organic, therapeutic or of a particular origin or grade unless documented and approved.</p><p><i>To add: legal business name, registered address, jurisdiction, grievance contact.</i></p></div>
<div class="psec" id="credits" hidden><h2>Image credits</h2><p id="creditEmpty">Photo credits appear here once product images are added with <code>tools/fetch_images.py</code>.</p><ul id="creditList"></ul></div>
</div></section>''')

# ---------------- 404 ----------------
page("404.html","notfound","Page not found | AGRIVA","That page could not be found.",
 '<section class="section"><div class="container narrow center"><span class="kicker">404</span><h1 class="display">That shelf <em>is empty.</em></h1><p class="lede" style="margin:1rem auto 2rem">The page you were looking for isn&rsquo;t here.</p><a class="btn" href="index.html">Back home</a> <a class="btn btn-ghost" href="shop.html">Shop</a></div></section>')

# ---------------- sitemap / robots ----------------
urls = ["", "shop.html", "about.html", "contact.html", "policies.html"]
(ROOT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{DOMAIN}/{u}</loc></url>\n" for u in urls) + '</urlset>\n')
(ROOT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
print("built for", DOMAIN)
