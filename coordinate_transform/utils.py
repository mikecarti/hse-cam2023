import matplotlib.pyplot as plt


def show_transformation(orig_image, transformed_image):
    fig, axs = plt.subplots(1, 2)

    # Set the image and title for the first subplot on the left
    axs[0].imshow(orig_image)
    axs[0].set_title("Initial image")

    # Set the image and title for the second subplot on the right
    axs[1].imshow(transformed_image)
    axs[1].set_title("Transformed Image")

    # Set the limits and aspect ratio for the second subplot
    axs[1].set_xlim((0, 700))
    axs[1].set_ylim((700, 0))

    # Show the figure
    plt.show()

    # Wait for 15 seconds
    plt.pause(15)
    plt.close()
