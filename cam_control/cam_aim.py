from typing import Tuple

import numpy as np
from shapely import Polygon


def calc_fov_middle(fov_corners: np.array) -> Tuple[float, float]:
    middle_of_fov_point = Polygon(fov_corners).centroid
    return middle_of_fov_point.x, middle_of_fov_point.y


def calc_princ_axis_intersection(fov_corners: np.array) -> Tuple[float, float]:
    furthest_corners = [1, 2]
    corner1, corner2 = np.array(fov_corners)[furthest_corners]
    principal_axis_intersection = (corner1[0] + corner2[0]) / 2, (corner1[1] + corner2[1]) / 2
    return principal_axis_intersection
