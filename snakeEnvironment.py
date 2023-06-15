import pygame
from settings import *
import random
from snake import Snake
import numpy as np

class SnakeEnvironment:
    def __init__(self):
        self.snake = Snake()

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake")

        self.clock = pygame.time.Clock()
        
        # ["UP", "DOWN", "LEFT", "RIGHT"]
        #   0,      1,      2,      3

        self.action_space = [0, 1, 2, 3]
        #self.observation_space = [[], [], [], []]
        self.observation_size = 4# 8
        self.action_size = len(self.action_space)
    
    def get_old_state(self):
        # Get the snake state values
        head_pos = self.snake.get_head_position()
        direction = self.snake.get_direction()
        game_map = self.snake.get_map()
        
        game_map = game_map.flatten()      

        state = np.concatenate((game_map, head_pos, direction), axis=0)
        # state = [snake head pos], [snake bod pos], [direction], [food pos]

         # Check if food on the left
        if head_col - 1 == food_col and food_row == head_row:
            left = 3

        if head_col + 1 == food_col and food_row == head_row:
            right = 3

        if head_col == food_col and food_row == head_row - 1:
            above = 3

        if head_col == food_col and food_row == head_row + 1:
            below = 3

        # Check if off screen on the left

        # Check if obstacle on the left
        if head_col - 1 == food_col and food_row == head_row:
            left = 3

        if head_col + 1 == food_col and food_row == head_row:
            right = 3

        if head_col == food_col and food_row == head_row - 1:
            above = 3

        if head_col == food_col and food_row == head_row + 1:
            below = 3


        return state
    
    def get_state(self):
        #state: left, right, above, below
        map = self.snake.get_map()

        left, right, above, below = 0, 0, 0, 0

        head_pos = self.snake.get_head_position()
        head_col= head_pos[0]
        head_row = head_pos[1]

        left = map[head_row][head_col-1]
        right = map[head_row][head_col+1]
        above = map[head_row-1][head_col]
        below = map[head_row+1][head_col]
        
        return np.array([left, right, above, below])
    
    def get_new_state(self):
        # front distance to apple, front dist to obstacle
        map = self.snake.get_map()

        head_pos = self.snake.get_head_position()
        head_col= head_pos[0]
        head_row = head_pos[1]

        left_distance_obstacle = 1000
        left_distance_food = 1000
        right_distance_obstacle = 1000
        right_distance_food = 1000
        above_distance_obstacle = 1000
        above_distance_food = 1000
        below_distance_obstacle = 1000
        below_distance_food = 1000

        # Distance left
        for i in range(0, len(map[0])):
            if map[head_row][head_col - i] == 1:
                left_distance_obstacle = i
                left_distance_food = 1000
                break
            elif map[head_row][head_col - i] == 3:
                left_distance_obstacle = 1000
                left_distance_food = i
                break
        
        # Distance right
        for j in range(0, len(map[0])):
            if map[head_row][head_col + j] == 1:
                right_distance_obstacle = j
                right_distance_food = 1000
                break
            elif map[head_row][head_col + j] == 3:
                right_distance_obstacle = 1000
                right_distance_food = j
                break
        
        # Distance above
        for k in range(0, len(map)):
            if map[head_row - k][head_col] == 1:
                above_distance_obstacle = k
                above_distance_food = 1000
                break
            elif map[head_row - k][head_col] == 3:
                above_distance_obstacle = 1000
                above_distance_food = k
                break

        # Distance below
        for x in range(0, len(map)):
            if map[head_row + x][head_col] == 1:
                below_distance_obstacle = x
                below_distance_food = 1000
                break
            elif map[head_row + x][head_col] == 3:
                below_distance_obstacle = 1000
                below_distance_food = x
                break
            

        s = np.array([
            left_distance_obstacle, left_distance_food, 
            right_distance_obstacle, right_distance_food,
            above_distance_obstacle, above_distance_food,
            below_distance_obstacle, below_distance_food
        ])
        return s 

    
    def reset(self):
        self.snake.reset()
        state = self.get_state() 

        return state
    
    def get_sample_action(self):
        return random.choice(self.action_space)
    
    def step(self, action):
        state = []
        reward = 0
        done = False

        dt = self.clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds

        self.snake.move(action) # Take action
        self.snake.update(dt)   # Update the game by one step

        if not self.snake.alive:
            reward = -10
            done = True

        elif self.snake.ate_food:
            reward += 1
            self.snake.ate_food = False

        state = self.get_state() 

        return state, reward, done
    
    def render(self):
        self.screen.fill((0, 0, 0))    # black background
        self.snake.draw(self.screen)

        pygame.display.update() # update display changes


