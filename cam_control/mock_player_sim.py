import numpy as np


class MockPlayerSim:
    def __init__(self, field_size, field_loc):
        self.field_size = field_size
        self.min_x, self.max_x = field_loc[0], field_loc[0] + field_size[0]
        self.min_y, self.max_y = field_loc[1], field_loc[1] + field_size[1]

    def get_positions(self, time) -> np.ndarray:
        n = 7
        positions = np.zeros((n, 2))
        # i will now initialize it with random positions
        for i in range(n):
            positions[i][0] = np.random.randint(self.min_x, self.max_x)
            positions[i][1] = np.random.randint(self.min_y, self.max_y)
        # np.ndarray([[1,1], [2,3], [5,6],... ,...])
        return positions