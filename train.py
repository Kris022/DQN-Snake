from collections import deque
import random
import numpy as np
import time
import pickle

from snakeEnvironment import SnakeEnvironment
from dqn import DQNAgent

# Initilise environment
env = SnakeEnvironment()

number_of_episodes = 400
number_of_timesteps = 500
batch_size = 64

dqn_agent = DQNAgent(load_model=False)

rewards, epsilon_values = list(), list() # Lists to keep logs of rewards and apsilon values, for plotting later

for episode in range(number_of_episodes):

    episode_reward = 0

    state = env.reset() # Reset the environment and get initial state

    start = time.time()

    for timestep in range(number_of_timesteps):
        env.render()

        dqn_agent.check_for_target_network_update(timestep+1)

        action = dqn_agent.choose_action(state) # Select action with epsilon policy

        next_state, reward, terminal = env.step(action) # Perform action on environment

        dqn_agent.replay_buffer.save(state, action, reward, next_state, terminal)

        state = next_state
        episode_reward += reward

        if terminal:
            print('Episode: ', episode+1, 'Reward: ', episode_reward)
            rewards.append(episode_reward)
            print(rewards)
            break
        
        # Train once enough experiences sampled
        if len(dqn_agent.replay_buffer.buffer) > batch_size:
            dqn_agent.train(batch_size)

    # Decrement epsilon
    dqn_agent.decay_epsilon()
    
    # Save the model
    dqn_agent.check_point_model(episode)
    
    if episode % 10 == 0:
        with open('rewards.pkl', 'wb') as file:
            pickle.dump(episode_reward, file)

print(rewards)
    