import os

from loguru import logger

from coordinate_transform.transform import CoordinateTransform
from frame_reader import FrameReader
from utils import show_transformation

stadium_length = 105
stadium_width = 68

# Corners pixel coordinates for the half of the stadium
p1 = (60, 152)
p2 = (47, 724)
p3 = (1620, 125)
p4 = (2139, 668)
corner_src_points = [p1, p2, p3, p4]

if __name__ == '__main__':
    video_path = os.path.join('data', 'yantar-230722-02-det.mp4')

    reader = FrameReader(video_path)
    frame = reader.read_frame(0)
    logger.info(reader.get_meta_data())

    transformer = CoordinateTransform(stadium_length, stadium_width, corner_src_points)
    image_view_from_above = transformer.to_top_perspective(image=frame)
    show_transformation(frame, image_view_from_above)
