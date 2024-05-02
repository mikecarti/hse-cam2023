from typing import Tuple

from numpy.linalg import norm
import numpy as np

from cam_control.strategy.utils import calc_corners


class Strategy:
    def __init__(self, field_size: Tuple[float, float], field_loc: Tuple[float, float]):
        self.width, self.height = field_size
        self.step = 0

        self.bottom_left, self.bottom_right, self.top_left, self.top_right = (
            calc_corners(width=self.width, height=self.height, loc=field_loc))
        self.top_border = np.array((self.top_left, self.top_right))
        self.bottom_border = np.array((self.bottom_left, self.bottom_right))
        self.left_border = np.array((self.top_left, self.bottom_left))
        self.right_border = np.array((self.top_right, self.bottom_right))

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
            d = norm(np.cross(p2 - p1, p1 - point)) / norm(p2 - p1)
            distances.append(d)
        # logger.debug(f"Distances between points: {distances}, {min(distances)}")
        return min(distances)
