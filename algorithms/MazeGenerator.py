from random import Random
from typing import List, Union, Set, Generator, Optional, Tuple
from enums import Direction
from objects import Maze


class MazeGenerator:
    def prepare_data(self, seed: int, width: int, height: int,
                     is_perfect: bool, heart: bool,
                     entry: int, exit: int) -> None:
        self.maze_random = Random()
        self.maze_random.seed(seed)
        self.maze_map: List[Union[bool, int]] = [False] * (width * height)
        self.available_cells: Set[int] = {x for x in range(width * height)}
        self.width = width
        self.height = height
        self.found: Set[int] = set()
        self.seed = seed
        self.is_perfect = is_perfect
        self.visualisation_tempo = 1
        self.heart = heart

        if self.heart:
            self.create_heart()
        if height > 7 and width > 8:
            self.set_42()
        self.is_entry_exit_valid(entry, exit)
        self.set_neighbors()
        self.remove_42_from_available()
        if self.heart:
            self.remove_outline()

    def is_entry_exit_valid(self, entry: int, exit: int) -> None:
        if self.maze_map[entry] == 0xF or self.maze_map[entry] == 1:
            raise ValueError("Invalid entry coordinates.")
        if self.maze_map[exit] == 0xF or self.maze_map[exit] == 1:
            raise ValueError("Invalid exit coordinates.")

    def set_42(self) -> None:
        x = self.width // 2
        y = self.height // 2

        central_cell = y * self.width + x

        self.maze_map[central_cell - 1] = 0xF
        self.maze_map[central_cell - 2] = 0xF
        self.maze_map[central_cell - 3] = 0xF
        self.maze_map[central_cell - 3 - self.width] = 0xF
        self.maze_map[central_cell - 3 - self.width * 2] = 0xF
        self.maze_map[central_cell - 1 + self.width] = 0xF
        self.maze_map[central_cell - 1 + self.width * 2] = 0xF
        self.maze_map[central_cell + 1] = 0xF
        self.maze_map[central_cell + 2] = 0xF
        self.maze_map[central_cell + 3] = 0xF
        self.maze_map[central_cell + 3 - self.width] = 0xF
        self.maze_map[central_cell + 3 - self.width * 2] = 0xF
        self.maze_map[central_cell + 2 - self.width * 2] = 0xF
        self.maze_map[central_cell + 1 - self.width * 2] = 0xF
        self.maze_map[central_cell + 1 + self.width] = 0xF
        self.maze_map[central_cell + 1 + self.width * 2] = 0xF
        self.maze_map[central_cell + 2 + self.width * 2] = 0xF
        self.maze_map[central_cell + 3 + self.width * 2] = 0xF

    def set_neighbors(self) -> None:
        self.neighbors: List[List[int]] = [[] for _ in range(self.width *
                                                             self.height)]

        for y in range(self.height):
            for x in range(self.width):
                c = y * self.width + x
                if (x > 0 and self.maze_map[c - 1] != 0xF
                        and self.maze_map[c - 1] != 1):
                    self.neighbors[c].append(c - 1)
                if (x < self.width - 1 and self.maze_map[c + 1] != 0xF
                        and self.maze_map[c + 1] != 1):
                    self.neighbors[c].append(c + 1)
                if (y > 0 and self.maze_map[c - self.width] != 0xF
                        and self.maze_map[c - self.width] != 1):
                    self.neighbors[c].append(c - self.width)
                if (y < self.height - 1
                    and self.maze_map[c + self.width] != 0xF
                        and self.maze_map[c + self.width] != 1):
                    self.neighbors[c].append(c + self.width)

    def remove_42_from_available(self) -> None:
        for i, cell in enumerate(self.maze_map):
            if cell == 0xF or cell == 1:
                self.available_cells.remove(i)

    def create_maze_instant(self, maze: Maze, seed: int) -> str:
        self.prepare_data(seed, maze.width, maze.height,
                          maze.is_perfect, maze.heart,
                          maze.entry, maze.exit)

        end = self.get_random_cell()
        self.maze_map[end] = 0b1111
        self.found.add(end)
        path_found: bool = False
        path: List[int] = []
        i: int = 0

        while self.available_cells:
            start = self.get_random_cell()
            path.append(start)

            self.maze_map[start] = 16
            current_pos = start

            path_found = False
            while not path_found:
                current_pos = self.move_at_random(current_pos, path)
                if self.maze_map[current_pos] == -1:
                    self.maze_map[current_pos] = 16
                    self.clear_last_path(current_pos, path)
                elif self.maze_map[current_pos] != 16:
                    path_found = True

                maze.map = self.maze_map
                i += 1

            self.save_new_path(path)
            path.clear()

        if not self.is_perfect:
            self.create_loops()

        maze.map = self.maze_map
        return self.get_maze_str()

    def create_maze(self, manager: Maze, seed: int,
                    visualize: Optional[bool] = False) -> Generator[
                        Tuple[set[int], List[int]], None, None]:
        self.prepare_data(seed, manager.width, manager.height,
                          manager.is_perfect, manager.heart)

        end = self.get_random_cell()
        self.maze_map[end] = 0b1111
        self.found.add(end)
        path_found: bool = False
        path: List[int] = []
        i: int = 0

        while self.available_cells:
            start = self.get_random_cell()
            path.append(start)

            self.maze_map[start] = 16
            current_pos = start

            path_found = False
            while not path_found:
                current_pos = self.move_at_random(current_pos, path)
                if self.maze_map[current_pos] == -1:
                    self.maze_map[current_pos] = 16
                    self.clear_last_path(current_pos, path)
                elif self.maze_map[current_pos] != 16:
                    path_found = True
                manager.map = self.maze_map

                i += 1
                if visualize and i % self.visualisation_tempo == 0:
                    yield self.found, path

            self.save_new_path(path)
            path.clear()

        if not self.is_perfect:
            self.create_loops()

        manager.map = self.maze_map
        yield self.found, path

    def create_loops(self) -> None:
        end_blocks: Set[int] = {0b0111, 0b1011, 0b1101, 0b1110}

        for i, cell in enumerate(self.maze_map):
            if cell in end_blocks:
                new_connection = self.maze_random.choice(self.neighbors[i])
                direction = self.create_directions([i, new_connection])[0]
                self.put_walls_in_cell(i, new_connection, direction)

    def get_maze_str(self) -> str:
        lines = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = y * self.width + x
                row.append(f"{self.maze_map[cell]:X}")
            lines.append("".join(row))

        return "\n".join(lines)

    def save_new_path(self, path: List[int]) -> int:
        self.maze_map[path[0]] = 0xF
        directions = self.create_directions(path)

        current = path[0]

        i: int = 0
        for direction in directions:
            previous = current
            i += 1
            current = path[i]
            self.put_walls_in_cell(previous, current, direction)

        for cell in path:
            self.found.add(cell)

        return len(path) + 1

    def create_directions(self, path: List[int]) -> List[Direction]:
        directions: List[Direction] = []

        previous: Optional[int] = None
        for cell in path:
            if previous is None:
                previous = cell
                continue

            if previous + 1 == cell:
                directions.append(Direction.EAST)
            elif previous - 1 == cell:
                directions.append(Direction.WEST)
            elif previous + self.width == cell:
                directions.append(Direction.SOUTH)
            elif previous - self.width == cell:
                directions.append(Direction.NORTH)
            previous = cell

        return directions

    def put_walls_in_cell(self, previous: int,
                          current: int,
                          direction: Direction) -> None:

        previous_cell = self.maze_map[previous]
        previous_cell = previous_cell & ~(1 << direction.value)
        self.maze_map[previous] = previous_cell

        current_cell = (0b1111 if self.maze_map[current] == 16
                        else self.maze_map[current])
        current_cell = current_cell & ~(1 << direction.opposite.value)
        self.maze_map[current] = current_cell

    def clear_last_path(self, current_pos: int,
                        path: List[int]) -> None:
        i = len(path) - 1
        while len(path) != 0 and path[-1] != current_pos:
            cell = path.pop()
            self.maze_map[cell] = False
            self.available_cells.add(cell)
            i -= 1

    def move_at_random(self, current_pos: int,
                       path: List[int]) -> int:
        current_pos = self.maze_random.choice(self.neighbors[current_pos])

        if not self.maze_map[current_pos]:
            path.append(current_pos)
            self.maze_map[current_pos] = 16
            self.available_cells.remove(current_pos)

        elif self.maze_map[current_pos] == 16:
            self.maze_map[current_pos] = -1

        else:
            path.append(current_pos)

        return (current_pos)

    def get_random_cell(self) -> int:
        cell = self.maze_random.choice(list(self.available_cells))
        self.available_cells.remove(cell)
        return (cell)

    def create_heart(self) -> None:
        heart_map = []

        for y in range(self.height):
            py = (self.height / 2 - y) / (self.height / 2.5)

            for x in range(self.width):
                px = (x - self.width / 2) / (self.width / 2.5)
                y_adj = py + 0.2

                equation = (px**2 + y_adj**2 - 1)**3 - (px**2 * y_adj**3)

                if equation <= 0:
                    heart_map.append(0)  # Inside the heart
                else:
                    heart_map.append(1)  # Background

        self.maze_map = heart_map

    def remove_outline(self) -> None:
        for i, cell in enumerate(self.maze_map):
            if cell == 1:
                self.maze_map[i] = 0
