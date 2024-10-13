import random

from utils.cells import CellGrid
from utils.memory import gc_decorator
from utils.palette import BLACK


class ColorLife(CellGrid):

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

                if old[x + ym1] > 0:
                    neighbor_count += 1
                    color = old[x + ym1]
                    if color in neighbor_colors:
                        neighbor_colors[color] += 1
                    else:
                        neighbor_colors[color] = 1

                if old[x + yp1] > 0:
                    neighbor_count += 1
                    color = old[x + yp1]
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

                if neighbor_count == 3 or (neighbor_count == 2 and int(old[x + yyy])):
                    living_cells += 1
                    if old[x + yyy]:
                        # If the cell is alive, keep the same color.
                        next_color = old[x + yyy]
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

                new[x + yyy] = next_color
                xm1 = x
        return living_cells / grid_size > 0.03


def run(gameboard, run_forever=False):
    runner = ColorLife(gameboard, run_forever)
    runner.run()
