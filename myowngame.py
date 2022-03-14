import pygame
import random
import sys
import time


pygame.font.init()
pygame.init()

# GLOBAL VARS AND CONSTANTS

play_width = 1200 # 1200 // 40 = 30
play_height = 600 # 600 // 20 = 30

grassX = 0
grassY = 120

platform_1_X = 120
platform_1_Y = 300

platform_2_X = 1200 - 30 * 8
platform_2_Y = platform_1_Y

platform_WIDTH = 180

vertical_platform_X = play_width // 2
vertical_platform_Y = play_height - 30 * 6

progress_bar_X = 60
progress_bar_Y = play_height - 30

block_size = 30
fall_speed = 10
jetpack_speed = 9

bonus_time = [1, 2, 3]
bonus_time_locations_x = []
bonus_time_locations_y = []

for i in range(0,play_width,block_size):
			bonus_time_locations_x.append(i)

for i in range(150,play_height - 90,block_size):
	bonus_time_locations_y.append(i)


block_colors = {'green' : (0,255,0),'brown': (150,75,0),'lightblue': (100,100,255),'black': (0,0,0),'white' : (255,255,255),'red' : (255,0,0)}

font = pygame.font.SysFont('Consolas', 80)

# PLAYER CLASS FOR PLAYER'S INTERACTIONS WITH PLATFORMS AND ITS GRAVITY, AND DRAWING IT 

class Player(object):
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color
		
		grassRect = pygame.Rect(grassX, play_height - grassY, play_width, grassY)
		self.grassRect = grassRect
		
		platformRect1 = pygame.Rect(platform_1_X, play_height - platform_1_Y, platform_WIDTH, block_size)
		self.platformRect1 = platformRect1
		
		platformRect2 = pygame.Rect(platform_2_X, play_height - platform_2_Y, platform_WIDTH, block_size)
		self.platformRect2 = platformRect2

		self.blocks = [self.grassRect, self.platformRect1, self.platformRect2]

		vertical_platform_rect = pygame.Rect(vertical_platform_X, play_height - vertical_platform_Y, block_size, play_height - vertical_platform_Y)
		self.vertical_platform_rect = vertical_platform_rect
		
		jetpack_fuel = 60
		self.jetpack_fuel = jetpack_fuel


	def draw(self, surface):
		playerRect = pygame.Rect(self.x, play_height - self.y, block_size, block_size)
		pygame.draw.rect(surface, self.color, playerRect)


	def gravity(self):
		playerRect = pygame.Rect(self.x, play_height - self.y, block_size, block_size)
		x = True

		for i in self.blocks:
			if i.colliderect(playerRect):
				x = False	
		if x:
			self.y -= fall_speed 


	def jump(self):
		if self.jetpack_fuel > 0:
			self.y += jetpack_speed
			self.jetpack_fuel -= 1
		else:
			self.gravity()


	def draw_progress_bar(self, surface):
		for i in range(self.jetpack_fuel):
			rect = pygame.Rect(progress_bar_X, play_height - progress_bar_Y, 18 * i, block_size)
			pygame.draw.rect(surface, (255 - i * 3 , 0 + i * 3, 0), rect)


	def draw_map(self, surface, bonus, time_left):
		surface.fill(block_colors['lightblue'])
		pygame.draw.rect(surface, block_colors['green'], self.grassRect)
		pygame.draw.rect(surface, block_colors['black'], self.platformRect1)
		pygame.draw.rect(surface, block_colors['black'], self.platformRect2)
		pygame.draw.rect(surface, block_colors['black'], self.vertical_platform_rect)

		bonusRect = pygame.Rect(bonus[0], play_height - bonus[1], block_size, block_size)
		pygame.draw.rect(surface, block_colors['brown'], bonusRect)
		self.draw_progress_bar(surface)

		text = str(time_left)
		win.blit(font.render(text, True, block_colors['black']), (play_width // 2, 60))


	def spawn_bonus(self):
		x = random.choice(bonus_time_locations_x)
		y = random.choice(bonus_time_locations_y)
		return [x,y]


	def check_bonus_collision(self, bonus):
		playerRect = pygame.Rect(self.x, play_height - self.y, block_size, block_size)
		bonusRect = pygame.Rect(bonus[0], play_height - bonus[1], block_size, block_size)

		if bonusRect.colliderect(playerRect):
			self.jetpack_fuel = 60
			return True
		return False


	def check_platform_collision(self):
		playerRect = pygame.Rect(self.x, play_height - self.y, block_size, block_size)

		if self.platformRect1.colliderect(playerRect) or self.platformRect2.colliderect(playerRect):
			return True
		
		return False


	def check_vertical_platform_collision(self):
		playerRect = pygame.Rect(self.x, play_height - self.y, block_size, block_size)

		return self.vertical_platform_rect.colliderect(playerRect)


def create_map_grid(locked_positions):
	grid = [[(0,0,0) for x in range(play_width // block_size)] for x in range(play_height // block_size)]

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if i == (play_height - grassY) // block_size:
				locked_positions.append([i,j])
	return grid


def draw_map_grid(surface, grid):
	for i in range(len(grid)):
		pygame.draw.line(surface, (128,128,128), (0, 0 + i*block_size), (0 + play_width, 0 + i*block_size))
		for j in range(len(grid[i])):
			pygame.draw.line(surface, (128,128,128), (0 + j * block_size, 0),(0 + j * block_size, 0 + play_height))


def check_lost(time):
	return time == 0


def draw_text_middle(surface, text, size, color):
	font = pygame.font.SysFont("comicsans", size, bold = True)
	label = font.render(text, 1, color)

	surface.blit(label, (play_width // 2 - (label.get_width()/2), play_height // 2 - label.get_height()/2))

def main(surface):
	global win
	run = True
	p = Player(play_width // 2, play_height // 2, block_colors['red'])
	clock = pygame.time.Clock()
	locked_positions = []
	grid = create_map_grid(locked_positions)
	counter = 10
	bonus = p.spawn_bonus()
	pygame.time.set_timer(pygame.USEREVENT, 1000)

	while run:
		pygame.time.delay(10)
		clock.tick(60)
		
		keys = pygame.key.get_pressed()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.display.quit()
				sys.exit()

			if event.type == pygame.USEREVENT:
				counter -= 1
				
		if keys[pygame.K_LEFT]:
			if p.check_vertical_platform_collision():
				p.y += 5
			else:
				p.x -= 10

		if keys[pygame.K_RIGHT]:
			if p.check_vertical_platform_collision():
				p.y += 5
			else:
				p.x += 10

		if keys[pygame.K_UP]:
			p.jump()
		else:
			p.gravity()

		if p.check_bonus_collision(bonus):
			bonus = p.spawn_bonus()
			counter += random.choice(bonus_time)

		if p.check_platform_collision() and keys[pygame.K_DOWN]:
			p.y -= 10

		if p.x >= play_width:
			p.x = 30
		elif p.x <= 0:
			p.x = play_width - 30
	
		p.draw_map(surface, bonus, counter)
		#draw_map_grid(surface, grid)
		p.draw(surface)

		if counter == 0:
			draw_text_middle(surface, "You Lost!", 60, block_colors['white'])
		if counter == -1:
			run = False

		pygame.display.update()

def main_menu(surface):
	run = True
	while run:
		win.fill((0, 0, 0))
		draw_text_middle(surface, 'Press any key to play', 60, (255,255,255))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				main(win)

	pygame.display.quit()

win = pygame.display.set_mode((play_width, play_height))
pygame.display.set_caption('My Game')
main_menu(win)


