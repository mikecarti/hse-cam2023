import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import yaml

INTERVAL = 1000/25

df = pd.read_csv('soccer_sim.csv')

with open("simulation_config.yaml", "r") as config_file:
    sim_config = yaml.safe_load(config_file)

grid_height = sim_config["height"]
grid_width = sim_config["width"]

fig, ax = plt.subplots()
ax.set_xlim([0, grid_width])
ax.set_ylim([0, grid_height])

scatters = [ax.scatter([], [], color=('red' if i < 11 else 'blue')) for i in range(0, 22)]
ball_scatter = ax.scatter([], [], color='black')

def animate(frame_number: int):
        for i, scatter in enumerate(scatters, start=1):
        player = df[df['Frame'] == frame_number][['Player{}_x'.format(i), 'Player{}_y'.format(i)]]
        scatter.set_offsets(player.values)

    ball = df[df['Frame'] == frame_number][['Ball_x', 'Ball_y']]
    ball_scatter.set_offsets(ball.values)

   
ani = animation.FuncAnimation(fig, animate, frames=range(df['Frame'].min(), df['Frame'].max() + 1), interval=INTERVAL)
ani.save('soccer_match_simulation.mp4', writer='ffmpeg')
plt.close(fig)

