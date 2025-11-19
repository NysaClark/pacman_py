# display.py
import pygame
from settings import WIDTH, HEIGHT, CHAR_SIZE, NAV_HEIGHT

pygame.font.init()

class Display:
	def __init__(self, screen):
		self.screen = screen
		# self.font = pygame.font.SysFont("ubuntumono", CHAR_SIZE)
		self.font = pygame.font.Font("assets/fonts/Tiny5-Regular.ttf", 26)
		self.game_over_font = pygame.font.SysFont("dejavusansmono", 48)
		self.text_color = pygame.Color("white")

	def show_top_nav(self, level, player_score, high_score, y_pos_top=0, y_pos_bottom=CHAR_SIZE):
		level_label = self.font.render(f'LVL {level}', True, self.text_color)
		highscore_label = self.font.render('HIGH SCORE', True, self.text_color)
		self.screen.blit(level_label, (5, y_pos_top))  # left
		self.screen.blit(highscore_label, ((WIDTH // 2) - (highscore_label.get_width() // 2 ), y_pos_top))  # center

        # Row 2: numeric scores
		player_score_text = self.font.render(f'{player_score:02d}', True, self.text_color)
		highscore_text = self.font.render(f'{high_score:04d}', True, self.text_color)
		self.screen.blit(player_score_text, (5, y_pos_bottom))  # left, under LEVEL
		self.screen.blit(highscore_text, ((WIDTH // 2) - (highscore_text.get_width() // 2), y_pos_bottom))  # center
					
	def show_life(self, life, y_pos):
		life_image = pygame.image.load("assets/life/life.png")
		life_image = pygame.transform.scale(life_image, (CHAR_SIZE, CHAR_SIZE))
		life_x = CHAR_SIZE // 2
		for _ in range(life):
			self.screen.blit(life_image, (life_x, y_pos))
			life_x += CHAR_SIZE

	def show_food(self, eaten_food, y_pos):
		food_x = WIDTH - CHAR_SIZE // 2 - CHAR_SIZE # start from right
		for food in eaten_food:
			food_image = pygame.image.load(f"assets/food/{food}.png")
			food_image = pygame.transform.scale(food_image, (CHAR_SIZE, CHAR_SIZE))
	 
			self.screen.blit(food_image, (food_x, y_pos))
			food_x -= CHAR_SIZE

	# add game over message
	def game_over(self):
		message = self.font.render("GAME OVER!!", True, pygame.Color("firebrick1"))
		message_rect = message.get_rect(center=(WIDTH // 2, NAV_HEIGHT + HEIGHT // 2 + CHAR_SIZE))
		self.screen.blit(message, message_rect)

		instruction = self.font.render('"R" TO RESTART', True, pygame.Color("dodgerblue2"))
		instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT // 2 - CHAR_SIZE))
		self.screen.blit(instruction, instruction_rect)