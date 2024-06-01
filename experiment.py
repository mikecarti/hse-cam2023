import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from cam_control.simulation import CamSimulation
from loguru import logger as log

N = 100

if __name__ == "__main__":
    scores = []
    start_from_frame = 0

    for i in range(N):
        log.info(f"Iteration {i + 1} of {N}")
        sim = CamSimulation(random_seed=i, start_from_frame=start_from_frame)
        score = sim.simulate()
        scores.append(score)
        start_from_frame += score

    scores_seconds = np.array(scores) / 25.0
    sns.histplot(scores_seconds, kde=True)
    plt.xlabel("seconds")
    plt.savefig("scores_histogram.svg", format="svg", bbox_inches="tight")

    np.savetxt("scores_seconds.txt", scores_seconds)
    avg_score = np.mean(scores)
    log.success(f"Average score of algorithm for N={N} is {avg_score} \nStats: {pd.Series(scores).describe()}")
