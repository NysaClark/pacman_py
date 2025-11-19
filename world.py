#world.py
import pygame
import time
import random

from settings import HEIGHT, WIDTH, NAV_HEIGHT, CHAR_SIZE, MAP, PLAYER_SPEED
from pac import Pac
from cell import Cell
from berry import Berry
from ghost import Ghost
from display import Display
from food import Food


class World:
	def __init__(self, screen):
		self.screen = screen
		self.map_surface = pygame.Surface((WIDTH, HEIGHT))

		self.player = pygame.sprite.GroupSingle()
		self.ghosts = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()
		self.berries = pygame.sprite.Group()
		self.foods = pygame.sprite.Group()

		self.display = Display(self.screen)

		self.game_over = False
		self.reset_pos = False
		self.first_move_done = False
		self.player_score = 0
		self.game_level = 1
		self.spawned_food = 0
		self.curr_food_count = 0
		self.eaten_food = []
		self.high_score = 0


		self._generate_world()


	# create and add player to the screen
	def _generate_world(self):
		self.gate_tiles = []
		# renders obstacle from the MAP table
		for y_index, col in enumerate(MAP):
			for x_index, char in enumerate(col):
				if char == "1":	# for walls
					self.walls.add(Cell(x_index, y_index, CHAR_SIZE, CHAR_SIZE))
				elif char == " ":	 # for paths to be filled with berries
					self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 8))
				elif char == "B":	# for big berries
					self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 3, is_power_up=True))

				# for Ghosts's starting position
				elif char == "s":
					self.ghosts.add(Ghost(x_index, y_index, "skyblue"))
				elif char == "p": 
					self.ghosts.add(Ghost(x_index, y_index, "pink"))
				elif char == "o":
					self.ghosts.add(Ghost(x_index, y_index, "orange"))
				elif char == "r":
					self.ghosts.add(Ghost(x_index, y_index, "red"))

				elif char == "-":
					gate = Cell(x_index, y_index, CHAR_SIZE, CHAR_SIZE)
					self.walls.add(gate)
					self.gate_tiles.append(gate)

				elif char == "P":	# for PacMan's starting position 
					self.player.add(Pac(x_index, y_index))

		self.walls_collide_list = [wall.rect for wall in self.walls.sprites()]


	def generate_new_level(self):
		self.first_move_done = False
		self.gate_tiles = []

		for y_index, col in enumerate(MAP):
			for x_index, char in enumerate(col):
				if char == " ":	 # for paths to be filled with berries
					self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 8))
				elif char == "B":	# for big berries
					self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 3, is_power_up=True))
				elif char == "-":
					gate = Cell(x_index, y_index, CHAR_SIZE, CHAR_SIZE)
					self.walls.add(gate)
					self.gate_tiles.append(gate)
		self.walls_collide_list = [wall.rect for wall in self.walls.sprites()]
		time.sleep(2)
		

	def restart_game(self):
		[food.kill() for food in self.foods.sprites()]

		self.game_level = 1
		self.first_move_done = False
		self.spawned_food = 0
		self.curr_food_count = 0
		self.eaten_food = []

		self.player.sprite.pac_score = 0
		self.player.sprite.life = 3
		self.player.sprite.move_to_start_pos()
		self.player.sprite.direction = (0, 0)
		self.player.sprite.status = "idle"
		

		for ghost in self.ghosts.sprites():
			ghost.move_to_start_pos()
			ghost.weak_time = 0
			ghost.weak = False
			ghost.respawing = False
			ghost.respawn_time = 0
		
		
		self.generate_new_level()


	# displays nav
	def _dashboard(self):
	
		# top nav
		top_nav_rect = pygame.Rect(0, 0, WIDTH, NAV_HEIGHT)
		pygame.draw.rect(self.screen, pygame.Color("black"), top_nav_rect)
		self.display.show_top_nav(
			level=self.game_level,
			player_score=self.player.sprite.pac_score,
			high_score=self.high_score,
			y_pos_top=5,
			y_pos_bottom=CHAR_SIZE-5
    	)
		# Bottom nav
		bottom_nav_rect = pygame.Rect(0, NAV_HEIGHT + HEIGHT, WIDTH, NAV_HEIGHT)
		pygame.draw.rect(self.screen, pygame.Color("black"), bottom_nav_rect)
		self.display.show_life(self.player.sprite.life, y_pos=NAV_HEIGHT + HEIGHT + CHAR_SIZE // 2)
		self.display.show_food(self.eaten_food, y_pos=NAV_HEIGHT + HEIGHT + CHAR_SIZE // 2)
	

	def _check_game_state(self):
		# checks if game over
		if self.player.sprite.life == 0:
			self.game_over = True

		# generates new level
		if len(self.berries) == 0 and self.player.sprite.life > 0:
			self.game_level += 1
			self.first_move_done = False
			self.eaten_food = []
			
			for ghost in self.ghosts.sprites():
				ghost.move_speed += (self.game_level - 1)
				ghost.move_to_start_pos()
				ghost.weak_time = 0
				ghost.weak = False
				ghost.respawing = False
				ghost.respawn_time = 0

			[food.kill() for food in self.foods.sprites()]
			self.spawned_food = 0
			self.curr_food_count = 0

			self.player.sprite.move_to_start_pos()
			self.player.sprite.direction = (0, 0)
			self.player.sprite.status = "idle"
			
			self.generate_new_level()


	def spawn_food(self):
		# Determine number of food for this level
		# max_food = self.game_level
		max_food = self.game_level if self.game_level < 7 else 7
		# max_food = self.game_level + 1

		if self.spawned_food >= max_food:
			return
		
		# Get all possible positions (all cells without walls, berries, or ghosts)
		possible_positions = []
		for y, col in enumerate(MAP):
			for x, char in enumerate(col):
				x_pos = x * CHAR_SIZE
				y_pos = y * CHAR_SIZE
				rect = pygame.Rect(x_pos, y_pos, CHAR_SIZE, CHAR_SIZE)
            	
				if char == " " and not any(
                    rect.colliderect(sprite.rect)
                    for sprite in self.walls.sprites() + self.ghosts.sprites()
                ):
					possible_positions.append((y, x))
    
		if not possible_positions:
			return 
		
		# spawn 1 food @ random position
		row, col = random.choice(possible_positions)

		# TODO randomize food type
		food_types = ["cherry", "strawberry", "orange", "pretzel", "apple", "pear", "banana"]
		type_points = [100, 200, 500, 700, 1000, 2000, 5000]
		type_max = self.game_level-1 if self.game_level < 7 else 6
		# lvl 1: cherry	 	0 
		# lvl 2: c, sb 		0 - 1
		# lvl 3: c, sb, o	0 - 2
		# etc...
		# lvl 7+: all foods 0 - 6 
		random_int = random.randint(0, type_max)
		print(f"Food random int(0 - {type_max}) = {random_int}")
		self.foods.add(Food(row, col, type=food_types[random_int], points=type_points[random_int]))
		
		self.spawned_food +=1
		self.curr_food_count +=1

	def update(self):
		if not self.game_over:
			# player movement
			pressed_key = pygame.key.get_pressed()

			if not self.first_move_done:
				if pressed_key[pygame.K_UP] or pressed_key[pygame.K_DOWN] or pressed_key[pygame.K_LEFT] or pressed_key[pygame.K_RIGHT]:
					self.first_move_done = True
					
					for gate in self.gate_tiles:
						self.walls.remove(gate)
					self.walls_collide_list = [wall.rect for wall in self.walls.sprites()]
			
			self.player.sprite.animate(pressed_key, self.walls_collide_list)

			# teleporting to the other side of the map
			if self.player.sprite.rect.right <= 0:
				self.player.sprite.rect.x = WIDTH
			elif self.player.sprite.rect.left >= WIDTH:
				self.player.sprite.rect.x = 0

			# PacMan eating-berry effect
			for berry in self.berries.sprites():
				if self.player.sprite.rect.colliderect(berry.rect):
					if berry.power_up:
						for ghost in self.ghosts.sprites():
							ghost.weak_time = 150 # Timer based from FPS count
							ghost.weak = True
						self.player.sprite.pac_score += 50
					else:
						self.player.sprite.pac_score += 10

					# Update high score immediately
					if self.player.sprite.pac_score > self.high_score:
						self.high_score = self.player.sprite.pac_score
					
					berry.kill()

			# pac eating-food effect
			for food in self.foods.sprites():
				if self.player.sprite.rect.colliderect(food.rect):
					self.player.sprite.pac_score += food.points
					# Update high score immediately
					if self.player.sprite.pac_score > self.high_score:
						self.high_score = self.player.sprite.pac_score
					self.curr_food_count -= 1
					self.eaten_food.append(food.type)
					food.kill()

			if self.first_move_done and self.curr_food_count == 0:
				# Random dynamic food spawning
				if random.randint(0, 1000) < 6:
					self.spawn_food()



			# PacMan bumping into ghosts
			for ghost in self.ghosts.sprites():
				if self.player.sprite.rect.colliderect(ghost.rect):
					if not ghost.weak:
						time.sleep(2)
						self.player.sprite.life -= 1
						self.reset_pos = True
						break
					else:
						ghost.respawning = True
						ghost.respawn_timer = 80
						ghost.weak_time = 0
						
						self.player.sprite.pac_score += 200
						# Update high score immediately
						if self.player.sprite.pac_score > self.high_score:
							self.high_score = self.player.sprite.pac_score

		self._check_game_state()

		

		# rendering
		# Clear map surface
		self.map_surface.fill(pygame.Color("black"))

		[wall.update(self.map_surface) for wall in self.walls.sprites()]
		[berry.update(self.map_surface) for berry in self.berries.sprites()]
		[food.update(self.map_surface) for food in self.foods.sprites()]
		[ghost.update(self.walls_collide_list) for ghost in self.ghosts.sprites()]
		
		# self.ghosts.draw(self.screen)

		for ghost in self.ghosts.sprites():
			if not ghost.respawning:
				self.map_surface.blit(ghost.image, ghost.rect)

		self.foods.draw(self.map_surface)
		self.player.update()
		self.player.draw(self.map_surface)

		# Blit the map_surface onto the main screen (below top nav)
		self.screen.blit(self.map_surface, (0, NAV_HEIGHT))
		
		self.display.game_over() if self.game_over else None
		self._dashboard()

		# reset Pac and Ghosts position after PacMan get captured
		if self.reset_pos and not self.game_over:
			
			[food.kill() for food in self.foods.sprites()]
			
			self.player.sprite.move_to_start_pos()
			self.player.sprite.status = "idle"
			self.player.sprite.direction = (0,0)

			self.reset_pos = False

			for ghost in self.ghosts.sprites():
				ghost.weak_time = 0
				ghost.weak = False
				ghost.respawing = False
				ghost.respawn_time = 0
				ghost.move_to_start_pos()


		# for restart button
		if self.game_over:
			pressed_key = pygame.key.get_pressed()
			if pressed_key[pygame.K_r]:
				self.game_over = False
				self.restart_game()


# TODO add more food than cherries w/ increasing points
	# (strawberry, orange, pretzel, apple, pear, banana)
# TODO make ghosts smarter based on lvl