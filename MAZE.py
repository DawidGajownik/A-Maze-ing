#from algorithms.MazeGenerator import MazeGenerator
#from algorithms.PathFinder import PathFinder
from typing import List, Tuple, Union
from random import randint


class MazeManager:
    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int], exit: Tuple[int, int],
                 is_perfect: bool):
        #self.generator = MazeGenerator()
        #self.finder = PathFinder()
        self.height = height
        self.width = width
        self.entry = entry[1] * width + entry[0]
        self.exit = exit[1] * width + exit[0]
        self.is_perfect = is_perfect
        self.map: List[Union[int, bool]] = []

#to tez wyjebalem po prostu i dziala xd
    #def generate(self, seed: int = None):
    #    if seed is None:
    #        seed = randint(0, 10000000)
    #    self.generator.create_maze(self, seed)
    #    self.str_map = self.generator.get_maze_str()

#wyjebalem i wstawilem to w mainie
    #def draw(self, seed):
        #self.visualizer = MazeVisualizer(self, (1, 1), (14, 14))
        #self.visualizer.open_window(self.generator, seed)

    #def find(self):
        #self.path = self.finder.find_path(self)
