from typing import Tuple

from cam_control.data_type import Point2D, Point3D
import numpy as np
from numpy.linalg import norm


class KNNSolver:
    def __init__(self, n_observed_agents: int):
        self.visited_agents = np.zeros(n_observed_agents)

    def determine_next_position(self, cur_pos: Point2D, agents: np.ndarray[Point2D]) -> Point2D:
        """
        Args:
            cur_pos: Tuple[float, float]
            agents: np.ndarray[Point2D]
        Returns: Tuple[float] (x,y)
        """

        agent_index, closest_point = self._find_closest_agent(np.array(cur_pos), agents)
        self._update_visited_agents(agent_index, agent_loc=agents[agent_index], closest_point=closest_point)
        return closest_point

    def _find_closest_agent(self, point: Point2D, agents: np.ndarray[Point2D]) -> Point2D:
        unvisited_agents_index = np.where(self.visited_agents != 0, agents)
        unvisited_agents = agents[unvisited_agents_index]

        assert len(unvisited_agents) != 0

        min_dist = np.inf
        min_dist_index = -1
        for i, agent_pos in enumerate(unvisited_agents):
            dist = norm(point - agent_pos)

            if dist < min_dist:
                min_dist = dist
                min_dist_index = unvisited_agents_index[i]

        return min_dist, min_dist_index

    def _update_visited_agents(self, agent_index: int, agent_loc: Point2D, closest_point: Point2D):
        if self._close_enough(agent_loc, closest_point):
            self.visited_agents[agent_index] = 1

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
        eps = 0.1
        return dist < eps
