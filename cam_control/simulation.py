import numpy as np

from cam_simulation.diplomagm.main_without_app import FOVCalculator
from plot import Plotter


class CamSimulation:
    def __init__(self):
        self.fov_calculator = FOVCalculator()
        self.plotter = Plotter(field_size=self.fov_calculator.get_field_size())

    def simulate(self):
        time = 0
        delta_yaw, delta_pitch = 0.5, 0.0
        while True:
            current_yaw, current_pitch = self.fov_calculator.get_rotation_coords()
            camera_properties = {"yaw": current_yaw + delta_yaw, "pitch": current_pitch + delta_pitch}
            fov_points = self.fov_calculator.get_points_of_fov(camera_properties)[0]
            # observed_objects_positions = self.player_sim.get_positions(time)
            observed_objects_positions = np.array([[1, 1], [2, 2], [3, 3], [4, 16]])
            self.plotter.plot(fov_points, observed_objects_positions, camera_properties=camera_properties)

            print(f"{camera_properties}")
            time += 1


if __name__ == '__main__':
    cam_simulation = CamSimulation()
    cam_simulation.simulate()
