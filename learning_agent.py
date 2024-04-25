import numpy as np
import random

class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.99):
        self.env = env
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = {}

    def choose_action(self, state):
        if random.random() < self.exploration_rate:
            # Exploration: Choose a random action
            return random.randint(0, len(self.env.state) - 1)
        else:
            # Exploitation: Choose action with highest Q-value
            state_str = str(state)
            if state_str not in self.q_table:
                # Initialize Q-values for the state if not present
                self.q_table[state_str] = [0] * len(self.env.state)
            return np.argmax(self.q_table[state_str])

    def update_q_value(self, state, action, reward, next_state):
        state_str = str(state)
        next_state_str = str(next_state)
        if state_str not in self.q_table:
            self.q_table[state_str] = [0] * len(self.env.state)
        if next_state_str not in self.q_table:
            self.q_table[next_state_str] = [0] * len(self.env.state)

        # Q-learning update rule
        self.q_table[state_str][action] += self.learning_rate * \
                                           (reward + self.discount_factor * max(self.q_table[next_state_str]) - \
                                            self.q_table[state_str][action])

    def train(self, episodes=100):
        for episode in range(episodes):
            state = self.env.state_im
            done = False
            episode_reward = 0

            while not done:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.update_q_value(state, action, reward, next_state)
                state = next_state
                episode_reward += reward

            print(f"Epsiode {episode}: Total Reward = {float(episode_reward)}")

            # Decay exploration rate
            self.exploration_rate *= self.exploration_decay

            # Reset environment for next episode
            self.env.reset()
            

