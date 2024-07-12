import pygame, sys
from settings import *
from world import World
from button import ImageButton

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
pygame.mixer.music.load("sounds/ColorfulFlowers.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

pygame.display.set_caption("Menu test")
main_background = pygame.image.load("assets/terrain/bg.png")

#ТЕСТ МЕНЮ

def main_menu():
    start_button = ImageButton(WIDTH/2-(252/2), 100, 90, 25,"Играть", "assets/buttons/button0.png", "assets/buttons/button1.png", "sounds/click.mp3")
    #settings_button = ImageButton(WIDTH/2-(252/2), 100, 90, 25,"Настройки", "assets/buttons/button0.png", "assets/buttons/button1.png", )
    exit_button = ImageButton(WIDTH/2-(252/2), 100, 90, 25,"Выйти", "assets/buttons/button0.png", "assets/buttons/button1.png", "sounds/click.mp3")

    running = True
    while running:
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

        screen.fill((0, 0, 0))
        screen.blit(main_background)

        font = pygame.font.Font(None, 72)
        text_surface = font.render("MENU TEST", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH/2,100))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.USEREVENT and event.button == exit_button:
                print("Кнопка 'Выйти' была нажата!")
                running = False
                pygame.quit()
                sys.exit()

            for btn in [start_button, exit_button]:
                btn.handle_event(event)

        for btn in [start_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()
#ТЕСТ МЕНЮ