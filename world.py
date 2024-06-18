import pygame
from enemy import Ghost, Lava

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("decoding your fears: Clara's path")

# variáveis de jogo
tile_size = 40

#carregamento de imagens
bg_img = pygame.image.load('assets/background.jpg')

#inimigos
ghost_group = pygame.sprite.Group()
lava_group= pygame.sprite.Group()

class World():
	def __init__(self, data): #
		self.tile_list = []
		dirt_img = pygame.image.load('assets/ground_dirt.png')
		grass_img= pygame.image.load('assets/ground2.png')
		rectTransp=pygame.image.load('assets/rectTransp.png')
		
		#Percorremos a matriz de posições world_data para desenhar objetos pertinentes na tela
		row_count = 0 
		for row in data:
			col_count = 0
			for tile in row:
		
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect() 
					img_rect.x = col_count * tile_size  
					img_rect.y = row_count * tile_size 
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					ghost = Ghost(col_count * tile_size, row_count * tile_size)
					ghost_group.add(ghost)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size//2))
					lava_group.add(lava)
				if tile==10:
					img= pygame.transform.scale(rectTransp, (tile_size, tile_size))
					img_rect = img.get_rect() 
					img_rect.x = col_count * tile_size  
					img_rect.y = row_count * tile_size 
					tile = (img, img_rect)
					self.tile_list.append(tile)
				col_count += 1
			row_count += 1

	def draw(self): #Desenha o mundo e objetos/inimigos que estejam neste mundo
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
		ghost_group.update()
		ghost_group.draw(screen)
		lava_group.update()
		lava_group.draw(screen)
		
		
			
	def update(self): #Atualiza a tela para manter a imagem de fundo 
		screen.blit(bg_img, (0, -25))
		

