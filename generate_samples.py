"""
Sample PNG generator for SPECTRAL SCANNER.

Reimplements the four JS pattern algorithms in Python so we can produce
samples/*.png without spinning up a browser. The algorithms mirror the
ones in index.html line-for-line where practical; small variations are
acceptable since the on-page renderer is the authoritative one.

Output: samples/WOODLAND-7B.png, MARPAT-D.png, FRACTAL-G.png, TERRAIN-X.png
Test palette: #4A7C2B, #8B6F47, #2D3E1F, #C4B896
"""

import math
import os
from PIL import Image, ImageDraw

# ---- Sample resolution (smaller than the 8.5"x11" print canvas) ----
# Keep aspect ratio 8.5:11. 850x1100 = 100 DPI preview.
W, H = 850, 1100
PX_PER_INCH = W / 8.5
SEED = 4242

PALETTE = ['#4A7C2B', '#8B6F47', '#2D3E1F', '#C4B896']
OUT_DIR = os.path.join(os.path.dirname(__file__), 'samples')


# ====================================================================
# Seeded RNG — mulberry32 (matches JS impl)
# ====================================================================

def mulberry32(seed):
    a = seed & 0xFFFFFFFF

    def next_float():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        t &= 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0

    return next_float


# ====================================================================
# Classic Perlin noise (matches JS impl)
# ====================================================================

def make_perlin(seed):
    rnd = mulberry32(seed)
    perm = list(range(256))
    for i in range(255, 0, -1):
        j = int(rnd() * (i + 1))
        perm[i], perm[j] = perm[j], perm[i]
    p = perm + perm  # length 512

    def fade(t): return t * t * t * (t * (t * 6 - 15) + 10)
    def lerp(a, b, t): return a + t * (b - a)
    def grad(h, x, y):
        h &= 7
        u = x if h < 4 else y
        v = y if h < 4 else x
        return (-u if (h & 1) else u) + (-2 * v if (h & 2) else 2 * v)

    def noise(x, y):
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255
        x -= math.floor(x)
        y -= math.floor(y)
        u, v = fade(x), fade(y)
        A = p[X] + Y
        B = p[X + 1] + Y
        n = lerp(
            lerp(grad(p[A],     x,     y    ), grad(p[B],     x - 1, y    ), u),
            lerp(grad(p[A + 1], x,     y - 1), grad(p[B + 1], x - 1, y - 1), u),
            v
        )
        return (n + 1) * 0.5

    return noise


def fbm(noise, x, y, octaves, lacunarity, gain):
    s, amp, freq, norm = 0.0, 1.0, 1.0, 0.0
    for _ in range(octaves):
        s += amp * noise(x * freq, y * freq)
        norm += amp
        amp *= gain
        freq *= lacunarity
    return s / norm


def hex_to_rgb(h):
    s = h.lstrip('#')
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


# ====================================================================
# EPIC CAMPUS ICON STAMP
# Scatters 4 recolored copies of the circular EPIC icon across each
# camo, one per quadrant. Each copy is recolored to the student
# palette by nearest-color match against the source logo regions.
# Mirrors the JS implementation in index.html.
# ====================================================================

import numpy as np

EPIC_LOGO_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'epic-logo.png')

# Source logo region colors (brightest → darkest):
# [white background, orange peaks, green river, navy mountain]
LOGO_REGION_RGB = np.array([
    [255, 255, 255],
    [232, 119,  34],
    [ 62, 157,  67],
    [ 27,  61,  94],
], dtype=np.int32)


def _recolor_icon(palette_rgb):
    icon = Image.open(EPIC_LOGO_PATH).convert('RGBA')
    arr = np.array(icon)
    rgb = arr[..., :3].astype(np.int32)
    alpha = arr[..., 3]
    h, w = rgb.shape[:2]
    flat = rgb.reshape(-1, 3)

    # Sort student colors brightest → darkest so they align rank-by-rank
    # with LOGO_REGION_RGB.
    sorted_student = sorted(
        palette_rgb,
        key=lambda c: -(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])
    )

    # For each pixel, find which logo region color it's closest to.
    diffs = flat[:, None, :] - LOGO_REGION_RGB[None, :, :]
    dists = (diffs * diffs).sum(axis=2)
    nearest = dists.argmin(axis=1)

    new_rgb = np.zeros_like(flat)
    for k in range(4):
        mask = nearest == k
        new_rgb[mask] = sorted_student[k]

    out = np.zeros_like(arr)
    out[..., :3] = new_rgb.reshape(h, w, 3)
    out[..., 3] = alpha
    # Zero RGB where fully transparent
    transparent = alpha < 16
    out[transparent, :3] = 0
    out[transparent, 3] = 0
    return Image.fromarray(out, 'RGBA')


def embed_epic_mark(img, w, h, palette_rgb, seed):
    if not os.path.exists(EPIC_LOGO_PATH):
        return img
    rnd = mulberry32((seed ^ 0xE91CCA) & 0xFFFFFFFF)
    px_per_inch = w / 8.5
    icon_size = int(1.4 * px_per_inch)
    recolored = _recolor_icon(palette_rgb).resize(
        (icon_size, icon_size), Image.LANCZOS
    )

    # 4 placements, one per quadrant; middle 60% of each quadrant.
    for q in range(4):
        qx = q % 2
        qy = q // 2
        x = int((qx * 0.5 + 0.10 + rnd() * 0.30) * w - icon_size / 2)
        y = int((qy * 0.5 + 0.10 + rnd() * 0.30) * h - icon_size / 2)
        img.paste(recolored, (x, y), recolored)
    return img


# ====================================================================
# MARPAT-D
# ====================================================================

def render_marpat(seed):
    img = Image.new('RGB', (W, H))
    pixels = img.load()
    cells_x, cells_y = 80, 100
    cell_w = W / cells_x
    cell_h = H / cells_y
    n1 = make_perlin(seed)
    n2 = make_perlin(seed ^ 0xA5A5A5)
    freq = 0.09
    rgb = [hex_to_rgb(c) for c in PALETTE]

    # Precompute cell colors then paint.
    grid = [[0] * cells_x for _ in range(cells_y)]
    for j in range(cells_y):
        for i in range(cells_x):
            v = n1(i * freq, j * freq) * 0.65 + n2(i * freq * 1.8 + 100, j * freq * 1.8 + 100) * 0.35
            if   v < 0.25: idx = 0
            elif v < 0.50: idx = 1
            elif v < 0.75: idx = 2
            else:          idx = 3
            grid[j][i] = idx

    draw = ImageDraw.Draw(img)
    for j in range(cells_y):
        for i in range(cells_x):
            x0 = int(i * cell_w)
            y0 = int(j * cell_h)
            x1 = int((i + 1) * cell_w) + 1
            y1 = int((j + 1) * cell_h) + 1
            draw.rectangle([x0, y0, x1, y1], fill=rgb[grid[j][i]])
    return embed_epic_mark(img, W, H, rgb, seed)


# ====================================================================
# WOODLAND-7B
# ====================================================================

def render_woodland(seed):
    rgbs = [hex_to_rgb(c) for c in PALETTE]
    ordered = sorted(rgbs, key=luminance)
    img = Image.new('RGB', (W, H), ordered[0])
    draw = ImageDraw.Draw(img)
    rnd = mulberry32(seed)
    total = 80 + int(rnd() * 71)
    third = total // 3
    buckets = [third, third, total - 2 * third]
    px_per_inch = PX_PER_INCH

    for tier in (1, 2, 3):
        color = ordered[tier]
        count = buckets[tier - 1]
        for _ in range(count):
            cx = rnd() * W
            cy = rnd() * H
            r = (0.5 + rnd() * 1.0) * px_per_inch
            n_pts = 14 + int(rnd() * 8)
            phase = rnd() * math.tau
            verts = []
            for i in range(n_pts):
                a = i * (math.tau / n_pts) + phase
                rr = r * (0.55 + rnd() * 0.7)
                verts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
            # Smooth with midpoint subdivision: sample 4 points per quad-bezier
            # to mimic the JS quadraticCurveTo path.
            smooth = []
            n = len(verts)
            for i in range(n):
                cur  = verts[i]
                nxt  = verts[(i + 1) % n]
                mid_prev = ((verts[(i - 1) % n][0] + cur[0]) / 2,
                            (verts[(i - 1) % n][1] + cur[1]) / 2)
                mid_next = ((cur[0] + nxt[0]) / 2,
                            (cur[1] + nxt[1]) / 2)
                # Sample 4 points along quadratic Bezier from mid_prev -> cur -> mid_next
                for t in (0.0, 0.25, 0.5, 0.75):
                    omt = 1 - t
                    x = omt * omt * mid_prev[0] + 2 * omt * t * cur[0] + t * t * mid_next[0]
                    y = omt * omt * mid_prev[1] + 2 * omt * t * cur[1] + t * t * mid_next[1]
                    smooth.append((x, y))
            draw.polygon(smooth, fill=color)
    return embed_epic_mark(img, W, H, rgbs, seed)


# ====================================================================
# FRACTAL-G
# ====================================================================

def render_fractalg(seed):
    rgbs = [hex_to_rgb(c) for c in PALETTE]
    img = Image.new('RGB', (W, H), rgbs[0])
    draw = ImageDraw.Draw(img)
    rnd = mulberry32(seed)
    cell = 1.0 * PX_PER_INCH
    cols = math.ceil(W / cell) + 1
    rows = math.ceil(H / cell) + 1

    pts = []
    for j in range(rows + 1):
        row = []
        for i in range(cols + 1):
            edge = (i == 0 or j == 0 or i == cols or j == rows)
            jx = 0 if edge else (rnd() - 0.5) * cell * 0.9
            jy = 0 if edge else (rnd() - 0.5) * cell * 0.9
            row.append((i * cell + jx, j * cell + jy))
        pts.append(row)

    noise = make_perlin(seed ^ 0x12345)
    cj = mulberry32(seed ^ 0x9988)

    def pick_diff(base, r, avoid):
        if r < 0.6: idx = base
        else: idx = (base + 1 + int(r * 3)) % 4
        if idx == avoid: idx = (idx + 1) % 4
        return idx

    for j in range(rows):
        for i in range(cols):
            a = pts[j][i]
            b = pts[j][i + 1]
            c = pts[j + 1][i]
            d = pts[j + 1][i + 1]
            alt = (((i * 73856093) ^ (j * 19349663) ^ seed) & 1) == 0
            region = noise(i * 0.18, j * 0.18)
            base = min(3, int(region * 4))
            t1 = pick_diff(base, cj(), -1)
            t2 = pick_diff(base, cj(), t1)
            if alt:
                draw.polygon([a, b, c], fill=rgbs[t1])
                draw.polygon([b, d, c], fill=rgbs[t2])
            else:
                draw.polygon([a, b, d], fill=rgbs[t1])
                draw.polygon([a, d, c], fill=rgbs[t2])
    return embed_epic_mark(img, W, H, rgbs, seed)


# ====================================================================
# TERRAIN-X
# ====================================================================

def render_terrainx(seed):
    rgbs = [hex_to_rgb(c) for c in PALETTE]
    scale = max(1, W // 600)
    ww = math.ceil(W / scale)
    hh = math.ceil(H / scale)
    noise = make_perlin(seed)
    freq = 3.0 / ww
    small = Image.new('RGB', (ww, hh))
    pixels = small.load()
    for j in range(hh):
        for i in range(ww):
            v = fbm(noise, i * freq, j * freq, 4, 2.0, 0.55)
            if   v < 0.25: idx = 0
            elif v < 0.50: idx = 1
            elif v < 0.75: idx = 2
            else:          idx = 3
            pixels[i, j] = rgbs[idx]
    big = small.resize((W, H), Image.NEAREST).convert('RGB')
    return embed_epic_mark(big, W, H, rgbs, seed)


# ====================================================================
# Driver
# ====================================================================

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    jobs = [
        ('MARPAT-D',    render_marpat),
        ('WOODLAND-7B', render_woodland),
        ('FRACTAL-G',   render_fractalg),
        ('TERRAIN-X',   render_terrainx),
    ]
    for name, fn in jobs:
        print(f'... rendering {name}')
        # JS uses seed XOR'd with first char code; mirror that for visual parity
        s = SEED ^ ord(name[0])
        img = fn(s)
        out = os.path.join(OUT_DIR, f'{name}.png')
        img.save(out, 'PNG', optimize=True)
        print(f'    -> {out}  ({os.path.getsize(out)//1024} KB)')
    print('DONE.')


if __name__ == '__main__':
    main()
