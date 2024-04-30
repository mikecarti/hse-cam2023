from typing import Tuple, Dict

from cam_simulation.diplomagm.main_without_app import FOVCalculator
import matplotlib.pyplot as plt
import numpy as np


class Plotter:

    def __init__(self, field_size: Tuple[float, float]):
        self.fig, self.ax = plt.subplots()

        self.field_size = field_size
        self.plot_field()
        self.fov_calculator = FOVCalculator()

        self.legend = None
        self.lines = []
        self.dots = []

    def plot(self, fov_points, observed_objects_positions: np.ndarray,
             camera_properties: Dict) -> None:
        """
        Plot the field of view and the observed objects.

        :param fov_points: Field of view points.
        :param observed_objects_positions: Observed objects positions. Matrix of shape 2xn,
        where n is the number of observed objects
        """
        yaw, pitch = camera_properties["yaw"], camera_properties["pitch"]

        # TODO: refactor ax
        self._clear_irrelevant()
        self.plot_fov(fov_points)
        self.plot_agents(observed_objects_positions)
        # self.plot_legend(yaw, pitch)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.axis('scaled')

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
        height, width = self.field_size
        # Calculate other corners of the rectangle
        top_right = (height + width, height)
        bottom_left = (height, height - width)
        bottom_right = (height + width, height - width)

        # Plot rectangle edges
        ax.plot([height, top_right[0]], [height, height], c='g')  # Top edge
        ax.plot([top_right[0], top_right[0]], [height, bottom_right[1]], c='g')  # Right edge
        ax.plot([top_right[0], height], [bottom_right[1], bottom_left[1]], c='g')  # Bottom edge
        ax.plot([height, height], [bottom_left[1], height], c='g')  # Left edge

    def plot_agents(self, observed_objects_positions: np.ndarray):
        pass

    def plot_legend(self, yaw, pitch):
        ax = self.ax

        # Create a legend
        legend_label = "yaw = {}, pitch = {}".format(yaw, pitch)
        ax.plot([], [], label=legend_label)  # Assuming x_data, y_data are your plotting data
        # Display the legend on the plot
        self.legend = ax.legend()
