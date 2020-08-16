import sys
try:
    import pygame
except:
    print("You must install pygame")
    sys.exit()

from difficulty import run_choices_gui
from settings import Settings
from gameboard import Gameboard

class MineSweeper:
    def __init__(self, difficulty):
        pygame.init()
        self.settings = Settings(difficulty)

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_icon(pygame.image.load('media/logo.bmp'))
        pygame.display.set_caption("Minesweeper")

        self.gameboard = Gameboard(self.settings, self.screen)

    def _check_end_game(self):
        if self.gameboard.bomb_hit:
            self.gameboard.reset_game()
            pygame.event.set_blocked(pygame.MOUSEMOTION)
            pygame.time.delay(2000)
            pygame.event.set_allowed(pygame.MOUSEMOTION)

    def run_game(self):
        while True:
            pygame.time.delay(40)
            self._check_events()

            self._update_screen()
            pygame.display.flip()
            self._check_end_game()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_button_down_events(event)

    def _check_mouse_button_down_events(self, event):
        # get cell coordinates
        x, y = event.pos[0] // self.settings.cell_side, event.pos[1] // self.settings.cell_side

        # create game on the first click
        if not self.gameboard.first_click:
            self.gameboard.create_game(x, y)
        # If mouse_button_down event is a left click
        if event.button == 1 and not self.gameboard.cells[x][y].flagged:
            # Reveal cell if not flagged
            self.gameboard.reveal_cell(x, y)
        # flag cell if right click
        elif event.button == 3:
            self.gameboard.cells[x][y].flag_cell()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_r:
            self.gameboard.reset_game()
        elif event.key == pygame.K_SPACE:
            self.gameboard.reveal_all_cells()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.gameboard.draw_cells()
        self.gameboard.draw_grid()

def main():
    try:
        diff = run_choices_gui()
    except:
        print("You must choose a difficulty")
        sys.exit()
    ai = MineSweeper(diff)
    ai.run_game()

if __name__ == "__main__":
    main()