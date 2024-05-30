import pandas as pd
import numpy as np

import warnings 
warnings.filterwarnings("ignore")

df_sim = pd.read_csv('soccer_sim.csv')

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

def calculate_all_players_stats(dt: float):
    player_teams = df_sim[['Player', 'Team']].drop_duplicates().values

    stats_df = pd.DataFrame(columns=['Player', 'Team', 'Mean', 'Variance', 'Direction'])

    for player_id, team in player_teams:
        mean_speed, speed_variance, avg_direction_vector = calculate_player_stats_sim(player_id, team, dt)

        stats_df = pd.concat([stats_df, pd.DataFrame({
            'Player': player_id,
            'Team': team,
            'Mean': mean_speed,
            'Variance': speed_variance,
            'Direction': avg_direction_vector
        })], ignore_index=True)

    return stats_df

stats_df = calculate_all_players_stats(0.04)  
#print(stats_df)

