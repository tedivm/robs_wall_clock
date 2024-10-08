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

    chunks = 255 // colors

    palette[0] = BLACK
    for i in range(1, colors):
        offset = i * chunks
        palette[i] = colorwheel(offset)
        print(f"Color {i}: {palette[i]} at offset {offset}")

    return palette
