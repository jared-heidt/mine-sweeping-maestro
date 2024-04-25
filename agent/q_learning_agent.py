import numpy as np

from minesweeper.minesweeper import GameAI

class QLearningAgent(GameAI):
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = np.zeros((state_size, action_size))

    def select_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return np.random.choice(self.action_size)  # Explore
        else:
            state = tuple(state)
            return np.argmax(self.q_table[state])  # Exploit

    def update_q_table(self, state, action, reward, next_state):
        state = tuple(state)
        next_state = tuple(next_state)
        
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error