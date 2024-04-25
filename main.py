import pygame
from minesweeper import Game
from minesweeperenv import MinesweeperEnv
from qlearning import QLearningAgent
from maestro import Maestro
from agent import Agent

def main():
    agent = Agent(100, 2)
    agent.train(episodes=100)

def train_maestro():
    minesweeper_environment = MinesweeperEnv(width=10, height=10, n_mines=10)
    env_state_size = minesweeper_environment.nrows * minesweeper_environment.ncols
    q_learning_agent = QLearningAgent(state_size=env_state_size, action_size=2)

    mine_sweeping_maestro = Maestro(minesweeper_environment, q_learning_agent)
    mine_sweeping_maestro.train(100)
  
def play_pygame_minesweeper():
    pygame.init()

    rows = 10
    cols = 10
    size_of_square = 100
    mines = 10

    game = Game(rows, cols, size_of_square, mines)
    game.main_loop()
    pygame.quit()

if __name__ == "__main__":
    main()
