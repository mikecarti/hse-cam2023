import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from sympy import Point3D, Plane as sPlane, Line3D

# Define type aliases for better readability
Point = Tuple[float, float, float]
Plane = List[Point]
Rectangle = Tuple[Point, Point, Point, Point]


def calculate_fov_rectangle(cam_coords: Point, camera_angles: Tuple[float, float, float], dist: int) -> Rectangle:
    """
    This function calculates the fov rectangle for a given camera coordinates, angle and plane coordinates.

    Theta - rotation angle along the z axis.
    Phi - rotation angle along the x axis.
    Psi - rotation angle along the y axis.

    :param cam_coords: Coordinates of the camera
    :type cam_coords: Point
    :param camera_angles: Camera angles in plane's coordinate system
    :type camera_angles: Tuple[float, float, float]
    :rtype: Rectangle
    """
    # Convert camera angles from degrees to radians
    theta, phi, psi = np.radians(camera_angles)

    # x_cam, y_cam, z_cam = camera_coords

    # Calculate the direction vector of the camera
    direction_vector = np.array([
        np.cos(phi) * np.cos(theta),
        np.cos(phi) * np.sin(theta),
        -np.sin(phi)
    ])

    # Calculate vectors orthogonal to the direction vector
    u_vector = np.array([-np.sin(theta), np.cos(theta), 0])
    v_vector = np.cross(direction_vector, u_vector)

    # Calculate half FOV angles in radians
    half_fov_horizontal = np.radians(fov[0] / 2)
    half_fov_vertical = np.radians(fov[1] / 2)

    # Calculate the vectors representing the corners of the rectangle
    center = cam_coords + dist * direction_vector
    top_left_corner = center - half_fov_horizontal * u_vector + half_fov_vertical * v_vector
    top_right_corner = center + half_fov_horizontal * u_vector + half_fov_vertical * v_vector
    bottom_left_corner = center - half_fov_horizontal * u_vector - half_fov_vertical * v_vector
    bottom_right_corner = center + half_fov_horizontal * u_vector - half_fov_vertical * v_vector

    return [top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner]

# rewrite plagiarism
def plot_fov_rectangle(camera_coords: Point, camera_angles: Tuple[float, float, float], fov: Tuple[float, float],
                       near_distance: float, plane: Plane) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot camera point
    ax.scatter(camera_coords[0], camera_coords[1], camera_coords[2], color='red', label='Camera')

    # Calculate and plot FOV rectangle
    fov_rectangle_corners = calculate_fov_rectangle(camera_coords, camera_angles, near_distance)
    x_vals = [corner[0] for corner in fov_rectangle_corners]
    y_vals = [corner[1] for corner in fov_rectangle_corners]
    z_vals = [corner[2] for corner in fov_rectangle_corners]
    ax.plot([x_vals[0], x_vals[1], x_vals[2], x_vals[3], x_vals[0]],
            [y_vals[0], y_vals[1], y_vals[2], y_vals[3], y_vals[0]],
            [z_vals[0], z_vals[1], z_vals[2], z_vals[3], z_vals[0]], color='blue')

    # Plot z=0 plane
    plane_corners = np.array(plane)
    ax.plot([plane_corners[0][0], plane_corners[1][0], plane_corners[2][0], plane_corners[3][0], plane_corners[0][0]],
            [plane_corners[0][1], plane_corners[1][1], plane_corners[2][1], plane_corners[3][1], plane_corners[0][1]],
            [plane_corners[0][2], plane_corners[1][2], plane_corners[2][2], plane_corners[3][2], plane_corners[0][2]],
            color='green', alpha=0.5)

    # Set tick frequency
    # ax.set_xticks(np.arange(0, 11, 2))
    # ax.set_yticks(np.arange(0, 11, 2))
    # ax.set_zticks(np.arange(0, 11, 2))
    ax.set_aspect('equal')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.legend()

    plt.show()

# rewrite plagiarism
def find_intersection(plane_points: List[Point], ) -> np.ndarray:
    # plane Points
    a1 = Point3D(*plane_points[0])
    a2 = Point3D(*plane_points[1])
    a3 = Point3D(*plane_points[2])
    # line Points
    p0 = Point3D(0, 3, 1)  # point in line
    v0 = [0, 1, 1]  # line direction as vector

    # create plane and line
    plane = sPlane(a1, a2, a3)

    line = Line3D(p0, direction_ratio=v0)

    print(f"plane equation: {plane.equation()}")
    print(f"line equation: {line.equation()}")

    # find intersection:

    intr = plane.intersection(line)

    intersection = np.array(intr[0], dtype=float)
    print(f"intersection: {intersection}")
    return intersection


def calculate_projection_corners(sensor_coords: Plane, camera_coords: Point, camera_angles: Tuple[float, float, float],
                                 plane_coords: Plane) -> List[Point]:
    pass


# Example usage:
camera_coords = (2.5, 2.5, 5)
camera_angles = (0, 90, 0)  # Theta, Phi, Psi in degrees
fov = (60, 45)  # Horizontal and vertical FOV in degrees
near_distance = 1  # Distance from the camera to the rectangle
height = 5
width = 5
plane = [(0, 0, 0), (height, 0, 0), (height, width, 0), (0, width, 0)]  # Plane with z = 0

plot_fov_rectangle(camera_coords, camera_angles, fov, near_distance, plane)
