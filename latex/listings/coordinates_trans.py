Algorithm: TransformCoordinates
Input: file_name (string, optional), player_labels_dataset_path (string, optional)
Output: new_coords (dataframe)

1: Define default values for file_name as 'track_df_new_coords.csv' and player_labels_dataset_path as 'yantar-230722-02_track.csv'

2: Function DownscaleDataFrame(df):
    # Implementation omitted for downscaling dataframe

3: Function ApplyProjectiveTransform(M, XY):
    # XY is an array of shape (3,), XY = [x, y, 1]
    # M is a matrix of shape (3, 3)
    3.1: XY_transformed <- M @ XY
    3.2: scaling_factor <- XY_transformed[2]
    3.3: unscaled_XY_transformed <- XY_transformed / scaling_factor
    3.4: Return unscaled_XY_transformed

4: Function GetPositionTransformed(frame):
    4.1: Initialize XY_init, id_count, and ones
    4.2: Concatenate XY_init with ones
    4.3: Initialize XY_transformed_frame as an empty list
    4.4: For i from 0 to length of id_count - 1:
        4.4.1: XY_trans <- ApplyProjectiveTransform(M, XY_init[i])
        4.4.2: Append XY_trans to XY_transformed_frame
    4.5: Return XY_transformed_frame

5: Load track_df from player_labels_dataset_path using CSV read function
6: Initialize track_df_transformed as an empty list
7: Compute shift as M @ [0, 0, 1]
8: Downscale track_df using DownscaleDataFrame function
9: Filter track_df to obtain rows where "frame" equals 1
10: Apply GetPositionTransformed to the filtered dataframe to get track_df_transformed

11: Modify new_coords:
    11.1: Subtract shift[0] from new_coords['x']
    11.2: Subtract shift[1] from new_coords['y']

12: Save new_coords to a CSV file with the given file_name
13: Return new_coords

End Algorithm
