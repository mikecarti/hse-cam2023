import os
import sys

current_dir = os.getcwd()
cam_dir = current_dir + "/cam_control"
sys.path.append(cam_dir)
cam_sim = cam_dir + "/cam_simulation/diplomagm"
sys.path.append(cam_sim)

from player_detect import PlayerDetector
from strategy.snake_strict import SnakeStrategyStrict
from cam_simulation.diplomagm.main_without_app import FOVCalculator
from plot import Plotter
from loguru import logger
from mock_player_sim import MockPlayerSim


class CamSimulation:
    def __init__(self):
        self.fov_calculator = FOVCalculator()
        field_size = self.fov_calculator.get_field_size()
        field_loc = self.fov_calculator.get_field_loc()
        image_sensor = self.fov_calculator.get_image_sensor()
        self.cam_pos = self.fov_calculator.get_cam_pos()
        self.focal_length=self.fov_calculator.get_focal_length()
        logger.debug(f"Cam pos: {self.cam_pos}, focal length: {self.focal_length}")
        self.strategy = SnakeStrategyStrict(field_size, field_loc, self.cam_pos, self.focal_length, image_sensor)
        self.plotter = Plotter(field_size=field_size, field_loc=field_loc, trajectory=self.strategy.get_trajectory())
        self.player_detector = PlayerDetector()
        self.player_sim = MockPlayerSim(field_size, field_loc)

        self.log_angles = True
        self.log_players = True
        self.field_size = field_size

    def simulate(self):
        time = 0
        delta_yaw, delta_pitch = 0, 0
        zoom = 1
        yaw, pitch = self.fov_calculator.get_rotation_coords()

        while True:
            yaw += delta_yaw
            pitch += delta_pitch
            camera_properties = {"yaw": yaw % 360.0, "pitch": pitch % 360.0, "zoom": zoom}

            fov_points = self.fov_calculator.get_points_of_fov(camera_properties)[0]
            delta_yaw, delta_pitch = self.strategy.move(fov_points, yaw, pitch)

            observed_objects_positions = self.player_sim.get_positions(time)
            players_inside_fov = self.player_detector.which_players_inside_fov(observed_objects_positions, fov_points)
            self.plotter.plot(fov_points, observed_objects_positions, camera_properties=camera_properties)

            if self.log_angles:
                logger.info(f"{camera_properties}")
            if self.log_players:
                logger.info(f"Players that are inside FOV: {players_inside_fov}")

            time += 1


if __name__ == '__main__':
    cam_simulation = CamSimulation()
    cam_simulation.simulate()
