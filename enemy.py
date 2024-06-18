import pygame
from abc import ABC, abstractmethod

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
	def __init__(self, x, y):
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
	
		