import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
from coordinate_transform.camera import CameraProjectionSimulation

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
            self.camera_sim.update_camera_coordinates(theta,phi,psi)
            # Clear previous plot
            ax.clear()

            # Plot the updated simulation
            self.camera_sim.plot(ax)

            # Pause for the frame duration
            plt.pause(frame_duration)
        plt.show()


if __name__ == '__main__':
    camera_sim = CameraProjectionSimulation()
    controller = SimulationController()