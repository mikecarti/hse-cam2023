from typing import Tuple, List

import numpy as np
import pandas as pd
from loguru import logger

from python_tsp.exact import solve_tsp_dynamic_programming


class StaticTSPSolver:
    def __init__(self, top_view_center: np.ndarray):
        # TSP starts at the center of a field and ends there.
        self.center = top_view_center

    def solve(self, top_view_track_df: pd.DataFrame, frame_index: int = 2):
        logger.info(f"Solving TSP for frame #{frame_index}")

        frame_num = top_view_track_df.query(f"frame == {frame_index}")
        d = self._find_dist(self._get_coord_list(frame_num))
        permutation, distance = solve_tsp_dynamic_programming(d)
        ids = np.array(frame_num['id'])
        ids = np.insert(ids, 0, 0)

        # output is a list of id's of the correct order of permutation
        for i in range(len(permutation)):
            permutation[i] = int(ids[permutation[i]])
        logger.info(f"Permutations: {permutation}")
        logger.info(f"Shortest path distance: {distance}")

    def _get_coord_list(self, frame):
        coordinate_list = [[self.center[0], self.center[1]]]
        x = np.array(frame['x'])
        y = np.array(frame['y'])
        for i in range(len(frame)):
            coordinate_list.append([x[i], y[i]])
        return coordinate_list

    def _find_dist(self, coordinates):
        n = len(coordinates)
        dist_matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                dist_matrix[i][j] = np.sqrt(
                    (coordinates[i][0] - coordinates[j][0]) ** 2 + (coordinates[i][1] - coordinates[j][1]) ** 2)

        return dist_matrix
