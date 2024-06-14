import pygame

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'assets/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            self.images_right.append(img_right)

        self.image = self.images_right[self.index]     
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0 
        self.jumped = False
    
    def update(self, screen, screen_height):
        dx = 0
        dy = 0
        walk_cooldown = 20

        # get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped:
            self.vel_y = -12
            self.jumped = True
        if not key[pygame.K_SPACE]:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1

        # adiciona gravidade
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # manipular a animação
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                    self.index = 0
            self.image = self.images_right[self.index]

        # checando a colisão

        # atualiza as coordenadas do player
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.vel_y = 0

        # coloca o player na tela
        screen.blit(self.image, self.rect)
