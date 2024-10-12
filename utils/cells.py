import random
import time

import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_matrixportal.matrixportal import MatrixPortal

from utils.memory import gc_decorator, logged_gc
from utils.palette import BLACK, WHITE, get_palette


class Cell:

    bit_depth = 2
    max_colors = 16
    life_scale = 1
    text_color = WHITE
    random_grid_density = 0.33
    reset_every = 1
    leave_after = 1

    def __init__(self, network, it, run_forever=False):
        logged_gc("Initializing Cell Board")
        self.network = network
        self.it = it
        self.run_forever = run_forever

        matrixportal = MatrixPortal(
            status_neopixel=board.NEOPIXEL,
            debug=True,
            esp=network._wifi.esp,
            use_wifi=False,
            bit_depth=self.bit_depth,
        )
        matrixportal.network = network
        self.display = matrixportal.graphics.display

        logged_gc("Display Initialized")

        b1 = displayio.Bitmap(
            self.display.width // self.life_scale,
            self.display.height // self.life_scale,
            self.max_colors,
        )
        b2 = displayio.Bitmap(
            self.display.width // self.life_scale,
            self.display.height // self.life_scale,
            self.max_colors,
        )

        logged_gc("Bitmaps Initialized")
        palette = get_palette(self.max_colors)
        self.palette = palette

        tg1 = displayio.TileGrid(b1, pixel_shader=palette)
        tg2 = displayio.TileGrid(b2, pixel_shader=palette)
        g1 = displayio.Group(scale=self.life_scale)
        g1.append(tg1)
        self.display.root_group = g1
        g2 = displayio.Group(scale=self.life_scale)
        g2.append(tg2)

        logged_gc("Groups Initialized")

        old_text = it.time_string()

        TEXT_SCALE_FACTOR = 2
        TEXT_POSITION = ((self.display.width / 2) + 1, (self.display.height / 2))
        clock_label_1 = label.Label(
            terminalio.FONT,
            text=old_text,
            scale=TEXT_SCALE_FACTOR,
            color=self.text_color,
        )
        clock_label_1.anchor_point = (0.5, 0.5)
        clock_label_1.anchored_position = TEXT_POSITION
        g1.append(clock_label_1)

        clock_label_2 = label.Label(
            terminalio.FONT,
            text=old_text,
            scale=TEXT_SCALE_FACTOR,
            color=self.text_color,
        )
        clock_label_2.anchor_point = (0.5, 0.5)
        clock_label_2.anchored_position = TEXT_POSITION
        g2.append(clock_label_2)

        logged_gc("Graphics Initialized")
        self.reset(b1)

        self.clock_label_1 = clock_label_1
        self.clock_label_2 = clock_label_2
        self.b1 = b1
        self.b2 = b2
        self.g1 = g1
        self.g2 = g2

    @gc_decorator
    def run(self):
        generations = 0
        old_text = ""
        first_run = True
        while True:
            new_text = self.it.time_string()
            if new_text != old_text:
                print(f"Updating time: {new_text}")
                print(f"Generations: {generations}")
                old_text = new_text
                self.clock_label_1.text = new_text
                self.clock_label_2.text = new_text

                if not first_run:
                    last_digit = int(new_text[-2])

                    # Leave this game to start another.
                    if not self.run_forever and last_digit % self.leave_after == 0:
                        print("Leaving Game.")
                        return

                    # Reset the board.
                    if last_digit % self.reset_every == 0:
                        print("Restarting Game.")
                        self.reset(self.b1)
                        generations = 0

            self.display.root_group = self.g1
            self.apply_life_rule(self.b1, self.b2)
            self.display.root_group = self.g2
            res = self.apply_life_rule(self.b2, self.b1)
            generations += 2

            if not res:
                print(f"Game has ended after {generations} generations.")
                self.reset(self.b1)
                generations = 0
            first_run = False

    @gc_decorator
    def reset(self, output):
        filler = random.choice(
            [
                self.randomize,
                self.rainbow_wave,
                self.rainbow_horizontal,
                self.rainbow_vertical,
            ]
        )
        filler(output)

    def randomize(self, output):
        for i in range(output.height * output.width):
            if random.random() < self.random_grid_density:
                output[i] = random.randint(1, self.max_colors - 1)

    def rainbow_wave(self, output):
        for i in range(output.height * output.width):
            if random.random() < self.random_grid_density:
                output[i] = (i % (self.max_colors - 1)) + 1

    def rainbow_vertical(self, output):
        width = output.width
        height = output.height

        # The offset means we can start the rainbow at any point in the spectrum.
        offset = random.randint(0, width)
        spectrum_size = width / (self.max_colors - 1)

        for y in range(height):
            yyy = y * width
            for x in range(width):
                if random.random() < self.random_grid_density:
                    adjusted_x = (x + offset) % width
                    output[x + yyy] = int(adjusted_x / spectrum_size) + 1

    def rainbow_horizontal(self, output):
        width = output.width
        height = output.height

        # The offset means we can start the rainbow at any point in the spectrum.
        offset = random.randint(0, height)
        spectrum_size = height / (self.max_colors - 1)

        for y in range(height):
            yyy = y * width
            for x in range(width):
                if random.random() < self.random_grid_density:
                    adjusted_y = (y + offset) % height
                    output[x + yyy] = int(adjusted_y / spectrum_size) + 1

    def apply_life_rule(self, old, new):
        raise NotImplementedError()
