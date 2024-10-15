import random

import displayio

from utils.shuffle import shuffle

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def colorwheel(pos):
    pos = pos % 255
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def get_palette(colors: int, brightness=1):
    palette = displayio.Palette(colors)
    reset_palette(palette, brightness=brightness)
    return palette


def reset_palette(palette, max_colors=None, brightness=1):
    dimness = 1 - brightness
    if max_colors is None:
        max_colors = len(palette)

    chunks = 255 // max_colors
    palette[0] = BLACK
    print(f"Regenerating Palette with brightness {brightness}.")
    random_offset = random.randint(0, 255)
    for i in range(1, max_colors):
        offset = i * chunks
        palette[i] = dim_color(colorwheel(offset + random_offset), dimness)
        print(f"Color {i}: {palette[i]}, offset: {offset}")


def randomize_palette(palette):
    reset_palette(palette)
    palette[0] = BLACK
    options = []

    for i in range(1, len(palette) - 1):
        options.append(palette[i])

    shuffle(options)

    for i in range(1, len(palette) - 1):
        palette[i] = options.pop()


def interpolate(color_a, color_b, t):
    # 'color_a' and 'color_b' are RGB tuples
    # 't' is a value between 0.0 and 1.0
    # this is a naive interpolation
    return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))


def dim_color(color, factor):
    if factor > 1.0:
        raise ValueError("Factor must be less than or equal to 1.0")
    if factor >= 0.95:
        return color
    if factor < 0.0:
        raise ValueError("Factor must be greater than or equal to 0.0")
    if factor <= 0.01:
        return color
    return interpolate(color, (0, 0, 0), factor)
