# ghost.py
import pygame
import random
import time
from settings import WIDTH, CHAR_SIZE, GHOST_SPEED

class Ghost(pygame.sprite.Sprite):
	def __init__(self, row, col, color):
		super().__init__()
		self.abs_x = (row * CHAR_SIZE)
		self.abs_y = (col * CHAR_SIZE)

		self.rect = pygame.Rect(self.abs_x, self.abs_y, CHAR_SIZE, CHAR_SIZE)
		self.move_speed = GHOST_SPEED

		# self.color = pygame.Color(color)
		self.color = color
		
		self.move_directions = [(-1,0), (0,-1), (1,0), (0,1)]

		self.moving_dir = "up"

		self.img_path = f'assets/ghosts/{color}/'
		self.img_name = f'{self.moving_dir}.png'
		self.image = pygame.image.load(self.img_path + self.img_name)
		self.image = pygame.transform.scale(self.image, (CHAR_SIZE, CHAR_SIZE))
		
		self.mask = pygame.mask.from_surface(self.image)

		self.directions = {'left': (-self.move_speed, 0), 'right': (self.move_speed, 0), 'up': (0, -self.move_speed), 'down': (0, self.move_speed)}
		self.keys = ['left', 'right', 'up', 'down']
		self.direction = (0, 0)

		self.weak_time = 0
		self.weak = False
		self.respawning = False
		self.respawn_timer = 0
	

	def move_to_start_pos(self):
		self.rect.x = self.abs_x
		self.rect.y = self.abs_y

	def is_collide(self, x, y, walls_collide_list):
		tmp_rect = self.rect.move(x, y)
		if tmp_rect.collidelist(walls_collide_list) == -1:
			return False
		return True

	def _animate(self):
		if self.weak:
			# self.img_name = ""
			weak_color = "white" if self.color in ["pink", "orange"] else "blue"
			
			# Flashing effect in the last 30 frames of weak mode
			if self.weak_time < 30 and self.weak_time % 10 < 5:
				 # Flash back to normal appearance
				self.img_path = f'assets/ghosts/{self.color}/'
				self.img_name = f'{self.moving_dir}.png'
			else:
				# Weak state sprite (white or blue based on ghost color)
				self.img_path = f'assets/ghosts/power_down/{weak_color}.png'
				self.img_name = ""  # No directional sprite for weak form
		else:
			self.img_path = f'assets/ghosts/{self.color}/'
			self.img_name = f'{self.moving_dir}.png'
		
		self.image = pygame.image.load(self.img_path + self.img_name)
		self.image = pygame.transform.scale(self.image, (CHAR_SIZE, CHAR_SIZE))
		self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

	def update(self, walls_collide_list):
		if self.respawning:
			self.respawn_timer -= 1
			if self.respawn_timer <= 0:
				self.move_to_start_pos()
				self.respawning = False
				self.weak = False
				self.weak_time = 0
			return
	
		# ghost movement
		available_moves = []
		for key in self.keys:
			if not self.is_collide(*self.directions[key], walls_collide_list):
				available_moves.append(key)
		
		randomizing = False if len(available_moves) <= 2 and self.direction != (0,0) else True
		# 60% chance of randomizing ghost move
		if randomizing and random.randrange( 0,100 ) <= 60:
			self.moving_dir = random.choice(available_moves)
			self.direction = self.directions[self.moving_dir]

		if not self.is_collide(*self.direction, walls_collide_list):
			self.rect.move_ip(self.direction)
		else:
			self.direction = (0,0)

		# teleporting to the other side of the map
		if self.rect.right <= 0:
			self.rect.x = WIDTH
		elif self.rect.left >= WIDTH:
			self.rect.x = 0

		self.weak = True if self.weak_time > 0 else False
		self.weak_time -= 1 if self.weak_time > 0 else 0

		self._animate()