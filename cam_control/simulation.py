import numpy as np

from cam_simulation.diplomagm.main_without_app import FOVCalculator
from plot import Plotter


class CamSimulation:
    def __init__(self):
        self.fov_calculator = FOVCalculator()
        self.plotter = Plotter()

    def simulate(self):
        field_size = self.fov_calculator.get_field_size()
        self.plotter.set_field_size(field_size)

        while True:
            fov_points = self.fov_calculator.get_points_of_fov()[0]
            # observed_objects_positions = self.player_sim.get_positions()
            observed_objects_positions = np.array([[1,1], [2,2], [3,3], [4,16]])
            self.plotter.plot(fov_points, observed_objects_positions)



if __name__ == '__main__':
    cam_simulation = CamSimulation()
    cam_simulation.simulate()
