import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List


class CameraProjection:
    """
    This class represents a camera projection in a 3D space.
    """

    def __init__(self, camera_coords: np.ndarray, camera_angles: np.ndarray, fov: Tuple[float, float],
                 near_distance: float, plane: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]):
        """
        Initialize the CameraProjection.

        :param camera_coords: Coordinates of the camera.
        :param camera_angles: Camera angles in degrees in plane's coordinate system (Theta, Phi, Psi).
        :param fov: Field of view (FOV) angles in degrees.
        :param near_distance: Distance from the camera to the rectangle.
        :param plane: Plane with z = 0 represented by four corner points.
        """
        self.camera_coords = camera_coords
        self.camera_angles = camera_angles
        self.fov = fov
        self.near_distance = near_distance
        self.plane = plane

    def calculate_fov_rectangle(self) -> Tuple[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], List[np.ndarray]]:
        """
        This function calculates the fov rectangle for a given camera coordinates, angle and plane coordinates.

        Theta - rotation angle along the z axis.
        Phi - rotation angle along the x axis.
        Psi - rotation angle along the y axis.

        :param cam_coords: Coordinates of the camera
        :type cam_coords: Point
        :param camera_angles: Camera angles in plane's coordinate system
        :type camera_angles: np.ndarray
        :rtype: Tuple[Rectangle, List[Point]]
        """
        theta, phi, psi = np.radians(self.camera_angles)

        direction_vector = np.array([
            np.cos(phi) * np.cos(theta),
            np.cos(phi) * np.sin(theta),
            -np.sin(phi)
        ])

        center = self.camera_coords - self.near_distance * direction_vector

        u_vector = np.array([-np.sin(theta), np.cos(theta), 0])
        v_vector = np.cross(u_vector, direction_vector)

        half_fov_horizontal = np.radians(self.fov[0] / 2)
        half_fov_vertical = np.radians(self.fov[1] / 2)

        orientations_from_center = ([-1, -1], [-1, 1], [1, 1], [1, -1])

        corners = [
            center + du * half_fov_horizontal * u_vector + dv * half_fov_vertical * v_vector
            for (dv, du) in orientations_from_center
        ]

        vectors = [corner - self.camera_coords for corner in corners]
        return tuple(corners), vectors

    def find_intersection_points(self, corners: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
                                 vectors: List[np.ndarray]) -> List[np.ndarray]:
        """
        Find the intersection points of the FOV rectangle with a given plane.

        :param corners: Corners of the FOV rectangle.
        :param vectors: Vectors from camera to corners.
        :return: List of intersection points.
        """
        intersection_points = []

        a1, a2, a3 = self.plane[0], self.plane[1], self.plane[2]
        normal = np.cross(np.array(a2) - np.array(a1), np.array(a3) - np.array(a1))
        D = np.dot(normal, np.array(a1))

        for vector in vectors:
            p0 = np.array(self.camera_coords)
            v0 = np.array(vector)

            t = (D - np.dot(normal, p0)) / np.dot(normal, v0)
            intersection_point = p0 + t * v0

            if t < 0:
                intersection_points.append(intersection_point)

        return intersection_points

    def plot(self):
        """
        Plot the FOV rectangle, camera point, plane, and intersection points.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(*self.camera_coords, color='red', label='Camera Center')

        corners, vectors = self.calculate_fov_rectangle()
        x_vals, y_vals, z_vals = zip(*corners)
        ax.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), z_vals + (z_vals[0],), color='blue',
                label="FOV Rectangle")

        ax.plot([self.plane[i][0] for i in range(4)] + [self.plane[0][0]],
                [self.plane[i][1] for i in range(4)] + [self.plane[0][1]],
                [self.plane[i][2] for i in range(4)] + [self.plane[0][2]],
                color='green', alpha=0.5, label="Plane")

        for vector in vectors:
            ax.plot([self.camera_coords[0], self.camera_coords[0] + vector[0]],
                    [self.camera_coords[1], self.camera_coords[1] + vector[1]],
                    [self.camera_coords[2], self.camera_coords[2] + vector[2]], color='purple')

        intersection_points = self.find_intersection_points(corners, vectors)
        intersection_x_vals, intersection_y_vals, intersection_z_vals = zip(*intersection_points)
        ax.plot(intersection_x_vals, intersection_y_vals, intersection_z_vals, 'ko', label='Intersection Points')

        for intersection, corner in zip(intersection_points, corners):
            ax.plot(
                [corner[0], intersection[0]],
                [corner[1], intersection[1]],
                [corner[2], intersection[2]],
                color="black", label="Intersection Points"
            )

        ax.set_aspect('equal')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.legend()

        plt.show()


# Example usage:
length = 50
width = 25

camera_coords = np.array([length / 2, -5, 5])
camera_angles = np.array([90, 20, 0])  # Theta, Phi, Psi in degrees
fov = (180, 90)  # Horizontal and vertical FOV in degrees
near_distance = 2  # Distance from the camera to the rectangle
plane = np.array([(0, 0, 0), (length, 0, 0), (length, width, 0), (0, width, 0)])  # Plane with z = 0

projection = CameraProjection(camera_coords, camera_angles, fov, near_distance, plane)
projection.plot()
