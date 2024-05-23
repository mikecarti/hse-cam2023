from loguru import logger as log


class Metric:
    def __init__(self, n_players: int):
        self.n_players = n_players
        self.iter = 0
        self.algorithm_finished = False

    def count_iteration(self):
        # if delta_yaw == delta_pitch == 0, that means that algorithm no longer moving,
        # it is FOR NOW only possible if algorithm traversed all points
        self.iter += 1

    def get_score(self):
        log.success(f"Metric score: {self.iter}\nFor:\n # of players: {self.n_players}\n")
        return self.iter
