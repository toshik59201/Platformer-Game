import pygame
import sys
import pygame_menu
from settings import *
from world import World

pygame.init()

# Initialize the screen
screen = pygame.display.set_mode((400, 300), pygame.RESIZABLE)
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

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player_event = False
        self.bg_img = pygame.image.load('assets/terrain/bg.png')
        self.bg_img = pygame.transform.scale(self.bg_img, (WIDTH, HEIGHT))
        self.world = World(world_map, self.screen)
    
    def update_bg_image(self, width, height):
        self.bg_img = pygame.transform.scale(pygame.image.load('assets/terrain/bg.png'), (width, height))

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
                    self.world = World(world_map, self.screen)  # Update the world for new screen size
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
            self.world.update(self.player_event)
            game_cursor()
            pygame.display.update()
            self.clock.tick(70)

# Menu code
def set_difficulty(value, difficulty):
    pass  # Implement difficulty setting here

def start_the_game():
    game = Game(screen, WIDTH, HEIGHT)
    game.main()

# Initialize the menu
menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == "__main__":
    menu.mainloop(screen)