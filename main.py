import numpy as np
from agent.q_learning_agent import QLearningAgent
from minesweeper.minesweeper import Game
from minesweeper.minesweeper import GameConfig

def main():
    # Initialize Q-learning agent
    agent = QLearningAgent(10 * 10, 2)

    num_episodes = 10
    episodes_total_rewards = np.array([])
    # Interaction loop with the game
    for episode in range(num_episodes):
        config = GameConfig(10, 10, 10)
        game = Game(config)  # Initialize the game
        state = game.get_state()  # Get the initial state
        total_reward = 0
        while not game.is_game_over():
            action = agent.select_action(state)  # Select action based on current state
            result = game.select(action)  # Perform action in the game
            next_state = game.get_state()  # Get the next state
            reward = result.reward  # Get the reward
            total_reward += reward
            agent.update_q_table(state, action, reward, next_state)  # Update Q-values
            state = next_state  # Move to the next state
        
        episodes_total_rewards = np.append(episodes_total_rewards, total_reward)

    print(f"Number of Episodes: {num_episodes}")
    print(f"Mean Reward: {np.mean(episodes_total_rewards)}")
    print(f"Median Reward: {np.median(episodes_total_rewards)}")
    print(f"Stddev: {np.median(episodes_total_rewards)}")


if __name__ == "__main__":
    main()