import pygame_menu
import pygame
from game import Game

pygame.init()

screen = pygame.display.set_mode((700, 500), pygame.RESIZABLE)

selected_difficulty = 'Easy'
player_name = None

def set_difficulty(value, difficulty):
    global selected_difficulty
    selected_difficulty = difficulty


def start_the_game():
    game = Game(screen)
    game.main()


myimage = pygame_menu.baseimage.BaseImage(
    image_path="assets/menu_background.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
)

mytheme = pygame_menu.themes.THEME_BLUE.copy()
mytheme.background_color = myimage
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE
mytheme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
mytheme.widget_font = pygame_menu.font.FONT_8BIT
mytheme.title_font = pygame_menu.font.FONT_8BIT
mytheme.title_background_color = (0, 0, 0)

menu = pygame_menu.Menu(
    'Mayor Grom: the game', 
    700, 500, 
    theme=mytheme
)

player_name = menu.add.text_input('Name :', default='your name here!')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

def run_menu():
    menu.mainloop(screen)

