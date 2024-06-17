import pygame

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("decoding your fears: Clara's path")

# game variables
tile_size = 40

#load images
bg_img = pygame.image.load('assets/background.jpg')


class World():
	def __init__(self, data):
		self.tile_list = []
		dirt_img = pygame.image.load('assets/ground_dirt.png')
		grass_img= pygame.image.load('assets/ground2.png')

		row_count = 0 
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect() #turn the surface into an object
					img_rect.x = col_count * tile_size #avoid superposition of surfaces
					img_rect.y = row_count * tile_size #avoid superposition of surfaces
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

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			
	def update(self):
		screen.blit(bg_img, (0, -25))