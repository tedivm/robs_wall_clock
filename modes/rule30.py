from utils.cells import CellRules


class Rule30(CellRules):
    rule_number = 30


def run(gameboard, run_forever=False):
    runner = Rule30(gameboard, run_forever)
    runner.run()
