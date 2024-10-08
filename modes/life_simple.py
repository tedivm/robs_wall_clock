import gc
import random

import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_matrixportal.matrixportal import MatrixPortal

from utils.palette import WHITE, BLACK, colorwheel
from utils.memory import gc_decorator, logged_gc

LIFE_SCALE = 1
MAX_COLORS = 4

# Function adapted from https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/CircuitPython_RGBMatrix/life/code.py
@gc_decorator
def apply_life_rule(old, new):
    width = old.width
    height = old.height
    for y in range(height):
        yyy = y * width
        ym1 = ((y + height - 1) % height) * width
        yp1 = ((y + 1) % height) * width
        xm1 = width - 1
        for x in range(width):
            xp1 = (x + 1) % width
            # fmt: off
            neighbors = (
                old[xm1 + ym1] + old[xm1 + yyy] + old[xm1 + yp1] +
                old[x   + ym1] +                  old[x   + yp1] +
                old[xp1 + ym1] + old[xp1 + yyy] + old[xp1 + yp1])
            # fmt: on
            new[x + yyy] = neighbors == 3 or (neighbors == 2 and old[x + yyy])
            xm1 = x

@gc_decorator
def randomize(output, fraction=0.33):
    for i in range(output.height * output.width):
        output[i] = random.random() < fraction


def run(network, it):
    logged_gc()
    matrixportal = MatrixPortal(
        status_neopixel=board.NEOPIXEL,
        debug=True,
        esp=network._wifi.esp,
        use_wifi=False,
        bit_depth=2,
    )
    matrixportal.network = network
    display = matrixportal.graphics.display

    logged_gc()

    b1 = displayio.Bitmap(
        display.width // LIFE_SCALE, display.height // LIFE_SCALE, MAX_COLORS
    )
    b2 = displayio.Bitmap(
        display.width // LIFE_SCALE, display.height // LIFE_SCALE, MAX_COLORS
    )
    palette = displayio.Palette(MAX_COLORS)

    palette[0] = BLACK
    palette[1] = colorwheel(random.randint(0, 255))

    tg1 = displayio.TileGrid(b1, pixel_shader=palette)
    tg2 = displayio.TileGrid(b2, pixel_shader=palette)
    g1 = displayio.Group(scale=LIFE_SCALE)
    g1.append(tg1)
    display.root_group = g1
    g2 = displayio.Group(scale=LIFE_SCALE)
    g2.append(tg2)

    old_text = it.time_string()

    TEXT_SCALE_FACTOR = 2
    TEXT_POSITION = ((display.width / 2) + 1, (display.height / 2))
    clock_label_1 = label.Label(
        font=terminalio.FONT,
        text=old_text,
        scale=TEXT_SCALE_FACTOR,
        color=WHITE,
    )
    clock_label_1.anchor_point = (0.5, 0.5)
    clock_label_1.anchored_position = TEXT_POSITION
    g1.append(clock_label_1)

    clock_label_2 = label.Label(
        font=terminalio.FONT,
        text=old_text,
        scale=TEXT_SCALE_FACTOR,
        color=WHITE,
    )
    clock_label_2.anchor_point = (0.5, 0.5)
    clock_label_2.anchored_position = TEXT_POSITION

    g2.append(clock_label_2)

    randomize(b1)
    generations = 0
    while True:

        new_text = it.time_string()
        if new_text != old_text:
            print(f"Updating time: {new_text}")
            print(f"Generations: {generations}")
            old_text = new_text
            clock_label_1.text = new_text
            clock_label_2.text = new_text
            palette[1] = colorwheel(random.randint(0, 255))
            randomize(b1)
            generations = 0

        display.root_group = g1
        apply_life_rule(b1, b2)
        display.root_group = g2
        apply_life_rule(b2, b1)
        generations += 2
