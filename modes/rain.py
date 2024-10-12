import random

from utils.cells import Cell
from utils.memory import gc_decorator


class Rain(Cell):

    # Function adapted from https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/CircuitPython_RGBMatrix/life/code.py
    @gc_decorator
    def apply_life_rule(self, old, new):
        width = old.width
        height = old.height
        for y in range(height):
            yyy = y * width
            ym1 = ((y + height - 1) % height) * width
            for x in range(width):
                if y == 0:
                    if random.random() < self.random_grid_density:
                        if self.one_color:
                            new[x + yyy] = self.color
                        else:
                            new[x + yyy] = random.randint(1, self.max_colors - 1)
                    else:
                        new[x + yyy] = 0
                else:
                    new[x + yyy] = old[x + ym1]

        return True

    @gc_decorator
    def reset(self, output):
        self.one_color = random.random() < 0.5
        if self.one_color:
            self.color = random.randint(1, self.max_colors - 1)
        for i in range(output.height * output.width):
            output[i] = 0


def run(network, it, run_forever=False):
    runner = Rain(network, it, run_forever)
    runner.run()
