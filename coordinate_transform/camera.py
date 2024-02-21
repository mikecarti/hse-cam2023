import numpy as np
import matplotlib.pyplot as plt


def calculate_quadrilateral(width, length, camera_coords, camera_angles):
    # Convert camera angles from degrees to radians
    theta, phi, psi = np.radians(camera_angles)

    # Extract camera coordinates
    x_cam, y_cam, z_cam = camera_coords

    # Calculate the corners of the quadrilateral
    corner1 = [x_cam + length * np.cos(theta), y_cam + length * np.sin(theta), z_cam]
    corner2 = [x_cam + width * np.cos(phi) * np.cos(psi),
               y_cam + width * np.sin(phi) * np.cos(psi),
               z_cam + width * np.sin(psi)]
    corner3 = [corner1[0] + corner2[0] - x_cam,
               corner1[1] + corner2[1] - y_cam,
               corner1[2] + corner2[2] - z_cam]
    corner4 = [x_cam + width * np.cos(phi + np.pi) * np.cos(psi),
               y_cam + width * np.sin(phi + np.pi) * np.cos(psi),
               z_cam + width * np.sin(psi)]

    return [corner1, corner2, corner3, corner4]


def plot_quadrilateral(width, length, camera_coords, camera_angles):
    # Calculate the quadrilateral
    quadrilateral = calculate_quadrilateral(width, length, camera_coords, camera_angles)

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
width = 100
length = 150
camera_coords = [50, -10, 200]
camera_angles = [15, 15, 15]  # Theta, Phi, Psi in degrees

plot_quadrilateral(width, length, camera_coords, camera_angles)
