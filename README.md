# AGRIVA website

Static site (HTML, CSS, vanilla JS). No framework, no build step needed to run it.

**Pages:** Home · Shop · Product (one template, `product.html?product=<id>`) · Our Story · Contact · Customer information, plus `404.html`.

## 1. Add the photos (once)
Image hosts are not reachable from every environment, so photos are fetched by a script you run on your own machine:

```bash
python3 tools/fetch_images.py            # downloads open-licence photos from Wikimedia Commons
python3 tools/fetch_images.py --list almonds                       # see candidates
python3 tools/fetch_images.py --pick almonds "File:Name.jpg"       # choose one yourself
```
Photos land in `assets/products/<id>.jpg` and `assets/img/*.jpg`; credits are written to `assets/credits.json` and shown on the Customer information page. **Check every photo.** Best of all: drop in your own product shots using the same file names. Until an image exists, a clean tinted label tile is shown instead.

### Use image URLs directly (hotlink, no downloads)
Paste direct image links into `images.js` (keys: `hero`, `oils`, `dryfruits`, `story`, and each product id), or generate the file:
```bash
export PEXELS_API_KEY=your_key
python3 tools/fetch_pexels.py --urls
```
Each image tries its URL first, then the local file, then a label tile.

### Better matched photos from Pexels (recommended)
Get a free key at pexels.com/api, then:
```bash
export PEXELS_API_KEY=your_key
python3 tools/fetch_pexels.py --review     # open tools/review.html, pick the right photo per product
python3 tools/fetch_pexels.py --pick almonds <photo-id>
```

## Motion
`fx.js` adds a scroll progress line, headline reveal, 3D hero tilt, card tilt with glare, parallax photos and magnetic buttons. It switches off for visitors who prefer reduced motion and skips pointer effects on touch devices.

## 2. Configure
Edit `site-config.js`: set `whatsappNumber` (digits only, e.g. `919876543210`), and optionally email, phone, address, hours.
Edit `catalog.js` to change products. Leave `price` empty to show "Price on enquiry".

## 3. Set your domain, then deploy
```bash
python3 tools/build.py --domain https://www.yourdomain.com   # regenerates pages, sitemap.xml, robots.txt
```
Upload the folder to Netlify (drag and drop, `netlify.toml` included), Cloudflare Pages, GitHub Pages or any static host.

## 4. Before going live
- Replace the draft text in `policies.html` (edit in `tools/build.py`, then rebuild) with approved policies.
- Confirm product claims (origin, grade, allergens) against labels. None are made on the site.

## Notes
- Basket is stored in the visitor's browser only. Checkout hands a message to WhatsApp; no payments are processed.
- Local preview: `python3 -m http.server 8000`.
- The earlier local-only admin prototype was removed from this build; it wasn't secure enough to ship.
