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
        """
        Solves the TSP for a given frame of the top view track data.

        Parameters:
        -----------
        top_view_track_df: pd.DataFrame
            A pandas dataframe containing the top view track data.
        frame_index: int, optional
            The index of the frame for which to solve the TSP. The default is 2.

        Returns:
        --------
        permutation: List[int]
            A list of IDs in the order of the TSP tour.
        distance: float
            The distance of the TSP tour.
        """

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

        return permutation, distance

    def _get_coord_list(self, frame: pd.DataFrame) -> list:
        """
        Retrieve list of coordinates from a dataframe
        Args:
            frame (pd.DataFrame):  Coordinate Position Movement

        Returns:
            coordinate_list (List): list of coordinates
        """
        coordinate_list = [[self.center[0], self.center[1]]]
        x = np.array(frame['x'])
        y = np.array(frame['y'])
        for i in range(len(frame)):
            coordinate_list.append([x[i], y[i]])
        return coordinate_list

    def _find_dist(self, coordinates: list) -> np.ndarray:
        """
        Calculates the Distance Matrix
        Args:
            coordinates: List of lists of coordinates (x,y)

        Returns:
            dist_matrix (np.ndarray): distance matrix
        """
        n = len(coordinates)
        dist_matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                dist_matrix[i][j] = np.sqrt(
                    (coordinates[i][0] - coordinates[j][0]) ** 2 + (coordinates[i][1] - coordinates[j][1]) ** 2)

        return dist_matrix
