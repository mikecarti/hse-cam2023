from typing import Tuple, Dict

from strategy.utils import calc_corners
from cam_simulation.diplomagm.main_without_app import FOVCalculator
import matplotlib.pyplot as plt
import numpy as np


class Plotter:

    def __init__(self, field_size: Tuple[float, float], field_loc: Tuple[float, float], trajectory: np.ndarray = None):
        self.vis_point_plot = None
        self.unvis_point_plot = None
        self.fig, self.ax = plt.subplots()

        self.field_size = field_size  # (width, height)
        self.field_loc = field_loc  # (x, y)
        self.plot_field()
        self.fov_calculator = FOVCalculator()
        self.ax.set_aspect('equal')
        if trajectory:
            self.plot_points(trajectory, color="r", leave_forever=True)  # trajectory

        self.legend = None
        self.lines = []
        self.dots = []

    def plot(self, fov_points: np.ndarray, observed_objects_positions: np.ndarray, visited_objects: np.array,
             camera_properties: Dict) -> None:
        """
        Args:
            fov_points: np.ndarray of FOV points
            observed_objects_positions: np.ndarray of agents
            visited_objects: np.ndarray[bool]
            camera_properties:

        Returns:

        """
        # yaw, pitch = camera_properties["yaw"], camera_properties["pitch"]

        # TODO: refactor ax
        self._clear_irrelevant()
        self.plot_fov(fov_points)
        self.plot_agents(observed_objects_positions, visited_objects)  # agents
        # self.plot_legend(yaw, pitch)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.axis('scaled')
        self.ax.set_xlim([-20, 150])
        self.ax.set_ylim([-20, 150])
        plt.pause(0.05)

    def plot_fov(self, points, color="r"):
        ax = self.ax

        self.lines = []
        self.dots = []
        for i in range(len(points)):
            dot = ax.scatter(points[i][0], points[i][1], c=color, marker='o')
            line = ax.plot([points[i][0], points[(i + 1) % len(points)][0]],
                           [points[i][1], points[(i + 1) % len(points)][1]], c='b')
            self.dots.append(dot)
            self.lines.append(line)

    def _clear_irrelevant(self):
        assert len(self.dots) == len(self.lines)
        for i in range(len(self.lines)):
            self.dots[i].remove()
            lines = self.lines[i]
            for line in lines:
                line.remove()

        if self.legend:
            self.legend.remove()

    def plot_field(self):
        ax = self.ax
        width, height = self.field_size
        # Calculate other corners of the rectangle
        bottom_left, bottom_right, top_left, top_right = calc_corners(height, width, loc=self.field_loc)

        # Plot rectangle edges
        ax.plot([top_left[0], top_right[0]], [top_left[1], top_right[1]], c='g')
        ax.plot([top_right[0], bottom_right[0]], [top_right[1], bottom_right[1]], c='g')
        ax.plot([bottom_right[0], bottom_left[0]], [bottom_right[1], bottom_left[1]], c='g')
        ax.plot([bottom_left[0], top_left[0]], [bottom_left[1], top_left[1]], c='g')

    def plot_agents(self, observed_objects_positions: np.ndarray,
                    visited_objects: np.array):
        visited_objects_positions = observed_objects_positions[visited_objects == 1]
        unvisited_objects_positions = observed_objects_positions[visited_objects == 0]
        self.plot_points(unvisited_objects_positions, color="b")
        self.plot_points(visited_objects_positions, color="black", visited=True)

    def plot_points(self, observed_objects_positions: np.ndarray, color: str = "b", leave_forever=False,
                    visited=False):
        ax = self.ax

        if visited:
            # Clear previous points if they exist
            if self.vis_point_plot:
                for point in self.vis_point_plot:
                    point.remove()
        else:
            if self.unvis_point_plot:
                for point in self.unvis_point_plot:
                    point.remove()

        x_coords = observed_objects_positions[:, 0]
        y_coords = observed_objects_positions[:, 1]

        # Plot agents with customized line plot
        # Here, linestyle='' means no connecting lines between markers
        point_plot = ax.plot(x_coords, y_coords, marker='o', color=color, linestyle='')

        if not leave_forever:
            if visited:
                self.vis_point_plot = point_plot
            else:
                self.unvis_point_plot = point_plot

    def plot_legend(self, yaw, pitch):
        ax = self.ax

        # Create a legend
        legend_label = "yaw = {}, pitch = {}".format(yaw, pitch)
        ax.plot([], [], label=legend_label)  # Assuming x_data, y_data are your plotting data
        # Display the legend on the plot
        self.legend = ax.legend()

    def __del__(self):
        plt.close(self.fig)
