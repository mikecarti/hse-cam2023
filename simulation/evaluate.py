import pandas as pd
import numpy as np

import warnings 
warnings.filterwarnings("ignore")

df_sim = pd.read_csv('soccer_sim.csv')
df_game = pd.read_csv('heatmaps/clear_data.csv')
df_game = df_game[df_game['Period'] == 1]

def calculate_player_stats_sim(player_id: int, team: str, dt: float):
    player_df = df_sim[(df_sim['Player'] == player_id) & (df_sim['Team'] == team)]

    player_df['Vx'] = player_df['X'].diff() / dt
    player_df['Vy'] = player_df['Y'].diff() / dt

    player_df['Speed'] = np.sqrt(player_df['Vx']**2 + player_df['Vy']**2)

    mean_speed = player_df['Speed'].mean()
    speed_variance = player_df['Speed'].var()

    player_df['Direction_X'] = np.arctan2(player_df['Vy'], player_df['Vx'])
    player_df['Direction_Y'] = np.arctan2(player_df['Vy'], player_df['Vx'])

    avg_direction_vector = [player_df['Direction_X'].mean(), player_df['Direction_Y'].mean()]

    return mean_speed, speed_variance, avg_direction_vector


def calculate_player_stats_game(player_id: str, dt: float):
    player_df = df_game[['Time [s]', player_id + '_x', player_id + '_y']]

    player_df['Vx'] = player_df[player_id + '_x'].diff() / dt
    player_df['Vy'] = player_df[player_id + '_y'].diff() / dt

    player_df['Speed'] = np.sqrt(player_df['Vx']**2 + player_df['Vy']**2)

    mean_speed = player_df['Speed'].mean()
    speed_variance = player_df['Speed'].var()

    player_df['Direction_X'] = np.arctan2(player_df['Vy'], player_df['Vx'])
    player_df['Direction_Y'] = np.arctan2(player_df['Vy'], player_df['Vy'])

    avg_direction_vector = [player_df['Direction_X'].mean(), player_df['Direction_Y'].mean()]

    return mean_speed, speed_variance, avg_direction_vector

def calculate_all_players_stats(dt: float):
    player_teams = df_sim[['Player', 'Team']].drop_duplicates().values

    stats_df_sim = pd.DataFrame(columns=['Player_id', 'Team', 'Mean', 'Variance', 'Direction'])
    stats_df_game = pd.DataFrame(columns=['Player_id', 'Mean', 'Variance', 'Direction'])

    for player_id, team in player_teams:
        mean_speed_sim, speed_variance_sim, avg_direction_vector_sim = calculate_player_stats_sim(player_id, team, dt)

        new_row = pd.DataFrame({
            'Player_id': [player_id],
            'Team': [team],
            'Mean': [mean_speed_sim],
            'Variance': [speed_variance_sim],
            'Direction': [avg_direction_vector_sim]
        })

        stats_df_sim = pd.concat([stats_df_sim, new_row], ignore_index=True) 

    for i in range(1, 23):
        player_id_game = 'Player' + str(i)
        mean_speed_game, speed_variance_game, avg_direction_vector_game = calculate_player_stats_game(player_id_game, dt)

        new_row = pd.DataFrame({
            'Player_id': [player_id_game],
            'Mean': [mean_speed_game],
            'Variance': [speed_variance_game],
            'Direction': [avg_direction_vector_game]
        })

        stats_df_game = pd.concat([stats_df_game, new_row], ignore_index=True)

    return stats_df_sim, stats_df_game

dt = 0.04
stats_df_sim, stats_df_game = calculate_all_players_stats(dt)  
print("Simulation Stats:\n", stats_df_sim)
print("Game Stats:\n", stats_df_game)

