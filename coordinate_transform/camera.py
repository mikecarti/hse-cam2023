import numpy as np
import matplotlib.pyplot as plt
from sympy import Point3D, Plane as sPlane, Line3D
from typing import Tuple

# Define type aliases for better readability
Point = np.ndarray
Rectangle = Tuple[Point, Point, Point, Point]


def calculate_fov_rectangle(cam_coords: Point, camera_angles: np.ndarray, dist: float) -> Rectangle:
    """
    This function calculates the fov rectangle for a given camera coordinates, angle and plane coordinates.

    Theta - rotation angle along the z axis.
    Phi - rotation angle along the x axis.
    Psi - rotation angle along the y axis.

    :param cam_coords: Coordinates of the camera
    :type cam_coords: Point
    :param camera_angles: Camera angles in plane's coordinate system
    :type camera_angles: np.ndarray
    :rtype: Rectangle
    """
    # Convert camera angles from degrees to radians
    theta, phi, psi = np.radians(camera_angles)

    # Calculate the direction vector of the camera
    direction_vector = np.array([
        np.cos(phi) * np.cos(theta),
        np.cos(phi) * np.sin(theta),
        -np.sin(phi)
    ])

    center = cam_coords - dist * direction_vector

    # Calculate vectors orthogonal to the direction vector
    u_vector = np.array([-np.sin(theta), np.cos(theta), 0])
    v_vector = np.cross(u_vector, direction_vector)

    # Calculate half FOV angles in radians
    half_fov_horizontal = np.radians(fov[0] / 2)
    half_fov_vertical = np.radians(fov[1] / 2)

    # Calculate the vectors representing the corners of the rectangle
    top_left_corner = center - half_fov_horizontal * u_vector + half_fov_vertical * v_vector
    top_right_corner = center + half_fov_horizontal * u_vector + half_fov_vertical * v_vector
    bottom_left_corner = center - half_fov_horizontal * u_vector - half_fov_vertical * v_vector
    bottom_right_corner = center + half_fov_horizontal * u_vector - half_fov_vertical * v_vector

    return top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner


def plot_fov_rectangle(camera_coords: Point, camera_angles: np.ndarray, fov: Tuple[float, float],
                       near_distance: float, plane: Point) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot camera point
    ax.scatter(camera_coords[0], camera_coords[1], camera_coords[2], color='red', label='Оптический центр линзы')

    # Calculate and plot FOV rectangle
    fov_rectangle_corners = calculate_fov_rectangle(camera_coords, camera_angles, near_distance)
    x_vals, y_vals, z_vals = zip(*fov_rectangle_corners)
    ax.plot([x_vals[0], x_vals[1], x_vals[2], x_vals[3], x_vals[0]],
            [y_vals[0], y_vals[1], y_vals[2], y_vals[3], y_vals[0]],
            [z_vals[0], z_vals[1], z_vals[2], z_vals[3], z_vals[0]], color='blue',
            label="Фокальная плоскость камеры")

    # Plot z=0 plane
    ax.plot([plane[0][0], plane[1][0], plane[2][0], plane[3][0], plane[0][0]],
            [plane[0][1], plane[1][1], plane[2][1], plane[3][1], plane[0][1]],
            [plane[0][2], plane[1][2], plane[2][2], plane[3][2], plane[0][2]],
            color='green', alpha=0.5, label="Наблюдаемая плоскость")

    ax.set_aspect('equal')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.legend()

    plt.show()


# def find_intersection(plane_points: Point) -> np.ndarray:
#     # plane Points
#     a1 = Point3D(*plane_points[0])
#     a2 = Point3D(*plane_points[1])
#     a3 = Point3D(*plane_points[2])
#     # line Points
#     p0 = Point3D(0, 3, 1)  # point in line
#     v0 = [0, 1, 1]  # line direction as vector
#
#     # create plane and line
#     plane = sPlane(a1, a2, a3)
#
#     line = Line3D(p0, direction_ratio=v0)
#
#     print(f"plane equation: {plane.equation()}")
#     print(f"line equation: {line.equation()}")
#
#     # find intersection:
#     intr = plane.intersection(line)
#
#     intersection = np.array(intr[0], dtype=float)
#     print(f"intersection: {intersection}")
#     return intersection


# Example usage:
length = 50
width = 25

camera_coords = np.array([length / 2, -5, 5])
camera_angles = np.array([90, 20, 0])  # Theta, Phi, Psi in degrees
# fov = (60, 45)  # Horizontal and vertical FOV in degrees
fov = (180, 90)  # Horizontal and vertical FOV in degrees
near_distance = 2  # Distance from the camera to the rectangle
plane = np.array([(0, 0, 0), (length, 0, 0), (length, width, 0), (0, width, 0)])  # Plane with z = 0

plot_fov_rectangle(camera_coords, camera_angles, fov, near_distance, plane)
