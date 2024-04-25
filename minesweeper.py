import pygame
import random

COLOR_BOMB = (255, 0, 0)
COLOR_FLAG = (255, 0, 0)
COLOR_REVEALED_TILE = (192, 192, 192)
COLOR_UNREVEALED_TILE = (128, 128, 128)
COLOR_SCREEN_FILL = (255, 255, 255)


class Tile:
    def __init__(self, row, col, size_of_square):
        self.row = row
        self.col = col
        self.size_of_square = size_of_square
        self.rect = pygame.Rect(col * size_of_square, row * size_of_square, size_of_square, size_of_square)
        self.is_bomb = False
        self.is_revealed = False
        self.is_flagged = False
        self.num_adjacent_bombs = 0

    def reveal(self):
        self.is_revealed = True

    def flag(self):
        self.is_flagged = not self.is_flagged

    def draw(self, screen, myfont):
        if self.is_revealed:
            if self.is_bomb:
                color = COLOR_BOMB
            else:
                color = COLOR_REVEALED_TILE
    
            pygame.draw.rect(screen, color, self.rect)

            if not self.is_bomb and self.num_adjacent_bombs > 0:
                text = myfont.render(str(self.num_adjacent_bombs), 1, (0, 0, 0))
                screen.blit(text, (self.col * self.size_of_square + 20, self.row * self.size_of_square + 20))
                
        else:
            color = COLOR_UNREVEALED_TILE 
            pygame.draw.rect(screen, color, self.rect)
            
            if self.is_flagged:
                text = myfont.render("F", 1, COLOR_FLAG)
                screen.blit(text, (self.col * self.size_of_square + 20, self.row * self.size_of_square + 20))

# This is the environment   
class MinesweeperGrid:
    def __init__(self, rows, cols, size_of_square, mines):
        self.rows = rows # nrows
        self.cols = cols # ncolsss=
        self.size_of_square = size_of_square
        self.tiles = [[Tile(row, col, size_of_square) for col in range(cols)] for row in range(rows)]
        self.plant_mines(mines)
        self.game_over = False
        self.rewards = REWARDS
        self.clicks = 0
        self.progress = 0
        self.wins = 0
        
    def plant_mines(self, num_mines):
        bomb_positions = random.sample([(r, c) for r in range(self.rows) for c in range(self.cols)], num_mines)
        
        for row, col in bomb_positions:
            self.tiles[row][col].is_bomb = True
        
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.tiles[row][col].is_bomb:
                    neighbors = self.get_neighbors(row, col)
                    self.tiles[row][col].num_adjacent_bombs = sum(self.tiles[r][c].is_bomb for r, c in neighbors)

    def reveal_tile(self, row, col):
        tile = self.tiles[row][col]
        if not tile.is_revealed and not tile.is_flagged:
            tile.reveal()
            if tile.is_bomb:
                self.game_over = True
                return
            if not tile.is_bomb and tile.num_adjacent_bombs == 0:
                neighbors = self.get_neighbors(row, col)
                for neighbor_row, neighbor_col in neighbors:
                    self.reveal_tile(neighbor_row, neighbor_col)

    def flag_tile(self, row, col):
        tile = self.tiles[row][col]
        if not tile.is_revealed:
            tile.flag()

    def get_neighbors(self, row, col):
        neighbors = []
        for d_row in range(-1, 2):
            for d_col in range(-1, 2):
                if d_row == 0 and d_col == 0:
                    continue
                neighbor_row = row + d_row
                neighbor_col = col + d_col
                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols:
                    neighbors.append((neighbor_row, neighbor_col))
                    
        return neighbors
    

    # Visuals
    def draw(self, screen, myfont):
        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles[row][col].draw(screen, myfont)

# Use for playing the game manually       
class Game:
    def __init__(self, rows, cols, size_of_square, mines):
        self.grid = MinesweeperGrid(rows, cols, size_of_square, mines)
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont("monospace-bold", 100)
        self.screen = pygame.display.set_mode((cols * size_of_square, rows * size_of_square))

    def main_loop(self):
        while not self.grid.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.grid.game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_left_click(pygame.mouse.get_pos())
                    elif event.button == 3:
                        self.handle_right_click(pygame.mouse.get_pos())

            self.screen.fill(COLOR_SCREEN_FILL)
            self.grid.draw(self.screen, self.myfont)
            pygame.display.flip()

    def handle_left_click(self, pos):
        col = pos[0] // self.grid.size_of_square
        row = pos[1] // self.grid.size_of_square
        if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
            self.grid.reveal_tile(row, col)

    def handle_right_click(self, pos):
        col = pos[0] // self.grid.size_of_square
        row = pos[1] // self.grid.size_of_square
        if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
            self.grid.flag_tile(row, col)