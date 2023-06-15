import random
import numpy as np

from collections import deque

class ReplayBuffer:
    def __init__(self, max_size=100_000):
        self.max_size = max_size
        self.buffer = deque(maxlen=max_size)

    def save(self, state, action, reward, next_state, done):
        experience = (state, action, reward, next_state, done)
        self.buffer.append(experience)

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = np.array(states).reshape(batch_size, 4)
        next_states = np.array(next_states).reshape(batch_size, 4)

        return states, actions, rewards, next_states, dones
