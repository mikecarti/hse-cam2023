from typing import Tuple, List, Dict
import numpy as np
from numpy.linalg import norm
from strategy.core import Strategy
from time import sleep
from math import sqrt, acos, atan, atan2, degrees
import math
from loguru import logger

Point2D = Tuple[float, float] | np.array
Point3D = Tuple[float, float, float] | np.array


class SnakeStrategyStrict(Strategy):
    def __init__(self, field_size: Tuple[float, float], field_loc: Point2D, cam_pos: Point3D,
                 focal_length: float, image_sensor: Dict):
        super().__init__(field_size=field_size, field_loc=field_loc)
        self.trajectory = np.array([
            [60, 0],
            [90, 0], [90, 20], [60, 20], [60, 40],
            [90, 40], [90, 60], [60, 60], [60, 80],
            [90, 80]
        ])
        self.trajectory = np.concatenate([self.trajectory, self.trajectory[::-1]])
        self.curr_target_pos = self.trajectory[0]

        self.vert_aov = self._calculate_vert_aov(focal_length, image_sensor["height"], image_sensor["width"])

        self.furthest_corners = [1, 2]
        self.debug = False
        self.cam_pos = cam_pos

    def get_trajectory(self):
        return self.trajectory

    def move(self, fov_corners: List[Point2D], yaw: float, pitch: float) \
            -> Tuple[float, float]:
        """
        Calculates the delta movement of the camera angle: yaw and pitch
        """
        corner1, corner2 = np.array(fov_corners)[self.furthest_corners]
        principal_axis_intersection = (corner1[0] + corner2[0]) / 2, (corner1[1] + corner2[1]) / 2

        if self._close_enough(principal_axis_intersection, self.curr_target_pos):
            self._change_target_pos()

        return self._move(self.curr_target_pos, principal_axis_intersection, yaw, pitch)

    def _move(self, target_pos: Point2D, principal_axis_intersection: Point2D, yaw: float, pitch: float) \
            -> Tuple[float, float]:
        """
        @param cam_pos: Tuple of size 3, xyz coordinates. Height matters.
        @param principal_axis_intersection: Tuple of size 2, intersection of principal axis of
        projection and the furthest line of the projection
        @param yaw: current yaw of the camera.
        @param pitch: current pitch of the camera.
        @return: Tuple[float, float]
        """
        principal_axis_intersection_target_pos = target_pos
        delta_yaw, delta_pitch = self._calculate_angle(cam_pos=self.cam_pos[:2], cam_height=self.cam_pos[2],
                                                       cam_pitch=pitch, init_pos=principal_axis_intersection,
                                                       target_pos=principal_axis_intersection_target_pos)

        logger.debug(f"Pitch: {pitch}+({delta_pitch}), Yaw: {yaw}+({delta_yaw})")
        logger.debug(f"init_pos: {principal_axis_intersection}, target_pos: {principal_axis_intersection_target_pos}")
        sleep(0.5)
        return delta_yaw, delta_pitch

    def _calculate_angle(self, cam_pos: Point2D, cam_height: float, cam_pitch: float,
                         init_pos: Point2D, target_pos: Point2D):
        top_aov = cam_pitch - self.vert_aov

        cam_x, cam_y = cam_pos
        init_x, init_y = init_pos
        target_x, target_y = target_pos

        init_vec = np.array((init_x - cam_x, init_y - cam_y))
        target_vec = np.array((target_x - cam_x, target_y - cam_y))

        init_vec_angle = self._vector_angle(init_vec)
        target_vec_angle = self._vector_angle(target_vec)

        tan_pitch = norm(target_vec) / norm(cam_height)
        raw_pitch = np.degrees(atan(tan_pitch)) % 360.0
        pitch = 90 - raw_pitch

        delta_yaw = target_vec_angle - init_vec_angle
        delta_pitch = pitch - top_aov

        logger.debug(f"raw_pitch: {raw_pitch}, corrected_pitch: {pitch}, delta_pitch: {delta_pitch}")

        return delta_yaw, delta_pitch

    def _calculate_vert_aov(self, focal_length, height_of_image_sensor, width_of_image_sensor):
        # self.__width_angle_of_view = 2 * math.atan(width_of_image_sensor / 2 / focal_length) * 180 / math.pi
        height_angle_of_view = 2 * math.atan(height_of_image_sensor / 2 / focal_length) * 180 / math.pi
        # AOV_v = 2 * math.degrees(math.atan(cam_height / (2 * focal_length)))
        # Determine angle of the most high-oriented ray
        # angle_of_ray = AOV_v / 2
        # adj_angle_of_ray = angle_of_ray * self.image_sensor_ratio
        logger.info(f"Vertical Angle Of View: {height_angle_of_view / 2}")
        return height_angle_of_view / 2

    def _vector_angle(self, v: np.array):
        """
        @param v:
        @return: Angle in degrees
        """
        return np.degrees(np.arctan2(*v.T[::-1])) % 360.0

    def _close_enough(self, pos_1: Point2D, pos_2: Point2D):
        dist = norm(np.array(pos_1) - np.array(pos_2))
        print(pos_1, pos_2, dist)
        return dist < 0.1

    def _change_target_pos(self):
        self.step = (self.step + 1) % len(self.trajectory)
        self.curr_target_pos = self.trajectory[self.step]
        logger.info(f"Switched to target position: {self.curr_target_pos}")

