from objects import Image, Maze, Window, Brick
from mlx import Mlx
from enums import Axle, Sign, Direction
from typing import Optional
class Draw():

    def _put_brick(
            cls, i: int, j: int, img, thickness: int, transparency: int,
            brick,
            color: bytes = None, mortar_color: bytes = None) -> None:
        start_x = i * img.scale + thickness
        start_y = j * img.scale + thickness
        size = img.scale


        for y in range(start_y, start_y + size):
            offset = (y * img.width + start_x) * 4
            img.data[offset: offset + size * 4] = brick.mortar if y % brick.brick_h < brick.mortar_thickness_y else brick.row_1 if (y // brick.brick_h)%2 == 0 else brick.row_3

    def _put_block(cls, i: int, j: int, img, line: bytes, color:bytes, thickness: int) -> None:

        start_x = i * img.scale + thickness
        start_y = j * img.scale + thickness
        size = img.scale - thickness

        row = color * size

        for y in range(start_y, start_y + size):
            offset = (y * img.width + start_x) * 4
            img.data[offset: offset + size * 4] = row

    def _put_up(cls, m: Mlx, mlx: any, win: Window, line: bytes, color: bytes, i: int, j: int, img: Image, wall_range: tuple, out: bool) -> None:

        start_y = j * img.scale + img.thickness
        start_x = i * img.scale + img.thickness - 1

        y_start = start_y + (-img.thickness if j == 0 else 0)
        y_end = start_y + img.thickness

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

    def _put_down(cls, m: Mlx, mlx: any, win: Window, line: int, color: bytes,
            i: int, j: int, img: Image, maze: Maze, w_range: tuple, out: bool
            ) -> None:

        start_x = i * img.scale + img.thickness - 1

        y_start = (
                (j + 1) * img.scale
                - img.thickness
                + (img.thickness if j == maze.height - 1 else 0)
                + img.thickness
        )
        y_end = (j + 1) * img.scale + img.thickness

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

    def _put_left(cls, m: Mlx, mlx: any, win: Window, line: bytes, color: bytes, i: int, j: int, img: Image, w_range: tuple, out: bool) -> None:
        start_y = j * img.scale + img.thickness - 1
        x_base = i * img.scale + img.thickness

        data = img.data
        width = img.width
        height = img.height

        y0 = start_y + w_range[0]
        y1 = start_y + w_range[1]

        pixels = img.thickness
        line = color * pixels

        # clip Y
        y0 = max(0, y0)
        y1 = min(height, y1)

        if y0 >= y1:
            return

        for y in range (y0,y1):
            offset = (y * width + x_base) * 4
            data[offset:offset + pixels*4] = line

    def _put_right(cls, m: Mlx, mlx: any, win: Window, line: bytes, color: bytes,
            i: int, j: int, img: Image, maze: Maze, w_range: tuple, out: bool
            ) -> None:
        start_y = j * img.scale + img.thickness - 1
        x_base = (i+1) * img.scale

        data = img.data
        width = img.width
        height = img.height

        # zakres Y
        y0 = start_y + w_range[0]
        y1 = start_y + w_range[1]

        pixels = img.thickness
        line = color * pixels
        # clip Y
        y0 = max(0, y0)
        y1 = min(height, y1)

        if y0 >= y1:
            return
        for y in range (y0,y1):
            offset = (y * width + x_base) * 4
            data[offset:offset + pixels*4] = line

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

    def draw_path(
            cls, m: Mlx, mlx: any, maze, img: Image, win: Window, list, colors:dict, lines: dict, play: bool
    ):
        if isinstance(list, int):
            x = list % maze.width
            y = list // maze.width
            cls._put_block(x, y, img, lines['Snake'], colors['Snake'][:3] + bytes([255]), img.thickness)
            m.mlx_put_image_to_window(mlx, win.ptr, img.ptr, 0, (img.height - maze.height*img.scale)//2)
            #m.mlx_pixel_put(mlx, win.ptr, 0, 0, 0xFF000000)
        else:
            for path in list:
                x = path % maze.width
                y = path // maze.width
                cls._put_block(x, y, img, lines['Snake'], colors['Snake'][:3] + bytes([255]), img.thickness)
                m.mlx_put_image_to_window(mlx, win.ptr, img.ptr, 0, (img.height - maze.height*img.scale)//2)
                m.mlx_pixel_put(mlx, win.ptr, 0, 0, 0xFF000000)
            play = False

    def draw_maze(
            cls, a: int, s: int, m: Mlx, mlx: any, maze, img: Image, win: Window, found, colors: dict, darken,
            brick_visible: bool,
            brick: Brick, lines: dict
            ) -> None:
        row_pixels = img.width
        fill_pixels = maze.width * img.scale + img.thickness*2
        rest_pixels = row_pixels - fill_pixels

        for row in range(maze.height * img.scale + img.thickness*2):
            row_start = row * img.width * 4
            row_end = row_start + img.width * 4

            # Zamaluj pierwszą część
            img.data[row_start:row_start + fill_pixels * 4] = colors['Grid 2'] * fill_pixels

            # Zamaluj resztę wiersza
            #img.data[row_start + fill_pixels * 4: row_end] = darken(colors['Background'][:3] + bytes([255]), 0.6) * rest_pixels

        #img.data[:maze.width*img.scale] = colors['Grid 2'] * (len(img.data)//4)
        wall_range = (-img.thickness+1, img.scale + img.thickness)
        for y in range(maze.height):
            for x in range (maze.width):
                if len(maze.map) > 0:
                    if (y * maze.width + x) not in found:
                        cls._put_block(x, y, img, lines['Block not found'], colors['Block not found'], 0)
                #cls._put_up(m, mlx, win.ptr, lines['line_x'], colors['Grid 2'], x, y, img, wall_range, False)
                #cls._put_down(m, mlx, win.ptr, lines['line_x'], colors['Grid 2'], x, y, img, maze, wall_range, False)
                #cls._put_left(m, mlx, win.ptr, lines['line_y'], colors['Grid 2'], x, y, img, wall_range, False)
                #cls._put_right(m, mlx, win.ptr, lines['line_y'], colors['Grid 2'], x, y, img, maze, wall_range, False)
        for y in range(maze.height):
            for x in range(maze.width):
                if len(maze.map) > 0:
                    if (y * maze.width + x) in found:
                        if brick_visible:
                            cls._put_brick(x, y, img, 0, int(colors['42'][3]), brick)
                        else:
                            cls._put_block(x, y, img, lines['Block found'], colors['Block found'], img.thickness)
                    if maze.map[y * maze.width + x] == 15:
                        cls._put_block(x, y, img, lines['42'], colors['42'], img.thickness)
                        cls._put_down(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x, y-1, img, maze, wall_range, False)
                        cls._put_up(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x, y+1, img, wall_range, False)
                        cls._put_left(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x+1, y, img, wall_range, False)
                        cls._put_right(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x-1, y, img, maze, wall_range, False)
                    if maze.map[y * maze.width + x] == 16:
                        cls._put_block(x, y, img, lines['Snake'], colors['Snake'], 0)
                        if maze.map[y * maze.width + x - 1] != 16:
                            cls._put_left(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x, y, img, wall_range, False)
                            cls._put_right(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x-1, y, img, maze, wall_range, False)
                        if x == maze.width - 1 or maze.map[y * maze.width + x + 1] != 16:
                            cls._put_right(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x, y, img, maze, wall_range, False)
                            cls._put_left(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x+1, y, img, wall_range, False)
                        if maze.map[(y-1) * maze.width + x] != 16:
                            cls._put_up(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x, y, img, wall_range, False)
                            cls._put_down(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x, y-1, img, maze, wall_range, False)
                        if y == maze.height - 1 or maze.map[(y+1) * maze.width + x] != 16:
                            cls._put_down(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x, y, img, maze, wall_range, False)
                            cls._put_up(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x, y+1, img, wall_range, False)
                        if maze.map[y * maze.width + x - 1] == 16:
                            if maze.map[(y-1) * maze.width + x - 1] != 16:
                                cls._put_up(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x - 1, y, img, wall_range, False)
                                cls._put_down(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x - 1, y - 1, img, maze, wall_range, False)
                        if maze.map[(y - 1) * maze.width + x] == 16:
                             if maze.map[(y-1) * maze.width + x - 1] != 16:
                                 cls._put_left(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x, y - 1, img, wall_range, False)
                                 cls._put_right(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x - 1, y - 1, img, maze, wall_range,False)
                    #if y * maze.width + x == maze.entry:
                        #cls._put_block(x, y, img, bytes([0, 255, 0, 10]), img.thickness)
                    #if y * maze.width + x == maze.exit:
                        #cls._put_block(x, y, img, bytes([255, 0, 0, 10]), img.thickness)
                    if maze.map[y * maze.width + x] & (1 << Direction.SOUTH.value):
                        cls._put_down(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x, y, img, maze, wall_range, False)
                        cls._put_up(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x, y + 1, img, wall_range, False)
                        if y == maze.height:
                            cls._put_down(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x, y - 1, img, maze, wall_range, False)
                    if maze.map[y * maze.width + x] & (1 << Direction.NORTH.value):
                        cls._put_up(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x, y, img, wall_range, False)
                        cls._put_down(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x, y-1, img, maze, wall_range, False)
                    if maze.map[y * maze.width + x] & (1 << Direction.WEST.value):
                        cls._put_left(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x, y, img, wall_range, False)
                        cls._put_right(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x-1, y, img, maze, wall_range, False)
                    if maze.map[y * maze.width + x] & (1 << Direction.EAST.value):
                        cls._put_right(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x, y, img, maze, wall_range, False)
                        cls._put_left(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x+1, y, img, wall_range, False)
                    if maze.map[y * maze.width + x - 1] & (1 << Direction.NORTH.value):
                        cls._put_up(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x - 1, y, img, wall_range, False)
                        cls._put_down(m, mlx, win.ptr, lines['line_x'], colors['Grid 1'], x - 1, y-1, img, maze, wall_range, False)
                    if maze.map[(y - 1)* maze.width + x] & (1 << Direction.WEST.value):
                        cls._put_left(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x, y - 1, img, wall_range, False)
                        cls._put_right(m, mlx, win.ptr, lines['line_y'], colors['Grid 1'], x - 1, y - 1, img, maze, wall_range, False)
        m.mlx_put_image_to_window(mlx, win.ptr, img.ptr, 0, (img.height - maze.height*img.scale)//2)
        m.mlx_pixel_put(mlx, win.ptr, 0, 0, 0xFF000000)
