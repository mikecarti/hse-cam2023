import random
import pandas as pd
import yaml
import random

# TODO: приступить к работе с хитмапами на каждого игрока
# для последующей имплементации в симуляции, прописать пару-тройку дефолтных
# формаций для команд вместо рандомно генерящихся.


with open("simulation_config.yaml", "r") as config_file:
    sim_config = yaml.safe_load(config_file)

grid_height = sim_config["height"]
grid_width = sim_config["width"]
sim_length_sec = sim_config["simulation_length_seconds"]
framerate = sim_config["framerate"]

initial_formations = [
    (56, 76),
    (39, 99),
    (50, 38),
    (49, 37),
    (54, 78),
    (54, 76),
    (43, 99),
    (50, 37),
    (55, 75),
    (45, 99),
    (25, 48),
    (93, 52),
    (62, 73),
    (57, 99),
    (59, 53),
    (74, 27),
    (72, 46),
    (61, 74),
    (76, 72),
    (57, 78),
    (55, 57),
    (98, 46)
]

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

class Ball:
    """
    This class represents the ball in a soccer match
    :param position: coordinates of the ball 
    :type position: Tuple
    :param player: corresponds to the player's ID, who is controlling the ball
    :type player: int
    """

    def __init__(self, position: tuple[int, int]):
        self.position = position
        self.controlled_by = None
        self.target_player = None

    def move_towards_target(self):
        if self.target_player is not None:
            dx = self.target_player.current_position[0] - self.position[0]
            dy = self.target_player.current_position[1] - self.position[1]
            direction = (dx / abs(dx) if dx != 0 else 0, dy / abs(dy) if dy != 0 else 0)
            x = self.position[0] + direction[0]
            y = self.position[1] + direction[1]
            self.position = (x, y)

    def pass_ball(self, player):
        if self.controlled_by is not None:
            self.controlled_by = None
            self.target_player = player


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

    def move(self, grid, ball):
        """
        Provides basic logic on player movement on the grid.

        :param grid: The grid on which the player moves.
        :type grid: Grid
        """

        direction = [0, 0]
        if random.random() < 0.3:
            dx = random.choice([-1, 1])
            dy = random.choice([-1, 1])
        else:
            dx = self.default_position[0] - self.current_position[0]
            dy = self.default_position[1] - self.current_position[1]
        direction = (dx / abs(dx) if dx != 0 else 0, dy / abs(dy) if dy != 0 else 0)

        x = self.current_position[0] + direction[0]
        y = self.current_position[1] + direction[1]
        x = max(0, min(x, grid.width))
        y = max(0, min(y, grid.height))

        self.current_position = (x, y)
        self.positions.append(self.current_position)

        if self.current_position == ball.position:
            self.has_ball_control = True
            ball.controlled_by = self
        else:
            self.has_ball_control = False

    def pass_ball(self, ball, players):
        opponents = [player for player in players if player.team_name != self.team_name]
        for opponent in opponents:
            if np.linalg.norm(np.array(self.current_position) - np.array(opponent.current_position)) < 2:
                teammates = [player for player in players if player.team_name == self.team_name and player != self]
                for teammate in teammates:
                    if self.current_position[0] == teammate.current_position[0] or self.current_position[1] == teammate.current_position[1]:
                        self.has_ball_control = False
                        ball.pass_ball(teammate)
                        return
        

class Goalkeeper(Player):
    def __init__(self, team_name: str, player_id: int, default_position: tuple[int, int], goal_position: tuple[int, int]):
        super().__init__(team_name, player_id, default_position)
        self.goal_position = goal_position

    def move(self, grid, ball):
        if ball.controlled_by and ball.controlled_by.team_name == self.team_name:
            dx = 5 if self.goal_position[0] < grid.width // 2 else -5
            dy = 0
        else:
            dx = self.goal_position[0] - self.current_position[0]
            dy = self.goal_position[1] - self.current_position[1]
        direction = (dx / abs(dx) if dx != 0 else 0, dy / abs(dy) if dy != 0 else 0)
        x = self.current_position[0] + direction[0]
        y = self.current_position[1] + direction[1]
        x = max(0, min(x, grid.width))
        y = max(0, min(y, grid.height))
        self.current_position = (x, y)
        self.positions.append(self.current_position)
        if self.current_position == ball.position:
            self.has_ball_control = True
            ball.controlled_by = self
        else:
            self.has_ball_control = False

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
        self.players = [Player(name, i, pos) for i, pos in enumerate(formation)]

    def move(self, grid, ball):
        """
        Moves all the players on the grid.

        :param grid: The grid on which the players move.
        :type grid: Grid
        """
        for player in self.players:
            player.move(grid, ball)

    def pass_ball(self, ball, from_player_id, to_player_id):
        from_player = self.players[from_player_id]
        to_player = self.players[to_player_id]
        from_player.pass_ball(ball, to_player)

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

#formation1 = [(random.randint(0, grid_width), random.randint(0, grid_height)) for _ in range(11)]
#formation2 = [(random.randint(0, grid_width), random.randint(0, grid_height)) for _ in range(11)]
formation1 = initial_formations[:11]
formation2 = initial_formations[11:]
field = Grid(grid_width, grid_height)
match = SoccerMatch(field, 'Team A', formation1, 'Team B', formation2)
df = match.simulate()
df.to_csv('soccer_sim.csv', index=False)
