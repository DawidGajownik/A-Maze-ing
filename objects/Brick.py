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
        color = None
        mortar_color = None
        self.color = bytes([28, 53, 116, max(255, self.transparency * 8)]) if not color else color[:3] + bytes([255])
        self.mortar_color = bytes([30, 30, 30, 255]) if not mortar_color else mortar_color[:3] + bytes([255])
        self.lines_amount = 21
        self.texture_create()

    def texture_create(self):
        self.brick_w = self.size // self.bricks_in_row - self.mortar_thickness_x
        self.brick_h = self.size // self.rows_in_block
        while self.size - ((self.brick_w + self.mortar_thickness_x) * self.bricks_in_row) > self.brick_w + self.mortar_thickness_x:
            self.bricks_in_row += 1

        self.half_brick_w = self.brick_w // 2

        sum_row_1 = (self.brick_w + self.mortar_thickness_x) * (self.bricks_in_row - 1) + self.brick_w
        sum_row_3 = self.half_brick_w + self.mortar_thickness_x + (self.brick_w + self.mortar_thickness_x) * (self.bricks_in_row - 1)

        self.rows_odd = [bytearray() for _ in range(self.lines_amount)]
        self.rows_even = [bytearray() for _ in range(self.lines_amount)]
        a = 2
        b = 9

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

        self.mortar = self.mortar_color * self.size
