from algorithms.MazeGenerator import MazeGenerator
from algorithms.PathFinder import PathFinder
from utils.MazeVisualizer import MazeVisualizer
from typing import List, Tuple
from random import randint


class MazeManager:
    def __init__(self, width: int, height: int,
                 entry: Tuple[int], exit: Tuple[int]):
        self.generator = MazeGenerator()
        self.finder = PathFinder()
        self.visualizer: MazeVisualizer
        self.height = height
        self.width = width
        self.entry = entry[1] * width + entry[0]
        self.exit = exit[1] * width + exit[0]
        self.map: List[int, bool] = []
        self.str_map = []
        self.path: str = ""

    def generate(self, seed: int = None):
        if seed is None:
            seed = randint(0, 10000000)
        self.generator.create_maze(self, seed)
        self.str_map = self.generator.get_maze_str()

    def draw(self):
        self.visualizer = MazeVisualizer(self, (1, 1), (49, 49))
        self.visualizer.draw()

    def find(self):
        self.path = self.finder.find_path(self)
