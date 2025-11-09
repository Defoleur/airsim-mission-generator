# MissionGenerator for AirSim Environments

`MissionGenerator` is a Python utility class designed to manage dynamic mission scenarios within a `cosysairsim` simulation. It is built to be integrated into a `gymnasium` (or OpenAI Gym) reinforcement learning environment, allowing for the procedural generation of unique obstacle layouts for each training episode.

This class handles the spawning, tracking, and automatic cleanup of obstacles, ensuring that each new mission is distinct and that objects are correctly removed from the simulation upon reset.

## Core Features

* **Dynamic Obstacle Spawning:** Generates a specified number of obstacles within defined 2D coordinate ranges (`x_range`, `y_range`).
* **Collision Avoidance:** Ensures that newly spawned obstacles maintain a minimum distance from each other to prevent unrealistic, overlapping placements.
* **Reproducibility:** Uses injected `random.Random` instances, allowing for deterministic and reproducible mission generation by controlling the initial seeds.
* **Automatic Cleanup:** Manages the lifecycle of spawned objects, automatically destroying them via `simDestroyObject` when a new mission is generated or when the class instance is deleted.

## Requirements

* `python >= 3.8`
* `cosysairsim` (or `airsim-client`)
* `math` (Standard Library)

## API Reference

### `__init__(client, rng_x, rng_y, obstacle_move_x, obstacle_move_y, obstacle_name, obstacle_scale)`

Initializes the generator.

* `client` (airsim.MultirotorClient): An active `MultirotorClient` instance connected to the simulation.
* `rng_x` (random.Random): A `random.Random` instance for generating X-coordinates.
* `rng_y` (random.Random): A `random.Random` instance for generating Y-coordinates.
* `obstacle_move_x` (random.Random): A `random.Random` instance for X-axis movement vectors (if used).
* `obstacle_move_y` (random.Random): A `random.Random` instance for Y-axis movement vectors (if used).
* `obstacle_name` (str): The base name (prefix) for spawned obstacles (e.g., "Obstacle").
* `obstacle_scale` (airsim.Vector3r): An AirSim vector defining the scale of the "Cube" obstacles.

---

### `spawn_obstacles(params)`

Clears the previous set of obstacles and generates a new one. This is the primary method to call at the beginning of each episode.

* `params` (dict): A dictionary containing the parameters for the new mission. Must include:
    * `"obstacle_count"` (int): The number of obstacles to spawn.
    * `"obstacle_x_range"` (list[float]): The `[min, max]` range for the X-axis.
    * `"obstacle_y_range"` (list[float]): The `[min, max]` range for the Y-axis.
    
---

### `clear_obstacles()`

Safely destroys all obstacles that were spawned by this manager. This is called automatically by `spawn_obstacles()` and the class destructor (`__del__`), so manual calls are generally not necessary.