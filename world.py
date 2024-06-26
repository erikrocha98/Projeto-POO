import pygame
from enemy import Ghost, Lava
from portal import Portal
from coin import Coin

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("decoding your fears: Clara's path")

# variáveis de jogo
tile_size = 40

# carregamento de imagens
bg_img = pygame.image.load('assets/background.jpg')

class World():
    def __init__(self, data, portal_group, coin_group):  # Adicionado parâmetro portal_group
        self.tile_list = []
        self.portal_positions = []
        dirt_img = pygame.image.load('assets/ground_dirt.png')
        grass_img = pygame.image.load('assets/ground2.png')
        rectTransp = pygame.image.load('assets/rectTransp.png')
        self.ghost_group = pygame.sprite.Group()
        self.lava_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.portal_group = portal_group  # Armazena portal_group no objeto
        
        # Percorremos a matriz de posições world_data para desenhar objetos pertinentes na tela
        for row_count, row in enumerate(data):
            for col_count, tile in enumerate(row):
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size  
                    img_rect.y = row_count * tile_size 
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 3:
                    ghost = Ghost(col_count * tile_size, row_count * tile_size)
                    self.ghost_group.add(ghost)
                elif tile == 4:  # Portal tile
                    portal = Portal(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    self.portal_group.add(portal)  # Adiciona o portal ao grupo portal_group
                    self.portal_positions.append((col_count * tile_size, row_count * tile_size - (tile_size // 2)))
                elif tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    self.lava_group.add(lava)
                elif tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    self.coin_group.add(coin)
                elif tile == 10:
                    img = pygame.transform.scale(rectTransp, (tile_size, tile_size))
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * tile_size  
                    img_rect.y = row_count * tile_size 
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
    
    def get_coin_positions(self):
        coin_positions = []
        for coin in self.coin_group:
            coin_positions.append((coin.rect.x, coin.rect.y))
        return coin_positions

    def update_enemies(self):  # Atualiza os inimigos e objetos no mundo
        self.ghost_group.update()
        self.lava_group.update()

    def get_portal_positions(self):
        return self.portal_positions

    def get_tile_list(self):
        return self.tile_list
