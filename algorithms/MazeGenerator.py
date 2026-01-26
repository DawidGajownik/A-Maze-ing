from random import Random
from typing import List, Union, Set
from enums import Direction
import math


class MazeGenerator:
    def prepare_data(self, seed: int, width: int, height: int) -> None:
        self.maze_random = Random()
        self.maze_random.seed(seed)
        self.maze: List[Union[bool, int]] = [False] * (width * height)
        self.available_cells: Set[int] = {x for x in range(width * height)}
        self.width = width
        self.height = height
        self.found: Set[int] = set()
        self.seed = seed
        self.is_perfect = True

        self.set_42()
        self.set_neighbors()
        self.remove_42_from_available()

    def set_42(self):
        pass
        x = self.width // 2
        y = self.height // 2

        central_cell = y * self.width + x

        self.maze[central_cell - 1] = 0xF
        self.maze[central_cell - 2] = 0xF
        self.maze[central_cell - 3] = 0xF
        self.maze[central_cell - 3 - self.width] = 0xF
        self.maze[central_cell - 3 - self.width * 2] = 0xF
        self.maze[central_cell - 1 + self.width] = 0xF
        self.maze[central_cell - 1 + self.width * 2] = 0xF
        self.maze[central_cell + 1] = 0xF
        self.maze[central_cell + 2] = 0xF
        self.maze[central_cell + 3] = 0xF
        self.maze[central_cell + 3 - self.width] = 0xF
        self.maze[central_cell + 3 - self.width * 2] = 0xF
        self.maze[central_cell + 2 - self.width * 2] = 0xF
        self.maze[central_cell + 1 - self.width * 2] = 0xF
        self.maze[central_cell + 1 + self.width] = 0xF
        self.maze[central_cell + 1 + self.width * 2] = 0xF
        self.maze[central_cell + 2 + self.width * 2] = 0xF
        self.maze[central_cell + 3 + self.width * 2] = 0xF

    def set_neighbors(self):
        self.neighbors: List[List[int]] = [[] for _ in range(self.width *
                                                             self.height)]

        for y in range(self.height):
            for x in range(self.width):
                c = y * self.width + x
                if x > 0 and self.maze[c - 1] != 0xF:
                    self.neighbors[c].append(c - 1)
                if x < self.width - 1 and self.maze[c + 1] != 0xF:
                    self.neighbors[c].append(c + 1)
                if y > 0 and self.maze[c - self.width] != 0xF:
                    self.neighbors[c].append(c - self.width)
                if y < self.height - 1 and self.maze[c + self.width] != 0xF:
                    self.neighbors[c].append(c + self.width)

    def remove_42_from_available(self):
        for i, cell in enumerate(self.maze):
            if cell == 0xF:
                self.available_cells.remove(i)

    def create_maze(self, manager, seed: int, visualize: bool = False):
        self.prepare_data(seed, manager.width, manager.height)

        end = self.get_random_cell()
        self.maze[end] = 0b1111
        self.found.add(end)
        path_found: bool = False
        path: List[int] = []
        # visualisation_tempo: int = max(1, (self.width * self.height) // 100)
        i: int = 0

        while self.available_cells:
            start = self.get_random_cell()
            path.append(start)

            num_cells = max(1, len(self.available_cells))
            visualisation_tempo: int = max(
                3, int((num_cells * math.log10(num_cells)) / 2000))
            # visualisation_tempo = 100
            self.maze[start] = 16
            current_pos = start

            path_found = False
            while not path_found:
                current_pos = self.move_at_random(current_pos, path)
                if self.maze[current_pos] == -1:
                    self.maze[current_pos] = 16
                    self.clear_last_path(current_pos, path)
                elif self.maze[current_pos] != 16:
                    path_found = True
                manager.map = self.maze

                i += 1
                if visualize and i % visualisation_tempo == 0:
                    yield self.found

            self.save_new_path(path)
            path.clear()

        if not self.is_perfect:
            self.create_loops()

        manager.map = self.maze
        yield self.found

    def create_loops(self):
        end_blocks: Set[int] = {0b0111, 0b1011, 0b1101, 0b1110}

        for i, cell in enumerate(self.maze):
            if cell in end_blocks:
                new_connection = self.maze_random.choice(self.neighbors[i])
                direction = self.create_directions([i, new_connection])[0]
                self.put_walls_in_cell(i, new_connection, direction)

    def get_maze_str(self):
        lines = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = y * self.width + x
                # Convert the value to Hex string
                row.append(f"{self.maze[cell]:X}")
            # Join the row characters, then add to lines
            lines.append("".join(row))

        # Join all lines with a newline character
        return "\n".join(lines)

    def save_new_path(self, path: List[int]) -> int:
        self.maze[path[0]] = 0xF
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

        previous: int = None
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

        previous_cell = self.maze[previous]
        previous_cell = previous_cell & ~(1 << direction.value)
        self.maze[previous] = previous_cell

        current_cell = (0b1111 if self.maze[current] == 16
                        else self.maze[current])
        current_cell = current_cell & ~(1 << direction.opposite.value)
        self.maze[current] = current_cell

    def clear_last_path(self, current_pos: int,
                        path: List[int]) -> None:
        i = len(path) - 1
        while len(path) != 0 and path[-1] != current_pos:
            cell = path.pop()
            self.maze[cell] = False
            self.available_cells.add(cell)
            i -= 1

    def move_at_random(self, current_pos: int,
                       path: List[int]) -> int:
        current_pos = self.maze_random.choice(self.neighbors[current_pos])

        if not self.maze[current_pos]:
            path.append(current_pos)
            self.maze[current_pos] = 16
            self.available_cells.remove(current_pos)

        elif self.maze[current_pos] == 16:
            self.maze[current_pos] = -1

        else:
            path.append(current_pos)

        return (current_pos)

    def get_random_cell(self) -> int:
        cell = self.maze_random.choice(list(self.available_cells))
        self.available_cells.remove(cell)
        return (cell)
