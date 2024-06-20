import pygame
from enemy import Ghost, Lava


pygame.mixer.init()

enemy_collide_sound = pygame.mixer.Sound('assets/enemy.ogg')
enemy_collide_sound.set_volume(0.1)
lava_collide_sound = pygame.mixer.Sound('assets/lava.ogg')
lava_collide_sound.set_volume(0.1)
coin_collide_sound = pygame.mixer.Sound('assets/coin.ogg')
coin_collide_sound.set_volume(0.1)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.score = 0  # Inicializa o score do jogador
        for num in range(1, 4):
            img_right = pygame.image.load(f'assets/girl{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        
        self.dead_image = pygame.image.load('assets/dead.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.jump_count = 0
        self.direction = 0

    def update(self, screen, screen_height, world, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        player_score = 0  # Inicializa a pontuação do jogador neste método

        # Pega os comandos das teclas
        key = pygame.key.get_pressed()
        if game_over == 0:
            if key[pygame.K_SPACE]:
                if not self.jumped and self.jump_count < 2:
                    self.vel_y = -12
                    self.jumped = True
                    self.jump_count += 1
            else:
                self.jumped = False

            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Adiciona gravidade
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Manipular a animação
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Checando a colisão
            for tile in world.tile_list:
                # Checando a colisão na direção x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Checando a colisão na direção y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.jump_count = 0  # Reseta o contador de pulos ao tocar o chão

                # Checando colisão com inimigos
                #checando colisão com inimigos
                if pygame.sprite.spritecollide(self, world.ghost_group, False):
                    enemy_collide_sound.play()
                    game_over = -1
                    print(game_over)

                # Checando colisão com lava
                if pygame.sprite.spritecollide(self, world.lava_group, False):
                    lava_collide_sound.play()
                    game_over = -1
                    print(game_over)

            # Checando a colisão com moedas
            coin_collision_list = pygame.sprite.spritecollide(self, world.coin_group, True)
            if coin_collision_list:
                coin_collide_sound.play()
                player_score = len(coin_collision_list)  # Atualiza o player_score com o número de moedas coletadas
                self.score += player_score  # Atualiza o score total do jogador com a pontuação do último update

        # Atualiza as coordenadas do player
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.vel_y = 0
            self.jump_count = 0  # Reseta o contador de pulos ao tocar o fundo da tela

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        # coloca o player na tela
        screen.blit(self.image, self.rect)

        # Retorna tanto o estado do jogo quanto a pontuação do jogador
        return game_over, player_score
