import os
import sys

from cam_control.cam_aim import calc_fov_middle

current_dir = os.getcwd()
cam_dir = current_dir + "/cam_control"
sys.path.append(cam_dir)
cam_sim = cam_dir + "/cam_simulation/diplomagm"
sys.path.append(cam_sim)

from cam_control.metric import Metric
from cam_control.strategy.follower import FollowerStrategy
from cam_control.tsp_solver.neighbor import NeighborSolver
from player_detect import PlayerDetector
# from cam_control.strategy.trajectory import TrajectoryStrategy
# from strategy.strategy import CameraMovementStrategy
from cam_simulation.diplomagm.main_without_app import FOVCalculator
from plot import Plotter
from loguru import logger
from time import sleep
from mock_player_sim import MockPlayerSim


class CamSimulation:
    def __init__(self, random_seed=42):
        self.fov_calculator = FOVCalculator()

        CLOSE_ENOUGH_EPS = 2
        SLEEP_EACH_ITER = 0.05

        field_size = self.fov_calculator.get_field_size()
        field_loc = self.fov_calculator.get_field_loc()
        image_sensor = self.fov_calculator.get_image_sensor()
        self.cam_pos = self.fov_calculator.get_cam_pos()
        self.focal_length = self.fov_calculator.get_focal_length()
        logger.debug(f"Cam pos: {self.cam_pos}, focal length: {self.focal_length}")

        self.strategy = FollowerStrategy(field_size, field_loc, self.cam_pos, self.focal_length, image_sensor,
                                         cam_aim_func=calc_fov_middle, eps=CLOSE_ENOUGH_EPS)
        self.plotter = Plotter(field_size=field_size, field_loc=field_loc, sleep_each_iter=SLEEP_EACH_ITER,
                               aim_radius=CLOSE_ENOUGH_EPS)
        self.player_detector = PlayerDetector()
        self.player_sim = MockPlayerSim(field_size, field_loc, random_seed=random_seed)
        self.solver = NeighborSolver(n_observed_agents=self.player_sim.n_agents, eps=CLOSE_ENOUGH_EPS)
        self.metric = Metric(n_players=self.player_sim.n_agents)

        self.log_angles = True
        self.log_players = True
        self.field_size = field_size

    def simulate(self):
        time = 0
        yaw, pitch = self.fov_calculator.get_rotation_coords()
        delta_yaw, delta_pitch = 0, 0
        zoom = 1

        while True:
            yaw += delta_yaw
            pitch += delta_pitch

            camera_properties = {
                "yaw": yaw % 360.0,
                "pitch": pitch % 360.0,
                "zoom": zoom
            }
            fov_points = self.fov_calculator.get_points_of_fov(camera_properties)[0]
            observed_objects_positions = self.player_sim.get_positions(time, randomize=True)
            cur_target = self.solver.determine_next_position(self.strategy.intermediate_target_pos,
                                                             observed_objects_positions)

            delta_yaw, delta_pitch = self.strategy.move(fov_points, yaw, pitch, to=cur_target)
            players_inside_fov = self.player_detector.which_players_inside_fov(
                observed_objects_positions, fov_points
            )

            self.plotter.plot(
                fov_points, observed_objects_positions, self.solver.visited_agents, camera_properties=camera_properties,
                cur_pos=calc_fov_middle(fov_points), target_pos=self.strategy.final_target,
            )

            self._log(camera_properties, players_inside_fov)
            self.metric.count_iteration()
            if self.solver.get_number_of_unvisited_agents() == 0:
                logger.success(f"Simulation finished on angle position {yaw, pitch}")
                break
            time += 1
        return self.metric.get_score()

    def _log(self, camera_properties, players_inside_fov):
        if self.log_angles:
            logger.info(f"{camera_properties}")
        if self.log_players:
            logger.info(f"Players that are inside FOV: {players_inside_fov}")

    @staticmethod
    def _finished(delta_yaw: float, delta_pitch: float):
        return delta_yaw == 0 and delta_pitch == 0


if __name__ == '__main__':
    cam_simulation = CamSimulation()
    cam_simulation.simulate()
