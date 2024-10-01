import pygame
import pygame_menu
from settings import HEIGHT, WIDTH

pygame.init()
pygame.font.init()


class Game:
    def __init__(self, screen):
        self.screen = pygame.display.set_mode((700, 500), pygame.RESIZABLE)
        self.font = pygame.font.SysFont("impact", 70)
        self.message_color = pygame.Color("darkorange")
        self.clock = pygame.time.Clock()

        # Load life animation frames
        self.life_frames = [pygame.image.load(f"assets/life/{i}.png") for i in range(4)]
        self.life_size = 30
        self.life_frames = [pygame.transform.scale(frame, (self.life_size, self.life_size)) for frame in self.life_frames]
        self.life_animation_index = 0
        self.animation_speed = 0.01  # Controls animation speed

        self.reset()

    def reset(self):
        # Initialize or reset game state here
        self.game_over = False
        self.player_win = False
        self.running = True
        self.game_over_menu = None

    def show_game_over_menu(self):
        self.game_over_menu = pygame_menu.Menu('Game Over', 700, 500, theme=pygame_menu.themes.THEME_BLUE)
        self.game_over_menu.add.button('Restart', self.restart_game)
        self.game_over_menu.add.button('Quit', pygame_menu.events.EXIT)
        self.game_over_menu.mainloop(self.screen)

    def restart_game(self):
        self.reset()
        self.main()  # Restart the game loop

    # Display number of player lives
    def show_life(self, player):
        start_x = 20  # Start 20 pixels from the left edge of the screen
        self.life_animation_index += self.animation_speed
        if self.life_animation_index >= len(self.life_frames):
            self.life_animation_index = 0
        
        current_frame = self.life_frames[int(self.life_animation_index)]

        for i in range(player.life):
            x_position = start_x + i * (self.life_size + 2)  # 2 pixel gap between hearts
            self.screen.blit(current_frame, (x_position, self.life_size))

    # Check if player lost
    def _game_lose(self, player):
        self.game_over = True
        message = self.font.render('You Lose...', True, self.message_color)
        self.screen.blit(message, (WIDTH // 3 + 70, 70))
        self.show_game_over_menu()

    # Check if player won
    def _game_win(self, player):
        self.game_over = True
        self.player_win = True
        message = self.font.render('You Win!!', True, self.message_color)
        self.screen.blit(message, (WIDTH // 3, 70))

    # Check game state and if the player won or lost
    def game_state(self, player, goal):
        if player.life <= 0 or player.rect.y >= HEIGHT:
            self._game_lose(player)
        elif player.rect.colliderect(goal.rect):
            self._game_win(player)
        if self.game_over:
            self.show_game_over_menu()

    def update(self):
        pass

    def draw(self):
        print("Отрисовка элементов")  # Добавляем отладочный вывод
        self.screen.fill((0, 0, 0))  # Заполняем экран черным
        pygame.display.update()

    def main(self):
        print("Запуск игрового цикла")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.restart_game()

            if not self.game_over:
                print("Игра обновляется")
                self.update()
                self.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
