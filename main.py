import pygame
import sys
import pygame_menu
from settings import *
from world import World
from enemy import Enemy
from player import Player
from clouds import CloudManager

# Initialize Pygame
pygame.init()

# Initialize the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Mayor Grom: the game")

# Load and play background music
pygame.mixer.music.load("sounds/ColorfulFlowers.mp3")
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
        self.font = pygame.font.SysFont(None, 36)  # Initialize font

        # Load assets and create managers
        self.bg_img = self.load_background(width, height)
        self.cloud_manager = self.create_cloud_manager()
        self.player = Player(pos=(55, 400))
        self.enemy = Enemy(pos=(90, 400))

        # Add entities to the world
        self.world.add(self.enemy)

        self.last_width = width

    def load_background(self, width, height):
        """Load and scale background image."""
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player_event = "left"
                elif event.key == pygame.K_RIGHT:
                    self.player_event = "right"
                elif event.key == pygame.K_SPACE:
                    self.player_event = "jump"
            elif event.type == pygame.KEYUP:
                self.player_event = None

    def main(self):
        """Main game loop."""
        while True:
            self.handle_events()

            # Draw background, clouds, and game elements
            self.screen.blit(self.bg_img, (0, 0))
            self.cloud_manager.update()
            self.player.update(self.player_event)
            self.enemy.update()

            # Update and draw the world
            self.world.update(self.player_event)
            self.world.draw(self.screen)

            # Display player lives and custom cursor
            self.show_life()
            game_cursor()

            pygame.display.update()
            self.clock.tick(60)  # Reduced to 60 FPS for consistency

# Menu code...
def set_difficulty(value, difficulty):
    """Placeholder function to set difficulty."""
    pass  # Implement difficulty setting here

def start_the_game():
    """Start the game when the 'Play' button is clicked."""
    game = GameMain(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    game.main()

# Initialize menu with custom background
myimage = pygame_menu.baseimage.BaseImage(
    image_path="assets/menu_background.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
)

# Configure theme with custom background image, underline title, left alignment, 8-bit font, and title font
mytheme = pygame_menu.themes.THEME_BLUE.copy()
mytheme.background_color = myimage
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE  # Underline style
mytheme.widget_alignment = pygame_menu.locals.ALIGN_LEFT  # Align widgets to the left
mytheme.widget_font = pygame_menu.font.FONT_8BIT  # Set 8-bit font for widgets
mytheme.title_font = pygame_menu.font.FONT_8BIT  # Set 8-bit font for the title
mytheme.title_background_color = (0, 0, 0)  # Set title background color to black (or any other color you like)

# Create menu
menu = pygame_menu.Menu(
    'Mayor Grom: the game', 
    700, 500, 
    theme=mytheme
)

menu.add.text_input('Nickname :', default='Тоши')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == "__main__":
    menu.mainloop(screen)