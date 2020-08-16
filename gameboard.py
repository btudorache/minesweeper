import pygame

import sys
from random import choice

class Gameboard:
    def __init__(self, settings, screen):
        self.grid_width = settings.screen_width
        self.grid_height = settings.screen_height
        self.grid_cell = settings.cell_side

        self.game_screen = screen
        self.game_settings = settings

        self.first_click = False
        self.bomb_hit = False
        self.reset_game()

    def draw_grid(self):
        for x in range(0, self.grid_width, self.grid_cell):
            pygame.draw.line(self.game_screen, self.game_settings.grid_color, (x, 0), (x, self.grid_height))
        for y in range(0, self.grid_height, self.grid_cell):
            pygame.draw.line(self.game_screen, self.game_settings.grid_color, (0, y), (self.grid_width, y))

    # Create cell objects for the entire board
    def create_board(self):
        self.cells = []
        for x in range(0, self.grid_width, self.grid_cell):
            new_row = []
            self.cells.append(new_row)
            for y in range(0, self.grid_height, self.grid_cell):
                cell = Cell(self.game_settings, self.game_screen, x, y)
                new_row.append(cell)

    def create_bombs(self, grid_coord):
        for _ in range(self.game_settings.bombs):
            bomb_coord = choice(grid_coord)
            self.cells[bomb_coord[0] // self.grid_cell][bomb_coord[1] // self.grid_cell].init_bomb_cell()
            grid_coord.remove(bomb_coord)

    def create_numbered_cells(self):
        # define check cell function
        def check_cell(x, y):
            nonlocal neighbour_bombs
            if self.cells[x][y].is_bomb():
                neighbour_bombs += 1

        for x in range(self.game_settings.columns):
            for y in range(self.game_settings.rows):
                # Check only plain cells
                if self.cells[x][y].type == 0:
                    neighbour_bombs = 0
                    # Check corners
                    # Check upper left corner
                    if x == 0 and y == 0:
                        check_cell(x + 1, y)
                        check_cell(x, y + 1)
                        check_cell(x + 1, y + 1)

                    # Check upper right corner
                    elif x == self.game_settings.columns - 1 and y == 0:
                        check_cell(x - 1, y)
                        check_cell(x, y + 1)
                        check_cell(x - 1, y + 1)

                    # Check lower left corner
                    elif x == 0 and y == self.game_settings.rows - 1:
                        check_cell(x + 1, y)
                        check_cell(x, y - 1)
                        check_cell(x + 1, y - 1)

                    # Check lower right corner
                    elif x == self.game_settings.columns - 1 and y == self.game_settings.rows - 1:
                        check_cell(x - 1, y)
                        check_cell(x, y - 1)
                        check_cell(x - 1, y - 1)

                    # Check sides
                    # Check left side
                    elif x == 0:
                        check_cell(x, y - 1)
                        check_cell(x + 1, y - 1)
                        check_cell(x + 1, y)
                        check_cell(x + 1, y + 1)
                        check_cell(x, y + 1)

                    # check right edge
                    elif x == self.game_settings.columns - 1:
                        check_cell(x, y - 1)
                        check_cell(x - 1, y - 1)
                        check_cell(x - 1, y)
                        check_cell(x - 1, y + 1)
                        check_cell(x, y + 1)

                    # check upper edge
                    elif y == 0:
                        check_cell(x - 1, y)
                        check_cell(x - 1, y + 1)
                        check_cell(x, y + 1)
                        check_cell(x + 1, y + 1)
                        check_cell(x + 1, y)

                    # check lower edge
                    elif y == self.game_settings.rows - 1:
                        check_cell(x - 1, y)
                        check_cell(x - 1, y - 1)
                        check_cell(x, y - 1)
                        check_cell(x + 1, y - 1)
                        check_cell(x + 1, y)

                    # check other edges
                    else:
                        check_cell(x, y - 1)
                        check_cell(x + 1, y - 1)
                        check_cell(x + 1, y)
                        check_cell(x + 1, y + 1)
                        check_cell(x, y + 1)
                        check_cell(x - 1, y + 1)
                        check_cell(x - 1, y)
                        check_cell(x - 1, y - 1)

                    # initialize numbered cell if there are bombs around
                    if neighbour_bombs:
                        self.cells[x][y].init_numbered_cell(neighbour_bombs)

    def protect_first_click(self, x, y):
        x, y = x * self.grid_cell, y * self.grid_cell
        grid_coord = self.game_settings.get_map_coord()

        grid_coord.remove((x, y))
        # check upper left corner
        if x == 0 and y == 0:
            grid_coord.remove((x + self.grid_cell, y))
            grid_coord.remove((x, y + self.grid_cell))
            grid_coord.remove((x + self.grid_cell, y + self.grid_cell))
        # check upper right corner
        elif x == 0 and y == self.grid_height - self.grid_cell:
            grid_coord.remove((x, y - self.grid_cell))
            grid_coord.remove((x + self.grid_cell, y - self.grid_cell))
            grid_coord.remove((x + self.grid_cell, y))
        # check lower left corner
        elif x == self.grid_width - self.grid_cell and y == 0:
            grid_coord.remove((x - self.grid_cell, y))
            grid_coord.remove((x, y + self.grid_cell))
            grid_coord.remove((x - self.grid_cell, y + self.grid_cell))
        # check lower right corner
        elif x == self.grid_width - self.grid_cell and y == self.grid_height - self.grid_cell:
            grid_coord.remove((x - self.grid_cell, y))
            grid_coord.remove((x, y - self.grid_cell))
            grid_coord.remove((x - self.grid_cell, y - self.grid_cell))
        # check left edge
        elif x == 0:
            grid_coord.remove((x, y - self.grid_cell))
            grid_coord.remove((x + self.grid_cell, y - self.grid_cell))
            grid_coord.remove((x + self.grid_cell, y))
            grid_coord.remove((x + self.grid_cell, y + self.grid_cell))
            grid_coord.remove((x, y + self.grid_cell))
        # check right edge
        elif x == self.grid_width - self.grid_cell:
            grid_coord.remove((x, y - self.grid_cell))
            grid_coord.remove((x - self.grid_cell, y - self.grid_cell))
            grid_coord.remove((x - self.grid_cell, y))
            grid_coord.remove((x - self.grid_cell, y + self.grid_cell))
            grid_coord.remove((x, y + self.grid_cell))
        # check upper edge
        elif y == 0:
            grid_coord.remove((x - self.grid_cell, y))
            grid_coord.remove((x - self.grid_cell, y + self.grid_cell))
            grid_coord.remove((x, y + self.grid_cell))
            grid_coord.remove((x + self.grid_cell, y + self.grid_cell))
            grid_coord.remove((x + self.grid_cell, y))
        # check lower edge
        elif y == self.grid_height - self.grid_cell:
            grid_coord.remove((x - self.grid_cell, y))
            grid_coord.remove((x + self.grid_cell, y))
            grid_coord.remove((x - self.grid_cell, y - self.grid_cell))
            grid_coord.remove((x, y - self.grid_cell))
            grid_coord.remove((x + self.grid_cell, y - self.grid_cell))
        # check every other edge
        else:
            grid_coord.remove((x, y - self.grid_cell))
            grid_coord.remove((x, y + self.grid_cell))
            grid_coord.remove((x + self.grid_cell, y))
            grid_coord.remove((x + self.grid_cell, y + self.grid_cell))
            grid_coord.remove((x + self.grid_cell, y - self.grid_cell))
            grid_coord.remove((x - self.grid_cell, y))
            grid_coord.remove((x - self.grid_cell, y + self.grid_cell))
            grid_coord.remove((x - self.grid_cell, y - self.grid_cell))

        return grid_coord

    def reset_game(self):
        self.first_click = False
        self.bomb_hit = False
        self.create_board()

    def create_game(self, x, y):
        grid_coord = self.protect_first_click(x, y)
        self.create_bombs(grid_coord)
        self.create_numbered_cells()

        self.first_click = True

    def reveal_all_cells(self):
        for row in self.cells:
            for cell in row:
                cell.reveal()

    def reveal_cell(self, x, y):
        # if cell is plain
        if self.cells[x][y].type == 0:
            self.reveal_plain_cells(x, y)
        elif self.cells[x][y].type == 1:
            self.cells[x][y].reveal()
        elif self.cells[x][y].is_bomb():
            self.bomb_hit = True
            for row in self.cells:
                for cell in row:
                    if cell.is_bomb() and not cell.flagged:
                        cell.reveal()

    # Clear neighbor plain cells recursively
    def reveal_plain_cells(self, x, y):
        # Return function if x, y are out of map grid bounds or
        # cell is not plain or cell is revealed
        if (x < 0 or x >= self.game_settings.columns or y < 0 or y >= self.game_settings.rows or
            self.cells[x][y].is_bomb() or self.cells[x][y].revealed):
            return
        self.cells[x][y].reveal()
        if self.cells[x][y].type == 1:
            return

        # call the function in every other 8 directions recursively
        self.reveal_plain_cells(x - 1, y)
        self.reveal_plain_cells(x - 1, y - 1)
        self.reveal_plain_cells(x + 1, y)
        self.reveal_plain_cells(x + 1, y + 1)
        self.reveal_plain_cells(x, y - 1)
        self.reveal_plain_cells(x + 1, y - 1)
        self.reveal_plain_cells(x, y + 1)
        self.reveal_plain_cells(x - 1, y + 1)

    def draw_cells(self):
        for row in self.cells:
            for cell in row:
                if cell.revealed:
                    cell.draw_revealed_cell()
                else:
                    cell.draw_unrevealed_cell()


class Cell:
    def __init__(self, settings, screen, x, y):
        self.x = x
        self.y = y
        self.size = settings.cell_side
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        # Cell types:
        # type = 0 ---> plain cell
        # type = 1 ---> numbered cell
        # type = 2 ---> bomb cell
        self.type = 0
        self.revealed = False
        self.flagged = False

        self.color = settings.cell_cover_color
        self.flag_image = pygame.image.load('media/flag.bmp')
        self.game_screen = screen

    def draw_unrevealed_cell(self):
        # Draw unrevealed cell if not flagged, else draw flag
        if not self.flagged:
            pygame.draw.rect(self.game_screen, self.color, self.rect)
        else:
            self.game_screen.blit(self.flag_image, self.rect)

    def draw_revealed_cell(self):
        # Draw revealed cells
        if not self.type == 0:
            self.game_screen.blit(self.image, (self.x, self.y, self.size, self.size))

    def flag_cell(self):
        if not self.flagged:
            self.flagged = True
        else:
            self.flagged = False

    def reveal(self):
        self.revealed = True

    def is_bomb(self):
        return self.type == 2

    def init_numbered_cell(self, bombs):
        self.type = 1
        self.image = pygame.image.load('media/' + str(bombs) + '.bmp')

    def init_bomb_cell(self):
        self.type = 2
        self.image = pygame.image.load('media/bomb.bmp')
