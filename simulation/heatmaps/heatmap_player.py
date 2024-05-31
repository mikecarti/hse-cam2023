#Assumption: the new, substitute players have the same posiitons, as the previous ones.

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import yaml

import warnings 
warnings.filterwarnings("ignore")

with open("heatmap_config.yaml", "r") as config_file:
    heatmap_config = yaml.safe_load(config_file)

PERIOD = 1
height = heatmap_config["height"]
width = heatmap_config["width"]

raw_data_away = pd.read_csv('raw_data/Sample_Game_1_RawTrackingData_Away_Team.csv', sep=',')
raw_data_home = pd.read_csv('raw_data/Sample_Game_1_RawTrackingData_Home_Team.csv', sep=',')


column_list_away = ['Period', 'Frame', 'Time [s]', 'Player25_x', 'Player25_y', 'Player15_x', 'Player15_y', 'Player16_x', 'Player16_y', 'Player17_x', 'Player17_y', \
              'Player18_x', 'Player18_y', 'Player19_x', 'Player19_y', 'Player20_x', 'Player20_y', 'Player21_x', 'Player21_y', 'Player22_x', 'Player22_y', \
              'Player23_x', 'Player23_y', 'Player24_x', 'Player24_y', 'Player26_x', 'Player26_y', 'Player27_x', 'Player27_y', 'Player28_x', 'Player28_y','Ball_x', 'Ball_y']
column_list_home = ['Period', 'Frame', 'Time [s]', 'Player11_x', 'Player11_y', 'Player1_x', 'Player1_y', 'Player2_x', 'Player2_y', 'Player3_x', 'Player3_y', \
              'Player4_x', 'Player4_y', 'Player5_x', 'Player5_y', 'Player6_x', 'Player6_y', 'Player7_x', 'Player7_y', 'Player8_x', 'Player8_y', \
              'Player9_x', 'Player9_y', 'Player10_x', 'Player10_y', 'Player12_x', 'Player12_y', 'Player13_x', 'Player13_y', 'Player14_x', 'Player14_y', 'Ball_x', 'Ball_y']

data_home = raw_data_home.iloc[2:]
data_away = raw_data_away.iloc[2:]
data_home.columns = column_list_home
data_away.columns = column_list_away
data_home['Player1_x'] = data_home['Player1_x'].combine_first(data_home['Player12_x']) 
data_home['Player1_y'] = data_home['Player1_y'].combine_first(data_home['Player12_y']) 
data_home['Player6_x'] = data_home['Player6_x'].combine_first(data_home['Player13_x']) 
data_home['Player6_y'] = data_home['Player6_y'].combine_first(data_home['Player13_y']) 
data_home['Player10_x'] = data_home['Player10_x'].combine_first(data_home['Player14_x']) 
data_home['Player10_y'] = data_home['Player10_y'].combine_first(data_home['Player14_y']) 
data_away['Player19_x'] = data_away['Player19_x'].combine_first(data_away['Player28_x']) 
data_away['Player19_y'] = data_away['Player19_y'].combine_first(data_away['Player28_y']) 
data_away['Player24_x'] = data_away['Player24_x'].combine_first(data_away['Player26_x']) 
data_away['Player24_y'] = data_away['Player24_y'].combine_first(data_away['Player26_y']) 
data_away['Player22_x'] = data_away['Player22_x'].combine_first(data_away['Player27_x']) 
data_away['Player22_y'] = data_away['Player22_y'].combine_first(data_away['Player27_y']) 

data_home.drop(['Player12_x', 'Player12_y', 'Player13_x', 'Player13_y', 'Player14_x', 'Player14_y', 'Ball_x', 'Ball_y'], axis=1, inplace=True)
data_away.drop(['Player26_x', 'Player26_y', 'Player27_x', 'Player27_y', 'Player28_x', 'Player28_y'], axis=1, inplace=True)
columns_home = list(data_home.columns)
columns_away = list(data_away.columns)
reorder_home = ['Player11_x', 'Player11_y']
reorder_away = ['Player25_x', 'Player25_y', 'Ball_x', 'Ball_y']

columns_home_reordered = [col for col in columns_home if col not in reorder_home] + reorder_home
columns_away_reordered = [col for col in columns_away if col not in reorder_away] + reorder_away
data_home = data_home[columns_home_reordered]
data_away = data_away[columns_away_reordered]

data_away.columns = ['Period', 'Frame', 'Time [s]'] + [f"Player{i}_{j}" for i in range(12, 23) for j in ('x', 'y')] + ['Ball_x', 'Ball_y']
data = data_home.merge(data_away, on=['Period', 'Frame', 'Time [s]'])

for i in range(1, 23):
    data[f'Player{i}_x'] = pd.to_numeric(data[f'Player{i}_x'], errors='coerce')
    data[f'Player{i}_y'] = pd.to_numeric(data[f'Player{i}_y'], errors='coerce')
    data[f'Player{i}_x'] = data[f'Player{i}_x'] * 100
    data[f'Player{i}_y'] = data[f'Player{i}_y'] * 100

data['Ball_x'] = pd.to_numeric(data['Ball_x'], errors='coerce')
data['Ball_x'] = pd.to_numeric(data['Ball_x'], errors='coerce')
data['Ball_x'] = data['Ball_x'] * 100
data['Ball_y'] = data['Ball_y'] * 100

data.to_csv('clear_data.csv', index=False)

def get_player_prob_matrix(data: pd.DataFrame, player_num: int, period: int):
    """
    Calculate the probability matrix for a player's position on the grid.

    :param data: The dataset containing player positions.
    :type data: pandas.DataFrame
    :param player_num: The number of the player.
    :type player_num: int
    :param period: The period of the game.
    :type period: int
    :return: The probability matrix for the player's position.
    :rtype: numpy.ndarray
    """

    data_period = data[data['Period'] == period]
    x = data_period[f'Player{player_num}_x'].values
    y = data_period[f'Player{player_num}_y'].values
    hist, xedges, yedges = np.histogram2d(x, y, bins=[width, height], range=[[0, width], [0, height]])
    prob_matrix = hist / np.sum(hist)
    return np.array(prob_matrix)


def assign_players_to_areas(data: pd.DataFrame, period: int):
    """
    Assign each player to an area of the grid based on their probability matrix.

    :param data: The dataset containing player positions.
    :type data: pandas.DataFrame
    :param period: The period of the game.
    :type period: int
    :return: A list of areas for each player.
    :rtype: list
    """

    player_areas = []
    for i in range(1, 23):
        matrix = get_player_prob_matrix(data, i, period)
        areas = [matrix[i:i+(width//10), j:j+(height//10)] for i in range(0,width,10) for j in range(0,height,10)]
        max_prob_area = max(areas, key=np.sum)
        player_areas.append(np.unravel_index(np.argmax(max_prob_area), max_prob_area.shape))
    return player_areas

def get_starting_positions(data, period: int):
    """
    Get the starting positions for each player.

    :param data: The dataset containing player positions.
    :type data: pandas.DataFrame
    :param period: The period of the game.
    :type period: int
    :return: A list of starting positions for each player.
    :rtype: list
    """

    formation = []
    for i in range(1, 23):
        player_prob_matrix = get_player_prob_matrix(data, i, period)
        max_prob_cell = np.unravel_index(np.argmax(player_prob_matrix), player_prob_matrix.shape)
        formation.append(max_prob_cell)
    return formation

player_areas = assign_players_to_areas(data, PERIOD)
initial_formation = get_starting_positions(data, PERIOD)
initial_formation_df = pd.DataFrame(initial_formation, columns=['x', 'y'])
player_areas_df = pd.DataFrame(player_areas, columns=['area_x', 'area_y'])
result_df = pd.concat([player_areas_df, initial_formation_df], axis=1)
result_df.to_csv('heatmaps.csv', index=False)
