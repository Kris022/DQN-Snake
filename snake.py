import pygame
from settings import *
import random
import numpy as np


class Snake:
    def __init__(self):
        self.size = BLOCK_SIZE

        self.color = (82, 235, 0)
        
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

        self.segments = [
            {"x": 5, "y": 8},
            {"x": 6, "y": 8},
            {"x": 7, "y": 8},
            {"x": 8, "y": 8},
            ]
        
        self.obstacles = []

        for i in range(0, MAX_LENGTH):
            self.obstacles.append({"x": i, "y": 0})

        for i in range(0, MAX_LENGTH):
            self.obstacles.append({"x": i, "y": MAX_LENGTH-1})

        for i in range(1, MAX_LENGTH-1):
            self.obstacles.append({"x": 0, "y": i})
        
        for i in range(1, MAX_LENGTH-1):
            self.obstacles.append({"x": MAX_LENGTH-1, "y": i})

        self.dir = {"x": 1, "y":0}
        self.dirqueue = []

        self.t = 0
        self.speed = 1000

        self.food_position = [self.place_food()]

        self.food_color = (245, 24, 24)
        self.obstacle_color = (240, 240, 240)

        self.alive = True
        self.ate_food = False

        self.num_of_foods = 3

    def place_food(self):
        while True:
            size = (WIDTH)//BLOCK_SIZE

            food_pos =  {"x": random.randint(self.obstacles[0]["x"]+1, self.obstacles[-1]["x"]-1), 
                              "y": random.randint(self.obstacles[0]["y"]+1, self.obstacles[-1]["y"]-1)} 
            
            if food_pos not in self.segments:
                break
        
        return food_pos
    
    def move(self, action):
        # Up
        if action == 0:
            dir = {"x": 0, "y":-1}
        # Down
        if action == 1:
            dir = {"x": 0, "y":1}
        # Left
        if action == 2:
            dir = {"x": -1, "y":0}
        # Right
        if action == 3:
            dir = {"x": 1, "y":0}   

        self.dirqueue.append(dir)     

    def update(self, dt):
        self.ate_food = False
        self.t = self.t + dt
        if self.t >= 1.0 / self.speed:
            if len(self.dirqueue) != 0:
                newdir = self.dirqueue.pop(0)
                opposite = newdir["x"] == -self.dir["x"] or newdir["y"] == -self.dir["y"] # Check if snake is trying to move into itself
                # if not opposite change direction, otherwise keep moving in the same direction
                if not opposite:
                    self.dir = newdir

            head = self.segments[-1]
            new_head = {"x": head["x"] + self.dir["x"], "y": head["y"] + self.dir["y"]}

            if self.is_dict_in_list(new_head, self.segments) or self.is_dict_in_list(new_head, self.obstacles) or self.is_out_of_bounds(new_head):
                self.alive = False

            # Check if snake ate food

            for f in range(0, len(self.food_position)):
                food = self.food_position[f]
                if new_head["x"] == food["x"] and new_head["y"] == food["y"]:
                    self.ate_food = True
                    print("ate food")

                    self.food_position.pop(f)

                    if len(self.food_position) <= 0:
                        for i in range(self.num_of_foods - len(self.food_position)):
                            self.food_position.append(self.place_food())

                    break # Can only eat one food at a time, therefore no need to check for other food
                
            if not self.ate_food:
                self.segments.pop(0)
                    

            self.segments.append(new_head)
                
            self.t = 0
            
    def draw(self, screen):
        
        obstacle_position = self.get_obstacles_as_list()
        for obs in obstacle_position:
                pygame.draw.rect(screen, (237, 237, 237), 
                             [obs[0]*BLOCK_SIZE, obs[1]*BLOCK_SIZE, 
                              self.size, self.size])

        for food in self.food_position:
            pygame.draw.rect(screen, self.food_color, 
                             [food["x"]*BLOCK_SIZE, food["y"]*BLOCK_SIZE, 
                              self.size, self.size])
        
        for segment in self.segments:
            pygame.draw.rect(screen, self.color, 
                             [segment["x"]*BLOCK_SIZE, segment["y"]*BLOCK_SIZE, self.size, self.size], 3)
        
        
            

    def is_dict_in_list(self, d, lst):
        for item in lst:
            if item == d:
                return True
        return False
    
    def reset(self):
        self.segments = [
            {"x": 7, "y": 8},
            {"x": 8, "y": 8},
            {"x": 9, "y": 8},
            {"x": 10, "y": 8},
            ]
        
        self.dir = {"x": 1, "y":0}
        self.dirqueue = []

        self.t = 0

        self.food_position = []
        
        for i in range(self.num_of_foods):
            self.food_position.append(self.place_food())
        
        self.food_color = (245, 24, 24)

        self.alive = True
        self.ate_food = False
    
    def is_out_of_bounds(self, head):
        if head["x"] >= WIDTH // BLOCK_SIZE or head["x"] < 0:
            self.alive = False
        elif head["y"] >= HEIGHT // BLOCK_SIZE or head["y"] < 0:
            self.alive = False
    
    def get_food_position(self):
        food_list = []

        for food in self.food_position:
            food_list.append([food["x"], food["y"]])

        return food_list
    
    def get_direction(self):
        return [self.dir["x"], self.dir["y"]]
    
    def get_head_position(self):
        head = self.segments[-1]
        return [head["x"], head["y"]]

    def get_body_segments_as_list(self):
        segments_list = []
        
        for segment in self.segments:
            segments_list.append([segment["x"], segment["y"]])
        
        return segments_list # return without the last segment as head is its own element
    
    def get_obstacles_as_list(self):
        segments_list = []
        
        for segment in self.obstacles:
            segments_list.append([segment["x"], segment["y"]])
        
        return segments_list # return without the last segment as head is its own element
    

    def get_map(self):
        # Consider making obstacle for circulum learning approach and ease of decreasing the play area
        body_position = self.get_body_segments_as_list()
        obstacle_position = self.get_obstacles_as_list()
        food_position = self.get_food_position()

        map = np.zeros((20, 20))

        
       # map[head_position[1]][head_position[0]] = 2

        for food in food_position:
            map[food[1], food[0]] = 2

        for segment in body_position:
            try:
                map[segment[1], segment[0]] = 1
            except:
                #print(f"Head segment out of bounds row: {segment[1]} col: {segment[0]}")
                continue
        
        for obstacle in obstacle_position:
            map[obstacle[1], obstacle[0]] = 1

        return map
    
    def draw_grid(self, screen):
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, (255,255,255), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, (255,255,255), (0, y), (WIDTH, y))