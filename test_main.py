from MAZE import MazeManager


def main() -> None:
    manager = MazeManager(50, 50, (1, 1), (49, 49))

    manager.generate(90)
    print(manager.str_map)
    manager.find()
    print(manager.path)
    manager.draw()


if __name__ == "__main__":
    main()
