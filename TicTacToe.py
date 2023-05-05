import pygame
import sys

pygame.init()


class TicTacToe:
    def __init__(self,										 # конструктор класса (определяем основные характеристки игрового поля)
                 size_block=100,
                 margin=10,
                 cnt_blocks=3,
                 background_color=(0, 0, 0),
                 block_color=(255, 255, 255),
                 tic_color=(255, 0, 0),
                 tac_toe_color=(0, 255, 0),
                 nobody_win_color=(0, 255, 255),
                 x_color=(0, 0, 255),
                 o_color=(255, 0, 255),
                 caption="Крестики-нолики") -> None:

        self.margin = margin
        self.cnt_blocks = cnt_blocks
        self.cnt_margin = cnt_blocks + 1
        self.size_block = size_block
        self.background_color = background_color
        self.block_color = block_color
        self.tic_color = tic_color
        self.tac_toe_color = tac_toe_color
        self.nobody_win_color = nobody_win_color
        self.x_color = x_color
        self.o_color = o_color
        self.caption = caption
        self.height = self.width = size_block * self.cnt_blocks + margin * self.cnt_margin
        self.states = [[0] * cnt_blocks for i in range(cnt_blocks)]
        self.size_window = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size_window)
        self.cnt = 0
        self.current_color = self.block_color
        self.game_over = False

    def run_game(self) -> None:									# основная функция для игры
        pygame.display.set_caption(self.caption)
        while True:
            self.event_handling()
            self.build_playground()

    def build_playground(self) -> None:								# построение игрового поля и обработка событий
        if not self.game_over:
            for row in range(self.cnt_blocks):
                for col in range(self.cnt_blocks):
                    if self.states[row][col] == 1:
                        self.current_color = self.tic_color
                    elif self.states[row][col] == 2:
                        self.current_color = self.tac_toe_color
                    else:
                        self.current_color = self.block_color
                    x = col * self.size_block + (col + 1) * self.margin
                    y = row * self.size_block + (row + 1) * self.margin
                    pygame.draw.rect(self.screen, self.current_color, (x, y, self.size_block, self.size_block))
                    if self.current_color == self.tic_color:
                        pygame.draw.line(self.screen, self.x_color, (x + 5, y + 5),
                                         (x + self.size_block - 5, y + self.size_block - 5), 3)

                        pygame.draw.line(self.screen, self.x_color, (x + self.size_block - 5, y + 5),
                                         (x + 5, y + self.size_block - 5), 3)
                    elif self.current_color == self.tac_toe_color:
                        pygame.draw.circle(self.screen, self.o_color, (x + self.size_block // 2, y + self.size_block // 2),
                                           self.size_block // 2 - 3, 3)
            if (self.cnt - 1) % 2 == 0:
                self.game_over = self.check_win(1)
            else:
                self.game_over = self.check_win(2)

            if self.game_over:
                self.screen.fill(self.background_color)
                font = pygame.font.SysFont('stxingkai', 40)
                if self.game_over == 1:
                    text = font.render('Win X!', True, self.tic_color)
                elif self.game_over == 2:
                    text = font.render('Win 0!', True, self.tac_toe_color)
                else:
                    text = font.render('Friendship has won!', True, self.nobody_win_color)
                text_rect = text.get_rect()
                text_x = self.screen.get_width() / 2 - text_rect.width / 2
                text_y = self.screen.get_height() / 2 - text_rect.height / 2
                self.screen.blit(text, [text_x, text_y])

        pygame.display.update()

    def event_handling(self) -> None:                                                 # метод для обработки состояний
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                col = x_mouse // (self.size_block + self.margin)
                row = y_mouse // (self.size_block + self.margin)
                print(col, row)
                if self.states[row][col] == 0:
                    if self.cnt % 2 == 0:
                        self.states[row][col] = 1                           # 1 - X, 2 - 0
                    else:
                        self.states[row][col] = 2
                    self.cnt += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.cnt = 0
                self.states = [[0] * self.cnt_blocks for i in range(self.cnt_blocks)]
                self.game_over = False
                self.screen.fill(self.background_color)

    def check_win(self, gamer) -> int:  # 0 -  game unfinished, -1 - tie, gamer - win
        zeroes = 0
        for raw in self.states:
            zeroes += raw.count(0)
            if raw.count(gamer) == self.cnt_blocks:
                return gamer

        for col in range(self.cnt_blocks):
            flag = True
            for raw in range(self.cnt_blocks):
                if self.states[raw][col] != gamer:
                    flag = False
                    break
            if flag:
                return gamer

        flag = True
        for ceil in range(self.cnt_blocks):
            if self.states[ceil][ceil] != gamer:
                flag = False
                break
        if flag:
            return gamer

        flag = True
        for ceil in range(self.cnt_blocks - 1, -1, -1):
            if self.states[self.cnt_blocks - ceil - 1][ceil] != gamer:
                flag = False
                break
        if flag:
            return gamer

        if zeroes == 0:
            return -1

        return 0
