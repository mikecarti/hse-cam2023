def calc_corners(height, width, loc=(0, 0)):
    x, y = loc

    top_right = (x+width, y+height)
    top_left = (x+0, y+height)
    bottom_left = (x+0, y+0)
    bottom_right = (x+width, y+0)
    return bottom_left, bottom_right, top_left, top_right