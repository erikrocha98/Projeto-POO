import pygame
from abc import ABC, abstractmethod

# variáveis de jogo
tile_size = 40
class Enemy(ABC):
	
	@abstractmethod
	def update(self)-> None:
		pass
	""" @abstractmethod
	def atack(self)-> None:
		pass """
	""" @abstractmethod
	def update(self)-> None:
		pass
 """
class Ghost(Enemy, pygame.sprite.Sprite):
	def __init__(self, x, y)-> None:
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('assets/ghost.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0
		
	def update (self)->None: #Implementa animação simples para o fantasma
		
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1
class Lava(Enemy, pygame.sprite.Sprite):
	def __init__(self,x,y) -> None:
		pygame.sprite.Sprite.__init__(self)
		self.frames = []
		for num in range(1, 5):
			img = pygame.image.load(f'assets/lava{num}.png')
			img = pygame.transform.scale(img, (tile_size, tile_size // 1.2))
			self.frames.append(img)
		self.current_frame = 0
		self.image = self.frames[self.current_frame]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self) -> None:
		self.current_frame = (self.current_frame + 1) % len(self.frames)
		self.image = self.frames[self.current_frame]