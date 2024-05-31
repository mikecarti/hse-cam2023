from typing import Tuple, List, Dict
import numpy as np
from numpy.linalg import norm
from strategy.core import Strategy
from math import atan
import math
from loguru import logger
from queue import Queue
from abc import ABC, abstractmethod

Point2D = Tuple[float, float] | np.array
Point3D = Tuple[float, float, float] | np.array


class CameraMovementStrategy(Strategy):
    """
    A strategy class for controlling the movement of a camera in any pattern.

    Args:
        field_size (Tuple[float, float]): Size of the field.
        field_loc (Point2D): Location of the field.
        cam_pos (Point3D): Position of the camera.
        focal_length (float): Focal length of the camera lens.
        image_sensor (Dict): Information about the image sensor.

    Attributes:
        trajectory (np.array): Trajectory of the camera movement.
        step (int): Current step in the trajectory.
        gradual_movement (Queue): Queue for storing gradual movement points.
        vert_aov (float): Vertical angle of view.
        furthest_corners (List[int]): Indices of the furthest corners of the field of view.
        debug (bool): Debug mode flag.
        cam_pos (Point3D): Position of the camera.

    Methods:
        get_trajectory() -> np.array:
            Get the trajectory of the camera movement.
        move(fov_corners: List[Point2D], yaw: float, pitch: float) -> Tuple[float, float]:
            Calculates the delta movement of the camera angle: yaw and pitch.
        _move(target_pos: Point2D, principal_axis_intersection: Point2D, yaw: float, pitch: float) -> Tuple[float, float]:
            Move the camera to the target position.
        _calculate_angle(cam_pos: Point2D, cam_height: float, cam_pitch: float, init_pos: Point2D, target_pos: Point2D) -> Tuple[float, float]:
            Calculate the angle of the camera.
        _calculate_vert_aov(focal_length, height_of_image_sensor, width_of_image_sensor) -> float:
            Calculate the vertical angle of view.
        _vector_angle(v: np.array) -> float:
            Calculate the angle of the vector.
        _close_enough(pos_1: Point2D, pos_2: Point2D) -> bool:
            Check if two positions are close enough.
        _change_target_pos(prev_target_pos: Point2D = None) -> None:
            Change the target position for the camera movement.
    """

    def __init__(self, field_size: Tuple[float, float], field_loc: Point2D, cam_pos: Point3D,
                 focal_length: float, image_sensor: Dict, eps: float):
        super().__init__(field_size=field_size, field_loc=field_loc)
        self.step = -1
        self.eps = eps

        self.gradual_movement = Queue()
        self.vert_aov = self._calculate_vert_aov(focal_length, image_sensor["height"], image_sensor["width"])

        self.furthest_corners = [1, 2]
        self.debug = False
        self.cam_pos = cam_pos

    @abstractmethod
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
        pass

    def _move(self, cur_pos: Point2D, target_pos: Point2D, yaw: float, pitch: float) \
            -> Tuple[float, float]:
        """
        Move the camera to the target position.

        Args:
            target_pos (Point2D): Target position to move the camera.
            cur_pos (Point2D): Middle of FOV Polygon
            yaw (float): Current yaw of the camera.
            pitch (float): Current pitch of the camera.

        Returns:
            Tuple[float, float]: Delta yaw and delta pitch.
        """
        delta_yaw, delta_pitch = self._calculate_angle(cam_pos=self.cam_pos[:2], cam_height=self.cam_pos[2],
                                                       cam_pitch=pitch, init_pos=cur_pos,
                                                       target_pos=target_pos)

        logger.debug(f"Pitch: {pitch}+({delta_pitch}), Yaw: {yaw}+({delta_yaw})")
        logger.debug(f"init_pos: {cur_pos}, target_pos: {target_pos}")
        # sleep(0.5)
        return delta_yaw, delta_pitch

    def _calculate_angle(self, cam_pos: Point2D, cam_height: float, cam_pitch: float,
                         init_pos: Point2D, target_pos: Point2D) -> Tuple[float, float]:
        """
        Calculate the yaw and pitch of the camera to aim at the target position.

        Args:
            cam_pos (Point2D): Camera position in the X-Y plane.
            cam_height (float): Height of the camera above the X-Y plane.
            cam_pitch (float): Current pitch of the camera.
            init_pos (Point2D): Initial position (middle of FOV polygon).
            target_pos (Point2D): Target position.

        Returns:
            Tuple[float, float]: Delta yaw and delta pitch.
        """
        cam_x, cam_y = cam_pos
        target_x, target_y = target_pos

        # Calculate vectors from camera to initial and target positions
        init_vec = np.array([init_pos[0] - cam_x, init_pos[1] - cam_y])
        target_vec = np.array([target_x - cam_x, target_y - cam_y])

        # Calculate angles of these vectors
        init_vec_angle = self._vector_angle(init_vec)
        target_vec_angle = self._vector_angle(target_vec)

        # Calculate delta yaw
        delta_yaw = target_vec_angle - init_vec_angle

        # Calculate the horizontal distance and height difference for pitch
        horizontal_distance = np.linalg.norm(target_vec)
        height_difference = cam_height  # Assuming the camera's height is the height difference

        # Calculate the target pitch angle incorporating vertical AOV
        target_pitch_rad = np.arctan2(height_difference, horizontal_distance)
        target_pitch_deg = np.degrees(target_pitch_rad)

        # Adjust the target pitch with the vertical angle of view
        corrected_target_pitch = target_pitch_deg + (self.vert_aov / 2)

        # Calculate the delta pitch
        delta_pitch = corrected_target_pitch - cam_pitch

        # Logging for debugging
        logger.debug(f"cam_pos: {cam_pos}, target_pos: {target_pos}")
        logger.debug(f"horizontal_distance: {horizontal_distance}, height_difference: {height_difference}")
        logger.debug(f"target_pitch_rad: {target_pitch_rad}, target_pitch_deg: {target_pitch_deg}")
        logger.debug(f"corrected_target_pitch: {corrected_target_pitch}, delta_pitch: {delta_pitch}")

        return delta_yaw, delta_pitch

    def _calculate_vert_aov(self, focal_length: float, height_of_image_sensor: float,
                            width_of_image_sensor: float) -> float:
        """
        Calculate the vertical angle of view.

        Args:
            focal_length (float): Focal length of the camera lens.
            height_of_image_sensor (float): Height of the image sensor.
            width_of_image_sensor (float): Width of the image sensor.

        Returns:
            float: Vertical angle of view.
        """
        height_angle_of_view = 2 * math.atan(height_of_image_sensor / 2 / focal_length) * 180 / math.pi
        logger.info(f"Vertical Angle Of View: {height_angle_of_view / 2}")
        return height_angle_of_view / 2

    def _vector_angle(self, v: np.array) -> float:
        """
        Calculate the angle of the vector.

        Args:
            v (np.array): Vector.

        Returns:
            float: Angle in degrees.
        """
        return np.degrees(np.arctan2(*v.T[::-1])) % 360.0

    def _close_enough(self, pos_1: Point2D, pos_2: Point2D) -> bool:
        """
        Check if two positions are close enough.

        Args:
            pos_1 (Point2D): First position.
            pos_2 (Point2D): Second position.

        Returns:
            bool: True if positions are close enough, False otherwise.
        """
        dist = norm(np.array(pos_1) - np.array(pos_2))
        return dist < self.eps

    def _plan_gradual_movement(self, curr_pos: Point2D, target_pos: Point2D) -> Queue:
        self.gradual_movement.empty()

        n_steps = int(norm(curr_pos, target_pos))
        print(n_steps)
        lin_space = np.linspace(curr_pos, target_pos, n_steps)
        for point in lin_space:
            self.gradual_movement.put(point)
        return self.gradual_movement
