from typing import Tuple
from loguru import logger
from cam_control.data_type import Point2D, Point3D
import numpy as np
from numpy.linalg import norm


class NeighborSolver:
    def __init__(self, n_observed_agents: int, eps: float):
        self.visited_agents = np.zeros(n_observed_agents)
        self.eps = eps


    def determine_next_position(self, cur_pos: Point2D, agents: np.ndarray[Point2D]) -> Point2D:
        """
        Args:
            cur_pos: Tuple[float, float]
            agents: np.ndarray[Point2D]
        Returns: Tuple[float] (x,y)
        """

        agent_index, closest_point = self._find_closest_agent(np.array(cur_pos), agents)
        if agent_index is None:
            return cur_pos
        self._update_visited_agents(agent_index, agents[agent_index], cur_pos)
        logger.debug(f"Moving to agent #{agent_index} with position {closest_point}")
        return closest_point

    def get_number_of_unvisited_agents(self):
        return np.sum(self.visited_agents == 0)

    def _find_closest_agent(self, point: Point2D, agents: np.ndarray[Point2D]) -> Point2D:
        unvisited_agents_index = np.where(self.visited_agents == 0)[0]
        unvisited_agents = agents[unvisited_agents_index]

        if len(unvisited_agents) == 0:
            return None, None

        dist = norm(point - unvisited_agents, axis=1)
        min_dist_index_unvisited = np.argmin(dist)
        min_dist_index = unvisited_agents_index[min_dist_index_unvisited]


        # min_dist = np.inf
        #
        # for i, agent_pos in enumerate(unvisited_agents):
        #     dist = norm(point - agent_pos)
        #
        #     if dist < min_dist:
        #         min_dist = dist
        #         min_dist_index = unvisited_agents_index[i]

        return min_dist_index, agents[min_dist_index]

    def _update_visited_agents(self, closest_agent_index: int, closest_agent_loc: Point2D, cur_point: Point2D):
        if self._close_enough(closest_agent_loc, cur_point):
            self.visited_agents[closest_agent_index] = 1

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
