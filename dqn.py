import random
import numpy as np

from replayBuffer import ReplayBuffer

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

class DQNAgent:
    def __init__(self,
                 alpha=0.001, gamma=0.99, 
                 epsilon=1., epsilon_decay=0.98,
                 epsilon_minimum=0.01, target_network_update_rate=10,
                 model_path="snake_agent", model_checkpoint_rate = 10,
                 load_model=False
                 ):

        # Replay buffer
        self.replay_buffer = ReplayBuffer()

        # Hyperparameters
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor

        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_minimum = epsilon_minimum

        # Neural Networks
        if load_model: self.policy_network = tf.keras.models.load_model(model_path)
        else: self.policy_network = self.create_network()

        self.target_network = self.create_network()
        self.update_target_network()

        self.target_network_update_rate = target_network_update_rate    # How often the target network is updated (in time steps)

        # Model saving
        self.model_path = model_path    # Where the model is to be saved/loaded from
        self.model_checkpoint_rate = model_checkpoint_rate  # How often the model is saved (in episodes)

        
    def create_network(self):
        model = Sequential()

        model.add(Dense(64, activation='relu', input_dim=4))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(4, activation='linear'))

        model.compile(loss='mse', optimizer=Adam(learning_rate=self.alpha))

        return model
    
    def update_target_network(self):
        # Sets target network weights to the policy network weights
        self.target_network.set_weights(self.policy_network.get_weights())
    
    def check_for_target_network_update(self, timestep):
        # Checks if enough time steps passed to update the target network
        if timestep % self.target_network_update_rate == 0:
            self.update_target_network()
    
    def choose_action(self, state):
        # Epsilon greedy policy for choosing the action
        if random.uniform(0, 1) < self.epsilon:
            return np.random.randint(4)

        state = state.reshape((1, 4)) # Reshape the state to be input into the network
        q_values = self.policy_network.predict(state, verbose=0)
        return np.argmax(q_values[0])
    
    def train(self, batch_size):
        # Sample replay buffer
        state_batch, action_batch, reward_batch, next_state_batch, terminal_batch = self.replay_buffer.sample(batch_size)

        # Compute Q-values and targets
        q_values = self.policy_network.predict(state_batch, verbose=0)
        target_q_values = self.target_network.predict(next_state_batch, verbose=0)

        for i in range(batch_size):
            # If terminal state set to immidate reward
            if terminal_batch[i]:
                q_values[i][action_batch[i]] = reward_batch[i] 
            else:
                q_values[i][action_batch[i]] = reward_batch[i] + self.gamma * np.max(target_q_values[i])

        # Train the policy network with update Q-values
        self.policy_network.fit(state_batch, q_values, verbose=0)
    
    def decay_epsilon(self):
        if self.epsilon > self.epsilon_minimum:
            self.epsilon *= self.epsilon_decay
    
    def save_model(self):
        # Saves the policy network
        tf.keras.models.save_model(self.policy_network,  self.model_path)
    
    def check_point_model(self, episode):
        # Check if enough episodes passed to checkpoint the model
        if episode % self.model_checkpoint_rate == 0:
            self.save_model()
            print("model saved")

