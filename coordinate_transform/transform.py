from typing import List, Tuple

import numpy as np
import cv2


class CoordinateTransform:
    def __init__(self, stadium_length: int, stadium_width: int, corner_src_points: List[Tuple[int, int]]):
        self.stadium_ratio = (stadium_length / 2) / stadium_width
        self.pic_height = 700  # arbitrary
        self.corner_src_points = corner_src_points
        self.corner_dest_points = self._init_destination_points()

    def _init_destination_points(self):
        """
        Transforms to expected rectangle with sides proportional to stadion ratio.
        :return:
        """
        d1 = (0, 0)
        d2 = (0, self.pic_height)
        d3 = (self.pic_height * self.stadium_ratio, 0)
        d4 = (self.pic_height * self.stadium_ratio, self.pic_height)
        return [d1, d2, d3, d4]

    def get_projective_transform_matrix(self) -> np.ndarray:
        # Projective transformation
        source = np.float32(self.corner_src_points)
        dest = np.float32(self.corner_dest_points)
        M = cv2.getPerspectiveTransform(source, dest)
        return M

    def to_top_perspective(self, image):
        height, width = image.shape[:2]
        M = self.get_projective_transform_matrix()
        return cv2.warpPerspective(image, M, (width, height), borderValue=(255, 255, 255))

