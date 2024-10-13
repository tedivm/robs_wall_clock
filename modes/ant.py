import random

from utils.cells import CellCreep
from utils.memory import gc_decorator
from utils.palette import randomize_palette, reset_palette

DIRECTION_NORTH = 0
DIRECTION_EAST = 1
DIRECTION_SOUTH = 2
DIRECTION_WEST = 3


# https://en.wikipedia.org/wiki/Langton%27s_ant
class Ant(CellCreep):
    reset_every = 5

    creeps = []
    min_creeps = 5
    max_creeps = 32

    fun_rules = [
        "RLR",
        "LLRR",
        "LRRRRRLLR",
        "LLRRRLRLRLLR",
    ]

    def process_creep(self, creep, old, new):
        start_x = creep["x"]
        start_y = creep["y"]
        start_cell_color = creep["cell_color"]

        turn_direction = self.rule[start_cell_color]

        if turn_direction == "L":
            creep["direction"] = (creep["direction"] + 1) % 4
        else:
            creep["direction"] = (creep["direction"] - 1) % 4

        if creep["direction"] == DIRECTION_NORTH:
            new_x = start_x
            new_y = (start_y - 1) % old.height
        elif creep["direction"] == DIRECTION_EAST:
            new_x = (start_x + 1) % old.width
            new_y = start_y
        elif creep["direction"] == DIRECTION_SOUTH:
            new_x = start_x
            new_y = (start_y + 1) % old.height
        else:
            new_x = (start_x - 1) % old.width
            new_y = start_y

        if old[new_x + new_y * old.width] == self.ant_color:
            # We have a collision, so just stay still
            return

        # Update Old Position Color
        new[start_x + start_y * old.width] = (start_cell_color + 1) % self.path_colors

        # Update New Position Color
        creep["x"] = new_x
        creep["y"] = new_y
        creep["cell_color"] = old[creep["x"] + creep["y"] * old.width]
        new[creep["x"] + creep["y"] * old.width] = self.ant_color

    @gc_decorator
    def reset(self, output):
        super().reset(output)

        # Update the rule to use as many colors as possible
        base_rule = random.choice(self.fun_rules)
        base_length = len(base_rule)
        max_repeats = (len(self.board.palette) - 1) // base_length
        self.rule = base_rule * random.randint(1, max_repeats)

        self.path_colors = len(self.rule)
        self.ant_color = len(self.rule)
        reset_palette(self.board.palette, self.path_colors + 1)
        print(f"Ant Rule: {self.rule} with {len(self.creeps)} ants.")

    def new_creep(self, output):
        return {
            "x": random.randint(0, output.width - 1),
            "y": random.randint(0, output.height - 1),
            "direction": random.randint(0, 3),
            "cell_color": 0,
        }


def run(gameboard, run_forever=False):
    runner = Ant(gameboard, run_forever)
    runner.run()
