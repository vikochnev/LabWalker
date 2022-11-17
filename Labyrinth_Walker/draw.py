from superwires import games, color
import labyrinth, pathfinder, math

games.init(screen_width=800, screen_height=600, fps=60)


class BoardMetric:
    """Класс для пересчёта координат"""

    def __init__(self, pos_x, pos_y):
        self.tile_width = 40
        self.tile_height = 40
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_x(self):
        return self.tile_width * (0.5 + self.pos_x)

    def get_y(self):
        return self.tile_width * (0.5 + self.pos_y)


class Player(games.Sprite):
    """Класс, определяющий Игрока"""
    image = games.load_image("player.bmp")
    STEP_DELAY = 10

    def __init__(self, game):
        self.game = game
        self.pos = game.lab.get_start()
        self.draw = BoardMetric(self.pos[0], self.pos[1])
        self.draw_x = self.draw.get_x()
        self.draw_y = self.draw.get_y()
        self.step_delay = 0
        self.a_step_delay = 0
        self.if_automove = False
        super(Player, self).__init__(image=Player.image,
                                     x=self.draw.get_x(),
                                     y=self.draw.get_y())

    def update(self):
        """Определяет передвижение Игрока"""
        super(Player, self).update()

        # Задаёт снижение таймера задержки между шагами
        if self.step_delay > 0:
            self.step_delay -= 1
        if self.a_step_delay > 0:
            self.a_step_delay -= 1

        if self.if_automove:
            if self.a_step_delay == 0:
                self.game.calc_path()
                self.automove()
                self.a_step_delay = self.STEP_DELAY

        # Отвечает за нажатие клавиш
        if self.step_delay == 0:
            if not self.if_automove:
                if games.keyboard.is_pressed(games.K_a):
                    self.try_move("LEFT")
                if games.keyboard.is_pressed(games.K_d):
                    self.try_move("RIGHT")
                if games.keyboard.is_pressed(games.K_w):
                    self.try_move("UP")
                if games.keyboard.is_pressed(games.K_s):
                    self.try_move("DOWN")
            if games.keyboard.is_pressed(games.K_q):
                if not self.if_automove:
                    self.if_automove = True
                else:
                    self.if_automove = False
                self.step_delay = self.STEP_DELAY

        self.move()
        self.game.check_win()

    def try_move(self, dir):
        """Определяет , может ли Игрок передвинуться на заданную клетку"""
        tpos_x, tpos_y = self.pos[0], self.pos[1]
        if dir == "LEFT":
            tpos_x = self.pos[0] - 1
        if dir == "RIGHT":
            tpos_x = self.pos[0] + 1
        if dir == "UP":
            tpos_y = self.pos[1] - 1
        if dir == "DOWN":
            tpos_y = self.pos[1] + 1

        if self.game.lab.is_valid_point([tpos_x, tpos_y]):
            if self.game.lab.get_cell_type(tpos_x, tpos_y) == labyrinth.CellType.Empty:
                self.pos[0], self.pos[1] = tpos_x, tpos_y
        self.step_delay = self.STEP_DELAY

    def move(self):
        """Отвечает за перерисовку положения Игрока"""
        self.draw = BoardMetric(self.pos[0], self.pos[1])
        self.x = self.draw.get_x()
        self.y = self.draw.get_y()

    def automove(self):
        self.pos[0], self.pos[1] = self.game.path[0].pos[1], self.game.path[0].pos[0]
        self.game.path.pop(0)


class Game:
    """Основной класс, отвечает за запуск и основные процессы игры"""

    def __init__(self):
        """Инициализировать объект игры"""
        self.path = None
        self.lab = None

    def set_board(self, board):
        self.lab = board

    def set_path(self, path):
        self.path = path

    def play(self):
        """Основной процесс игры"""
        self.draw_labyrinth()
        self.player = Player(game=self)
        games.screen.add(self.player)
        self.end_pos = self.lab.get_end()

        games.screen.mainloop()

    def draw_labyrinth(self):
        walk_image = games.load_image("walkable.bmp", transparent=False)
        wall_image = games.load_image("wall.bmp", transparent=False)
        start_image = games.load_image("start.bmp", transparent=False)
        end_image = games.load_image("end.bmp", transparent=False)
        lab_wdth, lab_hght = self.lab.get_size()
        for ix in range(lab_wdth):
            for iy in range(lab_hght):
                tile_mark = self.lab.get_cell_mark(ix, iy)
                tile_type = self.lab.get_cell_type(ix, iy)
                pos = BoardMetric(ix, iy)
                draw_x = pos.get_x()
                draw_y = pos.get_y()
                if tile_mark == labyrinth.CellMark.Start:
                    tile = games.Sprite(image=start_image, x=draw_x, y=draw_y)
                elif tile_mark == labyrinth.CellMark.End:
                    tile = games.Sprite(image=end_image, x=draw_x, y=draw_y)
                elif tile_mark == labyrinth.CellMark.No:
                    if tile_type == labyrinth.CellType.Empty:
                        tile = games.Sprite(image=walk_image, x=draw_x, y=draw_y)
                    elif tile_type == labyrinth.CellType.Block:
                        tile = games.Sprite(image=wall_image, x=draw_x, y=draw_y)
                games.screen.add(tile)

    def calc_path(self):
        filled = pathfinder.fill_shortest_path(self.lab, self.player.pos, self.lab.get_end())
        path = pathfinder.backtrack_to_start(filled, filled.get_end())
        path.reverse()
        path.pop(0)
        self.path = path

    def check_win(self):
        if self.player.pos == self.end_pos:
            print("You won!")
            games.screen.quit()
