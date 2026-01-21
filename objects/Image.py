from mlx import Mlx
from .Window import Window
from .Maze import Maze


class Image():
    def __init__(self, mlx: Mlx, mlx_ptr: any, win: Window, maze: Maze):
        self.height = win.height
        self.width = win.width
        self.set_scale(maze)
        self.height = maze.height * self.scale + 16
        self.width = maze.width * self.scale + 16
        self.ptr = mlx.mlx_new_image(mlx_ptr, self.width, self.height)
        (self.data, self.bits_per_pixel, self.size_line,
            self.theformat) = mlx.mlx_get_data_addr(self.ptr)
        self.thickness = 1
        self.prev_thickness = None
        self.prev_scale = None

    def set_scale(self, maze: Maze):
        self.scale = min(
            self.width // maze.width,
            self.height // maze.height
        ) - 1
