import pygame

COLOR_BOMB = (255, 0, 0)
COLOR_FLAG = (255, 0, 0)
COLOR_REVEALED_TILE = (192, 192, 192)
COLOR_UNREVEALED_TILE = (128, 128, 128)

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