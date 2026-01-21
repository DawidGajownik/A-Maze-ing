from mlx import Mlx


class Window():

    def __init__(self, mlx: Mlx, mlx_ptr: any, desc: str):
        self.val, self.width, self.height = mlx.mlx_get_screen_size(mlx_ptr)
        self.height -= 100
        self.width -= 100
        self.desc = desc
        self.ptr = mlx.mlx_new_window(
            mlx_ptr, self.width, self.height, self.desc)
