import os
import sys

import numpy as np

from cam_control.player_detect import PlayerDetector
from cam_control.strategy import SnakeStrategy
from cam_simulation.diplomagm.main_without_app import FOVCalculator
from plot import Plotter
from loguru import logger

current_dir = os.getcwd()
sys.path.append(current_dir + "/cam_control")

class CamSimulation:
    def __init__(self):
        self.fov_calculator = FOVCalculator()
        field_size = self.fov_calculator.get_field_size()
        self.plotter = Plotter(field_size=field_size)
        self.player_detector = PlayerDetector()
        self.strategy = SnakeStrategy(field_size=field_size)

    def simulate(self, observed_objects_positions: np.ndarray):
        time = 0
        delta_yaw, delta_pitch = 0, 0
        current_yaw, current_pitch = self.fov_calculator.get_rotation_coords()
        camera_properties = {"yaw": current_yaw, "pitch": current_pitch}

        while True:
            current_yaw, current_pitch = self.fov_calculator.get_rotation_coords()
            camera_properties = {"yaw": current_yaw + delta_yaw, "pitch": current_pitch + delta_pitch}
            fov_points = self.fov_calculator.get_points_of_fov(camera_properties)[0]
            delta_yaw, delta_pitch = self.strategy.move(fov_points, current_yaw, current_pitch, 0)

            observed_objects_positions = np.array([[25, 25], [45, 25], [65, 25], [85, 25]])
            players_inside_fov = self.player_detector.which_players_inside_fov(observed_objects_positions, fov_points)
            logger.info(f"Players that are inside FOV: {players_inside_fov}")
            # observed_objects_positions = self.player_sim.get_positions(time)
            self.plotter.plot(fov_points, observed_objects_positions, camera_properties=camera_properties)

            logger.info(f"{camera_properties}")
            time += 1




if __name__ == '__main__':
    cam_simulation = CamSimulation()
    cam_simulation.simulate([])
