from typing import List, Tuple

import numpy as np
import cv2


class CoordinateTransform:
    """
    A class for transforming coordinates between different perspectives.

    Args:
        stadium_length (int): The length of the stadium in meters.
        stadium_width (int): The width of the stadium in meters.
        corner_src_points (List[Tuple[int, int]]): A list of tuples, where each tuple represents the coordinates of one of the four corners of the original plane.

    Attributes:
        stadium_ratio (float): The ratio of the stadium's length to its width.
        pic_height (int): The height of the destination image, which is assumed to be 700 pixels.
        corner_src_points (List[Tuple[int, int]]): A list of tuples, where each tuple represents the coordinates of one of the four corners of the original plane.
        corner_dest_points (List[Tuple[int, int]]): A list of tuples, where each tuple represents the coordinates of one of the four corners of the destination plane, which is a rectangle with sides proportional to the stadium ratio.

    """

    def __init__(self, stadium_length: int, stadium_width: int, corner_src_points: List[Tuple[int, int]]):
        self.stadium_ratio = (stadium_length / 2) / stadium_width
        self.pic_height = 700  # arbitrary
        self.corner_src_points = corner_src_points
        self.corner_dest_points = self._init_destination_points()

    def _init_destination_points(self):
        """
        Initializes the destination points, which are the corners of a rectangle with sides proportional to the stadium ratio.

        Returns:
            List[Tuple[int, int]]: A list of tuples, where each tuple represents the coordinates of one of the four corners of the destination image.

        """
        d1 = (0, 0)
        d2 = (0, self.pic_height)
        d3 = (self.pic_height * self.stadium_ratio, 0)
        d4 = (self.pic_height * self.stadium_ratio, self.pic_height)
        return [d1, d2, d3, d4]

    def get_projective_transform_matrix(self) -> np.ndarray:
        """
        Returns the projective transformation matrix that can be used to transform points from the original image to the destination image.

        Returns:
            np.ndarray: The projective transformation matrix.

        """
        # Projective transformation
        source = np.float32(self.corner_src_points)
        dest = np.float32(self.corner_dest_points)
        M = cv2.getPerspectiveTransform(source, dest)
        return M

    def to_top_perspective(self, image: np.ndarray) -> np.ndarray:
        """
        Transforms an image from the original perspective to the top perspective.

        Args:
            image (np.ndarray): The image to be transformed.

        Returns:
            np.ndarray: The transformed image.
        """
        height, width = image.shape[:2]
        M = self.get_projective_transform_matrix()
        return cv2.warpPerspective(image, M, (width, height), borderValue=(255, 255, 255))

