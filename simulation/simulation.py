import random
import pandas as pd
import yaml


# TODO: приступить к работе с хитмапами на каждого игрока
# для последующей имплементации в симуляции, прописать пару-тройку дефолтных
# формаций для команд вместо рандомно генерящихся.

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

    def move(self, grid):
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

    def move(self, grid):
        """
        Moves all the players on the grid.

        :param grid: The grid on which the players move.
        :type grid: Grid
        """
        for player in self.players:
            player.move(grid)


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

    def simulate(self):
        """
        Simulates the soccer match and returns a DataFrame with the results.

        :return: A DataFrame with the results of the simulation.
        :rtype: DataFrame
        """

        data = []
        for i in range(1 * 15 * 25):
            self.team1.move(self.grid)
            self.team2.move(self.grid)
            for team in [self.team1, self.team2]:
                for player in team.players:
                    data.append([i, team.name, player.player_id, *player.current_position])
        df = pd.DataFrame(data, columns=['Frame', 'Team', 'Player', 'X', 'Y'])
        return df


with open("simulation_config.yaml", "r") as config_file:
    sim_config = yaml.safe_load(config_file)

grid_height = sim_config["height"]
grid_width = sim_config["width"]

formation1 = [(random.randint(0, grid_width), random.randint(0, grid_height)) for _ in range(11)]
formation2 = [(random.randint(0, grid_width), random.randint(0, grid_height)) for _ in range(11)]

field = Grid(grid_width, grid_height)
match = SoccerMatch(field, 'Team A', formation1, 'Team B', formation2)
df = match.simulate()
df.to_csv('soccer_sim.csv', index=False)
