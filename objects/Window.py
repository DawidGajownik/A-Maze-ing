from mlx import Mlx
from typing import Any, Tuple


class Window:

    def __init__(self, mlx: Mlx, mlx_ptr: Any, desc: str):
        screen_size: Tuple[Any, int, int] = mlx.mlx_get_screen_size(mlx_ptr)
        *_, self.width, self.height = screen_size
        self.height -= 100
        self.width -= 100
        self.desc = desc
        self.ptr = mlx.mlx_new_window(
            mlx_ptr, self.width, self.height, self.desc)
