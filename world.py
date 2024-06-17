import pygame

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("decoding your fears: Clara's path")

# variáveis de jogo
tile_size = 40

#carregamento de imagens
bg_img = pygame.image.load('assets/background.jpg')


class World():
	def __init__(self, data): #
		self.tile_list = []
		dirt_img = pygame.image.load('assets/ground_dirt.png')
		grass_img= pygame.image.load('assets/ground2.png')

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
				col_count += 1
			row_count += 1

	def draw(self): #Percorre a lista de blocos para desenhar na tela cada um deles nas coordenadas salvas em img_rect
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			
	def update(self): #atualiza a tela para manter a imagem de fundo 
		screen.blit(bg_img, (0, -25))


def aumento(self):
	return 1+1