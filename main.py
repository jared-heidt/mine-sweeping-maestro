import pygame
from minesweeper import Game

def main():
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
