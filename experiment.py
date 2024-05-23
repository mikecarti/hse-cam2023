import numpy as np
import pandas as pd

from cam_control.simulation import CamSimulation
from loguru import logger as log

N = 100

if __name__ == "__main__":
    scores = []

    for i in range(N):
        log.info(f"Iteration {i + 1} of {N}")
        sim = CamSimulation(random_seed=i)
        score = sim.simulate()
        scores.append(score)

    avg_score = np.mean(scores)
    log.success(f"Average score of algorithm for N={N} is {avg_score} \nStats: {pd.Series(scores).describe()}")