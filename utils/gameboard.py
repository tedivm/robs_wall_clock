import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_matrixportal.matrixportal import MatrixPortal

from utils.memory import logged_gc
from utils.palette import BLACK, WHITE, dim_color, get_palette, reset_palette


class GameBoard:

    bit_depth = 3

    def __init__(
        self,
        network,
        it,
        life_scale=1,
        max_colors=16,
        text_color=WHITE,
        clock_enabled=True,
        brightness=1,
        time_format="24",
    ):
        logged_gc("Initializing Game Board", log_always=True)
        self.network = network
        self.it = it
        self.life_scale = life_scale
        self.max_colors = max_colors
        self.text_color = text_color
        self.clock_enabled = clock_enabled
        self.brightness = brightness
        self.time_format = time_format

        matrixportal = MatrixPortal(
            status_neopixel=board.NEOPIXEL,
            debug=True,
            esp=network._wifi.esp,
            use_wifi=False,
            bit_depth=self.bit_depth,
        )
        matrixportal.network = network
        self.display = matrixportal.graphics.display

        logged_gc("Display Initialized", log_always=True)

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

        logged_gc("Bitmaps Initialized", log_always=True)
        palette = get_palette(self.max_colors)
        self.palette = palette

        tg1 = displayio.TileGrid(b1, pixel_shader=palette)
        tg2 = displayio.TileGrid(b2, pixel_shader=palette)
        g1 = displayio.Group(scale=self.life_scale)
        g1.append(tg1)
        self.display.root_group = g1
        g2 = displayio.Group(scale=self.life_scale)
        g2.append(tg2)

        logged_gc("Groups Initialized", log_always=True)

        if self.clock_enabled:
            old_text = self.get_time_string()
        else:
            old_text = ""

        TEXT_SCALE_FACTOR = 2
        TEXT_POSITION = ((self.display.width / 2) + 1, (self.display.height / 2))
        clock_label_1 = label.Label(
            terminalio.FONT,
            text=old_text,
            scale=TEXT_SCALE_FACTOR,
            color=BLACK,
        )
        clock_label_1.anchor_point = (0.5, 0.5)
        clock_label_1.anchored_position = TEXT_POSITION
        g1.append(clock_label_1)

        clock_label_2 = label.Label(
            terminalio.FONT,
            text=old_text,
            scale=TEXT_SCALE_FACTOR,
            color=BLACK,
        )
        clock_label_2.anchor_point = (0.5, 0.5)
        clock_label_2.anchored_position = TEXT_POSITION
        g2.append(clock_label_2)

        logged_gc("Graphics Initialized", log_always=True)

        self.clock_label_1 = clock_label_1
        self.clock_label_2 = clock_label_2
        self.b1 = b1
        self.b2 = b2
        self.g1 = g1
        self.g2 = g2

        self.test_screen()
        self.it.get_time()
        self.set_clock_color(self.text_color)

    def test_screen(self):
        print("Initializing Test Screen")
        for i in range(self.b1.height * self.b1.width):
            color = (i % (self.max_colors - 1)) + 1
            self.b1[i] = color
            self.b2[i] = color

    def disable_clock(self):
        self.clock_enabled = False
        self.clock_label_1.text = ""
        self.clock_label_2.text = ""

    def get_time_string(self):
        return self.it.time_string(format=self.time_format)

    def enable_clock(self):
        self.clock_enabled = True
        self.set_clock(self.get_time_string())

    def set_clock(self, text):
        if self.clock_enabled:
            self.clock_label_1.text = text
            self.clock_label_2.text = text

    def set_clock_color(self, color):
        if color != BLACK:
            color = dim_color(color, self.brightness)

        self.clock_label_1.color = color
        self.clock_label_2.color = color

    def clear_background(self):
        self.b1.fill(0)
        self.b2.fill(0)

    def reset_palette(self, max_colors=None):
        self.clear_background()
        reset_palette(self.palette, max_colors, self.brightness)
