import matplotlib
import numpy as np

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from loguru import logger


def show_transformation(orig_image: np.ndarray, transformed_image: np.ndarray) -> None:
    """
    Plots the transformation
    Args:
        orig_image (np.ndarray): original image
        transformed_image (np.ndarray): transformed coordinates image

    Returns:
        None
    """
    wait_seconds = 3

    fig, axs = plt.subplots(1, 2)
    plt.subplots_adjust(wspace=0.4)

    # Set the image and title for the first subplot on the left
    axs[0].imshow(orig_image)
    axs[0].set_title("Initial image")

    # Set the image and title for the second subplot on the right
    axs[1].imshow(transformed_image)
    axs[1].set_title("Transformed Image")

    # Set the limits and aspect ratio for the second subplot
    axs[1].set_xlim((0, 700))
    axs[1].set_ylim((700, 0))

    plt.savefig("transformation.png")
    logger.info("Close this plot window to continue...")
    # Show the figure
    plt.show()

    # Wait for 15 seconds
    plt.pause(wait_seconds)
    plt.close()
