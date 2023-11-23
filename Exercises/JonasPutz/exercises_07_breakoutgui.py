import numpy as np
from collections import deque

class BreakoutGUI:
    _output_data: deque[int] = deque(maxlen= 3) #accepts 3 outputs from the computer and will then interpret them
    _field = np.zeros((23, 43), dtype=int) #a 2d array for the game data
    _score : int = 0

    _paddle_X : int = 0
    _ball_X : int = 0

    def __init__(self, symbol_air: str, symbol_wall: str, symbol_block: str, symbol_paddle: str, symbol_ball: str) -> None:
        self._symbol_table = {
            0: symbol_air,
            1: symbol_wall,
            2: symbol_block,
            3: symbol_paddle,
            4: symbol_ball,
        }

    def add_output(self, value: int):
        self._output_data.append(value)
        if len(self._output_data) == 3:
            self.evaluate_position(self._output_data.popleft(), self._output_data.popleft(), self._output_data.popleft())

    def evaluate_position(self, x: int, y: int, type: int):
        if type == 3: #update the paddle position
            self._paddle_X = x
        elif type == 4: #update the ball position
            self._ball_X = x

        if x == -1 and y == 0: #update the score
            self._score = type
        else: #update the game data
            self._field[y, x] = type

    def __repr__(self) -> str:
        """ Returns an ASCII representation of the current game"""
        return "".join(
            "".join(self._symbol_table.get(block, block) for block in line) + "\n"
            for line in self._field) + f"Score: {self._score:05}"
    
    def get_ball_relative(self) -> int:
        return self._ball_X - self._paddle_X