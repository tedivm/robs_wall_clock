import random

from utils.cells import CellRules


class RuleRandom(CellRules):
    reset_every = 1

    rules_single = [30, 45, 57, 86, 105, 110, 124, 193]
    rules_multiple = [30, 45, 54, 57, 86, 110, 120, 124, 193]

    def reset(self, output):
        if random.random() < 0.33:
            self.rule_number = random.choice(self.rules_single)
            self.starting_cells = 1
        else:
            self.rule_number = random.choice(self.rules_multiple)
            self.starting_cells = random.randint(2, output.width // 3)

        print(
            f"Rule Random reset: rule {self.rule_number} with {self.starting_cells} starting cells."
        )
        return super().reset(output)


def run(gameboard, run_forever=False):
    runner = RuleRandom(gameboard, run_forever)
    runner.run()
