from random import randint

class Brick:
    def __init__(self, size:int, transparency: int, darken: callable, color: bytes = None, mortar_color: bytes = None):
        self.mortar_thickness_y = 1
        self.mortar_thickness_x = 2
        self.bricks_in_row = 2
        self.rows_in_block = 5
        self.darken = darken
        self.size = size
        self.transparency = transparency
        self.color = bytes([28, 53, 116, max(255, self.transparency * 2)]) if color else color
        self.mortar_color = bytes([100, 150, 200, max(255, self.transparency * 2)]) if mortar_color is None else mortar_color
        self.texture_create()

    def texture_create(self):
        self.brick_w = self.size // self.bricks_in_row - self.mortar_thickness_x
        self.brick_h = self.size // self.rows_in_block
        while self.size - ((self.brick_w + self.mortar_thickness_x) * self.bricks_in_row) > self.brick_w + self.mortar_thickness_x:
            self.bricks_in_row += 1

        self.half_brick_w = self.brick_w // 2

        sum_row_1 = (self.brick_w + self.mortar_thickness_x) * (self.bricks_in_row - 1) + self.brick_w
        sum_row_3 = self.half_brick_w + self.mortar_thickness_x + (self.brick_w + self.mortar_thickness_x) * (self.bricks_in_row - 1)

        self.rows_odd = [bytearray() for _ in range(21)]
        self.rows_even = [bytearray() for _ in range(21)]
        a = 6
        b = 9

        #self.row_1 = bytearray()

        for row in self.rows_odd:
            for _ in range(self.bricks_in_row - 1):
                for _ in range (self.brick_w):
                    row.extend(self.darken(self.color, randint(a,b)/10))
                for _ in range (self.mortar_thickness_x):
                    row.extend(self.mortar_color)
            for _ in range (self.brick_w):
                row.extend(self.darken(self.color, randint(a,b)/10))
            for _ in range(self.size - sum_row_1):
                row.extend(self.mortar_color)
            row = bytes(row)

        #self.row_3 = bytearray()

        for row in self.rows_even:
            for i in range(self.half_brick_w):
                row.extend(self.darken(self.color, randint(a,b) / 10))
            for i in range(self.mortar_thickness_x):
               row.extend(self.mortar_color)
            for _ in range(self.bricks_in_row - 1):
                for i in range(self.brick_w):
                    row.extend(self.darken(self.color, randint(a,b) / 10))
                for i in range(self.mortar_thickness_x):
                    row.extend(self.mortar_color)
            for i in range(self.size - sum_row_3):
                row.extend(self.darken(self.color, randint(a,b) / 10))
            row = bytes(row)

        #self.row_1 = (self.color * self.brick_w + self.mortar_color * self.mortar_thickness_x) * (
                    #self.bricks_in_row - 1) + self.color * self.brick_w + self.mortar_color * (self.size - sum_row_1)
        self.mortar = self.mortar_color * self.size
        #self.row_3 = self.color * self.half_brick_w + self.mortar_color * self.mortar_thickness_x + (
                    #self.color * self.brick_w + self.mortar_color * self.mortar_thickness_x) * (self.bricks_in_row - 1) + self.color * (
                            #self.size - sum_row_3)