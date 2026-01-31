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
| Increase/decrease maze size | `Arrows`                  |
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

