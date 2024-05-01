import numpy as np
from typing import Tuple


class PlayerDetector:
    def __init__(self):
        pass

    def get_players_inside_fov(self, player_positions: np.ndarray, fov_points: np.ndarray):
        self.fov_points = fov_points
        are_players_inside = np.array([self._is_player_inside_fov(xy) for xy in player_positions])
        return np.where(are_players_inside)

    def _is_player_inside_fov(self, xy: Tuple[int, int]) -> bool:
        return self._is_within_polygon(polygon=self.fov_points, point=xy)

    def _is_within_polygon(self, polygon, point):
        polygon = np.array(polygon)

        A = -(polygon[:, 1] - np.roll(polygon[:, 1], -1))
        B = polygon[:, 0] - np.roll(polygon[:, 0], -1)
        C = -(A * polygon[:, 0] + B * polygon[:, 1])

        x, y = point

        D = A * x + B * y + C

        return np.any(D >= 0) or np.any(D <= 0)
