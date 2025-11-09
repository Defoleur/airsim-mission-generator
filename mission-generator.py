import math
import cosysairsim as airsim

class MissionGenerator:
    def __init__(self, client, rng_x, rng_y, obstacle_move_x, obstacle_move_y, obstacle_name, obstacle_scale):
        self.client = client
        self.rng_x = rng_x
        self.rng_y = rng_y
        self.obstacle_move_x = obstacle_move_x
        self.obstacle_move_y = obstacle_move_y
        self.obstacle_name_prefix = obstacle_name
        self.obstacle_scale = obstacle_scale

        self.spawned_obstacle_names = []
        self.obstacle_positions = []
        self.obstacle_movement_vectors = []
        self.current_obstacle_count = 0

    @staticmethod
    def get_distance(point1, point2):
        return math.dist(point1, point2)

    def spawn_obstacles(self, params):
        self.clear_obstacles()

        self.current_obstacle_count = params["obstacle_count"]
        obstacle_x_range = params["obstacle_x_range"]
        obstacle_y_range = params["obstacle_y_range"]

        for i in range(self.current_obstacle_count):
            while True:
                collision = False
                current_obstacle_point = (
                    self.rng_x.uniform(obstacle_x_range[0], obstacle_x_range[1]),
                    self.rng_y.uniform(obstacle_y_range[0], obstacle_y_range[1])
                )
                obstacle_pose_vec = airsim.Vector3r(current_obstacle_point[0],
                                                    current_obstacle_point[1], 0)
                obstacle_pose = airsim.Pose(obstacle_pose_vec)

                for pos in self.obstacle_positions:
                    if self.get_distance(pos, current_obstacle_point) < 5:
                        collision = True
                        break

                if not collision:
                    break

            self.obstacle_positions.append(current_obstacle_point)

            self.obstacle_movement_vectors.append(
                (self.obstacle_move_x.uniform(-0.5, 0.5), self.obstacle_move_y.uniform(-0.5, 0.5))
            )

            current_obstacle_name = f"{self.obstacle_name_prefix}_{i}"
            self.client.simSpawnObject(current_obstacle_name, "Cube", obstacle_pose, self.obstacle_scale,
                                       physics_enabled=False)

            self.spawned_obstacle_names.append(current_obstacle_name)

    def clear_obstacles(self):
        for name in self.spawned_obstacle_names:
            try:
                self.client.simDestroyObject(name)
            except Exception as e:
                print(f"Warning: Could not destroy object {name}. Error: {e}")

        # Очищуємо списки
        self.spawned_obstacle_names = []
        self.obstacle_positions = []
        self.obstacle_movement_vectors = []
        self.current_obstacle_count = 0

    def __del__(self):
        self.clear_obstacles()