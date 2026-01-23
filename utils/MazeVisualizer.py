from mlx import Mlx
from objects import Image, Maze, Window
from enums import Direction
from .Draw import Draw
from algorithms.MazeGenerator import MazeGenerator
from random import randint
from typing import List


class MazeVisualizer():

    def __init__(
            self, maze, 
            enter: tuple[int, int], exit: tuple[int, int]):
        self.path = maze.path
        self.enter = enter
        self.exit = exit
        self.maze = maze
        self.x = -1
        self.y = -2
        self.colors = {
            '42': bytes([255, 0, 0, 255]),
            'Grid 1': bytes([255, 255, 255, 255]),
            'Grid 2': bytes([15, 15, 15, 255]),
            'Block found': bytes([0, 0, 0, 255]),
            'Block not found': bytes([30, 30, 30, 255]),
            'Snake': bytes([0, 0, 255, 255]),
            'Background': bytes([25, 25, 25, 255]),
        }
        self.palette = [
            # rząd 1
            bytes([255, 255, 255, 255]), bytes([192, 192, 192, 255]), bytes([255, 192, 192, 255]),
            bytes([255, 224, 192, 255]),
            bytes([255, 255, 192, 255]), bytes([192, 255, 192, 255]), bytes([192, 255, 255, 255]),
            bytes([192, 192, 255, 255]),

            # rząd 2
            bytes([224, 224, 224, 255]), bytes([160, 160, 160, 255]), bytes([255, 160, 160, 255]),
            bytes([255, 192, 160, 255]),
            bytes([255, 255, 160, 255]), bytes([160, 255, 160, 255]), bytes([160, 255, 255, 255]),
            bytes([160, 160, 255, 255]),

            # rząd 3
            bytes([192, 192, 192, 255]), bytes([128, 128, 128, 255]), bytes([255, 128, 128, 255]),
            bytes([255, 160, 128, 255]),
            bytes([255, 255, 128, 255]), bytes([128, 255, 128, 255]), bytes([128, 255, 255, 255]),
            bytes([128, 128, 255, 255]),

            # rząd 4
            bytes([160, 160, 160, 255]), bytes([96, 96, 96, 255]), bytes([255, 96, 96, 255]),
            bytes([255, 128, 96, 255]),
            bytes([255, 255, 96, 255]), bytes([96, 255, 96, 255]), bytes([96, 255, 255, 255]),
            bytes([96, 96, 255, 255]),

            # rząd 5
            bytes([128, 128, 128, 255]), bytes([64, 64, 64, 255]), bytes([255, 0, 0, 255]), bytes([255, 128, 0, 255]),
            bytes([255, 255, 0, 255]), bytes([0, 255, 0, 255]), bytes([0, 255, 255, 255]), bytes([0, 0, 255, 255]),

            # rząd 6
            bytes([96, 96, 96, 255]), bytes([32, 32, 32, 255]), bytes([192, 0, 0, 255]), bytes([192, 96, 0, 255]),
            bytes([192, 192, 0, 255]), bytes([0, 192, 0, 255]), bytes([0, 192, 192, 255]), bytes([0, 0, 192, 255]),

            # rząd 7
            bytes([64, 64, 64, 255]), bytes([0, 0, 0, 255]), bytes([128, 0, 0, 255]), bytes([128, 64, 0, 255]),
            bytes([128, 128, 0, 255]), bytes([0, 128, 0, 255]), bytes([0, 128, 128, 255]), bytes([0, 0, 128, 255]),

            # rząd 8
            bytes([32, 32, 32, 255]), bytes([16, 16, 16, 255]), bytes([64, 0, 0, 255]), bytes([64, 32, 0, 255]),
            bytes([64, 64, 0, 255]), bytes([0, 64, 0, 255]), bytes([0, 64, 64, 255]), bytes([0, 0, 64, 255]),
        ]

    def draw_slow(self, vars):
        if not self.bool:
            return
        try:
            found = next(self.generator)
            self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win, found, self.colors)
        except StopIteration as e:
            self.bool = False

    def _new_image_dict(self, mlx, width, height, i):
        img = mlx.mlx_new_image(self.mlx, width, height)
        data, bpp, sizeline, theformat = mlx.mlx_get_data_addr(img)
        data[:] = bytes([10*i, 10*i, 10*i, 255]) * (width*height)
        return {
            "img": img,
            "data": data,
            "bpp": bpp,
            "sizeline": sizeline,
            "theformat": theformat,
        }

    def fill_striped_block(self):
        data = self.colors_block_data
        width = self.colors_block.width

        self.segment_height = ((len(data) // 4) // width // 32) - 2

        leng = len(data)
        segment_bytes = leng // 32
        rows_in_segment = segment_bytes // (width * 4)

        color_left = self.colors['Background']
        self.segment_width = int((float(width) - 8.5 * float(self.segment_height)) // 8) - 2

        for i in range(32):
            segment_start = i * segment_bytes

            for row in range(rows_in_segment):
                row_start = segment_start + row * width * 4
                row_end = row_start + width * 4

                if i % 4 == 0:
                    data[row_start:row_end] = color_left * width
                else:
                    if row == 0 and i % 4 == 1 or row == rows_in_segment - 1 and i % 4 == 3:
                        data[row_start:row_end] = (
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * width
                        )[:width * 4]

                    else:
                        palette_base = ((i - 1) // 4) * 8

                        data[row_start:row_end] = (
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) +
                                self.palette[palette_base + 0] * self.segment_width +
                                bytes([255, 255, 255, 255]) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) +
                                self.palette[palette_base + 1] * self.segment_width +
                                bytes([255, 255, 255, 255]) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) +
                                self.palette[palette_base + 2] * self.segment_width +
                                bytes([255, 255, 255, 255]) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) +
                                self.palette[palette_base + 3] * self.segment_width +
                                bytes([255, 255, 255, 255]) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) +
                                self.palette[palette_base + 4] * self.segment_width +
                                bytes([255, 255, 255, 255]) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) +
                                self.palette[palette_base + 5] * self.segment_width +
                                bytes([255, 255, 255, 255]) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) +
                                self.palette[palette_base + 6] * self.segment_width +
                                bytes([255, 255, 255, 255]) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) +
                                self.palette[palette_base + 7] * self.segment_width +
                                bytes([255, 255, 255, 255]) +
                                color_left * width
                        )[:width * 4]

        last_row_start = leng - width * 4
        last_row_end = leng
        data[last_row_start:last_row_end] = (
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * self.segment_height +
                                bytes([255, 255, 255, 255]) * (self.segment_width + 2) +
                                color_left * width
                        )[:width * 4]

    def darken(self, color: bytes, factor: float) -> bytes:
        r, g, b, a = color
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return bytes([r, g, b, a])

    def transparent(self, color: bytes, level: int) -> bytes:
        r, g, b, a = color
        return bytes([r, g, b, level])

    def show_menu(self):
        self.background_img_data[:] = self.colors['Background'] * (len(self.background_img_data) // 4)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)
        self.menu_img_data[:] = self.darken(self.colors['Background'], 0.6) * (len(self.menu_img_data) // 4)
        self.fill_striped_block()
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.menu_img.ptr, self.win.width // 8 * 7, 0)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60, self.win.height // 64)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60, self.win.height // 64*9)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60, self.win.height // 64*17)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60, self.win.height // 64*25)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60, self.win.height // 64*33)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60, self.win.height // 64*41)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60, self.win.height // 64*49)
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64, 0xFFFFFFFF, "42")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64*9, 0xFFFFFFFF, "Grid 1")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64*17, 0xFFFFFFFF, "Grid 2")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64*25, 0xFFFFFFFF, "Block found")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64*33, 0xFFFFFFFF, "Block not found")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64*41, 0xFFFFFFFF, "Snake")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64*49, 0xFFFFFFFF, "Background")


    def drawq(self, generator, seed):

        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        self.win = Window(self.m, self.mlx, "window")
        self.img = Image(self.m, self.mlx, self.win, self.maze)
        self.background_img = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 8 * 7, self.win.height)
        self.background_img_data = self.m.mlx_get_data_addr(self.background_img.ptr)[0]
        self.background_img_data[:] = self.colors['Background'] * (len(self.background_img_data)//4)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)
        self.menu_img = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 8, self.win.height)
        self.menu_img_data = self.m.mlx_get_data_addr(self.menu_img.ptr)[0]
        self.menu_img_data[:] = (self.colors['Background'][:3] + bytes([128])) * (len(self.menu_img_data) // 4)
        self.colors_block = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 16, self.win.height // 64*7)
        self.colors_block_data = self.m.mlx_get_data_addr(self.colors_block.ptr)[0]
        self.show_menu()
        self.gen = generator
        self.seed = seed
        self.draw = Draw()
        self.vars = {
            'm': self.m,
            'mlx': self.mlx,
            'img': self.img,
            'win': self.win,
            'maze': self.maze,
            'draw': self.draw.draw_maze,
            'generator': generator,
            'draw_out': self.draw.draw_out
        }
        self.m.mlx_key_hook(self.win.ptr, self.key_hook, self.vars)
        self.m.mlx_mouse_hook(self.win.ptr, self.mouse_hook, self.vars)
        self.bool = True
        self.m.mlx_loop_hook(self.mlx, self.draw_slow, self.vars)
        self.gen = generator
        self.generator = self.gen.create_maze(self.maze, seed)
        self.m.mlx_loop(self.mlx)



    @staticmethod
    def close_window(vars: dict) -> int:
        vars['m'].mlx_destroy_window(vars['mlx'], vars['win'].ptr)
        vars['m'].mlx_loop_exit(vars['mlx'])
        return 0

    @staticmethod
    def can_go(maze: Maze, dir: Direction) -> bool:
        left, down, right, up = map(
            lambda b: b == '1',
            f"{int(maze.lines[maze.pacman.y][maze.pacman.x], 16):04b}"
        )
        dirs = {
            Direction.LEFT: not left,
            Direction.DOWN: not down,
            Direction.RIGHT: not right,
            Direction.UP: not up
        }
        return dirs.get(dir, False)

    def mouse_hook(self, cos, x, y, args):
        blocks = {
            '42': {
                'start': self.win.height // 64 + self.segment_height,
                'end': self.win.height // 64 + self.colors_block.height,
            },
            'Grid 1': {
                'start': self.win.height // 64 * 9 + self.segment_height,
                'end': self.win.height // 64 * 9 + self.colors_block.height,
            },
            'Grid 2': {
                'start': self.win.height // 64 * 17 + self.segment_height,
                'end': self.win.height // 64 * 17 + self.colors_block.height,
            },
            'Block found': {
                'start': self.win.height // 64 * 25 + self.segment_height,
                'end': self.win.height // 64 * 25 + self.colors_block.height,
            },
            'Block not found': {
                'start': self.win.height // 64 * 33 + self.segment_height,
                'end': self.win.height // 64 * 33 + self.colors_block.height,
            },
            'Snake': {
                'start': self.win.height // 64 * 41 + self.segment_height,
                'end': self.win.height // 64 * 41 + self.colors_block.height,
            },
            'Background': {
                'start': self.win.height // 64 * 49 + self.segment_height,
                'end': self.win.height // 64 * 49 + self.colors_block.height
            }
        }
        x_start = self.win.width // 64 * 60 + self.segment_height
        x_end = x_start + self.segment_width * 8 + self.segment_height * 10
        block_width = (x_end - x_start)/8
        if x_start < x <= x_end:
            for name, yy in blocks.items():
                if yy['start'] + self.segment_height / 2 <= y <= yy['end']:

                    y_rel = y - yy['start']
                    x_rel = x - x_start

                    if 0 <= y_rel < block_width * 8 and 0 <= x_rel < block_width * 8:
                        row = int(y_rel // block_width)
                        col = int(x_rel // block_width)
                        self.colors[name] = self.transparent(self.palette[row*8+col], 10)
                        if name == 'Background':
                            self.background_img_data[:] = self.colors['Background'] * (len(self.background_img_data)//4)
                            self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)
                            self.menu_img_data[:] = self.colors['Background'] * (len(self.menu_img_data) // 4)
                            self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.menu_img.ptr,
                                                           self.win.width // 8 * 7, 0)
                            self.show_menu()

    def key_hook(self, keycode, vars):
        img: Image = vars['img']
        maze: Maze = vars['maze']
        win: Window = vars['win']
        mlx = vars['mlx']
        draw: callable = vars['draw']
        m: Mlx = vars['m']
        #print(keycode)
        if keycode == 110:
            self.generator = self.gen.create_maze(self.maze, randint(0,9999))
            self.bool = True
        if keycode == 65451:
            img.thickness += 1
        if keycode == 65453:
            if (img.thickness > 1):
                img.thickness -= 1
        if keycode == 65361 and self.maze.width > 4:
            self.maze.width -= 1
            self.generator = self.gen.create_maze(self.maze, randint(0,9999))
            self.img = Image(self.m, self.mlx, self.win, self.maze)
            self.bool = True
        if keycode == 65362 and self.maze.height > 4:
            self.maze.height -= 1
            self.generator = self.gen.create_maze(self.maze, randint(0, 9999))
            self.img = Image(self.m, self.mlx, self.win, self.maze)
            self.bool = True
        if keycode == 65363:
            self.maze.width += 1
            self.generator = self.gen.create_maze(self.maze, randint(0, 9999))
            self.img = Image(self.m, self.mlx, self.win, self.maze)
            self.bool = True
        if keycode == 65364:
            self.maze.height += 1
            self.generator = self.gen.create_maze(self.maze, randint(0, 9999))
            self.img = Image(self.m, self.mlx, self.win, self.maze)
            self.bool = True
        if keycode == 65307:
            m.mlx_destroy_window(mlx, win.ptr)
            m.mlx_loop_exit(mlx)
