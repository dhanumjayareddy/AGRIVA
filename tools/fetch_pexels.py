#!/usr/bin/env python3
"""
Pexels downloader with a visual review step, so every photo matches its product.
Pexels photos are free to use (Pexels License). Get a free API key at https://www.pexels.com/api/

  export PEXELS_API_KEY=your_key            (Windows PowerShell: $env:PEXELS_API_KEY="your_key")
  python3 tools/fetch_pexels.py --review    # builds tools/review.html with 8 candidates per product
  python3 tools/fetch_pexels.py --pick almonds 1234567     # download the Pexels photo id you chose
  python3 tools/fetch_pexels.py --urls      # hotlink mode: writes images.js with direct Pexels URLs, no downloads
  python3 tools/fetch_pexels.py --auto      # fast path: best text match for every missing image, then CHECK them
Open tools/review.html in a browser, click through, and run the --pick command shown under each photo.
"""
import json, os, sys, pathlib, urllib.parse, urllib.request, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEY = os.environ.get("PEXELS_API_KEY", "")
UA = "AGRIVA-site-setup/1.0"

# key -> (output file, search query, words that must appear in the photo's description)
JOBS = {
 "groundnut-oil": ("assets/products/groundnut-oil.jpg", "peanut oil bottle", ["oil"]),
 "sesame-oil":    ("assets/products/sesame-oil.jpg", "sesame oil", ["sesame"]),
 "coconut-oil":   ("assets/products/coconut-oil.jpg", "coconut oil jar", ["coconut", "oil"]),
 "mustard-oil":   ("assets/products/mustard-oil.jpg", "mustard oil", ["mustard"]),
 "sunflower-oil": ("assets/products/sunflower-oil.jpg", "sunflower oil bottle", ["sunflower", "oil"]),
 "safflower-oil": ("assets/products/safflower-oil.jpg", "safflower oil", ["safflower", "oil"]),
 "almond-oil":    ("assets/products/almond-oil.jpg", "almond oil bottle", ["almond", "oil"]),
 "almonds":       ("assets/products/almonds.jpg", "almonds", ["almond"]),
 "cashews":       ("assets/products/cashews.jpg", "cashew nuts", ["cashew"]),
 "pistachios":    ("assets/products/pistachios.jpg", "pistachios", ["pistachio"]),
 "walnuts":       ("assets/products/walnuts.jpg", "walnuts kernels", ["walnut"]),
 "raisins":       ("assets/products/raisins.jpg", "raisins", ["raisin"]),
 "dates":         ("assets/products/dates.jpg", "dates dried fruit", ["date"]),
 "dried-figs":    ("assets/products/dried-figs.jpg", "dried figs", ["fig"]),
 "dried-apricots":("assets/products/dried-apricots.jpg", "dried apricots", ["apricot"]),
 "pumpkin-seeds": ("assets/products/pumpkin-seeds.jpg", "pumpkin seeds", ["pumpkin", "seed"]),
 "hero":          ("assets/img/hero.jpg", "nuts dried fruits oil still life", []),
 "oils":          ("assets/img/oils.jpg", "cooking oil bottles", ["oil"]),
 "dryfruits":     ("assets/img/dryfruits.jpg", "mixed dry fruits nuts bowl", []),
 "story":         ("assets/img/story.jpg", "indian spices nuts market", []),
}

def call(url):
    req = urllib.request.Request(url, headers={"Authorization": KEY, "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r: return r.read()

def search(q, n=8):
    u = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode({"query": q, "per_page": n, "orientation": "landscape"})
    return json.loads(call(u)).get("photos", [])

def score(ph, words):
    alt = (ph.get("alt") or "").lower()
    return sum(w in alt for w in words)

def save(key, ph):
    out = ROOT / JOBS[key][0]; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(call(ph["src"]["large2x"].split("?")[0] + "?auto=compress&cs=tinysrgb&w=1400"))
    cj = ROOT / "assets/credits.json"
    c = json.loads(cj.read_text()) if cj.exists() else {}
    c[key] = {"title": (ph.get("alt") or f"Pexels photo {ph['id']}")[:90], "author": ph["photographer"], "license": "Pexels License", "source": ph["url"]}
    cj.write_text(json.dumps(c, indent=2, ensure_ascii=False))
    print(f"saved {JOBS[key][0]}  ← Pexels {ph['id']} by {ph['photographer']}")

def main():
    if not KEY: sys.exit("Set PEXELS_API_KEY first (free key: https://www.pexels.com/api/)")
    if "--pick" in sys.argv:
        i = sys.argv.index("--pick"); key, pid = sys.argv[i+1], sys.argv[i+2]
        if key not in JOBS: sys.exit("Unknown key " + key)
        ph = json.loads(call(f"https://api.pexels.com/v1/photos/{pid}")); save(key, ph); return
    if "--review" in sys.argv:
        rows = []
        for key, (out, q, words) in JOBS.items():
            try: phs = sorted(search(q), key=lambda p: -score(p, words))
            except Exception as e: rows.append(f"<h2>{key}</h2><p>search failed: {html.escape(str(e))}</p>"); continue
            cards = "".join(f'<figure><img src="{p["src"]["medium"]}" loading="lazy"><figcaption>{html.escape((p.get("alt") or "")[:80])}<br><code>python3 tools/fetch_pexels.py --pick {key} {p["id"]}</code></figcaption></figure>' for p in phs)
            rows.append(f"<h2>{key} <small>“{html.escape(q)}”</small></h2><div class=g>{cards}</div>")
        (ROOT / "tools/review.html").write_text('<!doctype html><meta charset=utf-8><title>Pick photos</title><style>body{font:15px system-ui;margin:2rem;background:#f5efe3}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}img{width:100%;height:160px;object-fit:cover;border-radius:10px}figure{margin:0}figcaption{font-size:12px}code{font-size:11px;user-select:all;background:#fff;padding:2px 4px;display:block;margin-top:4px;word-break:break-all}</style><h1>Choose the photo that matches each product</h1>' + "".join(rows))
        print("Open tools/review.html, then run the --pick command under each photo you want."); return
    if "--urls" in sys.argv:
        urls, credits = {}, {}
        for key, (out, q, words) in JOBS.items():
            try: phs = sorted(search(q), key=lambda p: -score(p, words))
            except Exception as e: print("search failed:", key, e); continue
            if not phs: print("no result:", key); continue
            ph = phs[0]; size = "large2x" if key in ("hero", "oils", "dryfruits", "story") else "large"
            urls[key] = ph["src"][size]
            credits[key] = {"title": (ph.get("alt") or f"Pexels photo {ph['id']}")[:90], "author": ph["photographer"], "license": "Pexels License", "source": ph["url"]}
            print(f"{key}: {ph.get('alt','')[:70]}")
        (ROOT / "images.js").write_text("/* Generated by tools/fetch_pexels.py --urls. Check each photo matches; replace any URL by hand. */\nwindow.AGRIVA_IMAGES = " + json.dumps(urls, indent=2) + ";\n")
        (ROOT / "assets/credits.json").write_text(json.dumps(credits, indent=2, ensure_ascii=False))
        print("Wrote images.js. Open the site and check every photo matches its product."); return
    if "--auto" in sys.argv:
        for key, (out, q, words) in JOBS.items():
            if (ROOT / out).exists(): print("exists:", key); continue
            phs = sorted(search(q), key=lambda p: -score(p, words))
            if phs: save(key, phs[0])
            else: print("no result:", key)
        print("Now open each page and CHECK every photo matches its product; swap with --pick if not."); return
    print(__doc__)

if __name__ == "__main__": main()
