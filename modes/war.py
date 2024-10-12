import random

from utils.cells import Cell
from utils.memory import gc_decorator
from utils.palette import BLACK


class War(Cell):

    text_color = BLACK
    random_grid_density = 1
    reset_every = 5

    # Algorithm adapted from https://www.reddit.com/r/cellular_automata/comments/1bmicq6/a_simple_cellular_automaton_that_simulates_war/
    # Function adapted from https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/CircuitPython_RGBMatrix/life/code.py
    @gc_decorator
    def apply_life_rule(self, old, new):
        width = old.width
        height = old.height
        colors_active = set(list())
        for y in range(height):
            yyy = y * width
            ym1 = ((y + height - 1) % height) * width
            yp1 = ((y + 1) % height) * width
            xm1 = width - 1
            for x in range(width):
                xp1 = (x + 1) % width

                use_cell = random.randint(1, 8)
                colors_active.add(old[x + yyy])

                # Check all 8 neighbors.
                # Although this is a bit verbose, it is faster than using loops or functions.
                if use_cell == 1:
                    new[x + yyy] = old[xm1 + ym1]

                if use_cell == 2:
                    new[x + yyy] = old[xm1 + yyy]

                if use_cell == 3:
                    new[x + yyy] = old[xm1 + yp1]

                if use_cell == 4:
                    new[x + yyy] = old[x + ym1]

                if use_cell == 5:
                    new[x + yyy] = old[x + yp1]

                if use_cell == 6:
                    new[x + yyy] = old[xp1 + ym1]

                if use_cell == 7:
                    new[x + yyy] = old[xp1 + yyy]

                if use_cell == 8:
                    new[x + yyy] = old[xp1 + yp1]

                # If the color is 9, then the cell will not change.
                if use_cell == 9:
                    new[x + yyy] = old[x + yyy]

                xm1 = x
        return len(colors_active) > 1


def run(network, it, run_forever=False):
    runner = War(network, it, run_forever)
    runner.run()
