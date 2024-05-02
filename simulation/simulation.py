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
goal_A = config['goal_A']
goal_B = config['goal_B']


class Grid:
    """
    This class represents a grid on which the soccer match is played.

    :param width: The width of the grid.
    :type width: int
    :param height: The height of the grid.
    :type height: int
    """

    def __init__(self, width: int, height: int):
        """
        Constructs all the necessary attributes for the grid object.
        """

        self.width = width
        self.height = height

class Goal:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range

class Ball:
    """
    This class represents the ball in a soccer match
    :param position: coordinates of the ball 
    :type position: Tuple
    :param player: corresponds to the player's ID, who is controlling the ball
    :type player: int
    """

    def __init__(self, position: Tuple[int, int]):
        self.position = position
        self.controlled_by = None
        self.target_player = None
    
    def move_towards_target(self, target):
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
    """
    This class represents a player in the soccer match.

    :param team_name: The name of the team the player belongs to.
    :type team_name: str
    :param player_id: The unique identifier for the player.
    :type player_id: int
    :param default_position: The default position of the player on the grid.
    :type default_position: Tuple
    """

    def __init__(self, team_name: str, player_id: int, default_position: tuple[int, int]):
        """
        Constructs all the necessary attributes for the player object.
        """

        self.team_name = team_name
        self.player_id = player_id
        self.default_position = default_position
        self.current_position = default_position
        self.positions = []
        self.has_ball_control = False

    def move(self, grid, target):
        """
        Provides basic logic on player movement on the grid.

        :param grid: The grid on which the player moves.
        :type grid: Grid
        """

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

    def pass_ball(self, ball, target_player):
        if self.has_ball_control:
            ball.controlled_by = target_player
            self.has_ball_control = False

    def hit_ball(self, ball, target):
        if self.has_ball_control:
            ball.target = target
            ball.controlled_by = None
            self.has_ball_control = False

    def control_ball(self, ball):
        if self.current_position == ball.position:
            ball.controlled_by = self
            self.has_ball_control = True

class Goalkeeper(Player):
    def __init__(self, team_name: str, player_id: int, default_position: tuple[int, int]):
        super().__init__(team_name, player_id, default_position)

class OffencePlayer(Player):
    def __init__(self, team_name: str, player_id: int, default_position: tuple[int, int]):
        super().__init__(team_name, player_id, default_position)

class CenterPlayer(Player):
    def __init__(self, team_name: str, player_id: int, default_position: tuple[int, int], zone: tuple[int, int]):
        super().__init__(team_name, player_id, default_position)
        self.zone = zone

    def move(self, ball, opposing_team):
        if self.team.mode == 'defensive':
            if not (self.zone[0] <= ball.position[0] <= self.zone[1]):
                opposing_player_positions = [player.current_position for player in opposing_team.players]
                distances_to_opponents = [np.linalg.norm(np.array(self.current_position) - np.array(pos)) for pos in opposing_player_positions]
                closest_opponent = opposing_team.players[np.argmin(distances_to_opponents)]
                self.target = closest_opponent.current_position
            else:
                distances = [np.linalg.norm(np.array(player.current_position) - np.array(ball.position)) for player in self.team.players]
                closest_player = self.team.players[np.argmin(distances)]
                if self == closest_player:
                    self.target = ball.position
                else:
                    opposing_player_positions = [player.current_position for player in opposing_team.players]
                    distances_to_opponents = [np.linalg.norm(np.array(self.current_position) - np.array(pos)) for pos in opposing_player_positions]
                    closest_opponent = opposing_team.players[np.argmin(distances_to_opponents)]
                    self.target = closest_opponent.current_position
            else:
                if self.zone[0] <= ball.position[0] <= self.zone[1]:
                    if self.team_name == 'Team A':
                        self.target = (self.zone[1], self.current_position[1])
                    else:
                        self.target = (self.zone[0], self.current_position[1])
                else:
                    self.target = (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))

        super().move(self.target)

class DefencePlayer(Player):
    def __init__(self, team_name: str, player_id: int, default_position: tuple[int, int], zone: tuple[int, int]):
        super().__init__(team_name, player_id, default_position)
        self.zone = zone  

    def move(self, ball, opposing_team):
        if self.team_name == 'Team A':
            opposing_offence_players = opposing_team.players[8:10]
        else:
            opposing_offence_players = opposing_team_players[18:20]

        if self.team.mode == 'defensive' and not (self.zone[0] <= ball.position <= self.zone[1]):
            if self.player_id % 2 == 0:
                self.target = opposing_offensive_players[0].current_position
            else:
                self.target = opposing_offensive_players[1].current_position
        elif self.team.mode == 'defensive' and (self.zone[0] <= ball.position[0] <= self.zone[1]):
            distances = [np.linalg.norm(np.array(player.current_position) - np.array(ball.position)) for player in self.team.players]
            closest_player = self.team.players[np.argmin(distances)]
            if self == closest_player:
                self.target = ball.position
            else:
                opposing_player_positions = [player.current_position for player in opposing_team.players]
                distances_to_opponents = [np.linalg.norm(np.array(self.current_position) - np.array(pos)) for pos in opposing_player_positions]
                closest_opponent = opposing_team.players[np.argmin(distances_to_opponents)]
                self.target = closest_opponent.current_position
        else:
            self.target = (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))

        super().move(self.target)


class Team:
    """
    This class represents a team in the soccer match.

    :param name: The name of the team.
    :type name: str
    :param formation: The formation of the team.
    :type formation: list
    """

    def __init__(self, name: str, formation: list[int]):
        """
        Constructs all the necessary attributes for the team object.
        """
        self.name = name
        self.players = []
        for i, pos in enumerate(formation):
            if i == 10:
                self.players.append(Goalkeeper(name, i, pos))
            elif 5 <= i <= 7:
                self.players.append(CenterPlayer(name, i, pos))
            elif 1 <= i <= 3:
                self.players.append(DefencePlayer(name, i, pos))
            else:
                self.players.append(OffencePlayer(name, i, pos))

    def move(self, grid, ball):
        """
        Moves all the players on the grid.

        :param grid: The grid on which the players move.
        :type grid: Grid
        """
        for player in self.players:
            player.move(player.target)
            player.control_ball(ball)

    def pass_ball(self, ball, from_player_id, to_player_id):
        from_player = self.players[from_player_id]
        to_player = self.players[to_player_id]
        from_player.pass_ball(ball, to_player)

    def update_mode(self):
        if any(player.has_ball_control for player in self.players):
            self.mode = "offensive"
        else:
            self.mode = "defensive"

class SoccerMatch:
    """
    This class represents a soccer match.

    :param grid: The grid on which the match is played.
    :type grid: Grid
    :param team1: The first team.
    :type team1: Team
    :param formation1: The formation of the first team.
    :type formation1: list
    :param team2: The second team.
    :type team2: Team
    :param formation2: The formation of the second team.
    :type formation2: list
    """

    def __init__(self, grid, team1, formation1: list[int], team2, formation2: list[int]):
        """
        Constructs all the necessary attributes for the team object.
        """

        self.grid = grid
        self.team1 = Team(team1, formation1)
        self.team2 = Team(team2, formation2)
        random_team = random.choice([self.team1, self.team2])
        random_player = random.choice(random_team.players)
        self.ball = Ball(random_player.current_position)
        self.ball.controlled_by = random_player
        random_player.has_ball_control = True

    def simulate(self):
        """
        Simulates the soccer match and returns a DataFrame with the results.

        :return: A DataFrame with the results of the simulation.
        :rtype: DataFrame
        """

        data = []
        for i in range(framerate * sim_length_sec):
            self.team1.move(self.grid, self.ball)
            self.team2.move(self.grid, self.ball)
            if self.ball.target_player is not None:
                self.ball.move_towards_target()
            for team in [self.team1, self.team2]:
                for player in team.players:
                    data.append([1, i, i*0.04, team.name, player.player_id, *player.current_position, *self.ball.position])
                    if player.current_position == self.ball.position and self.ball.controlled_by and self.ball.controlled_by != player \
                            and random.random() < 0.5:
                        self.ball.controlled_by.has_ball_control = False
                        self.ball.controlled_by = player
                        player.has_ball_control = True
        df = pd.DataFrame(data, columns=['Period', 'Frame', 'Time [s]', 'Team', 'Player', 'X', 'Y', 'Ball_x', 'Ball_y'])
        df = df.pivot(index=['Period', 'Frame', 'Time [s]', 'Ball_x', 'Ball_y'], columns=['Team', 'Player'])
        df.columns = [f'Player{player_id+1}_{coord}' for player_id in range(22) for coord in ['x', 'y']]
        df.reset_index(inplace=True)
        columns = list(df.columns)
        columns_ball_reordered = [col for col in columns if col not in ['Ball_x', 'Ball_y']] + ['Ball_x', 'Ball_y']
        df = df[columns_ball_reordered]
        return df

df_formations = pd.read_csv('../heatmaps/heatmaps.csv', header=None, names=['area_x', 'area_y', 'x', 'y'], sep=',')
df_team_A = df.iloc[:11]
df_team_B = df.iloc[11:]
formation1 = list(df_team1[['x', 'y']].itertuples(index=False, name=None))
formation2 = list(df_team2[['x', 'y']].itertuples(index=False, name=None))
field = Grid(grid_width, grid_height)
match = SoccerMatch(field, 'Team A', formation1, 'Team B', formation2)
df = match.simulate()
df.to_csv('soccer_sim.csv', index=False)
