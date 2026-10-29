"""Render a Flightlog Japan Instagram Reel (1080x1920, silent) from a JSON spec.

Usage: python3 gen.py spec.json out.mp4
spec.json = {"hook": ["kicker", "title", "sub"],
             "tips": [["head", "body", "note"], ... exactly 5 ...]}
Also writes <out>.contact.png (all slides side by side) for a quick visual check.
Style: black/yellow station-sign look matching the site. Audio is silent;
the owner adds trending audio in Instagram.
"""
from PIL import Image, ImageDraw, ImageFont
import json, os, subprocess, sys, tempfile

W, H = 1080, 1920
SIGN, SIGN2, YEL, WHITE, GREY = "#1b1d20", "#2a2d32", "#f5c400", "#ffffff", "#b9c0c8"
BLACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"
f = lambda p, s: ImageFont.truetype(p, s)


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def block(d, y, text, font, fill, maxw=900, gap=1.18, x=90):
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += int(font.size * gap)
    return y


def base(n=None):
    im = Image.new("RGB", (W, H), SIGN)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 170], fill=SIGN2)
    d.rectangle([0, 170, W, 182], fill=YEL)
    lf = f(BLACK, 62)
    d.text((90, 52), "Flight", font=lf, fill=WHITE)
    x = 90 + d.textlength("Flight", font=lf)
    d.text((x, 52), "log", font=lf, fill=YEL)
    x += d.textlength("log", font=lf)
    d.text((x + 16, 64), "JAPAN", font=f(BOLD, 44), fill=GREY)
    if n:
        d.text((W - 230, 66), f"{n} / 5", font=f(BOLD, 46), fill=YEL)
    d.rectangle([0, H - 110, W, H], fill=YEL)
    d.text((90, H - 86), "Free Japan travel guides  →  link in bio", font=f(BOLD, 44), fill=SIGN)
    return im, d


def hook(kicker, title, sub):
    im, d = base()
    d.text((90, 470), kicker, font=f(BOLD, 64), fill=GREY)
    y = block(d, 570, title, f(BLACK, 112), WHITE, gap=1.1)
    d.rectangle([90, y + 30, 1000, y + 40], fill=YEL)
    y = block(d, y + 90, sub, f(BLACK, 84), YEL, gap=1.12)
    block(d, y + 80, "From someone who works on Japan's railways", f(REG, 50), GREY, gap=1.3)
    return im


def tip(n, head, body, note):
    im, d = base(n)
    d.rounded_rectangle([90, 400, 330, 640], radius=22, fill=YEL)
    nf = f(BLACK, 190)
    d.text((210 - d.textlength(str(n), font=nf) / 2, 380), str(n), font=nf, fill=SIGN)
    y = block(d, 740, head, f(BLACK, 90), WHITE, gap=1.12)
    d.rectangle([90, y + 40, 250, y + 50], fill=YEL)
    y = block(d, y + 100, body, f(REG, 52), GREY, gap=1.35)
    nfnt = f(BOLD, 48)
    nl = len(wrap(d, note, nfnt, 820))
    d.rounded_rectangle([90, y + 60, 990, y + 60 + 70 + nl * 58], radius=18, outline=YEL, width=5)
    block(d, y + 92, note, nfnt, YEL, maxw=820, gap=1.2, x=128)
    return im


def outro():
    im, d = base()
    d.text((90, 330), "More free guides on", font=f(BOLD, 60), fill=GREY)
    bf = f(BLACK, 150)
    d.text((90, 410), "Flight", font=bf, fill=WHITE)
    d.text((90 + d.textlength("Flight", font=bf), 410), "log", font=bf, fill=YEL)
    d.text((90, 640), "JAPAN", font=f(BOLD, 96), fill=GREY)
    d.rectangle([90, 790, 250, 800], fill=YEL)
    y = 860
    for item in ["Airport to city: Narita, Haneda, Kansai", "Shinkansen & rail passes",
                 "Suica, PASMO & tap-to-pay", "Tokyo, Kyoto, Osaka & Mt. Fuji trips"]:
        d.rectangle([90, y + 22, 112, y + 44], fill=YEL)
        y = block(d, y, item, f(BOLD, 54), WHITE, maxw=860, gap=1.25, x=140) + 22
    block(d, y + 20, "Written by someone who works on Japan's railways", f(REG, 46), GREY, gap=1.3)
    d.rounded_rectangle([90, 1520, 990, 1690], radius=85, fill=YEL)
    t, tf = "Link in bio  →", f(BLACK, 76)
    d.text((540 - d.textlength(t, font=tf) / 2, 1550), t, font=tf, fill=SIGN)
    return im


def render(spec, out):
    k, t, s = spec["hook"]
    tips = spec["tips"]
    assert len(tips) == 5, "need exactly 5 tips"
    work = tempfile.mkdtemp()
    slides = [(hook(k, t, s), 3.0)] + [(tip(i, *x), 4.2) for i, x in enumerate(tips, 1)] + [(outro(), 4.5)]
    files = []
    for i, (im, dur) in enumerate(slides):
        p = os.path.join(work, f"s{i}.png"); im.save(p); files.append((p, dur))
    FPS, X = 30, 0.4
    inputs, filt = [], []
    for i, (p, dur) in enumerate(files):
        inputs += ["-loop", "1", "-t", str(dur), "-i", p]
        filt.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(1+0.0009*on,1.1)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={int(dur*FPS)}:s={W}x{H}:fps={FPS},format=yuv420p[v{i}]")
    prev, off = "v0", 0.0
    for i in range(1, len(files)):
        off += files[i - 1][1] - X
        filt.append(f"[{prev}][v{i}]xfade=transition=slideleft:duration={X}:offset={off:.2f}[x{i}]")
        prev = f"x{i}"
    total = sum(x[1] for x in files) - X * (len(files) - 1)
    subprocess.run(["ffmpeg", "-y", *inputs, "-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo",
                    "-filter_complex", ";".join(filt), "-map", f"[{prev}]", "-map", f"{len(files)}:a",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-shortest",
                    "-movflags", "+faststart", out], check=True, capture_output=True)
    ims = [Image.open(p).resize((270, 480)) for p, _ in files]
    c = Image.new("RGB", (270 * len(ims), 480))
    for i, im in enumerate(ims): c.paste(im, (i * 270, 0))
    c.save(out + ".contact.png")
    print(out)


if __name__ == "__main__":
    render(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
