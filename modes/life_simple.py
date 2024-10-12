import random

from utils.cells import Cell
from utils.memory import gc_decorator
from utils.palette import colorwheel


class LifeSimple(Cell):

    # Function adapted from https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/CircuitPython_RGBMatrix/life/code.py
    @gc_decorator
    def apply_life_rule(self, old, new):
        width = old.width
        height = old.height
        grid_size = width * height
        living_cells = 0
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
                if neighbors == 3 or (neighbors == 2 and old[x + yyy]):
                    new[x + yyy] = True
                    living_cells += 1
                else:
                    new[x + yyy] = False

                xm1 = x
        return living_cells / grid_size > 0.03

    @gc_decorator
    def reset(self, output):
        self.board.palette[1] = colorwheel(random.randint(0, 255))
        for i in range(output.height * output.width):
            output[i] = random.random() < self.random_grid_density


def run(gameboard, run_forever=False):
    runner = LifeSimple(gameboard, run_forever)
    runner.run()
