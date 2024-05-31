import pandas as pd
import numpy as np
import yaml
import math
import random
from scipy.stats import truncnorm 
from typing import Tuple, List
import time

with open("simulation_config.yaml", "r") as config_file:
    sim_config = yaml.safe_load(config_file)

grid_height = sim_config["height"]
grid_width = sim_config["width"]
sim_length_sec = sim_config["simulation_length_seconds"]
framerate = sim_config["framerate"]

class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

class Entity:
    def __init__(self, position, grid):
        self.current_position = position
        self.grid = grid
        self.speed = self.generate_speed() 

    def get_truncated_normal(self, mean=0, sd=1, low=0, upp=10):
        return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

    def generate_speed(self):
        speed_distribution = self.get_truncated_normal(mean=0.08, sd=0.03, low=0, upp=1)
        speed = speed_distribution.rvs()
        return speed

    def move(self, target):
        dx = target[0] - self.current_position[0]
        dy = target[1] - self.current_position[1]

        angle_rad = math.atan2(dy, dx)

        angle_deg = math.degrees(angle_rad)

        angle_deg = angle_deg % 360

        dx = self.speed * math.cos(angle_rad)
        dy = self.speed * math.sin(angle_rad)

        x = self.current_position[0] + dx
        y = self.current_position[1] + dy

        self.current_position = (max(0, min(x, self.grid.width)), max(0, min(y, self.grid.height)))

    def move_opposite(self, target):
        dx = target[0] - self.current_position[0]
        dy = target[1] - self.current_position[1]

        angle_rad = math.atan2(dy, dx)

        angle_deg = math.degrees(angle_rad)

        angle_deg = angle_deg % 360

        dx = self.speed * math.cos(angle_rad)
        dy = self.speed * math.sin(angle_rad)

        x = self.current_position[0] - dx
        y = self.current_position[1] - dy

        self.current_position = (max(0, min(x, self.grid.width)), max(0, min(y, self.grid.height)))


class Ball(Entity):
    def __init__(self, position, grid):
        super().__init__(position, grid)
        self.controlled_by = None
        self.speed = self.generate_speed() * 4
        self.target = None

class Player(Entity):
    def __init__(self, team_name, team, player_id, position, grid, ball):
        super().__init__(position, grid)
        self.team = team
        self.team_name = team_name
        self.player_id = player_id
        self.has_ball_control = False
        self.ball = ball

    def move(self, target):
        if self.current_position == self.ball.target and self.ball.controlled_by == None and self.player_id != 10:
            self.speed = self.speed*1.1
            super().move(self.ball.current_position)

        else:
            if self.has_ball_control:
                self.speed = self.generate_speed()*1.1
                if self.current_position[0] >= self.team.hit_area[0][0] and self.current_position[0] <= self.team.hit_area[0][1] \
                and self.current_position[1] >= self.team.hit_area[1][0] and self.current_position[1] <= self.team.hit_area[1][1]:
                    self.hit_ball(self.ball, (self.team.opposing_goals[0], np.random.randint(self.team.opposing_goals[1][0],\
                            self.team.opposing_goals[1][1])))
                    target = self.get_closest_opposing_player()
                    super().move(target) 
                else:
                    dist_player_opp = np.linalg.norm(np.array(self.current_position) - np.array(self.get_closest_opposing_player()))
                    pass_target = self.find_open_teammate()
                    if dist_player_opp > 3:
                        target = ((self.team.hit_area[0][1] - self.team.hit_area[0][0])/2 + self.team.hit_area[0][0],\
                                    (self.team.hit_area[1][1] - self.team.hit_area[1][0])/2+self.team.hit_area[1][0])
                        super().move(target)
                    else:
                        if pass_target != -1: 
                            self.hit_ball(self.ball, pass_target.current_position)
                        else: 
                            target = self.get_closest_opposing_player()
                            super().move_opposite(target)
            else:
                self.speed = self.generate_speed()
                super().move(target)
        
    def hit_ball(self, ball, target):
        ball.controlled_by = None
        ball.target = target
        ball.move(ball.target)
        self.has_ball_control = False

    def find_open_teammate(self):
        open_teammates = [player for player in self.team.players\
                if self.opponent_between_target(player.current_position, self.team.opposing_team) == False and player != self]
        if not open_teammates:
            return -1
        return min(open_teammates, key=lambda player: (player.dist_to_opposing_goals(), \
                np.linalg.norm(np.array(self.current_position) - np.array(player.current_position))))

    def find_closeset_open_teammate(self):
        open_teammates = [player for player in self.team.players\
                if self.opponent_between_target(player.current_position, self.team.opposing_team) == False and player != self]
        if not open_teammates:
            return -1
        return max(open_teammates, key=lambda player: (player.dist_to_opposing_goals(), \
                np.linalg.norm(np.array(self.current_position) - np.array(player.current_position))))

    def get_closest_opposing_player(self):
        return self.team.opposing_team.players[np.argmin([np.linalg.norm(np.array(self.current_position) - np.array(pos)) \
            for pos in [player.current_position for player in self.team.opposing_team.players]])].current_position

    def is_ball_in_zone(self):
        return self.zone[0] <= float(self.ball.current_position[0]) <= self.zone[1]

    def is_closest_to_ball(self):
        return self == self.team.players[np.argmin([np.linalg.norm(np.array(player.current_position) - np.array(self.ball.current_position)) \
                for player in self.team.players])]

    def dist_to_opposing_goals(self): 
        return np.linalg.norm(np.array(self.current_position) - np.array([float(self.team.opposing_goals[0]), \
                float(self.team.opposing_goals[1][1])- float(self.team.opposing_goals[1][0]) + float(self.team.opposing_goals[1][0])]))

    def opponent_between_target(self, target, opposing_team):
        for opp_player in opposing_team.players:
            dist_player_target = np.linalg.norm(np.array(self.current_position) - np.array(target))
            dist_player_opponent = np.linalg.norm(np.array(self.current_position) - np.array(opp_player.current_position))
            dist_opponent_target = np.linalg.norm(np.array(opp_player.current_position) - np.array(target))
            if dist_player_target != 0:
                if random.random() < 0.25 or dist_opponent_target < 2.15 or dist_player_target < 2.5:
                    return True
            else: 
                return True
        return False
        
    def get_midpoint(self):
        player_with_ball = self.ball.controlled_by
        if player_with_ball is None:
            midpoint_x = (self.ball.current_position[0] + self.get_closest_opposing_player()[0]) / 2
            midpoint_y = (self.ball.current_position[1] + self.get_closest_opposing_player()[1]) / 2
            return (midpoint_x, midpoint_y)
        else:
            midpoint_x = (player_with_ball.current_position[0] + self.get_closest_opposing_player()[0]) / 2
            midpoint_y = (player_with_ball.current_position[1] + self.get_closest_opposing_player()[1]) / 2
            return (midpoint_x, midpoint_y)

class GoalKeeper(Player):  
    def __init__(self, team_name, team, player_id, position, grid, ball, zone):
        super().__init__(team_name, team, player_id, position, grid, ball)
        self.zone = zone

    def move(self, ball, opposing_team):
        if self.has_ball_control:
            target = (np.random.randint(self.zone[0][0], self.zone[0][1]), np.random.randint(self.zone[1][0], self.zone[1][1]))
            pass_to = self.find_closeset_open_teammate()
            if pass_to != -1:
                self.hit_ball(ball, pass_to.current_position)
            else:
                self.hit_ball(ball, [50, 50])
        else:
            if self.team.name == 'Team A':
                target = (min(ball.current_position[0], self.zone[0][1]), min(max(ball.current_position[1], 45), 55)) 
            else:
                target = (max(ball.current_position[0], self.zone[0][0]), min(max(ball.current_position[1], 45), 55))
        super(Player, self).move(target)

class OffencePlayer(Player):
    def __init__(self, team_name, team, player_id, position, grid, ball, zone):
        super().__init__(team_name, team, player_id, position, grid, ball)
        self.zone = zone
        self.default_pos = position

    def move(self, ball, opposing_team):
        if self.is_ball_in_zone():
            if self.team.mode == 'defensive':
                if self.is_closest_to_ball():
                    target = ball.current_position
                else:
                    target = self.get_midpoint()
            elif self.team.mode == 'neutral':
                target = ball.current_position
            else:
                target = (np.random.randint(self.team.hit_area[0][0], self.team.hit_area[0][1]), \
                        np.random.randint(self.team.hit_area[1][0], self.team.hit_area[1][1]))
        else:
            if self.team.mode == 'offensive' or self.team.mode == 'neutral':
                target = (np.random.randint(self.team.hit_area[0][0], self.team.hit_area[0][1]), \
                        np.random.randint(self.team.hit_area[1][0], self.team.hit_area[1][1]))
            else:
                target = self.default_pos
        super().move(target) 

class CenterPlayer(Player):
    def __init__(self, team_name, team, player_id, position, grid, ball, zone):
        super().__init__(team_name, team, player_id, position, grid, ball)
        self.zone = zone
        self.default_pos = position
    
    def move(self, ball, opposing_team):
        if self.is_ball_in_zone():
            if self.team.mode == 'defensive':
                target = self.get_midpoint()
            elif self.team.mode == 'neutral':
                target = ball.current_position
            else:
                target = (np.random.randint(self.zone[0], self.zone[1]), np.random.randint(0, self.grid.height)) 
        else:
            if self.team.mode == 'defensive':
                target = self.get_midpoint()
            elif self.team.mode == 'neutral':
                if self.is_closest_to_ball():
                    target = ball.current_position
                else:
                    target = self.get_midpoint()
            else:
                target = self.default_pos
        super().move(target)

class DefencePlayer(Player):
    def __init__(self, team_name, team, player_id, position, grid, ball, zone):
        super().__init__(team_name, team, player_id, position, grid, ball)
        self.zone = zone
        self.default_pos = position
    
    def move(self, ball, opposing_team):
        if self.is_ball_in_zone():
            if self.team.mode == 'defensive':
                if self.is_closest_to_ball():
                    target = ball.current_position
                else:
                    target = self.get_midpoint()
            else:
                target = ball.current_position
        else:
            if self.team.mode == 'neutral':
                if self.is_closest_to_ball():
                    target = ball.current_position
                else:
                    target = self.default_pos
            elif self.team.mode == 'defensive':
                target = self.get_midpoint()
            else:
                target = self.default_pos     
        super().move(target)

class Team:
    def __init__(self, name, grid, formation, ball, opposing_team=None, opposing_goals=None):
        self.name = name
        self.mode = 'neutral'
        self.opposing_team = opposing_team
        self.opposing_goals = opposing_goals
        self.hit_area = None
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
            player.move(ball, self.opposing_team)
            if ball.controlled_by == player:
                ball.current_postion = player.current_position

    def update_mode(self, ball):
        for player in self.players:
            if np.linalg.norm(np.array(player.current_position) - np.array(ball.current_position)) < 0.3:
                player.has_ball_control = True
                ball.controlled_by = player
                ball.target = None
                ball.current_position = player.current_position
            else:
                player.has_ball_control = False
                
        for opp_player in self.opposing_team.players:
            if np.linalg.norm(np.array(opp_player.current_position) - np.array(ball.current_position)) < 0.3:
                opp_player.has_ball_control = True
                ball.controlled_by = opp_player
                ball.target = None
                ball.current_position = opp_player.current_position
            else:
                opp_player.has_ball_control = False
                
        if any(player.has_ball_control for player in self.players):
            self.mode = 'offensive'
        elif any(opp_player.has_ball_control for opp_player in self.opposing_team.players):
            self.mode = 'defensive'
        else:
            self.mode = 'neutral'

class SoccerMatch:
    def __init__(self, grid, team1, formation1, team2, formation2):
        self.grid = grid
        self.ball = Ball(([50.0, 50.0]), self.grid)
        self.team1, self.team2 = Team(team1, self.grid, formation1, self.ball), Team(team2, self.grid, formation2, self.ball)
        self.team1.opposing_team, self.team2.opposing_team = self.team2, self.team1
        self.team1.opposing_goals, self.team2.opposing_goals = [100, [45, 55]], [0, [45, 55]] 
        self.team1.hit_area, self.team2.hit_area = [[75, 95], [35, 65]], [[5, 25], [35, 65]] 

    def simulate(self):
        data = []
        for i in range(framerate * sim_length_sec):
            self.team1.update_mode(self.ball)
            self.team1.move(self.grid, self.ball)
            self.team2.update_mode(self.ball)
            self.team2.move(self.grid, self.ball)
            if self.ball.controlled_by == None and self.ball.target != None:
                self.ball.move(self.ball.target)
            for team in [self.team1, self.team2]:
                for player in team.players:
                    data.append([1, i, i * 0.04, team.name, player.player_id, *player.current_position, *self.ball.current_position])
        df = pd.DataFrame(data, columns=['Period', 'Frame', 'Time [s]', 'Team', 'Player', 'X', 'Y', 'Ball_x', 'Ball_y'])
        return df


class SoccerSimulation:
    def __init__(self, df):
        self.df = df

    def get_positions(self, tick: int) -> np.ndarray:
        positions = []
        tick_data = self.df[self.df['Frame'] == tick]

        for _, row in tick_data.iterrows():
            positions.append([row['X'], row['Y']])

        return np.array(positions)


df_formations = pd.read_csv('formation442.csv', header=None, names=['area_x', 'area_y', 'x', 'y'], sep=',')
df_team_A = df_formations.iloc[:11]
df_team_B = df_formations.iloc[11:]
formation1 = list(df_team_A[['x', 'y']].itertuples(index=False, name=None))
formation2 = list(df_team_B[['x', 'y']].itertuples(index=False, name=None))
field = Grid(grid_width, grid_height)
match = SoccerMatch(field, 'Team A', formation1, 'Team B', formation2)
start = time.time()
df = match.simulate()
df.to_csv('soccer_sim.csv', index=False)
end = time.time()

print(f"Time taken to simulate: {(end - start):.2f} seconds")

soccer_sim = SoccerSimulation(df)
