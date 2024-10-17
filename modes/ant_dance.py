import random

from modes.ant import Ant
from utils.memory import gc_decorator


# https://en.wikipedia.org/wiki/Langton%27s_ant
class Dance(Ant):

    def place_creeps(self, output):
        chance = random.random()
        if chance < 0.25:
            # Even Separation - just plop them on the grid, lined up in the middle.
            creep1 = self.new_creep(output)
            creep1["x"] = output.width // 3
            creep1["y"] = output.height // 2
            self.creeps.append(creep1)
            creep2 = self.new_creep(output)
            creep2["x"] = output.width // 3 * 2
            creep2["y"] = output.height // 2
            self.creeps.append(creep2)
        else:
            distance = random.randint(1, 5)
            creep1 = self.new_creep(output)
            creep1["x"] = (output.width // 2) - distance
            creep1["y"] = output.height // 2
            self.creeps.append(creep1)
            creep2 = self.new_creep(output)
            creep2["x"] = (output.width // 2) + distance
            creep2["y"] = output.height // 2
            self.creeps.append(creep2)

        # Dancers - put two creeps close together so they interact.
        if random.random() < 0.3:
            # Since they both move in the same direction they aren't symmetrical.
            direction_1 = random.randint(0, 3)
            direction_2 = direction_1
        else:
            # In this mode the creeps mirror each other until they interact.
            # This is, in my super bias opinion, the prettiest automata in this entire project.
            if random.random() < 0.5:
                direction_1 = 1
                direction_2 = 3
            else:
                direction_1 = 3
                direction_2 = 1

        creep1["direction"] = direction_1
        creep2["direction"] = direction_2

        return


def run(gameboard, run_forever=False):
    runner = Dance(gameboard, run_forever)
    runner.run()
