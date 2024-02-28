import numpy as np
import matplotlib.pyplot as plt
from sympy import Point3D, Plane as sPlane, Line3D
from typing import Tuple, List

# Define type aliases for better readability
Point = np.ndarray
Rectangle = Tuple[Point, Point, Point, Point]


def calculate_fov_rectangle(cam_coords: Point, camera_angles: np.ndarray, dist: float, fov: Tuple[int, int]) \
        -> Tuple[Rectangle, List[Point]]:
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
    # Convert camera angles from degrees to radians
    theta, phi, psi = np.radians(camera_angles)

    # Calculate direction vector of the camera
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

    orientations_from_center = ([-1, -1], [-1, 1], [1, 1], [1, -1])
    # Calculate the corners of the rectangle
    corners = [
        center + du * half_fov_horizontal * u_vector + dv * half_fov_vertical * v_vector
        for (dv, du) in orientations_from_center
    ]

    # Calculate vectors from camera to corners
    vectors = [corner - cam_coords for corner in corners]
    return corners, vectors


def find_intersection_points(camera_coords: Point, vectors: List[Point], plane: Point) -> List[Point]:
    intersection_points = []

    # Define the plane equation
    a1, a2, a3 = plane[0], plane[1], plane[2]
    normal = np.cross(np.array(a2) - np.array(a1), np.array(a3) - np.array(a1))
    D = np.dot(normal, np.array(a1))

    for vector in list(vectors):
        # Define the line passing through camera_coords and parallel to the vector
        p0 = np.array(camera_coords)
        v0 = np.array(vector)

        # Solve the system of equations to find the intersection point
        t = (D - np.dot(normal, p0)) / np.dot(normal, v0)
        intersection_point = p0 + t * v0

        intersection_points.append(intersection_point)

    return intersection_points


def plot_fov_rectangle(camera_coords: Point, camera_angles: np.ndarray, fov: Tuple[float, float],
                       near_distance: float, plane: Rectangle) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot camera point
    ax.scatter(*camera_coords, color='red', label='Оптический центр линзы')

    # Calculate and plot FOV rectangle
    fov_rectangle_corners, vectors = calculate_fov_rectangle(camera_coords, camera_angles, near_distance, fov)
    x_vals, y_vals, z_vals = zip(*fov_rectangle_corners)
    ax.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), z_vals + (z_vals[0],), color='blue',
            label="Фокальная плоскость камеры")

    # Plot z=0 plane
    ax.plot([plane[i][0] for i in range(4)] + [plane[0][0]],
            [plane[i][1] for i in range(4)] + [plane[0][1]],
            [plane[i][2] for i in range(4)] + [plane[0][2]],
            color='green', alpha=0.5, label="Наблюдаемая плоскость")

    # Plot purple lines
    for vector in vectors:
        ax.plot([camera_coords[0], camera_coords[0] + vector[0]],
                [camera_coords[1], camera_coords[1] + vector[1]],
                [camera_coords[2], camera_coords[2] + vector[2]], color='purple')

    intersection_points = find_intersection_points(camera_coords, vectors, plane)
    # Plot intersection points
    # intersection_x_vals, intersection_y_vals, intersection_z_vals = zip(*intersection_points)
    # ax.plot(intersection_x_vals, intersection_y_vals, intersection_z_vals, color='black',
    #            label='Intersection Points')
    for intersection, corner in zip(intersection_points, fov_rectangle_corners):
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


# Call the plotting function with intersection points

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
