#!/usr/bin/env python3
"""Generates assets/terminal.svg, the animated terminal. Pure Python, no images needed."""

import math
import random
from pathlib import Path
from xml.sax.saxutils import escape

# Saves to the root /assets folder
OUT = Path(__file__).resolve().parent / "assets" / "terminal.svg"

# ---------------------------------------------------------------- content

USER, HOST = "deelaka", "github"
SHELL = "bash"

# <--- YOUR INFO GOES HERE (labels up to 7 characters)
INFO = [
    ("Name", "Deelaka Ransilu"),
    ("OS", "Ubuntu Linux"),
    ("Shell", "bash"),
    ("Editor", "VS Code"),
    ("Kernel", "Docker, Kubernetes"),
    ("Arch", "Cloud Infrastructure"),
    ("Ops", "CI/CD, Terraform"),
    ("CPU", "Automation"),
    ("Langs", "Python, TypeScript"),
    ("Design", "UI/UX and Systems"),
    ("Site", "deelakaransilu.me"),
    ("Mail", "ransilu.deelaka@gmail.com"),
]

# <--- YOUR PLAN GOES HERE
PLAN = [
    ("x", "green", "automate infrastructure"),
    ("x", "green", "design scalable systems"),
    ("~", "yellow", "learn something new every day"),
]

# ---------------------------------------------------------------- look

C = {
    "bg": "#0d1117", "bar": "#161b22", "border": "#30363d",
    "fg": "#c9d1d9", "dim": "#6e7681", "green": "#3fb950", "neon": "#7ee787",
    "blue": "#79c0ff", "yellow": "#e3b341", "red": "#ff7b72", "purple": "#d2a8ff",
    "cyan": "#56d4dd", "orange": "#ffa657",
}

# Colour bar under the info, like Ubuntu's neofetch: normal row, then bright row
PAL_NORMAL = ["#161b22", "#ff7b72", "#3fb950", "#e3b341", "#79c0ff", "#d2a8ff", "#56d4dd", "#c9d1d9"]
PAL_BRIGHT = ["#6e7681", "#ffa198", "#7ee787", "#f2cc60", "#a5d6ff", "#e2c5ff", "#b3f0ff", "#f0f6fc"]

# Logo: a 40 x 40 pixel scene seen from above. Dark-blue sea tiles with lighter vertical streaks,
# and a light-blue pixel whale with nine coloured Docker containers on its back. The whale is
# built from polygons and drawn as vector pixels, then it sways gently left and right.
LOGO_COLOUR = "blue"  # colour of the title and the Name:/OS:/... labels
GRID = 40             # the sea is GRID x GRID tiles
PX = 6                # size of one sea tile in px, so the scene is GRID*PX wide and tall
GAP = 1               # thin gap between sea tiles
SWAY = 3.2            # seconds for one full tail swish (smaller = faster)
TAIL_SWING = 10       # how far the tail end swings sideways, in whale pixels (bigger = more action)
FLIPPER_SWING = 4     # how far the flipper tips sweep, in whale pixels (0 = flippers stay still)
FLOW = 0.14           # seconds the water streaks take to drift down one tile (bigger = slower water)
GLINT = 3.0           # seconds for one shimmer wave to sweep across the water
SNAP = True           # True = move in whole pixels (crisp pixel art), False = smooth glide

# Sea map: '.' = normal tile, 'a' = faint streak tile, 'b' = bright streak tile.
SEA_MAP = [
    ".............................a..........",
    "...b.........................b..........",
    "...b.........................b..........",
    "...b................................a...",
    "...b................................b...",
    "...b....b..................b........b...",
    "...b....b..................b........b...",
    "........b..................b........b...",
    "........b..................b........b...",
    "........b...b..............b........a...",
    "........a...b.......................b...",
    "............b...........................",
    "............b...................b.......",
    "............a...................b.......",
    "................................b.......",
    "...b............................b.......",
    "...b............................b.......",
    "...b............................b.......",
    "...b............................b.......",
    "...b............................b.......",
    "...b............................a.......",
    "...b....................................",
    "...b.....a..........................a...",
    "...b.....b..........................b...",
    ".........b..........................b...",
    ".........b...................a......b...",
    ".........b...................b......b...",
    ".........b...................b......b...",
    ".........b...................b......b...",
    ".........b...................b......a...",
    ".........a......b............a..........",
    "................b...............a.......",
    "................a...............b.......",
    ".....a..........................b.......",
    ".....b..........................b.......",
    ".....b..........................b.......",
    ".....a..........................a.......",
    ".....a..........a..........a............",
    ".....a..........a..........a............",
    "...........................a............",
]
SEA_GAP = "#000f4b"   # colour showing through the gaps between tiles
SEA_TONES = {"a": "#0a3a80", "b": "#054dac"}
SEA = "#002565"       # normal sea tile
GLINT_SHADES = ["#06368a", "#0a4399", "#0b4aa6", "#1560c0"]  # the blues that shimmer through the water

WHALE = "#50affe"       # whale body
WHALE_LINE = "#2f8fe0"  # faint tile lines showing through the body
EYE = "#08164a"

# Whale outline, LEFT half only, traced on a 1254 x 1254 canvas (centre line x = 627).
# The right half is mirrored in code, then the polygon is turned into 80 x 80 pixels.
REF = 1254
HALF = [
    (590, 62), (575, 90), (540, 125), (522, 160), (508, 190), (497, 215), (497, 300), (490, 322),
    (490, 420),                                                      # head and shoulder
    (465, 445), (430, 490), (400, 525), (375, 560), (358, 590),      # flipper, front edge
    (358, 620), (370, 700), (385, 700), (385, 685),                  # flipper tip
    (400, 665), (432, 640), (465, 600), (490, 548), (500, 540),      # flipper, back edge
    (505, 600), (515, 660), (525, 690), (545, 740), (558, 775),      # belly
    (572, 830), (585, 870), (600, 895), (608, 920), (608, 985),      # tail stalk
    (590, 992), (560, 1030), (520, 1060), (495, 1100), (480, 1125),  # fluke
    (480, 1155), (500, 1162), (530, 1145), (580, 1132), (612, 1118), (627, 1085),
]
EYE_CELLS = [(14, 32), (14, 47)]  # (row, column) on the 80 x 80 whale grid

# Nine containers, 3 x 3, (colour) row by row, and where the block sits (reference px).
CONTAINERS = [
    ["#2f6bff", "#ef3b36", "#ffc21a"],
    ["#1fa34a", "#ff8a00", "#7a3cf0"],
    ["#17a38f", "#f2487f", "#a468f5"],
]
BLOCK_COLS = [530, 596, 661]
BLOCK_ROWS = [327, 423, 519]
CONT_W, CONT_H = 63, 92
# Seaweed clusters on the whale's back: (centre x, top y, height) in reference px.
SEAWEED = [(622, 232, 93), (548, 295, 25), (702, 292, 30), (511, 452, 70),
           (745, 440, 80), (565, 620, 60), (665, 625, 70), (692, 620, 35)]

W = 720
FONT = 14
CW = FONT * 0.6
LH = 20
PAD_X = 24
BAR_H = 34
TOP = BAR_H + 26
INFO_COL = 32  # text column where the info starts (a smaller logo means it can sit closer)

random.seed(7)
assert len(SEA_MAP) == GRID and all(len(r) == GRID for r in SEA_MAP), "SEA_MAP must be GRID x GRID"

# ---------------------------------------------------------------- builder

body, defs, css = [], [], []
row, t = 0, 0.4

def x_at(col): return PAD_X + col * CW
def y_at(r): return TOP + r * LH
def fmt(n): return f"{n:.3f}".rstrip("0").rstrip(".")
def show(begin): return f'<set attributeName="visibility" to="visible" begin="{fmt(begin)}s" fill="freeze"/>'
def hide(begin): return f'<set attributeName="visibility" to="hidden" begin="{fmt(begin)}s" fill="freeze"/>'

def spans(segments, grid_col=None):
    out, col = [], grid_col
    for text, colour, bold in segments:
        attrs = f' fill="{C[colour]}"' + (' font-weight="700"' if bold else "")
        if grid_col is not None:
            xs = " ".join(fmt(x_at(col + i)) for i in range(len(text)))
            attrs += f' x="{xs}"'
            col += len(text)
        out.append(f"<tspan{attrs}>{escape(text)}</tspan>")
    return "".join(out)

def line(r, col, segments, begin):
    body.append(
        f'<text x="{fmt(x_at(col))}" y="{y_at(r)}" visibility="hidden">'
        f"{spans(segments)}{show(begin)}</text>"
    )

PROMPT = [(USER, "green", True), ("@", "dim", False), (HOST, "green", True),
          (":", "dim", False), ("~", "blue", True), ("$ ", "dim", False)]
PROMPT_LEN = sum(len(s[0]) for s in PROMPT)

def cursor(r, col, begin, blink=False):
    el = (f'<rect x="{fmt(x_at(col))}" y="{y_at(r) - FONT + 2}" width="{fmt(CW)}" '
          f'height="{FONT + 3}" fill="{C["neon"]}" visibility="hidden">{show(begin)}')
    if blink:
        el += (f'<animate attributeName="opacity" values="1;0" dur="1.1s" calcMode="discrete" '
               f'begin="{fmt(begin)}s" repeatCount="indefinite"/>')
    return el

def command(cmd, think=0.7):
    global row, t
    r, begin = row, t
    clip = f"clip{r}"
    times, k = [], begin + think
    for ch in cmd:
        times.append(k)
        k += random.uniform(0.045, 0.11) + (0.08 if ch in " /." else 0)
    t0, dur = times[0], times[-1] - times[0] + 0.001
    key_times = ";".join(fmt((tt - t0) / dur) for tt in times)
    widths = ";".join(fmt((i + 1) * CW) for i in range(len(cmd)))
    xs = ";".join(fmt(x_at(PROMPT_LEN + i + 1)) for i in range(len(cmd)))
    anim = f'calcMode="discrete" keyTimes="{key_times}" begin="{fmt(t0)}s" dur="{fmt(dur)}s" fill="freeze"'

    defs.append(
        f'<clipPath id="{clip}"><rect x="{fmt(x_at(PROMPT_LEN))}" y="{y_at(r) - FONT - 2}" '
        f'width="0" height="{LH + 4}"><animate attributeName="width" values="{widths}" {anim}/>'
        f"</rect></clipPath>"
    )
    body.append(
        f'<text y="{y_at(r)}" visibility="hidden">{spans(PROMPT, 0)}{show(begin)}</text>'
        f'<text y="{y_at(r)}" clip-path="url(#{clip})">{spans([(cmd, "fg", False)], PROMPT_LEN)}</text>'
    )
    enter = times[-1] + 0.35
    body.append(
        cursor(r, PROMPT_LEN, begin)
        + f'<animate attributeName="x" values="{xs}" {anim}/>{hide(enter)}</rect>'
    )
    row += 1
    t = enter + 0.12

# ---------------------------------------------------------------- the whale

def shade(hex_colour, f):
    """Make a colour darker (f < 1) or lighter (f > 1)."""
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v * f))) for v in (r, g, b))

def inside(px, py, poly):
    """Even-odd point-in-polygon test."""
    hit, n = False, len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1:
            hit = not hit
    return hit

def whale_mask():
    """80 x 80 grid of booleans: which whale pixels are on."""
    poly = HALF + [(REF - x, y) for x, y in reversed(HALF)]
    cell = REF / 80
    return [[inside((i + 0.5) * cell, (j + 0.5) * cell, poly) for i in range(80)] for j in range(80)]

STEPS = 24                   # animation samples per swish
LAG = 2.0                    # how much the tail trails the middle (makes the swish ripple)
TAIL_START = 0.5             # the body is still from the nose down to here (0..1); only the back half moves

def keyframes(name, value_at):
    frames = "".join(f"{fmt(i * 100 / STEPS)}%{{transform:translateX({fmt(value_at(i))}px)}}" for i in range(STEPS + 1))
    css.append(f"@keyframes {name}{{{frames}}}")

def whale(x0, y0, begin):
    """The logo: still sea tiles, a head and cargo that stay put, and a tail and flippers that move."""
    tile = PX - GAP
    side = GRID * PX
    sub = side / 80            # size of one whale pixel (half a sea tile)
    k = side / REF             # reference px -> scene px
    snap = (lambda v: round(v / sub) * sub) if SNAP else (lambda v: v)

    # sea: a dark gap colour, normal tiles from a pattern, then the lighter streak tiles
    defs.append(f'<pattern id="seacell" width="{PX}" height="{PX}" patternUnits="userSpaceOnUse">'
                f'<rect width="{tile}" height="{tile}" rx="0.6" fill="{SEA}"/></pattern>')
    # whale skin: light blue with faint tile lines
    defs.append(f'<pattern id="skin" width="{PX}" height="{PX}" patternUnits="userSpaceOnUse">'
                f'<rect width="{PX}" height="{PX}" fill="{WHALE}"/>'
                f'<path d="M0 {PX - 0.5}H{PX}M{PX - 0.5} 0V{PX}" stroke="{WHALE_LINE}" '
                f'stroke-opacity="0.5" stroke-width="1"/></pattern>')
    sea = [f'<rect width="{side}" height="{side}" fill="{SEA_GAP}"/>',
           f'<rect width="{side}" height="{side}" fill="url(#seacell)"/>']
    # shimmer: scattered tiles fade through lighter blues, timed along a diagonal so bright bands sweep across
    BANDS = 12
    wr = random.Random(11)
    glints = {}
    for r in range(GRID):
        for c in range(GRID):
            if wr.random() < 0.14:
                key = ((r + c) % BANDS, wr.choice(GLINT_SHADES))
                glints.setdefault(key, []).append(f"M{c * PX} {r * PX}h{tile}v{tile}h-{tile}z")
    css.append(f"@keyframes glint{{0%,100%{{opacity:0}}50%{{opacity:.55}}}}")
    for n in range(BANDS):
        css.append(f".d{n}{{animation-delay:-{fmt(n / BANDS * GLINT)}s}}")
    for (n, shade_hex), cells in sorted(glints.items()):
        sea.append(f'<path class="sh d{n}" fill="{shade_hex}" d="{"".join(cells)}"/>')

    # streaks: each vertical run of lighter tiles drifts down the water one tile at a time, then re-enters at the top
    runs = []
    for c in range(GRID):
        r = 0
        while r < GRID:
            if SEA_MAP[r][c] in SEA_TONES:
                s = r
                while r < GRID and SEA_MAP[r][c] in SEA_TONES:
                    r += 1
                runs.append((c, s, r))
            else:
                r += 1
    sr = random.Random(5)
    for n, (c, r0, r1) in enumerate(runs):
        length = r1 - r0
        tiles_to_go = GRID + length
        speed = FLOW * sr.uniform(0.8, 1.3)
        css.append(f"@keyframes st{n}{{from{{transform:translateY({-(r0 + length) * PX}px)}}"
                   f"to{{transform:translateY({(GRID - r0) * PX}px)}}}}")
        tiles = "".join(f'<rect x="{c * PX}" y="{r * PX}" width="{tile}" height="{tile}" rx="0.6" '
                        f'fill="{SEA_TONES[SEA_MAP[r][c]]}"/>' for r in range(r0, r1))
        sea.append(f'<g class="st" style="animation:st{n} {fmt(speed * tiles_to_go)}s steps({tiles_to_go}) '
                   f'-{fmt(sr.uniform(0, speed * tiles_to_go))}s infinite">{tiles}</g>')

    # three separate shapes: the body (head, belly, tail) and the two flippers
    cell = REF / 80
    def raster(half, extra=()):
        poly = half + [(REF - x, y) for x, y in reversed(half)]
        return [[inside((i + 0.5) * cell, (j + 0.5) * cell, poly) for i in range(80)] for j in range(80)]
    body_half = HALF[:9] + [(500, 540)] + HALF[23:]
    flip_left = [(520, 420)] + HALF[8:23] + [(520, 545)]
    body_mask = raster(body_half)
    def flipper(points, mirror):
        pts = [(REF - x, y) for x, y in points] if mirror else points
        return [[inside((i + 0.5) * cell, (j + 0.5) * cell, pts) and not body_mask[j][i]
                 for i in range(80)] for j in range(80)]
    fl_mask, fr_mask = flipper(flip_left, False), flipper(flip_left, True)

    def row_rects(mask, j):
        out, i = [], 0
        while i < 80:
            if mask[j][i]:
                s = i
                while i < 80 and mask[j][i]:
                    i += 1
                out.append(f'<rect x="{fmt(s * sub)}" y="{fmt(j * sub)}" width="{fmt((i - s) * sub)}" '
                           f'height="{fmt(sub + 0.4)}" fill="url(#skin)"/>')
            else:
                i += 1
        return out

    def slices(mask, name, first, last, shift):
        """Rows first..last-1, two at a time. shift(row_centre, i) gives the sideways move at sample i,
        or shift is None for rows that stay still."""
        still, moving = [], []
        for g in range(first // 2, last // 2):
            rects = row_rects(mask, 2 * g) + row_rects(mask, 2 * g + 1)
            if not rects:
                continue
            if shift is None:
                still += rects
                continue
            rc = 2 * g + 1
            keyframes(f"{name}{g}", lambda i, rc=rc: snap(shift(rc, i)))
            moving.append(f'<g class="w" style="animation-name:{name}{g}">{"".join(rects)}</g>')
        return "".join(still) + "".join(moving)

    # the back half of the body swishes: nothing moves above TAIL_START, then more and more towards the tail
    def tail_shift(r, i):
        t = max(0.0, (r / 80 - TAIL_START) / (1 - TAIL_START))
        return TAIL_SWING * sub * t ** 1.5 * math.sin(2 * math.pi * i / STEPS - LAG * t)
    cut = int(TAIL_START * 80) // 2 * 2
    parts = [slices(body_mask, "b", 0, cut, None), slices(body_mask, "b", cut, 80, tail_shift)]

    # flippers paddle: the root stays on the body, the tip sweeps sideways
    def flip_shift(sign):
        def f(r, i):
            reach = min(1.0, max(0.0, (r - 27) / 17.0))
            return sign * FLIPPER_SWING * sub * reach * math.sin(2 * math.pi * i / STEPS + 1.0)
        return f
    parts.append(slices(fl_mask, "fl", 24, 48, flip_shift(1)))
    parts.append(slices(fr_mask, "fr", 24, 48, flip_shift(1)))

    # eyes stay with the head
    for (er, ec) in EYE_CELLS:
        parts.append(f'<rect x="{fmt(ec * sub)}" y="{fmt(er * sub)}" width="{fmt(sub)}" height="{fmt(sub)}" fill="{EYE}"/>')

    # cargo: nine containers stay exactly where they are
    cargo = []
    cw, ch = CONT_W * k, CONT_H * k
    for r, rowcols in enumerate(CONTAINERS):
        for c, colour in enumerate(rowcols):
            x, y = BLOCK_COLS[c] * k, BLOCK_ROWS[r] * k
            cargo.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(cw)}" height="{fmt(ch)}" '
                         f'rx="0.7" fill="{shade(colour, 0.55)}"/>')
            cargo.append(f'<rect x="{fmt(x + 0.6)}" y="{fmt(y + 0.6)}" width="{fmt(cw - 1.2)}" '
                         f'height="{fmt(ch - 1.2)}" rx="0.5" fill="{colour}"/>')
            for n in range(5):  # the ribs
                rx = x + 1.5 + n * (cw - 3) / 4.0
                cargo.append(f'<rect x="{fmt(rx - 0.35)}" y="{fmt(y + 1.6)}" width="0.7" '
                             f'height="{fmt(ch - 3.2)}" fill="{shade(colour, 0.72)}"/>')

    # seaweed: each tuft waves on its own, a little out of step with the others
    keyframes("sg", lambda i: 1.1 * math.sin(2 * math.pi * i / STEPS))
    rnd = random.Random(3)
    greens = ["#2f9e44", "#1f7a35", "#62c554"]
    seed_px = 1.3
    for n_tuft, (sx, st, sh) in enumerate(SEAWEED):
        tuft = []
        n = max(3, int(sh * k / seed_px))
        for i in range(n):
            wob = round(1.6 * math.sin(i * 0.9 + sx)) * seed_px
            for extra in ((0,) if rnd.random() < 0.5 else (0, 1)):
                tuft.append(f'<rect x="{fmt(sx * k + wob + extra * seed_px)}" '
                            f'y="{fmt((st + sh) * k - i * seed_px)}" width="{seed_px}" height="{seed_px}" '
                            f'fill="{rnd.choice(greens)}"/>')
        cargo.append(f'<g class="sg" style="animation-name:sg;animation-delay:-{fmt(n_tuft * 0.47)}s">{"".join(tuft)}</g>')

    defs.append(f'<clipPath id="logo"><rect width="{side}" height="{side}" rx="{fmt(PX * 0.6)}"/></clipPath>')
    body.append(
        f'<g transform="translate({fmt(x0)} {fmt(y0)})"><g clip-path="url(#logo)" visibility="hidden">'
        f'{"".join(sea)}'
        f'<g filter="url(#glow)">{"".join(parts)}{"".join(cargo)}</g>'
        f'{show(begin)}</g></g>'
    )

def output(rows, step=0.04):
    global row, t
    for items in rows:
        for col, segs in items:
            line(row, col, segs, t)
        row += 1
        t += step
    t += 0.5

# ---------------------------------------------------------------- script

command("neofetch")

info_rows = [
    [(USER, LOGO_COLOUR, True), ("@", "fg", False), (HOST, LOGO_COLOUR, True)],
    [("-" * len(f"{USER}@{HOST}"), "dim", False)],
] + [[(f"{k + ':':<8}", LOGO_COLOUR, True), (v, "fg", False)] for k, v in INFO]
palette_row = len(info_rows) + 1

# info, a blank line, two rows of colour bar, a blank line
rows = [[(INFO_COL, r)] for r in info_rows] + [[], [], [], []]

block_top = y_at(row) - FONT
whale(PAD_X, block_top + (len(info_rows) * LH - GRID * PX) / 2, t)
palette_at, palette_begin = row + palette_row, t + palette_row * 0.04
output(rows)

swatches = "".join(
    f'<rect x="{fmt(x_at(INFO_COL + i * 3))}" y="{y_at(palette_at + k) - FONT + 1}" '
    f'width="{fmt(CW * 3)}" height="{LH}" fill="{colour}"/>'
    for k, pal in enumerate((PAL_NORMAL, PAL_BRIGHT))
    for i, colour in enumerate(pal)
)
body.append(f'<g visibility="hidden">{swatches}{show(palette_begin)}</g>')

command("cat ~/.plan", think=0.9)
output([[(0, [("[", "dim", False), (m, colour, True), ("] ", "dim", False), (text, "fg", False)])]
        for m, colour, text in PLAN], step=0.12)

body.append(f'<text y="{y_at(row)}" visibility="hidden">{spans(PROMPT, 0)}{show(t)}</text>')
body.append(cursor(row, PROMPT_LEN, t, blink=True) + "</rect>")

# ---------------------------------------------------------------- render

H = y_at(row) + 26
dots = "".join(
    f'<circle cx="{20 + i * 20}" cy="{BAR_H / 2}" r="6" fill="{c}"/>'
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"])
)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title">
<title id="title">{USER}@{HOST}: neofetch. DevOps and Design.</title>
<style>
text {{ font: {FONT}px ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace; white-space: pre; }}
.title {{ font-size: 12px; fill: {C["dim"]}; }}
.w {{ animation-duration: {SWAY}s; }}
.sg {{ animation-duration: 2.6s; }}
.sh {{ opacity: 0; animation: glint {GLINT}s ease-in-out infinite; }}
.w, .sg {{ animation-iteration-count: infinite; animation-timing-function: linear; }}
{chr(10).join(css)}
@media (prefers-reduced-motion: reduce) {{ .w, .sg, .sh, .st {{ animation: none !important; }} }}
</style>
<defs>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
<feGaussianBlur stdDeviation="3" result="blur"/>
<feComponentTransfer in="blur" result="soft"><feFuncA type="linear" slope="0.9"/></feComponentTransfer>
<feMerge><feMergeNode in="soft"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#ffffff" fill-opacity="0.025"/></pattern>
<clipPath id="window"><rect width="{W}" height="{H}" rx="10"/></clipPath>
{chr(10).join(defs)}
</defs>
<g clip-path="url(#window)">
<rect width="{W}" height="{H}" fill="{C["bg"]}"/>
<rect width="{W}" height="{BAR_H}" fill="{C["bar"]}"/>
<line x1="0" y1="{BAR_H}" x2="{W}" y2="{BAR_H}" stroke="{C["border"]}"/>
{dots}
<text class="title" x="{W / 2}" y="{BAR_H / 2 + 4}" text-anchor="middle">{USER}@{HOST}: ~ — {SHELL}</text>
<g xml:space="preserve">
{chr(10).join(body)}
</g>
<rect y="{BAR_H}" width="{W}" height="{H - BAR_H}" fill="url(#scan)" pointer-events="none"/>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{C["border"]}"/>
</svg>
"""

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(svg, encoding="utf-8")
print(f"Successfully created {OUT}  ({len(svg) / 1024:.0f} KB)")