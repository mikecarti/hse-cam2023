import os

import pandas as pd
from loguru import logger

from coordinate_transform.transform import CoordinateTransform
from coordinate_transform.frame_reader import FrameReader
from coordinate_transform.utils import show_transformation
from tsp.static_tsp import StaticTSPSolver

stadium_length = 105
stadium_width = 68

# Corners pixel coordinates for the half of the stadium
p1 = (60, 152)
p2 = (47, 724)
p3 = (1620, 125)
p4 = (2139, 668)
corner_src_points = [p1, p2, p3, p4]


def run_demo(coord_transformer):
    video_path = os.path.join('coordinate_transform', 'data', 'yantar-230722-02-det.mp4')
    reader = FrameReader(video_path)
    frame = reader.read_frame(0)
    logger.info(reader.get_meta_data())
    image_view_from_above = coord_transformer.image_to_top_perspective(image=frame)
    show_transformation(frame, image_view_from_above)


if __name__ == '__main__':
    transformer = CoordinateTransform(stadium_length, stadium_width, corner_src_points)

    run_demo(coord_transformer=transformer)

    track_df_path = os.path.join("coordinate_transform", "data", "yantar-230722-02_track.csv")
    transformed_positions = transformer.transform_coordinates(pd.read_csv(track_df_path))
    logger.info("All positions transformed to top-view perspective, ready to run TSP optimization")

    solver = StaticTSPSolver()


