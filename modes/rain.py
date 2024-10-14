import random

from utils.cells import CellLine
from utils.memory import gc_decorator
from utils.palette import BLACK, WHITE


class Rain(CellLine):

    def first_row(self, old, new):
        y = 0
        has_cells = False
        if self.mode == "spectrum":
            self.current_color += 1
            if self.current_color >= self.board.max_colors:
                self.current_color = 1

        for x in range(old.width):
            if random.random() < self.random_grid_density:
                has_cells = True
                if self.mode == "one":
                    new[x + y] = self.color
                elif self.mode == "spectrum":
                    new[x + y] = self.current_color
                else:
                    new[x + y] = random.randint(1, self.board.max_colors - 1)
            else:
                new[x + y] = 0

        return has_cells

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
            self.board.reset_palette()
        else:
            self.mode = "spectrum"
            self.board.reset_palette()
            self.current_color = random.randint(1, self.board.max_colors - 1)

        if self.mode == "random" or self.mode == "spectrum":
            if random.random() < 0.2:
                self.random_grid_density = 1

        self.board.clear_background()

        if self.random_grid_density == 1:
            print("BLACK CLOCK")
            self.board.set_clock_color(BLACK)
        else:
            print("WHITE CLOCK")
            self.board.set_clock_color(WHITE)


def run(gameboard, run_forever=False):
    runner = Rain(gameboard, run_forever)
    runner.run()
