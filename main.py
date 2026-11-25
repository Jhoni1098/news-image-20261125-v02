#!/usr/bin/env python3
"""news-image-20261125 v02 — evening edition front page.

Draws a one-page newspaper front page summing up the world news of
Wednesday 25 November 2026, as verified from Reuters / AP / Just
Security / ISW reporting of that day. Pure standard library: the PNG
is encoded by hand (zlib + struct), text is rendered with a small
built-in 5x7 bitmap font, and every shape is drawn pixel by pixel.
No network, no randomness, no clock: two runs write identical bytes.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py   (writes out/entry.png)
Grader: writes /output/entry.png
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)
PAPER_DIM = (232, 224, 207)
INK = (22, 22, 22)
GREY = (110, 104, 90)
RED = (172, 32, 28)
SEA1 = (18, 72, 96)
SEA2 = (13, 60, 84)
SEA3 = (9, 48, 70)
FLAME = (232, 92, 18)
FLAME_Y = (244, 176, 44)
SMOKE = (120, 118, 112)
WHITE = (255, 255, 255)
BLACK = (12, 12, 12)
GOLD = (186, 140, 32)
TEAL = (24, 96, 96)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows, each a 5-bit mask, bit 4 = leftmost pixel.
FONT = {
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    "X": (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    "Y": (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F),
    "3": (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 0x0C, 0x0C),
    ",": (0, 0, 0, 0, 0x0C, 0x04, 0x08),
    ":": (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
    ";": (0, 0x0C, 0x0C, 0, 0x0C, 0x04, 0x08),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    "-": (0, 0, 0, 0x0E, 0, 0, 0),
    "/": (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10),
    "%": (0x19, 0x19, 0x02, 0x04, 0x08, 0x13, 0x13),
    "$": (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    "&": (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    "+": (0, 0x04, 0x04, 0x0E, 0x04, 0x04, 0),
    "=": (0, 0, 0x1F, 0, 0x1F, 0, 0),
    "?": (0x0E, 0x11, 0x01, 0x02, 0x04, 0, 0x04),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04),
    '"': (0x0A, 0x0A, 0, 0, 0, 0, 0),
    "|": (0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
}


def glyph(ch):
    # The font carries capitals only; render lower case as capitals,
    # which suits the newspaper style and keeps every letter legible.
    return FONT.get(ch.upper(), FONT["?"])


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def wrap_text(text, max_width, scale):
    """Greedy word wrap; returns a list of lines fitting max_width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                j = base + (xx - x0) * 3
                self.px[j], self.px[j + 1], self.px[j + 2] = color

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err, x, y = dx - dy, x0, y0
        while True:
            self.set(x, y, color)
            if x == x1 and y == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        ymin, ymax = min(y0, y1, y2), max(y0, y1, y2)
        for yy in range(ymin, ymax + 1):
            xs = []
            for (ax, ay, bx, by) in ((x0, y0, x1, y1), (x1, y1, x2, y2),
                                     (x2, y2, x0, y0)):
                if ay == by:
                    continue
                if (yy - ay) * (yy - by) <= 0 and ay != by:
                    t = (yy - ay) / (by - ay)
                    xs.append(ax + t * (bx - ax))
            if len(xs) >= 2:
                for xx in range(int(min(xs)), int(max(xs)) + 1):
                    self.set(xx, yy, color)

    def text(self, x, y, s, color, scale):
        for ch in s:
            g = glyph(ch)
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        self.rect(x + col * scale, y + row * scale,
                                  scale, scale, color)
            x += 6 * scale

    def text_center(self, y, s, color, scale):
        self.text((self.w - text_width(s, scale)) // 2, y, s, color, scale)


# ---------------------------------------------------------------- PNG writer
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    return out + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def write_png(path, canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.px[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr)
           + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + _chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ---------------------------------------------------------------- icons
# Small pictograms drawn inside a light box at the top-right of a cell.

def flame(c, x, y, s):
    c.triangle(x, y + 14 * s, x + 5 * s, y, x + 10 * s, y + 14 * s, FLAME)
    c.triangle(x + 2 * s, y + 14 * s, x + 5 * s, y + 5 * s,
               x + 8 * s, y + 14 * s, FLAME_Y)


def draw_icon(c, kind, x, y, w, h):
    c.rect(x, y, w, h, PAPER_DIM)
    cx, cy = x + w // 2, y + h // 2
    if kind == "refinery":
        c.rect(cx - 26, cy - 4, 12, 22, INK)
        c.rect(cx - 10, cy - 14, 12, 32, INK)
        c.rect(cx + 6, cy + 2, 14, 16, INK)
        c.rect(cx - 30, cy + 18, 62, 4, INK)
        flame(c, cx - 4, cy - 30, 1)
    elif kind == "jet":
        c.triangle(cx - 30, cy + 4, cx + 26, cy - 6, cx + 26, cy + 2, INK)
        c.triangle(cx - 6, cy - 2, cx + 2, cy - 18, cx + 10, cy - 2, INK)
        c.triangle(cx - 6, cy + 6, cx + 2, cy + 20, cx + 10, cy + 6, INK)
        c.triangle(cx + 26, cy - 6, cx + 34, cy - 12, cx + 34, cy + 2, RED)
    elif kind == "tariff":
        for i, bh in enumerate((14, 24, 34)):
            bx = cx - 28 + i * 20
            c.rect(bx, cy + 18 - bh, 12, bh, INK if i < 2 else RED)
        c.line(cx - 32, cy - 22, cx + 30, cy - 26, RED)
        c.triangle(cx + 30, cy - 26, cx + 20, cy - 30, cx + 20, cy - 20, RED)
    elif kind == "chart":
        c.line(cx - 32, cy + 20, cx + 32, cy + 20, INK)
        c.line(cx - 32, cy + 20, cx - 32, cy - 22, INK)
        pts = [(cx - 30, cy + 8), (cx - 14, cy - 6), (cx, cy + 10),
               (cx + 14, cy - 14), (cx + 30, cy - 20)]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            c.line(ax, ay, bx, by, RED)
        c.circle(pts[-1][0], pts[-1][1], 3, RED)
    elif kind == "islands":
        c.circle(cx - 16, cy + 6, 12, TEAL)
        c.circle(cx + 18, cy - 4, 9, TEAL)
        c.line(cx - 16, cy - 6, cx + 18, cy - 13, RED)
        c.circle(cx - 16, cy - 6, 2, RED)
        c.circle(cx + 18, cy - 13, 2, RED)
        c.line(cx - 30, cy + 20, cx + 30, cy + 20, INK)
    elif kind == "rocket":
        c.rect(cx - 6, cy - 22, 12, 34, INK)
        c.triangle(cx - 6, cy - 22, cx + 6, cy - 22, cx, cy - 34, RED)
        c.triangle(cx - 6, cy + 6, cx - 16, cy + 18, cx - 6, cy + 12, INK)
        c.triangle(cx + 6, cy + 6, cx + 16, cy + 18, cx + 6, cy + 12, INK)
        flame(c, cx - 5, cy + 12, 1)
        c.circle(cx, cy - 10, 3, WHITE)
    elif kind == "pin":
        c.circle(cx, cy - 6, 14, RED)
        c.triangle(cx - 12, cy + 2, cx + 12, cy + 2, cx, cy + 24, RED)
        c.circle(cx, cy - 6, 5, WHITE)


# ---------------------------------------------------------------- stories
# (kicker, headline, deck, icon) — every fact verified 25 Nov 2026.
STORIES = [
    ("SAUDI ARABIA - HOUTHIS",
     "HOUTHIS CLAIM STRIKE ON RAS TANURA REFINERY",
     "Yahya Saree says the attack caused fires at the kingdom's largest "
     "refinery; satellite images show thick black smoke. Riyadh says it "
     "shot down four drones over the site.",
     "refinery"),
    ("RUSSIA - UKRAINE WAR",
     "UKRAINE HITS AIR BASE, DAMAGES FIVE WARPLANES",
     "Kyiv says the Savasleyka strike knocked out three MiG-31 jets and "
     "two Su-34 bombers. Russia did not immediately comment.",
     "jet"),
    ("WASHINGTON - TRADE",
     "U.S. PROPOSES NEW TARIFFS ON 14 PARTNERS",
     "Section 301 duties follow a probe into excess factory capacity: "
     "China faces 20% more, the EU 15%. Levies could start in January.",
     "tariff"),
    ("U.S. ECONOMY - MARKETS",
     "HOT INFLATION, FAST GROWTH: PCE 3.8%, GDP 4.3%",
     "Core PCE hit 3.3%, its highest in three years. The Dow held above "
     "50,000 after a 1,100-point intraday plunge; the Nasdaq fell.",
     "chart"),
    ("PACIFIC - SECURITY",
     "SOLOMONS SIGN SECURITY TREATY WITH AUSTRALIA",
     "The pact names Canberra the islands' main security partner and bars "
     "foreign military bases. Australia pledges $490m over a decade.",
     "islands"),
    ("SPACE - CHINA",
     "SHENZHOU-24 DOCKS WITH PAKISTAN'S FIRST ASTRONAUT",
     "Muhammad Zeeshan Ali joins the Tiangong station, the first Pakistani "
     "and first foreign guest aboard China's space station.",
     "rocket"),
]

SUDAN = ("SUDAN - CIVIL WAR",
         "RSF DRONE STRIKES KILL 19 CIVILIANS, MONITORS SAY",
         "Emergency Lawyers says paramilitary drone strikes killed 19 people "
         "and wounded 20 in two cities as the war grinds on.",
         "pin")

TICKER = ("DOW 50,183 +0.3%  |  BRENT $93.60  |  KOSPI -6.2%  |  "
          "NASDAQ -0.6%  |  PCE 3.8%")


# ---------------------------------------------------------------- lead art
def draw_hormuz(c, x, y, w, h):
    """Strait of Hormuz: two tankers, flames, smoke and naval mines."""
    c.rect(x, y, w, h // 3, SEA1)
    c.rect(x, y + h // 3, w, h // 3, SEA2)
    c.rect(x, y + 2 * h // 3, w, h - 2 * h // 3, SEA3)
    for wy in (y + 18, y + 52, y + 96):
        for wx in range(x + 12, x + w - 40, 74):
            c.hline(wx, wy, 34, WHITE, 2)
    # mines: spiked black circles
    for mx, my in ((x + 500, y + 30), (x + 690, y + 22), (x + 880, y + 44)):
        for dx, dy in ((-12, 0), (12, 0), (0, -12), (0, 12),
                       (-8, -8), (8, -8), (-8, 8), (8, 8)):
            c.line(mx, my, mx + dx, my + dy, BLACK)
        c.circle(mx, my, 9, BLACK)
    # tanker 1 (left, burning)
    tx, ty = x + 90, y + h - 52
    c.rect(tx, ty, 300, 24, BLACK)
    c.triangle(tx + 300, ty, tx + 330, ty + 12, tx + 300, ty + 24, BLACK)
    c.rect(tx + 180, ty - 22, 70, 22, BLACK)
    c.rect(tx + 210, ty - 36, 16, 14, RED)
    flame(c, tx + 60, ty - 52, 2)
    flame(c, tx + 110, ty - 40, 1)
    for sx, sy, r in ((tx + 40, ty - 44, 12), (tx + 70, ty - 62, 15),
                      (tx + 100, ty - 52, 10)):
        c.circle(sx, sy, r, SMOKE)
    # tanker 2 (right)
    tx2, ty2 = x + 600, y + h - 46
    c.rect(tx2, ty2, 260, 20, BLACK)
    c.triangle(tx2 + 260, ty2, tx2 + 286, ty2 + 10, tx2 + 260, ty2 + 20, BLACK)
    c.rect(tx2 + 150, ty2 - 18, 56, 18, BLACK)
    c.rect(tx2 + 172, ty2 - 30, 13, 12, RED)
    flame(c, tx2 + 40, ty2 - 34, 1)
    c.text(x + 12, y + h - 18, "THE STRAIT OF HORMUZ", WHITE, 1)


# ---------------------------------------------------------------- page
def draw_cell(c, x, y, w, h, story):
    kicker, headline, deck, icon = story
    c.text(x, y, kicker, RED, 1)
    draw_icon(c, icon, x + w - 92, y + 2, 92, 62)
    hl_lines = wrap_text(headline, w - 104, 2)
    yy = y + 14
    for ln in hl_lines[:2]:
        c.text(x, yy, ln, INK, 2)
        yy += 16
    deck_lines = wrap_text(deck, w - 104, 1)
    yy += 4
    for ln in deck_lines[:3]:
        c.text(x, yy, ln, INK, 1)
        yy += 9


def draw_page():
    c = Canvas(W, H, PAPER)
    # masthead
    c.text_center(26, "THE WORLD TODAY", INK, 6)
    c.text_center(80, "WEDNESDAY, 25 NOVEMBER 2026 - EVENING EDITION",
                  INK, 2)
    c.hline(28, 102, 968, INK, 3)
    c.hline(28, 108, 968, INK, 1)
    # lead story
    c.text(28, 122, "IRAN WAR - STRAIT OF HORMUZ", RED, 2)
    c.text(28, 146, "TWO TANKERS HIT MINES", INK, 4)
    c.text(28, 178, "AND CATCH FIRE IN HORMUZ", INK, 4)
    deck = ("Iran's Revolutionary Guards say the tankers struck naval mines "
            "on an unauthorised route early Wednesday and exploded; the "
            "ships were not named and the claim was not independently "
            "confirmed. Brent crude jumped past $93 a barrel.")
    yy = 214
    for ln in wrap_text(deck, 968, 2)[:3]:
        c.text(28, yy, ln, INK, 2)
        yy += 15
    draw_hormuz(c, 28, 262, 968, 132)
    c.hline(28, 406, 968, INK, 2)
    # six-cell grid, 2 columns x 3 rows
    col_w = (968 - 20) // 2
    row_y = [420, 548, 676]
    for i, story in enumerate(STORIES):
        cx = 28 + (i % 2) * (col_w + 20)
        cy = row_y[i // 2]
        draw_cell(c, cx, cy, col_w, 120, story)
        if i % 2 == 0:
            c.vline(cx + col_w + 10, cy, 112, GREY, 1)
    c.hline(28, 804, 968, INK, 2)
    # Sudan, full width
    kicker, headline, deck, icon = SUDAN
    c.text(28, 818, kicker, RED, 1)
    draw_icon(c, icon, 904, 818, 92, 62)
    c.text(28, 834, headline, INK, 2)
    yy = 856
    for ln in wrap_text(deck, 860, 1)[:2]:
        c.text(28, yy, ln, INK, 1)
        yy += 9
    # ticker
    c.rect(0, 892, W, 42, BLACK)
    c.text_center(906, TICKER, WHITE, 2)
    # footer
    c.text_center(946, "SOURCES: REUTERS, AP, JUST SECURITY, ISW - ALL EVENTS "
                       "REPORTED ON WEDNESDAY, 25 NOVEMBER 2026", GREY, 1)
    c.hline(28, 972, 968, INK, 1)
    c.text_center(982, "THE WORLD TODAY - ONE DAY, ONE PAGE, THE WHOLE WORLD",
                  GREY, 1)
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    write_png(path, draw_page())
    print("wrote", path)


if __name__ == "__main__":
    main()
