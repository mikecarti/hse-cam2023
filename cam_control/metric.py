from loguru import logger as log


class Metric:
    def __init__(self, n_players: int):
        self.n_players = n_players
        self.iter = 0
        self.algorithm_finished = False

    def count_iteration(self, delta_yaw, delta_pitch):
        # if delta_yaw == delta_pitch == 0, that means that algorithm no longer moving,
        # it is FOR NOW only possible if algorithm traversed all points
        if delta_yaw == delta_pitch == 0 and not self.algorithm_finished:
            self.algorithm_finished = True
            log.success(f"Metric score: {self.iter}\nFor:\n # of players: {self.n_players}\n")
            return self.iter

        self.iter += 1
        return None

    def get_score(self):
        return self.iter
