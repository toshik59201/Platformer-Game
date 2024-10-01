import pygame
import sys

from settings import *
from world import World
from enemy import Enemy
from player import Player
from clouds import CloudManager
from userdatabase import initialize_database
from mainmenu import run_menu

pygame.init()

screen = pygame.display.set_mode((700, 500), pygame.RESIZABLE)
pygame.display.set_caption("Mayor Grom: the game")

# Load and play background music
pygame.mixer.music.load("sounds/Background_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Load the custom cursor and hide the default one
cursor = pygame.image.load("assets/cursor/cursor.png")
pygame.mouse.set_visible(False)

def game_cursor():
    x, y = pygame.mouse.get_pos()
    screen.blit(cursor, (x - 2, y - 2))

class GameMain:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player_event = None
        self.world = World(world_map, self.screen)
        self.font = pygame.font.SysFont(None, 36)

        # Загрузка фона и других ресурсов
        self.bg_img = self.load_background(width, height)
        self.cloud_manager = self.create_cloud_manager()
        self.player = Player(pos=(55, 400))
        self.enemy = Enemy(pos=(90, 400))

        # Добавляем врагов в мир
        self.world.add(self.enemy)
        self.last_width = width


    def load_background(self, width, height):
        bg_img = pygame.image.load('assets/terrain/bg.png')
        return pygame.transform.scale(bg_img, (width, height))


    def create_cloud_manager(self):
        """Initialize cloud manager with cloud images."""
        cloud_images = [
            pygame.image.load('assets/clouds/cloud1.png'),
            pygame.image.load('assets/clouds/cloud2.png'),
            pygame.image.load('assets/clouds/cloud3.png')
        ]
        return CloudManager(self.screen, cloud_images)

    def show_life(self):
        """Display player lives on screen."""
        life_text = self.font.render(f"Lives: {self.player.life}", True, (255, 255, 255))
        self.screen.blit(life_text, (50, 50))

    def update_bg_image(self, width, height):
        """Update background image and adjust player scaling based on screen size."""
        self.bg_img = self.load_background(width, height)
        scale_factor = width / self.last_width
        self.player.rect.x = int(self.player.rect.x * scale_factor)
        self.last_width = width

    def handle_events(self):
        """Handle game events like player input and screen resizing."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                self.update_bg_image(width, height)
                self.world = World(world_map, self.screen)  # Update the world for new screen size
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player_event = "left"
                if event.key == pygame.K_d:
                    self.player_event = "right"
                if event.key == pygame.K_SPACE:
                    self.player_event = "space"
            elif event.type == pygame.KEYUP:
                self.player_event = False

    def main(self):
        while True:
            self.handle_events()

            self.screen.blit(self.bg_img, (0, 0))
            self.cloud_manager.update()
            self.player.update(self.player_event)
            self.enemy.update()
            self.world.draw(self.screen)
            self.show_life()
            game_cursor()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    initialize_database()
    run_menu()