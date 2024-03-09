import random
import pandas as pd

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
'''
class Ball:
    def __init__(self, default_position, controller=None):
        self.position = position
        self.controller = controller

    def update_ball_position(self):
        if self.controller:
            self.position = self.controller.position
'''

class Player:
    def __init__(self, team_name, player_id, default_position):
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
        for i in range(1*15*25): #minutes * seconds * frames
            self.team1.move(self.grid)
            self.team2.move(self.grid)
            for team in [self.team1, self.team2]:
                for player in team.players:
                    data.append([i, team.name, player.player_id, *player.current_position])
        df = pd.DataFrame(data, columns=['Frame', 'Team', 'Player', 'X', 'Y'])
        return df

# Define formations
formation1 = [(random.randint(0, 105), random.randint(0, 68)) for _ in range(11)]  # random formation of Team1
formation2 = [(random.randint(0, 105), random.randint(0, 68)) for _ in range(11)]  # random formation of Team2

# Simulate a match between 'Team A' and 'Team B'
field = Grid(105,68)
match = SoccerMatch(field, 'Team A', formation1, 'Team B', formation2)
df = match.simulate()
df.to_csv('soccer_sim.csv', index=False)
