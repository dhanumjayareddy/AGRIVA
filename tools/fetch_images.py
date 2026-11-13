#!/usr/bin/env python3
"""
Downloads openly licensed photos from Wikimedia Commons into assets/ and records credits.

  python3 tools/fetch_images.py                 # fetch every missing image
  python3 tools/fetch_images.py --only almonds  # one product (or: hero, oils, dryfruits, story)
  python3 tools/fetch_images.py --list almonds  # show candidates, download nothing
  python3 tools/fetch_images.py --pick almonds "File:Some_name.jpg"   # use a specific file
  python3 tools/fetch_images.py --force         # replace existing images

Only CC0, public domain, CC BY and CC BY-SA files are accepted. Credits go to assets/credits.json
and are shown on the Customer information page. Review every photo before publishing.
Replace any of them with your own product photos by saving a JPG with the same file name.
"""
import json, re, sys, time, pathlib, urllib.parse, urllib.request, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://commons.wikimedia.org/w/api.php"
UA = "AGRIVA-site-image-fetch/1.0 (static website setup script)"
OK_LICENSE = re.compile(r"^(cc0|public domain|pd|cc[ -]by(?!.*nc)(?!.*nd))", re.I)

# key -> (output path, search query, words that should appear in the file title)
JOBS = {
 "groundnut-oil": ("assets/products/groundnut-oil.jpg", "groundnut oil bottle", ["oil"]),
 "sesame-oil":    ("assets/products/sesame-oil.jpg", "sesame oil bottle", ["sesame"]),
 "coconut-oil":   ("assets/products/coconut-oil.jpg", "coconut oil jar", ["coconut"]),
 "mustard-oil":   ("assets/products/mustard-oil.jpg", "mustard oil bottle", ["mustard"]),
 "sunflower-oil": ("assets/products/sunflower-oil.jpg", "sunflower oil bottle", ["sunflower"]),
 "safflower-oil": ("assets/products/safflower-oil.jpg", "safflower oil", ["safflower"]),
 "almond-oil":    ("assets/products/almond-oil.jpg", "almond oil bottle", ["almond"]),
 "almonds":       ("assets/products/almonds.jpg", "almonds shelled bowl", ["almond"]),
 "cashews":       ("assets/products/cashews.jpg", "cashew nuts bowl", ["cashew"]),
 "pistachios":    ("assets/products/pistachios.jpg", "pistachios shelled", ["pistachio"]),
 "walnuts":       ("assets/products/walnuts.jpg", "walnut kernels", ["walnut"]),
 "raisins":       ("assets/products/raisins.jpg", "raisins bowl", ["raisin"]),
 "dates":         ("assets/products/dates.jpg", "dates fruit dried", ["date"]),
 "dried-figs":    ("assets/products/dried-figs.jpg", "dried figs", ["fig"]),
 "dried-apricots":("assets/products/dried-apricots.jpg", "dried apricots", ["apricot"]),
 "pumpkin-seeds": ("assets/products/pumpkin-seeds.jpg", "pumpkin seeds pepitas", ["pumpkin"]),
 "hero":          ("assets/img/hero.jpg", "nuts dried fruits oil table still life", []),
 "oils":          ("assets/img/oils.jpg", "cooking oil bottles", ["oil"]),
 "dryfruits":     ("assets/img/dryfruits.jpg", "mixed dried fruits and nuts", []),
 "story":         ("assets/img/story.jpg", "spices nuts market india", []),
}

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()

def search(query, limit=25):
    q = {"action":"query","format":"json","generator":"search","gsrnamespace":"6","gsrsearch":query + " filetype:bitmap",
         "gsrlimit":str(limit),"prop":"imageinfo","iiprop":"url|mime|size|extmetadata","iiurlwidth":"1400"}
    data = json.loads(get(API + "?" + urllib.parse.urlencode(q)))
    out = []
    for pg in (data.get("query", {}).get("pages", {}) or {}).values():
        ii = (pg.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "")
        if ii.get("mime") != "image/jpeg" or not OK_LICENSE.match(lic): continue
        if ii.get("width", 0) < 900 or ii.get("height", 0) < 700: continue
        author = re.sub(r"<[^>]+>", "", md.get("Artist", {}).get("value", "Unknown"))
        out.append({"title": pg["title"], "url": ii.get("thumburl") or ii["url"], "page": ii.get("descriptionurl"),
                    "license": lic, "author": html.unescape(author).strip()[:120] or "Unknown",
                    "w": ii["width"], "h": ii["height"], "index": pg.get("index", 99)})
    return sorted(out, key=lambda c: c["index"])

def score(c, words):
    t = c["title"].lower()
    s = -c["index"]
    s += 8 * sum(w in t for w in words)
    ratio = c["w"] / c["h"]
    s += 3 if 0.9 <= ratio <= 1.6 else 0
    s -= 6 if any(b in t for b in ("tree","flower","plantation","map","diagram","logo","painting")) else 0
    return s

def save(key, cand):
    path = ROOT / JOBS[key][0]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(get(cand["url"]))
    cj = ROOT / "assets/credits.json"
    credits = json.loads(cj.read_text()) if cj.exists() else {}
    credits[key] = {"title": cand["title"].replace("File:", ""), "author": cand["author"], "license": cand["license"], "source": cand["page"]}
    cj.write_text(json.dumps(credits, indent=2, ensure_ascii=False))
    print(f"  saved {JOBS[key][0]}  ←  {cand['title']}  [{cand['license']}]")

def arg(flag):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else None

def main():
    only, lst, pick = arg("--only"), arg("--list"), arg("--pick")
    force = "--force" in sys.argv
    if pick:
        key, fname = pick, sys.argv[sys.argv.index("--pick") + 2]
        q = {"action":"query","format":"json","titles":fname,"prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":"1400"}
        pg = list(json.loads(get(API + "?" + urllib.parse.urlencode(q)))["query"]["pages"].values())[0]
        ii, md = pg["imageinfo"][0], pg["imageinfo"][0]["extmetadata"]
        save(key, {"title": pg["title"], "url": ii.get("thumburl") or ii["url"], "page": ii["descriptionurl"],
                   "license": md.get("LicenseShortName", {}).get("value", "?"),
                   "author": html.unescape(re.sub(r"<[^>]+>", "", md.get("Artist", {}).get("value", "Unknown")))[:120]})
        return
    keys = [lst] if lst else [only] if only else list(JOBS)
    for key in keys:
        if key not in JOBS: sys.exit(f"Unknown key: {key}")
        out, query, words = JOBS[key]
        if not lst and (ROOT / out).exists() and not force:
            print(f"- {key}: exists, skipping"); continue
        print(f"- {key}: searching “{query}”")
        try:
            cands = search(query)
        except Exception as e:
            print("  search failed:", e); continue
        if not cands: print("  no suitable open-licence match; add your own photo at", out); continue
        cands.sort(key=lambda c: -score(c, words))
        if lst:
            for c in cands[:8]: print(f"  {c['title']}  [{c['license']}] {c['w']}x{c['h']}")
        else:
            try: save(key, cands[0])
            except Exception as e: print("  download failed:", e)
        time.sleep(1)

if __name__ == "__main__":
    main()
