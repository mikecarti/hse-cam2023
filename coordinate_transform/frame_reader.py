import imageio
from loguru import logger
from imageio.core.util import Array
import matplotlib.pyplot as plt


class FrameReader:
    def __init__(self, video_path: str):
        self.video_path = video_path

    def read_frame(self, frame_index: int = 0) -> Array:
        with imageio.get_reader(self.video_path) as video:
            # Read the first frame
            frame = video.get_data(frame_index)
            logger.info(f"Shape of a frame:  {frame.shape}")
        plt.imsave('test.jpg', frame)
        return frame

    def get_meta_data(self) -> dict:
        video_reader = imageio.get_reader(self.video_path)
        return video_reader.get_meta_data()


