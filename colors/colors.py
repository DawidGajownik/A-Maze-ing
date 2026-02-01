def get_palette() -> list[bytes]:
    return [
            bytes([255, 255, 255, 255]), bytes([192, 192, 192, 255]),
            bytes([255, 192, 192, 255]), bytes([255, 224, 192, 255]),
            bytes([255, 255, 192, 255]), bytes([192, 255, 192, 255]),
            bytes([192, 255, 255, 255]), bytes([192, 192, 255, 255]),

            bytes([224, 224, 224, 255]), bytes([160, 160, 160, 255]),
            bytes([255, 160, 160, 255]), bytes([255, 192, 160, 255]),
            bytes([255, 255, 160, 255]), bytes([160, 255, 160, 255]),
            bytes([160, 255, 255, 255]), bytes([160, 160, 255, 255]),

            # rząd 3
            bytes([192, 192, 192, 255]), bytes([128, 128, 128, 255]),
            bytes([255, 128, 128, 255]), bytes([255, 160, 128, 255]),
            bytes([255, 255, 128, 255]), bytes([128, 255, 128, 255]),
            bytes([128, 255, 255, 255]), bytes([128, 128, 255, 255]),

            # rząd 4
            bytes([160, 160, 160, 255]), bytes([96, 96, 96, 255]),
            bytes([255, 96, 96, 255]), bytes([255, 128, 96, 255]),
            bytes([255, 255, 96, 255]), bytes([96, 255, 96, 255]),
            bytes([96, 255, 255, 255]), bytes([96, 96, 255, 255]),

            # rząd 5
            bytes([128, 128, 128, 255]), bytes([64, 64, 64, 255]),
            bytes([255, 0, 0, 255]), bytes([255, 128, 0, 255]),
            bytes([255, 255, 0, 255]), bytes([0, 255, 0, 255]),
            bytes([0, 255, 255, 255]), bytes([0, 0, 255, 255]),

            # rząd 6
            bytes([96, 96, 96, 255]), bytes([32, 32, 32, 255]),
            bytes([192, 0, 0, 255]), bytes([192, 96, 0, 255]),
            bytes([192, 192, 0, 255]), bytes([0, 192, 0, 255]),
            bytes([0, 192, 192, 255]), bytes([0, 0, 192, 255]),

            # rząd 7
            bytes([64, 64, 64, 255]), bytes([0, 0, 0, 255]),
            bytes([128, 0, 0, 255]), bytes([128, 64, 0, 255]),
            bytes([128, 128, 0, 255]), bytes([0, 128, 0, 255]),
            bytes([0, 128, 128, 255]), bytes([0, 0, 128, 255]),

            # rząd 8
            bytes([32, 32, 32, 255]), bytes([16, 16, 16, 255]),
            bytes([64, 0, 0, 255]), bytes([64, 32, 0, 255]),
            bytes([64, 64, 0, 255]), bytes([0, 64, 0, 255]),
            bytes([0, 64, 64, 255]), bytes([0, 0, 64, 255]),
        ]


def get_themes(transparency: int) -> dict:
    return {
        1: {
            'name': 'dgajowni',
            '42': bytes([0, 0, 255, transparency]),
            'Grid 1': bytes([240, 240, 240, transparency]),
            'Grid 2': bytes([5, 10, 5, transparency]),
            'Block found': bytes([30, 30, 30, transparency]),
            'Block not found': bytes([0, 0, 0, transparency]),
            'Snake': bytes([192, 96, 0, transparency]),
            'Background': bytes([0, 0, 0, transparency]),
        },

        2: {
            'name': 'classic',
            '42': bytes([255, 0, 0, transparency]),
            'Grid 1': bytes([200, 200, 200, transparency]),
            'Grid 2': bytes([120, 120, 120, transparency]),
            'Block found': bytes([0, 200, 0, transparency]),
            'Block not found': bytes([50, 50, 50, transparency]),
            'Snake': bytes([0, 255, 0, transparency]),
            'Background': bytes([0, 0, 0, transparency]),
        },

        3: {
            'name': 'neon',
            '42': bytes([255, 0, 255, transparency]),
            'Grid 1': bytes([0, 255, 255, transparency]),
            'Grid 2': bytes([20, 20, 20, transparency]),
            'Block found': bytes([255, 255, 0, transparency]),
            'Block not found': bytes([255, 0, 0, transparency]),
            'Snake': bytes([0, 255, 128, transparency]),
            'Background': bytes([0, 0, 0, transparency]),
        },

        4: {
            'name': 'forest',
            '42': bytes([34, 139, 34, transparency]),
            'Grid 1': bytes([85, 107, 47, transparency]),
            'Grid 2': bytes([0, 50, 0, transparency]),
            'Block found': bytes([46, 139, 87, transparency]),
            'Block not found': bytes([10, 30, 10, transparency]),
            'Snake': bytes([0, 255, 127, transparency]),
            'Background': bytes([5, 20, 5, transparency]),
        },

        5: {
            'name': 'desert',
            '42': bytes([210, 180, 140, transparency]),
            'Grid 1': bytes([238, 214, 175, transparency]),
            'Grid 2': bytes([189, 154, 122, transparency]),
            'Block found': bytes([160, 82, 45, transparency]),
            'Block not found': bytes([120, 60, 30, transparency]),
            'Snake': bytes([255, 215, 0, transparency]),
            'Background': bytes([80, 50, 20, transparency]),
        },

        6: {
            'name': 'ice',
            '42': bytes([180, 220, 255, transparency]),
            'Grid 1': bytes([220, 240, 255, transparency]),
            'Grid 2': bytes([120, 170, 200, transparency]),
            'Block found': bytes([100, 140, 180, transparency]),
            'Block not found': bytes([50, 80, 120, transparency]),
            'Snake': bytes([0, 255, 255, transparency]),
            'Background': bytes([10, 30, 60, transparency]),
        },

        7: {
            'name': 'mono',
            '42': bytes([255, 255, 255, transparency]),
            'Grid 1': bytes([200, 200, 200, transparency]),
            'Grid 2': bytes([150, 150, 150, transparency]),
            'Block found': bytes([100, 100, 100, transparency]),
            'Block not found': bytes([50, 50, 50, transparency]),
            'Snake': bytes([220, 220, 220, transparency]),
            'Background': bytes([0, 0, 0, transparency]),
        },

        8: {
            'name': 'retro',
            '42': bytes([255, 128, 0, transparency]),
            'Grid 1': bytes([255, 255, 0, transparency]),
            'Grid 2': bytes([0, 128, 128, transparency]),
            'Block found': bytes([128, 0, 128, transparency]),
            'Block not found': bytes([0, 0, 128, transparency]),
            'Snake': bytes([0, 255, 0, transparency]),
            'Background': bytes([0, 0, 0, transparency]),
        },
        9: {
            'name': 'neon_pink',
            '42': bytes([255, 0, 150, transparency]),
            'Grid 1': bytes([40, 40, 40, transparency]),
            'Grid 2': bytes([20, 20, 20, transparency]),
            'Block found': bytes([255, 0, 200, transparency]),
            'Block not found': bytes([10, 10, 10, transparency]),
            'Snake': bytes([0, 255, 200, transparency]),
            'Background': bytes([0, 0, 0, transparency]),
        },

        10: {
            'name': 'toxic_green',
            '42': bytes([0, 255, 0, transparency]),
            'Grid 1': bytes([30, 60, 30, transparency]),
            'Grid 2': bytes([10, 30, 10, transparency]),
            'Block found': bytes([0, 200, 0, transparency]),
            'Block not found': bytes([0, 50, 0, transparency]),
            'Snake': bytes([150, 255, 0, transparency]),
            'Background': bytes([0, 10, 0, transparency]),
        },

        11: {
            'name': 'lava',
            '42': bytes([255, 80, 0, transparency]),
            'Grid 1': bytes([80, 20, 0, transparency]),
            'Grid 2': bytes([40, 10, 0, transparency]),
            'Block found': bytes([200, 40, 0, transparency]),
            'Block not found': bytes([30, 10, 0, transparency]),
            'Snake': bytes([255, 200, 0, transparency]),
            'Background': bytes([10, 0, 0, transparency]),
        },

        12: {
            'name': 'cyber_blue',
            '42': bytes([0, 150, 255, transparency]),
            'Grid 1': bytes([20, 40, 60, transparency]),
            'Grid 2': bytes([10, 20, 30, transparency]),
            'Block found': bytes([0, 100, 200, transparency]),
            'Block not found': bytes([0, 20, 40, transparency]),
            'Snake': bytes([0, 255, 255, transparency]),
            'Background': bytes([0, 0, 20, transparency]),
        },

        13: {
            'name': 'matrix',
            '42': bytes([0, 255, 70, transparency]),
            'Grid 1': bytes([0, 60, 20, transparency]),
            'Grid 2': bytes([0, 30, 10, transparency]),
            'Block found': bytes([0, 180, 50, transparency]),
            'Block not found': bytes([0, 20, 10, transparency]),
            'Snake': bytes([120, 255, 120, transparency]),
            'Background': bytes([0, 5, 0, transparency]),
        },

        14: {
            'name': 'purple_haze',
            '42': bytes([180, 0, 255, transparency]),
            'Grid 1': bytes([60, 0, 80, transparency]),
            'Grid 2': bytes([30, 0, 40, transparency]),
            'Block found': bytes([140, 0, 200, transparency]),
            'Block not found': bytes([20, 0, 30, transparency]),
            'Snake': bytes([255, 0, 255, transparency]),
            'Background': bytes([5, 0, 10, transparency]),
        },

        15: {
            'name': 'sandstorm',
            '42': bytes([210, 180, 120, transparency]),
            'Grid 1': bytes([160, 140, 100, transparency]),
            'Grid 2': bytes([120, 100, 70, transparency]),
            'Block found': bytes([180, 150, 90, transparency]),
            'Block not found': bytes([60, 50, 30, transparency]),
            'Snake': bytes([255, 220, 150, transparency]),
            'Background': bytes([40, 30, 20, transparency]),
        },

        16: {
            'name': 'ice_core',
            '42': bytes([180, 240, 255, transparency]),
            'Grid 1': bytes([120, 180, 200, transparency]),
            'Grid 2': bytes([80, 120, 150, transparency]),
            'Block found': bytes([100, 200, 255, transparency]),
            'Block not found': bytes([30, 60, 80, transparency]),
            'Snake': bytes([0, 255, 255, transparency]),
            'Background': bytes([0, 20, 40, transparency]),
        },

        17: {
            'name': 'blood',
            '42': bytes([180, 0, 0, transparency]),
            'Grid 1': bytes([80, 0, 0, transparency]),
            'Grid 2': bytes([40, 0, 0, transparency]),
            'Block found': bytes([255, 0, 0, transparency]),
            'Block not found': bytes([30, 0, 0, transparency]),
            'Snake': bytes([255, 80, 80, transparency]),
            'Background': bytes([10, 0, 0, transparency]),
        },

        18: {
            'name': 'gold',
            '42': bytes([255, 215, 0, transparency]),
            'Grid 1': bytes([120, 100, 20, transparency]),
            'Grid 2': bytes([80, 60, 10, transparency]),
            'Block found': bytes([200, 170, 0, transparency]),
            'Block not found': bytes([40, 30, 5, transparency]),
            'Snake': bytes([255, 255, 150, transparency]),
            'Background': bytes([20, 15, 0, transparency]),
        },

        19: {
            'name': 'terminal',
            '42': bytes([0, 255, 0, transparency]),
            'Grid 1': bytes([0, 80, 0, transparency]),
            'Grid 2': bytes([0, 40, 0, transparency]),
            'Block found': bytes([0, 200, 0, transparency]),
            'Block not found': bytes([0, 20, 0, transparency]),
            'Snake': bytes([120, 255, 120, transparency]),
            'Background': bytes([0, 0, 0, transparency]),
        },

        20: {
            'name': 'void',
            '42': bytes([100, 100, 100, transparency]),
            'Grid 1': bytes([30, 30, 30, transparency]),
            'Grid 2': bytes([15, 15, 15, transparency]),
            'Block found': bytes([80, 80, 80, transparency]),
            'Block not found': bytes([5, 5, 5, transparency]),
            'Snake': bytes([200, 200, 200, transparency]),
            'Background': bytes([0, 0, 0, transparency]),
        },
        21: {
            'name': 'synthwave',
            '42': bytes([255, 0, 200, transparency]),
            'Grid 1': bytes([60, 0, 80, transparency]),
            'Grid 2': bytes([30, 0, 40, transparency]),
            'Block found': bytes([0, 255, 255, transparency]),
            'Block not found': bytes([20, 0, 30, transparency]),
            'Snake': bytes([255, 255, 0, transparency]),
            'Background': bytes([10, 0, 20, transparency]),
        },

        22: {
            'name': 'doom',
            '42': bytes([255, 60, 0, transparency]),
            'Grid 1': bytes([80, 20, 0, transparency]),
            'Grid 2': bytes([40, 10, 0, transparency]),
            'Block found': bytes([200, 0, 0, transparency]),
            'Block not found': bytes([20, 0, 0, transparency]),
            'Snake': bytes([255, 200, 0, transparency]),
            'Background': bytes([5, 0, 0, transparency]),
        },

        23: {
            'name': 'mario',
            '42': bytes([255, 0, 0, transparency]),
            'Grid 1': bytes([255, 255, 255, transparency]),
            'Grid 2': bytes([0, 0, 255, transparency]),
            'Block found': bytes([255, 200, 0, transparency]),
            'Block not found': bytes([0, 0, 0, transparency]),
            'Snake': bytes([0, 200, 0, transparency]),
            'Background': bytes([90, 170, 255, transparency]),
        },

        24: {
            'name': 'night_city',
            '42': bytes([0, 255, 200, transparency]),
            'Grid 1': bytes([20, 20, 40, transparency]),
            'Grid 2': bytes([10, 10, 25, transparency]),
            'Block found': bytes([255, 0, 150, transparency]),
            'Block not found': bytes([30, 0, 20, transparency]),
            'Snake': bytes([255, 255, 0, transparency]),
            'Background': bytes([5, 5, 15, transparency]),
        },

        25: {
            'name': 'outrun',
            '42': bytes([255, 0, 100, transparency]),
            'Grid 1': bytes([100, 0, 120, transparency]),
            'Grid 2': bytes([50, 0, 60, transparency]),
            'Block found': bytes([0, 255, 255, transparency]),
            'Block not found': bytes([20, 0, 40, transparency]),
            'Snake': bytes([255, 255, 0, transparency]),
            'Background': bytes([10, 0, 30, transparency]),
        },

        26: {
            'name': 'forest',
            '42': bytes([0, 180, 0, transparency]),
            'Grid 1': bytes([40, 80, 40, transparency]),
            'Grid 2': bytes([20, 40, 20, transparency]),
            'Block found': bytes([0, 120, 0, transparency]),
            'Block not found': bytes([10, 20, 10, transparency]),
            'Snake': bytes([120, 255, 120, transparency]),
            'Background': bytes([5, 10, 5, transparency]),
        },

        27: {
            'name': 'desert',
            '42': bytes([255, 200, 120, transparency]),
            'Grid 1': bytes([180, 150, 90, transparency]),
            'Grid 2': bytes([120, 100, 60, transparency]),
            'Block found': bytes([200, 160, 80, transparency]),
            'Block not found': bytes([50, 40, 20, transparency]),
            'Snake': bytes([255, 230, 170, transparency]),
            'Background': bytes([30, 25, 15, transparency]),
        },

        28: {
            'name': 'ice',
            '42': bytes([150, 220, 255, transparency]),
            'Grid 1': bytes([100, 160, 200, transparency]),
            'Grid 2': bytes([60, 120, 160, transparency]),
            'Block found': bytes([120, 200, 255, transparency]),
            'Block not found': bytes([30, 60, 80, transparency]),
            'Snake': bytes([0, 255, 255, transparency]),
            'Background': bytes([0, 20, 40, transparency]),
        },

        29: {
            'name': 'acid',
            '42': bytes([180, 255, 0, transparency]),
            'Grid 1': bytes([80, 120, 0, transparency]),
            'Grid 2': bytes([40, 60, 0, transparency]),
            'Block found': bytes([0, 255, 0, transparency]),
            'Block not found': bytes([20, 30, 0, transparency]),
            'Snake': bytes([255, 255, 100, transparency]),
            'Background': bytes([10, 15, 0, transparency]),
        },

        30: {
            'name': 'grayscale',
            '42': bytes([200, 200, 200, transparency]),
            'Grid 1': bytes([120, 120, 120, transparency]),
            'Grid 2': bytes([80, 80, 80, transparency]),
            'Block found': bytes([160, 160, 160, transparency]),
            'Block not found': bytes([30, 30, 30, transparency]),
            'Snake': bytes([255, 255, 255, transparency]),
            'Background': bytes([0, 0, 0, transparency]),
        },
    }
