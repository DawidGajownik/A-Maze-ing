from objects import Maze
from enums import Arrow, Direction
from typing import List


class Player:
    def __init__(self, maze: Maze) -> None:
        self.current_position = maze.entry
        self.taret_position = maze.exit
        self.maze_map = maze.map
        self.path: List[int] = [maze.entry]

    def move(self, key_pressed: Arrow) -> List[int]:
        direction = self._get_direction(key_pressed)

        if direction is not None and self._is_valid_move(direction):
            self.path.append(self._get_next_cell(direction))

        return self.path

    @staticmethod
    def _get_direction(key_pressed: Arrow):
        direction: Direction = None

        if key_pressed == Arrow.UP:
            direction = Direction.NORTH
        elif key_pressed == Arrow.RIGHT:
            direction = Direction.EAST
        elif key_pressed == Arrow.DOWN:
            direction = Direction.SOUTH
        elif key_pressed == Arrow.LEFT:
            direction = Direction.WEST

        return direction

    def _is_valid_move(self, direction: Direction) -> bool:
        val = self.maze[self.current_position]

        return not (val & (1 << direction.value))

    def _get_next_cell(self, direction: Direction) -> int:
        if direction == Direction.NORTH:
            return self.current_position - self.width
        if direction == Direction.SOUTH:
            return self.current_position + self.width
        if direction == Direction.EAST:
            return self.current_position + 1
        if direction == Direction.WEST:
            return self.current_position - 1
