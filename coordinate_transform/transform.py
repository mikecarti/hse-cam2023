from typing import List, Tuple, Dict

from loguru import logger
import numpy as np
import cv2
import pandas as pd


class CoordinateTransform:
    """
    A class for transforming coordinates between different perspectives.

    Args:
        stadium_length (int): The length of the stadium in meters.
        stadium_width (int): The width of the stadium in meters.
        corner_src_points (List[Tuple[int, int]]): A list of tuples, where each tuple represents the coordinates of one
                                                        of the four corners of the original plane.

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

        self.default_tracking_players_path = "coordinate_transform/data/yantar-230722-02_track.csv"
        self.MAX_FRAMES = np.inf  # put here lower bound for testing purposes
        self.center_orig_perspective = [1846, 343]  # 1846, 343 - are approximately the center of the stadium left side

    def transform_coordinates(self, track_boxes_df: pd.DataFrame = None,
                              file_save_name: str = 'track_df_new_coords.csv') -> pd.DataFrame:
        """
        Transforms the coordinates of the players in the given DataFrame from the original perspective to the top perspective.

        Args:
            track_boxes_df (pd.DataFrame, optional): The DataFrame containing the tracking data. If None, the default tracking data will be used.
            file_save_name (str, optional): The name of the file to which the transformed coordinates will be saved. Defaults to 'track_df_new_coords.csv'.

        Returns:
            pd.DataFrame: The transformed DataFrame.
        """

        # transform pos person -> pos trans
        # 25 FPS
        M = self._get_projective_transform_matrix()

        if track_boxes_df is None:
            track_boxes_df = pd.read_csv(self.default_tracking_players_path)

        shift = M @ np.array([0, 0, 1])
        track_boxes_df = self._downscale_df(track_boxes_df)
        tracking_coords_transformed = []

        for i in range(1, track_boxes_df["frame"].max() + 1):
            if i > self.MAX_FRAMES:
                logger.info(f"Max frames reached. Stopping: {self.MAX_FRAMES}")
                break
            if i % 10000 == 0:
                logger.info(f"Transforming frame {i}...")
            df = track_boxes_df[track_boxes_df["frame"] == i]
            tracking_coords_transformed += self._get_position_transformed(df, transformation_matrix=M)

        transformed_coords = pd.DataFrame(tracking_coords_transformed, columns=['id', 'x', 'y', 'coef'])
        transformed_coords['frame'] = track_boxes_df['frame']
        transformed_coords['x'] -= shift[0]
        transformed_coords['y'] -= shift[1]
        transformed_coords = transformed_coords[['frame', 'id', 'x', 'y', 'coef']]
        transformed_coords.to_csv(file_save_name)
        return transformed_coords

    def get_top_view_center(self) -> np.ndarray:
        M = self._get_projective_transform_matrix()
        center = M @ np.array(self.center_orig_perspective + [1])
        return center

    def image_to_top_perspective(self, image: np.ndarray) -> np.ndarray:
        """
        Transforms an image from the original perspective to the top perspective.

        Args:
            image (np.ndarray): The image to be transformed.

        Returns:
            np.ndarray: The transformed image.
        """
        height, width = image.shape[:2]
        M = self._get_projective_transform_matrix()
        return cv2.warpPerspective(image, M, (width, height), borderValue=(255, 255, 255))

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

    def _get_projective_transform_matrix(self) -> np.ndarray:
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

    def _downscale_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Args:
            df (pd.DataFrame): containing object's dynamics (movement)

        Returns:
            df (pd.DataFrame): having downscaled coordinates (2x downscale)

        """
        df = df.copy()

        df["x1"] = df["x1"] // 2
        df["x2"] = df["x2"] // 2
        df["y1"] = df["y1"] // 2
        df["y2"] = df["y2"] // 2
        return df

    def _apply_projective_transform(self, M: np.ndarray, XY: np.ndarray) -> np.ndarray:
        """
        Apply a projective transformation M on coordinate point.
        Args:
            M (np.ndarray): Projective Matrix
            XY (np.ndarray): Coordinate point
        Returns:
            unscaled_XY_transformed (np.ndarray): True transformed point
        """
        # XY.shape = (3,); XY = [x,y,1]
        # M.shape = (3,3)
        XY_transformed = M @ XY
        scaling_factor = XY_transformed[2]
        unscaled_XY_transformed = XY_transformed / scaling_factor
        return unscaled_XY_transformed

    def _get_position_transformed(self, frame: pd.DataFrame, transformation_matrix: np.ndarray) -> List[Dict]:
        """
        Transforms dataframe with positions to positions from top view
        Args:
            frame (pd.DataFrame): positions
            transformation_matrix (np.ndarray): Projective Transform Matrix

        Returns:
            XY_transformed ( List(Dict) ): Transformed positions
        """
        x1, y1, x2, y2 = frame['x1'], frame['y1'], frame['x2'], frame['y2']
        x = (x2 + x1) // 2
        y = y2
        id_count = np.array(frame['id'])
        XY_init = np.array([x, y]).T
        ones = np.ones((len(id_count), 1))
        XY_init = np.hstack((XY_init, ones))
        XY_transformed = []

        for i in range(len(id_count)):
            XY_trans = self._apply_projective_transform(transformation_matrix, XY_init[i])
            XY_transformed.append(XY_trans)

        for i in range(len(id_count)):
            XY_transformed[i] = np.append(id_count[i], XY_transformed[i])

        return XY_transformed
