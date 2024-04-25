from minesweeper_env import MinesweeperEnv
from learning_agent import QLearningAgent  # type: ignore # Import your MinesweeperEnv class

if __name__ == "__main__":
    # Initialize Minesweeper environment
    env = MinesweeperEnv(width=8, height=8, n_mines=10)

    # Initialize Q-learning agent
    agent = QLearningAgent(env)

    # Train the agent
    agent.train()
