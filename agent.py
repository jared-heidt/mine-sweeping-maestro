import numpy as np
from minesweeperenv import MinesweeperEnv
import qlearning

DISCOUNT = 0.1 #gamma

class Agent:
    def __init__(self, 
                 state_size, 
                 action_size, 
                 environment=MinesweeperEnv(width=10, height=10, n_mines=10),
                 learning_rate=qlearning.LEARNING_RATE, 
                 discount_factor=qlearning.DISCOUNT_FACTOR, 
                 exploration_rate=qlearning.EXPLORATION_RATE, 
                 exploration_decay=qlearning.EXPLORATION_DECAY):
        self.state_size = state_size
        self.action_size = action_size
        self.environment = environment
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

    # TODO Implement train to train the QLearning Agent
    def train(self, episodes):
        for episode in range(episodes):
        # Reset environment
            self.environment.reset()
            state = self.environment.state
            done = False
            total_reward = 0
        
            while not done:
                # Choose action
                action = self.choose_action(state)
                
                # Take action
                next_state, reward, done = self.environment.step(action)
                
                # Update Q-values
                self.update_q_table(state, action, reward, next_state)
                
                # Update total reward
                total_reward += reward
                
                # Decay exploration rate
                self.decay_exploration_rate()
                
                # Update state for next iteration
                state = next_state
            
            # Print total reward for the episode
            print(f"Episode {episode + 1}, Total Reward: {total_reward}")