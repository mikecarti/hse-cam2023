import numpy as np
import time


class MockPlayerSim:
    def __init__(self, field_size, field_loc):
        self.field_size = field_size
        self.min_x, self.max_x = field_loc[0], field_loc[0] + field_size[0]
        self.min_y, self.max_y = field_loc[1], field_loc[1] + field_size[1]
        self.static_pos = np.array([[50, 50], [65, 55], [80, 70], [50, 80], [80, 50], [90, 50], [45, 45]])
        self.n_agents = len(self.static_pos)

        np.random.seed(1337)

    def get_positions(self, time, randomize=False) -> np.ndarray:
        if randomize:
            deltas = np.random.uniform(-1, 2, size=self.n_agents * 2)
            for i, pos in enumerate(self.static_pos):
                self.static_pos[i][0] += deltas[2 * i]
                self.static_pos[i][1] += deltas[2 * i + 1]
        return self.static_pos
