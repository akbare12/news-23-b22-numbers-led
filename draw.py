#!/usr/bin/env python3
"""news-23 b22 numbers-led: draw the front page with PIL (stdlib + Pillow)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 246, 236)          # warm paper
INK = (20, 20, 20)
RED = (178, 34, 34)
NAVY = (18, 38, 66)
BLUE = (30, 80, 160)
TEAL = (0, 110, 110)
ORANGE = (200, 100, 0)
PURPLE = (110, 60, 140)
BROWN = (140, 100, 40)
GREY = (110, 110, 110)
LIGHT = (238, 232, 220)
CARD_BG = (255, 253, 247)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(draw, text, f):
    b = draw.textbbox((0, 0), text, font=f)
    return b[2] - b[0]


def wrap(draw, text, f, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(draw, t, f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, f, maxw, fill=INK, lh=None, max_lines=None):
    lines = wrap(draw, text, f, maxw)
    if max_lines:
        lines = lines[:max_lines]
    if lh is None:
        lh = int(f.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def chip(draw, x, y, label, fill):
    f = font(F_SANS_B, 9)
    w = tw(draw, label, f) + 10
    draw.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    draw.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


REGIONS = [
    ("NORTH AMERICA", 8, BLUE),
    ("EUROPE", 6, ORANGE),
    ("MIDDLE EAST", 6, PURPLE),
    ("ASIA-PACIFIC", 6, TEAL),
    ("AFRICA", 3, BROWN),
    ("WORLD", 2, GREY),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- top red rule ----
    d.rectangle([0, 0, W, 6], fill=RED)

    # ---- masthead ----
    f_mast = font(F_SERIF_B, 46)
    d.text((14, 10), "THE WORLD TODAY", font=f_mast, fill=INK)
    f_sr = font(F_SANS_B, 15)
    d.text((W - 14 - tw(d, "31 STORIES", f_sr), 14), "31 STORIES", font=f_sr, fill=INK)
    d.text((W - 14 - tw(d, "6 REGIONS", f_sr), 34), "6 REGIONS", font=f_sr, fill=INK)

    # ---- date line ----
    f_date = font(F_SANS_B, 17)
    d.text((14, 62), "MONDAY 23 NOVEMBER 2026", font=f_date, fill=RED)
    f_kick = font(F_SANS_B, 11)
    kr = "AI ROUT  ·  AI RULES  ·  POWER SHIFT"
    d.text((W - 14 - tw(d, kr, f_kick), 66), kr, font=f_kick, fill=(90, 90, 90))
    d.line([(14, 84), (W - 14, 84)], fill=INK, width=2)

    # ---- number grid 2x5 ----
    nums = [
        ("-3.3%", "KOSPI"),
        ("5.3", "US-CHINA GAP"),
        ("11,762", "EBOLA CASES"),
        ("10T WON", "SEOUL FUND"),
        ("2%", "BILLIONAIRE TAX"),
        ("$450M", "SKUBAL DEAL"),
        ("165", "MISSILES / WEEK"),
        ("12,000", "CLEARED MANCHESTER"),
        ("264 KG", "EXPLOSIVES"),
        ("$107.3B", "ANTHROPIC IPO"),
    ]
    gx, gy, cw, ch = 14, 90, 198, 44
    f_num = font(F_SANS_B, 25)
    f_numlab = font(F_SANS_B, 9)
    for i, (n, lab) in enumerate(nums):
        r, c = divmod(i, 5)
        x = gx + c * cw
        y = gy + r * ch
        if c > 0:
            d.line([(x - 3, y + 4), (x - 3, y + ch - 6)], fill=(200, 192, 178), width=1)
        d.text((x + (cw - tw(d, n, f_num)) // 2, y), n, font=f_num, fill=RED)
        d.text((x + (cw - tw(d, lab, f_numlab)) // 2, y + 29), lab, font=f_numlab, fill=INK)
    d.line([(14, 182), (W - 14, 182)], fill=INK, width=2)

    # ---- region bar ----
    ry, rh = 186, 20
    total = sum(c for _, c, _ in REGIONS)
    x = 14
    f_reg = font(F_SANS_B, 10)
    for name, cnt, col in REGIONS:
        w = int((W - 28) * cnt / total)
        d.rectangle([x, ry, x + w - 1, ry + rh], fill=col)
        label = f"{name} {cnt}"
        d.text((x + (w - tw(d, label, f_reg)) // 2, ry + 4), label, font=f_reg, fill=(255, 255, 255))
        x += w

    # ---- UTC strip ----
    uy = 210
    d.rectangle([14, uy, W - 14, uy + 20], fill=NAVY)
    f_utc = font(F_SANS_B, 10)
    items = ["THE DAY IN UTC", "~00:00 ASIA OPENS", "06:30 KOSPI -3.3%",
             "~09:00 SEOUL FUND", "14:30 WALL ST +3%", "~16:00 GUTERRES",
             "~21:00 FBI HACK", "(~ = APPROX.)"]
    xx = 22
    d.text((xx, uy + 4), items[0], font=font(F_SANS_B, 10), fill=(255, 210, 90))
    xx += tw(d, items[0], f_utc) + 14
    for it in items[1:]:
        d.text((xx, uy + 4), it, font=f_utc, fill=(255, 255, 255))
        xx += tw(d, it, f_utc) + 12

    # ---- hero scenes ----
    hy = 236
    hw = 326
    heroes = [
        dict(num=1, kick="#1 ASIA · MARKETS", title="AI ROUT HITS ASIA",
             body="Kospi closes 4,708.54, sheds 161 pts. Samsung -3.1%, SK Hynix -2.5%. AI sell-off spreads from Wall Street.",
             src="Yonhap · Korea JoongAng", chip=("REPORTED", (0, 130, 60)), scene="kospi"),
        dict(num=2, kick="#2 WORLD · UNITED NATIONS", title="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
             body="UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
             src="UN News · Reuters", chip=("REPORTED", (0, 130, 60)), scene="guterres"),
        dict(num=3, kick="#3 ASIA-PACIFIC · POWER", title="US LEAD OVER CHINA AT RECORD LOW",
             body="Gap 5.3 narrowest since 2018. US diplomatic influence -6 to 76.7. India third at 40.5.",
             src="Lowy Institute", chip=("REPORTED", (0, 130, 60)), scene="power"),
    ]
    f_hkick = font(F_SANS_B, 9)
    f_htitle = font(F_SANS_B, 15)
    f_hbody = font(F_SANS, 10)
    f_hsrc = font(F_SANS, 9)
    for i, h in enumerate(heroes):
        x = 14 + i * (hw + 8)
        # scene box
        d.rectangle([x, hy, x + hw, hy + 118], fill=NAVY if h["scene"] != "power" else (245, 240, 228))
        if h["scene"] == "kospi":
            # skyline
            import random
            rnd = random.Random(7)
            for bx in range(x + 8, x + hw - 8, 22):
                bh = rnd.randint(28, 62)
                d.rectangle([bx, hy + 118 - bh, bx + 18, hy + 118], fill=(30, 55, 90))
                for wy in range(hy + 118 - bh + 5, hy + 112, 10):
                    for wx in range(bx + 3, bx + 16, 7):
                        if rnd.random() < 0.6:
                            d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 90))
            pts = [(x + 14, hy + 26), (x + 70, hy + 34), (x + 130, hy + 30),
                   (x + 190, hy + 52), (x + 250, hy + 66), (x + 312, hy + 96)]
            d.line(pts, fill=(255, 80, 80), width=3)
            for px, py in pts:
                d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255), outline=(255, 80, 80))
            f_big = font(F_SANS_B, 30)
            d.text((x + hw - tw(d, "-3.3%", f_big) - 10, hy + 6), "-3.3%", font=f_big, fill=(255, 80, 80))
            f_int = font(F_SANS_B, 10)
            d.text((x + 8, hy + 6), "intraday -5.8%", font=f_int, fill=(255, 255, 255))
        elif h["scene"] == "guterres":
            # globe
            cx, cy, r = x + 62, hy + 58, 42
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 200))
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
            d.ellipse([cx - 16, cy - r, cx + 16, cy + r], outline=(255, 255, 255), width=1)
            d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=1)
            # network nodes
            import random
            rnd = random.Random(11)
            nodes = []
            for _ in range(7):
                nx = rnd.randint(x + 130, x + hw - 16)
                ny = rnd.randint(hy + 10, hy + 108)
                nodes.append((nx, ny))
            for a in range(len(nodes)):
                for b in range(a + 1, len(nodes)):
                    d.line([nodes[a], nodes[b]], fill=(120, 170, 220), width=1)
            for nx, ny in nodes:
                d.ellipse([nx - 4, ny - 4, nx + 4, ny + 4], fill=(255, 210, 90))
            # podium silhouette
            d.rectangle([x + 150, hy + 96, x + 190, hy + 118], fill=(10, 20, 36))
            d.ellipse([x + 164, hy + 82, x + 176, hy + 96], fill=(10, 20, 36))
            f_del = font(F_SANS_B, 10)
            d.rectangle([x + hw - 118, hy + 6, x + hw - 8, hy + 22], fill=(255, 210, 90))
            d.text((x + hw - 112, hy + 8), "150 DELEGATES", font=f_del, fill=INK)
        else:
            f_pt = font(F_SANS_B, 12)
            d.text((x + 8, hy + 6), "ASIA POWER INDEX 2026", font=f_pt, fill=INK)
            d.text((x + 8, hy + 30), "US", font=font(F_SANS_B, 12), fill=INK)
            d.rectangle([x + 62, hy + 30, x + 62 + 190, hy + 46], fill=BLUE)
            d.text((x + 258, hy + 30), "78.9", font=font(F_SANS_B, 12), fill=INK)
            d.text((x + 8, hy + 56), "CHINA", font=font(F_SANS_B, 12), fill=INK)
            d.rectangle([x + 62, hy + 56, x + 62 + 176, hy + 72], fill=RED)
            d.text((x + 244, hy + 56), "73.6", font=font(F_SANS_B, 12), fill=INK)
            d.text((x + 8, hy + 82), "INDIA", font=font(F_SANS_B, 11), fill=INK)
            d.rectangle([x + 66, hy + 82, x + 66 + 98, hy + 96], fill=GREY)
            d.text((x + 170, hy + 82), "40.5", font=font(F_SANS_B, 11), fill=INK)
            d.text((x + 8, hy + 100), "GAP 5.3", font=font(F_SANS_B, 13), fill=RED)
            d.text((x + 84, hy + 102), "narrowest since 2018", font=font(F_SANS, 10), fill=INK)
        # text under scene
        ty = hy + 124
        d.text((x, ty), h["kick"], font=f_hkick, fill=RED)
        ty += 13
        ty = draw_wrapped(d, x, ty, h["title"], f_htitle, hw, fill=INK, lh=17, max_lines=2)
        ty += 2
        ty = draw_wrapped(d, x, ty, h["body"], f_hbody, hw, fill=(50, 50, 50), lh=12, max_lines=3)
        d.text((x, ty + 2), "Source: " + h["src"], font=f_hsrc, fill=(100, 100, 100))
        chip(d, x + hw - 74, ty + 1, h["chip"][0], h["chip"][1])

    # ---- 10 small cards ----
    cards = [
        (4, "SPORT · US", "Skubal signs $450M Mets deal", "Two-time Cy Young winner, nine years — the largest ever for a pitcher.", "ESPN", "REPORTED", (0, 130, 60), BLUE),
        (5, "TECH · US", "Anthropic IPO: $107.3B, largest ever", "Claude maker raised at $83 a share on 19 Nov; debut close $97.17.", "Bloomberg", "REPORTED", (0, 130, 60), TEAL),
        (6, "EUROPE · WAR", "Poland: 3 Russian missiles crossed airspace", "Kyiv says three Kh-101 entered Poland on Friday; Tusk: provocation.", "AP", "CLAIM", (200, 140, 0), ORANGE),
        (7, "EUROPE · SECURITY", "Intel warns of Russian nuclear satellite", "Moscow built a satellite to carry a nuclear warhead; launch possible next month.", "Bloomberg", "CLAIM", (200, 140, 0), ORANGE),
        (8, "EUROPE · ECONOMY", "Paris: 100+ back 2% billionaire tax", "Economists, politicians and unions rally behind France's 2% minimum wealth tax.", "AFP", "REPORTED", (0, 130, 60), ORANGE),
        (9, "EUROPE · UK", "Manchester: 12,000 cleared after scare", "Substance scare empties arena district; no casualties reported.", "AP", "REPORTED", (0, 130, 60), PURPLE),
        (10, "EUROPE · WAR", "Zelenskyy: 165 Russian missiles in a week", "Kyiv says Moscow fired 165 missiles in seven days as US delays Patriots.", "Kyiv", "CLAIM", (200, 140, 0), ORANGE),
        (11, "WORLD · CLIMATE", "COP31: the day after", "Sunday's collapse — 194 nations reject the Antalya pact — draws fury; Guterres 'profoundly frustrated'.", "CNN", "REPORTED", (0, 130, 60), GREY),
        (12, "AFRICA · LIBYA", "Benghazi: UN demands probe of port attacks", "Drones hit two Russian ships; UN calls for an investigation.", "UN News", "CLAIM", (200, 140, 0), BROWN),
        (13, "MIDDLE EAST · ISRAEL", "Israel unity talks resume", "Likud and Gantz's Yesh Atid return to the table after Sunday's stall.", "Reuters", "ONGOING", (30, 110, 180), PURPLE),
    ]
    cy0, chh = 470, 108
    cw2 = 196
    f_ckick = font(F_SANS_B, 8)
    f_ctitle = font(F_SANS_B, 11)
    f_cbody = font(F_SANS, 9)
    f_csrc = font(F_SANS, 8)
    for i, (num, kick, title, body, src, lab, labcol, col) in enumerate(cards):
        r, c = divmod(i, 5)
        x = 14 + c * (cw2 + 4)
        y = cy0 + r * (chh + 6)
        d.rectangle([x, y, x + cw2, y + chh], fill=CARD_BG, outline=(200, 192, 178))
        # strip
        d.rectangle([x, y, x + cw2, y + 14], fill=col)
        d.text((x + 4, y + 3), f"#{num}", font=font(F_SANS_B, 8), fill=(255, 255, 255))
        d.text((x + 26, y + 3), kick, font=f_ckick, fill=(255, 255, 255))
        ty = y + 17
        ty = draw_wrapped(d, x + 4, ty, title, f_ctitle, cw2 - 8, fill=INK, lh=13, max_lines=2)
        ty = draw_wrapped(d, x + 4, ty + 1, body, f_cbody, cw2 - 8, fill=(50, 50, 50), lh=11, max_lines=3)
        d.text((x + 4, y + chh - 13), src, font=f_csrc, fill=(100, 100, 100))
        chip(d, x + cw2 - 62, y + chh - 14, lab, labcol)

    # ---- map + ALSO ----
    my = 700
    map_x, map_w = 14, 600
    d.text((map_x, my), "THE WORLD — WHERE IT HAPPENED", font=font(F_SANS_B, 12), fill=RED)
    d.text((map_x, my + 15), "PIN = STORY NUMBER", font=font(F_SANS_B, 8), fill=(100, 100, 100))
    mx0, my0, mx1, my1 = map_x, my + 30, map_x + map_w, my + 150
    d.rectangle([mx0, my0, mx1, my1], fill=(225, 235, 240), outline=(180, 190, 200))
    # graticule
    for gx2 in range(mx0 + 60, mx1, 60):
        d.line([(gx2, my0), (gx2, my1)], fill=(200, 210, 220), width=1)
    for gy2 in range(my0 + 34, my1, 34):
        d.line([(mx0, gy2), (mx1, gy2)], fill=(200, 210, 220), width=1)
    # rough continents (simple blobs)
    d.polygon([(mx0 + 30, my0 + 30), (mx0 + 120, my0 + 18), (mx0 + 150, my0 + 45),
               (mx0 + 120, my0 + 80), (mx0 + 60, my0 + 78), (mx0 + 28, my0 + 55)], fill=(232, 220, 190))  # N America
    d.polygon([(mx0 + 60, my0 + 95), (mx0 + 110, my0 + 88), (mx0 + 130, my0 + 115),
               (mx0 + 100, my0 + 130), (mx0 + 62, my0 + 122)], fill=(232, 220, 190))  # S America
    d.polygon([(mx0 + 290, my0 + 18), (mx0 + 360, my0 + 12), (mx0 + 375, my0 + 40),
               (mx0 + 340, my0 + 62), (mx0 + 300, my0 + 55)], fill=(232, 220, 190))  # Europe
    d.polygon([(mx0 + 300, my0 + 62), (mx0 + 370, my0 + 60), (mx0 + 380, my0 + 105),
               (mx0 + 340, my0 + 135), (mx0 + 305, my0 + 110)], fill=(232, 220, 190))  # Africa
    d.polygon([(mx0 + 380, my0 + 15), (mx0 + 560, my0 + 10), (mx0 + 575, my0 + 55),
               (mx0 + 520, my0 + 95), (mx0 + 430, my0 + 85), (mx0 + 385, my0 + 50)], fill=(232, 220, 190))  # Asia
    d.polygon([(mx0 + 520, my0 + 118), (mx0 + 580, my0 + 112), (mx0 + 585, my0 + 132),
               (mx0 + 530, my0 + 136)], fill=(232, 220, 190))  # Australia
    d.text((mx0 + 6, my1 - 12), "N ↑", font=font(F_SANS_B, 9), fill=INK)

    def lonlat(lon, lat, dx=0, dy=0):
        px = mx0 + (lon + 170) / 360.0 * map_w + dx
        py = my0 + (75 - lat) / 130.0 * (my1 - my0) + dy
        return px, py

    pins = [
        (1, 127, 37.5, -12, -8, False), (2, -59.6, 13.1, 0, 0, False),
        (3, -150, -30, 0, 0, False), (4, -74, 40.7, 0, -8, False),
        (5, -122.4, 37.8, 0, 0, False), (6, 19, 52, 0, -8, True),
        (7, 37.6, 55.7, 0, 0, True), (8, 2.35, 48.85, 0, 0, False),
        (9, -2.24, 53.48, -6, -4, False), (10, 30.5, 50.45, 8, -8, True),
        (11, 30.7, 36.9, 4, 10, False), (12, 20.07, 32.1, 10, 2, True),
        (13, 35.2, 31.8, -12, -10, False), (14, 34.45, 31.5, 10, 8, False),
        (15, 35.2, 32.0, -14, 2, False), (16, 51.4, 35.7, 0, 0, False),
        (17, 35.5, 33.9, 0, -12, False), (18, 50.6, 26.2, 0, 0, False),
        (19, 32.5, 15.6, 0, 0, False), (20, 29.5, 1.5, 0, 0, False),
        (21, 90.4, 23.8, 0, 0, False), (22, 127, 37.5, 12, -6, False),
        (23, 127, 37.5, -12, 8, False), (24, 116.4, 39.9, 0, 0, False),
        (25, 127, 37.5, 10, 10, False), (26, -77, 38.9, -10, -6, False),
        (27, -77, 38.9, 10, -6, False), (28, -77, 38.9, 0, 10, False),
        (29, -74, 40.7, 0, 8, False), (30, -105, 39.7, 0, 0, False),
        (31, -100, 38, 0, 0, False),
    ]
    f_pin = font(F_SANS_B, 8)
    for num, lon, lat, dx, dy, claim in pins:
        px, py = lonlat(lon, lat, dx, dy)
        col = (200, 140, 0) if claim else (178, 34, 34)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col, outline=(255, 255, 255), width=1)
        t = str(num)
        d.text((px - tw(d, t, f_pin) / 2, py - 5), t, font=f_pin, fill=(255, 255, 255))

    # ALSO list — two columns so it ends above DATE CHECK
    ax = 630
    d.text((ax, my), "ALSO ON MONDAY — 18 MORE STORIES", font=font(F_SANS_B, 12), fill=RED)
    also_cols = [
        (ax, [
            ("MIDDLE EAST", RED, [
                (14, "Gaza: two killed in Israeli strike"),
                (15, "West Bank: settler attacks hit villages"),
                (16, "Iran war: no deal in sight"),
                (17, "Lebanon seizes 264 kg of explosives"),
                (18, "Bahrain: Iranian strike hits plant"),
            ]),
            ("AFRICA", BROWN, [
                (19, "Sudan drones downed over Khartoum"),
                (20, "DRC: fighting traps Ebola teams"),
            ]),
        ]),
        (824, [
            ("ASIA-PACIFIC", TEAL, [
                (21, "Bangladesh: Hasina jailed if returns"),
                (22, "Seoul minister quits over AI exam"),
                (23, "SK Telecom -7.3%, Anthropic hype cools"),
                (24, "China eases margin rules to calm rout"),
                (25, "Seoul readies 10T-won stabilisation"),
            ]),
            ("NORTH AMERICA", BLUE, [
                (26, "Bessent demands Nvidia answers"),
                (27, "FBI probes hack of police database"),
                (28, "Trump: Iran strikes may resume"),
                (29, "US futures jump 3% holiday week"),
                (30, "Tom Jackson dies at 75"),
                (31, "States sue SpaceX over AI claims"),
            ]),
        ]),
    ]
    f_also_h = font(F_SANS_B, 10)
    f_also = font(F_SANS, 9)
    for col_x, groups in also_cols:
        ay = my + 18
        for name, col, items2 in groups:
            d.text((col_x, ay), name, font=f_also_h, fill=col)
            ay += 12
            for num, txt in items2:
                d.text((col_x, ay), f"{num}  {txt}", font=f_also, fill=INK)
                ay += 11
            ay += 3

    # ---- DATE CHECK ----
    dy0 = 884
    d.rectangle([14, dy0, W - 14, dy0 + 66], outline=RED, width=2, fill=(255, 240, 240))
    f_dc = font(F_SANS_B, 11)
    d.text((22, dy0 + 5), "DATE CHECK", font=f_dc, fill=RED)
    d.text((22, dy0 + 20), "Every story above happened or was first reported on Monday 23 November 2026.",
           font=font(F_SANS, 10), fill=INK)
    d.text((W - 14 - tw(d, "WIRES READ UP TO 23:00 UTC", font(F_SANS_B, 9)), dy0 + 6),
           "WIRES READ UP TO 23:00 UTC", font=font(F_SANS_B, 9), fill=RED)
    f_dcl = font(F_SANS, 9)
    draw_wrapped(d, 22, dy0 + 34,
                 "LEFT OUT (not 23 Nov): Democrats reach 258 (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) · EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov).",
                 f_dcl, W - 44, fill=INK, lh=11, max_lines=1)
    draw_wrapped(d, 22, dy0 + 50,
                 "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff.",
                 f_dcl, W - 44, fill=INK, lh=11, max_lines=1)

    # ---- footer ----
    fy = 958
    f_f = font(F_SANS, 8)
    d.text((14, fy), "SOURCES: AP · Reuters · Bloomberg · AFP · CNN · ESPN · UN News · WHO · Kyiv · Lowy Institute · Korea JoongAng · Morningstar",
           font=f_f, fill=(100, 100, 100))
    d.text((14, fy + 11), "CONFIRMED = 2+ outlets · REPORTED = carried by a wire · CLAIM = one side alleges · ONGOING = developing.  Red pin = reported · Amber pin = claim (unverified).",
           font=f_f, fill=(100, 100, 100))
    d.text((14, fy + 22), "THE WORLD TODAY · 23 NOV 2026", font=font(F_SANS_B, 8), fill=(100, 100, 100))
    d.text((W - 14 - tw(d, "Scenes are drawn illustrations, not photographs.", f_f), fy + 22),
           "Scenes are drawn illustrations, not photographs.", font=f_f, fill=(100, 100, 100))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
