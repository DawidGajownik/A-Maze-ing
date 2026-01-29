from typing import List, Tuple, Union


class Maze:
    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int], exit: Tuple[int, int],
                 is_perfect: bool):
        self.height = height
        self.width = width
        self.entry = entry[1] * width + entry[0]
        self.exit = exit[1] * width + exit[0]
        self.is_perfect = is_perfect
        self.map: List[Union[int, bool]] = []
