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
    ax.clear()
    frame_data = df[df['Frame'] == frame_number]

    team1_data = frame_data[frame_data['Team'] == 'Team A']
    ax.scatter(team1_data['X'], team1_data['Y'], color='blue', label='Team 1')

    team2_data = frame_data[frame_data['Team'] == 'Team B']
    ax.scatter(team2_data['X'], team2_data['Y'], color='red', label='Team 2')

    ax.legend()

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Player positions in frame {frame_number}')

    ax.set_xlim([0, grid_width])
    ax.set_ylim([0, grid_height])   

   
ani = animation.FuncAnimation(fig, animate, frames=range(df['Frame'].min(), df['Frame'].max() + 1), interval=INTERVAL)
ani.save('soccer_match_simulation.mp4', writer='ffmpeg')
plt.close(fig)

