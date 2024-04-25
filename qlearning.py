import numpy as np

LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EXPLORATION_RATE = 1.0
EXPLORATION_DECAY = 0.995

class QLearningAgent:
    def __init__(self, 
                 state_size, 
                 action_size, 
                 learning_rate=LEARNING_RATE, 
                 discount_factor=DISCOUNT_FACTOR, 
                 exploration_rate=EXPLORATION_RATE, 
                 exploration_decay=EXPLORATION_DECAY):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = np.zeros((state_size, state_size, action_size))

    def choose_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return np.random.choice(self.action_size), state
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        #print('State: ' + str(state) + '\n')
        print('Next State: ' + str(next_state) + '\n')
    
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

    def decay_exploration_rate(self):
        self.exploration_rate *= self.exploration_decay