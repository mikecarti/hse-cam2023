Algorithm: GetProjectiveTransformMatrix
Input: base_size (integer), corner_src_points (list of tuples of integers)
Output: M (2D array)

1: Initialize base_size to 700  # arbitrary size of smallest side of new plane in pixels
2: Initialize whole_stadion_length to 105  # size of actual football stadium in meters
3: Initialize whole_stadion_width to 68
4: Calculate stadion_ratio as (whole_stadion_length / 2) / whole_stadion_width  # length to width ratio

Function GetProjectiveTransformMatrix(base_size: integer, corner_src_points: list of tuples of integers) -> 2D array:
    5: Set d1 to (0, 0)
    6: Set d2 to (0, base_size)
    7: Set d3 to (base_size * stadion_ratio, 0)
    8: Set d4 to (base_size * stadion_ratio, base_size)

    9: Set corner_dest_points to [d1, d2, d3, d4]

    10: Convert corner_src_points to a float32 2D array named source
    11: Convert corner_dest_points to a float32 2D array named dest
    12: Calculate the projective transformation matrix M using cv2.getPerspectiveTransform(source, dest)
    13: Return M
End Function
