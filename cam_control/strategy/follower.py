from typing import Tuple, List, Dict, Callable
import numpy as np
from loguru import logger
from queue import Queue
from numpy.linalg import norm
from shapely.geometry import Polygon

from cam_control.data_type import Point2D, Point3D
from cam_control.strategy.strategy import CameraMovementStrategy


class FollowerStrategy(CameraMovementStrategy):
    def __init__(self, field_size: Tuple[float, float], field_loc: Point2D, cam_pos: Point3D,
                 focal_length: float, image_sensor: Dict, cam_aim_func: Callable, eps: float):
        super().__init__(field_size=field_size, field_loc=field_loc,
                         cam_pos=cam_pos, focal_length=focal_length, image_sensor=image_sensor, eps=eps)

        self.cam_aim = cam_aim_func
        self.intermediate_target_pos = [0, 0]
        self.target_pos = [0, 0]

        # Given fps = 25, and speed is in meters
        # then camera should be able to traverse a field in 5 seconds
        # therefore if a field length is 100, it is 20 meters in 1 second,
        # that is 0.8 meters in 1/25 seconds
        self.speed_meters_per_tick = 0.8

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
        self.target_pos = to
        cur_pos = self.cam_aim(fov_corners)

        logger.debug(f"Current position of camera aim: {cur_pos}")
        if self.is_target_reached(cur_pos):
            logger.warning(f"Follower strategy finished traversing at position: {self.target_pos}")
        #     return 0, 0

        self.intermediate_target_pos = self._get_next_intermediate_target(cur_pos, self.target_pos)

        delta_yaw, delta_pitch = self._move(cur_pos=cur_pos, target_pos=self.intermediate_target_pos,
                                            yaw=yaw, pitch=pitch)
        return delta_yaw, delta_pitch

    def is_target_reached(self, cur_pos: Point2D):
        return self._close_enough(cur_pos, self.target_pos)


    def _plan_gradual_movement(self, cur_pos: Point2D, target_pos: Point2D) -> Queue:
        self.gradual_movement.empty()
        distance = norm(cur_pos - target_pos)
        n_iterations = distance / self.speed_meters_per_tick
        n_steps = int(max(n_iterations, 2))
        logger.debug(f"traversing distance {distance} meters in # of iterations: {n_steps} and # of seconds: {n_steps / 25}")

        lin_space = np.linspace(cur_pos, target_pos, n_steps)
        self.final_target = target_pos
        for point in lin_space:
            self.gradual_movement.put(point)
        return self.gradual_movement

    def _get_next_intermediate_target(self, cur_pos, target_pos):
        if self.gradual_movement.empty():
            self._plan_gradual_movement(cur_pos, target_pos)
        intermediate_target_pos = self.gradual_movement.get(block=False)
        return intermediate_target_pos
