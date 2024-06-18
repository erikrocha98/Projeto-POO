import pygame
from pygame.locals import *
from player import Player
from world import World
from button import Button



pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("decoding your fears: Clara's path")

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


world_data = [
[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 10], 
[10, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 2], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 10], 
[10, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10], 
[2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 10], 
[10, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10], 
[10, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2], 
[10, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[10, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[10, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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
