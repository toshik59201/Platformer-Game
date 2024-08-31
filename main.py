import pygame
import sys
import pygame_menu
from settings import *
from world import World
from enemy import Enemy
from player import Player
from clouds import CloudManager

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

        # Create player and enemy
        self.player = Player(pos=(55, 400))
        self.enemy = Enemy(pos=(90, 400))

        # Add player and enemy to world
        #self.world.add(self.player)
        self.world.add(self.enemy)

        self.last_width = width

    def show_life(self, player):
            # Отображение жизней игрока
            life_text = self.font.render(f"Lives: {player.life}", True, (255, 255, 255))
            self.screen.blit(life_text, (10, 10))  # Позиция на экране (10, 10)

    def update_bg_image(self, width, height):
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/terrain/bg.png'), (width, height))
        # Adjust player position proportional to screen width change
        scale_factor = width / self.last_width
        self.player.rect.x = int(self.player.rect.x * scale_factor)
        self.last_width = width  # Update last_width to current width

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

            # Update and draw clouds
            self.cloud_manager.update()

            # Update player and enemy
            self.player.update(self.player_event)
            self.enemy.update()

            # Update and draw the world
            self.world.update(self.player_event)
            self.world.draw(self.screen)
            
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
menu.add.text_input('Nickname :', default='Тоши')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == "__main__":
    menu.mainloop(screen)
