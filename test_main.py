from objects import Maze
from random import randint
from algorithms import MazeGenerator, PathFinder
from utils import MazeVisualizer
from typing import Dict


def is_true_false(key: str, config: Dict[str, str]) -> None:
    if not (config[key].lower() == "true"
            or config[key].lower() == "false"):
        raise ValueError(f"{key}: Diffrent from 'True' or 'False'.")


def main() -> None:
    config = {}
    with open("config.txt") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
        entry = str((config["ENTRY"])).split(",")
        exit = str((config["EXIT"])).split(",")
        entry = int(entry[0]), int(entry[1])
        exit = int(exit[0]), int(exit[1])
        if (entry[0] < 0 or entry[0] > width - 1
            or entry[1] < 0 or entry[1] > height - 1
            or exit[0] < 0 or exit[0] > width - 1
                or exit[1] < 0 or exit[1] > height - 1):
            print("Invalid (start, end) coordinates.")
            return
        output = config["OUTPUT_FILE"]

        is_true_false('PERFECT', config)
        perfect = config["PERFECT"].lower() == "true"

        is_true_false('HEART', config)
        heart = config['HEART'].lower() == "true"

        maze = Maze(width, height, entry, exit, perfect, heart)
        seed = (int(config['SEED']) if 'SEED' in list(config.keys())
                else randint(1, 9999))
        generator = MazeGenerator()
        finder = PathFinder()
        maze_map_hex = generator.create_maze_instant(maze, seed)
        path_str = finder.find_path_instant(maze)
        path_str = finder.get_str_path(path_str)

        with open(output, "w") as file:
            file.write(maze_map_hex)
            file.write(f"\n\n{entry[0]},{entry[1]}\n")
            file.write(f"{exit[0]},{exit[1]}\n")
            file.write(f"{path_str}\n")

        visualizer = MazeVisualizer(maze, finder)
        visualizer.open_window(generator, seed)

    except KeyError as e:
        print(f"Brakuje klucza w configu: {e}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
