#!/usr/bin/env python3
"""Draw the 24 Nov 2026 world-news front page, 1024x1024.

Rendered at 2x supersampling with PIL, then downscaled, for crisp text.
Story data lives in stories.py (numbered 1..36). Illustrations are simple
flat original drawings keyed by each story's "art" field.
"""
from PIL import Image, ImageDraw, ImageFont
import stories as S

SS = 2
W = H = 1024 * SS
PAPER = (250, 246, 233)
INK = (17, 17, 17)
RED = (178, 26, 26)
DARKRED = (140, 20, 20)
NAVY = (18, 38, 74)
GREY = (96, 92, 84)
LGREY = (214, 208, 192)
GREEN = (18, 110, 60)
GOLD = (196, 138, 20)
TEAL = (14, 110, 120)
PURPLE = (96, 52, 140)
ORANGE = (214, 106, 20)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, int(size * SS))


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def X(v):
    return v * SS


def rect(box, **kw):
    if "width" in kw:
        kw["width"] = max(1, int(kw["width"] * SS))
    d.rectangle([X(box[0]), X(box[1]), X(box[2]), X(box[3])], **kw)


def line(pts, **kw):
    if "width" in kw:
        kw["width"] = int(kw["width"] * SS)
    d.line([(X(x), X(y)) for x, y in pts], **kw)


def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((X(x), X(y)), s, font=font, fill=fill, anchor=anchor)


def tlen(s, font):
    return d.textlength(s, font=font) / SS


def wrap(s, font, width):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tlen(t, font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x, y, s, font, width, fill=INK, leading=3, max_lines=None):
    lines = wrap(s, font, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = font.size / SS + leading
    for ln in lines:
        text(x, y, ln, font, fill)
        y += lh
    return y


def chip(x, y, s, fill, font=None, fg=(255, 255, 255), pad=5):
    font = font or F(SANS_B, 10)
    w = tlen(s, font) + pad * 2
    rect([x, y, x + w, y + 15], fill=fill)
    text(x + pad, y + 2.5, s, font, fg)
    return w


def tag(x, y, s):
    """small outlined certainty tag, right-aligned at x"""
    font = F(SANS_B, 8.5)
    w = tlen(s, font) + 8
    rect([x - w, y, x, y + 12], outline=GREY, width=1)
    text(x - w + 4, y + 2, s, font, GREY)
    return w


# ---------------------------------------------------------------- arts
def art(kind, x, y, w, h):
    """flat original mini-illustration inside box (x,y,w,h), clipped by caller bg"""
    cx, cy = x + w / 2, y + h / 2
    if kind == "chart_down":
        rect([x, y, x + w, y + h], fill=(16, 26, 48))
        pts = [(x + 8, y + h * 0.28), (x + w * 0.3, y + h * 0.4), (x + w * 0.48, y + h * 0.34),
               (x + w * 0.68, y + h * 0.62), (x + w * 0.9, y + h * 0.78)]
        line(pts, fill=(255, 92, 82), width=3)
        for i in range(5):
            gx = x + 12 + i * (w - 24) / 4
            line([(gx, y + 6), (gx, y + h - 6)], fill=(52, 72, 110), width=1)
        d.polygon([(X(pts[-1][0]), X(pts[-1][1])), (X(pts[-1][0] - 12), X(pts[-1][1] - 3)),
                   (X(pts[-1][0] - 3), X(pts[-1][1] + 10))], fill=(255, 92, 82))
    elif kind == "chart_up":
        rect([x, y, x + w, y + h], fill=(14, 44, 34))
        pts = [(x + 8, y + h * 0.75), (x + w * 0.3, y + h * 0.6), (x + w * 0.5, y + h * 0.66),
               (x + w * 0.72, y + h * 0.34), (x + w * 0.9, y + h * 0.2)]
        line(pts, fill=(74, 222, 128), width=3)
    elif kind == "chip":
        rect([x, y, x + w, y + h], fill=(18, 30, 58))
        rect([cx - 26, cy - 20, cx + 26, cy + 20], fill=(24, 148, 96), outline=(140, 230, 190), width=2)
        for i in range(-2, 3):
            line([(cx + i * 11, cy - 28), (cx + i * 11, cy - 20)], fill=(200, 210, 220), width=2)
            line([(cx + i * 11, cy + 20), (cx + i * 11, cy + 28)], fill=(200, 210, 220), width=2)
        rect([cx - 12, cy - 9, cx + 12, cy + 9], outline=(220, 255, 240), width=2)
    elif kind == "tower":
        rect([x, y, x + w, y + h], fill=(24, 30, 52))
        rect([cx - 15, y + 10, cx + 15, y + h - 8], fill=(70, 84, 112))
        for r in range(4):
            for c in range(2):
                rect([cx - 10 + c * 12, y + 16 + r * 13, cx - 3 + c * 12, y + 23 + r * 13], fill=(250, 204, 84))
        d.polygon([(X(cx - 22), X(y + h - 6)), (X(cx + 26), X(y + 16)), (X(cx + 30), X(y + h - 6))],
                  fill=(214, 84, 40))
        d.ellipse([X(cx + 16), X(y + 8), X(cx + 34), X(y + 26)], fill=(120, 124, 132))
    elif kind == "ship":
        rect([x, y, x + w, y + h], fill=(26, 54, 92))
        rect([x, y + h * 0.62, x + w, y + h], fill=(18, 84, 130))
        d.polygon([(X(x + w * 0.2), X(y + h * 0.62)), (X(x + w * 0.82), X(y + h * 0.62)),
                   (X(x + w * 0.72), X(y + h * 0.78)), (X(x + w * 0.3), X(y + h * 0.78))], fill=(40, 44, 54))
        rect([x + w * 0.42, y + h * 0.38, x + w * 0.6, y + h * 0.62], fill=(88, 96, 110))
        rect([x + w * 0.48, y + h * 0.24, x + w * 0.54, y + h * 0.38], fill=(60, 66, 78))
    elif kind == "boat":
        rect([x, y, x + w, y + h], fill=(30, 74, 116))
        for i in range(3):
            line([(x + 6, y + h * (0.66 + i * 0.1)), (x + w - 6, y + h * (0.66 + i * 0.1))],
                 fill=(120, 180, 220), width=2)
        d.polygon([(X(x + w * 0.22), X(y + h * 0.6)), (X(x + w * 0.8), X(y + h * 0.6)),
                   (X(x + w * 0.68), X(y + h * 0.74)), (X(x + w * 0.34), X(y + h * 0.74))], fill=(240, 236, 224))
        rect([x + w * 0.4, y + h * 0.36, x + w * 0.62, y + h * 0.6], fill=(196, 60, 44))
    elif kind == "gavel":
        rect([x, y, x + w, y + h], fill=(238, 230, 210))
        rect([x + 8, y + h - 12, x + w - 8, y + h - 7], fill=(150, 128, 92))
        line([(cx - 20, cy + 10), (cx + 10, cy - 14)], fill=(120, 82, 40), width=6)
        rect([cx + 2, cy - 22, cx + 22, cy - 9], fill=(160, 108, 52))
        rect([cx - 30, cy + 16, cx + 2, cy + 21], fill=(120, 82, 40))
    elif kind == "ballot":
        rect([x, y, x + w, y + h], fill=(232, 226, 208))
        rect([cx - 26, cy - 18, cx + 26, cy + 20], fill=(255, 255, 252), outline=INK, width=1)
        line([(cx - 16, cy - 6), (cx - 4, cy + 6)], fill=GREEN, width=4)
        line([(cx - 4, cy + 6), (cx + 18, cy - 12)], fill=GREEN, width=4)
        rect([cx - 30, cy + 22, cx + 30, cy + 27], fill=INK)
    elif kind == "factory":
        rect([x, y, x + w, y + h], fill=(70, 66, 74))
        rect([x + 10, y + h * 0.45, x + w - 10, y + h - 6], fill=(104, 98, 104))
        rect([x + 18, y + h * 0.18, x + 30, y + h * 0.45], fill=(88, 82, 88))
        d.ellipse([X(x + 8), X(y + 2), X(x + 34), X(y + h * 0.24)], fill=(140, 138, 140))
        d.polygon([(X(cx + 6), X(y + h * 0.5)), (X(cx + 18), X(y + h * 0.2)), (X(cx + 26), X(y + h * 0.5))], fill=(240, 130, 30))
        d.polygon([(X(cx + 22), X(y + h * 0.52)), (X(cx + 30), X(y + h * 0.3)), (X(cx + 36), X(y + h * 0.52))], fill=(250, 178, 44))
    elif kind == "plane":
        rect([x, y, x + w, y + h], fill=(38, 84, 140))
        d.ellipse([X(x + w * 0.14), X(y + h * 0.52), X(x + w * 0.86), X(y + h * 0.72)], fill=(238, 240, 244))
        d.polygon([(X(x + w * 0.44), X(y + h * 0.56)), (X(x + w * 0.62), X(y + h * 0.24)),
                   (X(x + w * 0.7), X(y + h * 0.24)), (X(x + w * 0.6), X(y + h * 0.58))], fill=(210, 214, 222))
        d.polygon([(X(x + w * 0.78), X(y + h * 0.5)), (X(x + w * 0.9), X(y + h * 0.3)),
                   (X(x + w * 0.92), X(y + h * 0.52))], fill=RED)
        for i in range(5):
            d.ellipse([X(x + w * (0.3 + i * 0.09)), X(y + h * 0.585), X(x + w * (0.345 + i * 0.09)), X(y + h * 0.635)], fill=(70, 110, 170))
    elif kind == "ball":
        rect([x, y, x + w, y + h], fill=(24, 120, 62))
        line([(x, cy), (x + w, cy)], fill=(230, 240, 230), width=1)
        d.ellipse([X(cx - 17), X(cy - 17), X(cx + 17), X(cy + 17)], fill=(250, 250, 248), outline=INK, width=1)
        d.polygon([(X(cx - 6), X(cy - 8)), (X(cx + 6), X(cy - 8)), (X(cx + 9), X(cy + 2)),
                   (X(cx), X(cy + 9)), (X(cx - 9), X(cy + 2))], fill=INK)
    elif kind == "cricket":
        rect([x, y, x + w, y + h], fill=(30, 116, 66))
        rect([cx - 9, y + 10, cx + 9, y + h - 10], fill=(216, 192, 138))
        for i in range(3):
            line([(cx - 6 + i * 6, y + 14), (cx - 6 + i * 6, y + 26)], fill=(250, 240, 210), width=2)
        d.ellipse([X(cx + 16), X(cy + 8), X(cx + 26), X(cy + 18)], fill=(198, 30, 40))
    elif kind == "smog":
        rect([x, y, x + w, y + h], fill=(172, 158, 128))
        rect([x + 10, y + h * 0.4, x + 34, y + h - 6], fill=(120, 108, 88))
        rect([x + w - 38, y + h * 0.3, x + w - 12, y + h - 6], fill=(110, 98, 80))
        rect([cx - 14, y + h * 0.48, cx + 14, y + h - 6], fill=(128, 114, 90))
        d.ellipse([X(x + w * 0.62), X(y + 6), X(x + w * 0.82), X(y + h * 0.3)], fill=(226, 208, 168))
    elif kind == "oil":
        rect([x, y, x + w, y + h], fill=(44, 40, 36))
        d.polygon([(X(x + 16), X(y + h - 8)), (X(cx), X(y + 12)), (X(x + w - 16), X(y + h - 8))], outline=(220, 200, 160), width=3)
        line([(cx, y + 12), (x + w - 22, y + 26)], fill=(220, 200, 160), width=3)
        rect([x + w - 34, y + 22, x + w - 12, y + 32], fill=(220, 200, 160))
        rect([x + 8, y + h - 12, x + w - 8, y + h - 8], fill=(150, 130, 90))
    elif kind == "mine":
        rect([x, y, x + w, y + h], fill=(84, 62, 40))
        d.polygon([(X(x + 8), X(y + h - 8)), (X(x + w * 0.4), X(y + 14)), (X(x + w * 0.62), X(y + h - 8))], fill=(120, 92, 54))
        d.polygon([(X(x + w * 0.42), X(y + h - 8)), (X(x + w * 0.68), X(y + 22)), (X(x + w - 8), X(y + h - 8))], fill=(104, 78, 44))
        d.ellipse([X(cx - 6), X(cy - 4), X(cx + 8), X(cy + 10)], fill=(90, 200, 230))
        d.ellipse([X(cx + 16), X(cy + 8), X(cx + 27), X(cy + 19)], fill=(250, 200, 70))
    elif kind == "globe":
        rect([x, y, x + w, y + h], fill=(20, 48, 92))
        d.ellipse([X(cx - 26), X(cy - 26), X(cx + 26), X(cy + 26)], fill=(90, 170, 220), outline=(220, 240, 255), width=2)
        d.ellipse([X(cx - 20), X(cy - 18), X(cx - 2), X(cy - 2)], fill=(80, 170, 100))
        d.ellipse([X(cx + 2), X(cy + 4), X(cx + 20), X(cy + 20)], fill=(80, 170, 100))
        d.ellipse([X(cx - 16), X(cy + 8), X(cx - 4), X(cy + 18)], fill=(80, 170, 100))
    elif kind == "handshake":
        rect([x, y, x + w, y + h], fill=(36, 62, 110))
        rect([x + 8, cy - 16, cx - 2, cy + 14], fill=(52, 88, 150))
        rect([cx + 2, cy - 16, x + w - 8, cy + 14], fill=(150, 52, 60))
        d.ellipse([X(cx - 13), X(cy - 9), X(cx + 13), X(cy + 15)], fill=(232, 186, 140))
        line([(cx - 22, cy + 16), (cx + 22, cy + 16)], fill=(240, 220, 160), width=3)
    elif kind == "microphone":
        rect([x, y, x + w, y + h], fill=(54, 40, 84))
        d.ellipse([X(cx - 9), X(y + 7), X(cx + 9), X(y + h * 0.52)], fill=(214, 218, 226), outline=INK, width=1)
        for i in range(3):
            line([(cx - 9, y + 12 + i * 6), (cx + 9, y + 12 + i * 6)], fill=(120, 126, 140), width=1)
        line([(cx, y + h * 0.52), (cx, y + h - 11)], fill=(220, 220, 226), width=3)
        line([(cx - 13, y + h - 9), (cx + 13, y + h - 9)], fill=(220, 220, 226), width=3)
    elif kind == "satellite":
        rect([x, y, x + w, y + h], fill=(10, 14, 34))
        for sx, sy in [(0.15, 0.2), (0.8, 0.16), (0.66, 0.7), (0.24, 0.78)]:
            d.ellipse([X(x + w * sx), X(y + h * sy), X(x + w * sx + 3), X(y + h * sy + 3)], fill=(255, 255, 240))
        rect([cx - 9, cy - 9, cx + 9, cy + 9], fill=(190, 196, 206))
        rect([cx - 34, cy - 6, cx - 12, cy + 6], fill=(52, 92, 190))
        rect([cx + 12, cy - 6, cx + 34, cy + 6], fill=(52, 92, 190))
    else:  # generic skyline
        rect([x, y, x + w, y + h], fill=(52, 66, 96))
        rect([x + 10, y + h * 0.36, x + 30, y + h - 6], fill=(30, 38, 58))
        rect([cx - 10, y + h * 0.22, cx + 12, y + h - 6], fill=(36, 46, 68))
        rect([x + w - 32, y + h * 0.44, x + w - 10, y + h - 6], fill=(30, 38, 58))
        for i in range(6):
            rect([x + 14 + (i % 3) * 7, y + h * (0.46 + (i // 3) * 0.2), x + 18 + (i % 3) * 7, y + h * (0.54 + (i // 3) * 0.2)], fill=(250, 204, 84))


def num_badge(x, y, n, fill=RED, r=9):
    d.ellipse([X(x), X(y), X(x + 2 * r), X(y + 2 * r)], fill=fill)
    s = str(n)
    f = F(SANS_B, 11 if n < 10 else 9.5)
    if r < 9:
        f = F(SANS_B, 9 if n < 10 else 8)
    text(x + r, y + r + 0.5, s, f, (255, 255, 255), anchor="mm")


# ---------------------------------------------------------------- header
rect([0, 0, 1024, 24], fill=INK)
text(14, 5, "THE WORLD IN ONE DAY  •  ONE PAGE", F(SANS_B, 11), (255, 255, 255))
hdr_r = f"{S.TOTAL} STORIES  •  {S.REGIONS} REGIONS  •  ALL FROM {S.DATE_LONG.upper()}"
text(1010, 5, hdr_r, F(SANS_B, 11), (255, 255, 255), anchor="ra")

text(512, 30, S.DATE_LONG, F(SERIF_B, 57), INK, anchor="ma")
sub = S.SUBLINE
text(512, 94, sub, F(SERIF_I, 15.5), RED, anchor="ma")
line([(14, 116), (1010, 116)], fill=INK, width=2.5)

# data strip
dx, dw = 14, (1024 - 28 - 5 * 6) / 6
for i, (big, small, col) in enumerate(S.DATA):
    x = dx + i * (dw + 6)
    rect([x, 121, x + 3, 163], fill=col)
    text(x + 9, 122, big, F(SERIF_B, 24), col)
    para(x + 9, 149, small, F(SANS, 8.6), dw - 12, GREY, leading=1, max_lines=2)
line([(14, 168), (1010, 168)], fill=INK, width=1)

# region bar
rx = 14
tot = sum(n for _, n, _ in S.REGION_BAR)
for name, n, col in S.REGION_BAR:
    wseg = (1024 - 28) * n / tot
    rect([rx, 172, rx + wseg, 188], fill=col)
    lab = f"{name} {n}"
    if wseg > 52:
        text(rx + wseg / 2, 175.5, lab, F(SANS_B, 9.5), (255, 255, 255), anchor="ma")
    rx += wseg

# timeline
rect([14, 191, 1010, 209], fill=NAVY)
tt = "   •   ".join(f"{t} {ev}" for t, ev in S.TIMELINE)
text(512, 194.5, tt, F(SANS_B, 9.5), (255, 255, 255), anchor="ma")

# ---------------------------------------------------------------- lead row
LY = 214
LW = (1024 - 28 - 2 * 10) / 3
for i, st in enumerate(S.LEADS):
    x = 14 + i * (LW + 10)
    art(st["art"], x, LY, LW, 86)
    chip(x + 7, LY + 7, st["kicker"], RED if i != 1 else NAVY)
    tag(x + LW - 7, LY + 93, st.get("cert", "REPORTED"))
    num_badge(x, LY + 93, st["n"], NAVY if i == 1 else RED)
    text(x + 24, LY + 91, st["loc"], F(SANS_B, 10.5), RED)
    y = para(x, LY + 110, st["head"], F(SERIF_B, 18.5), LW, leading=2, max_lines=2)
    para(x, y + 1, st["body"], F(SANS, 10.8), LW, (52, 50, 46), leading=2, max_lines=2)
line([(14, 392), (1010, 392)], fill=INK, width=2)

# ---------------------------------------------------------------- mid grid
MY = 398
MW = (1024 - 28 - 4 * 8) / 5
MH = 148
for j, st in enumerate(S.MIDS):
    r, c = divmod(j, 5)
    x = 14 + c * (MW + 8)
    y = MY + r * (MH + 8)
    if c:
        line([(x - 4, y), (x - 4, y + MH)], fill=LGREY, width=1)
    art(st["art"], x, y, MW, 44)
    chip(x + 5, y + 5, st["kicker"], NAVY, F(SANS_B, 8.5), pad=4)
    num_badge(x, y + 49, st["n"], RED, r=8)
    text(x + 20, y + 50, st["loc"], F(SANS_B, 8.5), RED)
    yy = para(x, y + 64, st["head"], F(SERIF_B, 13.5), MW, leading=1.5, max_lines=3)
    para(x, yy + 1, st["body"], F(SANS, 9.5), MW, (52, 50, 46), leading=1.5, max_lines=3)
line([(14, MY + 2 * MH + 8), (1010, MY + 2 * MH + 8)], fill=INK, width=2)

# ---------------------------------------------------------------- bottom
BY = MY + 2 * MH + 16
text(14, BY, "WHERE IT HAPPENED", F(SANS_B, 11), RED)
text(370, BY, S.ALSO_TITLE, F(SANS_B, 11), RED)
line([(14, BY + 16), (1010, BY + 16)], fill=GREY, width=1)

# dotted world map (very simplified continents as dot grids)
MAP_X, MAP_Y, MAP_W, MAP_H = 14, BY + 22, 342, 168
rect([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=(238, 232, 214))
# continent blobs: (cx, cy, rx, ry) in map fractions
blobs = [(0.16, 0.30, 0.13, 0.16), (0.27, 0.68, 0.07, 0.15), (0.52, 0.26, 0.10, 0.11),
         (0.55, 0.52, 0.09, 0.16), (0.68, 0.30, 0.17, 0.15), (0.80, 0.62, 0.06, 0.10),
         (0.90, 0.80, 0.055, 0.07), (0.44, 0.14, 0.05, 0.06)]
step = 7
for gx in range(int(MAP_X) + 4, int(MAP_X + MAP_W) - 2, step):
    for gy in range(int(MAP_Y) + 4, int(MAP_Y + MAP_H) - 2, step):
        fx, fy = (gx - MAP_X) / MAP_W, (gy - MAP_Y) / MAP_H
        inside = any(((fx - bx) / brx) ** 2 + ((fy - by) / bry) ** 2 < 1 for bx, by, brx, bry in blobs)
        if inside:
            d.ellipse([X(gx), X(gy), X(gx + 2.2), X(gy + 2.2)], fill=(150, 142, 122))
for n, fx, fy in S.PINS:
    px, py = MAP_X + fx * MAP_W, MAP_Y + fy * MAP_H
    d.ellipse([X(px - 8), X(py - 8), X(px + 8), X(py + 8)], fill=RED, outline=(255, 255, 255), width=1)
    text(px, py + 0.5, str(n), F(SANS_B, 8.5), (255, 255, 255), anchor="mm")
text(MAP_X, MAP_Y + MAP_H + 4, "pins: stories 1–13  •  map is a schematic, not to scale", F(SANS, 8.5), GREY)

# ALSO list, two columns
AX, AW = 370, 640
colw = (AW - 18) / 2
items = S.ALSO
half = (len(items) + 1) // 2
for ci, chunk in enumerate([items[:half], items[half:]]):
    x = AX + ci * (colw + 18)
    y = BY + 22
    for st in chunk:
        num_badge(x, y, st["n"], NAVY, r=7.5)
        s = f"{st['where']}: {st['text']}"
        yy = para(x + 19, y - 1, s, F(SANS, 9.5), colw - 19, INK, leading=1.1, max_lines=2)
        y = max(yy, y + 14) + 3.5

# ---------------------------------------------------------------- footer
FY = 966
rect([14, FY, 1010, FY + 30], outline=RED, width=1.5)
text(22, FY + 5, "DATE CHECK", F(SANS_B, 10.5), RED)
para(108, FY + 4.5, S.DATE_CHECK, F(SANS, 9.3), 890, (52, 50, 46), leading=1.2, max_lines=2)
text(14, FY + 36, S.SOURCES, F(SANS, 8.5), GREY)
text(1010, FY + 36, "Drawings and map: original  •  THE WORLD IN ONE DAY", F(SANS_B, 8.5), GREY, anchor="ra")

img = img.resize((1024, 1024), Image.LANCZOS)
img.save("entry.png", optimize=True)
print("saved entry.png")
