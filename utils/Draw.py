from objects import Image, Maze, Window
from mlx import Mlx
from enums import Axle, Sign, Direction
from time import sleep


class Draw():

    def _set_pixel(cls, img: Image, x: int, y: int, color: int):
        offset = y * img.size_line + x * (img.bits_per_pixel // 8)
        img.data[offset:offset+4] = bytes((
            color & 0xFF,           # Blue
            (color >> 8) & 0xFF,    # Green
            (color >> 16) & 0xFF,   # Red
            (color >> 24) & 0xFF    # Alpha
        ))

    def get_pixel(img: Image, x, y):
        offset = y * img.size_line + x * img.bits_per_pixel // 8
        blue = img.data[offset + 0]
        green = img.data[offset + 1]
        red = img.data[offset + 2]
        transparency = img.data[offset + 3]
        return (transparency << 24) | (red << 16) | (green << 8) | blue

    def _put_block(cls, i: int, j: int, img: Image, color: int) -> None:
        for x in range(img.thickness + 2, img.scale - img.thickness - 2):
            for y in range(img.thickness + 2, img.scale - img.thickness - 2):
                cls._set_pixel(
                    img, i * img.scale + x + img.thickness,
                    j * img.scale + y + img.thickness, color)

    def _put_up(cls, m: Mlx, mlx: any, win: Window, color: int, i: int, j: int, img: Image, wall_range: tuple, out: bool) -> None:
        thickness = img.prev_thickness if out else img.thickness
        scale = img.prev_scale if out else img.scale
        for p in range((- thickness if j == 0 else 0), thickness):
            for pixel in range(*wall_range):
                #m.mlx_pixel_put(mlx, win, i*img.scale + pixel + img.thickness,
                #    j * img.scale + p + img.thickness, color)
                cls._set_pixel(
                    img, i*img.scale + pixel + img.thickness,
                    j * img.scale + p + img.thickness, 0xFFFFFFFF)

    def _put_down(cls, m: Mlx, mlx: any, win: Window, color: int,
            i: int, j: int, img: Image, maze: Maze, w_range: tuple, out: bool
            ) -> None:
        thickness = img.prev_thickness if out else img.thickness
        scale = img.prev_scale if out else img.scale
        for p in range(
                (-thickness if j == maze.height - 1 else 0),
                thickness):
            for pixel in range(*w_range):
                #m.mlx_pixel_put(mlx, win, i*img.scale + pixel + img.thickness,
                #    (j + 1) * img.scale - p + img.thickness, color)
                cls._set_pixel(
                    img, i*img.scale + pixel + img.thickness,
                    (j + 1) * img.scale - p + img.thickness, 0xFFFFFFFF)

    def _put_left(cls, m: Mlx, mlx: any, win: Window, color: int, i: int, j: int, img: Image, w_range: tuple, out: bool) -> None:
        thickness = img.prev_thickness if out else img.thickness
        scale = img.prev_scale if out else img.scale
        for p in range((-thickness if i == 0 else 0), thickness):
            for pixel in range(*w_range):
                #m.mlx_pixel_put(mlx, win, i*img.scale + img.thickness + p,
                #    j * img.scale + pixel + img.thickness, color)
                cls._set_pixel(
                    img, i*img.scale + img.thickness + p,
                    j * img.scale + pixel + img.thickness, 0xFFFFFFFF)

    def _put_right(cls, m: Mlx, mlx: any, win: Window, color: int,
            i: int, j: int, img: Image, maze: Maze, w_range: tuple, out: bool
            ) -> None:
        thickness = img.prev_thickness if out else img.thickness
        scale = img.prev_scale if out else img.scale
        for p in range(
            (-thickness if i == maze.width - 1 else 0), thickness
                ):
            for pixel in range(*w_range):
                #m.mlx_pixel_put(mlx, win, (i + 1)*img.scale - p + img.thickness,
                #    j * img.scale + pixel + img.thickness, color)
                cls._set_pixel(
                    img, (i + 1)*img.scale - p + img.thickness,
                    j * img.scale + pixel + img.thickness, 0xFFFFFFFF)

    @classmethod
    def _offset(
        cls, img: Image, maze: Maze, axle: Axle, sing: Sign, idx: int
            ):
        if (axle == Axle.X and sing == Sign.POSITIVE):
            if (
                (idx > 0 and maze.path[idx][1] > maze.path[idx - 1][1])
                    or (idx < len(maze.path) - 1
                        and maze.path[idx][1] > maze.path[idx + 1][1])):
                return img.thickness
        if (axle == Axle.X and sing == Sign.NEGATIVE):
            if (
                (idx > 0 and maze.path[idx][1] < maze.path[idx - 1][1])
                    or (idx < len(maze.path) - 1
                        and maze.path[idx][1] < maze.path[idx + 1][1])):
                return img.thickness
        if (axle == Axle.Y and sing == Sign.POSITIVE):
            if (
                (idx > 0 and maze.path[idx][0] > maze.path[idx - 1][0])
                    or (idx < len(maze.path) - 1
                        and maze.path[idx][0] > maze.path[idx + 1][0])):
                return img.thickness
        if (axle == Axle.Y and sing == Sign.NEGATIVE):
            if (
                (idx > 0 and maze.path[idx][0] < maze.path[idx - 1][0])
                    or (idx < len(maze.path) - 1
                        and maze.path[idx][0] < maze.path[idx + 1][0])):
                return img.thickness
        return 0

    def _put_road_block(
            cls, i: int, j: int, img: Image, maze: Maze, idx: int
            ) -> None:
        x_m = cls._offset(img, maze, Axle.X, Sign.NEGATIVE, idx)
        x_p = cls._offset(img, maze, Axle.X, Sign.POSITIVE, idx)
        y_m = cls._offset(img, maze, Axle.Y, Sign.NEGATIVE, idx)
        y_p = cls._offset(img, maze, Axle.Y, Sign.POSITIVE, idx)

        for x in range(
                img.thickness - y_p, img.scale - img.thickness + 1 + y_m):
            for y in range(
                img.thickness - 1 - x_p, img.scale - img.thickness + 1 + x_m
                    ):
                cls._set_pixel(
                    img, i * img.scale + x + img.thickness,
                    j * img.scale + y + img.thickness, 0xFFaaaaaa)
                
    def draw_out(
            cls, x: int, y: int, m: Mlx, mlx: any, maze: Maze, img: Image, win: Window
            ) -> None:
        if img.prev_thickness is not None:
            wall_range = (-img.prev_thickness+1, img.prev_scale + img.prev_thickness)
        else:
            wall_range = 0
        p_left = p_down = p_right = p_up = False
        if (maze.prev_lines is not None):
            p_left, p_down, p_right, p_up = map(
                lambda x: x == '1',
                f"{int(maze.prev_lines[y][x], 16):04b}")
        if p_up:
            cls._put_up(m, mlx, win.ptr, 0xFF000000, x, y, img, wall_range, True)
        if p_down:
            cls._put_down(m, mlx, win.ptr, 0xFF000000, x, y, img, maze, wall_range, True)
        if p_left:
            cls._put_left(m, mlx, win.ptr, 0xFF000000, x, y, img, wall_range, True)
        if p_right:
            cls._put_right(m, mlx, win.ptr, 0xFF000000, x, y, img, maze, wall_range, True)

    def draw_maze(
            cls, a: int, s: int, m: Mlx, mlx: any, maze, img: Image, win: Window
            ) -> None:
        img.data[:] = bytes([0, 0, 0, 255]) * (len(img.data)//4)
        #m.mlx_destroy_image(mlx, img.ptr)
        #img.ptr = mlx.mlx_new_image(mlx, img.width, img.height)
        wall_range = (-img.thickness+1, img.scale + img.thickness)
        for y in range(maze.height):
            for x in range(maze.width):
        #print('draw', x, y, left, down, right, up)
        #if [x, y] in maze.way:
        #    cls._put_block(x, y, img, 0xFFFFFF00)
        #if [x, y] in maze.path:
        #    idx = maze.path.index([x, y])
        #    cls._put_road_block(x, y, img, maze, idx)
        #if x == maze.pacman.x and y == maze.pacman.y:
        #    if [x, y] in maze.way:
        #        maze.remove()
        #    else:
        #        maze.add([x, y])
        #    cls._put_block(x, y, img, 0xFF00FFFF)
        #if x == maze.enter.x and y == maze.enter.y:
        #    cls._put_block(x, y, img, 0xFF00FF00)
        #if x == maze.exit.x and y == maze.exit.y:
        #    cls._put_block(x, y, img, 0xFF0000FF)
        #if up and down and right and left:
        #    cls._put_block(x, y, img, 0xFFFF0000)
                if len(maze.map) > 0:
                    if maze.map[y * maze.width + x] == 16:
                        cls._put_block(x, y, img, 0xFFFF0000)
                    if (maze.map[y * maze.width + x] & (1 << Direction.NORTH.value)):
                        cls._put_up(m, mlx, win.ptr, 0xFFFFFFFF, x, y, img, wall_range, False)
                    if (maze.map[y * maze.width + x] & (1 << Direction.SOUTH.value)):
                        cls._put_down(m, mlx, win.ptr, 0xFFFFFFFF, x, y, img, maze, wall_range, False)
                    if (maze.map[y * maze.width + x] & (1 << Direction.WEST.value)):
                        cls._put_left(m, mlx, win.ptr, 0xFFFFFFFF, x, y, img, wall_range, False)
                    if (maze.map[y * maze.width + x] & (1 << Direction.EAST.value)):
                        cls._put_right(m, mlx, win.ptr, 0xFFFFFFFF, x, y, img, maze, wall_range, False)
        m.mlx_put_image_to_window(mlx, win.ptr, img.ptr, 0, 0)
        m.mlx_pixel_put(mlx, win.ptr, 0, 0, 0xff000000)

            
