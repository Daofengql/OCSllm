"""Create the small project-local OCS tray icon without external packages."""
from __future__ import annotations
import math, struct, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def inside_round(x, y, left, top, right, bottom, radius):
    if left + radius <= x <= right - radius or top + radius <= y <= bottom - radius:
        return left <= x <= right and top <= y <= bottom
    cx = left + radius if x < left + radius else right - radius
    cy = top + radius if y < top + radius else bottom - radius
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2

def inside_bubble(x, y):
    # Rounded white speech bubble.
    if 42 <= x <= 215 and 54 <= y <= 169:
        r = 28
        if 42 + r <= x <= 215 - r or 54 + r <= y <= 169 - r:
            return True
        cx = 42 + r if x < 42 + r else 215 - r
        cy = 54 + r if y < 54 + r else 169 - r
        return (x - cx) ** 2 + (y - cy) ** 2 <= r * r
    # Tail.
    return 55 <= x <= 125 and 150 <= y <= 205 and y >= 205 - (x - 55) * 0.8

def circle(x, y, cx, cy, r):
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r

def make_png(size):
    scale = 4
    w = h = size
    W = H = size * scale
    pixels = []
    for yy in range(H):
        y = (yy + .5) / scale
        row = bytearray()
        for xx in range(W):
            x = (xx + .5) / scale
            a = 255 if inside_round(x, y, 7, 7, size - 8, size - 8, max(3, size * .21)) else 0
            # Diagonal blue-to-indigo gradient.
            t = max(0.0, min(1.0, (x + y) / (2 * size)))
            r, g, b = int(28 - 6*t), int(78 - 30*t), int(216 - 35*t)
            if a:
                if inside_bubble(x * 256 / size, y * 256 / size):
                    r, g, b = 248, 250, 252
                # Colored answer nodes.
                for cx, cy, cr, color in ((82, 103, 12, (14, 165, 233)), (128, 103, 12, (99, 102, 241)), (174, 103, 12, (16, 185, 129))):
                    if circle(x * 256 / size, y * 256 / size, cx, cy, cr):
                        r, g, b = color
                # White check / connection stroke.
                X, Y = x * 256 / size, y * 256 / size
                if (abs(Y - (X - 116) * .72 - 139) < 4.5 and 116 <= X <= 139) or (abs(Y + (X - 139) * .72 - 156) < 4.5 and 139 <= X <= 170):
                    r, g, b = 28, 78, 216
            row.extend((r, g, b, a))
        pixels.append(row)
    # Box downsample with alpha-aware averaging.
    down = bytearray()
    for y in range(size):
        for x in range(size):
            vals = [pixels[y*scale+j][(x*scale+i)*4:(x*scale+i+1)*4] for j in range(scale) for i in range(scale)]
            down.extend(tuple(sum(v[k] for v in vals)//len(vals) for k in range(4)))
    raw = b''.join(b'\x00' + bytes(down[y*size*4:(y+1)*size*4]) for y in range(size))
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')

def main():
    sizes = [16, 32, 48, 256]
    images = [make_png(s) for s in sizes]
    header = struct.pack('<HHH', 0, 1, len(images))
    offset = 6 + 16 * len(images)
    entries, body = [], []
    for size, image in zip(sizes, images):
        entries.append(struct.pack('<BBBBHHII', 0 if size == 256 else size, 0 if size == 256 else size, 0, 0, 1, 32, len(image), offset))
        body.append(image); offset += len(image)
    (ROOT / 'app.ico').write_bytes(header + b''.join(entries) + b''.join(body))
    (ROOT / 'app-preview.png').write_bytes(images[-1])
    print('wrote', ROOT / 'app.ico')

if __name__ == '__main__': main()
