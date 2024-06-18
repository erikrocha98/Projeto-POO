import pygame
from enemy import Ghost
from world import World

world= World

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
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
		self.jump_count = 0  # Conta o número de pulos
		self.direction = 0
	
	def update(self, screen, screen_height, world, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 5

		if game_over == 0:
			#pega o comando das teclas
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped==False:
				self.vel_y = -12
				self.jumped = True
			if key[pygame.K_SPACE]==False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] ==False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

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
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

			# checando a colisão
			for tile in world.tile_list:
				#checando a colisão na direção x
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#checanodo a colisão na direção y
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top

				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					if self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom

			#check for collision with enemies
				if pygame.sprite.spritecollide(self, world.ghost_group, False):
					game_over = -1
					print(game_over)

				#check for collision with lava
				if pygame.sprite.spritecollide(self, world.lava_group, False):
					game_over = -1
					print(game_over)

			# atualiza as coordenadas do player
			self.rect.x += dx
			self.rect.y += dy

			if self.rect.bottom > screen_height:
				self.rect.bottom = screen_height
				self.vel_y = 0

		elif game_over == -1:
			self.image = self.dead_image
			if self.rect.y > 200:
				self.rect.y -= 5
		# coloca o player na tela
		screen.blit(self.image, self.rect)

		return game_over
		
