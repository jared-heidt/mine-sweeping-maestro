class Maestro:
    def __init__(self, environemnt, learning_agent):
        self.environment = environemnt
        self.learning_agent = learning_agent
        
    def train(self, episodes):
        
        for episode in range(episodes):
            self.environment.reset()
            state = self.environment.state
            
            done = False

            while not done:
                action = self.learning_agent.choose_action(state)
                next_state, reward, done = self.environment.step(action)

                 # Find the index of the current state using the coordinate pair
                state_index = self.environment.find_state_index(next_state)


                self.learning_agent.update_q_table(state, action, reward, state_index)
                state = next_state
            
            print('Episode ' + str(episode) + ' completed.')

            # TODO print output with each episode? find use for this
            self.learning_agent.decay_exploration_rate()