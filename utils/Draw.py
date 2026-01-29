from typing import Any, Union
from random import randint
from mlx import Mlx
from objects import Image, Window, Brick
from enums import Direction
from MAZE import MazeManager


def _put_block(
        i: int, j: int, img: Image,
        color: bytes, thickness: int) -> None:

    start_x = i * img.scale + thickness
    start_y = j * img.scale + thickness
    size = img.scale - thickness

    row = color * size

    for y in range(start_y, start_y + size):
        offset = (y * img.width + start_x) * 4
        img.data[offset: offset + size * 4] = row


def _put_brick(
        i: int, j: int, img: Image, thickness: int,
        brick: Brick) -> None:
    start_x = i * img.scale + thickness
    start_y = j * img.scale + thickness
    size = img.scale



    for y in range(start_y, start_y + size):
        idx = y%(brick.lines_amount-1)
        idx = randint(0, brick.lines_amount - 1)
        brick_even = brick.rows_even[idx]
        brick_odd = brick.rows_odd[idx]
        offset = (y * img.width + start_x) * 4
        img.data[offset: offset + size * 4] = brick.mortar if y % brick.brick_h < brick.mortar_thickness_y else brick_even if (y // brick.brick_h)%2 == 0 else brick_odd


def _put_up(color: bytes, i: int, j: int, img: Image, wall_range: tuple,
            thickness: int) -> None:

    start_y = j * img.scale + thickness
    start_x = i * img.scale + thickness - 1

    y_start = start_y + (-thickness if j == 0 else 0)
    y_end = start_y + thickness

    x0 = start_x + wall_range[0]
    x1 = start_x + wall_range[1]

    x0 = max(0, x0)
    x1 = min(img.width, x1)

    if x0 >= x1:
        return

    pixels = x1 - x0
    line = color * pixels
    line_len = pixels * 4

    for y in range(y_start, y_end):
        if 0 <= y < img.height:
            offset = (y * img.width + x0) * 4
            img.data[offset:offset + line_len] = line


def _put_down(color: bytes,
              i: int, j: int, img: Image, maze: MazeManager, w_range: tuple,
              thickness: int
              ) -> None:

    start_x = i * img.scale + thickness - 1

    y_start = (
            (j + 1) * img.scale
            - thickness
            + (thickness if j == maze.height - 1 else 0)
            + thickness
    )
    y_end = (j + 1) * img.scale + thickness

    x0 = start_x + w_range[0]
    x1 = start_x + w_range[1]

    x0 = max(0, x0)
    x1 = min(img.width, x1)

    if x0 >= x1:
        return

    pixels = x1 - x0
    line = color * pixels
    line_len = pixels * 4

    for y in range(y_start, y_end):
        if 0 <= y < img.height:
            offset = (y * img.width + x0) * 4
            img.data[offset:offset + line_len] = line


def _put_left(color: bytes, i: int, j: int, img: Image, w_range: tuple,
              thickness: int) -> None:
    start_y = j * img.scale + thickness - 1
    x_base = i * img.scale + thickness

    data = img.data
    width = img.width
    height = img.height

    y0 = start_y + w_range[0]
    y1 = start_y + w_range[1]

    pixels = thickness
    line = color * pixels

    y0 = max(0, y0)
    y1 = min(height, y1)

    if y0 >= y1:
        return

    for y in range (y0,y1):
        offset = (y * width + x_base) * 4
        data[offset:offset + pixels*4] = line


def _put_right(color: bytes,
               i: int, j: int, img: Image, w_range: tuple,
               thickness: int
               ) -> None:
    start_y = j * img.scale + thickness - 1
    x_base = (i+1) * img.scale

    data = img.data
    width = img.width
    height = img.height

    y0 = start_y + w_range[0]
    y1 = start_y + w_range[1]

    pixels = thickness
    line = color * pixels
    y0 = max(0, y0)
    y1 = min(height, y1)

    if y0 >= y1:
        return
    for y in range (y0,y1):
        offset = (y * width + x_base) * 4
        data[offset:offset + pixels*4] = line


def _put_road_block(
        i: int, j: int, img: Image, color: bytes, thickness: int, path: list, idx: int, width: int
        ) -> None:

    x_m = thickness if idx == 0 or path[idx - 1] - path[idx] != -1 else 0
    x_p = thickness if path[idx - 1] - path[idx] == 1 else 0
    y_m = thickness if path[idx - 1] - path[idx] != -width else 0
    y_p = thickness if path[idx - 1] - path[idx] == width else 0

    start_x = i * img.scale + img.thickness + x_m*2 - 2
    start_y = j * img.scale + img.thickness + y_m*2 - 2
    size_x = img.scale - img.thickness - x_m * 2 + 1 + x_p*2 + 1
    size_y = img.scale - img.thickness - y_m * 2 + 1 + y_p*2 + 1

    row = color * size_x

    for y in range(start_y, start_y + size_y):
        offset = (y * img.width + start_x) * 4
        img.data[offset: offset + size_x * 4] = row


class Draw():

    def draw_path(
            cls, m: Mlx, mlx: Any, maze: MazeManager, img: Image, path_img: Image, final_path_img:Image, win: Window, path_list: Union[int, list[int]], colors: dict, offset: int
    ) -> None:
        if isinstance(path_list, int):
            x = path_list % maze.width
            y = path_list // maze.width
            _put_block(x, y, path_img, colors['Snake'][:3] + bytes([30]), 0)
            m.mlx_put_image_to_window(mlx, win.ptr, path_img.ptr, 0, offset)
            m.mlx_pixel_put(mlx, win.ptr, 0, 0, 0xFF000000)


        else:

            for idx, path in enumerate(path_list):
                m.mlx_put_image_to_window(mlx, win.ptr, img.ptr, 0, offset)
                x = path % maze.width
                y = path // maze.width
                _put_road_block(x, y, final_path_img, colors['Snake'][:3] + bytes([255]), img.thickness, path_list, idx, maze.width)
                m.mlx_put_image_to_window(mlx, win.ptr, final_path_img.ptr, 0, offset)
                m.mlx_pixel_put(mlx, win.ptr, 0, 0, 0xFF000000)



    def draw_maze(
            cls, m: Mlx, mlx: Any, maze: MazeManager, img: Image, win: Window, found: set[int], colors: dict,
            brick_visible: bool,
            brick: Brick, offset: int
            ) -> None:
        
        img.data[:] = colors['Grid 2'] * (len(img.data)//4)
        wall_range = (-img.thickness+1, img.scale + img.thickness)
        for y in range(maze.height):
            for x in range(maze.width):
                if len(maze.map) > 0:
                    if (y * maze.width + x) in found:
                        if brick_visible:
                            _put_brick(x, y, img, 0, brick)
                        else:
                            _put_block(x, y, img, colors['Block found'], img.thickness)
                    if maze.map[y * maze.width + x] == 15:
                        _put_block(x, y, img, colors['42'], img.thickness)
                        _put_down(colors['Grid 1'], x, y-1, img, maze, wall_range, img.thickness)
                        _put_up(colors['Grid 1'], x, y+1, img, wall_range, img.thickness)
                        _put_left(colors['Grid 1'], x+1, y, img, wall_range, img.thickness)
                    if maze.map[y * maze.width + x] == 16:
                        _put_block(x, y, img, colors['Snake'], 0)
                        if maze.map[y * maze.width + x - 1] != 16:
                            _put_left(colors['Grid 1'], x, y, img, wall_range, img.thickness)
                            _put_right(colors['Grid 1'], x-1, y, img, wall_range, img.thickness)
                        if x == maze.width - 1 or maze.map[y * maze.width + x + 1] != 16:
                            _put_right(colors['Grid 1'], x, y, img, wall_range, img.thickness)
                            _put_left(colors['Grid 1'], x+1, y, img, wall_range, img.thickness)
                        if maze.map[(y-1) * maze.width + x] != 16:
                            _put_up(colors['Grid 1'], x, y, img, wall_range, img.thickness)
                            _put_down(colors['Grid 1'], x, y-1, img, maze, wall_range, img.thickness)
                        if y == maze.height - 1 or maze.map[(y+1) * maze.width + x] != 16:
                            _put_down(colors['Grid 1'], x, y, img, maze, wall_range, img.thickness)
                            _put_up(colors['Grid 1'], x, y+1, img, wall_range, img.thickness)
                        if maze.map[y * maze.width + x - 1] == 16:
                            if maze.map[(y-1) * maze.width + x - 1] != 16:
                                _put_up(colors['Grid 1'], x - 1, y, img, wall_range, img.thickness)
                                _put_down(colors['Grid 1'], x - 1, y - 1, img, maze, wall_range, img.thickness)
                        if maze.map[(y - 1) * maze.width + x] == 16:
                            if maze.map[(y-1) * maze.width + x - 1] != 16:
                                _put_left(colors['Grid 1'], x, y - 1, img, wall_range, img.thickness)
                                _put_right(colors['Grid 1'], x - 1, y - 1, img, wall_range, img.thickness)
                    if maze.map[y * maze.width + x] & (1 << Direction.SOUTH.value):
                        _put_down(colors['Grid 1'], x, y, img, maze, wall_range, img.thickness)
                        _put_up(colors['Grid 1'], x, y + 1, img, wall_range, img.thickness)
                        if y == maze.height:
                            _put_down(colors['Grid 1'], x, y - 1, img, maze, wall_range, img.thickness)
                    if maze.map[y * maze.width + x] & (1 << Direction.NORTH.value):
                        _put_up(colors['Grid 1'], x, y, img, wall_range, img.thickness)
                        _put_down(colors['Grid 1'], x, y-1, img, maze, wall_range, img.thickness)
                    if maze.map[y * maze.width + x] & (1 << Direction.WEST.value):
                        _put_left(colors['Grid 1'], x, y, img, wall_range, img.thickness)
                        _put_right(colors['Grid 1'], x-1, y, img, wall_range, img.thickness)
                    if maze.map[y * maze.width + x] & (1 << Direction.EAST.value):
                        _put_right(colors['Grid 1'], x, y, img, wall_range, img.thickness)
                        _put_left(colors['Grid 1'], x+1, y, img, wall_range, img.thickness)
                    if maze.map[y * maze.width + x - 1] & (1 << Direction.NORTH.value):
                        _put_up(colors['Grid 1'], x - 1, y, img, wall_range, img.thickness)
                        _put_down(colors['Grid 1'], x - 1, y-1, img, maze, wall_range, img.thickness)
                    if maze.map[(y - 1)* maze.width + x] & (1 << Direction.WEST.value):
                        _put_left(colors['Grid 1'], x, y - 1, img, wall_range, img.thickness)
                        _put_right(colors['Grid 1'], x - 1, y - 1, img, wall_range, img.thickness)
        m.mlx_put_image_to_window(mlx, win.ptr, img.ptr, 0, offset)
        m.mlx_pixel_put(mlx, win.ptr, 0, 0, 0xFF000000)
