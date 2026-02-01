from objects import Maze
from enums import Arrow, Direction, Key
from typing import List, Union


class Player:
    def __init__(self, maze: Maze) -> None:
        self.current_position = maze.entry
        self.taret_position = maze.exit
        self.maze_map = maze.map
        self.width = maze.width
        self.path: List[int] = [maze.entry]

    def move(self, key_pressed: Arrow | Key) -> List[int]:
        direction = self._get_direction(key_pressed)

        if direction is not None and self._is_valid_move(direction):
            self._get_next_cell(direction)
            if self.current_position in self.path:
                self._remove_loop()
            else:
                self.path.append(self.current_position)

        elif key_pressed == Key.K_BACKSPACE and len(self.path) > 1:
            self.path.pop()

        return self.path

    @staticmethod
    def _get_direction(key_pressed: Arrow) -> Direction:
        direction: Union[Direction, None] = None

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
        val = self.maze_map[self.current_position]

        return not (val & (1 << direction.value))

    def _get_next_cell(self, direction: Direction) -> None:
        if direction == Direction.NORTH:
            self.current_position -= self.width
        if direction == Direction.SOUTH:
            self.current_position += self.width
        if direction == Direction.EAST:
            self.current_position += 1
        if direction == Direction.WEST:
            self.current_position -= 1

    def _remove_loop(self) -> None:
        while len(self.path) != 0 and self.path[-1] != self.current_position:
            self.path.pop()
