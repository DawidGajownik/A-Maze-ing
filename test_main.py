from debian.debtags import output

from MAZE import MazeManager
from random import randint


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
        print(entry, exit)
        output = config["OUTPUT_FILE"]
        perfect = config["PERFECT"].lower() == "true"
        manager = MazeManager(width, height, entry, exit)
        manager.draw(int(config['SEED']) if config['SEED'] else randint(1, 9999))
        s = manager.generator.get_maze_str()
        with open(output, "w") as file:
            file.write(str(s))

    except KeyError as e:
        raise RuntimeError(f"Brakuje klucza w configu: {e}")



if __name__ == "__main__":
    main()
