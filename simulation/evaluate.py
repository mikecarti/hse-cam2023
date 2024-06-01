import pandas as pd
import numpy as np

import warnings 
warnings.filterwarnings("ignore")

df_sim = pd.read_csv('soccer_sim.csv')
df_game = pd.read_csv('heatmaps/clear_data.csv')
df_game = df_game[df_game['Period'] == 1]

def calculate_player_stats_sim(player_id: int, team: str, dt: float, sim_num: int):
    filename = f'soccer_simulations/soccer_sim_{sim_num}.csv'

    df_sim = pd.read_csv(filename)
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

def calculate_all_players_stats(dt: float, num_sims: int):
    player_teams = df_sim[['Player', 'Team']].drop_duplicates().values
    avg_stats_sim = []

    avg_stats_sim = pd.DataFrame(columns=['Player_id', 'Team', 'Mean', 'Variance', 'Direction'])
    stats_df_game = pd.DataFrame(columns=['Player_id', 'Mean', 'Variance', 'Direction'])

    for player_id, team in player_teams:
        mean_speed_sum = 0
        speed_variance_sum = 0
        avg_direction_vector_sum = np.zeros(2)
        
        for sim_number in range(1, num_sims + 1):
            mean_speed_sim, speed_variance_sim, avg_direction_vector_sim = calculate_player_stats_sim(player_id, team, dt, sim_number)
            
            mean_speed_sum += mean_speed_sim
            speed_variance_sum += speed_variance_sim
            avg_direction_vector_sum += np.array(avg_direction_vector_sim)
        
        num_sims_float = float(num_sims)
        avg_mean_speed = mean_speed_sum / num_sims_float
        avg_speed_variance = speed_variance_sum / num_sims_float
        avg_direction_vector = avg_direction_vector_sum / num_sims_float

        new_row = pd.DataFrame({
            'Player_id': [f"Player{player_id + 1}"],
            'Team': [team],
            'Mean': [mean_speed_sim],
            'Variance': [speed_variance_sim],
            'Direction': [avg_direction_vector_sim]
        })

        avg_stats_sim = pd.concat([avg_stats_sim, new_row], ignore_index=True) 

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

    return avg_stats_sim, stats_df_game

dt = 0.04
num_sims = 20
stats_df_sim, stats_df_game = calculate_all_players_stats(dt, num_sims)  
stats_df_sim['Player_id'] = stats_df_game['Player_id']
stats_df_sim.drop(['Team'], axis=1, inplace=True)
stats_df_sim.to_csv('results/stats_sim.csv', index=False)
stats_df_game.to_csv('results/stats_game.csv', index=False)
print("Simulation Stats:\n", stats_df_sim)
print("Game Stats:\n", stats_df_game)

