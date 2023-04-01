import pygame

pygame.init()

display_w = 800
display_h = 600

display = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption('Forgotten Warrior')

icon = pygame.image.load('icons.png')
pygame.display.set_icon(icon)


def run_game():
    game = True

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill((255,255,255))
        pygame.display.update()

run_game()