import random

from utils.memory import gc_decorator
from utils.palette import WHITE, reset_palette


class Cell:

    text_color = WHITE
    random_grid_density = 0.33
    reset_every = 1
    leave_after = 5

    def __init__(self, gameboard, run_forever=False):
        self.run_forever = run_forever
        self.board = gameboard
        self.reset(self.board.b1)
        self.board.set_clock_color(self.text_color)

    @gc_decorator
    def run(self):
        generations = 0
        old_text = ""
        first_run = True
        while True:
            new_text = self.board.it.time_string()
            if new_text != old_text:
                print(f"Updating time: {new_text}")
                print(f"Generations: {generations}")
                old_text = new_text
                self.board.clock_label_1.text = new_text
                self.board.clock_label_2.text = new_text

                if not first_run:
                    print("Checking for game exit conditions.")
                    last_digits = int(new_text[-2:])

                    # Leave this game to start another.
                    if not self.run_forever and last_digits % self.leave_after == 0:
                        print("Leaving Game.")
                        return

                    # Reset the board.
                    if last_digits % self.reset_every == 0:
                        print("Restarting Game.")
                        self.reset(self.board.b1)
                        generations = 0

            self.board.display.root_group = self.board.g1
            self.apply_life_rule(self.board.b1, self.board.b2)
            self.board.display.root_group = self.board.g2
            res = self.apply_life_rule(self.board.b2, self.board.b1)
            generations += 2

            if not res:
                print(f"Game has ended after {generations} generations.")
                self.reset(self.board.b1)
                generations = 0
            first_run = False

    @gc_decorator
    def reset(self, output):
        reset_palette(self.board.palette)
        filler = random.choice(
            [
                self.randomize,
                self.rainbow_wave,
                self.rainbow_horizontal,
                self.rainbow_vertical,
            ]
        )
        filler(output)

    def randomize(self, output):
        for i in range(output.height * output.width):
            if random.random() < self.random_grid_density:
                output[i] = random.randint(1, self.board.max_colors - 1)

    def rainbow_wave(self, output):
        for i in range(output.height * output.width):
            if random.random() < self.random_grid_density:
                output[i] = (i % (self.board.max_colors - 1)) + 1

    def rainbow_vertical(self, output):
        width = output.width
        height = output.height

        # The offset means we can start the rainbow at any point in the spectrum.
        offset = random.randint(0, width)
        spectrum_size = width / (self.board.max_colors - 1)

        for y in range(height):
            yyy = y * width
            for x in range(width):
                if random.random() < self.random_grid_density:
                    adjusted_x = (x + offset) % width
                    output[x + yyy] = int(adjusted_x / spectrum_size) + 1

    def rainbow_horizontal(self, output):
        width = output.width
        height = output.height

        # The offset means we can start the rainbow at any point in the spectrum.
        offset = random.randint(0, height)
        spectrum_size = height / (self.board.max_colors - 1)

        for y in range(height):
            yyy = y * width
            for x in range(width):
                if random.random() < self.random_grid_density:
                    adjusted_y = (y + offset) % height
                    output[x + yyy] = int(adjusted_y / spectrum_size) + 1

    def apply_life_rule(self, old, new):
        raise NotImplementedError()
