import random

from utils.cells import CellTotalistic


class WolframThree(CellTotalistic):
    rules_single = [357, 420, 600, 777, 946, 948, 966, 1599, 1635, 1884]
    rules_multiple = [357, 420, 600, 777, 1599]

    def reset(self, output):
        if random.random() < 0.50:
            self.code = random.choice(self.rules_single)
            self.starting_cells = 1
        else:
            self.code = random.choice(self.rules_multiple)
            self.starting_cells = random.randint(2, output.width // 3)

        print(f"WolframThree Random reset.")
        print(f"Rule: {self.code}")
        print(f"Num Colors: {self.num_colors}")
        print(f"Starting Cells: {self.starting_cells}")
        return super().reset(output)


def run(gameboard, run_forever=False):
    runner = WolframThree(gameboard, run_forever)
    runner.run()
