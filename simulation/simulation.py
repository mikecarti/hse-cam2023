import random
import pandas as pd
import numpy as np
import yaml
import random
from typing import Tuple, List

# TODO: приступить к работе с хитмапами на каждого игрока
# для последующей имплементации в симуляции.

# дописать наследующие классы для класса игрок, закинуть зоны в конфиг,
# прописать логику для класса player - для движения с мячом, мяч должен рандомно доставаться одному из игроков в начале симуляции.


with open("simulation_config.yaml", "r") as config_file:
    sim_config = yaml.safe_load(config_file)

grid_height = sim_config["height"]
grid_width = sim_config["width"]
sim_length_sec = sim_config["simulation_length_seconds"]
framerate = sim_config["framerate"]
goal_A = sim_config['goal_A']
goal_B = sim_config['goal_B']


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Goal:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range

class Ball:
    def __init__(self, position, grid):
        self.current_position = position
        self.controlled_by = None
        self.target = None
    
    def move_towards_target(self, grid, target):
        direction = [0, 0]
        dx = target[0] - self.current_position[0]
        dy = target[1] - self.current_position[1]
        direction = (dx / abs(dx) if dx != 0 else 0, dy / abs(dy) if dy != 0 else 0)

        x = self.current_position[0] + direction[0]
        y = self.current_position[1] + direction[1]
        x = max(0, min(x, grid.width))
        y = max(0, min(y, grid.height))

        self.current_position = (x, y)
        self.positions.append(self.current_position)      


class Player:
    def __init__(self, team_name, team, player_id, default_position, grid):
        self.team_name = team_name
        self.player_id = player_id
        self.default_position = default_position
        self.current_position = default_position
        self.positions = []
        self.has_ball_control = False
        self.team = team
        self.grid = grid

    def move(self, grid, target):
        direction = [0, 0]
        dx = target[0] - self.current_position[0]
        dy = target[1] - self.current_position[1]
        direction = (dx / abs(dx) if dx != 0 else 0, dy / abs(dy) if dy != 0 else 0)

        x = self.current_position[0] + direction[0]
        y = self.current_position[1] + direction[1]
        x = max(0, min(x, grid.width))
        y = max(0, min(y, grid.height))

        self.current_position = (x, y)
        self.positions.append(self.current_position)

    def hit_ball(self, ball, target):
        if self.has_ball_control:
            ball.target = target
            ball.controlled_by = None
            self.has_ball_control = False
            # team mode update for both teams

    def control_ball(self, ball):
        if self.current_position == ball.current_position:
            ball.controlled_by = self
            self.has_ball_control = True
            #team mode update for both teams

class Goalkeeper(Player):
    def __init__(self, team_name, team, player_id, default_position, grid, zone):
        super().__init__(team_name, team, player_id, default_position, grid)
        self.zone = zone
        self.target = None

    def move(self, ball, target):
        self.target = (np.random.randint(self.zone[0][0], self.zone[0][1]), np.random.randint(self.zone[1][0], self.zone[1][1]))
        super().move(self.grid, self.target)

class OffencePlayer(Player):
    def __init__(self, team_name, team, player_id, default_position, grid, zone):
        super().__init__(team_name, team, player_id, default_position, grid)
        self.zone = zone
        self.target = None

    def move(self, ball, opposing_team):
        if self.team.mode == 'defensive':
            if not (self.zone[0] <= int(ball[0]) <= self.zone[1]):
                self.target = (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))
            else:
                self.target = ball
        super().move(self.grid, self.target)

class CenterPlayer(Player):
    def __init__(self, team_name, team, player_id, default_position, grid, zone):
        super().__init__(team_name, team, player_id, default_position, grid)
        self.zone = zone
        self.target = None

    def move(self, ball, opposing_team):
        if self.team.mode == 'defensive':
            if not (self.zone[0] <= int(ball[0]) <= self.zone[1]):
                opposing_player_positions = [player.current_position for player in opposing_team.players]
                distances_to_opponents = [np.linalg.norm(np.array(self.current_position) - np.array(pos)) for pos in opposing_player_positions]
                closest_opponent = opposing_team.players[np.argmin(distances_to_opponents)]
                self.target = closest_opponent.current_position
            else:
                distances = [np.linalg.norm(np.array(player.current_position) - np.array(ball)) for player in self.team.players]
                closest_player = self.team.players[np.argmin(distances)]
                if self == closest_player:
                    self.target = ball
                else:
                    opposing_player_positions = [player.current_position for player in opposing_team.players]
                    distances_to_opponents = [np.linalg.norm(np.array(self.current_position) - np.array(pos)) for pos in opposing_player_positions]
                    closest_opponent = opposing_team.players[np.argmin(distances_to_opponents)]
                    self.target = closest_opponent.current_position
        else:
            if self.zone[0] <= ball[0] <= self.zone[1]:
                if self.team_name == 'Team A':
                    self.target = (self.zone[1], self.current_position[1])
                else:
                    self.target = (self.zone[0], self.current_position[1])
            else:
                self.target = (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))

        super().move(self.grid, self.target)

class DefencePlayer(Player):
    def __init__(self, team_name, team, player_id, default_position: tuple[int, int], grid, zone: tuple[int, int]):
        super().__init__(team_name, team, player_id, default_position, grid)
        self.zone = zone 
        self.target = [0,0]
        self.grid = grid

    def move(self, ball, opposing_team):
        if self.team_name == 'Team A':
            opposing_offence_players = opposing_team.players[8:10]
        else:
            opposing_offence_players = opposing_team.players[18:20]
        
        if self.team.mode == 'defensive' and not (self.zone[0] <= int(ball[0]) <= self.zone[1]):
            if self.player_id % 2 == 0:
                self.target = opposing_offence_players[0].current_position
            else:
                self.target = opposing_offence_players[1].current_position
        elif self.team.mode == 'defensive' and (self.zone[0] <= int(ball[0]) <= self.zone[1]):
            distances = [np.linalg.norm(np.array(player.current_position) - np.array(ball)) for player in self.team.players]
            closest_player = self.team.players[np.argmin(distances)]
            if self == closest_player:
                self.target = ball
            else:
                opposing_player_positions = [player.current_position for player in opposing_team.players]
                distances_to_opponents = [np.linalg.norm(np.array(self.current_position) - np.array(pos)) for pos in opposing_player_positions]
                closest_opponent = opposing_team.players[np.argmin(distances_to_opponents)]
                self.target = closest_opponent.current_position
        else:
            self.target = (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))
        super().move(self.grid, self.target)


class Team:
    def __init__(self, name: str, grid, formation: List[int], opposing_team = None):
        self.name = name
        self.opposing_team = opposing_team
        self.players = []
        for i, pos in enumerate(formation):
            if i == 10:
                if self.name == 'Team_A':
                    self.players.append(Goalkeeper(name, self, i, pos, grid, [[0, 5], [45, 55]]))
                else:
                    self.players.append(Goalkeeper(name, self, i, pos, grid, [[95, 100], [45, 55]]))
            elif 4 <= i <= 7:
                if self.name == 'Team_A':
                    self.players.append(CenterPlayer(name, self, i, pos, grid, [35, 65]))
                else:
                    self.players.append(CenterPlayer(name, self, i, pos, grid, [35, 65]))
            elif 0 <= i <= 3:
                if self.name == 'Team_A':
                    self.players.append(DefencePlayer(name, self, i, pos, grid, [5, 35]))
                else:
                    self.players.append(DefencePlayer(name, self, i, pos, grid, [65, 95]))
            else:
                if self.name == 'Team_A':
                    self.players.append(OffencePlayer(name, self, i, pos, grid, [65, 95]))
                else:
                    self.players.append(OffencePlayer(name, self, i, pos, grid, [5, 35]))
        self.mode = ('offensive' if any(player.has_ball_control for player in self.players) else 'defensive')


    def move(self, grid, ball):
        for player in self.players:
            player.move(ball.current_position, self.opposing_team)

    def pass_ball(self, ball, from_player_id, to_player_id):
        from_player = self.players[from_player_id]
        to_player = self.players[to_player_id]
        from_player.hit_ball(ball, to_player)

    def update_mode(self):
        if any(player.has_ball_control for player in self.players):
            self.mode = "offensive"
        else:
            self.mode = "defensive"

class SoccerMatch:
    def __init__(self, grid, team1, formation1: List[int], team2, formation2: List[int]):
        self.grid = grid
        self.team1 = Team(team1, self.grid, formation1)
        self.team2 = Team(team2, self.grid, formation2)
        self.team1.opposing_team = self.team2
        self.team2.opposing_team = self.team1
        random_team = random.choice([self.team1, self.team2])
        random_player = random.choice(random_team.players)
        self.ball = Ball([50,25], self.grid)
        self.ball.controlled_by = random_player
        random_player.has_ball_control = True

    def simulate(self):
        data = []
        for i in range(framerate * sim_length_sec):
            self.team1.move(self.grid, self.ball)
            self.team2.move(self.grid, self.ball)
            if self.ball.target is not None:
                self.ball.move_towards_target(self.grid, self.ball.target.current_position)
            for team in [self.team1, self.team2]:
                for player in team.players:
                    data.append([1, i, i*0.04, team.name, player.player_id, *player.current_position, *self.ball.current_position])
        df = pd.DataFrame(data, columns=['Period', 'Frame', 'Time [s]', 'Team', 'Player', 'X', 'Y', 'Ball_x', 'Ball_y'])
        df = df.pivot(index=['Period', 'Frame', 'Time [s]', 'Ball_x', 'Ball_y'], columns=['Team', 'Player'])
        df.columns = [f'Player{player_id+1}_{coord}' for player_id in range(22) for coord in ['x', 'y']]
        df.reset_index(inplace=True)
        columns = list(df.columns)
        columns_ball_reordered = [col for col in columns if col not in ['Ball_x', 'Ball_y']] + ['Ball_x', 'Ball_y']
        df = df[columns_ball_reordered]
        return df

df_formations = pd.read_csv('formation442.csv', header=None, names=['area_x', 'area_y', 'x', 'y'], sep=',')
df_team_A = df_formations.iloc[1:12]
df_team_A = df_team_A.astype(int)
df_team_B = df_formations.iloc[12:]
df_team_B = df_team_B.astype(int)
formation1 = list(df_team_A[['x', 'y']].itertuples(index=False, name=None))
formation2 = list(df_team_B[['x', 'y']].itertuples(index=False, name=None))
field = Grid(grid_width, grid_height)
match = SoccerMatch(field, 'Team A', formation1, 'Team B', formation2)
df = match.simulate()
df.to_csv('soccer_sim.csv', index=False)
