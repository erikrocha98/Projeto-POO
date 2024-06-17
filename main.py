import pygame
from pygame.locals import *
from player import Player
from button import Button

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("decoding your fears: Clara's path")

# game variables
tile_size = 40
main_menu = True

# load images
bg_img = pygame.image.load('assets/background_start.png')
startbtn_img = pygame.image.load('assets/start.png')
exitbtn_img = pygame.image.load('assets/exit.png')
music_on_img = pygame.image.load('assets/music_on.png')
music_off_img = pygame.image.load('assets/music_off.png')

# load sounds
pygame.mixer.music.set_volume(0.5)
bg_sound = pygame.mixer.music.load('assets/desafio.mp3')
pygame.mixer.music.play(-1)

button_sound = pygame.mixer.Sound('assets/botao.wav')
button_sound.set_volume(0.2)

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

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, screen_height - 130)
world = World(world_data)

#create buttons
start_button = Button(screen_width // 2 - 90, screen_height // 2 , startbtn_img)
exit_button = Button(screen_width // 2 - 90, screen_height // 2 + 60, exitbtn_img)
music_on_button = Button(screen_width // 2 - 40, screen_height // 2 + 120, music_on_img)
music_off_button = Button(screen_width // 2 + 15, screen_height // 2 + 120, music_off_img)


running = True
while running:
	clock.tick(fps)
	screen.blit(bg_img, (0, -25))
	
	if main_menu == True:
		if exit_button.drawbutton():
			button_sound.play()
			running = False
		if start_button.drawbutton():
			button_sound.play()
			pygame.mixer.music.fadeout(1)
			pygame.mixer.music.stop()
			pygame.mixer.music.set_volume(0.1)
			pygame.mixer.music.load('assets/level1.mp3')  # Carregar a nova música
			pygame.mixer.music.play(-1)
			main_menu = False
			bg_img = pygame.image.load('assets/background.jpg')
		if music_on_button.drawbutton():
			button_sound.play()
			pygame.mixer.music.play(-1)
		if music_off_button.drawbutton():
			button_sound.play()
			pygame.mixer.music.stop()

	else:
		world.draw()
	
		music_on_button = Button(screen_width // 2 + 350, screen_height // 2 + 270, music_on_img)
		music_off_button = Button(screen_width // 2 + 350, screen_height // 2 + 320, music_off_img)
		if music_on_button.drawbutton():
			pygame.mixer.music.play(-1)
		if music_off_button.drawbutton():
			pygame.mixer.music.stop()
	
		player.update(screen, screen_height, world)  # Passa 'world' como argumento para o método update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.display.update()

pygame.quit()
