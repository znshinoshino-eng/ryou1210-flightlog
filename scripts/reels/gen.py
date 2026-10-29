"""Render a Flightlog Japan Instagram Reel (1080x1920, ~15 s, silent) from a JSON spec. Version 2.

Usage: python3 gen.py spec.json out.mp4
spec.json = {
  "kicker": "I work on Japan's railways",          # small yellow line above the hook (<= 30 chars)
  "hook":   "Kids ride *FREE* on Japan's trains?",  # big hook (<= 34 chars); *word* = yellow sign highlight
  "cards":  [["Ages 6-11 pay *half*", "Child fare on JR and Tokyo Metro"], ...],  # exactly 4 x [head <= 34, sub <= 48]
  "end":    ["Save this for your Japan trip", "Full guide: link in bio"],    # optional [big, small yellow]
  "photo":  "scripts/reels/photos/platform.jpg"     # optional; relative to the repo root; cover-cropped
}
Also writes <out>.contact.png (one frame per card, fully animated in) for a visual check.
Prints "WARN ..." if any text leaves the Instagram safe zone (x 65-960, y 270-1248).

Design (based on reel research, Oct 2026): hook text visible from frame 0, a cut every 2-3.5 s,
one idea per card, text kept inside Meta's 9:16 safe zone, constant motion (passing-train streaks,
scrolling tactile-paving strip, progress bar), text pop-in, and an end screen laid out like the hook so it loops.
The old 26 s slide style is kept in gen_classic.py.
"""
import json, math, os, random, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
SAFE_X0, SAFE_X1, SAFE_Y0, SAFE_Y1 = 65, 960, 270, 1248
X = 80  # text left edge
TEXT_W = SAFE_X1 - X
BG0, BG1 = (30, 33, 39), (12, 13, 15)
YEL, WHITE, GREY, INK = (245, 196, 0), (255, 255, 255), (196, 202, 210), (22, 23, 26)
FD = "/usr/share/fonts/opentype/inter/"
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def font(name, size):
    for p in (FD + name, "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# ---------- rich text: *highlight* words get a yellow station-sign box ----------
def tokens(text):
    """-> [(word, highlighted, glued_to_previous)]. Punctuation next to *...* stays outside the box."""
    out, hl = [], False
    for w in text.split():
        pre = post = ""
        m = re.match(r"^([^\w*¥$]*)\*(.*)$", w)
        opening = bool(m)
        if m:
            pre, w = m.group(1), m.group(2)
        m = re.match(r"^(.*?)\*([^\w*]*)$", w)
        closing = bool(m)
        if m:
            w, post = m.group(1), m.group(2)
        if pre:
            out.append((pre, False, False))
        if opening:
            hl = True
        if w:
            out.append((w, hl, bool(pre)))
        if post:
            out.append((post, False, True))
        if closing:
            hl = False
    return out


def layout(text, fnt, maxw):
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    sp = d.textlength(" ", font=fnt)
    lines, cur, cw = [], [], 0
    for w, hl, glue in tokens(text):
        tw = d.textlength(w, font=fnt) + (fnt.size * 0.36 if hl else 0)
        gap = 0 if (glue or not cur) else sp
        if cur and not glue and cw + gap + tw > maxw:
            lines.append(cur); cur, cw, gap = [], 0, 0
        cur.append((w, hl, tw, glue)); cw += gap + tw
    if cur:
        lines.append(cur)
    widest = max(sum(t[2] for t in l) + sp * sum(1 for t in l[1:] if not t[3]) for l in lines)
    return lines, widest


def fit(text, name, size, maxw, maxlines, minsize):
    while True:
        f = font(name, size)
        lines, widest = layout(text, f, maxw)
        if (len(lines) <= maxlines and widest <= maxw) or size <= minsize:
            return f, lines
        size -= 6


def draw_rich(d, lines, f, x, y, fill, lh=1.14):
    sp = d.textlength(" ", font=f)
    pad = f.size * 0.18
    asc = f.getbbox("Hg")[1]
    for ln in lines:
        cx = x
        for j, (w, hl, tw, glue) in enumerate(ln):
            if j and not glue:
                cx += sp
            if hl:
                d.rounded_rectangle([cx, y + asc - pad * 0.7, cx + tw, y + f.size * 1.08 + pad * 0.3],
                                    radius=int(f.size * 0.12), fill=YEL)
                d.text((cx + pad, y), w, font=f, fill=INK)
            else:
                d.text((cx, y), w, font=f, fill=fill)
            cx += tw
        y += int(f.size * lh)
    return y


# ---------- background ----------
def gradient():
    g = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / H
        g.putpixel((0, y), tuple(int(BG0[i] * (1 - t) + BG1[i] * t) for i in range(3)))
    return g.resize((W, H))


def paving_strip():
    s = Image.new("RGBA", (W + 120, 70), YEL + (255,))
    d = ImageDraw.Draw(s)
    for cx in range(20, W + 120, 40):
        for cy in (17, 52):
            d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(214, 168, 0, 255))
    return s


def photo_bg(path):
    im = Image.open(path).convert("RGB")
    sw, sh = int(W * 1.12), int(H * 1.12)
    r = max(sw / im.width, sh / im.height)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    l, t = (im.width - sw) // 2, (im.height - sh) // 2
    im = im.crop((l, t, l + sw, t + sh))
    shade = Image.new("L", (1, sh))
    for y in range(sh):  # darker where the text sits
        shade.putpixel((0, y), int(150 + 60 * math.sin(math.pi * min(1, y / sh * 1.3))))
    dark = Image.new("RGB", (sw, sh), BG1)
    return Image.composite(dark, im, shade.resize((sw, sh)))


class Background:
    def __init__(self, photo=None, seed=7):
        self.photo = photo_bg(photo) if photo and os.path.exists(photo) else None
        self.grad = gradient()
        self.strip = paving_strip()
        rnd = random.Random(seed)
        self.streaks = [(rnd.randint(190, 1700), rnd.randint(220, 900), rnd.choice([3, 4, 6]),
                         rnd.uniform(0.7, 1.6), rnd.random() * 3000, rnd.random() < 0.25) for _ in range(26)]

    def frame(self, t, i_card, rush):
        if self.photo:
            z = 1.04 + 0.03 * math.sin(t * 0.35 + i_card)  # always >= 1, so no black edges
            pw, ph = self.photo.size
            cw, ch = int(W * 1.12 / z), int(H * 1.12 / z)
            ox = (pw - cw) / 2 + 30 * math.sin(t * 0.25 + i_card * 1.7)
            ox = min(max(ox, 0), pw - cw)
            oy = (ph - ch) / 2
            im = self.photo.crop((int(ox), int(oy), int(ox) + cw, int(oy) + ch)).resize((W, H))
        else:
            im = self.grad.copy()
        im = im.convert("RGBA")
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        speed = 2600 if rush else 900
        for y, ln, th, sp, ph, yel in self.streaks:  # passing-train light streaks
            x = W + 200 - ((ph + t * speed * sp) % (W + ln + 400))
            a = (70 if not self.photo else 45) if not 440 < y < 1180 else 26  # faint behind the text
            d.rectangle([x, y, x + ln, y + th], fill=(YEL if yel else WHITE) + (a,))
        im.alpha_composite(lay)
        off = int((t * 60) % 40)
        im.alpha_composite(self.strip.crop((off, 0, off + W, 70)), (0, 1330))
        return im


# ---------- text layers ----------
def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def hook_layers(kicker, hook):
    a = layer(); d = ImageDraw.Draw(a)
    kf = font("Inter-ExtraBold.otf", 50)
    hf, lines = fit(hook, "InterDisplay-Black.otf", 132, TEXT_W, 4, 90)
    h = int(hf.size * 1.14) * len(lines)
    y0 = max(SAFE_Y0 + 150, int((SAFE_Y0 + SAFE_Y1) / 2 - h / 2))
    d.text((X, y0 - 95), kicker.upper(), font=kf, fill=YEL)
    yend = draw_rich(d, lines, hf, X, y0, WHITE)
    return [(a, (X, y0 - 95, yend))]


def card_layers(n, total, head, sub):
    a = layer(); d = ImageDraw.Draw(a)
    bf = font("InterDisplay-Black.otf", 110)
    d.rounded_rectangle([X, 470, X + 150, 620], radius=20, fill=YEL)
    d.text((X + 75 - d.textlength(str(n), font=bf) / 2, 478), str(n), font=bf, fill=INK)
    hf, lines = fit(head, "InterDisplay-Black.otf", 100, TEXT_W, 3, 70)
    yend = draw_rich(d, lines, hf, X, 675, WHITE)
    b = layer(); e = ImageDraw.Draw(b)
    sf, slines = fit(sub, "Inter-SemiBold.otf", 58, TEXT_W, 3, 44)
    y2 = yend + 40
    e.rectangle([X, y2, X + 120, y2 + 9], fill=YEL)
    y3 = draw_rich(e, slines, sf, X, y2 + 40, GREY, lh=1.25)
    return [(a, (X, 470, yend)), (b, (X, y2, y3))]


def end_layers(l1, l2):
    """Same layout as the hook (yellow line on top, big text centred) so the loop back to frame 0 is smooth."""
    a = layer(); d = ImageDraw.Draw(a)
    kf = font("Inter-ExtraBold.otf", 50)
    f1, lines = fit(l1, "InterDisplay-Black.otf", 132, TEXT_W, 4, 90)
    h = int(f1.size * 1.14) * len(lines)
    y0 = max(SAFE_Y0 + 150, int((SAFE_Y0 + SAFE_Y1) / 2 - h / 2))
    d.text((X, y0 - 95), l2.upper(), font=kf, fill=YEL)
    y = draw_rich(d, lines, f1, X, y0, WHITE)
    lf = font("InterDisplay-Black.otf", 60)
    yb = y + 40
    d.text((X, yb), "Flight", font=lf, fill=WHITE)
    d.text((X + d.textlength("Flight", font=lf), yb), "log", font=lf, fill=YEL)
    d.text((X + d.textlength("Flightlog ", font=lf), yb + 10), "JAPAN", font=font("Inter-Bold.otf", 44), fill=GREY)
    return [(a, (X, y0 - 95, yb + 75))]


def pop(lay, k):
    """k: 0..1 animation progress -> scale 1.10->1.0 and slide up 40px, alpha in."""
    if k >= 1:
        return lay, (0, 0)
    e = 1 - (1 - k) ** 3
    s = 1.10 - 0.10 * e
    w, h = int(W * s), int(H * s)
    im = lay.resize((w, h), Image.BILINEAR)
    al = im.getchannel("A").point(lambda v: int(v * min(1, 0.25 + e)))
    im.putalpha(al)
    ox = int(X - X * s)  # keep the left edge anchored
    oy = int((H - h) / 2 + 40 * (1 - e))
    return im, (ox, oy)


def comp(base, lay, xy):
    ox, oy = xy
    cl = lay.crop((max(0, -ox), max(0, -oy), min(lay.width, W - ox), min(lay.height, H - oy)))
    base.alpha_composite(cl, (max(ox, 0), max(oy, 0)))


def render(spec, out):
    cards = spec["cards"]
    assert len(cards) == 4, "need exactly 4 cards"
    end = spec.get("end") or ["Save this for your Japan trip", "Full guide: link in bio"]
    segs = [("hook", 2.4, hook_layers(spec.get("kicker", "I work on Japan's railways"), spec["hook"]))]
    for i, (head, sub) in enumerate(cards, 1):
        words = len(head.split()) + len(sub.split())
        segs.append(("card", max(2.4, min(3.0, 1.2 + 0.18 * words)), card_layers(i, len(cards), head, sub)))
    segs.append(("end", 2.4, end_layers(*end)))

    for kind, _, lays in segs:
        for _, (x0, y0, y1) in lays:
            if y0 < SAFE_Y0 or y1 > SAFE_Y1:
                print(f"WARN {kind}: text spans y {y0}-{y1}, outside safe zone {SAFE_Y0}-{SAFE_Y1}")
        for lay, _ in lays:
            bb = lay.getbbox()
            if bb and (bb[2] > SAFE_X1 + 25 or bb[0] < SAFE_X0):
                print(f"WARN {kind}: text spans x {bb[0]}-{bb[2]}, outside safe zone {SAFE_X0}-{SAFE_X1}")

    total = sum(s[1] for s in segs)
    photo = spec.get("photo")
    if photo and not os.path.isabs(photo) and not os.path.exists(photo):
        photo = os.path.join(REPO, photo)  # allow paths relative to the repo root
    if photo and not os.path.exists(photo):
        print(f"WARN photo not found: {spec.get('photo')} (using the plain background)")
        photo = None
    bg = Background(photo)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo",
                           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                           "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-movflags", "+faststart", out],
                          stdin=subprocess.PIPE)
    shots, t0, n_cards = [], 0.0, len(cards)
    for si, (kind, dur, lays) in enumerate(segs):
        nf = int(round(dur * FPS))
        for fi in range(nf):
            lt = fi / FPS
            t = t0 + lt
            im = bg.frame(t, si, rush=(kind == "hook" and lt < 0.6))
            d = ImageDraw.Draw(im, "RGBA")
            # progress bar inside the safe zone
            d.rectangle([SAFE_X0, 285, SAFE_X1, 295], fill=(255, 255, 255, 60))
            d.rectangle([SAFE_X0, 285, SAFE_X0 + (SAFE_X1 - SAFE_X0) * (t / total), 295], fill=YEL)
            if kind == "card":
                d.text((SAFE_X1 - 90, 315), f"{si}/{n_cards}", font=font("Inter-ExtraBold.otf", 44), fill=GREY)
            for li, (lay, _) in enumerate(lays):
                start = 0.0 if kind == "hook" else 0.05 + 0.35 * li
                # the hook is already readable on frame 0 (it is also the cover); it just settles in
                k = 0.55 + lt / 0.35 if kind == "hook" else (lt - start) / 0.28
                if k <= 0:
                    continue
                pl, xy = pop(lay, min(1, k))
                comp(im, pl, xy)
            ff.stdin.write(im.convert("RGB").tobytes())
            if fi == nf - 1:
                shots.append(im.convert("RGB").resize((270, 480)))
        t0 += dur
    ff.stdin.close(); ff.wait()
    if ff.returncode:
        raise SystemExit("ffmpeg failed")
    c = Image.new("RGB", (270 * len(shots), 480))
    for i, s in enumerate(shots):
        c.paste(s, (i * 270, 0))
    c.save(out + ".contact.png")
    print(f"{out}  ({total:.1f} s)")


if __name__ == "__main__":
    render(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
