# -*- coding: utf-8 -*-
# 外部依存なし(標準ライブラリのみ)でPWA用PNGアイコンを生成する。
# 紫グラデの背景に白い「¥」をSDFベースのアンチエイリアスで描画。
import zlib, struct, math, os

def clamp(x, a, b): return a if x < a else (b if x > b else x)
def lerp(a, b, t): return a + (b - a) * t

def write_png(path, w, h, buf):
    def chunk(typ, data):
        return struct.pack('>I', len(data)) + typ + data + struct.pack('>I', zlib.crc32(typ + data) & 0xffffffff)
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)  # 8bit RGBA
    rb = w * 4
    raw = bytearray()
    for y in range(h):
        raw.append(0)            # filter: none
        raw += buf[y * rb:(y + 1) * rb]
    idat = zlib.compress(bytes(raw), 9)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b''))

def render(size, rounded=True, yscale=1.0):
    half = size / 2.0
    r = 0.22 * size                       # 角丸半径
    c0 = (0x8b, 0x7d, 0xff)               # 左上の色
    c1 = (0x5a, 0x48, 0xc7)               # 右下の色
    W = (255, 255, 255)
    sw = 0.072 * size * yscale            # ¥ストロークの半幅

    def P(fx, fy): return (half + fx * size * yscale, half + fy * size * yscale)
    apex = P(0.0, -0.05)
    segs = [
        (P(-0.23, -0.30), apex),          # 左上の斜め
        (P(0.23, -0.30), apex),           # 右上の斜め
        (apex, P(0.0, 0.32)),             # 縦棒
        (P(-0.20, 0.02), P(0.20, 0.02)),  # 上の横棒
        (P(-0.20, 0.13), P(0.20, 0.13)),  # 下の横棒
    ]
    pre = []
    for (ax, ay), (bx, by) in segs:
        vx, vy = bx - ax, by - ay
        pre.append((ax, ay, vx, vy, vx * vx + vy * vy))

    buf = bytearray(size * size * 4)
    for y in range(size):
        fy = y + 0.5
        for x in range(size):
            fx = x + 0.5
            if rounded:
                qx = abs(fx - half) - (half - r)
                qy = abs(fy - half) - (half - r)
                ox = qx if qx > 0 else 0.0
                oy = qy if qy > 0 else 0.0
                d = math.hypot(ox, oy) + min(max(qx, qy), 0.0) - r
                aa = clamp(0.5 - d, 0, 1)
            else:
                aa = 1.0
            idx = (y * size + x) * 4
            if aa <= 0:
                buf[idx + 3] = 0
                continue
            t = clamp((fx + fy) / (2 * size), 0, 1)
            br = lerp(c0[0], c1[0], t); bg = lerp(c0[1], c1[1], t); bb = lerp(c0[2], c1[2], t)
            dm = 1e18
            for ax, ay, vx, vy, L2 in pre:
                if L2 == 0:
                    dx = fx - ax; dy = fy - ay
                else:
                    tt = ((fx - ax) * vx + (fy - ay) * vy) / L2
                    tt = 0.0 if tt < 0 else (1.0 if tt > 1 else tt)
                    dx = fx - (ax + tt * vx); dy = fy - (ay + tt * vy)
                dd = dx * dx + dy * dy
                if dd < dm: dm = dd
            yk = clamp(sw - math.sqrt(dm) + 0.5, 0, 1)
            buf[idx]     = int(lerp(br, W[0], yk))
            buf[idx + 1] = int(lerp(bg, W[1], yk))
            buf[idx + 2] = int(lerp(bb, W[2], yk))
            buf[idx + 3] = int(aa * 255)
    return bytes(buf)

here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, 'icons')
os.makedirs(out, exist_ok=True)
jobs = [
    ('icon-192.png', 192, True, 1.0),
    ('icon-512.png', 512, True, 1.0),
    ('icon-512-maskable.png', 512, False, 0.8),  # Android maskable: 全面塗り+安全領域
    ('apple-touch-icon.png', 180, False, 1.0),   # iOS: OS側が角丸処理
    ('favicon-32.png', 32, True, 1.0),
]
for name, sz, rnd, ys in jobs:
    write_png(os.path.join(out, name), sz, sz, render(sz, rnd, ys))
    print('wrote', name, sz)
print('all done ->', out)
