from cam_control.strategy.strategy import CameraMovementStrategy
import numpy as np
from typing import Tuple, List, Dict
from loguru import logger
from cam_control.data_type import Point2D, Point3D


class TrajectoryStrategy(CameraMovementStrategy):
    SNAKE_TRAJECTORY = np.array([[60, 0], [90, 0], [90, 20], [60, 20], [60, 40],
                                 [90, 40], [90, 60], [60, 60], [60, 80], [90, 80]])

    def __init__(self, field_size: Tuple[float, float], field_loc: Point2D, cam_pos: Point3D,
                 focal_length: float, image_sensor: Dict, trajectory: np.ndarray = SNAKE_TRAJECTORY):
        super().__init__(field_size=field_size, field_loc=field_loc,
                         cam_pos=cam_pos, focal_length=focal_length, image_sensor=image_sensor)

        self.trajectory = trajectory
        self.trajectory = np.concatenate([self.trajectory, self.trajectory[::-1]])
        self._change_target_pos(cam_pos[:2])

    def get_trajectory(self) -> np.array:
        """
        Get the trajectory of the camera movement.

        Returns:
            np.array: Trajectory of the camera movement.
        """
        return self.trajectory

    def move(self, fov_corners: List[Point2D], yaw: float, pitch: float) \
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

        if self._close_enough(principal_axis_intersection, self.curr_target_pos):
            self._change_target_pos()

        intermediate_target_pos = self.gradual_movement.get(block=True)

        delta_yaw, delta_pitch = self._move(intermediate_target_pos, principal_axis_intersection, yaw, pitch)
        return delta_yaw, delta_pitch

    def _change_target_pos(self, prev_target_pos: Point2D = None) -> None:
        """
        Change the target position for the camera movement.

        Args:
            prev_target_pos (Point2D, optional): Previous target position. Defaults to None.
        """
        if prev_target_pos is None:
            self.prev_target_pos = self.curr_target_pos
        else:
            self.prev_target_pos = prev_target_pos

        self.step = (self.step + 1) % len(self.trajectory)
        self.curr_target_pos = self.trajectory[self.step]
        self.gradual_movement.empty()

        self._plan_gradual_movement(self.prev_target_pos, self.curr_target_pos)
        logger.info(f"Switched to target position: {self.curr_target_pos}")

