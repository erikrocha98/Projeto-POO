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

# uteis para entrada de texto
base_font = pygame.font.Font(None, 30)
user_text = ''
input_rect = pygame.Rect(screen_width // 2 - 90, screen_height // 2 - 2, 175, 45)
input_rect2 = pygame.Rect(screen_width // 2 - 92, screen_height // 2 - 5, 180, 50)
rect_color = (80, 80, 80)

active = False
nickname_entered = False
main_menu = True
game_over=0

# load images
bg_img = pygame.image.load('assets/background_start.png')
startbtn_img = pygame.image.load('assets/start.png')
exitbtn_img = pygame.image.load('assets/exit.png')
submitbtn_img = pygame.image.load('assets/submit.png')
music_on_img = pygame.image.load('assets/music_on.png')
music_off_img = pygame.image.load('assets/music_off.png')
restartbtn_img = pygame.image.load('assets/restart.png')

# load sounds
pygame.mixer.music.set_volume(0.5)
bg_sound = pygame.mixer.music.load('assets/desafio.mp3')
pygame.mixer.music.play(-1)

button_sound = pygame.mixer.Sound('assets/botao.wav')
button_sound.set_volume(0.2)

world_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 10], 
[10, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 2], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 10], 
[10, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10], 
[2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 10], 
[10, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 10], 
[10, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10], 
[10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2], 
[10, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[10, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[10, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, screen_height - 130)
world = World(world_data)

#create buttons
start_button = Button(screen_width // 2 - 98, screen_height // 2 - 5, startbtn_img)
exit_button = Button(screen_width // 2 - 98, screen_height // 2 + 55, exitbtn_img)
submit_button = Button(screen_width // 2 - 20, screen_height // 2 + 50, submitbtn_img)
music_on_button = Button(screen_width // 2 + 350, screen_height // 2 + 270, music_on_img)
music_off_button = Button(screen_width // 2 + 350, screen_height // 2 + 320, music_off_img)
restart_button = Button(screen_width // 2 - 98, screen_height // 2, restartbtn_img)

running = True
while running:
	clock.tick(fps)
	screen.blit(bg_img, (0, -25))

	if main_menu == True:
		if not nickname_entered:
			if start_button.drawbutton():
				button_sound.play()
				nickname_entered = True
			if exit_button.drawbutton():
				button_sound.play()
				running = False
			
		else:
			pygame.draw.rect(screen, (200, 200, 200), input_rect, 0, 90)
			pygame.draw.rect(screen, rect_color, input_rect2, 5, 90)
			text_surface = base_font.render(user_text, True, (0, 0, 0))
			screen.blit(text_surface, (input_rect.x + 15, input_rect.y + 12))

			if submit_button.drawbutton():
				button_sound.play()
				main_menu = False
				# Carregar a nova música
				pygame.mixer.music.stop()
				pygame.mixer.music.set_volume(0.1)
				pygame.mixer.music.load('assets/level1.mp3')
				pygame.mixer.music.play(-1)
				bg_img = pygame.image.load('assets/background.jpg')

	else: 
		world.draw()
		world.draw_enemies()

		if game_over==0:
			world.update_enemies()

		game_over = player.update(screen, screen_height, world, game_over)  # Passa 'world' como argumento para o método update()

		if game_over == -1:
			pygame.mixer.music.stop()
			if restart_button.drawbutton():
				button_sound.play()
				player = Player(100, screen_height - 130)  # Reseta o jogador
				world = World(world_data)  # Reseta o mundo
				game_over = 0
				pygame.mixer.music.play(-1)

	if music_on_button.drawbutton():
		button_sound.play()
		pygame.mixer.music.play(-1)
	if music_off_button.drawbutton():
		button_sound.play()
		pygame.mixer.music.stop()	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			if input_rect.collidepoint(event.pos):
				active = True
				rect_color = (56, 56, 56)
			else:
				active = False
				rect_color = (70, 110, 119)

		if event.type == pygame.KEYDOWN:
			if active and nickname_entered:
				if event.key == pygame.K_BACKSPACE:
					user_text = user_text[:-1]
				else:
					# Limitar o tamanho do texto ao tamanho do retângulo
					if base_font.size(user_text + event.unicode)[0] < input_rect.width - 20:
						user_text += event.unicode

	pygame.display.update()

pygame.quit()
