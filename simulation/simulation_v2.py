import pandas as pd
import numpy as np
import yaml
import math
import random
from typing import Tuple, List

with open("simulation_config.yaml", "r") as config_file:
    sim_config = yaml.safe_load(config_file)

grid_height = sim_config["height"]
grid_width = sim_config["width"]
sim_length_sec = sim_config["simulation_length_seconds"]
framerate = sim_config["framerate"]
acc = sim_config["acceleration"]

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Entity:
    def __init__(self, position, grid):
        self.current_position = position
        self.grid = grid
        self.speed = 0.2

    def move(self, target, speed = 0.15):
        dx, dy = target[0] - self.current_position[0], target[1] - self.current_position[1]
        direction = (dx / abs(dx) if dx != 0 else 0, dy / abs(dy) if dy != 0 else 0)
        x, y = self.current_position[0] + direction[0]*speed, self.current_position[1] + direction[1]*speed
        self.current_position = (max(0, min(x, self.grid.width)), max(0, min(y, self.grid.height)))

    def move_semicircle(self, target, speed = 0.2, radius=1):
        dx, dy = target[0] - self.current_position[0], target[1] - self.current_position[1]
        direction = (dx / abs(dx) if dx != 0 else 0, dy / abs(dy) if dy != 0 else 0)
        angle = math.atan2(dy, dx)
        angle = (angle + math.pi / 180) % (2 * math.pi)
        x = self.current_position[0] + radius * math.cos(angle)
        y = self.current_position[1] + radius * math.sin(angle)
        self.current_position = (max(0, min(x, self.grid.width)), max(0, min(y, self.grid.height)))

class Ball(Entity):
    def __init__(self, position, grid):
        super().__init__(position, grid)
        self.controlled_by = None
        #self.target

    def move_with_control(self, player_target):
        speed = self.speed if self.controlled_by is not None else self.speed
        super().move(player_target, speed)

class Player(Entity):
    def __init__(self, team_name, team, player_id, position, grid, ball):
        super().__init__(position, grid)
        self.team = team
        self.team_name = team_name
        self.player_id = player_id
        self.has_ball_control = False
        self.ball = ball

    def move(self, target):
        speed = self.speed
        if self.has_ball_control:
            nearest_teammate = self.get_nearest_teammate()
            closest_opponent = self.team.opposing_team.players[np.argmin([np.linalg.norm(np.array(self.current_position) - np.array(pos)) \
                                                for pos in [player.current_position for player in self.team.opposing_team.players]])] 
            if np.linalg.norm(np.array(self.current_position) - np.array(closest_opponent.current_position)) < 0.3:
                dx, dy = self.current_position[0] - closest_opponent.current_position[0], self.current_position[1] - closest_opponent.current_position[1]
                direction = (dx / abs(dx) if dx != 0 else 0, dy / abs(dy) if dy != 0 else 0)
                target = (self.current_position[0] + direction[0]*speed, self.current_position[1] + direction[1]*speed)
            else:
                if not self.opponent_between_target(nearest_teammate.current_position, self.team.opposing_team) and nearest_teammate.distance_to_opposing_goals() < self.distance_to_opposing_goals() and np.linalg.norm(np.array(self.current_position) - np.array(closest_opponent.current_position)) <= 1: 
                    self.hit_ball(self.ball, nearest_teammate.current_position)

                if self.current_position[0] >= self.team.hit_area[0][0] and self.current_position[0] <= self.team.hit_area[0][1] \
                     and self.current_position[1] >= self.team.hit_area[1][0] and self.current_position[1] <= self.team.hit_area[1][1]:
                    self.hit_ball(self.ball, (self.team.opposing_goals[0], np.random.randint(self.team.opposing_goals[1][0], self.team.opposing_goals[1][1])))
                    target = self.get_closest_opposing_player(self.team.opposing_team)
                else:
                    target = (self.team.opposing_goals[0], np.random.randint(self.team.opposing_goals[1][0], self.team.opposing_goals[1][1]))
                    self.ball.move(target)
        super().move(target, speed)
       
    def get_nearest_teammate(self):
        return min(self.team.players, key=lambda player: np.linalg.norm(np.array(self.current_position) - np.array(player.current_position)) \
                if player != self else float('inf'))

    def distance_to_opposing_goals(self):
        opposing_goals = np.array((self.team.opposing_goals[0], np.random.randint(self.team.opposing_goals[1][0], self.team.opposing_goals[1][1])))
        player_position = np.array(self.current_position)
        return np.linalg.norm(opposing_goals - player_position)

    def hit_ball(self, ball, target):
        #че дел если есть противник между таргетом и игрком?
        if self.has_ball_control:
            ball_speed = 2*self.speed
            self.ball.move(target, ball_speed)
            self.ball.controlled_by = None
            self.has_ball_control = False

    def is_ball_in_zone(self, ball):
        return self.zone[0] <= float(ball[0]) <= self.zone[1]

    def is_closest_to_ball(self, ball):
        return self == self.team.players[np.argmin([np.linalg.norm(np.array(player.current_position) - np.array(ball)) \
                for player in self.team.players])]

    def get_closest_opposing_player(self, opposing_team):
        return opposing_team.players[np.argmin([np.linalg.norm(np.array(self.current_position) - np.array(pos)) \
                                                for pos in [player.current_position for player in opposing_team.players]])].current_position

    def get_target_position(self, ball):
        return ball if self.is_ball_in_zone(ball) else (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))
        #return (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))
    
    def opponent_between_target(self, target, opposing_team):
        for player in opposing_team.players:
            if min(self.current_position[0], target[0]) <= player.current_position[0] <= max(self.current_position[0], target[0]) and \
               min(self.current_position[1], target[1]) <= player.current_position[1] <= max(self.current_position[1], target[1]):
                return player.current_position
        return False

class GoalKeeper(Player):
    def __init__(self, team_name, team, player_id, position, grid, ball, zone):
        super().__init__(team_name, team, player_id, position, grid, ball)
        self.zone = zone
    def move(self, ball, target):
        target = (np.random.randint(self.zone[0][0], self.zone[0][1]), np.random.randint(self.zone[1][0], self.zone[1][1]))
        super().move(target)

class OffencePlayer(Player):
    def __init__(self, team_name, team, player_id, position, grid, ball, zone):
        super().__init__(team_name, team, player_id, position, grid, ball)
        self.zone = zone
    def move(self, ball, opposing_team):
        target = self.get_target_position(ball)
        if self.team.mode == 'defensive':
            target = self.get_target_position(ball)
        else:
            target = (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))

        super().move(target)

class CenterPlayer(Player):
    def __init__(self, team_name, team, player_id, position, grid, ball, zone):
        super().__init__(team_name, team, player_id, position, grid, ball)
        self.zone = zone
    def move(self, ball, opposing_team):
        target = self.get_target_position(ball)
        if self.team.mode == 'defensive':
            target = self.get_target_position(ball)
        else:
            target = (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))
        super().move(target)

class DefencePlayer(Player):
    def __init__(self, team_name, team, player_id, position, grid, ball, zone):
        super().__init__(team_name, team, player_id, position, grid, ball)
        self.zone = zone
    
    def move(self, ball, opposing_team):
        target = self.get_target_position(ball)
        if self.team.mode == 'defensive':
            target = self.get_target_position(ball)
        else:
            target = (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height))

        super().move(target)

class Team:
    def __init__(self, name, grid, formation, ball, opposing_team=None, opposing_goals=None):
        self.name = name
        self.opposing_team = opposing_team
        self.opposing_goals = opposing_goals
        self.players = []
        for i, pos in enumerate(formation):
            if i >= 0 and i <= 3:
                if self.name == 'Team A':
                    self.players.append(DefencePlayer(name, self, i, pos, grid, ball, [5.0, 35.0]))
                else:
                    self.players.append(DefencePlayer(name, self, i, pos, grid, ball, [65.0, 95.0]))
            if i >= 4 and i <= 7:
                if self.name == 'Team A':
                    self.players.append(CenterPlayer(name, self, i, pos, grid, ball, [35.0, 65.0]))
                else:
                    self.players.append(CenterPlayer(name, self, i, pos, grid, ball, [35.0, 65.0]))
            if i >= 8 and i <= 9:
                if self.name == 'Team A':
                    self.players.append(OffencePlayer(name, self, i, pos, grid, ball, [65.0, 95.0]))
                else:
                    self.players.append(OffencePlayer(name, self, i, pos, grid, ball, [5.0, 35.0]))
            if i == 10:
                if self.name == 'Team A':
                    self.players.append(GoalKeeper(name, self, i, pos, grid, ball, [[0.0, 5.0], [45.0, 55.0]]))
                else:
                    self.players.append(GoalKeeper(name, self, i, pos, grid, ball, [[95.0, 100.0], [45.0, 55.0]]))

    def move(self, grid, ball):
        for player in self.players:
            if np.linalg.norm(np.array(player.current_position) - np.array(ball.current_position)) <= 0.15:  
                player.has_ball_control = True
                ball.current_position = player.current_position
            for opponent in self.opposing_team.players:
                if np.linalg.norm(np.array(player.current_position) - np.array(opponent.current_position)) < 0.05 and player.has_ball_control:
                    if random.random() < 0.75:
                        player.has_ball_control = True
                        opponent.has_ball_control = False
                    else:
                        player.has_ball_control = False
                        opponent.has_ball_control = True
                    if player.has_ball_control:
                        target = (self.opposing_goals[0], np.random.randint(self.opposing_goals[1][0],self.opposing_goals[1][1]))
                        super(type(player), player).move(target)
                        ball.move(target)
                        self.mode = 'offensive'
                    else:
                        target = (self.opposing_team.opposing_goals[0], np.random.randint(self.opposing_team.opposing_goals[1][0], \
                                self.opposing_team.opposing_goals[1][1]))
                        super(type(opponent), opponent).move(target)
                        ball.move(target)
                        self.mode = 'defensive'
            player.move(ball.current_position, self.opposing_team)

    def update_mode(self):
        if any(player.has_ball_control for player in self.players):
            self.mode = 'offensive'
        elif any(player.has_ball_control for player in self.opposing_team.players):
            self.mode = 'defensive'
        else:
            self.mode = 'neutral'

class SoccerMatch:
    def __init__(self, grid, team1, formation1, team2, formation2):
        self.grid = grid
        self.ball = Ball(([50, 50]), self.grid)
        self.team1, self.team2 = Team(team1, self.grid, formation1, self.ball), Team(team2, self.grid, formation2, self.ball)
        self.team1.opposing_team, self.team2.opposing_team = self.team2, self.team1
        self.team1.opposing_goals, self.team2.opposing_goals = [100, [45, 55]], [0, [45, 55]] #переписать по-человечески
        self.team1.hit_area, self.team2.hit_area = [[75, 95], [35, 65]], [[25, 5], [35, 65]] #переписать по-человечески

    def simulate(self):
        data = []
        for i in range(framerate * sim_length_sec):
            self.team1.update_mode()
            if self.team1.mode == 'offensive':
                self.team2.mode = 'defensive'
            elif self.team1.mode == 'defensive':
                self.team2.mode = 'offensive'
            else:
                self.team2.mode = 'neutral'
            self.team1.move(self.grid, self.ball)
            self.team2.move(self.grid, self.ball)
            for team in [self.team1, self.team2]:
                for player in team.players:
                    data.append([1, i, i * 0.04, team.name, player.player_id, *player.current_position, *self.ball.current_position])
        df = pd.DataFrame(data, columns=['Period', 'Frame', 'Time [s]', 'Team', 'Player', 'X', 'Y', 'Ball_x', 'Ball_y'])
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
