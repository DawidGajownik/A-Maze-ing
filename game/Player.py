from MAZE import MazeManager
from enums import Key, Numpad, Arrow, Direction
from typing import List


class Player:
    def __init__(self, maze: MazeManager) -> None:
        self.current_position = maze.entry
        self.taret_position = maze.exit
        self.maze_map = maze.map
        self.path: List[int] = []

    def move(self, key_pressed: Key) -> List[int]:
        direction: Direction = None

        if key_pressed == Arrow.UP:
            direction = Direction.NORTH
        elif key_pressed == Arrow.RIGHT:
            direction = Direction.EAST
        elif key_pressed == Arrow.DOWN:
            direction = Direction.SOUTH
        elif key_pressed == Arrow.LEFT:
            direction = Direction.WEST

        if direction is not None and self.is_valid_move(direction):
            

    def is_valid_move(self, direction: Direction) -> bool:
        val = self.maze[self.current_position]

        return not (val & (1 << direction.value))

