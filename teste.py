import pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Teste Pygame')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    pygame.display.flip()
pygame.quit()