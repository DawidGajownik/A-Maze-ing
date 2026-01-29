from mlx import Mlx
from .Window import Window
from .Maze import Maze
from typing import Any


class Image():
    def __init__(self, mlx: Mlx, mlx_ptr: Any, win: Window, maze: Maze,
                 width: int | None = None,
                 height: int | None = None
                 ):
        self.height = win.height
        self.width = win.width // 8 * 7
        self.set_scale(maze)
        self.height = height if height else maze.height * self.scale + 2
        self.width = width if width else maze.width * self.scale + 2
        self.height = height if height else win.height
        self.width = width if width else win.width // 8 * 7

        self.ptr = mlx.mlx_new_image(mlx_ptr, self.width, self.height)
        (self.data, self.bits_per_pixel, self.size_line,
            self.theformat) = mlx.mlx_get_data_addr(self.ptr)
        self.thickness = 1
        self.prev_thickness = None
        self.prev_scale = None

    def set_scale(self, maze: Maze) -> None:
        self.scale = min(
            self.width // maze.width,
            self.height // maze.height
        )
