from copy import copy
from datetime import datetime
from random import randint
from enums import Direction
from mlx import Mlx
from objects import Image, Maze, Window, Brick
from colors import colors
from .Draw import Draw


class MazeVisualizer:

    def __init__(
            self, maze, 
            enter: tuple[int, int], exit: tuple[int, int]):
        self.start_time = datetime.now()

        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        self.win = Window(self.m, self.mlx, "A-Maze-ing")
        self.draw = Draw()
        self.path = list()
        self.list = list()
        self.enter = enter
        self.exit = exit
        self.maze = maze
        self.x = -1
        self.y = -2
        self.transparency = 1
        self.menu_showed = False
        self.brick_visible = False
        self.paused = False
        self.freezed = False
        self.player = True
        self.path_finding = False

        self.slider_x = 0
        self.theme_idx = 1

        self.finder = maze.finder.find_path(maze)
        self.themes = colors.get_themes(self.transparency)
        self.colors = copy(self.themes[self.theme_idx])
        self.palette = colors.get_palette()

        self.img = Image(self.m, self.mlx, self.win, self.maze)
        self.path_img = Image(self.m, self.mlx, self.win, self.maze)
        self.final_path_img = Image(self.m, self.mlx, self.win, self.maze)
        self.offset = (self.img.height - self.maze.height * self.img.scale) // 2
        self.lines = {
            'Snake': self.colors['Snake'] * self.img.scale,
            'Block not found': self.colors['Block not found'] * (self.img.scale - 1),
            'Block found': self.colors['Block found'] * (self.img.scale - self.img.thickness),
            '42': self.colors['42'] * (self.img.scale - self.img.thickness),
            'line_x': self.colors['Grid 1'] * (self.img.scale + 2 * self.img.thickness),
            'line_y': self.colors['Grid 1'] * self.img.thickness
        }
        self.load_images()
        self.create_elements()
        self.create_background_images()


    def create_background_images(self):
        self.background_img = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 8 * 7, self.win.height)
        self.background_img_data = self.m.mlx_get_data_addr(self.background_img.ptr)[0]
        self.background_img_data[:] = self.darken(self.colors['Background'], 0.6) * (len(self.background_img_data) // 4)
        self.menu_img = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 8, self.win.height)
        self.menu_img_data = self.m.mlx_get_data_addr(self.menu_img.ptr)[0]
        self.menu_img_data[:] = self.darken(self.colors['Background'], 0.6) * (len(self.menu_img_data) // 4)
        self.strings_background = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 64 * 4,
                                        self.win.height // 64 * 5)
        self.strings_background_data = self.m.mlx_get_data_addr(self.strings_background.ptr)[0]


    def create_elements(self):
        self.brick = Brick(self.img.scale, self.transparency, self.colors['Block found'], bytes([30, 30, 30, 30]))
        self.corrector = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 400, self.win.width // 100)
        self.corrector_data = self.m.mlx_get_data_addr(self.corrector.ptr)[0]
        self.corrector_data[:] = bytes([120, 120, 120, 255]) * (len(self.corrector_data) // 4)
        self.slider = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 20, self.win.width // 400)
        self.slider_data = self.m.mlx_get_data_addr(self.slider.ptr)[0]
        self.slider_data[:] = bytes([255, 255, 255, 255]) * (len(self.slider_data) // 4)
        self.colors_block = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 16,
                                  self.win.height // 64 * 7)
        self.colors_block_data = self.m.mlx_get_data_addr(self.colors_block.ptr)[0]
        self.create_color_palette()
        
    def load_images(self):
        self.icon_size = self.get_icon_size()
        self.save = self.m.mlx_png_file_to_image(self.mlx, "pictures/save.png")
        self.play = self.m.mlx_png_file_to_image(self.mlx, "pictures/play.png")
        self.pause = self.m.mlx_png_file_to_image(self.mlx, "pictures/pause.png")
        self.freeze = self.m.mlx_png_file_to_image(self.mlx, "pictures/freeze.png")
        self.frozen = self.m.mlx_png_file_to_image(self.mlx, "pictures/freezed.png")
        self.start = self.m.mlx_png_file_to_image(self.mlx, f"pictures/start{self.icon_size}.png")
        self.finish = self.m.mlx_png_file_to_image(self.mlx, f"pictures/finish{self.icon_size}.png")
        self.refresh = self.m.mlx_png_file_to_image(self.mlx, "pictures/refresh.png")
    
    def get_icon_size(self):
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
    
    def make_lines(self):
        self.lines = {
            'Snake': self.colors['Snake'] * self.img.scale,
            'Block not found': self.colors['Block not found'] * (self.img.scale - 1),
            'Block found': self.colors['Block found'] * (self.img.scale - self.img.thickness),
            '42': self.colors['42'] * (self.img.scale - self.img.thickness),
            'line_x': self.colors['Grid 1'] * (self.img.scale + 2 * self.img.thickness - 1),
            'line_y': self.colors['Grid 1'] * self.img.thickness
        }

    def draw_maze(self, vars):
        if not self.bool or self.freezed:
            if self.path_finding:
                self.draw_path()
            return
        try:
            diff = (datetime.now() - self.start_time).total_seconds()*2
            transparency = int((diff*diff))
            if 0 < transparency < 26:
                if self.transparency != transparency:
                    self.transparency = transparency
                    for color in self.colors:
                        if color != 'name':
                            self.colors[color] = self.transparent(self.colors[color], self.transparency)
                    self.put_strings()
            else:
                if not self.menu_showed:
                    self.show_menu()
                    self.put_strings()
                    self.menu_showed = True
            if not self.paused:
                self.found = next(self.generator)
            self.background_img_data[:] = self.darken(self.colors['Background'], 0.6) * (len(self.background_img_data) // 4)
            self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)
            offset = (self.img.scale - self.start[1])//2
            offset_y = (self.img.height - self.maze.height*self.img.scale)//2
            self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.start[0], self.maze.start[0] * self.img.scale + offset, self.maze.start[1] * self.img.scale + offset + offset_y)
            self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.finish[0], self.maze.end[0] * self.img.scale + offset, self.maze.end[1] * self.img.scale + offset + offset_y)
            self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win, self.found, self.colors, self.darken, self.brick_visible, self.brick, self.lines, self.offset)
            self.time = datetime.now()

        except StopIteration:
            if not self.path_finding:
                self.path_finding = True
            if (datetime.now() - self.time).total_seconds() < 3:
                self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win, self.found,
                                    self.colors, self.darken, self.brick_visible, self.brick, self.lines, self.offset)
                if self.path_finding:
                    for color in self.colors:
                        if color != 'name':
                            self.colors[color] = self.transparent(self.colors[color], self.transparency)
                    self.bool = False
                    self.draw_path()

    def draw_path(self):
        try:
            self.path = next(self.finder)
            self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.img.ptr, 0, self.offset)

            self.draw.draw_path(self.m, self.mlx, self.maze, self.path_img, self.final_path_img, self.win, self.path, self.colors, self.lines, self.offset)
        except StopIteration as e:
            self.path_finding = False
            self.bool = False

    def create_color_palette(self):
        data = self.colors_block_data
        leng = len(data)
        height = self.colors_block.height
        width = self.colors_block.width
        line_size = leng // height
        space_size = 2
        color_block_height = height//10 - 3
        l_size = line_size // 4
        wid = (l_size - 16 * space_size) // 8
        sequence = bytes()
        background = bytes([0, 0, 0, 0])
        for i in range (8):
            sequence = sequence + ((
                        bytes([0,0,0,0]) * (l_size * space_size) +  #odstep y
                        (
                            #biała linia y
                                (background * space_size +  # odstęp x
                                 bytes([255, 255, 255, 255]) * wid +  # bialy pasek
                                 background * space_size) * 8 +  # odstep x
                                (background * (l_size - 8 * (space_size * 2 + wid))) #dopelłnij
                        )
                        +
                        (
                            #wypełnienie
                            (
                                    b''.join(
                                        background * space_size +
                                        bytes([255, 255, 255, 255]) * 1 +
                                        self.palette[i * 8 + j] * (wid - 2) +
                                        bytes([255, 255, 255, 255]) * 1 +
                                        background * space_size
                                        for j in range(8)
                                    )
                                    +
                                    background * (l_size - 8 * (space_size * 2 + wid))
                            )
                        )
                        * color_block_height +  #ilosc multiplikacji segmentu
                        (
                            # biała linia y
                                (
                                background * space_size +  # odstęp x
                                bytes([255, 255, 255, 255]) * wid +  # bialy pasek
                                background * space_size) * 8 +  # odstep x
                                background * (l_size - 8 * (space_size * 2 + wid)) #dopełnij
                        ) +
                        background * (l_size * space_size) #odstep y
                ))
        data[:] = ( sequence
                + background * l_size + b'\x00' * len(data)
            )[:leng]
        self.segment_height = self.colors_block.height // 32
        self.segment_width = max(1, int((width - 8.5 * self.segment_height) // 8) - 2)


    def darken(self, color: bytes, factor: float) -> bytes:
        r, g, b, a = color
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return bytes([r, g, b, a])

    def transparent(self, color: bytes, level: int) -> bytes:
        r, g, b, a = color
        return bytes([r, g, b, level])

    def restart(self):
        self.background_img_data[:] = self.darken(self.colors['Background'], 0.6) * (
                    len(self.background_img_data) // 4)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)
    def show_menu(self):
        self.menu_img_data[:] = self.darken((self.colors['Background'][:3] + bytes([255])), 0.6) * (
                    len(self.menu_img_data) // 4)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.menu_img.ptr, self.win.width // 8 * 7, 0)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60,
                                       self.win.height // 64)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60,
                                       self.win.height // 64 * 9)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60,
                                       self.win.height // 64 * 17)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60,
                                       self.win.height // 64 * 25)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60,
                                       self.win.height // 64 * 33)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60,
                                       self.win.height // 64 * 41)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.colors_block.ptr, self.win.width // 64 * 60,
                                       self.win.height // 64 * 49)
        # self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64, 0xFFFFFFFF,
        #                       "42")
        # self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 9, 0xFFFFFFFF,
        #                       "Gr 1")
        # self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 17, 0xFFFFFFFF,
        #                       "Gr 2")
        # self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 25, 0xFFFFFFFF,
        #                       "B 1")
        # self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 33, 0xFFFFFFFF,
        #                       "B 2")
        # self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 41, 0xFFFFFFFF,
        #                       "S")
        # self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 49, 0xFFFFFFFF,
        #                       "Bckg")


    def put_strings(self):
        self.show_menu()
        #self.strings_background_data[:] = self.darken((self.colors['Background'][:3] + bytes([255])), 0.6) * (len(self.strings_background_data) // 4)
        #self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.strings_background.ptr, self.win.width // 64 * 57, self.win.height // 64 * 57)
        # self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 58, 0xFFFFFFFF,
        #                         f"S = {self.seed}")
        # self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 59, 0xFFFFFFFF,
        #                       "X = " + str(self.maze.width) + "(l/ri)")
        # self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 56, 0xFFFFFFFF,
        #                       "Y = " + str(self.maze.height) + "(up/dn)")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 61, 0xFFFFFFFF,
                              "T = " + str(self.transparency) + "(w/s)")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 62, 0xFFFFFFFF,
                              "Thm = " + self.themes[self.theme_idx]['name'] + "(a/d)")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 63, 0xFFFFFFFF,
                              "Th = " + str(self.img.thickness) + "(+/-)")
        if self.theme_changed():
            self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.save[0], self.win.width // 64 * 63, self.win.height // 64 * 57)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.refresh[0], self.win.width // 64 * 61, self.win.height // 64 * 57)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.play[0] if self.paused else self.pause[0], self.win.width // 64 * 63,
                                       self.win.height // 64 * 59)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.frozen[0] if self.freezed else self.freeze[0], self.win.width // 64 * 63, self.win.height // 64 * 61)
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width * 251 // 256, self.win.height * 231 // 256, 0xFFFFFFFF, f"{self.slider_x}")
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.slider.ptr, self.win.width // 128 * 119, self.win.height // 64 * 59 + self.play[1]//2)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.corrector.ptr, self.slider_x * self.slider.width // 100 + self.win.width // 128 * 119, self.win.height // 64 * 59 + self.play[1]//2 - self.corrector.height//2 + self.slider.height//2)

    def theme_changed(self):
        for a, b in zip(self.themes[self.theme_idx].values(), self.colors.values()):
            if a[:3] != b[:3]:
                return True
        return False
    def open_window(self, generator, seed):
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)
        self.gen = generator
        self.seed = seed
        self.show_menu()
        self.put_strings()

        self.vars = {
            'm': self.m,
            'mlx': self.mlx,
            'img': self.img,
            'win': self.win,
            'maze': self.maze,
            'draw': self.draw.draw_maze,
            'generator': generator,
        }
        self.m.mlx_key_hook(self.win.ptr, self.key_hook, self.vars)
        self.m.mlx_mouse_hook(self.win.ptr, self.mouse_hook, self.vars)
        self.bool = True
        self.m.mlx_loop_hook(self.mlx, self.draw_maze, self.vars)
        self.generator = self.gen.create_maze(self.maze, seed, self.player)
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

    def cursor_over_slider(self, x: int, y: int) -> bool:
        return self.win.width // 128 * 119 < x < self.win.width // 128 * 119 + self.slider.width + 10 \
                and self.win.height // 64 * 59 + self.slider.height < y < self.win.height // 64 * 59 + self.corrector.height + self.slider.height

    def cursor_over_save_icon(self, x: int, y: int) -> bool:
        return self.win.width // 64 * 63 < x < self.win.width // 64 * 63 + self.save[1] and self.win.height // 64 * 57 < y < self.win.height // 64 * 57 + \
                    self.save[2]

    def cursor_over_refresh_icon(self, x: int, y: int) -> bool:
        return self.win.width // 64 * 61 < x < self.win.width // 64 * 61 + self.refresh[1] and self.win.height // 64 * 57 < y < self.win.height // 64 * 57 + \
                self.refresh[2]

    def cursor_over_play_or_pause_icon(self, x: int, y: int) -> bool:
        return self.win.width // 64 * 63 < x < self.win.width // 64 * 63 + self.play[1] and self.win.height // 64 * 59 < y < self.win.height // 64 * 59 + \
                self.play[2]

    def cursor_over_freeze_icon(self, x: int, y: int) -> bool:
        return self.win.width // 64 * 63 < x < self.win.width // 64 * 63 + self.freeze[1] and self.win.height // 64 * 61 < y < self.win.height // 64 * 61 + \
                self.freeze[2]

    def mouse_hook(self, cos, x, y, args):
        if self.cursor_over_slider(x, y):
            result = (x - self.win.width // 128 * 119) - self.corrector.width//2
            result = result * 100 // self.slider.width
            result = result if result <= 100 else 100
            self.slider_x = result if result >=0 else 0

        blocks = {
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
        x_start = self.win.width // 64 * 60 + self.segment_height
        x_end = x_start + self.segment_width * 8 + self.segment_height * 16
        block_width = (x_end - x_start)/8
        if self.theme_changed():
            if self.cursor_over_save_icon(x, y):
                self.themes[self.theme_idx] = copy(self.colors)
        if self.cursor_over_refresh_icon(x, y):
            self.player = not self.player
            self.generator = self.gen.create_maze(self.maze, self.seed, self.player)
        if self.cursor_over_play_or_pause_icon(x, y):
            self.paused = not self.paused
        if self.cursor_over_freeze_icon(x, y):
            self.freezed = not self.freezed
        if x_start < x <= x_end:
            for name, yy in blocks.items():
                if yy['start'] + self.segment_height / 2 <= y <= yy['end']:

                    y_rel = y - yy['start']
                    x_rel = x - x_start

                    if 0 <= y_rel < block_width * 8 and 0 <= x_rel < block_width * 8:
                        row = int(y_rel // block_width)
                        col = int(x_rel // block_width)
                        self.colors[name] = self.transparent(self.palette[row*8+col], self.transparency)
                        if name == 'Background':
                            #self.restart()

                            self.show_menu()
        self.time = datetime.now()
        self.bool = True
        self.make_lines()
        self.put_strings()


    def key_hook(self, keycode, vars):
        img: Image = vars['img']
        maze: Maze = vars['maze']
        win: Window = vars['win']
        mlx = vars['mlx']
        draw: callable = vars['draw']
        m: Mlx = vars['m']
        if keycode == 98:
            self.brick_visible = not self.brick_visible
        if keycode == 108:
            if self.brick.bricks_in_row > 1 and self.brick.brick_w > 1:
                self.brick.bricks_in_row -=1
        if keycode == 106:
            if self.brick.brick_w > 2:
                self.brick.bricks_in_row +=1
        if keycode == 105:
            if self.brick.rows_in_block > 2:
                self.brick.rows_in_block -=1
        if keycode == 107:
            self.brick.rows_in_block +=1
        if keycode == 65431:
            self.brick.mortar_thickness_x+=1
        if keycode == 65433:
            if self.brick.mortar_thickness_x > 0:
                self.brick.mortar_thickness_x -= 1
        if keycode == 65432:
            self.brick.mortar_thickness_y+=1
        if keycode == 65430:
            if self.brick.mortar_thickness_y > 0:
                self.brick.mortar_thickness_y -= 1
        if keycode == 119:
            if self.transparency < 5:
                self.transparency += 1
            elif self.transparency < 255:
                self.transparency +=5
            for color in self.colors:
                if color != 'name':
                    self.colors[color] = self.transparent(self.colors[color], self.transparency)
            self.put_strings()

        if keycode == 115:
            if self.transparency > 5:
                self.transparency -= 5
            elif self.transparency > 0:
                self.transparency -= 1
            for color in self.colors:
                if color != 'name':
                    self.colors[color] = self.transparent(self.colors[color], self.transparency)
            self.put_strings()

        if keycode == 100:
            if self.theme_idx < 30:
                self.theme_idx += 1
                self.colors = copy(self.themes[self.theme_idx])
                for color in self.colors:
                    if color != 'name':
                        self.colors[color] = self.transparent(self.colors[color], self.transparency)
                self.show_menu()
                self.put_strings()
        if keycode == 97:
            if self.theme_idx >1:
                self.theme_idx -= 1
                self.colors = copy(self.themes[self.theme_idx])
                for color in self.colors:
                    if color != 'name':
                        self.colors[color] = self.transparent(self.colors[color], self.transparency)
                self.show_menu()
                self.put_strings()
        if keycode == 110:
            self.seed = randint(0,9999)
            self.generator = self.gen.create_maze(self.maze, self.seed, self.player)
            #self.start_time = datetime.now()
            #self.put_strings()
            self.bool = True
        if keycode == 65451:
            self.img.thickness += 1
        self.put_strings()

        if keycode == 65453:
            if (self.img.thickness > 1):
                self.img.thickness -= 1
                self.put_strings()

        if keycode == 65361 and self.maze.width > 4:
            self.maze.width -= 1
            self.seed = randint(0,9999)
            self.generator = self.gen.create_maze(self.maze, self.seed, self.player)
            self.restart()
            self.show_menu()
            self.put_strings()
            thickness = self.img.thickness
            self.img = Image(self.m, self.mlx, self.win, self.maze)
            self.img.thickness = thickness
            self.bool = True
        if keycode == 65362 and self.maze.height > 4:
            self.maze.height -= 1
            self.seed = randint(0,9999)
            self.generator = self.gen.create_maze(self.maze, self.seed, self.player)
            self.restart()
            self.show_menu()

            self.put_strings()
            thickness = self.img.thickness
            self.img = Image(self.m, self.mlx, self.win, self.maze)
            self.img.thickness = thickness
            self.bool = True
        if keycode == 65363:
            self.maze.width += 1
            self.seed = randint(0,9999)
            self.generator = self.gen.create_maze(self.maze, self.seed, self.player)
            self.restart()
            self.show_menu()

            self.put_strings()
            thickness = self.img.thickness
            self.img = Image(self.m, self.mlx, self.win, self.maze)
            self.img.thickness = thickness
            self.bool = True
        if keycode == 65364:
            self.maze.height += 1
            self.seed = randint(0,9999)
            self.generator = self.gen.create_maze(self.maze, self.seed, self.player)
            self.restart()
            self.show_menu()

            self.put_strings()
            thickness = self.img.thickness
            self.img = Image(self.m, self.mlx, self.win, self.maze)
            self.img.thickness = thickness
            self.bool = True
        self.brick.size = self.img.scale
        self.brick.texture_create()
        self.time = datetime.now()
        self.make_lines()
        self.bool = True
        if keycode == 65307:
            m.mlx_destroy_window(mlx, win.ptr)
            m.mlx_loop_exit(mlx)


