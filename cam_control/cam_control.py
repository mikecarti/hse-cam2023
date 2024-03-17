import matplotlib.pyplot as plt
from cam_simulation.camera import CameraProjectionSimulation

import matplotlib.pyplot as plt


class SimulationController:
    def __init__(self, camera_projection_sim: CameraProjectionSimulation):
        self.camera_sim = camera_projection_sim

    def control_simulation(self, frame_duration: float):
        """
        Control the simulation by updating camera coordinates and plotting the simulation for each frame.

        :param num_frames: Number of frames to simulate.
        :param frame_duration: Duration of each frame in seconds.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        while True:
            # Update camera coordinates for each frame
            theta = int(input('Theta:'))
            phi = int(input('Phi:'))
            psi = int(input('Psi:'))
            self.camera_sim.update_camera_angle(theta, phi, psi)
            # Clear previous plot
            ax.clear()

            # Plot the updated simulation
            self.camera_sim.plot(ax)

            # Pause for the frame duration
            plt.pause(frame_duration)


if __name__ == '__main__':
    camera_sim = CameraProjectionSimulation.init_from_config()
    controller = SimulationController(camera_sim)
    controller.control_simulation(frame_duration=1)
