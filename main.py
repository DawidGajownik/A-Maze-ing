from utils.MazeVisualizer import MazeVisualizer
from algotirhms import MazeGenerator
from random import randint

maze_gen = MazeGenerator()

path = "NNNNNEESSEENEESSSSSEESSENESSSSSSSESSSSWSEEEEEN"

enter = [2, 5]
exit = [17, 18]
visualizer = MazeVisualizer(maze_gen, path, enter, exit)
visualizer.draw()
