from typing import Tuple

from cam_simulation.diplomagm.main_without_app import FOVCalculator
import matplotlib.pyplot as plt
import numpy as np


class Plotter:

    def __init__(self):
        self.fov_calculator = FOVCalculator()

    def plot(self, fov_points, observed_objects_positions: np.ndarray) -> None:
        """
        Plot the field of view and the observed objects.

        :param fov_points: Field of view points.
        :param observed_objects_positions: Observed objects positions. Matrix of shape 2xn,
        where n is the number of observed objects
        """
        fig, ax = plt.subplots()  # Create a figure and axes object
        self.plot_fov(ax, fov_points)
        self.plot_agents(ax, observed_objects_positions)
        self.plot_field(ax)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

    def plot_fov(self, ax, points,color="r"):
        for i in range(len(points)):
            ax.scatter(points[i][0], points[i][1], c=color, marker='o')
            ax.plot([points[i][0], points[(i + 1) % len(points)][0]],
                    [points[i][1], points[(i + 1) % len(points)][1]], c='b')

    def plot_field(self, ax):
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

    def plot_agents(self, ax, observed_objects_positions: np.ndarray):
        pass

    def set_field_size(self, field_size: Tuple[int,int]):
        self.field_size = field_size

