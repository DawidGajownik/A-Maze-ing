from copy import copy
from datetime import datetime
from random import randint
from typing import Tuple, Any

from algorithms import PathFinder, MazeGenerator
from mlx import Mlx
from objects import Image, Window, Brick
from MAZE import MazeManager
from colors import colors
from .Draw import Draw


def darken(color: bytes, factor: float) -> bytes:
    r, g, b, a = color
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return bytes([r, g, b, a])


def transparent(color: bytes, level: int) -> bytes:
    r, g, b, a = color
    return bytes([r, g, b, level])


class MazeVisualizer:

    def __init__(
            self, maze: MazeManager, path_finder: PathFinder):
        self.start_time = datetime.now()
        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        self.win = Window(self.m, self.mlx, "A-Maze-ing")
        self.draw = Draw()
        self.exit = exit
        self.maze = maze
        self.x = -1
        self.y = -2
        self.transparency = 1
        self.maze_draw = True
        self.menu_showed = False
        self.brick_visible = False
        self.paused = False
        self.frozen = False
        self.player = True
        self.path_finding: bool = False
        self.slider_x = 1
        self.theme_idx = 1
        self.path_finder = path_finder
        self.finder = self.path_finder.find_path(maze)
        self.themes = colors.get_themes(self.transparency)
        self.colors = copy(self.themes[self.theme_idx])
        self.palette = colors.get_palette()
        self.img = Image(self.m, self.mlx, self.win, self.maze)
        self.path_img = Image(self.m, self.mlx, self.win, self.maze)
        self.final_path_img = Image(self.m, self.mlx, self.win, self.maze)
        self.offset\
            = (self.img.height - self.maze.height * self.img.scale) // 2 - 8
        self.color_blocks_height_multipliers = [1, 9, 17, 25, 33, 41, 49]
        self.load_images()
        self.create_elements()
        self.create_background_images()
        self.create_blocks()
        self.map_keys()
        self.set_images_and_position()
        self.set_palettes_data()

    def load_images(self) -> None:
        self.icon_size = self.get_icon_size()
        self.save: Tuple[Any, int, int]\
            = self.m.mlx_png_file_to_image(self.mlx, "pictures/save.png")
        self.play: Tuple[Any, int, int]\
            = self.m.mlx_png_file_to_image(self.mlx, "pictures/play.png")
        self.pause: Tuple[Any, int, int]\
            = self.m.mlx_png_file_to_image(self.mlx, "pictures/pause.png")
        self.freeze: Tuple[Any, int, int]\
            = self.m.mlx_png_file_to_image(self.mlx, "pictures/freeze.png")
        self.frozen_img: Tuple[Any, int, int]\
            = self.m.mlx_png_file_to_image(self.mlx, "pictures/frozen.png")
        self.start: Tuple[Any, int, int]\
            = self.m.mlx_png_file_to_image(
            self.mlx, f"pictures/start{self.icon_size}.png")
        self.finish: Tuple[Any, int, int]\
            = self.m.mlx_png_file_to_image(
            self.mlx, f"pictures/finish{self.icon_size}.png")
        self.refresh: Tuple[Any, int, int]\
            = self.m.mlx_png_file_to_image(self.mlx, "pictures/refresh.png")

    def create_elements(self) -> None:
        self.brick = Brick(
            self.img.scale, self.transparency, darken,
            self.colors['Block found'], bytes([30, 30, 30, 30]))
        self.corrector = Image(
            self.m, self.mlx, self.win, self.maze,
            self.win.width // 400, self.win.width // 100)
        self.corrector_data = self.m.mlx_get_data_addr(self.corrector.ptr)[0]
        self.corrector_data[:]\
            = bytes([120, 120, 120, 255]) * (len(self.corrector_data) // 4)
        self.slider = Image(
            self.m, self.mlx, self.win, self.maze,
            self.win.width // 20, self.win.width // 400)
        self.slider_data = self.m.mlx_get_data_addr(self.slider.ptr)[0]
        self.slider_data[:]\
            = bytes([255, 255, 255, 255]) * (len(self.slider_data) // 4)
        self.colors_block = Image(
            self.m, self.mlx, self.win, self.maze,
            self.win.width // 16, self.win.height // 64 * 7)
        self.colors_block_data\
            = self.m.mlx_get_data_addr(self.colors_block.ptr)[0]
        self.create_color_palette()

    def create_background_images(self) -> None:
        self.strings_background = Image(
            self.m, self.mlx, self.win, self.maze,
            self.win.width // 8, self.win.height // 8)
        self.strings_background.data[:]\
            = bytes([0, 0, 0, 255]) * (len(self.strings_background.data) // 4)
        self.background_img = Image(
            self.m, self.mlx, self.win, self.maze,
            self.win.width, self.win.height)
        self.background_img.data[:]\
            = bytes([0, 0, 0, 255]) * (len(self.background_img.data) // 4)
        self.background_img_with_transparency = Image(
            self.m, self.mlx, self.win, self.maze,
            self.win.width, self.win.height)
        self.background_img_with_transparency.data[:] = bytes(
            [0, 0, 0, self.transparency]) * (
                len(self.background_img_with_transparency.data) // 4)
        self.menu_img = Image(
            self.m, self.mlx, self.win, self.maze,
            self.win.width // 8, self.win.height)
        self.menu_img.data[:] = darken(
            self.colors['Background'], 0.6) * (len(self.menu_img.data) // 4)

    def create_blocks(self) -> None:
        self.blocks = {
            '42': {
                'start': self.win.height // 64,
                'end': self.win.height // 64 + self.colors_block.height,
            },
            'Grid 1': {
                'start': self.win.height // 64 * 9,
                'end': self.win.height // 64 * 9 + self.colors_block.height,
            },
            'Grid 2': {
                'start': self.win.height // 64 * 17,
                'end': self.win.height // 64 * 17 + self.colors_block.height,
            },
            'Block found': {
                'start': self.win.height // 64 * 25,
                'end': self.win.height // 64 * 25 + self.colors_block.height,
            },
            'Block not found': {
                'start': self.win.height // 64 * 33,
                'end': self.win.height // 64 * 33 + self.colors_block.height,
            },
            'Snake': {
                'start': self.win.height // 64 * 41,
                'end': self.win.height // 64 * 41 + self.colors_block.height,
            },
            'Background': {
                'start': self.win.height // 64 * 49,
                'end': self.win.height // 64 * 49 + self.colors_block.height
            }
        }

    def map_keys(self) -> None:
        self.keys = {
            'b': 98,
            'l': 108,
            'j': 106,
            'i': 105,
            'k': 107,
            'numpad-8': 65431,
            'numpad-2': 65433,
            'numpad-6': 65432,
            'numpad-4': 65430,
            'w': 119,
            's': 115,
            'd': 100,
            'a': 97,
            'n': 110,
            'numpad-plus': 65451,
            'numpad-minus': 65453,
            'left-arrow': 65361,
            'up-arrow': 65362,
            'right-arrow': 65363,
            'down-arrow': 65364,
            'esc': 65307
        }

    def set_images_and_position(self) -> None:
        self.images_with_height_and_width = {
            self.save[0]:
            {
                'width': self.win.width // 64 * 63,
                'height': self.win.height // 64 * 57
            },
            self.refresh[0]:
            {
                'width': self.win.width // 64 * 61,
                'height': self.win.height // 64 * 57
            },
            self.play[0] if self.paused else self.pause[0]:
            {
                'width': self.win.width // 64 * 63,
                'height': self.win.height // 64 * 59
            },
            self.frozen_img[0] if self.frozen else self.freeze[0]:
            {
                'width': self.win.width // 64 * 63,
                'height': self.win.height // 64 * 61
            },
            self.slider.ptr:
            {
                'width': self.win.width // 128 * 119,
                'height': self.win.height // 64 * 59 + self.play[1]//2
            },
            self.corrector.ptr:
            {
                'width': (
                        self.slider_x * self.slider.width // 100
                        + self.win.width // 128 * 119),
                'height': (
                        self.win.height // 64 * 59 + self.play[1]//2
                        - self.corrector.height//2 + self.slider.height//2)
            },
        }

    def set_palettes_data(self) -> None:
        self.palettes_descriptions_with_height_multiplier = {
            "42": 1,
            "Grid found": 9,
            "Grid not found": 17,
            "Block found": 25,
            "Block not found": 33,
            "Snake": 41,
            "Background": 49
        }

    def set_menu_data(self) -> None:
        self.menu_data = {
            "Y=" + str(self.maze.height):
                {
                    'width': self.win.width // 64 * 57,
                    'height': self.win.height // 64 * 56
                },
            "X=" + str(self.maze.width):
                {
                    'width': self.win.width // 64 * 57,
                    'height': self.win.height // 64 * 57
                },
            f"S={self.seed}":
                {
                    'width': self.win.width // 64 * 57,
                    'height': self.win.height // 64 * 58
                },
            "Tr=" + str(self.transparency) + "(w/s)":
                {
                    'width': self.win.width // 64 * 57,
                    'height': self.win.height // 64 * 61
                },
            "Th=" + str(self.theme_idx) + "(a/d)":
                {
                    'width': self.win.width // 64 * 57,
                    'height': self.win.height // 64 * 62
                },
            "Thi=" + str(self.img.thickness) + "(+/-)":
                {
                    'width': self.win.width // 64 * 57,
                    'height': self.win.height // 64 * 63
                },
            f"{self.slider_x}x":
                {
                    'width': self.win.width * 251 // 256,
                    'height': self.win.height * 231 // 256
                }
        }

    def draw_maze(self, vars: dict) -> None:
        if not self.maze_draw or self.frozen:
            if self.path_finding:
                self.draw_path()
            return
        try:
            diff = (datetime.now() - self.start_time).total_seconds()*2
            transparency = int((diff*diff))
            if 0 < transparency < 25:
                if self.transparency != transparency:
                    self.transparency = transparency
                    for color in self.colors:
                        if color != 'name':
                            self.colors[color]\
                                = transparent(self.colors[color],
                                              self.transparency)
            if not self.paused:
                self.found = next(self.generator)
                self.gen.visualisation_tempo = self.slider_x
            # self.m.mlx_put_image_to_window(self.mlx, self.win.ptr,
            # self.start[0], self.enter[0]*self.img.scale,
            # self.enter[1]*self.img.scale)
            self.m.mlx_put_image_to_window(
                self.mlx, self.win.ptr,
                self.background_img_with_transparency.ptr, 0, 0)
            self.show_menu()
            self.draw.draw_maze(
                self.m, self.mlx, self.maze, self.img,
                self.win, self.found[0], self.colors,
                self.brick_visible, self.brick, self.offset)
            self.time = datetime.now()

        except StopIteration:
            if not self.path_finding:
                self.path_finding = True
                self.maze_draw = False

    def draw_path(self) -> None:
        try:
            self.path = next(self.finder)
            # self.m.mlx_put_image_to_window(self.mlx, self.win.ptr,
            # self.start[0], self.enter[0]*self.img.scale,
            # self.enter[1]*self.img.scale)
            self.m.mlx_put_image_to_window(
                self.mlx, self.win.ptr,
                self.background_img_with_transparency.ptr, 0, 0)
            self.m.mlx_put_image_to_window(
                self.mlx, self.win.ptr, self.img.ptr, 0, self.offset)
            self.show_menu()

            self.draw.draw_path(
                self.m, self.mlx, self.maze, self.img,
                self.path_img, self.final_path_img, self.win,
                self.path, self.colors, self.offset)
        except StopIteration:
            self.path_finding = False
            self.maze_draw = False

    def create_color_palette(self) -> None:
        data = self.colors_block_data
        leng = len(data)
        height = self.colors_block.height
        width = self.colors_block.width
        line_size = leng // height
        space_size = 2
        color_block_height = height//10 - 3
        l_size = line_size // 4
        wid = (l_size - 16 * space_size) // 8
        sequence = bytearray()
        background = bytes([0, 0, 0, 0])
        white = bytes([255, 255, 255, 255])
        for i in range(8):
            sequence.extend(
                (
                        background * (l_size * space_size) +  # offset y
                        (
                            # white stripe y
                            (
                                background * space_size +  # offset x
                                white * wid +  # white stripe
                                background * space_size
                            ) * 8 +  # offset x
                            (background * (l_size - 8 * (
                                    space_size * 2 + wid)))  # fill to full line
                        )
                        +
                        (
                            # blocks
                            (
                                    b''.join(
                                        background * space_size +
                                        white +
                                        self.palette[i * 8 + j] * (wid - 2) +
                                        white +
                                        background * space_size
                                        for j in range(8)
                                    )
                                    +
                                    background * (
                                            l_size - 8 *
                                            (
                                                space_size * 2 + wid))
                            )
                        )
                        * color_block_height +  # rows of pixels for one row
                        (
                            # white stripe y
                            (
                                background * space_size +  # offset x
                                white
                                * wid +  # white stripe
                                background * space_size
                            ) * 8 +  # offset x
                            background * (
                                l_size - 8 * (space_size * 2 + wid)
                            )  # fill to full line
                            ) +
                        background * (l_size * space_size)  # offset y
                ))
        data[:] = (
                bytes(sequence)
                + background * l_size + b'\x00' * len(data))[:leng]
        self.segment_height = self.colors_block.height // 32
        self.segment_width = max(
            1, int((width - 8.5 * self.segment_height) // 8) - 2)

    def put_palettes_descriptions(self) -> None:
        for name, multiplier in (
                self.palettes_descriptions_with_height_multiplier.items()
        ):
            self.m.mlx_string_put(
                self.mlx, self.win.ptr, self.win.width // 64 * 57,
                self.win.height // 64 * multiplier, 0xFFFFFFFF, name)

    def show_menu(self) -> None:
        # for multiplier in self.color_blocks_height_multipliers:
        #     self.m.mlx_put_image_to_window(
        #     self.mlx, self.win.ptr, self.colors_block.ptr,
        #     self.win.width // 64 * 60,
        #     self.win.height // 64 * multiplier)
        self.set_images_and_position()
        self.m.mlx_put_image_to_window(
            self.mlx, self.win.ptr, self.strings_background.ptr,
            self.win.width // 64 * 56, self.win.height // 64 * 56)
        self.set_menu_data()

        for name, position in self.menu_data.items():
            self.m.mlx_string_put(
                self.mlx, self.win.ptr,
                position['width'], position['height'],
                0xFFFFFFFF, name)
        for img, position in self.images_with_height_and_width.items():
            if self.theme_changed() or img != self.save[0]:
                self.m.mlx_put_image_to_window(
                    self.mlx, self.win.ptr, img,
                    position['width'], position['height'])
        # self.put_palettes_descriptions()

    def theme_changed(self) -> bool:
        for a, b in zip(
                self.themes[self.theme_idx].values(), self.colors.values()
        ):
            if a[:3] != b[:3]:
                return True
        return False

    def open_window(self, generator: MazeGenerator, seed: int) -> None:
        self.gen = generator
        self.seed = seed
        self.show_menu()
        self.vars = {
            'm': self.m,
            'mlx': self.mlx,
            'win': self.win
        }
        self.m.mlx_key_hook(self.win.ptr, self.key_hook, self.vars)
        self.m.mlx_mouse_hook(self.win.ptr, self.mouse_hook, self.vars)
        self.generate_new_maze(False)
        self.m.mlx_loop_hook(self.mlx, self.draw_maze, self.vars)
        self.m.mlx_loop(self.mlx)

    def mouse_hook(self, button: int, x: int, y: int, vars: dict) -> None:
        if self.cursor_over_slider(x, y):
            result = ((x - self.win.width // 128 * 119)
                      - self.corrector.width//2)
            result = result * 100 // self.slider.width
            result = result if result <= 100 else 100
            self.slider_x = result if result >= 1 else 1
            self.gen.visualisation_tempo = self.slider_x
        if self.theme_changed() and self.cursor_over_save_icon(x, y):
            self.themes[self.theme_idx] = copy(self.colors)
        if self.cursor_over_refresh_icon(x, y):
            self.generate_new_maze(False)
        if self.cursor_over_play_or_pause_icon(x, y):
            self.paused = not self.paused
        if self.cursor_over_freeze_icon(x, y):
            self.frozen = not self.frozen

        x_start = self.win.width // 64 * 60 + self.segment_height
        x_end = x_start + self.segment_width * 8 + self.segment_height * 16
        block_width = (x_end - x_start)/8
        if x_start < x <= x_end:
            for name, reach_y in self.blocks.items():
                if (
                        reach_y['start'] + self.segment_height / 2
                        <= y <= reach_y['end']):

                    y_rel = y - reach_y['start']
                    x_rel = x - x_start

                    if (
                            0 <= y_rel < block_width * 8
                            and 0 <= x_rel < block_width * 8
                    ):
                        row = int(y_rel // block_width)
                        col = int(x_rel // block_width)
                        self.colors[name] = transparent(
                            self.palette[row*8+col], self.transparency)
        self.time = datetime.now()
        self.maze_draw = True
        self.show_menu()

    def key_hook(self, keycode: int, vars: dict) -> None:
        m: Mlx = vars['m']
        win: Window = vars['win']
        mlx = vars['mlx']

        if self.is_key('esc', keycode):
            m.mlx_destroy_window(mlx, win.ptr)
            m.mlx_loop_exit(mlx)

        if self.is_key('b', keycode):
            self.brick_visible = not self.brick_visible

        if self.is_key('l', keycode):
            if self.brick.bricks_in_row > 1 and self.brick.brick_w > 1:
                self.brick.bricks_in_row -= 1

        if self.is_key('j', keycode):
            if self.brick.brick_w > 2:
                self.brick.bricks_in_row += 1

        if self.is_key('i', keycode):
            if self.brick.rows_in_block > 2:
                self.brick.rows_in_block -= 1

        if self.is_key('k', keycode):
            self.brick.rows_in_block += 1

        if self.is_key('numpad-8', keycode):
            self.brick.mortar_thickness_x += 1

        if self.is_key('numpad-2', keycode):
            if self.brick.mortar_thickness_x > 0:
                self.brick.mortar_thickness_x -= 1

        if self.is_key('numpad-6', keycode):
            self.brick.mortar_thickness_y += 1

        if self.is_key('numpad-4', keycode):
            if self.brick.mortar_thickness_y > 0:
                self.brick.mortar_thickness_y -= 1

        if self.is_key('w', keycode):
            self.increase_transparency()

        if self.is_key('s', keycode):
            self.decrease_transparency()

        if self.is_key('d', keycode):
            if self.theme_idx < 30:
                self.theme_idx += 1
            self.set_theme()

        if self.is_key('a', keycode):
            if self.theme_idx > 1:
                self.theme_idx -= 1
            self.set_theme()

        if self.is_key('n', keycode):
            self.generate_new_maze(True)

        if self.is_key('numpad-plus', keycode):
            self.img.thickness += 1

        if self.is_key('numpad-minus', keycode):
            if (self.img.thickness > 1):
                self.img.thickness -= 1

        if self.is_key('left-arrow', keycode) and self.maze.width > 4:
            self.m.mlx_put_image_to_window(
                self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)

            self.maze.width -= 1
            self.generate_new_maze(True)

        if self.is_key('up-arrow', keycode) and self.maze.height > 4:
            self.m.mlx_put_image_to_window(
                self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)

            self.maze.height -= 1
            self.generate_new_maze(True)

        if self.is_key('right-arrow', keycode):
            self.m.mlx_put_image_to_window(
                self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)

            self.maze.width += 1
            self.generate_new_maze(True)

        if self.is_key('down-arrow', keycode):
            self.m.mlx_put_image_to_window(
                self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)
            self.maze.height += 1
            self.generate_new_maze(True)

        self.brick.size = self.img.scale
        self.brick.texture_create()
        self.time = datetime.now()
        self.maze_draw = True
        self.set_images_and_position()

    def is_key(self, key: str, code: int) -> bool:
        return self.keys[key] == code

    def decrease_transparency(self) -> None:
        if self.transparency > 5:
            self.transparency -= 5
        elif self.transparency > 0:
            self.transparency -= 1
        self.create_colors()

    def increase_transparency(self) -> None:
        if self.transparency < 5:
            self.transparency += 1
        elif self.transparency > 249:
            self.transparency = 255
        elif self.transparency < 255:
            self.transparency += 5
        self.create_colors()

    def set_theme(self) -> None:
        self.colors = copy(self.themes[self.theme_idx])
        self.create_colors()

    def generate_new_maze(self, new_seed: bool) -> None:
        self.m.mlx_put_image_to_window(
            self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)
        self.seed = randint(0, 9999) if new_seed else self.seed
        self.generator = (
            self.gen.create_maze(self.maze, self.seed, self.player))
        self.finder = self.path_finder.find_path(self.maze)
        self.path_img = Image(self.m, self.mlx, self.win, self.maze)
        self.final_path_img = Image(self.m, self.mlx, self.win, self.maze)
        thickness = self.img.thickness
        self.img = Image(self.m, self.mlx, self.win, self.maze)
        self.img.thickness = thickness
        if not self.path_finding:
            self.maze_draw = True

    def create_colors(self) -> None:
        for color in self.colors:
            if color != 'name':
                self.colors[color] = (
                    transparent(self.colors[color], self.transparency))

    def cursor_over_slider(self, x: int, y: int) -> bool:
        return (self.win.width // 128 * 119 < x <
                self.win.width // 128 * 119 + self.slider.width + 10
                and self.win.height // 64 * 59 + self.slider.height < y <
                self.win.height // 64 * 59 + self.corrector.height +
                self.slider.height)

    def cursor_over_save_icon(self, x: int, y: int) -> bool:
        return (self.win.width // 64 * 63 < x <
                self.win.width // 64 * 63 + self.save[1]
                and self.win.height // 64 * 57 < y <
                self.win.height // 64 * 57 +
                self.save[2])

    def cursor_over_refresh_icon(self, x: int, y: int) -> bool:
        return (self.win.width // 64 * 61 < x <
                self.win.width // 64 * 61 + self.refresh[1]
                and self.win.height // 64 * 57 < y <
                self.win.height // 64 * 57 +
                self.refresh[2])

    def cursor_over_play_or_pause_icon(self, x: int, y: int) -> bool:
        return (self.win.width // 64 * 63 < x <
                self.win.width // 64 * 63 + self.play[1]
                and self.win.height // 64 * 59 < y <
                self.win.height // 64 * 59 +
                self.play[2])

    def cursor_over_freeze_icon(self, x: int, y: int) -> bool:
        return (
                self.win.width // 64 * 63 < x <
                self.win.width // 64 * 63 + self.freeze[1]
                and self.win.height // 64 * 61 < y <
                self.win.height // 64 * 61 +
                self.freeze[2])

    def get_icon_size(self) -> int:
        size = (
            10 if self.img.scale < 15 else
            15 if self.img.scale < 20 else
            20 if self.img.scale < 30 else
            30 if self.img.scale < 40 else
            40 if self.img.scale < 60 else
            60 if self.img.scale < 80 else
            80 if self.img.scale < 100 else
            100
        )
        return size
