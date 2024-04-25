import random
import numpy as np
import pandas as pd

WIN_STR = 'win'
WIN_REWARD = 1
LOSE_STR = 'lose'
LOSE_REWARD = -1
PROGRESS_STR = 'progress'
PROGRESS_REWARD = 0.3
GUESS_STR = 'guess'
GUESS_REWARD = -0.3
NO_PROGRESS_STR = 'no_progress'
NO_PROGRESS_REWARD = -0.3

REWARDS = {
    WIN_STR: WIN_REWARD,
    LOSE_STR: LOSE_REWARD,
    PROGRESS_STR: PROGRESS_REWARD,
    GUESS_STR: GUESS_REWARD,
    NO_PROGRESS_STR: NO_PROGRESS_REWARD,
}

class MinesweeperEnv(object):
    def __init__(self, width, height, n_mines, rewards=REWARDS):
        self.nrows, self.ncols = width, height
        self.ntiles = self.nrows * self.ncols
        self.n_mines = n_mines
        self.grid = self.init_grid()
        self.board = self.get_board()
        self.state, self.state_im = self.init_state()
        self.n_clicks = 0
        self.n_progress = 0
        self.n_wins = 0
        self.rewards = rewards

    def init_grid(self):
        board = np.zeros((self.nrows, self.ncols), dtype='object')
        mines = self.n_mines

        while mines > 0:
            row, col = random.randint(0, self.nrows-1), random.randint(0, self.ncols-1)
            if board[row][col] != 'B':
                board[row][col] = 'B'
                mines -= 1

        return board

    def get_neighbors(self, coord):
        x,y = coord[0], coord[1]

        neighbors = []
        for col in range(y-1, y+2):
            for row in range(x-1, x+2):
                if ((x != row or y != col) and
                    (0 <= col < self.ncols) and
                    (0 <= row < self.nrows)):
                    neighbors.append(self.grid[row,col])

        return np.array(neighbors)

    def count_bombs(self, coord):
        neighbors = self.get_neighbors(coord)
        return np.sum(neighbors=='B')

    def get_board(self):
        board = self.grid.copy()

        coords = []
        for x in range(self.nrows):
            for y in range(self.ncols):
                if self.grid[x,y] != 'B':
                    coords.append((x,y))

        for coord in coords:
            board[coord] = self.count_bombs(coord)

        return board


    def get_state_im(self, state):
        #Gets the numeric image representation state of the board.
        #This is what will be the input for the DQN.
        state_im = [t['value'] for t in state]
        state_im = np.reshape(state_im, (self.nrows, self.ncols, 1)).astype(object)

        state_im[state_im=='U'] = -1
        state_im[state_im=='B'] = -2

        state_im = state_im.astype(np.int8) / 8
        state_im = state_im.astype(np.float16)

        return state_im

    
    def init_state(self):
        unsolved_array = np.full((self.nrows, self.ncols), 'U', dtype='object')

        state = []
        for (x, y), value in np.ndenumerate(unsolved_array):
            state.append({'coord': (x, y), 'value':value})

        state_im = self.get_state_im(state)

        return state, state_im
        
    def click(self, action_index):
        coord = self.state[action_index]['coord']
        value = self.board[coord]

        # ensure first move is not a bomb
        if (value == 'B') and (self.n_clicks == 0):
            grid = self.grid.reshape(1, self.ntiles)
            move = np.random.choice(np.nonzero(grid!='B')[1])
            coord = self.state[move]['coord']
            value = self.board[coord]
            self.state[move]['value'] = value
        else:
            # make state equal to board at given coordinates
            self.state[action_index]['value'] = value

        # reveal all neighbors if value is 0
        if value == 0.0:
            self.reveal_neighbors(coord, clicked_tiles=[])

        self.n_clicks += 1

    def reveal_neighbors(self, coord, clicked_tiles):
        processed = clicked_tiles
        state_df = pd.DataFrame(self.state)
        x,y = coord[0], coord[1]

        neighbors = []
        for col in range(y-1, y+2):
            for row in range(x-1, x+2):
                if ((x != row or y != col) and
                    (0 <= col < self.ncols) and
                    (0 <= row < self.nrows) and
                    ((row, col) not in processed)):

                    # prevent redundancy for adjacent zeros
                    processed.append((row,col))

                    index = state_df.index[state_df['coord'] == (row,col)].tolist()[0]

                    self.state[index]['value'] = self.board[row, col]

                    # recursion in case neighbors are also 0
                    if self.board[row, col] == 0.0:
                        self.reveal_neighbors((row, col), clicked_tiles=processed)

    '''
    # Start dumb code 
    def init_state(self):
        # Initialize the state as an array of 'U's (unrevealed)
        state = np.full((self.nrows, self.ncols), 'U', dtype=object)
        state_im = self.get_state_im(state)
        return state, state_im

    def get_state_im(self, state):
        # Convert the state to numeric image representation
        state_im = state.copy()
        state_im[state_im == 'U'] = -1  # Unrevealed tiles
        state_im[state_im == 'B'] = -2  # Bombs
        state_im = state_im.astype(np.float16) / 8  # Scale to range [0, 1]
        return state_im

    def click(self, action_index):
        # Update the state by revealing the value at the clicked tile
        x, y = np.unravel_index(action_index, (self.nrows, self.ncols))
        if self.state_im[x, y] == -1:  # If unrevealed
            value = self.board[x, y]
            self.state_im[x, y] = value
            if value == 0:
                self.reveal_neighbors((x, y))

    def reveal_neighbors(self, coord):
        # Recursively reveal neighboring tiles if they are empty
        x, y = coord
        for i in range(max(0, x - 1), min(self.nrows, x + 2)):
            for j in range(max(0, y - 1), min(self.ncols, y + 2)):
                if self.state_im[i, j] == -1:  # If unrevealed
                    self.state_im[i, j] = self.board[i, j]
                    if self.board[i, j] == 0:
                        self.reveal_neighbors((i, j))
    # End dumb code 
    '''

    def find_state_index(self, coord):
        for i, tile in enumerate(self.state):
            if tile['coord'] == coord:
                return i
        return None  # Return None if the coordinate pair is not found in the state

    def color_state(self, value):
        if value == -1:
            color = 'white'
        elif value == 0:
            color = 'slategrey'
        elif value == 1:
            color = 'blue'
        elif value == 2:
            color = 'green'
        elif value == 3:
            color = 'red'
        elif value == 4:
            color = 'midnightblue'
        elif value == 5:
            color = 'brown'
        elif value == 6:
            color = 'aquamarine'
        elif value == 7:
            color = 'black'
        elif value == 8:
            color = 'silver'
        else:
            color = 'magenta'

        return f'color: {color}'

    def draw_state(self, state_im):
        state = state_im * 8.0
        state_df = pd.DataFrame(state.reshape((self.nrows, self.ncols)), dtype=np.int8)

        display(state_df.style.applymap(self.color_state))

    

    def reset(self):
        self.n_clicks = 0
        self.n_progress = 0
        self.grid = self.init_grid()
        self.board = self.get_board()
        self.state, self.state_im = self.init_state()
        print('Set State in MinesweeperEnv to the following: ' + str(self.state))

    def step(self, action_index):
        done = False
        # coords = self.state[action_index]['coord']
        print('\nBANG\n' + str(action_index) + '\nBANG\n')
        coords = action_index[1]['coord']
        value = action_index[1]['value']

    

        current_state = self.state_im

        # get neighbors before action
        neighbors = self.get_neighbors(coords)

        self.click(action_index)

        # update state image
        new_state_im = self.get_state_im(self.state)
        self.state_im = new_state_im

        if self.state[action_index]['value']=='B': # if lose
            reward = self.rewards[LOSE_STR]
            done = True

        elif np.sum(new_state_im==-0.125) == self.n_mines: # if win
            reward = self.rewards[WIN_STR]
            done = True
            self.n_progress += 1
            self.n_wins += 1

        elif np.sum(self.state_im == -0.125) == np.sum(current_state == -0.125):
            reward = self.rewards[NO_PROGRESS_STR]

        else: # if progress
            if all(t==-0.125 for t in neighbors): # if guess (all neighbors are unsolved)
                reward = self.rewards[GUESS_STR]

            else:
                reward = self.rewards[PROGRESS_STR]
                self.n_progress += 1 # track n of non-isoloated clicks

        return self.state_im, reward, done#