from typing import Tuple
import numpy as np
from enum import Enum
from utils import calc_corners
from numpy.linalg import norm


class Direction(Enum):
    UP = "w"
    LEFT = "a"
    DOWN = "s"
    RIGHT = "d"


class Strategy:
    pass


class SnakeStrategy(Strategy):
    def __init__(self, field_size: Tuple[float, float]):
        self.width, self.height = field_size
        self.direction = Direction.RIGHT

        self.bottom_left, self.bottom_right, self.top_left, self.top_right = (
            calc_corners(width=self.width, height=self.height))
        self.top_border = np.array((self.top_left, self.top_right))
        self.bottom_border = np.array((self.bottom_left, self.bottom_right))
        self.left_border = np.array((self.top_left, self.bottom_left))
        self.right_border = np.array((self.top_right, self.bottom_right))

        self.min_margin = 10
        self.delta_yaw = 0.1
        self.delta_pitch = 0.1
        self.went_up_iterations_in_a_row = 0
        self.max_iter_up_in_a_row = 500

        self.prev_direction = None

    def move(self, fov_points: np.ndarray, yaw: float, pitch: float, t: float) -> Tuple[float, float]:
        """
        Calculates the delta movement of the camera angle: yaw and pitch
        """
        fov_points = fov_points[:, :2]

        if self.direction == Direction.RIGHT:
            margin_from_border = self._distance_between_closest_point_and_line(self.right_border, fov_points)
            if margin_from_border < self.min_margin:
                self._change_direction(Direction.UP)
        elif self.direction == Direction.UP:
            margin_from_border = self._distance_between_closest_point_and_line(self.top_border, fov_points)
            if self.went_up_iterations_in_a_row > self.max_iter_up_in_a_row:
                self._change_direction(self._opposite_of_prev_direction())
                self.went_up_iterations_in_a_row = 0
            elif margin_from_border < self.min_margin:
                return 0, 0
            else:
                self.went_up_iterations_in_a_row += 1
        elif self.direction == Direction.DOWN:
            margin_from_border = self._distance_between_closest_point_and_line(self.bottom_border, fov_points)
            if margin_from_border < self.min_margin:
                self._change_direction(Direction.LEFT)
        elif self.direction == Direction.LEFT:
            margin_from_border = self._distance_between_closest_point_and_line(self.left_border, fov_points)
            if margin_from_border < self.min_margin:
                self._change_direction(Direction.UP)
        else:
            raise ValueError(f"Invalid direction: {self.direction}")

        return self._determine_delta_rotation(fov_points, yaw, pitch)

    def _distance_between_closest_point_and_line(self, line: np.ndarray, points: np.ndarray) -> float:
        """
        Calculate the minimum distance between points and a line.

        Args:
        - line: An array of shape (2, 2) representing a line segment defined by two points.
        - points: An array of shape (2, k) representing k points.

        Returns:
        - The minimum distance from any point in `points` to the line.
        """

        p1 = line[0, :]
        p2 = line[1, :]

        distances = []
        for point in points:
            d = norm(np.cross(p2 - p1, line[0, :] - point)) / norm(p2 - p1)
            distances.append(d)
        return min(distances)

    def _determine_delta_rotation(self, fov_points, yaw, pitch) -> Tuple[float, float]:
        if self.direction == Direction.UP:
            return self.delta_yaw, 0
        elif self.direction == Direction.DOWN:
            return -self.delta_yaw, 0
        elif self.direction == Direction.LEFT:
            return 0, self.delta_pitch
        elif self.direction == Direction.RIGHT:
            return 0, -self.delta_pitch
        else:
            raise ValueError(f"Unknown direction: {self.direction}")

    def _opposite_of_prev_direction(self):
        if self.prev_direction == Direction.RIGHT:
            return Direction.LEFT
        elif self.prev_direction == Direction.LEFT:
            return Direction.RIGHT
        else:
            raise ValueError(f"Function does not support previous direction: {self.prev_direction}")

    def _change_direction(self, to):
        self.prev_direction = self.direction
        self.direction = to

        if to == Direction.UP:
            self.went_up_iterations_in_a_row = 0
        return to
