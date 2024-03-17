import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
from loguru import logger
from copy import deepcopy

import yaml
from geometry.solver import GeometrySolver3D

Quadrilateral = Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
Plane = Tuple[np.ndarray, np.ndarray, np.ndarray]


# TODO: зафиксить проблему того, что точки выпадают за пределы поля и не прорисовывают верный 4-угольник
# Чтобы сделать это можно взять проекцию исходящих векторов, которые не касаются плоскости
# А затем найти их пересечение с границей поля


class CameraProjectionSimulation:
    """
    This class calculates a camera projection in a 3D space.
    """

    def __init__(self, camera_coords: np.ndarray, camera_angles: np.ndarray, fov: Tuple[float, float],
                 near_distance: float, rectangle: Quadrilateral, length: float, width: float):
        """
        Initialize the CameraProjection.

        :param camera_coords: Coordinates of the camera.
        :param camera_angles: Camera angles in degrees in plane's coordinate system (Theta, Phi, Psi).
        :param fov: Field of view (FOV) angles in degrees.
        :param near_distance: Distance from the camera to the rectangle.
        :param rectangle: Plane with z = 0 represented by four corner points.
        """
        self.geo_solver = GeometrySolver3D()
        self.ray_exit_border_index = [1, 2, 3]
        self.x_min, self.x_max = 0, length
        self.y_min, self.y_max = 0, width
        self.ray_exit_rect_border_planes = self._determine_exit_border_planes(rectangle)
        self.camera_coords = camera_coords
        self.camera_angles = camera_angles
        self.fov = fov
        self.near_distance = near_distance
        self.rectangle = rectangle
        self.SHOW_PROJECTION_LINES = False
        self.DEBUG_SHOW_ALL_LINES = False

    def _calculate_focal_plane_rectangle(self) -> Tuple[
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

    def _find_intersection_points(self, corner_focal_plane_vectors: List[np.ndarray]) -> List[np.ndarray]:
        """
        Find the intersection points of the focal plane corner vectors with a given plane.

        :param corner_focal_plane_vectors: Vectors from focal plane to optical lens centre.
        :return: List of intersection points.
        """
        intersection_points = []

        normal = self.geo_solver.calculate_plane_normal_vec(*self.rectangle[:3])
        # plane equation: ax + by + cz = (a,b,c)^T @ (x,y,z) = D
        D = np.dot(normal, np.array(self.rectangle[0]))
        camera_vector = np.array(self.camera_coords)

        for vector in corner_focal_plane_vectors:
            focal_plane_corner_vector = np.array(vector)

            intersection_point, t = self.geo_solver.find_vector_plane_intersection(
                D, camera_vector, focal_plane_corner_vector, normal
            )
            if self.DEBUG_SHOW_ALL_LINES:
                intersection_points.append(intersection_point)

            # if t < 0, vector falls on the plane
            if t < 0:
                intersection_points.append(intersection_point)
            # if t > 0, vector does not fall on the plane, but flies into the sky
            else:
                intersection_points = self._find_upwards_oriented_ray_intersection_points(D, camera_vector,
                                                                                          focal_plane_corner_vector,
                                                                                          intersection_points)
        return intersection_points

    def _find_upwards_oriented_ray_intersection_points(self, D: float, camera_vector: np.array,
                                                       focal_plane_corner_vector: np.array,
                                                       intersection_points: List[np.array]) -> List[np.array]:
        """
        Some rays from camera, do not hit the plane, for these rays, this function finds x,y projection of such points,
        it stores it in the intersection_points list
        @param D: float - ax + by + cz - plane equation
        @param camera_vector: np.array
        @param focal_plane_corner_vector: np.array
        @param intersection_points: List[np.array]
        @return: List[np.array]
        """
        intersection_points = deepcopy(intersection_points)

        intersection_point_found = False
        log_buffer = []
        for border_plane in self.ray_exit_rect_border_planes:
            border_normal = self.geo_solver.calculate_plane_normal_vec(*border_plane)
            D = np.dot(border_normal, np.array(border_plane[0]))

            intersection_point, _ = self.geo_solver.find_vector_plane_intersection(
                D, camera_vector, focal_plane_corner_vector, border_normal
            )

            log_buffer.append(intersection_point)

            if self._point_inside_rectangle(intersection_point):
                p = intersection_point
                intersection_point_projection = np.array([p[0], p[1], 0], dtype=np.float64)
                intersection_points.append(intersection_point_projection)
                intersection_point_found = True
                break
        if not intersection_point_found:
            logger.error(f"No intersection point found, but found such points: {log_buffer}\nRemember, these are the "
                         f"restrictions: x_min, x_max, y_min, y_max: {self.x_min, self.x_max, self.y_min, self.y_max}")
        return intersection_points

    def _point_inside_rectangle(self, intersection_point: np.array):
        """
        Check if a given point is inside the observed rectangle.
        @param intersection_point: Point
        @return: bool
        """
        eps = 0.01
        x_valid = self.x_min - eps <= intersection_point[0] <= self.x_max + eps
        y_valid = self.y_min - eps <= intersection_point[1] <= self.y_max + eps
        return x_valid and y_valid

    def _determine_exit_border_planes(self, rectangle: Quadrilateral) -> List[Plane]:
        """
        Determine the exit border planes of our fov rays
        @param rectangle: Quadrilateral
        @return: List of Planes
        """
        exit_border_planes = []

        plane_defining_points_n = 3
        for i in range(plane_defining_points_n + 1):
            if i not in self.ray_exit_border_index:
                continue

            # next_point_index = (i + 1) % len(rectangle)
            point_a = rectangle[i]
            # for no index issues, represents cycle
            point_b = rectangle[(i + 1) % len(rectangle)]

            # add point with z=1
            point_c = point_a + np.array([0, 0, 1])

            border_plane = (point_a, point_b, point_c)
            exit_border_planes.append(border_plane)
        return exit_border_planes

    def plot(self, ax=None) -> None:
        """
        Plot the simulation.
        """
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

        ax.scatter(*self.camera_coords, color='red', label='Оптический центр линзы')

        corners, corner_fov_vectors = self._calculate_focal_plane_rectangle()
        x_vals, y_vals, z_vals = zip(*corners)
        # Focal plane
        ax.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), z_vals + (z_vals[0],), color='blue',
                label="Фокальная плоскость камеры")

        # Observed Rectangle
        # x,y,z
        ax.plot([self.rectangle[i][0] for i in range(4)] + [self.rectangle[0][0]],
                [self.rectangle[i][1] for i in range(4)] + [self.rectangle[0][1]],
                [self.rectangle[i][2] for i in range(4)] + [self.rectangle[0][2]],
                color='darkgreen', alpha=0.5, label="Наблюдаемая плоскость (Ray enter)")

        ax.plot([self.rectangle[i][0] for i in range(4) if i in self.ray_exit_border_index] + [self.rectangle[0][0]],
                [self.rectangle[i][1] for i in range(4) if i in self.ray_exit_border_index] + [self.rectangle[0][1]],
                [self.rectangle[i][2] for i in range(4) if i in self.ray_exit_border_index] + [self.rectangle[0][2]],
                color='lime', alpha=0.5, label="Наблюдаемая плоскость (Ray Exit)")

        # Fov vectors
        for vector in corner_fov_vectors:
            ax.plot([self.camera_coords[0], self.camera_coords[0] + vector[0]],
                    [self.camera_coords[1], self.camera_coords[1] + vector[1]],
                    [self.camera_coords[2], self.camera_coords[2] + vector[2]], color='purple')

        # Points of Intersect
        intersection_points = self._find_intersection_points(corner_fov_vectors)
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
        ax.set_zticks([])

        ax.legend(loc='upper right')

        plt.show()

    def update_camera_coordinates(self, theta, phi, psi):
        self.camera_coords = np.array([theta, phi, psi])

    @staticmethod
    def init_from_config():
        with open("coordinate_transform/cam_config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)

        length = config["length"]
        width = config["width"]
        camera_coords = np.array(config["camera_coords"])
        camera_angles = np.array(config["camera_angles"])
        fov = tuple(config["fov"])
        near_distance = config["near_distance"]
        plane = np.array([(0, 0, 0), (length, 0, 0), (length, width, 0), (0, width, 0)])  # Plane with z = 0

        return CameraProjectionSimulation(camera_coords, camera_angles, fov, near_distance, plane, length, width)


projection = CameraProjectionSimulation.init_from_config()
projection.plot()
