from cam_simulation.diplomagm.main_without_app import FOVCalculator
import matplotlib.pyplot as plt
import numpy as np


class Plotter:

    def __init__(self):
        self.fov_calculator = FOVCalculator()

    def plot(self):
        fig, ax = plt.subplots()  # Create a figure and axes object
        self.plot_fov(ax)
        self.plot_field(ax)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

    def plot_fov(self, ax):
        points = self.fov_calculator.get_points_of_fov()[0]
        for i in range(len(points)):
            ax.scatter(points[i][0], points[i][1], c='r', marker='o')
            ax.plot([points[i][0], points[(i + 1) % len(points)][0]],
                    [points[i][1], points[(i + 1) % len(points)][1]], c='b')

    def plot_field(self, ax):
        height, width = self.fov_calculator.get_points_of_field()
        # Calculate other corners of the rectangle
        top_right = (height + width, height)
        bottom_left = (height, height - width)
        bottom_right = (height + width, height - width)

        # Plot rectangle edges
        ax.plot([height, top_right[0]], [height, height], c='g')  # Top edge
        ax.plot([top_right[0], top_right[0]], [height, bottom_right[1]], c='g')  # Right edge
        ax.plot([top_right[0], height], [bottom_right[1], bottom_left[1]], c='g')  # Bottom edge
        ax.plot([height, height], [bottom_left[1], height], c='g')  # Left edge


if __name__ == '__main__':
    plotter = Plotter()
    plotter.plot()
