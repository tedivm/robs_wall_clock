import random

from utils.cells import CellTotalistic


class WolframFour(CellTotalistic):
    rules_single = [107395, 107396, 107398, 107399, 107401]
    rules_multiple = [107395, 107396, 107398, 107399, 107401]
    num_colors = 4

    def reset(self, output):
        if random.random() < 0.8:
            self.code = random.choice(self.rules_single)
            self.starting_cells = 1
        else:
            self.code = random.choice(self.rules_multiple)
            self.starting_cells = random.randint(2, output.width // 4)

        print(f"WolframFour Random reset.")
        print(f"Rule: {self.code}")
        print(f"Num Colors: {self.num_colors}")
        print(f"Starting Cells: {self.starting_cells}")

        return super().reset(output)


def run(gameboard, run_forever=False):
    runner = WolframFour(gameboard, run_forever)
    runner.run()
