from typing import Iterable, Tuple

import numpy as np


class GeometrySolver3D:
    def __init__(self):
        pass

    def find_vector_plane_intersection(self, D: float, p0: np.ndarray, v0: np.ndarray, normal: np.ndarray) \
            -> Tuple[np.ndarray, float]:
        """
                Let p0 be the camera vector and
                v0 be the direction vector of focal plane corner light, that goes through the
                camera_vector (centre of focal lens).

                Then the parametric equation of the line can be defined as:
                P(t) = p0 + t * v0            (P(t) is the point on the line)

                We need to find such t, that P(t) lies on the given plane.
                Substituting it into the plane equation we get:
                a(P0_x + tV0_x) + b(P0_y + tV0_y) + c(P0_z + tV0_z) = d

                Solving for t:
                t = ( D - (normal @ P0) ) / (normal @ V0)

                We are interested in t < 0, as positive values correspond to wrong light direction

                :param D: Distance from the origin to the plane
                :type D: float
                :param p0: Camera vector (center of optical lens)
                :type p0: np.ndarray
                :param v0: Direction vector of focal plane corner light
                :type v0: np.ndarray
                :param normal: Normal vector of the plane
                :type normal: np.ndarray

                :return: Tuple of intersection point and intersection parameter
                :rtype: Tuple[np.ndarray, float]
                """
        t = (D - np.dot(normal, p0)) / np.dot(normal, v0)
        intersection_point = p0 + t * v0
        return intersection_point, t

    def calculate_plane_normal_vec(self, a1: Iterable, a2: Iterable, a3: Iterable) -> np.ndarray:
        """
        Calculate the normal vector of a plane, using points

        return: Normal vector of the plane
        """
        return np.cross(np.array(a2) - np.array(a1), np.array(a3) - np.array(a1))
