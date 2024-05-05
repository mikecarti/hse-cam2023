import numpy as np


class PlayerDetector:
    def __init__(self):
        pass

    def which_players_inside_fov(self, players, fov_points):
        fov_points_no_z = np.array(fov_points)[:, [0, 1]]
        are_players_inside_fov = np.array([self.is_point_inside_tetragon(point, fov_points_no_z) for point in players])
        return np.where(are_players_inside_fov != False)

    def is_point_inside_tetragon(self, point, tetragon):
        """
        Check if a point is inside a tetragon.

        Args:
        - point: Tuple (x, y) representing the coordinates of the point.
        - tetragon: List of four tuples [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] representing the vertices of the tetragon.

        Returns:
        - True if the point is inside the tetragon, False otherwise.
        """
        x, y = point
        wn = 0  # Winding number

        # Iterate through each edge of the tetragon
        for i in range(len(tetragon)):
            x1, y1 = tetragon[i]
            x2, y2 = tetragon[(i + 1) % len(tetragon)]  # Wrap around for the last edge

            if y1 <= y:  # Start y <= P.y
                if y2 > y:  # An upward crossing
                    if self.is_left((x1, y1), (x2, y2), point) > 0:
                        wn += 1  # Have a valid up intersect
            else:  # Start y > P.y (no test needed)
                if y2 <= y:  # A downward crossing
                    if self.is_left((x1, y1), (x2, y2), point) < 0:
                        wn -= 1  # Have a valid down intersect

        return wn != 0

    def is_left(self, p0, p1, p2):
        """
        Return positive if the point p2 is left of the line through p0 and p1,
        negative if it's to the right, and 0 if it's on the line.

        Args:
        - p0, p1, p2: Tuples (x, y) representing the coordinates of the points.

        Returns:
        - Positive, negative, or zero value based on the position of p2 relative to the line through p0 and p1.
        """
        return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])