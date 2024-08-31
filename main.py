import pygame
import sys
import pygame_menu
import random
from settings import *
from world import World
from enemy import Enemy  # Импортируем класс Enemy
from player import Player  # Импортируем класс Player

pygame.init()

# Initialize the screen
screen = pygame.display.set_mode((700, 500), pygame.RESIZABLE)
pygame.display.set_caption("Platformer")

# Load and play background music
pygame.mixer.music.load("sounds/ColorfulFlowers.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Load the custom cursor and hide the default one
cursor = pygame.image.load("assets/cursor/cursor.png")
pygame.mouse.set_visible(False)

def game_cursor():
    x, y = pygame.mouse.get_pos()
    screen.blit(cursor, (x-2, y-2))

class Cloud:
    def __init__(self, image, x, y, speed):
        self.original_image = image
        self.image = image.copy()
        self.x = x
        self.y = y
        self.speed = speed
        self.alpha = 0
        self.image.set_alpha(self.alpha)

    def move(self):
        self.x += self.speed
        if self.x > WIDTH:
            return True
        return False

    def draw(self, screen):
        if self.alpha < 255:
            self.alpha += 1  # Increase transparency gradually
            self.image.set_alpha(self.alpha)
        screen.blit(self.image, (self.x, self.y))

class CloudManager:
    def __init__(self, screen, cloud_images, min_clouds=5, max_clouds=10):
        self.screen = screen
        self.cloud_images = cloud_images
        self.min_clouds = min_clouds
        self.max_clouds = max_clouds
        self.clouds = []
        self.cloud_timer = 0

        for _ in range(self.min_clouds):
            self.add_cloud()

    def add_cloud(self):
        cloud_image = random.choice(self.cloud_images)
        x = random.randint(-cloud_image.get_width(), WIDTH)
        y = random.randint(0, HEIGHT // 2)
        speed = random.uniform(0.5, 2)
        self.clouds.append(Cloud(cloud_image, x, y, speed))

    def update(self):
        self.cloud_timer += 1
        if self.cloud_timer > 60:  # Adjust cloud generation frequency
            if len(self.clouds) < self.max_clouds:
                self.add_cloud()
            self.cloud_timer = 0

        for cloud in self.clouds[:]:
            if cloud.move():
                self.clouds.remove(cloud)
            cloud.draw(self.screen)

class GameMain:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player_event = False
        self.bg_img = pygame.image.load('assets/terrain/bg.png')
        self.bg_img = pygame.transform.scale(self.bg_img, (width, height))
        self.world = World(world_map, self.screen)

        # Load cloud images and create CloudManager
        cloud_images = [
            pygame.image.load('assets/clouds/cloud1.png'),
            pygame.image.load('assets/clouds/cloud2.png'),
            pygame.image.load('assets/clouds/cloud3.png')
        ]
        self.cloud_manager = CloudManager(self.screen, cloud_images)

        # Создаем объект игрока
        self.player = Player(pos=(50, 400))
        self.last_width = width  # Сохраняем начальную ширину экрана

    def update_bg_image(self, width, height):
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/terrain/bg.png'), (width, height))
        # Пропорционально обновляем позицию игрока
        scale_factor = width / self.last_width
        self.player.rect.x = int(self.player.rect.x * scale_factor)
        self.last_width = width  # Обновляем текущую ширину экрана

    def main(self):
        while True:
            self.screen.blit(self.bg_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    self.update_bg_image(width, height)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player_event = "left"
                    if event.key == pygame.K_RIGHT:
                        self.player_event = "right"
                    if event.key == pygame.K_SPACE:
                        self.player_event = "space"
                elif event.type == pygame.KEYUP:
                    self.player_event = False

            self.screen.blit(self.bg_img, (0, 0))

            # Update and draw clouds
            self.cloud_manager.update()

            # Update player and enemy
            self.player.update(self.player_event)

            self.world.update(self.player_event)
            game_cursor()
            pygame.display.update()
            self.clock.tick(70)

# Menu code...
def set_difficulty(value, difficulty):
    pass  # Implement difficulty setting here

def start_the_game():
    game = GameMain(screen, 700, 500)
    game.main()

# Initialize the menu
menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == "__main__":
    menu.mainloop(screen)
