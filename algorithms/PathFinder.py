from typing import Dict, List, Deque, Set, Generator, Union
from enums import Direction
from collections import deque


class PathFinder:
    def prepare_data(self, manager) -> None:
        self.entry: int = manager.entry
        self.exit: int = manager.exit
        self.height: int = manager.height
        self.width: int = manager.width
        self.maze: int = manager.map

    def find_path_instant(self, manager) -> str:
        self.prepare_data(manager)

        maze_connections: Dict[int, int] = {}
        queue: Deque[int] = deque([self.entry])
        current: int = self.entry
        visited: Set[int] = {self.entry}

        while queue:
            current = queue.popleft()

            if current == self.exit:
                break

            for neighbor in self.find_neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    maze_connections[neighbor] = current

        path: List[int] = []

        while current != self.entry:
            path.append(current)
            current = maze_connections[current]

        path.append(self.entry)
        path.reverse()

        return self.get_str_path(path)

    def find_path(self, manager) -> Generator[Union[int, List[int]],
                                              None, None]:
        self.prepare_data(manager)

        maze_connections: Dict[int, int] = {}
        queue: Deque[int] = deque([self.entry])
        current: int = self.entry
        visited: Set[int] = {self.entry}

        while queue:
            current = queue.popleft()
            yield current

            if current == self.exit:
                break

            for neighbor in self.find_neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    maze_connections[neighbor] = current

        path: List[int] = []

        while current != self.entry:
            path.append(current)
            current = maze_connections[current]

        path.append(self.entry)
        path.reverse()
        yield path

        return self.get_str_path(path)

    def find_neighbors(self, current: int) -> Generator[int,
                                                        None,
                                                        None]:
        val = self.maze[current]

        if not (val & (1 << Direction.NORTH.value)):
            yield current - self.width
        if not (val & (1 << Direction.SOUTH.value)):
            yield current + self.width
        if not (val & (1 << Direction.EAST.value)):
            yield current + 1
        if not (val & (1 << Direction.WEST.value)):
            yield current - 1

    def get_str_path(self, path: List[int]) -> str:
        directions: List[str] = []

        previous: int = None
        for cell in path:
            if previous is None:
                previous = cell
                continue

            if previous + 1 == cell:
                directions.append("E")
            elif previous - 1 == cell:
                directions.append("W")
            elif previous + self.width == cell:
                directions.append("S")
            elif previous - self.width == cell:
                directions.append("N")
            previous = cell

        return "".join(directions)
