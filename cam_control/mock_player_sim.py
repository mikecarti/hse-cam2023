import numpy as np
import time


class MockPlayerSim:
    def __init__(self, field_size, field_loc, random_seed: int, n_agents=7):
        np.random.seed(random_seed)
        self.field_size = field_size
        self.min_x, self.max_x = field_loc[0], field_loc[0] + field_size[0]
        self.min_y, self.max_y = field_loc[1], field_loc[1] + field_size[1]
        self.player_pos = self._init_players(n_agents)
        self.n_agents = len(self.player_pos)

        np.random.seed(1337)

    def _init_players(self, n_agents):
        static_pos = []
        for i in range(n_agents):
            static_pos.append([np.random.uniform(self.min_x, self.max_x),
                                    np.random.uniform(self.min_y, self.max_y)])
        return np.array(static_pos)

    def get_positions(self, time, randomize=False) -> np.ndarray:
        if randomize:
            deltas = np.random.normal(0, 2, size=self.n_agents * 2)
            for i, pos in enumerate(self.player_pos):
                new_x = pos[0] + deltas[2 * i]
                new_y = pos[1] + deltas[2 * i + 1]

                if not (self.min_x <= new_x <= self.max_x):
                    if new_x < self.min_x:
                        new_x = pos[0] + abs(deltas[2 * i])
                    elif new_x > self.max_x:
                        new_x = pos[0] - abs(deltas[2 * i])

                if not (self.min_y <= new_y <= self.max_y):
                    if new_y < self.min_y:
                        new_y = pos[1] + abs(deltas[2 * i + 1])
                    elif new_y > self.max_y:
                        new_y = pos[1] - abs(deltas[2 * i + 1])

                self.player_pos[i] = [new_x, new_y]
        return self.player_pos

    def _doesnt_suit_constraints(self, new_x, new_y):
        return new_x < self.min_x or new_x > self.max_x or new_y < self.min_y or new_y > self.max_y
