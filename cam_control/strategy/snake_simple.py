from typing import Tuple
import numpy as np
from enum import Enum
from loguru import logger
from strategy.utils import calc_corners
from strategy.core import Strategy


class Direction(Enum):
    UP = "w"
    LEFT = "a"
    DOWN = "s"
    RIGHT = "d"


class SnakeStrategySimple(Strategy):
    def __init__(self, field_size: Tuple[float, float], field_loc: Tuple[float, float]):
        super().__init__(field_size=field_size, field_loc=field_loc)

        self.direction = Direction.LEFT
        self._change_direction(Direction.RIGHT)

        self.min_margin = 2
        self.delta_yaw = 0.1
        self.delta_pitch = 0.1
        self.went_up_iterations_in_a_row = 0
        self.max_iter_up_in_a_row = 100

        self.prev_direction = None
        self.furthest_corners = [1, 2]

    def move(self, fov_points: np.ndarray, yaw: float, pitch: float, t: int) -> Tuple[float, float]:
        """
        Calculates the delta movement of the camera angle: yaw and pitch
        """
        fov_points = fov_points[self.furthest_corners, :2]
        self.step = t

        if self.direction == Direction.RIGHT:
            margin_from_border = self._distance_between_closest_point_and_line(self.right_border, fov_points)
            if margin_from_border < self.min_margin:
                self._change_direction(Direction.UP)
        elif self.direction == Direction.UP:
            margin_from_border = self._distance_between_closest_point_and_line(self.top_border, fov_points)
            if self.went_up_iterations_in_a_row > self.max_iter_up_in_a_row:
                self._change_direction(self._opposite_of_prev_direction())
                self.went_up_iterations_in_a_row = 0
            elif margin_from_border < self.min_margin and self.prev_direction:
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

        # logger.debug(f"{t}: Going in {self.direction.name} direction")

        return self._determine_delta_rotation(fov_points, yaw, pitch)

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

        logger.debug(f"{self.step}: Changing direction to {self.direction.name}")
        return to
