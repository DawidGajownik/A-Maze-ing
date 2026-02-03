*This project has been created as part of the 42 curriculum by Dawid Gajownik (dgajowni) and Sebastian Kolsut (skolsut)

# A-Maze-ing

## Description

This project is an advanced maze generator and visualizer that focuses on real-time rendering, animation, and user interaction.
It allows users not only to generate and display mazes, but also to observe and control the entire generation and solving processes through smooth animations and customizable visuals.

The application supports real-time maze rendering as well as a separate animation showing how the maze is built step by step.
It also includes shortest-path visualization, along with an animated process of finding that path, making the underlying algorithms easy to understand and visually engaging.

A key feature of the project is its high level of visual customization.
Users can smoothly adjust the maze size, color palette, wall thickness, fading effects, and overall visual theme during runtime.
All changes are applied fluidly without restarting the application.

The maze generation animation can be paused, resumed, or restarted at any time.
Additionally, a dedicated slider allows precise control over the animation speed, enabling the user to slow down or accelerate the maze generation process in real time.

In addition to visualization, the project includes a game mode, allowing the user to navigate through the maze manually and complete it against the clock.

As an advanced visual feature, the interior of the maze walls uses a dynamically generated, modifiable rough brick texture.
This texture is created in real time and can be customized by independently adjusting the vertical and horizontal mortar thickness, as well as the number of bricks in both directions.
Changing these parameters directly affects the brick size and overall appearance of the maze walls.

Overall, the project combines algorithmic maze generation with interactive gameplay and advanced visual effects, emphasizing both technical correctness and aesthetic flexibility.

## Instructions


### Instalation
```bash
git clone https://github.com/DawidGajownik/A-Maze-ing
cd A-Maze-ing
python3 a_maze_ing.py config.txt
```

### Controls

#### Maze generation

| Action                                 | Control                    |
| -------------------------------------- | -------------------------- |
| Generate new maze                      | `N`                        |
| Increase/decrease maze size            | `Arrows`                   |
| Restart current maze                   | `Restart icon`             |
| Display/animation mode                 | `Animation icon`           |
| Pause/Resume maze generation animation | `Pause/play icon`          |
| Freez/Resume painting                  | `Freeze icon`              |
| Adjust maze generation speed           | `Speed slider`             |
| Toggle shortest path display/animation | `Path icon`                |
| Enter/Exit game mode                   | `G`                        |

#### Game mode

| Action             | Control       |
| ------------------ | ------------- |
| Move               | `Arrows`      |
| Undo last move     | `Backspace`   |

#### Visual effects

| Action                      | Control                   |
| --------------------------- | ------------------------- |
| Change wall thickness       | `+/-` (numpad)            |
| Change maze colors          | `Color palettes`          |
| Toggle/adjust fading effect | `W/S`                     |
| Change overall theme        | `A/D`                     |
| Save theme                  | `Save icon`               |

#### Bricks adjustment

| Action                                           | Control         |
| -------------------------------------------------| --------------- |
| Brick visible                                    | `B`             |
| Increase/decrease horizontal mortar thickness    | `8/2` (numpad)  |
| Increase/decrease vertical mortar thickness      | `6/4` (numpad)  |
| Increase/decrease amount of bricks horizontally  | `J/L`           |
| Increase/decrease amount of bricks vertically    | `K/I`           |


## mazegen Package Documentation

The `mazegen` package is a standalone module designed for generating and solving mazes. It provides a flexible API for creating randomized mazes with customizable parameters and finding solutions.

### Installation

To install the package, first build the distribution files:

```bash
make install
python3 setup.py sdist bdist_wheel
```

Then install the generated wheel file using pip:

```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Usage

Here is a comprehensive example of how to use the `mazegen` package to generate a maze and find a path through it.

```python
from mazegen import MazeGenerator, PathFinder, Maze

# 1. Instantiate the Maze object
# Define dimensions (width, height)
width = 15
height = 15
# Define Start (0,0) and End (14,14) coordinates
entry_coord = (0, 0)
exit_coord = (14, 14)
# Configuration flags
is_perfect = True  # True for a perfect maze (no loops)
heart_shape = False # True for heart shaped maze

maze = Maze(width, height, entry_coord, exit_coord, is_perfect, heart_shape)

# 2. Generate the Maze
# Initialize the generator
generator = MazeGenerator()
seed = 123456  # Optional seed for reproducibility

# This populates the maze.map with the generated structure
generator.create_maze_instant(maze, seed)

# 3. Access the Structure
# The maze structure is stored in maze.map as a flat list
# Each integer represents a cell and its wall configuration
print(f"Maze Map: {maze.map}")

# 4. Get String Representation
# You can also get a hex string representation of the maze
maze_str = generator.get_maze_str()
print(f"Maze String: \n{maze_str}")

# 5. Solve the Maze
# Initialize the pathfinder
finder = PathFinder()

# Find the shortest path (returns a list of cell indices)
solution_path = finder.find_path_instant(maze)
print(f"Solution Path: {solution_path}")

# 6. Get Path as Directions
# Convert the solution path to a string of directions (N, S, E, W)
path_str = finder.get_str_path(solution_path)
print(f"Path String: {path_str}")
```

### Parameters

The `MazeGenerator` and `Maze` classes support the following custom parameters:

-   **width** (`int`): The width of the maze grid.
-   **height** (`int`): The height of the maze grid.
-   **entry** (`Tuple[int, int]`): The starting coordinates (x, y) of the maze.
-   **exit** (`Tuple[int, int]`): The ending coordinates (x, y) of the maze.
-   **is_perfect** (`bool`): If `True`, generates a perfect maze where exactly one path exists between any two points. If `False`, the maze may contain loops.
-   **heart** (`bool`): If `True`, creates a heart-shaped pattern within the maze (experimental feature).
-   **seed** (`int`): An integer seed passed to the generator to ensure deterministic and reproducible maze generation.

### Structure Access

-   **Maze Structure**: Use `maze.map` to access the generated grid. It is a one-dimensional list of integers where each index corresponds to `y * width + x`. The integer value encodes the state of the cell (walls, visited status, etc.).
-   **Solution**: The `find_path_instant` method returns a list of integers, where each integer represents the index of a cell in the path from the entry to the exit.
