import random
import pandas as pd
import yaml

#TODO: написать докстринги, приступить к работе с хитмапами на каждого игрока
# для последующей имплементации в симуляции, прописать пару-тройку дефолтных
# формаций для команд вместо рандомно генерящихся.

class Grid:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class Player:
    def __init__(self, team_name: str, player_id: int, default_position):
        self.team_name = team_name
        self.player_id = player_id
        self.default_position = default_position
        self.current_position = default_position
        self.positions = []

    def move(self, grid):
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
    def __init__(self, name, formation):
        self.name = name
        self.players = [Player(name, i, pos) for i, pos in enumerate(formation)]

    def move(self, grid):
        for player in self.players:
            player.move(grid)

class SoccerMatch:

    def __init__(self, grid, team1, formation1, team2, formation2):
        self.grid = grid
        self.team1 = Team(team1, formation1)
        self.team2 = Team(team2, formation2)

    def simulate(self):
        data = []
        for i in range(1*15*25): 
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
