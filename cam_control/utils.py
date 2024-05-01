def calc_corners(height, width):
    top_right = (width, height)
    top_left = (0, height)
    bottom_left = (0, 0)
    bottom_right = (width, 0)
    return bottom_left, bottom_right, top_left, top_right