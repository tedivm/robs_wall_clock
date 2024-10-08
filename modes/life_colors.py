import random
import board
import displayio
import terminalio

from adafruit_display_text import label
from adafruit_matrixportal.matrixportal import MatrixPortal

from utils.palette import get_palette, BLACK, WHITE
from utils.memory import gc_decorator, logged_gc

LIFE_SCALE = 1
MAX_COLORS = 16
BIT_DEPTH = 2

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

            neighbor_count = 0
            neighbor_colors = {}

            # Check all 8 neighbors.
            # Although this is a bit verbose, it is faster than using loops or functions.
            if old[xm1 + ym1] > 0:
                neighbor_count += 1
                color = old[xm1 + ym1]
                if color in neighbor_colors:
                    neighbor_colors[color] += 1
                else:
                    neighbor_colors[color] = 1

            if old[xm1 + yyy] > 0:
                neighbor_count += 1
                color = old[xm1 + yyy]
                if color in neighbor_colors:
                    neighbor_colors[color] += 1
                else:
                    neighbor_colors[color] = 1

            if old[xm1 + yp1] > 0:
                neighbor_count += 1
                color = old[xm1 + yp1]
                if color in neighbor_colors:
                    neighbor_colors[color] += 1
                else:
                    neighbor_colors[color] = 1

            if old[x   + ym1] > 0:
                neighbor_count += 1
                color = old[x   + ym1]
                if color in neighbor_colors:
                    neighbor_colors[color] += 1
                else:
                    neighbor_colors[color] = 1

            if old[x   + yp1] > 0:
                neighbor_count += 1
                color = old[x   + yp1]
                if color in neighbor_colors:
                    neighbor_colors[color] += 1
                else:
                    neighbor_colors[color] = 1

            if old[xp1 + ym1] > 0:
                neighbor_count += 1
                color = old[xp1 + ym1]
                if color in neighbor_colors:
                    neighbor_colors[color] += 1
                else:
                    neighbor_colors[color] = 1

            if old[xp1 + yyy] > 0:
                neighbor_count += 1
                color = old[xp1 + yyy]
                if color in neighbor_colors:
                    neighbor_colors[color] += 1
                else:
                    neighbor_colors[color] = 1

            if old[xp1 + yp1] > 0:
                neighbor_count += 1
                color = old[xp1 + yp1]
                if color in neighbor_colors:
                    neighbor_colors[color] += 1
                else:
                    neighbor_colors[color] = 1

            if neighbor_count == 3 or (neighbor_count == 2 and int(old[x+yyy])):

                if old[x+yyy]:
                    # If the cell is alive, keep the same color.
                    next_color = old[x+yyy]
                else:
                    # If the cell is dead, choose the most common color from the neighbors.

                    next_color = False
                    for color, count in neighbor_colors.items():
                        # If we haven't chosen a color yet start with the current one.
                        if not next_color:
                            next_color = color
                            continue

                        # If the current color has more neighbors, choose it.
                        if count > neighbor_colors[next_color]:
                            next_color = color
                            continue

                        # If the current color has the same number of neighbors, randomly choose between the two.
                        if count == neighbor_colors[next_color]:
                            next_color = random.choice([next_color, color])


            else:
                next_color = BLACK

            new[x+yyy] = next_color
            xm1 = x

@gc_decorator
def randomize(output, fraction=0.33):
    for i in range(output.height * output.width):
        if random.random() < fraction:
            output[i] = random.randint(1, MAX_COLORS-1)


def run(network, it):
    logged_gc("Starting Colorful Life")

    matrixportal = MatrixPortal(
        status_neopixel=board.NEOPIXEL,
        debug=True,
        esp=network._wifi.esp,
        use_wifi=False,
        bit_depth=BIT_DEPTH,
    )
    matrixportal.network = network
    display = matrixportal.graphics.display

    logged_gc("Display Initialized")

    b1 = displayio.Bitmap(display.width//LIFE_SCALE, display.height//LIFE_SCALE, MAX_COLORS)
    b2 = displayio.Bitmap(display.width//LIFE_SCALE, display.height//LIFE_SCALE, MAX_COLORS)

    logged_gc("Bitmaps Initialized")
    palette = get_palette(MAX_COLORS)

    tg1 = displayio.TileGrid(b1, pixel_shader=palette)
    tg2 = displayio.TileGrid(b2, pixel_shader=palette)
    g1 = displayio.Group(scale=LIFE_SCALE)
    g1.append(tg1)
    display.root_group = g1
    g2 = displayio.Group(scale=LIFE_SCALE)
    g2.append(tg2)

    logged_gc("Groups Initialized")

    old_text = it.time_string()

    TEXT_SCALE_FACTOR = 2
    TEXT_POSITION = ((display.width / 2) + 1, (display.height / 2))
    clock_label_1 = label.Label(
        terminalio.FONT,
        text=old_text,
        scale=TEXT_SCALE_FACTOR,
        color=WHITE,
    )
    clock_label_1.anchor_point = (0.5, 0.5)
    clock_label_1.anchored_position = TEXT_POSITION
    g1.append(clock_label_1)

    clock_label_2 = label.Label(
        terminalio.FONT,
        text=old_text,
        scale=TEXT_SCALE_FACTOR,
        color=WHITE,
    )
    clock_label_2.anchor_point = (0.5, 0.5)
    clock_label_2.anchored_position = TEXT_POSITION
    g2.append(clock_label_2)

    logged_gc("Labels Initialized")

    randomize(b1)
    generations = 0

    logged_gc("Starting Life Loop")
    while True:
        new_text = it.time_string()
        if new_text != old_text:
            print(f"Updating time: {new_text}")
            print(f"Generations: {generations}")
            old_text = new_text
            clock_label_1.text = new_text
            clock_label_2.text = new_text
            randomize(b1)
            generations = 0

        display.root_group = g1
        apply_life_rule(b1, b2)
        display.root_group = g2
        apply_life_rule(b2, b1)
        generations += 2

