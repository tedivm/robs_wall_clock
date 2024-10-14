import random

from utils.cells import CellRules


class WolframTwo(CellRules):
    reset_every = 1

    rules_single = [30, 45, 57, 86, 105, 110, 124, 137, 182, 193]
    rules_multiple = [30, 45, 54, 57, 62, 86, 110, 120, 124, 137, 182, 193]

    def reset(self, output):
        if random.random() < 0.50:
            self.rule_number = random.choice(self.rules_single)
            self.starting_cells = 1
        else:
            self.rule_number = random.choice(self.rules_multiple)
            self.starting_cells = random.randint(2, output.width // 3)

        print(f"WolframTwo Random reset.")
        print(f"Rule: {self.rule_number}")
        print(f"Num Colors: 2")
        print(f"Starting Cells: {self.starting_cells}")

        return super().reset(output)


def run(gameboard, run_forever=False):
    runner = WolframTwo(gameboard, run_forever)
    runner.run()
