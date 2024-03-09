import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt

df = pd.read_csv('soccer_sim.csv')

fig, ax = plt.subplots()
def animate(frame_number):
    ax.clear()
    frame_data = df[df['Frame'] == frame_number]

    team1_data = frame_data[frame_data['Team'] == 'Team A']
    ax.scatter(team1_data['X'], team1_data['Y'], color='blue', label='Team 1')

    team2_data = frame_data[frame_data['Team'] == 'Team B']
    ax.scatter(team2_data['X'], team2_data['Y'], color='red', label='Team 2')

    ax.legend()

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Player positions in frame 1')

    ax.set_xlim([0, 105])
    ax.set_ylim([0, 68])

ani = animation.FuncAnimation(fig, animate, frames=range(df['Frame'].min(), df['Frame'].max() + 1), interval=1000/25)

ani.save('soccer_match_simulation.mp4', writer='ffmpeg')

plt.close(fig)
