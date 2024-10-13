import random

from utils.cells import Cell
from utils.memory import gc_decorator
from utils.palette import BLACK, WHITE, reset_palette


class Rain(Cell):

    # Function adapted from https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/CircuitPython_RGBMatrix/life/code.py
    @gc_decorator
    def apply_life_rule(self, old, new):
        width = old.width
        height = old.height
        for y in range(height):
            if y == 0:
                self.first_row(old, new)
                continue

            yyy = y * width
            ym1 = ((y + height - 1) % height) * width
            for x in range(width):
                new[x + yyy] = old[x + ym1]

        return True

    def first_row(self, old, new):
        y = 0

        if self.mode == "spectrum":
            self.current_color += 1
            if self.current_color >= self.board.max_colors:
                self.current_color = 1

        for x in range(old.width):
            if random.random() < self.random_grid_density:
                if self.mode == "one":
                    new[x + y] = self.color
                elif self.mode == "spectrum":
                    new[x + y] = self.current_color
                else:
                    new[x + y] = random.randint(1, self.board.max_colors - 1)
            else:
                new[x + y] = 0

        return

    @gc_decorator
    def reset(self, output):
        print("Rain reset")

        random_value = random.random()
        self.random_grid_density = random.randint(22, 66) / 100
        if random_value <= 0.20:
            self.mode = "one"
            self.color = random.randint(1, self.board.max_colors - 1)
        elif random_value <= 0.60:
            self.mode = "random"
            reset_palette(self.board.palette)
        else:
            self.mode = "spectrum"
            reset_palette(self.board.palette)
            self.current_color = random.randint(1, self.board.max_colors - 1)

        if self.mode == "random" or self.mode == "spectrum":
            if random.random() < 0.5:
                self.random_grid_density = 1

        for i in range(output.height * output.width):
            output[i] = 0

        if self.random_grid_density == 1:
            print("BLACK CLOCK")
            self.board.set_clock_color(BLACK)
        else:
            print("WHITE CLOCK")
            self.board.set_clock_color(WHITE)


def run(gameboard, run_forever=False):
    runner = Rain(gameboard, run_forever)
    runner.run()
