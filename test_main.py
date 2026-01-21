from MAZE import MazeManager


def main() -> None:
    manager = MazeManager(20, 20, (1, 1), (14, 14))

   # manager.generate(90)
   # print(manager.str_map)
   # manager.find()
   # print(manager.path)
    manager.draw(90)


if __name__ == "__main__":
    main()
