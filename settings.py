class Settings:
    def __init__(self, difficulty):
        # screen_width and screen_height must be multiple of cell_side
        choices = [(225, 225, 10), (400, 400, 40), (600, 400, 74)]
        choice = choices[difficulty]
        self.cell_side = 25
        self.screen_width = choice[0]
        self.screen_height = choice[1]
        self.bombs = choice[2]   # 76 is the best value for grid size 600x400

        self.columns = self.screen_width // self.cell_side
        self.rows = self.screen_height // self.cell_side
        self.total_cubes = self.columns * self.rows

        self.bg_color = (230, 230, 230)
        self.grid_color = (210, 210, 210)
        self.cell_cover_color = (200, 200, 200)

    def get_map_coord(self):
        map_coords = []
        for x in range(0, self.screen_width, self.cell_side):
            for y in range(0, self.screen_height, self.cell_side):
                map_coords.append((x, y))
        return map_coords