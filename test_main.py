from MAZE import MazeManager
from random import randint

from algorithms import MazeGenerator, PathFinder
from utils import MazeVisualizer

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
        perfect = config["PERFECT"].lower() == "true"
        manager = MazeManager(width, height, entry, exit, perfect)
        seed = int(config['SEED']) if 'SEED' in list(config.keys()) else randint(1, 9999)
        #to zmienilem
        #maze_map_hex = manager.generator.create_maze_instant(manager, seed)
        #path_str = manager.finder.find_path_instant(manager)
        #na to
        generator = MazeGenerator()
        finder = PathFinder()
        maze_map_hex = generator.create_maze_instant(manager, seed)
        path_str = finder.find_path_instant(manager)

        with open(output, "w") as file:
            file.write(maze_map_hex)
            file.write(f"\n\n{entry[0]},{entry[1]}\n")
            file.write(f"{exit[0]},{exit[1]}\n")
            file.write(f"{path_str}\n")

        #te dwie linie wstawilem z managera
        visualizer = MazeVisualizer(manager, finder)
        visualizer.open_window(generator, seed)
        #ta wyjebalem
        #manager.draw(seed)

    except KeyError as e:
        print(f"Brakuje klucza w configu: {e}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
