import random
import time

from modes.rain import Rain
from utils.memory import gc_decorator
from utils.palette import colorwheel


class Rule30(Rain):
    current_color = None

    def first_row(self, old, new):
        y = 0

        if self.one_color:
            color = 1
        else:
            if not self.current_color:
                self.current_color = random.randint(1, self.board.max_colors)
            else:
                self.current_color += 1
                if self.current_color >= self.board.max_colors:
                    self.current_color = 1
            color = self.current_color
            print(f"Color: {color}")

        for x in range(old.width):
            left = old[((x - 1) % old.width)] > 0
            current = old[x] > 0
            right = old[((x + 1) % old.width)] > 0

            if left == True and current == False and right == False:
                new[x + y] = color
            elif left == False and current == True and right == True:
                new[x + y] = color
            elif left == False and current == True and right == False:
                new[x + y] = color
            elif left == False and current == False and right == True:
                new[x + y] = color
            else:
                new[x + y] = 0
        return

    @gc_decorator
    def reset(self, output):
        print("Rule 32 reset.")
        self.one_color = random.random() < 0.2
        if self.one_color:
            self.board.palette[1] = colorwheel(random.randint(0, 255))
            start_color = 1
        else:
            self.current_color = random.randint(1, self.board.max_colors)
            start_color = self.current_color

        for i in range(output.height * output.width):
            output[i] = 0
        output[output.width // 2] = start_color


def run(gameboard, run_forever=False):
    runner = Rule30(gameboard, run_forever)
    runner.run()
