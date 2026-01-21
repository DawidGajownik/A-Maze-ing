from random import Random, randint
from typing import List, Union, Set
from enum import Enum
from objects.Maze import Maze


class Direction(int, Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
    def opposite(self):
        mapping = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST
        }
        return mapping[self]


class MazeGenerator:
    def prepare_data(self, seed: int, width: int, height: int) -> None:
        self.maze_random = Random()
        self.maze_random.seed(seed)
        self.maze: List[Union[bool, int]] = [False] * (width * height)
        self.available_cells: Set[int] = {x for x in range(width * height)}
        self.width = width
        self.height = height
        self.neighbors: List[List[int]] = [[] for _ in range(width *
                                                             height)]

        for y in range(self.height):
            for x in range(self.width):
                c = y * self.width + x
                if x > 0:
                    self.neighbors[c].append(c - 1)
                if x < self.width - 1:
                    self.neighbors[c].append(c + 1)
                if y > 0:
                    self.neighbors[c].append(c - self.width)
                if y < self.height - 1:
                    self.neighbors[c].append(c + self.width)

    def create_maze(self, width: int, height: int,
                    seed: int = randint(0, 1000000)):
        self.prepare_data(seed, width, height)

        end = self.get_random_cell()
        self.maze[end] = 0xF
        path_found: bool = False
        path: List[int] = []

        while len(self.available_cells) > 0:
            # and i < 15:
            start = self.get_random_cell()
            path.append(start)

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

            self.save_new_path(path)
            path.clear()

        return Maze(self.maze, self.width, self.height)

    def print_maze(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = y * self.width + x
                print(f"{self.maze[cell]:X}", end="")
            print()

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
        previous_cell = previous_cell & ~(1 << direction)
        self.maze[previous] = previous_cell

        current_cell = (0b1111 if self.maze[current] == 16
                        else self.maze[current])
        current_cell = current_cell & ~(1 << direction.opposite)
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


def main() -> None:
    maze_gen = MazeGenerator()

    i = 0
    maze_gen.create_maze(seed=1000, width=50, height=50)
    maze_gen.print_maze()
    print(i)

    #  maze_gen.create_maze()
    #  for col in maze_gen.maze:
    #      for cell in col:
    #          print(cell, end="")
    #      print()
    #  print()


if __name__ == "__main__":
    main()
