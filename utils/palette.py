import random

import displayio

BLACK = 0x000000
WHITE = 0xFFFFFF


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


def get_palette(colors: int):
    palette = displayio.Palette(colors)
    reset_palette(palette)
    return palette


def reset_palette(palette):
    chunks = 255 // len(palette)
    palette[0] = BLACK
    print(f"Color 0: {palette[0]}")
    random_offset = random.randint(0, 50)
    for i in range(1, len(palette)):
        offset = i * chunks
        palette[i] = colorwheel(offset + random_offset)
        print(f"Color {i}: {palette[i]} at offset {offset}")
