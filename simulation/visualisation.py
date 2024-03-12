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

def animate(frame_number: int):
    """
    This function animates the scatter plot of player positions for each frame.

    :param frame_number: The frame number to be animated.
    :type frame_number: int
    """

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
"""
FuncAnimation creates an animation by repeatedly calling a function animate.

:param fig: The figure object that is used to get draw events.
:type fig: Figure
:param animate: The function to call at each frame.
:type animate: callable
:param frames: Source of data to pass function and each frame of the animation
:type frames: int
:param interval: Delay between frames in milliseconds.
:type interval: int
"""

ani.save('soccer_match_simulation.mp4', writer='ffmpeg')
"""
Saves a animation to a file.

:param filename: The output filename.
:type filename: str
:param writer: The writer to use. 
:type writer: str
"""

plt.close(fig)
