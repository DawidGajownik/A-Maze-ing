from .Point import Point
from typing import List, Union


class Maze():

    def __init__(
            self, map: List[Union[bool, int]],
            width: int, height: int,
        enter: Point, exit: Point
            ):
        self.map: List[Union[bool, int]] = map
        #self.way = []
        #self.last = None
        self.width = width
        self.height = height
        #self.enter = Point(enter[0], enter[1])
        #self.path_txt = path_txt
        #self.path = [enter]
        #for c in self.path_txt:
        #    if c == "N":
        #        self.path.append([self.path[-1][0], self.path[-1][1]-1])
        #    if c == "S":
        #        self.path.append([self.path[-1][0], self.path[-1][1]+1])
        #    if c == "W":
        #        self.path.append([self.path[-1][0]-1, self.path[-1][1]])
        #    if c == "E":
        #        self.path.append([self.path[-1][0]+1, self.path[-1][1]])
        #self.pacman = Point(enter[0], enter[1])
        self.exit = exit.y * width + exit.x
        self.enter = enter.y * width + enter.x
#
    #def add(self, point):
    #    self.way.append(self.last)
    #    self.last = point
#
    #def remove(self):
    #    self.last = self.way.pop()
#