import random
import pandas as pd
import numpy as np
import yaml
import random
from typing import Tuple, List

with open("simulation_config.yaml", "r") as config_file:
    sim_config = yaml.safe_load(config_file)

grid_height = sim_config["height"]
grid_width = sim_config["width"]
sim_length_sec = sim_config["simulation_length_seconds"]
framerate = sim_config["framerate"]


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Entity:
    def __init__(self, position, grid):
        self.current_position = position
        self.grid = grid

    def move(self, target):
        dx, dy = target[0] - self.current_position[0], target[1] - self.current_position[1]
        direction = (dx / abs(dx) if dx != 0 else 0, dy / abs(dy) if dy != 0 else 0)
        x, y = self.current_position[0] + direction[0], self.current_position[1] + direction[1]
        self.current_position = (max(0, min(x, self.grid.width)), max(0, min(y, self.grid.height)))


class Ball(Entity):
    def __init__(self, position, grid):
        super().__init__(position, grid)
        self.controlled_by = None
        self.target = None


class Player(Entity):
    # игрок должен бежать в свою зону, если не в ней
    def __init__(self, team_name, team, player_id, default_position, grid):
        super().__init__(default_position, grid)
        self.team_name = team_name
        self.player_id = player_id
        self.default_position = default_position
        self.has_ball_control = False
        self.team = team

    def hit_ball(self, ball, target):
        if self.has_ball_control:
            ball.target = target
            ball.controlled_by = None
            self.has_ball_control = False

    def control_ball(self, ball):
        if self.current_position == ball.current_position:
            ball.controlled_by = self
            self.has_ball_control = True

    def is_ball_in_zone(self, ball):
        return self.zone[0] <= int(ball[0]) <= self.zone[1]

    def is_closest_to_ball(self, ball):
        return self == self.team.players[np.argmin(
            [np.linalg.norm(np.array(player.current_position) - np.array(ball)) for player in self.team.players])]

    def get_closest_opposing_player(self, opposing_team):
        return opposing_team.players[np.argmin([np.linalg.norm(np.array(self.current_position) - np.array(pos)) \
                                                for pos in [player.current_position for player in
                                                            opposing_team.players]])].current_position

    def get_target_position(self, ball):
        return ball if self.is_ball_in_zone(ball) else (
        np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))


class Goalkeeper(Player):
    def __init__(self, team_name, team, player_id, default_position, grid, zone):
        super().__init__(team_name, team, player_id, default_position, grid)
        self.zone = zone

    def move(self, ball, target):
        self.target = (
        np.random.randint(self.zone[0][0], self.zone[0][1]), np.random.randint(self.zone[1][0], self.zone[1][1]))
        super().move(self.target)


class OffencePlayer(Player):
    def __init__(self, team_name, team, player_id, default_position, grid, zone):
        super().__init__(team_name, team, player_id, default_position, grid)
        self.zone = zone

    def move(self, ball, opposing_team):
        if self.team.mode == 'defensive':
            if not self.is_ball_in_zone:
                self.target = (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))
            else:
                self.target = ball
        else:
            if self.is_ball_in_zone:
                self.target = ball
            else:
                super().hit_ball(get_closest_opposing_player)
                self.target = (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))
        super().move(self.target)


class CenterPlayer(Player):
    def __init__(self, team_name, team, player_id, default_position, grid, zone):
        super().__init__(team_name, team, player_id, default_position, grid)
        self.zone = zone

    def move(self, ball, opposing_team):
        if self.team.mode == 'defensive' and not self.is_ball_in_zone(ball) or not self.is_closest_to_ball(ball):
            self.target = self.get_closest_opposing_player(opposing_team)
        else:
            self.target = self.get_target_position(ball)
        super().move(self.target)


class DefencePlayer(Player):
    def __init__(self, team_name, team, player_id, default_position, grid, zone):
        super().__init__(team_name, team, player_id, default_position, grid)
        self.zone = zone

    def move(self, ball, opposing_team):
        if self.team.mode == 'defensive' and not self.is_ball_in_zone(ball) or not self.is_closest_to_ball(ball):
            self.target = self.get_closest_opposing_player(opposing_team)
        else:
            self.target = self.get_target_position(ball)
        super().move(self.target)


class Team:
    def __init__(self, name: str, grid, formation: List[int], opposing_team=None):
        self.name = name
        self.opposing_team = opposing_team
        self.players = []
        for i, pos in enumerate(formation):
            if i >= 0 and i <= 3:
                if self.name == 'Team A':
                    self.players.append(DefencePlayer(name, self, i, pos, grid, [5, 35]))
                else:
                    self.players.append(DefencePlayer(name, self, i, pos, grid, [65, 95]))
            if i >= 4 and i <= 7:
                if self.name == 'Team A':
                    self.players.append(CenterPlayer(name, self, i, pos, grid, [35, 65]))
                else:
                    self.players.append(CenterPlayer(name, self, i, pos, grid, [35, 65]))
            if i >= 8 and i <= 9:
                if self.name == 'Team A':
                    self.players.append(OffencePlayer(name, self, i, pos, grid, [65, 95]))
                else:
                    self.players.append(OffencePlayer(name, self, i, pos, grid, [5, 35]))
            if i == 10:
                if self.name == 'Team A':
                    self.players.append(Goalkeeper(name, self, i, pos, grid, [[0, 5], [45, 55]]))
                else:
                    self.players.append(Goalkeeper(name, self, i, pos, grid, [[95, 100], [45, 55]]))

        self.mode = ('offensive' if any(player.has_ball_control for player in self.players) else 'defensive')

    def move(self, grid, ball):
        for player in self.players:
            player.move(ball.current_position, self.opposing_team)

    def update_mode(self):
        self.mode = "offensive" if any(player.has_ball_control for player in self.players) else "defensive"


class SoccerMatch:
    def __init__(self, grid, team1, formation1: List[int], team2, formation2: List[int]):
        self.grid = grid
        self.team1, self.team2 = Team(team1, self.grid, formation1), Team(team2, self.grid, formation2)
        self.team1.opposing_team, self.team2.opposing_team = self.team2, self.team1
        self.ball = Ball([50, 50], self.grid)

    def simulate(self):
        data = []
        for i in range(framerate * sim_length_sec):
            self.team1.move(self.grid, self.ball)
            self.team2.move(self.grid, self.ball)
            self.team1.update_mode()
            self.team2.update_mode()
            if self.ball.target is not None:
                self.ball.move_towards_target(self.grid, self.ball.target.current_position)
            for team in [self.team1, self.team2]:
                for player in team.players:
                    data.append([1, i, i * 0.04, team.name, player.player_id, *player.current_position,
                                 *self.ball.current_position])
        df = pd.DataFrame(data, columns=['Period', 'Frame', 'Time [s]', 'Team', 'Player', 'X', 'Y', 'Ball_x', 'Ball_y'])

        # df = df.pivot(index=['Period', 'Frame', 'Time [s]', 'Ball_x', 'Ball_y'], columns=['Team', 'Player'])
        # df.columns = [f'Player{player_id+1}_{coord}' for player_id in range(22) for coord in ['x', 'y']]
        # df.reset_index(inplace=True)
        # columns = list(df.columns)
        # columns_ball_reordered = [col for col in columns if col not in ['Ball_x', 'Ball_y']] + ['Ball_x', 'Ball_y']
        # df = df[columns_ball_reordered]
        return df


df_formations = pd.read_csv('formation442.csv', header=None, names=['area_x', 'area_y', 'x', 'y'], sep=',')
df_team_A = df_formations.iloc[:11]
df_team_B = df_formations.iloc[11:]
formation1 = list(df_team_A[['x', 'y']].itertuples(index=False, name=None))
formation2 = list(df_team_B[['x', 'y']].itertuples(index=False, name=None))
field = Grid(grid_width, grid_height)
match = SoccerMatch(field, 'Team A', formation1, 'Team B', formation2)
df = match.simulate()
df.to_csv('soccer_sim.csv', index=False)
