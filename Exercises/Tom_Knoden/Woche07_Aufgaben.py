import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

class BreakoutGame:
    def __init__(self, program):
        self.int_computer = IntComputer(self.get_input, self.process_output)
        self.program = program
        self.screen = {}
        self.score = 0

    def get_input(self):
        # For Part 2, you can implement paddle control logic here.
        # For now, we keep the paddle in position (return 0).
        return 0

    def process_output(self, value):
        if len(self.int_computer.output) % 3 == 0:
            x, y, tile_type = self.int_computer.output[-3:]
            if x == -1 and y == 0:
                self.score = tile_type
            else:
                self.screen[(x, y)] = tile_type

    def run_game(self):
        self.int_computer.run(self.program)

    def visualize_game(self):
        min_x = min(coord[0] for coord in self.screen)
        max_x = max(coord[0] for coord in self.screen)
        min_y = min(coord[1] for coord in self.screen)
        max_y = max(coord[1] for coord in self.screen)

        grid = np.zeros((max_y - min_y + 1, max_x - min_x + 1))

        for coord, tile_type in self.screen.items():
            x, y = coord
            grid[y - min_y, x - min_x] = tile_type

        plt.imshow(grid, cmap='viridis', interpolation='none', aspect='equal')
        plt.title(f'Score: {self.score}')
        plt.show()

# Load the program from the file using PathLib
input_file_path = Path('data/breakout_commands.txt')
with input_file_path.open() as f:
    program = list(map(int, f.readline().strip().split(',')))

# PART 1
game_part1 = BreakoutGame(program.copy())
game_part1.run_game()
game_part1.visualize_game()

# PART 2
program[0] = 2
game_part2 = BreakoutGame(program.copy())
game_part2.run_game()
game_part2.visualize_game()
print(f'Score: {game_part2.score}')
