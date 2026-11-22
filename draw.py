#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news summary image (1024x1024).

Dense broadsheet front page in LIGHT GREY monochrome (bre's standing
style): a big date masthead + sub-deck of the day's three biggest stories,
a region bar with counts, a strip of six key numbers, 3 large illustrated
cards, 10 medium illustrated cards, a numbered "also on" index of 17 more
stories beside a small world map, and a DATE CHECK box naming the other
days' news that was deliberately left out. 30 stories in all, 7 regions,
every one verified against a reputable source on Sunday 22 November 2026
(see BUILD_LOG.md). All illustrations are drawn here in PIL — no AI image
generator, no copied image or text from any other entry. Deterministic:
same output bytes on every run. Output: entry.png next to this script.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Light grey monochrome palette (no colour anywhere).
PAPER = (234, 234, 232)
PANEL = (226, 226, 224)
INK = (26, 26, 26)
DARK = (58, 58, 58)
MID = (110, 110, 110)
LIGHT = (168, 168, 168)
PALE = (205, 205, 203)
WHITE = (250, 250, 250)
NIGHT_T = (52, 54, 60)
NIGHT_B = (104, 106, 114)
MARGIN = 28
CW = W - 2 * MARGIN  # 968 content width


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines."""
    out, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def text_cx(d, cx, y, s, font, fill=INK):
    d.text((cx - d.textlength(s, font=font) / 2, y), s, font=font, fill=fill)


def sky_band(d, x0, y0, x1, y1, top, bot):
    """Vertical grey gradient band."""
    h = max(1, y1 - y0)
    for i in range(h):
        t = i / h
        c = tuple(int(top[j] + (bot[j] - top[j]) * t) for j in range(3))
        d.line([x0, y0 + i, x1, y0 + i], fill=c)


def paper_texture(img):
    """Deterministic newsprint speckle (seeded, same every run)."""
    rng = random.Random(20261122)
    px = img.load()
    for _ in range(4800):
        x, y = rng.randrange(W), rng.randrange(H)
        v = rng.choice((-5, -4, -3, 3, 4, 5))
        r, g, b = px[x, y]
        px[x, y] = (max(0, r + v), max(0, g + v), max(0, b + v))


def chip(d, x, y, s, font):
    """Dark label chip with white text; returns its width."""
    tw = d.textlength(s, font=font)
    w = int(tw) + 12
    d.rectangle([x, y, x + w, y + 17], fill=DARK)
    d.text((x + 6, y + 2), s, font=font, fill=WHITE)
    return w


def card_text(d, x, y, w, kicker, headline, summary, hk_font, hl_font, sm_font):
    """Kicker + wrapped headline + wrapped summary; returns bottom y."""
    d.text((x, y), kicker, font=hk_font, fill=DARK)
    y += 16
    for ln in wrap(d, headline, hl_font, w):
        d.text((x, y), ln, font=hl_font, fill=INK)
        y += 22
    y += 1
    for ln in wrap(d, summary, sm_font, w):
        d.text((x, y), ln, font=sm_font, fill=(74, 74, 74))
        y += 14
    return y


# ---------------------------------------------------------------- art scenes
# Each draws a small grey pictogram inside (x0, y0, x1, y1). All original.

def art_cop31(d, x0, y0, x1, y1):
    """COP31: globe, cracked pact paper, gavel-less empty chair of a deal."""
    sky_band(d, x0, y0, x1, y1, (216, 216, 214), (186, 186, 184))
    gx, gy = x0 + 56, y0 + 48
    d.ellipse([gx - 34, gy - 34, gx + 34, gy + 34], fill=(88, 88, 88))
    d.ellipse([gx - 20, gy - 22, gx - 2, gy - 2], fill=(150, 150, 150))
    d.ellipse([gx + 4, gy + 6, gx + 24, gy + 26], fill=(150, 150, 150))
    d.ellipse([gx + 8, gy - 26, gx + 22, gy - 10], fill=(150, 150, 150))
    # pact paper, torn across the middle
    px0, py0, px1, py1 = x0 + 128, y0 + 14, x0 + 218, y0 + 82
    d.polygon([(px0, py0), (px1, py0), (px1, py1), (px0 + 46, py1),
               (px0 + 38, py1 - 12), (px0 + 22, py1 - 4), (px0, py1 - 12)],
              fill=WHITE, outline=DARK)
    for i, yy in enumerate(range(py0 + 12, py0 + 44, 9)):
        d.line([px0 + 10, yy, px1 - 10 - (10 if i == 2 else 0), yy], fill=MID, width=2)
    d.line([px0 + 8, py1 - 16, px1 - 8, py0 + 18], fill=INK, width=4)
    # thermometer, mercury low
    tx = x0 + 268
    d.rounded_rectangle([tx - 7, y0 + 16, tx + 7, y0 + 62], radius=7,
                        fill=WHITE, outline=DARK)
    d.rectangle([tx - 3, y0 + 52, tx + 3, y0 + 58], fill=DARK)
    d.ellipse([tx - 11, y0 + 56, tx + 11, y0 + 78], fill=DARK)


def art_house(d, x0, y0, x1, y1):
    """US House: capitol dome, columns, ballot box with 258 tally."""
    sky_band(d, x0, y0, x1, y1, (222, 222, 220), (196, 196, 194))
    cx = x0 + 156
    d.polygon([(cx - 52, y0 + 62), (cx - 52, y0 + 44), (cx - 30, y0 + 20),
               (cx - 8, y0 + 14), (cx + 8, y0 + 14), (cx + 30, y0 + 20),
               (cx + 52, y0 + 44), (cx + 52, y0 + 62)], fill=DARK)
    d.rectangle([cx - 3, y0 + 6, cx + 3, y0 + 16], fill=DARK)
    d.ellipse([cx - 6, y0 + 2, cx + 6, y0 + 10], fill=DARK)
    for i in range(-2, 3):
        d.rectangle([cx + i * 22 - 5, y0 + 62, cx + i * 22 + 5, y0 + 86],
                    fill=(120, 120, 120))
    d.rectangle([x0 + 88, y0 + 86, x0 + 224, y0 + 92], fill=DARK)
    # ballot box, right
    bx0, by0 = x0 + 246, y0 + 52
    d.rectangle([bx0, by0, bx0 + 44, by0 + 38], fill=WHITE, outline=DARK, width=2)
    d.rectangle([bx0 - 4, by0 - 8, bx0 + 48, by0], fill=DARK)
    d.line([bx0 + 14, by0 - 4, bx0 + 30, by0 - 4], fill=WHITE, width=3)
    d.text((bx0 + 10, by0 + 12), "258", font=F(SANS_B, 15), fill=INK)


def art_f1(d, x0, y0, x1, y1):
    """Las Vegas GP: night sky, strip lights, race car, chequered flag."""
    sky_band(d, x0, y0, x1, y1, NIGHT_T, NIGHT_B)
    for sx, sy in [(x0 + 30, y0 + 12), (x0 + 90, y0 + 22), (x0 + 170, y0 + 10),
                   (x0 + 250, y0 + 20), (x0 + 290, y0 + 12)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)
    # strip buildings
    for bx, bh in [(x0 + 8, 34), (x0 + 52, 48), (x0 + 108, 30), (x0 + 150, 44),
                   (x0 + 210, 36), (x0 + 258, 50)]:
        d.rectangle([bx, y1 - 30 - bh, bx + 34, y1 - 30], fill=(30, 30, 34))
        d.rectangle([bx + 6, y1 - 30 - bh + 6, bx + 12, y1 - 30 - bh + 12],
                    fill=(220, 220, 220))
    d.rectangle([x0, y1 - 30, x1, y1], fill=(70, 70, 74))
    # race car
    cx, cy = x0 + 150, y1 - 34
    d.polygon([(cx - 52, cy), (cx - 38, cy - 12), (cx + 8, cy - 12),
               (cx + 30, cy - 4), (cx + 52, cy)], fill=(225, 225, 225))
    d.rectangle([cx + 44, cy - 12, cx + 54, cy - 2], fill=(225, 225, 225))
    for wx in (cx - 34, cx + 26):
        d.ellipse([wx - 9, cy - 4, wx + 9, cy + 12], fill=INK)
        d.ellipse([wx - 4, cy + 1, wx + 4, cy + 7], fill=(150, 150, 150))
    # chequered flag, top right
    fx, fy = x1 - 46, y0 + 8
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([fx + c * 9, fy + r * 9, fx + c * 9 + 9, fy + r * 9 + 9],
                            fill=INK)
            else:
                d.rectangle([fx + c * 9, fy + r * 9, fx + c * 9 + 9, fy + r * 9 + 9],
                            fill=WHITE)


def art_bahrain(d, x0, y0, x1, y1):
    """Bahrain: night sky, industrial plant, missile arc, impact flash."""
    sky_band(d, x0, y0, x1, y1, NIGHT_T, (80, 82, 90))
    for sx, sy in [(x0 + 20, y0 + 10), (x0 + 70, y0 + 18), (x0 + 140, y0 + 8)]:
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=WHITE)
    base = y1 - 6
    d.rectangle([x0 + 10, base - 26, x0 + 90, base], fill=(40, 40, 44))
    d.rectangle([x0 + 100, base - 18, x0 + 140, base], fill=(40, 40, 44))
    d.rectangle([x0 + 26, base - 40, x0 + 32, base - 26], fill=(40, 40, 44))
    d.rectangle([x0 + 60, base - 34, x0 + 66, base - 26], fill=(40, 40, 44))
    for wx in range(x0 + 18, x0 + 86, 12):
        d.rectangle([wx, base - 20, wx + 5, base - 14], fill=(230, 230, 230))
    # missile arc + flash
    d.arc([x0 + 90, y0 - 30, x0 + 190, y0 + 50], start=200, end=330, fill=WHITE, width=2)
    fx, fy = x0 + 158, y0 + 26
    for dx, dy in [(0, -12), (9, -9), (12, 0), (9, 9), (0, 12), (-9, 9), (-12, 0), (-9, -9)]:
        d.line([fx, fy, fx + dx, fy + dy], fill=WHITE, width=2)
    d.ellipse([fx - 5, fy - 5, fx + 5, fy + 5], fill=WHITE)


def art_kyiv(d, x0, y0, x1, y1):
    """Kyiv: apartment block, drone above, smoke, one dark window row."""
    sky_band(d, x0, y0, x1, y1, (206, 206, 204), (172, 172, 170))
    bx0, by0 = x0 + 30, y0 + 10
    d.rectangle([bx0, by0, bx0 + 86, y1 - 4], fill=(120, 120, 120))
    d.rectangle([bx0 + 86, y0 + 24, bx0 + 118, y1 - 4], fill=(96, 96, 96))
    for r in range(4):
        for c in range(4):
            wx, wy = bx0 + 8 + c * 20, by0 + 8 + r * 14
            lit = (r * 4 + c) % 3 != 0
            d.rectangle([wx, wy, wx + 10, wy + 8],
                        fill=(240, 240, 240) if lit else (52, 52, 52))
    # smoke
    for sx, sy, sr in [(x0 + 150, y0 + 14, 10), (x0 + 162, y0 + 24, 13),
                       (x0 + 148, y0 + 34, 9)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 150, 150))
    # drone
    dx, dy = x0 + 150, y0 + 48
    d.line([dx - 12, dy - 8, dx + 12, dy + 8], fill=INK, width=2)
    d.line([dx - 12, dy + 8, dx + 12, dy - 8], fill=INK, width=2)
    d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=INK)


def art_liverpool(d, x0, y0, x1, y1):
    """Liverpool 4-0: stands, goal, ball in the net."""
    sky_band(d, x0, y0, x1, y1, (214, 214, 212), (188, 188, 186))
    d.rectangle([x0, y0 + 8, x1, y0 + 30], fill=(70, 70, 70))
    for cx in range(x0 + 8, x1 - 6, 12):
        d.ellipse([cx, y0 + 14, cx + 6, y0 + 20], fill=(200, 200, 200))
    d.rectangle([x0, y1 - 22, x1, y1], fill=(140, 140, 140))
    d.line([x0, y1 - 22, x1, y1 - 22], fill=WHITE, width=2)
    # goal
    gx0, gy0 = x0 + 96, y0 + 34
    d.rectangle([gx0, gy0, gx0 + 84, y1 - 22], outline=WHITE, width=3)
    for vx in range(gx0 + 12, gx0 + 84, 12):
        d.line([vx, gy0, vx, y1 - 22], fill=(225, 225, 225), width=1)
    for hy in range(gy0 + 10, y1 - 22, 10):
        d.line([gx0, hy, gx0 + 84, hy], fill=(225, 225, 225), width=1)
    # ball
    bx, by = gx0 + 60, y1 - 34
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=WHITE, outline=INK)
    d.polygon([(bx, by - 5), (bx + 5, by - 1), (bx + 3, by + 5),
               (bx - 3, by + 5), (bx - 5, by - 1)], fill=INK)


def art_ashes(d, x0, y0, x1, y1):
    """Ashes: pitch, stumps, bat mid-swing, ball."""
    sky_band(d, x0, y0, x1, y1, (218, 218, 216), (190, 190, 188))
    d.rectangle([x0, y1 - 26, x1, y1], fill=(150, 150, 150))
    d.rectangle([x0 + 60, y1 - 26, x0 + 130, y1 - 8], fill=(196, 194, 190))
    # stumps
    sx = x0 + 150
    for i in range(3):
        d.rectangle([sx + i * 7, y1 - 44, sx + i * 7 + 4, y1 - 26], fill=(240, 240, 240))
    d.rectangle([sx, y1 - 47, sx + 18, y1 - 44], fill=(240, 240, 240))
    # bat
    d.polygon([(x0 + 30, y1 - 52), (x0 + 44, y1 - 46), (x0 + 66, y1 - 14),
               (x0 + 54, y1 - 8), (x0 + 32, y1 - 40)], fill=(120, 120, 120))
    d.line([x0 + 30, y1 - 52, x0 + 20, y1 - 62], fill=INK, width=4)
    # ball
    d.ellipse([x0 + 78, y1 - 56, x0 + 90, y1 - 44], fill=(90, 90, 90))


def art_wellington(d, x0, y0, x1, y1):
    """Wellington: scoreboard 720-9, bat, ball, stands."""
    sky_band(d, x0, y0, x1, y1, (216, 216, 214), (188, 188, 186))
    d.rectangle([x0, y0 + 6, x1, y0 + 26], fill=(70, 70, 70))
    for cx in range(x0 + 8, x1 - 6, 12):
        d.ellipse([cx, y0 + 11, cx + 6, y0 + 17], fill=(200, 200, 200))
    # scoreboard (no text: the chip below already names the score)
    sx0, sy0 = x0 + 40, y0 + 32
    d.rectangle([sx0, sy0, sx0 + 104, sy0 + 26], fill=DARK)
    for bx in range(sx0 + 10, sx0 + 96, 16):
        d.rectangle([bx, sy0 + 9, bx + 9, sy0 + 17], fill=(220, 220, 220))
    d.rectangle([x0, y1 - 12, x1, y1], fill=(150, 150, 150))
    d.polygon([(x0 + 130, y1 - 40), (x0 + 142, y1 - 34), (x0 + 160, y1 - 12),
               (x0 + 148, y1 - 8), (x0 + 130, y1 - 28)], fill=(120, 120, 120))
    d.ellipse([x0 + 168, y1 - 34, x0 + 178, y1 - 24], fill=(90, 90, 90))


def art_fire(d, x0, y0, x1, y1):
    """Indonesia fire: factory, chimney, flame, smoke."""
    sky_band(d, x0, y0, x1, y1, (210, 210, 208), (176, 176, 174))
    base = y1 - 4
    d.rectangle([x0 + 14, base - 26, x0 + 110, base], fill=(88, 88, 88))
    d.rectangle([x0 + 116, base - 18, x0 + 150, base], fill=(88, 88, 88))
    d.rectangle([x0 + 30, base - 44, x0 + 38, base - 26], fill=(70, 70, 70))
    for wx in range(x0 + 22, x0 + 104, 14):
        d.rectangle([wx, base - 20, wx + 7, base - 12], fill=(225, 225, 225))
    # flame
    fx = x0 + 132
    d.polygon([(fx - 14, base), (fx - 10, base - 18), (fx - 4, base - 26),
               (fx + 2, base - 14), (fx + 8, base - 24), (fx + 14, base - 8),
               (fx + 12, base)], fill=(60, 60, 60))
    d.polygon([(fx - 6, base), (fx - 3, base - 12), (fx + 3, base - 14),
               (fx + 6, base)], fill=(200, 200, 200))
    for sx, sy, sr in [(x0 + 34, y0 + 10, 9), (x0 + 48, y0 + 18, 11),
                       (x0 + 60, y0 + 8, 8)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(140, 140, 140))


def art_ship(d, x0, y0, x1, y1):
    """Benghazi: sea, cargo ship, smoke column, drone."""
    sky_band(d, x0, y0, x1, y1, (212, 212, 210), (182, 182, 180))
    d.rectangle([x0, y1 - 20, x1, y1], fill=(140, 140, 140))
    for wy in range(y1 - 16, y1 - 2, 6):
        d.line([x0 + 8, wy, x0 + 60, wy], fill=(200, 200, 200), width=2)
        d.line([x1 - 60, wy + 3, x1 - 8, wy + 3], fill=(200, 200, 200), width=2)
    # ship
    sx0, sy = x0 + 46, y1 - 34
    d.polygon([(sx0, sy), (sx0 + 96, sy), (sx0 + 84, sy + 14), (sx0 + 10, sy + 14)],
              fill=(64, 64, 64))
    d.rectangle([sx0 + 18, sy - 16, sx0 + 78, sy], fill=(96, 96, 96))
    d.rectangle([sx0 + 40, sy - 26, sx0 + 52, sy - 16], fill=(64, 64, 64))
    # smoke
    for px, py, pr in [(x0 + 118, y0 + 12, 8), (x0 + 126, y0 + 20, 10),
                       (x0 + 114, y0 + 28, 7)]:
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(120, 120, 120))
    # drone
    dx, dy = x0 + 158, y0 + 18
    d.line([dx - 9, dy - 6, dx + 9, dy + 6], fill=INK, width=2)
    d.line([dx - 9, dy + 6, dx + 9, dy - 6], fill=INK, width=2)
    d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=INK)


def art_shuri(d, x0, y0, x1, y1):
    """Shuri Castle: tiered roofs, sun, steps."""
    sky_band(d, x0, y0, x1, y1, (220, 220, 218), (192, 192, 190))
    d.ellipse([x0 + 138, y0 + 8, x0 + 162, y0 + 32], fill=(120, 120, 120))
    cx = x0 + 92
    base = y1 - 4
    d.rectangle([cx - 46, base - 34, cx + 46, base], fill=(110, 110, 110))
    d.polygon([(cx - 58, base - 34), (cx + 58, base - 34), (cx + 44, base - 48),
               (cx - 44, base - 48)], fill=DARK)
    d.rectangle([cx - 32, base - 62, cx + 32, base - 48], fill=(110, 110, 110))
    d.polygon([(cx - 42, base - 62), (cx + 42, base - 62), (cx + 30, base - 74),
               (cx - 30, base - 74)], fill=DARK)
    d.rectangle([cx - 18, base - 84, cx + 18, base - 74], fill=(110, 110, 110))
    d.polygon([(cx - 26, base - 84), (cx + 26, base - 84), (cx, base - 94)],
              fill=DARK)
    for r in range(3):
        d.rectangle([cx - 8, base - 30 + r * 10, cx + 8, base - 22 + r * 10],
                    fill=(70, 70, 70))
    for sx in (x0 + 12, x1 - 30):
        d.ellipse([sx, base - 10, sx + 16, base + 2], fill=(150, 150, 150))


def art_westbank(d, x0, y0, x1, y1):
    """West Bank: night street, car, flame, moon."""
    sky_band(d, x0, y0, x1, y1, NIGHT_T, (86, 88, 96))
    d.ellipse([x0 + 150, y0 + 8, x0 + 168, y0 + 26], fill=(235, 235, 235))
    d.ellipse([x0 + 156, y0 + 8, x0 + 172, y0 + 26], fill=(86, 88, 96))
    d.rectangle([x0, y1 - 16, x1, y1], fill=(64, 64, 64))
    # car
    cx, cy = x0 + 84, y1 - 22
    d.polygon([(cx - 52, cy), (cx - 40, cy - 12), (cx - 18, cy - 16),
               (cx + 16, cy - 16), (cx + 34, cy - 10), (cx + 52, cy - 4),
               (cx + 52, cy)], fill=(40, 40, 40))
    for wx in (cx - 32, cx + 26):
        d.ellipse([wx - 9, cy - 4, wx + 9, cy + 10], fill=INK)
        d.ellipse([wx - 4, cy + 1, wx + 4, cy + 5], fill=(140, 140, 140))
    # flame above the car
    fx = cx + 6
    d.polygon([(fx - 10, cy - 16), (fx - 7, cy - 30), (fx - 2, cy - 38),
               (fx + 3, cy - 26), (fx + 8, cy - 34), (fx + 10, cy - 16)],
              fill=(220, 220, 220))
    d.polygon([(fx - 4, cy - 16), (fx - 2, cy - 26), (fx + 3, cy - 28),
               (fx + 4, cy - 16)], fill=(120, 120, 120))


def art_psg(d, x0, y0, x1, y1):
    """PSG 3-2: floodlights, goal net, ball, scoreboard."""
    sky_band(d, x0, y0, x1, y1, NIGHT_T, (88, 90, 98))
    for lx in (x0 + 18, x1 - 26):
        d.line([lx + 4, y0 + 6, lx + 4, y0 + 26], fill=(160, 160, 160), width=3)
        d.ellipse([lx - 2, y0 + 2, lx + 10, y0 + 12], fill=WHITE)
    d.rectangle([x0, y1 - 18, x1, y1], fill=(130, 130, 130))
    gx0, gy0 = x0 + 52, y0 + 22
    d.rectangle([gx0, gy0, gx0 + 84, y1 - 18], outline=WHITE, width=3)
    for vx in range(gx0 + 12, gx0 + 84, 12):
        d.line([vx, gy0, vx, y1 - 18], fill=(225, 225, 225), width=1)
    for hy in range(gy0 + 10, y1 - 18, 10):
        d.line([gx0, hy, gx0 + 84, hy], fill=(225, 225, 225), width=1)
    bx, by = gx0 + 26, y1 - 30
    d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=WHITE, outline=INK)
    d.polygon([(bx, by - 4), (bx + 4, by - 1), (bx + 2, by + 4),
               (bx - 2, by + 4), (bx - 4, by - 1)], fill=INK)
    d.text((x0 + 148, y0 + 30), "3-2", font=F(SANS_B, 18), fill=WHITE)


# ---------------------------------------------------------------- world map
CONTINENTS = [
    [(0.02, 0.28), (0.08, 0.12), (0.20, 0.10), (0.28, 0.22), (0.26, 0.38),
     (0.18, 0.42), (0.12, 0.52), (0.06, 0.45)],  # N America
    [(0.28, 0.06), (0.33, 0.08), (0.31, 0.14), (0.27, 0.12)],  # Greenland
    [(0.26, 0.52), (0.33, 0.50), (0.36, 0.60), (0.32, 0.75), (0.28, 0.68),
     (0.25, 0.58)],  # S America
    [(0.46, 0.14), (0.52, 0.10), (0.56, 0.16), (0.54, 0.24), (0.48, 0.26),
     (0.45, 0.20)],  # Europe
    [(0.44, 0.16), (0.46, 0.15), (0.46, 0.19)],  # Britain
    [(0.46, 0.32), (0.54, 0.30), (0.60, 0.36), (0.58, 0.52), (0.52, 0.60),
     (0.47, 0.48), (0.44, 0.38)],  # Africa
    [(0.56, 0.10), (0.70, 0.08), (0.85, 0.12), (0.95, 0.22), (0.92, 0.35),
     (0.82, 0.42), (0.72, 0.38), (0.66, 0.48), (0.60, 0.40), (0.56, 0.28),
     (0.54, 0.18)],  # Asia
    [(0.90, 0.28), (0.92, 0.30), (0.90, 0.36), (0.88, 0.32)],  # Japan
    [(0.82, 0.62), (0.90, 0.60), (0.94, 0.66), (0.90, 0.74), (0.83, 0.72)],  # Australia
    [(0.95, 0.72), (0.97, 0.74), (0.95, 0.78)],  # New Zealand
]
ISLANDS = [(0.78, 0.50), (0.81, 0.53), (0.84, 0.50), (0.80, 0.56)]  # Indonesia
DOTS = {  # story number -> (rx, ry) on the map
    1: (0.565, 0.30), 2: (0.235, 0.33), 3: (0.145, 0.36), 4: (0.615, 0.42),
    5: (0.545, 0.22), 6: (0.465, 0.18), 7: (0.845, 0.70), 8: (0.965, 0.76),
    9: (0.815, 0.55), 10: (0.53, 0.38), 11: (0.885, 0.36), 12: (0.59, 0.40),
    13: (0.49, 0.26),
}


def draw_map(d, x0, y0, x1, y1):
    mw, mh = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(208, 208, 206), outline=DARK)
    for poly in CONTINENTS:
        pts = [(x0 + rx * mw, y0 + ry * mh) for rx, ry in poly]
        d.polygon(pts, fill=(128, 128, 128))
    for rx, ry in ISLANDS:
        d.ellipse([x0 + rx * mw - 3, y0 + ry * mh - 2,
                   x0 + rx * mw + 3, y0 + ry * mh + 2], fill=(128, 128, 128))
    f = F(SANS_B, 7)
    for n, (rx, ry) in DOTS.items():
        cx, cy = x0 + rx * mw, y0 + ry * mh
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=DARK, outline=WHITE)
        s = str(n)
        d.text((cx - d.textlength(s, font=f) / 2, cy - 5), s, font=f, fill=WHITE)


# ---------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top kicker + rule
    d.text((MARGIN, 12), "THE WORLD IN ONE DAY", font=F(SANS_B, 15), fill=INK)
    right = "30 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    d.text((W - MARGIN - d.textlength(right, font=F(SANS_B, 15)), 12), right,
           font=F(SANS_B, 15), fill=INK)
    d.line([MARGIN, 34, W - MARGIN, 34], fill=DARK, width=2)

    # --- masthead
    text_cx(d, W // 2, 40, "Sunday 22 November 2026", F(SERIF, 62))
    text_cx(d, W // 2, 108,
            "COP31 collapses with no deal · Democrats take 258 House seats · "
            "Verstappen wins a 35-lead-change Las Vegas GP",
            F(SERIF_I, 17), fill=(60, 60, 60))

    # --- region bar (widths proportional to story counts, total 968)
    regions = [("EUROPE 9", 9), ("AMERICAS 5", 5), ("MIDDLE EAST 4", 4),
               ("AFRICA 2", 2), ("ASIA 3", 3), ("OCEANIA 4", 4), ("GLOBAL 3", 3)]
    shades = [(58, 58, 58), (105, 105, 105), (150, 150, 150), (190, 190, 190)]
    x = MARGIN
    yb, hb = 130, 22
    for i, (label, n) in enumerate(regions):
        w = int(round(CW * n / 30))
        if i == len(regions) - 1:
            w = W - MARGIN - x
        sh = shades[i % len(shades)]
        d.rectangle([x, yb, x + w - 1, yb + hb], fill=sh)
        fill = WHITE if sh[0] < 140 else INK
        text_cx(d, x + w // 2, yb + 4, label, F(SANS_B, 12), fill=fill)
        x += w

    # --- key numbers strip
    nums = [("258", "Democrats' House seats,\nmost since 1992"),
            ("35", "lead changes in the\nLas Vegas GP"),
            ("123", "Head's runs off\n83 balls, Perth"),
            ("720", "India's record total\nin New Zealand"),
            ("52%", "cholesterol cut by\none-time CRISPR"),
            ("3", "dead in the Indonesia\nfactory fire")]
    col_w = CW // 6
    yn = 160
    for i, (num, lab) in enumerate(nums):
        cx0 = MARGIN + i * col_w
        if i:
            d.line([cx0 - 6, yn + 4, cx0 - 6, yn + 34], fill=PALE, width=1)
        text_cx(d, cx0 + col_w // 2, yn, num, F(SERIF, 30))
        for j, ln in enumerate(lab.split("\n")):
            text_cx(d, cx0 + col_w // 2, yn + 34 + j * 12, ln, F(SANS, 10),
                    fill=(74, 74, 74))
    d.line([MARGIN, yn + 62, W - MARGIN, yn + 62], fill=DARK, width=1)

    # --- 3 large cards
    large = [
        (art_cop31, "COP31: NO DEAL", "1  ANTALYA, TÜRKIYE · CLIMATE",
         "COP31 collapses with no deal",
         "Summit ends Sunday, two days late, after the EU rejects a draft "
         "that never names fossil fuels; the longest COP ever. (CNN, AFP)"),
        (art_house, "258 SEATS", "2  WASHINGTON, USA · POLITICS",
         "Democrats reach 258 House seats",
         "North Carolina win gives Democrats their biggest House majority "
         "since 1992; a net gain of 44 seats. (AP, Reuters)"),
        (art_f1, "VEGAS: VERSTAPPEN", "3  LAS VEGAS, USA · FORMULA 1",
         "Verstappen wins a 35-lead-change thriller",
         "Holds off Norris and Piastri in a slipstreaming Las Vegas GP; 352 "
         "overtakes in 50 laps. (F1, AP)"),
    ]
    yl = 232
    card_w, gap = 312, 16
    for i, (art, ch, kick, head, summ) in enumerate(large):
        x0 = MARGIN + i * (card_w + gap)
        x1 = x0 + card_w
        d.rectangle([x0, yl, x1, yl + 216], outline=(150, 150, 150))
        art(d, x0 + 1, yl + 1, x1 - 1, yl + 91)
        chip(d, x0 + 8, yl + 72, ch, F(SANS_B, 10))
        card_text(d, x0 + 8, yl + 98, card_w - 16, kick, head, summ,
                  F(SANS_B, 10), F(SERIF, 20), F(SANS, 11))

    # --- 10 medium cards, 2 rows of 5
    medium = [
        (art_bahrain, "BAHRAIN HIT", "4  BAHRAIN · CONFLICT",
         "Iran strikes Bahrain site; two hurt",
         "Projectiles hit a civilian industrial site; Gulf states condemn "
         "the attack. (Reuters, AFP)"),
        (art_kyiv, "KYIV: 3 KILLED", "5  DYMER, UKRAINE · WAR",
         "Drone hits flats near Kyiv; 3 killed",
         "Five-storey block struck Sunday; 14 people missing under the "
         "rubble. (AP)"),
        (art_liverpool, "4-0 AT ANFIELD", "6  LIVERPOOL, ENGLAND · FOOTBALL",
         "Liverpool rout Man Utd 4-0",
         "Szoboszlai and Wirtz strike early at Anfield; Hull also beat "
         "Brighton 2-0. (Sportradar)"),
        (art_ashes, "ASHES: 2 DAYS", "7  PERTH, AUSTRALIA · CRICKET",
         "Head's 123 wins Ashes Test in two days",
         "Australia chase 205 in 28.2 overs to beat England by 8 wickets; "
         "Starc takes 10. (Sportskeeda)"),
        (art_wellington, "720-9 DECLARED", "8  WELLINGTON, NZ · CRICKET",
         "India declare on 720-9, a record in NZ",
         "Pant hits 128; New Zealand 119-2 at stumps on day four, still "
         "233 behind. (ICC)"),
        (art_fire, "3 DEAD, 36 MISSING", "9  CIKANDE, INDONESIA · DISASTER",
         "Candy factory fire: 3 dead, 36 missing",
         "Blaze guts a factory in Banten; rescuers search the ruins for "
         "the missing. (AP)"),
        (art_ship, "SHIP HIT", "10  BENGHAZI, LIBYA · CONFLICT",
         "Russian ship hit at Benghazi port",
         "Vessel struck in a suspected Ukrainian drone attack, Libyan "
         "officials say. (BBC)"),
        (art_shuri, "SHURI RESTORED", "11  OKINAWA, JAPAN · CULTURE",
         "Shuri Castle hall rises again",
         "Okinawa celebrates the restored main hall, seven years after "
         "the fire. (AP)"),
        (art_westbank, "WEST BANK ARSON", "12  RAMALLAH, WEST BANK · CONFLICT",
         "Settlers torch cars; Israel opens inquiry",
         "Twelve vehicles burned in four villages overnight; opposition "
         "leader calls it terrorism. (AP)"),
        (art_psg, "PSG 3-2", "13  NICE, FRANCE · FOOTBALL",
         "PSG win 3-2 at Nice, lose Doué",
         "Leaders extend their winning run but star forward Doué goes "
         "off injured. (Ligue 1)"),
    ]
    mw, mgap = 185, 10
    for row in range(2):
        yr = 458 + row * 172
        for j in range(5):
            k = row * 5 + j
            art, ch, kick, head, summ = medium[k]
            x0 = MARGIN + j * (mw + mgap)
            x1 = x0 + mw
            d.rectangle([x0, yr, x1, yr + 162], outline=(150, 150, 150))
            art(d, x0 + 1, yr + 1, x1 - 1, yr + 63)
            chip(d, x0 + 6, yr + 46, ch, F(SANS_B, 9))
            # kicker: shrink to 8px if the full location would overflow
            kf = F(SANS_B, 9)
            if d.textlength(kick, font=kf) > mw - 12:
                kf = F(SANS_B, 8)
            d.text((x0 + 6, yr + 68), kick, font=kf, fill=DARK)
            yy = yr + 82
            for ln in wrap(d, head, F(SERIF, 15), mw - 12):
                d.text((x0 + 6, yy), ln, font=F(SERIF, 15), fill=INK)
                yy += 17
            yy += 1
            for ln in wrap(d, summ, F(SANS, 10), mw - 12):
                d.text((x0 + 6, yy), ln, font=F(SANS, 10), fill=(74, 74, 74))
                yy += 13

    # --- also-on header
    ya = 800
    d.text((MARGIN, ya), "ALSO ON SUNDAY 22 NOVEMBER 2026 — 17 MORE STORIES · 30 IN ALL",
           font=F(SANS_B, 14), fill=INK)
    d.line([MARGIN, ya + 20, W - MARGIN, ya + 20], fill=DARK, width=1)

    # --- map + index
    ym = 828
    d.text((MARGIN, ym), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=INK)
    draw_map(d, MARGIN, ym + 18, 330, ym + 126)

    index = [
        (14, "Warsaw: Russia twice tried to kill a US rapper (AP)"),
        (15, "London: UK and EU strike new deals (OneTurn)"),
        (16, "Europe: Cost-of-living protests spread (Hansen)"),
        (17, "Geneva: UN extends killer-robot work to 2028 (Hansen)"),
        (18, "USA: One-time CRISPR cuts cholesterol 52% (OneTurn)"),
        (19, "Washington: Nvidia faces accounting probe (reports)"),
        (20, "Global: GL.iNet flaw used to infect routers (reports)"),
        (21, "Iowa: Army defies court to detonate explosives (reports)"),
        (22, "Jerusalem: Netanyahu resumes coalition talks (reports)"),
        (23, "Washington: Trump says Iran wants a deal (AP)"),
        (24, "Moscow: Russia grasps US offer on security (AP)"),
        (25, "Khartoum: Drones damage a UN building (OneTurn)"),
        (26, "Rome: Jeweller Paolo Bulgari dies at 89 (AP)"),
        (27, "Melbourne: Charges over fatal CBD stabbing (reports)"),
        (28, "Indonesia: New flying frog species found (reports)"),
        (29, "Sydney: NSW bonds could raise $200m a year (ABC)"),
        (30, "Colombia: Soldier killed in army base attack (Rio Times)"),
    ]
    col_x = [346, 676]
    col_w = 320
    for ci, items in enumerate([index[:9], index[9:]]):
        yy = ym
        for n, txt in items:
            d.text((col_x[ci], yy), f"{n}", font=F(SANS_B, 10), fill=DARK)
            tx = col_x[ci] + 24
            for ln in wrap(d, txt, F(SANS, 10), col_w - 24):
                d.text((tx, yy), ln, font=F(SANS, 10), fill=INK)
                yy += 12
            yy += 2

    # --- DATE CHECK box
    yd = 962
    d.rectangle([MARGIN, yd, W - MARGIN, yd + 38], outline=DARK, width=2)
    d.text((MARGIN + 8, yd + 4), "DATE CHECK", font=F(SANS_B, 11), fill=INK)
    dc = ("Left out as other days' news: the El Chapo Isidro capture (Sat); "
          "the Sparta II drone hit (Sat); BepiColombo reaches Mercury (Sat); "
          "the EU–Indonesia trade deal (Sat); Boca win the Sudamericana (Sat); "
          "the Junín quake (Sat); the ICJ Myanmar ruling (Thu 19 Nov).")
    for j, ln in enumerate(wrap(d, dc, F(SANS, 10), CW - 118)):
        d.text((MARGIN + 108, yd + 4 + j * 12), ln, font=F(SANS, 10),
               fill=(74, 74, 74))

    # --- footer
    d.text((MARGIN, 1008),
           "Every story here happened, or was first reported, on Sunday 22 November 2026 · "
           "Sources named beside each story · All illustrations drawn in code",
           font=F(SANS, 9), fill=(90, 90, 90))

    paper_texture(img)
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
