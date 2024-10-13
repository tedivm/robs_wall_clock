import random

from utils.cells import CellRules


class RuleRandom(CellRules):
    reset_every = 1

    def reset(self, output):
        if random.random() < 0.20:
            self.rule_number = 30
            self.starting_cells = 1
        else:
            self.rule_number = random.choice([30, 90, 110, 120])
            self.starting_cells = random.randint(1, output.width // 3)

        print(
            f"Rule Random reset: rule {self.rule_number} with {self.starting_cells} starting cells."
        )
        return super().reset(output)


def run(gameboard, run_forever=False):
    runner = RuleRandom(gameboard, run_forever)
    runner.run()
