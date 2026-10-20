"""Linear regions of a small random ReLU network on the plane (2 -> 24 -> 24 -> 24).

Each pixel gets the activation pattern of all hidden units; pixels sharing a pattern
lie in the same affine piece. Pieces are coloured, boundaries drawn dark.
"""
import colorsys
import sys

import numpy as np
from PIL import Image

out = sys.argv[1]
W, H, SS = 480, 270, 2  # output size, supersampling
rng = np.random.default_rng(7)

xs = np.linspace(-2.0, 2.0, W * SS)
ys = np.linspace(-1.125, 1.125, H * SS)
X, Y = np.meshgrid(xs, ys)
h = np.stack([X.ravel(), Y.ravel()], axis=1)

bits = []
for fan_in, width in [(2, 24), (24, 24), (24, 24)]:
    Wl = rng.normal(0, np.sqrt(2.0 / fan_in), (fan_in, width))
    bl = rng.normal(0, 0.3, width)
    pre = h @ Wl + bl
    bits.append(pre > 0)
    h = np.maximum(pre, 0)
pattern = np.concatenate(bits, axis=1)

# One integer id per pattern, then one colour per id
_, ids = np.unique(pattern, axis=0, return_inverse=True)
ids = ids.reshape(H * SS, W * SS)
n = ids.max() + 1
hues = (np.arange(n) * 0.618034) % 1.0
palette = np.array([colorsys.hls_to_rgb(0.52 + 0.30 * hh, 0.42 + 0.18 * ((i * 7) % 5) / 4, 0.35)
                    for i, hh in enumerate(hues)])
rgb = palette[ids]

edge = np.zeros_like(ids, dtype=bool)
edge[:, 1:] |= ids[:, 1:] != ids[:, :-1]
edge[1:, :] |= ids[1:, :] != ids[:-1, :]
rgb[edge] = np.array([0x1a, 0x1d, 0x1f]) / 255.0

img = Image.fromarray((rgb * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
img.save(out, quality=85, optimize=True, progressive=True)
print(out, "regions:", n)
