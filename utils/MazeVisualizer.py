from copy import copy

from mlx import Mlx
from objects import Image, Maze, Window, Brick
from enums import Direction
from .Draw import Draw
from algorithms.MazeGenerator import MazeGenerator
from random import randint
from time import sleep
from datetime import datetime
import math


class MazeVisualizer:

    def __init__(
            self, maze, 
            enter: tuple[int, int], exit: tuple[int, int]):
        self.path = list()
        self.list = list()
        self.enter = enter
        self.exit = exit
        self.maze = maze
        self.x = -1
        self.y = -2
        self.start_time = datetime.now()
        self.transparency = 1
        self.menu_showed = False
        self.brick_visible = False
        self.finder = maze.finder.find_path(maze)
        self.themes = {
            1: {
                'name': 'dgajowni',
                '42': bytes([0, 0, 255, self.transparency]),
                'Grid 1': bytes([240, 240, 240, self.transparency]),
                'Grid 2': bytes([5, 10, 5, self.transparency]),
                'Block found': bytes([30, 30, 30, self.transparency]),
                'Block not found': bytes([0, 0, 0, self.transparency]),
                'Snake': bytes([0, 255, 255, self.transparency]),
                'Background': bytes([0, 0, 0, self.transparency]),
            },

            2: {
                'name': 'classic',
                '42': bytes([255, 0, 0, self.transparency]),
                'Grid 1': bytes([200, 200, 200, self.transparency]),
                'Grid 2': bytes([120, 120, 120, self.transparency]),
                'Block found': bytes([0, 200, 0, self.transparency]),
                'Block not found': bytes([50, 50, 50, self.transparency]),
                'Snake': bytes([0, 255, 0, self.transparency]),
                'Background': bytes([0, 0, 0, self.transparency]),
            },

            3: {
                'name': 'neon',
                '42': bytes([255, 0, 255, self.transparency]),
                'Grid 1': bytes([0, 255, 255, self.transparency]),
                'Grid 2': bytes([20, 20, 20, self.transparency]),
                'Block found': bytes([255, 255, 0, self.transparency]),
                'Block not found': bytes([255, 0, 0, self.transparency]),
                'Snake': bytes([0, 255, 128, self.transparency]),
                'Background': bytes([0, 0, 0, self.transparency]),
            },

            4: {
                'name': 'forest',
                '42': bytes([34, 139, 34, self.transparency]),
                'Grid 1': bytes([85, 107, 47, self.transparency]),
                'Grid 2': bytes([0, 50, 0, self.transparency]),
                'Block found': bytes([46, 139, 87, self.transparency]),
                'Block not found': bytes([10, 30, 10, self.transparency]),
                'Snake': bytes([0, 255, 127, self.transparency]),
                'Background': bytes([5, 20, 5, self.transparency]),
            },

            5: {
                'name': 'desert',
                '42': bytes([210, 180, 140, self.transparency]),
                'Grid 1': bytes([238, 214, 175, self.transparency]),
                'Grid 2': bytes([189, 154, 122, self.transparency]),
                'Block found': bytes([160, 82, 45, self.transparency]),
                'Block not found': bytes([120, 60, 30, self.transparency]),
                'Snake': bytes([255, 215, 0, self.transparency]),
                'Background': bytes([80, 50, 20, self.transparency]),
            },

            6: {
                'name': 'ice',
                '42': bytes([180, 220, 255, self.transparency]),
                'Grid 1': bytes([220, 240, 255, self.transparency]),
                'Grid 2': bytes([120, 170, 200, self.transparency]),
                'Block found': bytes([100, 140, 180, self.transparency]),
                'Block not found': bytes([50, 80, 120, self.transparency]),
                'Snake': bytes([0, 255, 255, self.transparency]),
                'Background': bytes([10, 30, 60, self.transparency]),
            },

            7: {
                'name': 'mono',
                '42': bytes([255, 255, 255, self.transparency]),
                'Grid 1': bytes([200, 200, 200, self.transparency]),
                'Grid 2': bytes([150, 150, 150, self.transparency]),
                'Block found': bytes([100, 100, 100, self.transparency]),
                'Block not found': bytes([50, 50, 50, self.transparency]),
                'Snake': bytes([220, 220, 220, self.transparency]),
                'Background': bytes([0, 0, 0, self.transparency]),
            },

            8: {
                'name': 'retro',
                '42': bytes([255, 128, 0, self.transparency]),
                'Grid 1': bytes([255, 255, 0, self.transparency]),
                'Grid 2': bytes([0, 128, 128, self.transparency]),
                'Block found': bytes([128, 0, 128, self.transparency]),
                'Block not found': bytes([0, 0, 128, self.transparency]),
                'Snake': bytes([0, 255, 0, self.transparency]),
                'Background': bytes([0, 0, 0, self.transparency]),
            },
            9: {
                'name': 'neon_pink',
                '42': bytes([255, 0, 150, self.transparency]),
                'Grid 1': bytes([40, 40, 40, self.transparency]),
                'Grid 2': bytes([20, 20, 20, self.transparency]),
                'Block found': bytes([255, 0, 200, self.transparency]),
                'Block not found': bytes([10, 10, 10, self.transparency]),
                'Snake': bytes([0, 255, 200, self.transparency]),
                'Background': bytes([0, 0, 0, self.transparency]),
            },

            10: {
                'name': 'toxic_green',
                '42': bytes([0, 255, 0, self.transparency]),
                'Grid 1': bytes([30, 60, 30, self.transparency]),
                'Grid 2': bytes([10, 30, 10, self.transparency]),
                'Block found': bytes([0, 200, 0, self.transparency]),
                'Block not found': bytes([0, 50, 0, self.transparency]),
                'Snake': bytes([150, 255, 0, self.transparency]),
                'Background': bytes([0, 10, 0, self.transparency]),
            },

            11: {
                'name': 'lava',
                '42': bytes([255, 80, 0, self.transparency]),
                'Grid 1': bytes([80, 20, 0, self.transparency]),
                'Grid 2': bytes([40, 10, 0, self.transparency]),
                'Block found': bytes([200, 40, 0, self.transparency]),
                'Block not found': bytes([30, 10, 0, self.transparency]),
                'Snake': bytes([255, 200, 0, self.transparency]),
                'Background': bytes([10, 0, 0, self.transparency]),
            },

            12: {
                'name': 'cyber_blue',
                '42': bytes([0, 150, 255, self.transparency]),
                'Grid 1': bytes([20, 40, 60, self.transparency]),
                'Grid 2': bytes([10, 20, 30, self.transparency]),
                'Block found': bytes([0, 100, 200, self.transparency]),
                'Block not found': bytes([0, 20, 40, self.transparency]),
                'Snake': bytes([0, 255, 255, self.transparency]),
                'Background': bytes([0, 0, 20, self.transparency]),
            },

            13: {
                'name': 'matrix',
                '42': bytes([0, 255, 70, self.transparency]),
                'Grid 1': bytes([0, 60, 20, self.transparency]),
                'Grid 2': bytes([0, 30, 10, self.transparency]),
                'Block found': bytes([0, 180, 50, self.transparency]),
                'Block not found': bytes([0, 20, 10, self.transparency]),
                'Snake': bytes([120, 255, 120, self.transparency]),
                'Background': bytes([0, 5, 0, self.transparency]),
            },

            14: {
                'name': 'purple_haze',
                '42': bytes([180, 0, 255, self.transparency]),
                'Grid 1': bytes([60, 0, 80, self.transparency]),
                'Grid 2': bytes([30, 0, 40, self.transparency]),
                'Block found': bytes([140, 0, 200, self.transparency]),
                'Block not found': bytes([20, 0, 30, self.transparency]),
                'Snake': bytes([255, 0, 255, self.transparency]),
                'Background': bytes([5, 0, 10, self.transparency]),
            },

            15: {
                'name': 'sandstorm',
                '42': bytes([210, 180, 120, self.transparency]),
                'Grid 1': bytes([160, 140, 100, self.transparency]),
                'Grid 2': bytes([120, 100, 70, self.transparency]),
                'Block found': bytes([180, 150, 90, self.transparency]),
                'Block not found': bytes([60, 50, 30, self.transparency]),
                'Snake': bytes([255, 220, 150, self.transparency]),
                'Background': bytes([40, 30, 20, self.transparency]),
            },

            16: {
                'name': 'ice_core',
                '42': bytes([180, 240, 255, self.transparency]),
                'Grid 1': bytes([120, 180, 200, self.transparency]),
                'Grid 2': bytes([80, 120, 150, self.transparency]),
                'Block found': bytes([100, 200, 255, self.transparency]),
                'Block not found': bytes([30, 60, 80, self.transparency]),
                'Snake': bytes([0, 255, 255, self.transparency]),
                'Background': bytes([0, 20, 40, self.transparency]),
            },

            17: {
                'name': 'blood',
                '42': bytes([180, 0, 0, self.transparency]),
                'Grid 1': bytes([80, 0, 0, self.transparency]),
                'Grid 2': bytes([40, 0, 0, self.transparency]),
                'Block found': bytes([255, 0, 0, self.transparency]),
                'Block not found': bytes([30, 0, 0, self.transparency]),
                'Snake': bytes([255, 80, 80, self.transparency]),
                'Background': bytes([10, 0, 0, self.transparency]),
            },

            18: {
                'name': 'gold',
                '42': bytes([255, 215, 0, self.transparency]),
                'Grid 1': bytes([120, 100, 20, self.transparency]),
                'Grid 2': bytes([80, 60, 10, self.transparency]),
                'Block found': bytes([200, 170, 0, self.transparency]),
                'Block not found': bytes([40, 30, 5, self.transparency]),
                'Snake': bytes([255, 255, 150, self.transparency]),
                'Background': bytes([20, 15, 0, self.transparency]),
            },

            19: {
                'name': 'terminal',
                '42': bytes([0, 255, 0, self.transparency]),
                'Grid 1': bytes([0, 80, 0, self.transparency]),
                'Grid 2': bytes([0, 40, 0, self.transparency]),
                'Block found': bytes([0, 200, 0, self.transparency]),
                'Block not found': bytes([0, 20, 0, self.transparency]),
                'Snake': bytes([120, 255, 120, self.transparency]),
                'Background': bytes([0, 0, 0, self.transparency]),
            },

            20: {
                'name': 'void',
                '42': bytes([100, 100, 100, self.transparency]),
                'Grid 1': bytes([30, 30, 30, self.transparency]),
                'Grid 2': bytes([15, 15, 15, self.transparency]),
                'Block found': bytes([80, 80, 80, self.transparency]),
                'Block not found': bytes([5, 5, 5, self.transparency]),
                'Snake': bytes([200, 200, 200, self.transparency]),
                'Background': bytes([0, 0, 0, self.transparency]),
            },
            21: {
                'name': 'synthwave',
                '42': bytes([255, 0, 200, self.transparency]),
                'Grid 1': bytes([60, 0, 80, self.transparency]),
                'Grid 2': bytes([30, 0, 40, self.transparency]),
                'Block found': bytes([0, 255, 255, self.transparency]),
                'Block not found': bytes([20, 0, 30, self.transparency]),
                'Snake': bytes([255, 255, 0, self.transparency]),
                'Background': bytes([10, 0, 20, self.transparency]),
            },

            22: {
                'name': 'doom',
                '42': bytes([255, 60, 0, self.transparency]),
                'Grid 1': bytes([80, 20, 0, self.transparency]),
                'Grid 2': bytes([40, 10, 0, self.transparency]),
                'Block found': bytes([200, 0, 0, self.transparency]),
                'Block not found': bytes([20, 0, 0, self.transparency]),
                'Snake': bytes([255, 200, 0, self.transparency]),
                'Background': bytes([5, 0, 0, self.transparency]),
            },

            23: {
                'name': 'mario',
                '42': bytes([255, 0, 0, self.transparency]),
                'Grid 1': bytes([255, 255, 255, self.transparency]),
                'Grid 2': bytes([0, 0, 255, self.transparency]),
                'Block found': bytes([255, 200, 0, self.transparency]),
                'Block not found': bytes([0, 0, 0, self.transparency]),
                'Snake': bytes([0, 200, 0, self.transparency]),
                'Background': bytes([90, 170, 255, self.transparency]),
            },

            24: {
                'name': 'night_city',
                '42': bytes([0, 255, 200, self.transparency]),
                'Grid 1': bytes([20, 20, 40, self.transparency]),
                'Grid 2': bytes([10, 10, 25, self.transparency]),
                'Block found': bytes([255, 0, 150, self.transparency]),
                'Block not found': bytes([30, 0, 20, self.transparency]),
                'Snake': bytes([255, 255, 0, self.transparency]),
                'Background': bytes([5, 5, 15, self.transparency]),
            },

            25: {
                'name': 'outrun',
                '42': bytes([255, 0, 100, self.transparency]),
                'Grid 1': bytes([100, 0, 120, self.transparency]),
                'Grid 2': bytes([50, 0, 60, self.transparency]),
                'Block found': bytes([0, 255, 255, self.transparency]),
                'Block not found': bytes([20, 0, 40, self.transparency]),
                'Snake': bytes([255, 255, 0, self.transparency]),
                'Background': bytes([10, 0, 30, self.transparency]),
            },

            26: {
                'name': 'forest',
                '42': bytes([0, 180, 0, self.transparency]),
                'Grid 1': bytes([40, 80, 40, self.transparency]),
                'Grid 2': bytes([20, 40, 20, self.transparency]),
                'Block found': bytes([0, 120, 0, self.transparency]),
                'Block not found': bytes([10, 20, 10, self.transparency]),
                'Snake': bytes([120, 255, 120, self.transparency]),
                'Background': bytes([5, 10, 5, self.transparency]),
            },

            27: {
                'name': 'desert',
                '42': bytes([255, 200, 120, self.transparency]),
                'Grid 1': bytes([180, 150, 90, self.transparency]),
                'Grid 2': bytes([120, 100, 60, self.transparency]),
                'Block found': bytes([200, 160, 80, self.transparency]),
                'Block not found': bytes([50, 40, 20, self.transparency]),
                'Snake': bytes([255, 230, 170, self.transparency]),
                'Background': bytes([30, 25, 15, self.transparency]),
            },

            28: {
                'name': 'ice',
                '42': bytes([150, 220, 255, self.transparency]),
                'Grid 1': bytes([100, 160, 200, self.transparency]),
                'Grid 2': bytes([60, 120, 160, self.transparency]),
                'Block found': bytes([120, 200, 255, self.transparency]),
                'Block not found': bytes([30, 60, 80, self.transparency]),
                'Snake': bytes([0, 255, 255, self.transparency]),
                'Background': bytes([0, 20, 40, self.transparency]),
            },

            29: {
                'name': 'acid',
                '42': bytes([180, 255, 0, self.transparency]),
                'Grid 1': bytes([80, 120, 0, self.transparency]),
                'Grid 2': bytes([40, 60, 0, self.transparency]),
                'Block found': bytes([0, 255, 0, self.transparency]),
                'Block not found': bytes([20, 30, 0, self.transparency]),
                'Snake': bytes([255, 255, 100, self.transparency]),
                'Background': bytes([10, 15, 0, self.transparency]),
            },

            30: {
                'name': 'grayscale',
                '42': bytes([200, 200, 200, self.transparency]),
                'Grid 1': bytes([120, 120, 120, self.transparency]),
                'Grid 2': bytes([80, 80, 80, self.transparency]),
                'Block found': bytes([160, 160, 160, self.transparency]),
                'Block not found': bytes([30, 30, 30, self.transparency]),
                'Snake': bytes([255, 255, 255, self.transparency]),
                'Background': bytes([0, 0, 0, self.transparency]),
            },

        }
        self.mouse = False
        self.slider_x = 0
        self.paused = False
        self.freezed = False
        self.theme_idx = 1
        self.colors = copy(self.themes[self.theme_idx])
        self.player = True
        self.path_finding = False
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

    def make_lines(self):
        self.lines = {
            'Snake': self.colors['Snake'] * self.img.scale,
            'Block not found': self.colors['Block not found'] * (self.img.scale - 1),
            'Block found': self.colors['Block found'] * (self.img.scale - self.img.thickness),
            '42': self.colors['42'] * (self.img.scale - self.img.thickness),
            'line_x': self.colors['Grid 1'] * (self.img.scale + 2 * self.img.thickness - 1),
            'line_y': self.colors['Grid 1'] * self.img.thickness
        }

    def draw_slow(self, vars):
        if not self.bool or self.freezed:
            if self.path_finding:
                self.path_show()
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
                self.brick.texture_create()
                self.path_finding = True
            if (datetime.now() - self.time).total_seconds() < 3:
                self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win, self.found,
                                    self.colors, self.darken, self.brick_visible, self.brick, self.lines, self.offset)
                if self.path_finding:
                    #self.transparency = 5
                    for color in self.colors:
                        if color != 'name':
                            self.colors[color] = self.transparent(self.colors[color], self.transparency)
                    self.bool = False
                    self.path_show()
                
                
        

    def path_show(self):
        try:
            self.path = next(self.finder)
            self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.img.ptr, 0, self.offset)

            self.draw.draw_path(self.m, self.mlx, self.maze, self.path_img, self.final_path_img, self.win, self.path, self.colors, self.lines, self.offset)
        except StopIteration as e:
            self.path_finding = False
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
        leng = len(data)
        height = self.colors_block.height
        width = self.colors_block.width
        line_size = len(data) // height
        tt = 2
        t = height//10 - 3
        l_size = line_size//4
        wid = (l_size - 16*tt)//8
        sequence = bytes()
        background = bytes([255,0,0,255])
        background = bytes([0,0,0,0])
        for i in range (8):
            sequence = sequence + ((
                        bytes([0,0,0,0]) * (l_size * tt) +  #odstep y
                        (
                            #biała linia y
                                (background * tt +  # odstęp x
                                 bytes([255, 255, 255, 255]) * wid +  # bialy pasek
                                 background * tt) * 8 +  # odstep x
                                (background * (l_size - 8 * (tt * 2 + wid))) #dopelłnij
                        )
                        +
                        (
                            #wypełnienie
                            (
                                    b''.join(
                                        background * tt +
                                        bytes([255, 255, 255, 255]) * 1 +
                                        self.palette[i * 8 + j] * (wid - 2) +
                                        bytes([255, 255, 255, 255]) * 1 +
                                        background * tt
                                        for j in range(8)
                                    )
                                    +
                                    background * (l_size - 8 * (tt * 2 + wid))
                            )
                        )
                        * t +  #ilosc multiplikacji segmentu
                        (
                            # biała linia y
                                (
                                background * tt +  # odstęp x
                                bytes([255, 255, 255, 255]) * wid +  # bialy pasek
                                background * tt) * 8 +  # odstep x
                                background * (l_size - 8 * (tt * 2 + wid)) #dopełnij
                        ) +
                        background * (l_size * tt) #odstep y
                ))
        data[:] = ( sequence
                + background * l_size + b'\x120' * len(data)
            )[:leng]
        self.segment_height = self.colors_block.height // 32
        self.segment_width = max(1, int((width - 8.5 * self.segment_height) // 8) - 2)
    def fill_striped_blockw(self):
        data = self.colors_block_data
        width = self.colors_block.width

        self.segment_height = max(2, self.colors_block.height // 32 - 2)

        leng = len(data)
        segment_bytes = leng // 32
        rows_in_segment = segment_bytes // (width * 4)

        color_left = self.colors['Background']
        self.segment_width = max(1, int((width - 8.5 * self.segment_height) // 8) - 2)

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

    def restart(self):
        #self.start_time = datetime.now()
        self.background_img_data[:] = self.darken(self.colors['Background'], 0.6) * (
                    len(self.background_img_data) // 4)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)
    def show_menu(self):
        self.menu_img_data[:] = self.darken((self.colors['Background'][:3] + bytes([255])), 0.6) * (
                    len(self.menu_img_data) // 4)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.menu_img.ptr, self.win.width // 8 * 7, 0)

        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64, 0xFFFFFFFF,
                              "42")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 9, 0xFFFFFFFF,
                              "Gr 1")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 17, 0xFFFFFFFF,
                              "Gr 2")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 25, 0xFFFFFFFF,
                              "B 1")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 33, 0xFFFFFFFF,
                              "B 2")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 41, 0xFFFFFFFF,
                              "S")
        self.m.mlx_string_put(self.mlx, self.win.ptr, self.win.width // 64 * 57, self.win.height // 64 * 49, 0xFFFFFFFF,
                              "Bckg")
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



    def put_strings(self):
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

    import math

    def is_hex_filled(x: int, y: int, hex_r: int) -> bool:
        """
        Zwraca True jeśli punkt (x, y) leży wewnątrz heksagonu
        w powtarzalnej siatce hex
        """

        h = math.sqrt(3) * hex_r
        x_step = 3 * hex_r / 2
        y_step = h

        # indeks kolumny
        col = int(x // x_step)

        # przesunięcie co drugą kolumnę
        y_offset = y_step / 2 if col % 2 else 0

        # indeks wiersza
        row = int((y - y_offset) // y_step)

        # środek aktualnego heksagonu
        cx = col * x_step
        cy = row * y_step + y_offset

        # lokalne współrzędne
        dx = abs(x - cx)
        dy = abs(y - cy)

        # szybkie odrzucenie
        if dx > hex_r or dy > h / 2:
            return False

        # właściwy test heksagonu
        return (math.sqrt(3) * dx + dy) <= h

    def theme_changed(self):
        for a, b in zip(self.themes[self.theme_idx].values(), self.colors.values()):
            if a[:3] != b[:3]:
                return True
        return False
    def drawq(self, generator, seed):

        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        self.win = Window(self.m, self.mlx, "A-Maze-ing")
        self.img = Image(self.m, self.mlx, self.win, self.maze)
        self.path_img = Image(self.m, self.mlx, self.win, self.maze)
        self.final_path_img = Image(self.m, self.mlx, self.win, self.maze)
        scale = self.img.scale
        self.offset = (self.img.height - self.maze.height*self.img.scale)//2

        self.lines = {
            'Snake': self.colors['Snake'] * self.img.scale,
            'Block not found': self.colors['Block not found'] * (self.img.scale - 1),
            'Block found': self.colors['Block found'] * (self.img.scale - self.img.thickness),
            '42': self.colors['42'] * (self.img.scale - self.img.thickness),
            'line_x': self.colors['Grid 1'] * (self.img.scale + 2 * self.img.thickness),
            'line_y': self.colors['Grid 1'] * self.img.thickness
        }
        self.brick = Brick(self.img.scale, self.transparency, self.colors['Block found'], bytes([30,30,30,30]))
        size = (
            10 if scale < 15 else
            15 if scale < 20 else
            20 if scale < 30 else
            30 if scale < 40 else
            40 if scale < 60 else
            60 if scale < 80 else
            80 if scale < 100 else
            100
        )
        self.save = self.m.mlx_png_file_to_image(self.mlx, "pictures/save.png")
        self.play = self.m.mlx_png_file_to_image(self.mlx, "pictures/play.png")
        self.pause = self.m.mlx_png_file_to_image(self.mlx, "pictures/pause.png")
        self.freeze = self.m.mlx_png_file_to_image(self.mlx, "pictures/freeze.png")
        self.frozen = self.m.mlx_png_file_to_image(self.mlx, "pictures/freezed.png")
        self.start = self.m.mlx_png_file_to_image(self.mlx, f"pictures/start{size}.png")
        self.finish = self.m.mlx_png_file_to_image(self.mlx, f"pictures/finish{size}.png")
        self.refresh = self.m.mlx_png_file_to_image(self.mlx, "pictures/refresh.png")
        self.corrector = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 400, self.win.width // 100)
        self.corrector_data = self.m.mlx_get_data_addr(self.corrector.ptr)[0]
        self.corrector_data[:] = bytes([120, 120, 120, 255]) * (len(self.corrector_data) // 4)
        self.slider = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 20, self.win.width // 400)
        self.slider_data = self.m.mlx_get_data_addr(self.slider.ptr)[0]
        self.slider_data[:] = bytes([255, 255, 255, 255]) * (len(self.slider_data) // 4)
        self.background_img = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 8 * 7, self.win.height)
        self.background_img_data = self.m.mlx_get_data_addr(self.background_img.ptr)[0]
        self.background_img_data[:] = self.darken(self.colors['Background'], 0.6) * (len(self.background_img_data)//4)
        self.m.mlx_put_image_to_window(self.mlx, self.win.ptr, self.background_img.ptr, 0, 0)
        self.menu_img = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 8, self.win.height)
        self.menu_img_data = self.m.mlx_get_data_addr(self.menu_img.ptr)[0]
        self.menu_img_data[:] = self.darken(self.colors['Background'], 0.6) * (len(self.menu_img_data) // 4)
        self.colors_block = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 16, self.win.height // 64*7)
        self.colors_block_data = self.m.mlx_get_data_addr(self.colors_block.ptr)[0]
        self.gen = generator
        self.seed = seed
        self.fill_striped_block()
        self.strings_background = Image(self.m, self.mlx, self.win, self.maze, self.win.width // 64 * 4, self.win.height // 64 * 5)
        self.strings_background_data = self.m.mlx_get_data_addr(self.strings_background.ptr)[0]
        self.show_menu()
        self.put_strings()
        self.draw = Draw()
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
        #self.m.mlx_hook(self.win.ptr, 6, 1 << 6, self.mouse_move, self.vars)
        #self.m.mlx_hook(self.win.ptr, 4, 1 << 2, self.mouse_press, self.vars)
        #self.m.mlx_hook(self.win.ptr, 5, 1 << 3, self.mouse_release, self.vars)
        self.m.mlx_loop_hook(self.mlx, self.draw_slow, self.vars)
        
        self.gen = generator
        self.generator = self.gen.create_maze(self.maze, seed, self.player)
        self.m.mlx_loop(self.mlx)

    def mouse_press(self, button, x, y, vars):
        self.mouse = True

    def mouse_release(self, button, x, y, vars):
        self.mouse = False

    def mouse_move(self, x, y, vars):
        if (self.mouse and self.slider_x + self.win.width // 128 * 119 < x < self.slider_x + self.win.width // 128 * 119 + self.slider.width and
                self.win.height // 64 * 59 + self.play[1] // 2 - self.corrector.height//2 + self.slider.height//2 < y < self.win.height // 64 * 59 + self.play[1]//2 - self.corrector.height//2 + self.slider.height//2 + self.slider.width):
            if x - (self.win.width // 128 * 119) - self.slider_x > 10 or x - (self.win.width // 128 * 119) - self.slider_x < -10:
                self.slider_x = (x - self.win.width // 128 * 119)
                self.put_strings()
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
        self.mouse = True
        if self.win.width // 128 * 119 < x < self.win.width // 128 * 119 + self.slider.width + 10 \
                and self.win.height // 64 * 59 + self.slider.height < y < self.win.height // 64 * 59 + self.corrector.height + self.slider.height:
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
            if self.win.width // 64 * 63 < x < self.win.width // 64 * 63 + self.save[1] and self.win.height // 64 * 57 < y < self.win.height // 64 * 57 + \
                    self.save[2]:
                self.themes[self.theme_idx] = copy(self.colors)
        if self.win.width // 64 * 61 < x < self.win.width // 64 * 61 + self.refresh[1] and self.win.height // 64 * 57 < y < self.win.height // 64 * 57 + \
                self.refresh[2]:
            self.player = not self.player
            self.generator = self.gen.create_maze(self.maze, self.seed, self.player)
        if self.win.width // 64 * 63 < x < self.win.width // 64 * 63 + self.play[1] and self.win.height // 64 * 59 < y < self.win.height // 64 * 59 + \
                self.play[2]:
            self.paused = not self.paused
        if self.win.width // 64 * 63 < x < self.win.width // 64 * 63 + self.freeze[1] and self.win.height // 64 * 61 < y < self.win.height // 64 * 61 + \
                self.freeze[2]:
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
            self.put_strings()
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
