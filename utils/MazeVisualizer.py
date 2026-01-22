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
        #self.generator.create_maze(15, 15)
        #self.maze = Maze(self.generator.maze, self.path, self.enter, self.exit)
        self.x = -1
        self.y = -2

    def draw_slow(self, vars):
        if not self.bool:
            return
        try:
            found = next(self.generator)
        #gen = self.gen.create_maze(self.maze, self.seed)
        #if self.bool:
            #for found in gen:
            self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win, self.imgs, found)
            #self.bool = False
        except StopIteration as e:
            print(e)
            self.bool = False
        # if self.bool:
        #    generator = vars['generator']
        #    gen = generator.create_maze(self.maze, 90)
        #    for _ in gen:
        #        self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win)
        #    self.bool = False
            #img: Image = vars['img']
            #maze: Maze = vars['maze']
            #win: Window = vars['win']
            #mlx = vars['mlx']
            #draw: callable = vars['draw']
            #draw_out: callable = vars['draw_out']
            #m: Mlx = vars['m']
            ##if self.x < self.maze.width - 1 and self.y < self.maze.height - 2 and self.bool:
            #    #self.x += 1
            #    #draw_out(self.x, self.y+2, m, mlx, maze, img, win)
            ##elif self.y < self.maze.height - 2 and self.bool:
            ##    self.x = 0
            ##    self.y += 1
            #    #draw_out(self.x, self.y+2, m, mlx, maze, img, win)
            #if self.x < self.maze.width - 1 and self.bool:
            #    self.x += 1
            #    draw(self.x, self.y, m, mlx, maze, img, win)
            #    
            #elif self.y < self.maze.height - 1 and self.bool:
            #    self.x = 0
            #    self.y += 1
            #    draw(self.x, self.y, m, mlx, maze, img, win)
            #else:
            #    self.x = -1
            #    self.y = -2
            #    img.prev_thickness = img.thickness
            #    img.prev_scale = img.scale
            #    self.bool = False

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

    def drawq(self, generator, seed):

        self.m = Mlx()
        self.mlx = self.m.mlx_init()
        self.win = Window(self.m, self.mlx, "window")
        self.img = Image(self.m, self.mlx, self.win, self.maze)
        self.imgs = {
            i: self._new_image_dict(self.m, self.img.width, self.img.height, i)
            for i in range(17)
        }
        self.gen = generator
        self.imgs[False] = self._new_image_dict(self.m, self.img.width, self.img.height, 20)
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
        #wall_range = (-self.img.thickness+1, self.img.scale + self.img.thickness)
        self.m.mlx_key_hook(self.win.ptr, self.key_hook, self.vars)
        self.bool = True
        self.m.mlx_loop_hook(self.mlx, self.draw_slow, self.vars)
        self.gen = generator
        self.generator = self.gen.create_maze(self.maze, seed)
        #for found in gen:
        #    self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win, self.imgs, found)
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

    def key_hook(self, keycode, vars):
        img: Image = vars['img']
        maze: Maze = vars['maze']
        win: Window = vars['win']
        mlx = vars['mlx']
        draw: callable = vars['draw']
        m: Mlx = vars['m']
        #print(keycode)
        if keycode == 110:
            gen = self.gen.create_maze(self.maze, randint(1, 9999))
            img.set_scale(self.maze)
            for found in gen:
                self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win, self.imgs, found)
            
            self.x = -1
            self.y = -2
            self.bool = True
        if keycode == 65451:
            img.thickness += 1
        if keycode == 65453:
            if (img.thickness > 1):
                img.thickness -= 1
        if keycode == 65361 and self.gen.width > 4:
            self.gen.width -= 1
            sgen = self.gen.create_maze(self.maze, randint(1, 9999))
            img.set_scale(self.maze)
            #for _ in gen:
            self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win, self.imgs)
        if keycode == 65362 and self.gen.height > 4:
            self.gen.height -= 1
            gen = self.gen.create_maze(self.maze, randint(1, 9999))
            img.set_scale(self.maze)
            # for _ in gen:
            self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win, self.imgs)
        if keycode == 65363:
            self.gen.width += 1
            gen = self.gen.create_maze(self.maze, randint(1, 9999))
            img.set_scale(self.maze)
            # for _ in gen:
            self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win, self.imgs)
        if keycode == 65364:
            self.gen.height += 1
            gen = self.gen.create_maze(self.maze, randint(1, 9999))
            img.set_scale(self.maze)
            # for _ in gen:
            self.draw.draw_maze(self.x, self.y, self.m, self.mlx, self.maze, self.img, self.win, self.imgs)
        #if keycode == 65361 and self.can_go(maze, Direction.LEFT):
        #    if maze.pacman.x > 0:
        #        maze.pacman.x -= 1
        #        print("W", end="", flush=True)
        #if keycode == 65362 and self.can_go(maze, Direction.UP):
        #    if maze.pacman.y > 0:
        #        maze.pacman.y -= 1
        #        print("N", end="", flush=True)
        #if keycode == 65363 and self.can_go(maze, Direction.RIGHT):
        #    if maze.pacman.x < maze.width - 1:
        #        maze.pacman.x += 1
        #        print("E", end="", flush=True)
        #if keycode == 65364 and self.can_go(maze, Direction.DOWN):
        #    if maze.pacman.y < maze.height - 1:
        #        maze.pacman.y += 1
        #        print("S", end="", flush=True)
        #if keycode in (
        #    #65451, 
        #    65453, 65451, 65361, 65362, 65363, 65364):
        #    self.bool = True
        if keycode == 65307:
            m.mlx_destroy_window(mlx, win.ptr)
            m.mlx_loop_exit(mlx)
