"""Render one real Craftax frame (pixels) after a few random steps, save as JPEG."""
import sys

import jax
import numpy as np
from PIL import Image

from craftax.craftax.constants import BLOCK_PIXEL_SIZE_IMG
from craftax.craftax.renderer import make_craftax_pixel_renderer
from craftax.craftax_env import make_craftax_env_from_name

out = sys.argv[1]
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0

env = make_craftax_env_from_name("Craftax-Symbolic-v1", auto_reset=True)
params = env.default_params
key = jax.random.PRNGKey(seed)
key, k = jax.random.split(key)
_, state = env.reset(k, params)

# A handful of moves so the player is not frozen on the spawn tile
step = jax.jit(env.step)
for _ in range(12):
    key, ka, ks = jax.random.split(key, 3)
    action = jax.random.randint(ka, (), 1, 5)  # left / right / up / down
    _, state, _, _, _ = step(ks, state, action, params)

render = jax.jit(make_craftax_pixel_renderer(BLOCK_PIXEL_SIZE_IMG, do_night_noise=False))
pixels = np.asarray(render(state))
img = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8))
img.save(out)
print(out, img.size)
