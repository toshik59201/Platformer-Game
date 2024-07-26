import pygame, pygame_menu
from settings import HEIGHT, WIDTH

pygame.font.init()


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 70)
        self.message_color = pygame.Color("darkorange")

    def show_game_over_menu(self):
        game_over_menu = pygame_menu.Menu('Game Over', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
        game_over_menu.add.button('Restart', self.restart_game)
        game_over_menu.add.button('Quit', pygame_menu.events.EXIT)
        game_over_menu.mainloop(self.screen)

    def restart_game(self):
        self.__init__(self.screen, 20, 15)
        self.main()

 #отображение кол-ва жизней игрока
    def show_life(self, player):
        life_size = 30
        img_path = "assets/life/life.png"
        life_image = pygame.image.load(img_path)
        life_image = pygame.transform.scale(life_image, (life_size, life_size))
        # life_rect = life_image.get_rect(topleft = pos)
        indent = 0
        for life in range(player.life):
            indent += life_size
            self.screen.blit(life_image, (indent, life_size))

#проверка, если игрок вышел за край мира
    def _game_lose(self, player):
        player.game_over = True
        message = self.font.render('You Lose...', True, self.message_color)
        self.screen.blit(message,(WIDTH // 3 + 70, 70))
        self.show_game_over_menu()

#проверка, если игрок выиграл
    def _game_win(self, player):
        player.game_over = True
        player.win = True
        message = self.font.render('You Win!!', True, self.message_color)
        self.screen.blit(message,(WIDTH // 3, 70))

#проверка, если игра закончена или нет, и если игрок выиграл или нет
    def game_state(self, player, goal):
        if player.life <= 0 or player.rect.y >= HEIGHT:
            self._game_lose(player)
            self.show_game_over_menu()
        elif player.rect.colliderect(goal.rect):
            self._game_win(player)