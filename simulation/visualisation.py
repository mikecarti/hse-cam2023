import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('soccer_sim.csv')

fig, ax = plt.subplots()
def animate(frame_number):
    ax.clear()
    frame_data = df[df['Frame'] == frame_number]

# Plotting players of team 1
    team1_data = frame_data[frame_data['Team'] == 'Team A']
    ax.scatter(team1_data['X'], team1_data['Y'], color='blue', label='Team 1')

# Plotting players of team 2
    team2_data = frame_data[frame_data['Team'] == 'Team B']
    ax.scatter(team2_data['X'], team2_data['Y'], color='red', label='Team 2')

    ax.legend()

# Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Player positions in frame 1')

ani = animation.FuncAnimation(fig, animate, frames=range(df['Frame'].min(), df['Frame'].max() + 1), interval=1000/25)

ani.save('soccer_match_simulation.mp4', writer='ffmpeg')

plt.close(fig)
