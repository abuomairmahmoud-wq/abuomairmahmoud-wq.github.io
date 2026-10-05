import os, sys, json, html, shutil, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json as _j
_D=_j.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'products.json'),encoding='utf-8'))
P=[(p['slug'],p['title'],p['cat'],p['price_cents'],p['cover'],p['h1'],p['desc'],p['bullets']) for p in _D['products']]
CATS=[(c['id'],c['name'],c['desc']) for c in _D['categories']]
from guides import G
from tools import T, TOOL_CSS
KOFI = _D.get('kofi', '')

BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else "https://abuomairmahmoud-wq.github.io"
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_site")
GUM = "https://mahmoudian113.gumroad.com/l/"
IMG = "https://public-files.gumroad.com/"
TODAY = datetime.date.today().isoformat()
E = html.escape
BYSLUG = {p[0]: p for p in P}
CATNAME = {c[0]: c[1] for c in CATS}


def short(t, n):
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0].rstrip(',;:') + '...'


def price(c):
    return "Free" if c == 0 else f"${c/100:.2f}"


def is_excel(p):
    t = (p[1] + p[5] + p[6]).lower()
    return ("excel" in t or "spreadsheet" in t) and "word" not in t and "flutter" not in t and "binder" not in t


CSS = """:root{--bg:#f8fafc;--card:#fff;--ink:#0f172a;--mut:#475569;--line:#e2e8f0;--acc:#16a34a;--acc2:#0f172a;--hl:#fef3c7}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}
a{color:#0b63c5}img{max-width:100%;height:auto;display:block}
header{background:var(--acc2);color:#fff}header .w{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 16px;flex-wrap:wrap}
header a{color:#fff;text-decoration:none}.logo{font-weight:800;font-size:20px}nav a{margin-left:16px;font-size:15px;opacity:.9}
.w{max-width:1100px;margin:0 auto;padding:0 16px}
.hero{background:linear-gradient(135deg,#0f172a,#1e293b);color:#fff;padding:48px 0 40px}.hero h1{font-size:clamp(28px,4vw,42px);margin:0 0 12px;line-height:1.2}.hero p{color:#cbd5e1;font-size:18px;max-width:720px;margin:0 0 20px}
.btn{display:inline-block;background:var(--acc);color:#fff;padding:12px 22px;border-radius:10px;font-weight:700;text-decoration:none}.btn:hover{filter:brightness(1.08)}.btn.ghost{background:transparent;border:2px solid #fff;margin-left:8px}
h2{font-size:26px;margin:40px 0 6px}.sub{color:var(--mut);margin:0 0 18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;text-decoration:none;color:inherit;transition:transform .15s,box-shadow .15s}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(15,23,42,.08)}.card img{aspect-ratio:16/9;object-fit:cover;background:#e2e8f0}
.card .b{padding:12px 14px 16px;display:flex;flex-direction:column;gap:6px;flex:1}.card h3{font-size:16px;margin:0;line-height:1.35}.card .pr{font-weight:800;color:var(--acc)}
.tag{display:inline-block;background:var(--hl);color:#92400e;font-size:12px;font-weight:700;padding:2px 8px;border-radius:99px}
.prod{display:grid;grid-template-columns:1.2fr 1fr;gap:32px;padding:32px 0}@media(max-width:800px){.prod{grid-template-columns:1fr}nav a{margin-left:10px}}
.prod h1{font-size:clamp(24px,3.2vw,34px);line-height:1.25;margin:0 0 10px}.prod .big{font-size:30px;font-weight:800;color:var(--acc);margin:8px 0 16px}
.box{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px}ul.ck{list-style:none;padding:0;margin:0}ul.ck li{padding:6px 0 6px 28px;position:relative}ul.ck li:before{content:"\\2713";position:absolute;left:0;color:var(--acc);font-weight:900}
.crumb{font-size:14px;color:var(--mut);padding-top:18px}.crumb a{color:var(--mut)}
.faq h3{font-size:17px;margin:18px 0 4px}.faq p{margin:0;color:var(--mut)}
article{max-width:760px;margin:0 auto;padding:32px 16px}article h1{font-size:clamp(26px,3.6vw,38px);line-height:1.2}article h2{font-size:22px;margin-top:28px}
.cta{background:#ecfdf5;border:1px solid #bbf7d0;border-radius:14px;padding:20px;margin:28px 0}.cta h3{margin:0 0 6px}
footer{background:var(--acc2);color:#94a3b8;margin-top:56px;padding:28px 0;font-size:14px}footer a{color:#cbd5e1}
.trust{display:flex;gap:18px;flex-wrap:wrap;color:#cbd5e1;font-size:15px;margin-top:18px}"""


def page(path, title, desc, body, canon=None, img=None, jsonld=None, typ="website"):
    canon = canon or (BASE + "/" + path.replace("index.html", ""))
    img = img or (IMG + P[0][4])
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j)}</script>' for j in (jsonld or []))
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{canon}">
<meta property="og:type" content="{typ}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{img}"><meta property="og:site_name" content="LaunchKit Labs">
<meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="{rel(path)}style.css">{ld}</head><body>
<header><div class="w"><a class="logo" href="{rel(path)}">LaunchKit Labs</a><nav><a href="{rel(path)}tools/">Free calculators</a><a href="{rel(path)}free/">Free templates</a><a href="{rel(path)}#all">All templates</a><a href="{rel(path)}guides/">Guides</a></nav></div></header>
{body}
<footer><div class="w"><p><strong style="color:#fff">LaunchKit Labs</strong>: practical Excel templates, planners and calculators. Instant download, no subscriptions.</p>
<p><a href="{rel(path)}tools/">Free calculators</a> · <a href="{rel(path)}free/">Free templates</a> · <a href="{rel(path)}guides/">Guides</a> · <a href="https://mahmoudian113.gumroad.com" rel="noopener">Shop on Gumroad</a> · <a href="https://payhip.com/BestLaunchKitLabs" rel="noopener">Payhip store</a></p>
{('<p><a class="kofi" href="'+KOFI+'" rel="noopener">☕ Support LaunchKit Labs on Ko-fi</a></p>') if KOFI else ''}
<p>Templates are planning tools, not financial, legal, tax or medical advice. © {datetime.date.today().year} LaunchKit Labs</p></div></footer></body></html>"""
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(doc)


def rel(path):
    d = path.count("/")
    return "../" * d if d else "./"


def card(p, pre):
    tag = '<span class="tag">FREE</span>' if p[3] == 0 else ""
    return f"""<a class="card" href="{pre}{p[0]}/"><img loading="lazy" src="{IMG}{p[4]}" alt="{E(p[1])} Excel template preview" width="640" height="360">
<div class="b">{tag}<h3>{E(p[1])}</h3><span class="pr">{price(p[3])}</span></div></a>"""


def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    open(os.path.join(OUT, "style.css"), "w").write(CSS + "\n" + TOOL_CSS)
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    for f in os.listdir(root):
        if f.startswith("google") and f.endswith(".html"):
            shutil.copy(os.path.join(root, f), os.path.join(OUT, f))
    urls = []

    # ---------- home ----------
    secs = ""
    for cid, cname, cdesc in CATS:
        items = [p for p in P if p[2] == cid]
        if not items:
            continue
        anchor = ' id="all"' if cid == "deals" else ""
        secs += f'<section{anchor}><h2 id="{cid}">{E(cname)}</h2><p class="sub">{E(cdesc)}</p><div class="grid">{"".join(card(p, "") for p in items)}</div></section>'
    guides = "".join(f'<li><a href="guides/{g[0]}/">{E(g[1])}</a></li>' for g in G)
    tl = "".join(f'<li><a href="tools/{t[0]}/">{E(t[1])}</a></li>' for t in T)
    body = f"""<section class="hero"><div class="w"><h1>Excel Templates for Budgets, Deals, Small Business &amp; Life Planning</h1>
<p>Ready-to-use spreadsheets that do the math for you: budget planners, Black Friday deal trackers, grocery price books, car loan calculators, invoice trackers and more. Built for the USA, UK and Canada.</p>
<a class="btn" href="free/">Get free templates</a><a class="btn ghost" href="#all">Browse all</a>
<div class="trust"><span>✓ Instant download</span><span>✓ No subscription</span><span>✓ Works in Microsoft Excel</span><span>✓ Sample data included</span></div></div></section>
<main class="w"><section><h2 id="tools">Free online calculators</h2><p class="sub">Quick answers in your browser, no download needed.</p><ul>{tl}</ul></section>{secs}<section><h2>Free money-saving guides</h2><ul>{guides}</ul></section></main>"""
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "LaunchKit Labs", "url": BASE + "/",
           "sameAs": ["https://mahmoudian113.gumroad.com", "https://payhip.com/BestLaunchKitLabs", "https://contra.com/mahmoud_abuomair_7sxshnhl"]}
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "LaunchKit Labs", "url": BASE + "/"}
    page("index.html", "Excel Templates: Budget, Deal Tracker & Small Business Spreadsheets | LaunchKit Labs",
         "Practical Excel templates: free budget spreadsheet, Black Friday deal planner, grocery unit price calculator, car deal analyzer, invoice trackers and more. Instant download.",
         body, jsonld=[org, site])
    urls.append(BASE + "/")

    # ---------- free page ----------
    fr = [p for p in P if p[3] == 0]
    body = f"""<section class="hero"><div class="w"><h1>Free Excel Templates</h1><p>Download free spreadsheets for budgeting, Black Friday shopping, grocery savings and small business. No cost, instant download.</p></div></section>
<main class="w"><h2>Free downloads</h2><div class="grid">{"".join(card(p, "../") for p in fr)}</div></main>"""
    page("free/index.html", "Free Excel Templates: Budget, Black Friday & Grocery Spreadsheets | LaunchKit Labs",
         "Free Excel templates to download: simple monthly budget, Black Friday wishlist and price checker, grocery unit price calculator and small business starter pack.", body)
    urls.append(BASE + "/free/")

    # ---------- product pages ----------
    for p in P:
        slug, name, cat, cents, img, kw, desc, bullets = p
        path = f"{slug}/index.html"
        link = GUM + slug
        rel_items = [q for q in P if q[2] == cat and q[0] != slug][:4]
        if len(rel_items) < 4:
            rel_items += [q for q in P if q[3] == 0 and q[0] != slug and q not in rel_items][:4 - len(rel_items)]
        faqs = [("How do I get it?", "Click the button to open the secure checkout on Gumroad. You get the download link instantly by email and on screen." if cents else "Click the button, enter your email on Gumroad and download it instantly. It is completely free."),
                ("Is this a subscription?", "No. It is a one-time download with no monthly fees." if cents else "No. It is free, with no subscription.")]
        if is_excel(p):
            faqs.append(("What do I need to use it?", "Microsoft Excel. The file is a standard .xlsx workbook with no macros and includes sample data so you can see how it works."))
            faqs.append(("Can I edit it?", "Yes. Yellow input cells are for your own data, and categories and labels can be changed to fit you."))
        faqhtml = "".join(f"<h3>{E(q)}</h3><p>{E(a)}</p>" for q, a in faqs)
        btn = "Download free" if cents == 0 else f"Buy now: {price(cents)}"
        body = f"""<main class="w"><div class="crumb"><a href="../">Home</a> › <a href="../#{cat}">{E(CATNAME[cat])}</a> › {E(name)}</div>
<div class="prod"><div><img src="{IMG}{img}" alt="{E(name)} preview" width="1280" height="720" style="border-radius:14px;border:1px solid var(--line)"></div>
<div><h1>{E(kw)}</h1><div class="big">{price(cents)}</div><p>{E(desc)}</p><a class="btn" href="{link}" rel="noopener">{btn}</a>
<p style="color:var(--mut);font-size:14px;margin-top:10px">Instant download · Secure checkout on Gumroad</p></div></div>
<div class="prod" style="padding-top:0"><div class="box"><h2 style="margin-top:0">What's included</h2><ul class="ck">{"".join(f"<li>{E(b)}</li>" for b in bullets)}</ul></div>
<div class="box faq"><h2 style="margin-top:0">Questions</h2>{faqhtml}</div></div>
<h2>You may also like</h2><div class="grid">{"".join(card(q, "../") for q in rel_items)}</div></main>"""
        prod = {"@context": "https://schema.org", "@type": "Product", "name": name, "description": desc, "image": IMG + img,
                "brand": {"@type": "Brand", "name": "LaunchKit Labs"}, "url": BASE + f"/{slug}/",
                "offers": {"@type": "Offer", "price": f"{cents/100:.2f}", "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": link}}
        faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
        crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": BASE + f"/{slug}/"}]}
        t = f"{kw} | LaunchKit Labs"
        if len(t) > 70:
            t = kw
        md = (desc[:150].rsplit(" ", 1)[0] + "...") if len(desc) > 155 else desc
        page(path, t, md, body, img=IMG + img, jsonld=[prod, faq, crumbs], typ="product")
        urls.append(BASE + f"/{slug}/")

    # ---------- guides ----------
    gl = ""
    for slug, title, desc, free_slug, paid_slug, content in G:
        f, pd = BYSLUG[free_slug], BYSLUG[paid_slug]
        body = f"""<article><div class="crumb"><a href="../../">Home</a> › <a href="../">Guides</a></div><h1>{E(title)}</h1>{content}
<div class="cta"><h3>Free download: {E(f[1])}</h3><p>{E(short(f[6], 180))}</p><a class="btn" href="../../{f[0]}/">Get it free</a></div>
<div class="cta" style="background:#eff6ff;border-color:#bfdbfe"><h3>Want the full version? {E(pd[1])}</h3><p>{E(short(pd[6], 180))}</p><a class="btn" href="../../{pd[0]}/">See {E(pd[1])}: {price(pd[3])}</a></div></article>"""
        art = {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc, "datePublished": TODAY, "dateModified": TODAY,
               "author": {"@type": "Organization", "name": "LaunchKit Labs"}, "publisher": {"@type": "Organization", "name": "LaunchKit Labs"}, "image": IMG + pd[4]}
        page(f"guides/{slug}/index.html", title, desc, body, img=IMG + pd[4], jsonld=[art], typ="article")
        urls.append(BASE + f"/guides/{slug}/")
        gl += f'<li style="margin:10px 0"><a href="{slug}/"><strong>{E(title)}</strong></a><br><span style="color:var(--mut)">{E(desc)}</span></li>'
    page("guides/index.html", "Money-Saving Guides: Budgeting, Deals & Grocery Savings | LaunchKit Labs",
         "Free step-by-step guides: spot fake Black Friday deals, calculate grocery unit prices, make a monthly budget, debt snowball vs avalanche and lease vs buy a car.",
         f'<article><h1>Money-Saving Guides</h1><ul style="list-style:none;padding:0">{gl}</ul></article>')
    urls.append(BASE + "/guides/")


    # ---------- tools ----------
    tlist = ""
    for slug, title, h1, desc, intro, tool, paid_slug, free_slug in T:
        pd, f = BYSLUG[paid_slug], BYSLUG[free_slug]
        kofi = f'<p class="mut">Found this useful? <a href="{KOFI}" rel="noopener">Buy me a coffee on Ko-fi</a>.</p>' if KOFI else ""
        body = f"""<article><div class="crumb"><a href="../../">Home</a> \u203a <a href="../">Free calculators</a></div><h1>{E(h1)}</h1>{intro}{tool}
<div class="cta" style="background:#eff6ff;border-color:#bfdbfe"><h3>Want to track this every week? {E(pd[1])}</h3><p>{E(short(pd[6], 200))}</p><a class="btn" href="../../{pd[0]}/">See {E(pd[1])}: {price(pd[3])}</a></div>
<div class="cta"><h3>Free download: {E(f[1])}</h3><p>{E(short(f[6], 160))}</p><a class="btn" href="../../{f[0]}/">Get it free</a></div>{kofi}</article>"""
        app = {"@context": "https://schema.org", "@type": "WebApplication", "name": title, "url": BASE + f"/tools/{slug}/", "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": desc}
        page(f"tools/{slug}/index.html", f"{h1} | Free", desc, body, img=IMG + pd[4], jsonld=[app], typ="website")
        urls.append(BASE + f"/tools/{slug}/")
        tlist += f'<li style="margin:10px 0"><a href="{slug}/"><strong>{E(h1)}</strong></a><br><span style="color:var(--mut)">{E(desc)}</span></li>'
    page("tools/index.html", "Free Online Money Calculators: Budget, Debt, Mortgage, Car & Grocery | LaunchKit Labs",
         "Free calculators: grocery unit price, Black Friday countdown, lease vs buy, debt snowball vs avalanche, mortgage payment and 50/30/20 budget.",
         f'<article><h1>Free Online Money Calculators</h1><p>No sign-up, no download. Your numbers stay in your browser.</p><ul style="list-style:none;padding:0">{tlist}</ul></article>')
    urls.append(BASE + "/tools/")

    # ---------- 404, robots, sitemap ----------
    page("404.html", "Page not found | LaunchKit Labs", "Page not found.", '<article><h1>Page not found</h1><p><a href="/">Go to the home page</a></p></article>', canon=BASE + "/")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    return urls


if __name__ == "__main__":
    u = build()
    print(len(u), "pages ->", OUT)
