import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List

import yaml
from geometry.solver import GeometrySolver3D


# TODO: зафиксить проблему того, что точки выпадают за пределы поля и не прорисовывают верный 4-угольник
# Чтобы сделать это можно взять проекцию исходящих векторов, которые не касаются плоскости
# А затем найти их пересечение с границей поля


class CameraProjection:
    """
    This class calculates a camera projection in a 3D space.
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
        self.geo_solver = GeometrySolver3D()
        self.camera_coords = camera_coords
        self.camera_angles = camera_angles
        self.fov = fov
        self.near_distance = near_distance
        self.plane = plane
        self.SHOW_PROJECTION_LINES = True
        self.DEBUG_SHOW_ALL_LINES = True

    def calculate_focal_plane_rectangle(self) -> Tuple[
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray], List[np.ndarray]]:
        """
        This function calculates the focal plane for a given camera coordinates, angle and plane coordinates.
        Function returns corners of focal plane (literal point coordinates) and vectors of light
        that go from focal plane corners to center of optical lens.

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

    def find_intersection_points(self, corner_focal_plane_vectors: List[np.ndarray]) -> List[np.ndarray]:
        """
        Find the intersection points of the focal plane corner vectors with a given plane.

        :param corner_focal_plane_vectors: Vectors from focal plane to optical lens centre.
        :return: List of intersection points.
        """
        intersection_points = []

        normal = self.geo_solver.calculate_plane_normal_vec(*self.plane[:3])
        # plane equation: ax + by + cz = D
        D = np.dot(normal, np.array(self.plane[0]))

        for vector in corner_focal_plane_vectors:
            camera_vector = np.array(self.camera_coords)
            focal_plane_corner_vector = np.array(vector)

            intersection_point, t = self.geo_solver.find_vector_plane_intersection(
                D, camera_vector, focal_plane_corner_vector, normal
            )

            # if t > 0, camera corner vector fall behind the camera, which actually means
            # that this vector does not fall on the observed rectangle of the plane
            if t < 0 or self.DEBUG_SHOW_ALL_LINES:
                intersection_points.append(intersection_point)

        return intersection_points

    def plot(self) -> None:
        """
        Plot the FOV rectangle, camera point, plane, and intersection points.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(*self.camera_coords, color='red', label='Оптический центр линзы')

        corners, corner_fov_vectors = self.calculate_focal_plane_rectangle()
        x_vals, y_vals, z_vals = zip(*corners)
        ax.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), z_vals + (z_vals[0],), color='blue',
                label="Фокальная плоскость камеры")

        ax.plot([self.plane[i][0] for i in range(4)] + [self.plane[0][0]],
                [self.plane[i][1] for i in range(4)] + [self.plane[0][1]],
                [self.plane[i][2] for i in range(4)] + [self.plane[0][2]],
                color='green', alpha=0.5, label="Наблюдаемая плоскость")

        for vector in corner_fov_vectors:
            ax.plot([self.camera_coords[0], self.camera_coords[0] + vector[0]],
                    [self.camera_coords[1], self.camera_coords[1] + vector[1]],
                    [self.camera_coords[2], self.camera_coords[2] + vector[2]], color='purple')

        # Points of Intersect
        intersection_points = self.find_intersection_points(corner_fov_vectors)
        intersection_x_vals, intersection_y_vals, intersection_z_vals = zip(*intersection_points)
        ax.plot(intersection_x_vals, intersection_y_vals, intersection_z_vals, 'ko', label='Intersection Points')

        # Intersection Projection vectors
        if self.SHOW_PROJECTION_LINES:
            for intersection, corner in zip(intersection_points, corners):
                ax.plot(
                    [corner[0], intersection[0]],
                    [corner[1], intersection[1]],
                    [corner[2], intersection[2]],
                    color="black", linestyle='--',
                )

        # Projection Quadrilateral
        for i in range(len(intersection_points)):
            current_intersection = intersection_points[i]
            next_intersection = intersection_points[(i + 1) % len(intersection_points)]
            ax.plot([current_intersection[0], next_intersection[0]],
                    [current_intersection[1], next_intersection[1]],
                    [current_intersection[2], next_intersection[2]],
                    color="red", linestyle='dashdot')

        ax.set_aspect('equal')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.legend(loc='upper right')

        plt.show()


# Загрузка параметров из YAML файла
with open("coordinate_transform/cam_config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

length = config["length"]
width = config["width"]
camera_coords = np.array(config["camera_coords"])
camera_angles = np.array(config["camera_angles"])
fov = tuple(config["fov"])
near_distance = config["near_distance"]
plane = np.array([(0, 0, 0), (length, 0, 0), (length, width, 0), (0, width, 0)])  # Plane with z = 0

projection = CameraProjection(camera_coords, camera_angles, fov, near_distance, plane)
projection.plot()
