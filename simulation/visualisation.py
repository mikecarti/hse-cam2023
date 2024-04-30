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

scatters = [ax.scatter([], [], color=('red' if i <= 11 else 'blue')) for i in range(1, 23)]
ball_scatter = ax.scatter([], [], color='black')

def animate(frame_number: int):
    """
    This function animates the scatter plot of player positions for each frame.

    :param frame_number: The frame number to be animated.
    :type frame_number: int
    """

    for i, scatter in enumerate(scatters, start=1):
        player = df[df['Frame'] == frame_number][['Player{}_x'.format(i), 'Player{}_y'.format(i)]]
        scatter.set_offsets(player.values)

    ball = df[df['Frame'] == frame_number][['Ball_x', 'Ball_y']]
    ball_scatter.set_offsets(ball.values)

   
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
