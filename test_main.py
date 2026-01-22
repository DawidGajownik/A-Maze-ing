from MAZE import MazeManager
from random import randint


def main() -> None:
    manager = MazeManager(100, 60, (1, 1), (14, 14))

    # manager.generate(90)
    # print(manager.str_map)
    # manager.find()
    # print(manager.path)
    manager.draw(randint(1, 9999))


if __name__ == "__main__":
    main()
