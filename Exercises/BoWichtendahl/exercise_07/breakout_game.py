
from int_computer import IntComputer
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import os


class BreakoutGame:
    def __init__(self, commands_path: Path = Path(__file__).parents[3] / 'data' / 'breakout_commands.txt',
                 export_movie: bool = False) -> None:
        def input_setter_no_movie() -> int:
            self._analyse_frame_update()
            if self._paddle_x < self._ball_x:
                return 1
            if self._paddle_x > self._ball_x:
                return -1
            return 0

        def input_setter_movie() -> int:
            return_val = input_setter_no_movie()

            fig, ax = plt.subplots()
            ax.set_axis_off()
            ax.set_title(f'Score: {self._score}', fontsize=15)
            ax.imshow(self._frame)
            plt.savefig(f'img_out/{str(self._frame_counter).zfill(5)}.png', bbox_inches='tight')
            plt.close()
            self._frame_counter += 1

            return return_val

        def output_collector(out_val: int) -> None:
            self._update_data.append(out_val)

        if export_movie:
            self._computer = IntComputer(input_setter_movie, output_collector)
            self._frame_counter = 0
            Path.mkdir(Path.cwd() / 'img_out')
        else:
            self._computer = IntComputer(input_setter_no_movie, output_collector)

        with commands_path.open('r') as commands_in:
            self._commands = [int(command.strip()) for command in commands_in.readlines()]
            self._commands[0] = 2
        self._export_movie = export_movie
        self._update_data = []
        self._frame = np.zeros((23, 43))
        self._paddle_x = None
        self._ball_x = None
        self._score = 0

    def _analyse_frame_update(self) -> None:
        for index in range(0, len(self._update_data), 3):
            x, y, data = self._update_data[index], self._update_data[index + 1], self._update_data[index + 2]
            if x < 0:
                self._score = data
            else:
                self._frame[y, x] = data
            if data == 3:
                self._paddle_x = x
            elif data == 4:
                self._ball_x = x
        self._update_data = []

    def run(self) -> None:
        self._computer.run(self._commands)
        self._analyse_frame_update()

        if self._export_movie:
            fig, ax = plt.subplots()
            ax.set_axis_off()
            ax.set_title(f'Score: {self._score}', fontsize=15)
            ax.imshow(self._frame)
            for _ in range(120):
                plt.savefig(f'img_out/{str(self._frame_counter).zfill(5)}.png', bbox_inches='tight')
                self._frame_counter += 1
            plt.close()

            os.system(
                'ffmpeg -framerate 60 -pattern_type glob -i "img_out/*.png" -s:v 516x418 -c:v libx264 -crf 17 '
                '-pix_fmt yuv420p breakout_movie.mp4')  # TODO do it with ffmpeg wrapper (if it would just work...)

        print(f'Final score: {self._score}')



