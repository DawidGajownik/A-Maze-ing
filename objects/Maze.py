from typing import List, Tuple, Union, Optional


class Maze:
    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int], exit: Tuple[int, int],
                 is_perfect: bool, heart: Optional[bool] = False) -> None:
        self.height = height
        self.width = width
        self.entry = entry[1] * width + entry[0]
        self.exit = exit[1] * width + exit[0]
        self.is_perfect = is_perfect
        self.heart = heart
        self.map: List[Union[int, bool]] = []

    def set_height(self, new_height: int) -> None:
        if new_height != self.height:
            self.height = new_height
            self.entry = 0
            self.exit = (self.height - 1) * self.width + self.width - 1

    def set_width(self, new_width: int) -> None:
        if new_width != self.width:
            self.width = new_width
            self.entry = 0
            self.exit = (self.height - 1) * self.width + self.width - 1
