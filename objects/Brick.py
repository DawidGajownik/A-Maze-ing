class Brick:
    def __init__(self, size:int, transparency: int, color: bytes = None, mortar_color: bytes = None):
        self.mortar_thickness_y = 3
        self.mortar_thickness_x = 5
        self.bricks_in_row = 3
        self.rows_in_block = 7
        self.size = size
        self.transparency = transparency
        self.color = bytes([28, 53, 116, max(255, self.transparency * 2)]) if color is None else color
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

        self.row_1 = (self.color * self.brick_w + self.mortar_color * self.mortar_thickness_x) * (
                    self.bricks_in_row - 1) + self.color * self.brick_w + self.mortar_color * (self.size - sum_row_1)
        self.mortar = self.mortar_color * self.size
        self.row_3 = self.color * self.half_brick_w + self.mortar_color * self.mortar_thickness_x + (
                    self.color * self.brick_w + self.mortar_color * self.mortar_thickness_x) * (self.bricks_in_row - 1) + self.color * (
                            self.size - sum_row_3)