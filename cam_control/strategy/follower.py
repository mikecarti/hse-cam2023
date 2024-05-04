from typing import Tuple, List, Dict, Union
import numpy as np
from numpy.linalg import norm
from strategy.core import Strategy
from math import atan
import math
from loguru import logger
from queue import Queue

from cam_control.strategy.strategy import CameraMovementStrategy

Point2D = Tuple[float, float] | np.array
Point3D = Tuple[float, float, float] | np.array


class FollowerStrategy(CameraMovementStrategy):
    def __init__(self, field_size: Tuple[float, float], field_loc: Point2D, cam_pos: Point3D,
                 focal_length: float, image_sensor: Dict):
        super().__init__(field_size=field_size, field_loc=field_loc,
                         cam_pos=cam_pos, focal_length=focal_length, image_sensor=image_sensor)

        self.current_pos = [0, 0]
        self.target_pos = [0, 0]

    def move(self, fov_corners: List[Point2D], yaw: float, pitch: float, to: Point2D) \
            -> Tuple[float, float]:
        """
        Calculates the delta movement of the camera angle: yaw and pitch.

        Args:
            fov_corners (List[Point2D]): Corners of the field of view.
            yaw (float): Current yaw of the camera.
            pitch (float): Current pitch of the camera.

        Returns:
            Tuple[float, float]: Delta yaw and delta pitch.
        """
        corner1, corner2 = np.array(fov_corners)[self.furthest_corners]
        principal_axis_intersection = (corner1[0] + corner2[0]) / 2, (corner1[1] + corner2[1]) / 2

        if self._close_enough(principal_axis_intersection, self.target_pos):
            logger.warning(f"Follower strategy reached destination: {self.target_pos}")

        if self.gradual_movement.empty():
        self._plan_gradual_movement(principal_axis_intersection, )
            intermediate_target_pos = self.gradual_movement.get(block=True)
        self.current_pos = intermediate_target_pos  # or maybe = principal_axis_intersection

        delta_yaw, delta_pitch = self._move(intermediate_target_pos, principal_axis_intersection, yaw, pitch)
        return delta_yaw, delta_pitch


    def is_target_reached(self):
        return self._close_enough(self.current_pos, self.target_pos)
