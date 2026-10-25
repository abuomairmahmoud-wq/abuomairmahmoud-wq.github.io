"""Build tall Pinterest pin images (1000x1500) for every product from its real cover image.
Usage: python _build/pins.py <out_dir> [local_cover_dir]
Writes <out_dir>/pins/<slug>.png. Never fails the site build: errors are printed and skipped."""
import io, json, os, sys, urllib.request

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("pins: Pillow not installed, skipping")
    sys.exit(0)

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "products.json"), encoding="utf-8"))
OUT = os.path.join(sys.argv[1] if len(sys.argv) > 1 else "_site", "pins")
LOCAL = sys.argv[2] if len(sys.argv) > 2 else None
IMG = "https://public-files.gumroad.com/"
W, H = 1000, 1500
NAVY, NAVY2, WHITE, GREY = (15, 23, 42), (30, 41, 59), (255, 255, 255), (203, 213, 225)
ACC = {"free": (34, 197, 94), "money": (34, 197, 94), "deals": (245, 158, 11), "business": (56, 189, 248),
       "life": (167, 139, 250), "work": (129, 140, 248), "home": (251, 113, 133), "creator": (244, 114, 182)}
FD = "/usr/share/fonts/truetype/dejavu/"


def font(bold, size):
    for n in (("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),):
        try:
            return ImageFont.truetype(FD + n, size)
        except OSError:
            pass
    return ImageFont.load_default()


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > maxw and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def cover(cid):
    if LOCAL and os.path.exists(os.path.join(LOCAL, cid)):
        return Image.open(os.path.join(LOCAL, cid)).convert("RGB")
    req = urllib.request.Request(IMG + cid, headers={"User-Agent": "Mozilla/5.0 LaunchKitPins"})
    return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=30).read())).convert("RGB")


def pin(p):
    acc = ACC.get(p.get("cat"), (34, 197, 94))
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    for y in range(H):  # vertical gradient
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(NAVY[i] + (NAVY2[i] - NAVY[i]) * t) for i in range(3)))
    free = p["price_cents"] == 0
    pw = p.get("pwyw")
    badge = "FREE TEMPLATE" if free else ("PAY WHAT YOU WANT" if pw else "EXCEL + GOOGLE SHEETS")
    fb = font(True, 30)
    bw = d.textlength(badge, font=fb) + 48
    d.rounded_rectangle([60, 60, 60 + bw, 118], 29, fill=acc)
    d.text((84, 72), badge, font=fb, fill=NAVY)
    title = p["h1"].split("(")[0].strip()
    y = 150
    for size in (78, 68, 60, 54):
        ft = font(True, size)
        lines = wrap(d, title, ft, 880)
        if len(lines) <= 3:
            break
    for ln in lines[:3]:
        d.text((60, y), ln, font=ft, fill=WHITE)
        y += int(size * 1.15)
    fs = font(False, 34)
    sub = p["bullets"][0] if p.get("bullets") else ""
    for ln in wrap(d, sub, fs, 880)[:2]:
        d.text((60, y + 10), ln, font=fs, fill=GREY)
        y += 46
    y += 40
    c = cover(p["cover"])
    cw = 900
    ch = int(c.height * cw / c.width)
    c = c.resize((cw, ch), Image.LANCZOS)
    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw, ch], 22, fill=255)
    d.rounded_rectangle([46, y - 4, 54 + cw, y + ch + 4], 26, fill=acc)
    im.paste(c, (50, y), mask)
    y += ch + 50
    fc = font(True, 30)
    y += 10
    for b in (p.get("bullets") or [])[1:5]:
        if y > H - 250:
            break
        txt = b
        while d.textlength(txt, font=fc) > 830 and " " in txt:
            txt = txt.rsplit(" ", 1)[0].rstrip(",;:-")
        d.text((60, y), "✓", font=fc, fill=acc)
        d.text((108, y), txt, font=fc, fill=(226, 232, 240))
        y += 62
    price = "FREE" if free else ("$0+" if pw else f"${p['price_cents'] / 100:.2f}")
    fp = font(True, 50)
    pw_ = d.textlength(price, font=fp) + 60
    d.rounded_rectangle([60, H - 150, 60 + pw_, H - 60], 20, fill=acc)
    d.text((90, H - 137), price, font=fp, fill=NAVY)
    d.text((100 + pw_, H - 128), "LaunchKit Labs · Instant download", font=font(True, 30), fill=(148, 163, 184))
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for p in D["products"]:
        try:
            pin(p).save(os.path.join(OUT, p["slug"] + ".png"), optimize=True)
            n += 1
        except Exception as e:  # keep the site build going
            print("pins: skip", p["slug"], e)
    print(f"pins: {n} images -> {OUT}")


if __name__ == "__main__":
    main()
