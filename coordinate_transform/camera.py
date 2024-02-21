from typing import List

import numpy as np
import matplotlib.pyplot as plt


def calculate_quadrilateral(width: int, length: int,
                            camera_coords: list, camera_angles: list, fov: list) -> List[List[float]]:
    """
    This function calculates the quadrilateral for a given camera coordinates, angle
    and plane coordinates.

    Theta - rotation angle along the z axis.
    Phi - rotation angle along the x axis.
    Psi - rotation angle along the y axis.

    :param width: Width of the plane
    :type width: int (y axis)
    :param length: Length of the plane
    :type length: int (x axis)
    :param camera_coords: Camera coordinates in plane's coordinate system
    :type camera_coords: list
    :param camera_angles: Camera angles in plane's coordinate system
    :type camera_angles: list
    :param fov: Field of view in plane's coordinate system
    :type fov: list
    :return: Quadrilateral in plane's coordinate system
    :rtype: List[List[float]]
    """
    # Convert camera angles from degrees to radians
    theta, phi, psi = np.radians(camera_angles)

    # Extract camera coordinates
    x_cam, y_cam, z_cam = camera_coords

    # Calculate half FOV angles in radians
    half_fov_horizontal = np.radians(fov[0] / 2)
    half_fov_vertical = np.radians(fov[1] / 2)

    # Define vectors representing the edges of the quadrilateral
    vec1 = [length * np.cos(theta - half_fov_horizontal), length * np.sin(theta - half_fov_horizontal), 0]
    vec2 = [length * np.cos(theta + half_fov_horizontal), length * np.sin(theta + half_fov_horizontal), 0]
    vec3 = [width * np.cos(phi - half_fov_vertical) * np.cos(psi),
            width * np.cos(phi - half_fov_vertical) * np.sin(psi), width * np.sin(phi - half_fov_vertical)]
    vec4 = [width * np.cos(phi + half_fov_vertical) * np.cos(psi),
            width * np.cos(phi + half_fov_vertical) * np.sin(psi), width * np.sin(phi + half_fov_vertical)]

    # Calculate corners by intersecting vectors with the plane z = 0
    corner1 = np.array(camera_coords) + np.array([0, 0, z_cam]) + vec1
    corner2 = np.array(camera_coords) + np.array([0, 0, z_cam]) + vec2
    corner3 = np.array(camera_coords) + np.array([0, 0, z_cam]) + vec3
    corner4 = np.array(camera_coords) + np.array([0, 0, z_cam]) + vec4

    return [corner1, corner2, corner3, corner4]


def plot_quadrilateral(width, length, camera_coords, camera_angles, fov):
    # Calculate the quadrilateral
    quadrilateral = calculate_quadrilateral(width, length, camera_coords, camera_angles, fov)

    # Extract x, y, z coordinates of quadrilateral corners
    x = [corner[0] for corner in quadrilateral]
    y = [corner[1] for corner in quadrilateral]
    z = [corner[2] for corner in quadrilateral]

    # Plot the plane
    plt.fill([0, length, length, 0], [0, 0, width, width], color='black', alpha=0.3)

    # Plot the quadrilateral
    plt.fill(x, y, color='red', alpha=0.5)

    # Set plot limits and labels
    plt.xlim(0, length)
    plt.ylim(0, width)
    plt.xlabel('Length')
    plt.ylabel('Width')
    plt.title('Camera View on Plane')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)

    # Show plot
    plt.show()


# Example usage:
width = 2000
length = 3000
camera_coords = [length / 2, width/ 2, 50]
camera_angles = [90, 0, 0]  # Theta, Phi, Psi in degrees
fov = [60, 45]  # Horizontal and vertical FOV in degrees

plot_quadrilateral(width, length, camera_coords, camera_angles, fov)
