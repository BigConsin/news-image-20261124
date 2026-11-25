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

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
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
    """detailed original mini-graphic inside box (x,y,w,h)"""
    cx, cy = x + w / 2, y + h / 2
    WHITE = (245, 245, 240)
    if kind == "rally":
        rect([x, y, x + w, y + h], fill=(13, 22, 44))
        gx0, gx1, gy0, gy1 = x + 36, x + w - 14, y + 12, y + h - 18
        def vy(v):
            return gy0 + (35 - v) / 45 * (gy1 - gy0)
        for gv, lab in [(30, "+30%"), (15, "+15%"), (0, "0%"), (-10, None)]:
            line([(gx0, vy(gv)), (gx1, vy(gv))], fill=(120, 140, 180) if gv == 0 else (52, 72, 110), width=1)
            if lab:
                text(gx0 - 32, vy(gv) - 5, lab, F(SANS, 7.5), (150, 168, 200))
        vals = [2, 4, 31.5, 9, -4.4]
        pts = [(gx0 + i * (gx1 - gx0) / 4, vy(v)) for i, v in enumerate(vals)]
        line(pts, fill=(255, 92, 82), width=3)
        for px_, py_ in (pts[2], pts[4]):
            d.ellipse([X(px_ - 4), X(py_ - 4), X(px_ + 4), X(py_ + 4)], fill=WHITE)
        text(pts[2][0] - 66, pts[2][1] + 4, "+31.5% MON", F(SANS_B, 9.5), (255, 170, 120))
        text(pts[4][0] - 58, pts[4][1] - 14, "-4.4% TUE", F(SANS_B, 9.5), (255, 120, 110))
        for px_, lab in [(pts[0][0], "FRI"), (pts[2][0], "MON")]:
            text(px_ - 8, gy1 + 5, lab, F(SANS, 7.5), (150, 168, 200))
    elif kind == "deal":
        rect([x, y, x + w, y + h], fill=(24, 44, 88))
        bw, bh = w * 0.32, 36
        by0 = y + 10
        cyb = by0 + bh / 2
        rect([x + 12, by0, x + 12 + bw, by0 + bh], fill=(238, 240, 244))
        text(x + 12 + bw / 2 - 12, cyb - 8, "SANOFI", F(SERIF_B, 13), (20, 40, 80), anchor="mm")
        text(x + 12 + bw / 2 - 12, cyb + 7, "Paris - buyer", F(SANS, 7.5), (90, 100, 120), anchor="ma")
        flag_fr(x + 12 + bw - 25, by0 + 3, 21, 13)
        rect([x + w - 12 - bw, by0, x + w - 12, by0 + bh], fill=(250, 226, 170))
        text(x + w - 12 - bw / 2 - 12, cyb - 8, "INSMED", F(SERIF_B, 13), (110, 70, 10), anchor="mm")
        text(x + w - 12 - bw / 2 - 12, cyb + 7, "US - target", F(SANS, 7.5), (130, 100, 40), anchor="ma")
        flag_us(x + w - 12 - 26, by0 + 3, 23, 13)
        ax0, ax1, ay = x + 18 + bw, x + w - 18 - bw, cyb
        line([(ax0, ay), (ax1, ay)], fill=(250, 200, 90), width=4)
        d.polygon([(X(ax1), X(ay - 6)), (X(ax1), X(ay + 6)), (X(ax1 + 10), X(ay))], fill=(250, 200, 90))
        text((ax0 + ax1) / 2, ay - 17, "$41bn CASH", F(SANS_B, 10.5), (250, 210, 110), anchor="ma")
        steps = [("$119.9", "BEFORE", (140, 160, 200)), ("$170.39", "MON CLOSE", (230, 190, 110)),
                 ("$175", "THE OFFER", (250, 120, 90))]
        by = y + h - 27
        text(x + 12, by + 2, "INSMED PRICE:", F(SANS_B, 8), (170, 190, 230))
        for i, (lab, cap, col) in enumerate(steps):
            bx = x + 96 + i * 74
            rect([bx, by - 2, bx + 8, by + 14], fill=col)
            text(bx + 11, by - 4, lab, F(SANS_B, 9), WHITE)
            text(bx + 11, by + 7, cap, F(SANS, 6.5), (180, 195, 225))
    elif kind == "deal_s":
        rect([x, y, x + w, y + h], fill=(24, 44, 88))
        bw = w * 0.3
        rect([x + 8, y + 5, x + 8 + bw, y + 27], fill=(238, 240, 244))
        text(x + 15, y + 11, "SANOFI", F(SERIF_B, 11), (20, 40, 80))
        rect([x + w - 8 - bw, y + 5, x + w - 8, y + 27], fill=(250, 226, 170))
        text(x + w - 8 - bw + 7, y + 11, "INSMED", F(SERIF_B, 11), (110, 70, 10))
        ax0, ax1, ay = x + 14 + bw, x + w - 14 - bw, y + 16
        line([(ax0, ay), (ax1, ay)], fill=(250, 200, 90), width=3)
        d.polygon([(X(ax1), X(ay - 5)), (X(ax1), X(ay + 5)), (X(ax1 + 8), X(ay))], fill=(250, 200, 90))
        text((ax0 + ax1) / 2 - 30, ay - 14, "$41bn CASH", F(SANS_B, 9.5), (250, 210, 110))
        text(x + 8, y + h - 15, "INSMED PRICE:", F(SANS_B, 7.5), (170, 190, 230))
        for i, (lab, col) in enumerate([("$119.9", (140, 160, 200)), ("$170.39", (230, 190, 110)), ("$175 OFFER", (250, 120, 90))]):
            bx = x + 86 + i * 82
            rect([bx, y + h - 16, bx + 7, y + h - 5], fill=col)
            text(bx + 10, y + h - 14, lab, F(SANS_B, 8.5), WHITE)
    elif kind == "strike":
        rect([x, y, x + w, y + h], fill=(16, 18, 34))
        for bx, bw2, bh in [(0.04, 0.13, 0.52), (0.2, 0.1, 0.38), (0.66, 0.12, 0.46), (0.82, 0.14, 0.58)]:
            rect([x + w * bx, y + h * 0.78 - h * bh, x + w * (bx + bw2), y + h * 0.78], fill=(38, 44, 66))
            for r in range(3):
                rect([x + w * bx + 5, y + h * 0.78 - h * bh + 6 + r * 11, x + w * bx + 11, y + h * 0.78 - h * bh + 11 + r * 11], fill=(250, 204, 84))
        ex, ey = x + w * 0.47, y + h * 0.34
        for a in range(12):
            import math as _m
            dx, dy = _m.cos(a * 0.524), _m.sin(a * 0.524)
            line([(ex, ey), (ex + dx * 17, ey + dy * 17)], fill=(255, 150, 60), width=2)
        d.ellipse([X(ex - 8), X(ey - 8), X(ex + 8), X(ey + 8)], fill=(255, 190, 80))
        for dxx in (0.3, 0.58):
            dxp, dyp = x + w * dxx, y + h * 0.16
            d.polygon([(X(dxp - 9), X(dyp)), (X(dxp + 9), X(dyp)), (X(dxp + 3), X(dyp + 5)), (X(dxp - 3), X(dyp + 5))], fill=(200, 205, 215))
            line([(dxp - 13, dyp + 2), (dxp - 4, dyp + 2)], fill=(200, 205, 215), width=2)
            line([(dxp + 4, dyp + 2), (dxp + 13, dyp + 2)], fill=(200, 205, 215), width=2)
        rect([x, y + h - 17, x + w, y + h], fill=(150, 30, 26))
        text(x + 10, y + h - 13.5, "2 DEAD - 40+ WOUNDED - 96 DRONES LAUNCHED", F(SANS_B, 9), (255, 240, 230))
    elif kind == "mic2":
        rect([x, y, x + w, y + h], fill=(54, 40, 84))
        d.ellipse([X(cx - 26), X(cy - 13), X(cx - 8), X(cy + 13)], fill=(214, 218, 226), outline=INK, width=1)
        for i in range(3):
            line([(cx - 26, cy - 7 + i * 7), (cx - 8, cy - 7 + i * 7)], fill=(120, 126, 140), width=1)
        line([(cx - 17, cy + 13), (cx - 17, cy + 19)], fill=(220, 220, 226), width=3)
        line([(cx - 27, cy + 20), (cx - 7, cy + 20)], fill=(220, 220, 226), width=3)
        for r in (10, 17, 24):
            d.arc([X(cx - 2), X(cy - r), X(cx - 2 + 2 * r * 0.62), X(cy + r)], start=-55, end=55, fill=(250, 200, 90), width=2)
        text(cx + 26, cy - 7, "PRESS", F(SANS_B, 10), (240, 230, 255))
        text(cx + 26, cy + 5, "BRIEFING", F(SANS, 7.5), (190, 180, 220))
    elif kind == "gaza":
        rect([x, y, x + w, y + h], fill=(40, 36, 44))
        rect([x, y + h - 8, x + w, y + h], fill=(24, 22, 28))
        for bx, bw2, bh in [(0.06, 0.16, 0.5), (0.3, 0.13, 0.66), (0.52, 0.17, 0.44), (0.76, 0.15, 0.58)]:
            rect([x + w * bx, y + h - 8 - h * bh, x + w * (bx + bw2), y + h - 8], fill=(66, 60, 66))
        for sx in (0.36, 0.58, 0.82):
            for r in range(3):
                d.ellipse([X(x + w * sx - 5 - r * 2), X(y + 3 + r * 6), X(x + w * sx + 5 + r * 2), X(y + 11 + r * 6)], fill=(110, 104, 104))
        line([(x + w * 0.12, y + 4), (x + w * 0.34, y + h * 0.4)], fill=(255, 150, 70), width=2)
        line([(x + w * 0.2, y + 2), (x + w * 0.56, y + h * 0.34)], fill=(255, 120, 60), width=2)
        chip(x + w - 52, y + h - 22, "7 DEAD", RED, font=F(SANS_B, 8.5))
    elif kind == "boat2":
        rect([x, y, x + w, y + h], fill=(30, 74, 116))
        for i in range(3):
            line([(x + 6, y + h * (0.68 + i * 0.1)), (x + w * 0.58, y + h * (0.68 + i * 0.1))], fill=(120, 180, 220), width=2)
        d.polygon([(X(x + w * 0.08), X(y + h * 0.6)), (X(x + w * 0.52), X(y + h * 0.6)),
                   (X(x + w * 0.44), X(y + h * 0.74)), (X(x + w * 0.16), X(y + h * 0.74))], fill=(240, 236, 224))
        rect([x + w * 0.2, y + h * 0.36, x + w * 0.38, y + h * 0.6], fill=(196, 60, 44))
        for t in range(5):
            d.ellipse([X(x + w * (0.56 + t * 0.055)), X(y + h * (0.3 - t * 0.028)), X(x + w * (0.56 + t * 0.055) + 3), X(y + h * (0.3 - t * 0.028) + 3)], fill=(255, 210, 120))
        text(x + w * 0.63, y + 5, "175", F(SERIF_B, 19), (255, 220, 150))
        text(x + w * 0.63, y + 27, "MISSING", F(SANS_B, 8), (200, 225, 250))
    elif kind == "conf" and h < 52:
        rect([x, y, x + w, y + h], fill=(14, 44, 34))
        pts = [(x + 8, y + h - 8), (x + w * 0.45, y + h - 12), (x + w - 52, y + 6)]
        line(pts, fill=(74, 222, 128), width=3)
        for px_, py_ in (pts[0], pts[-1]):
            d.ellipse([X(px_ - 3), X(py_ - 3), X(px_ + 3), X(py_ + 3)], fill=WHITE)
        text(pts[0][0], pts[0][1] - 13, "91.9", F(SANS_B, 8), (190, 250, 210))
        text(pts[-1][0] + 6, pts[-1][1] - 2, "103.3", F(SANS_B, 10), (160, 255, 190))
    elif kind == "conf":
        rect([x, y, x + w, y + h], fill=(14, 44, 34))
        gx0, gx1, gy0, gy1 = x + 8, x + w - 8, y + 7, y + h - 13
        for i in range(3):
            gy = gy0 + (gy1 - gy0) * i / 2
            line([(gx0, gy), (gx1, gy)], fill=(36, 84, 62), width=1)
        fy = gy0 + (gy1 - gy0) * 0.62
        for sx in range(int(gx0), int(gx1), 7):
            line([(sx, fy), (sx + 4, fy)], fill=(250, 200, 90), width=1)
        text(gx0 + 2, fy - 10, "FORECAST 92.5", F(SANS, 6.5), (250, 200, 90))
        pts = [(gx0 + 4, gy0 + (gy1 - gy0) * 0.78), (x + w * 0.42, gy0 + (gy1 - gy0) * 0.72), (gx1 - 26, gy0 + 3)]
        line(pts, fill=(74, 222, 128), width=3)
        for px_, py_ in (pts[0], pts[-1]):
            d.ellipse([X(px_ - 3), X(py_ - 3), X(px_ + 3), X(py_ + 3)], fill=WHITE)
        text(pts[0][0] - 2, pts[0][1] - 12, "91.9", F(SANS_B, 8.5), (190, 250, 210))
        text(pts[-1][0] - 36, pts[-1][1] + 2, "103.3", F(SANS_B, 9.5), (160, 255, 190))
    elif kind == "tariff":
        rect([x, y, x + w, y + h], fill=(44, 48, 66))
        for r in range(4):
            for c in range(4):
                rect([x + 12 + c * 13, y + 7 + r * 9, x + 21 + c * 13, y + 14 + r * 9], fill=(240, 170, 60) if (r * 4 + c) % 3 else (150, 160, 185))
        d.ellipse([X(cx + 8), X(cy - 14), X(cx + 30), X(cy + 8)], outline=(255, 240, 210), width=3)
        line([(cx + 26, cy + 5), (cx + 40, cy + 19)], fill=(255, 240, 210), width=4)
        text(cx + 44, cy - 8, "x16", F(SERIF_B, 15), (255, 220, 150))
        text(cx + 44, cy + 8, "PARTNERS", F(SANS_B, 7), (210, 215, 230))
    elif kind == "debt":
        rect([x, y, x + w, y + h], fill=(238, 232, 216))
        text(x + 8, y + 4, "DEBT $237.5bn", F(SANS_B, 8), (170, 40, 34))
        rect([x + 8, y + 15, x + w - 66, y + 21], fill=(188, 44, 38))
        text(x + w - 56, y + 3, "242%", F(SERIF_B, 13), (170, 40, 34))
        text(x + w - 56, y + 17, "OF GDP", F(SANS_B, 6.5), (120, 90, 80))
        text(x + 8, y + 24, "GDP ~$98bn", F(SANS_B, 8), (30, 110, 100))
        rect([x + 8, y + 35, x + 8 + (w - 74) * 0.413, y + 41], fill=(20, 130, 118))
    elif kind == "cricket2":
        rect([x, y, x + w, y + h], fill=(30, 116, 66))
        rect([x + 12, y + 8, x + 28, y + h - 8], fill=(216, 192, 138))
        for i in range(3):
            line([(x + 15 + i * 5, y + 11), (x + 15 + i * 5, y + 21)], fill=(250, 240, 210), width=2)
        d.ellipse([X(x + 36), X(y + h - 14), X(x + 45), X(y + h - 5)], fill=(198, 30, 40))
        text(x + 54, y + 12, "188-2", F(SERIF_B, 14), (255, 255, 245))
        text(x + 54, y + 30, "DONALD 85 OFF 32 - CHASED 185 IN 13.1 OV", F(SANS_B, 6.5), (210, 245, 220))
    elif kind == "mine2":
        rect([x, y, x + w, y + h], fill=(84, 62, 40))
        for i, bh in enumerate((0.3, 0.48, 0.66, 0.86)):
            rect([x + 12 + i * 17, y + h - 8 - h * bh, x + 25 + i * 17, y + h - 8], fill=(240, 190, 80))
        text(cx + 12, y + 8, "$965M", F(SERIF_B, 15), (255, 230, 160))
        text(cx + 12, y + 25, "NEW FINANCING", F(SANS_B, 7), (240, 215, 170))
    elif kind == "oil2":
        rect([x, y, x + w, y + h], fill=(44, 40, 36))
        d.polygon([(X(x + 14), X(y + h - 8)), (X(x + 34), X(y + 10)), (X(x + 54), X(y + h - 8))], outline=(220, 200, 160), width=3)
        line([(x + 34, y + 10), (x + 62, y + 22)], fill=(220, 200, 160), width=3)
        rect([x + 56, y + 18, x + 70, y + 27], fill=(220, 200, 160))
        text(x + 82, y + 7, "BRENT $88.62", F(SANS_B, 9.5), (250, 230, 190))
        text(x + 82, y + 20, "DOWN 0.8%", F(SANS_B, 8), (255, 150, 120))
        text(x + 82, y + 32, "3-MONTH LOW", F(SANS, 7), (200, 190, 170))
    elif kind == "gavel":
        rect([x, y, x + w, y + h], fill=(238, 230, 210))
        rect([x + 8, y + h - 12, x + w - 8, y + h - 7], fill=(150, 128, 92))
        line([(cx - 20, cy + 10), (cx + 10, cy - 14)], fill=(120, 82, 40), width=6)
        rect([cx + 2, cy - 22, cx + 22, cy - 9], fill=(160, 108, 52))
        rect([cx - 30, cy + 16, cx + 2, cy + 21], fill=(120, 82, 40))
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


# ---------------------------------------------------------------- winners' layout v4
import glob as _glob
WHITE = (255, 255, 255)
from PIL import Image as _Img, ImageEnhance as _Enh

def flag_fr(fx, fy, fw=20, fh=13):
    for i, cc in enumerate([(0, 85, 164), (255, 255, 255), (239, 65, 53)]):
        rect([fx + i * fw / 3, fy, fx + (i + 1) * fw / 3, fy + fh], fill=cc)
    rect([fx, fy, fx + fw, fy + fh], outline=(13, 26, 54), width=1)

def flag_us(fx, fy, fw=22, fh=13):
    for i in range(7):
        rect([fx, fy + i * fh / 7, fx + fw, fy + (i + 1) * fh / 7], fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    cw, chh = fw * 0.42, fh * 4 / 7
    rect([fx, fy, fx + cw, fy + chh], fill=(60, 59, 110))
    for r in range(3):
        for c in range(4):
            px_, py_ = fx + 1.6 + c * (cw - 3) / 3, fy + 1.4 + r * (chh - 2.6) / 2
            d.ellipse([X(px_), X(py_), X(px_ + 1.1), X(py_ + 1.1)], fill=(255, 255, 255))
    rect([fx, fy, fx + fw, fy + fh], outline=(13, 26, 54), width=1)

def illus(name, x, y, w, h):
    files = sorted(_glob.glob(f"assets/{name}.*"))
    if not files:
        rect([x, y, x + w, y + h], fill=(210, 200, 175))
        return
    im = _Img.open(files[0]).convert("RGB")
    im = _Enh.Contrast(im).enhance(1.3)
    im = _Enh.Color(im).enhance(1.2)
    im = _Enh.Sharpness(im).enhance(1.3)
    tw, th = w * SS, h * SS
    scale = max(tw / im.width, th / im.height)
    im = im.resize((int(im.width * scale) + 1, int(im.height * scale) + 1), _Img.LANCZOS)
    ox = (im.width - int(tw)) // 2
    oy = (im.height - int(th)) // 2
    im = im.crop((ox, oy, ox + int(tw), oy + int(th)))
    img.paste(im, (int(X(x)), int(X(y))))
    rect([x, y, x + w, y + h], outline=(90, 84, 70), width=1)

def rule(y, x0=14, x1=1010, wdt=1, col=(60, 56, 50)):
    line([(x0, y), (x1, y)], fill=col, width=wdt)

def banner(x, y, txt, fill=RED, size=13):
    f = F(SANS_B, size)
    tw = tlen(txt, f)
    h = size + 9
    d.polygon([(X(x), X(y)), (X(x + tw + 16), X(y)), (X(x + tw + 7), X(y + h)), (X(x), X(y + h))], fill=fill)
    text(x + 7, y + 3.5, txt, f, WHITE)

def chip_r(x1, y, txt, fill=(10, 10, 12), size=10.5):
    f = F(SANS_B, size)
    tw = tlen(txt, f)
    rect([x1 - tw - 12, y, x1, y + size + 7], fill=fill)
    text(x1 - tw - 6, y + 2.5, txt, f, WHITE)

CERT_COL = {"CONFIRMED": (26, 118, 56), "REPORTED": (28, 66, 138), "OFFICIAL": (158, 106, 8), "CLAIM": (186, 28, 28)}
def cert_tag(x1, y, cert, size=7.5):
    f = F(SANS_B, size)
    tw = tlen(cert, f)
    col = CERT_COL[cert]
    rect([x1 - tw - 8, y, x1, y + size + 5], outline=col, width=1)
    text(x1 - tw - 4, y + 1.5, cert, f, col)

def loc_line(x, y, wdt, n, loc, cert):
    num_badge(x, y, n, RED, r=8)
    text(x + 21, y + 2, loc, F(SANS_B, 8.5), NAVY)
    cert_tag(x + wdt, y, cert)

# ---- top line + giant date (winners' masthead)
text(14, 7, "THE WORLD IN ONE DAY  •  ONE PAGE", F(SANS_B, 10.5), RED)
text(1010, 7, "36 STORIES  •  7 REGIONS  •  ALL FROM TUESDAY 24 NOVEMBER 2026", F(SANS_B, 10.5), (70, 66, 60), anchor="ra")
text(512, 26, "Tuesday 24 November 2026", F(SERIF_B, 55), INK, anchor="ma")
rule(90, wdt=3); rule(95, wdt=1)
text(512, 102, "Sanofi's $41bn Insmed deal  •  Kremlin shuts Europe out of Ukraine talks  •  Chip rally unwinds", F(SERIF_I, 13.5), RED, anchor="ma")
# ---- region colour bar
RY = 124
regions = [("EUROPE", 10, (32, 64, 128)), ("MIDDLE EAST", 6, (178, 34, 34)), ("ASIA", 5, (216, 110, 30)),
           ("AMERICAS", 8, (110, 60, 160)), ("AFRICA", 4, (40, 130, 70)), ("OCEANIA", 1, (20, 140, 150)), ("WORLD", 2, (90, 90, 96))]
total = sum(c for _, c, _ in regions)
widths = [max(64, 996 * c / total) for _, c, _ in regions]
scale = 996 / sum(widths)
widths = [wd * scale for wd in widths]
widths[0] -= 16; widths[5] += 10; widths[6] += 6
rx = 14
for (nm, c, col), wd in zip(regions, widths):
    d.polygon([(X(rx + 8), X(RY)), (X(rx + wd - 2), X(RY)), (X(rx + wd - 8), X(RY + 16)), (X(rx + 2), X(RY + 16))], fill=col)
    _lab = f"{nm} {c}"
    _sz = 9.0
    while _sz > 6.5 and tlen(_lab, F(SANS_B, _sz)) > wd - 17:
        _sz -= 0.5
    text(rx + wd / 2 - 2, RY + 2.5 + (9 - _sz) * 0.35, _lab, F(SANS_B, _sz), WHITE, anchor="ma")
    rx += wd
# ---- black timeline bar
TY = RY + 20
rect([14, TY, 1010, TY + 17], fill=(12, 12, 14))
tx = 20
text(tx, TY + 3.5, "UTC", F(SANS_B, 9), (255, 120, 100))
tx += 34
for t, s in S.TIMELINE:
    text(tx, TY + 3.5, t, F(SANS_B, 9), (250, 200, 90))
    tx += tlen(t, F(SANS_B, 9)) + 4
    text(tx, TY + 3.5, s.upper(), F(SANS, 9), WHITE)
    tx += tlen(s.upper(), F(SANS, 9)) + 14

# ---- leads
LZ = TY + 27
L1, L2, L3 = S.LEADS
LEAD_ART = [("art", "rally", "CHIP RALLY UNWINDS", "NASDAQ FUT -1.11%"),
            ("art", "deal", None, None),
            ("illus", "strike", "DAWN STRIKE", "96 DRONES LAUNCHED")]
LW3 = (1024 - 28 - 2 * 11) / 3
for i, st in enumerate([L1, L2, L3]):
    x = 14 + i * (LW3 + 11)
    kind, key, ban, chip = LEAD_ART[i]
    if kind == "art":
        art(key, x, LZ, LW3, 112)
    else:
        illus(key, x, LZ, LW3, 112)
    if ban:
        banner(x, LZ, ban, RED, 15)
    if chip:
        chip_r(x + LW3, LZ + 88, chip, size=12)
    loc_line(x, LZ + 118, LW3, st["n"], st["loc"], st["cert"])
    yy = para(x, LZ + 136, st["head"], F(SERIF_B, 20), LW3, INK, leading=1.1, max_lines=3)
    para(x, yy + 3, st["body"], F(SANS, 9.5), LW3, (52, 50, 46), leading=1.2, max_lines=3)
rule(LZ + 235, wdt=2)

# ---- mids: 2 rows x 5 cards
MZ = LZ + 256
MW2 = (1024 - 28 - 4 * 12) / 5
MH2 = 158
ILLUS_KINDS = {"mic2": "talks", "gaza": "gaza", "boat2": "boat", "gavel": "hall", "tariff": "tariff", "cricket2": "cricket", "mine2": "mine", "oil2": "oil"}
CERTS = {4: "REPORTED", 5: "REPORTED", 6: "REPORTED", 7: "OFFICIAL", 8: "REPORTED", 9: "REPORTED", 10: "REPORTED", 11: "CONFIRMED", 12: "REPORTED", 13: "OFFICIAL"}
for idx, st in enumerate(S.MIDS):
    r, c = divmod(idx, 5)
    x = 14 + c * (MW2 + 12)
    y = MZ + r * (MH2 + 8)
    kind = st["art"]
    if kind in ILLUS_KINDS:
        illus(ILLUS_KINDS[kind], x, y, MW2, 48)
        banner(x, y, st["kicker"], (14, 20, 36), 11.5)
    else:
        art(kind, x, y, MW2, 48)
    MID_CHIPS = {5: "7 DEAD", 7: "4TH SINCE 2025", 9: "16 PARTNERS", 11: "188-2", 13: "4 PROVINCES"}
    if st["n"] in MID_CHIPS:
        chip_r(x + MW2, y + 26, MID_CHIPS[st["n"]], size=9.5)
    loc_line(x, y + 53, MW2, st["n"], st["loc"], CERTS[st["n"]])
    yy = para(x, y + 70, st["head"], F(SERIF_B, 13.5), MW2, INK, leading=1.1, max_lines=3)
    para(x, yy + 2, st["body"], F(SANS, 9), MW2, (52, 50, 46), leading=1.18, max_lines=3)
    if r == 0:
        rule(y + MH2 + 4, x0=14, x1=1010, wdt=1, col=(196, 188, 168))
rule(MZ + 2 * MH2 + 6, wdt=2)

import re as _re
def _also_words(st):
    ws = [(st["where"] + ":", F(SANS_B, 9.3), INK)]
    for tok in st["text"].split():
        bold = bool(_re.search(r"\d", tok))
        ws.append((tok, F(SANS_B, 9.3) if bold else F(SANS, 9.3), INK))
    return ws

def para_runs(x, y, words, max_w, leading=1.08, max_lines=2):
    lines_, cur, curw = [], [], 0.0
    for w, fnt, col in words:
        ww = tlen(w, fnt); sp = tlen(" ", fnt)
        if cur and curw + sp + ww > max_w:
            lines_.append(cur); cur, curw = [], 0.0
        cur.append((w, fnt, col)); curw += (sp if curw else 0) + ww
    if cur:
        lines_.append(cur)
    lh = 9.3 * leading
    for i, ln in enumerate(lines_[:max_lines]):
        cx = x
        for j, (w, fnt, col) in enumerate(ln):
            if j:
                cx += tlen(" ", fnt)
            text(cx, y + i * lh, w, fnt, col)
            cx += tlen(w, fnt)
    return y + min(len(lines_), max_lines) * lh

# ---- bottom: map + also
BZ = MZ + 2 * MH2 + 22
text(14, BZ, "WHERE IT HAPPENED", F(SANS_B, 11.5), RED)
text(370, BZ, S.ALSO_TITLE, F(SANS_B, 11.5), RED)
rule(BZ + 17)
MAP_X, MAP_Y, MAP_W, MAP_H = 14, BZ + 23, 342, 138
rect([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=(232, 238, 244))
# real world map: land mask rasterised from country polygons (Natural Earth via world.geo.json)
import json as _json
from PIL import ImageDraw as _IDraw
_mask = _Img.new("L", (int(MAP_W * SS), int(MAP_H * SS)), 0)
_md = _IDraw.Draw(_mask)
def _proj(lon, lat):
    return ((lon + 180) / 360 * MAP_W * SS, (85 - lat) / 145 * MAP_H * SS)
try:
    _geo = _json.load(open("assets/world.geo.json"))
    for _feat in _geo["features"]:
        _g = _feat["geometry"]
        if not _g:
            continue
        _polys = _g["coordinates"] if _g["type"] == "MultiPolygon" else [_g["coordinates"]]
        for _poly in _polys:
            for _ring in _poly:
                _pts = [_proj(lon, lat) for lon, lat in _ring]
                if len(_pts) > 2:
                    _md.polygon(_pts, fill=255)
except Exception:
    pass
_mp = _mask.load()
step = 6
for gx in range(int(MAP_X) + 3, int(MAP_X + MAP_W) - 2, step):
    for gy in range(int(MAP_Y) + 3, int(MAP_Y + MAP_H) - 2, step):
        sx, sy = int((gx - MAP_X) * SS), int((gy - MAP_Y) * SS)
        if _mp[sx, sy]:
            d.ellipse([X(gx), X(gy), X(gx + 2.4), X(gy + 2.4)], fill=(120, 140, 170))
PINS_GEO = [(1, -74.0, 40.7), (2, 2.35, 48.9), (3, 35.2, 47.8), (4, 37.6, 55.8), (5, 34.3, 31.4),
            (6, -17.4, 14.7), (7, 116.4, 39.9), (8, -77.0, 38.9), (9, -77.0, 38.9), (10, -66.9, 10.5),
            (11, 151.2, -33.9), (12, 15.3, -4.3), (13, 44.4, 33.3)]
for n, lon, lat in PINS_GEO:
    fx, fy = (lon + 180) / 360, (85 - lat) / 145
    if n == 9:
        fx += 0.012; fy += 0.012
    if n == 1:
        fx += 0.014; fy -= 0.016
    if n == 3:
        fx -= 0.010; fy += 0.012
    if n == 5:
        fx -= 0.012; fy += 0.008
    px, py = MAP_X + fx * MAP_W, MAP_Y + fy * MAP_H
    d.ellipse([X(px - 8), X(py - 8), X(px + 8), X(py + 8)], fill=RED, outline=(255, 255, 255), width=1)
    text(px, py + 0.5, str(n), F(SANS_B, 8.5), (255, 255, 255), anchor="mm")
text(MAP_X, MAP_Y + MAP_H + 5, "pins: stories 1–13, at their real locations  •  dots: land", F(SANS, 8.5), GREY)
AX, AW = 370, 640
colw = (AW - 18) / 2
items = S.ALSO
half = (len(items) + 1) // 2
for ci, chunk in enumerate([items[:half], items[half:]]):
    x = AX + ci * (colw + 18)
    y = BZ + 20
    for st in chunk:
        num_badge(x, y + 5, st["n"], NAVY, r=7)
        yy = para_runs(x + 19, y + 4.5, _also_words(st), colw - 19)
        _lines = round((yy - y - 4.5) / 10.04)
        y = y + max(_lines * 10.04, 13) + 1.8

# ---- date check + legend
FY = 978
rect([14, FY, 1010, FY + 27], outline=RED, width=1.5)
text(22, FY + 4, "DATE CHECK", F(SANS_B, 10.5), RED)
para(108, FY + 3.5, S.DATE_CHECK, F(SANS, 9), 890, (52, 50, 46), leading=1.15, max_lines=2)
text(14, FY + 33, "REPORTED = carried by wires or officials  •  OFFICIAL = an authority's own word  •  CLAIM = one side says  •  " + S.SOURCES, F(SANS, 8.3), GREY)

img = img.resize((1024, 1024), Image.LANCZOS)
img.save("entry.png")
print("saved entry.png")
