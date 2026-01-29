from enum import IntEnum


class Key(IntEnum):
    K_B = 98
    K_L = 108
    K_J = 106
    K_I = 105
    K_K = 107
    K_W = 119
    K_S = 115
    K_A = 97
    K_N = 110
    K_ESCAPE = 65307


class Numpad(IntEnum):
    EIGHT = 65431
    TWO = 65433
    SIX = 65432
    FOUR = 65430
    PLUS = 65451
    MINUS = 65453


class Arrow(IntEnum):
    LEFT = 65461
    UP = 65362
    RIGHT = 65363
    DOWN = 65364
