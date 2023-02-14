import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk1,player_walk2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0
		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.05)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()


	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300: 
			self.rect.bottom = 300

	def animation_status(self):
		if self.rect.bottom < 300:
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk): 
				self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_status() 


class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type):
		super().__init__()

		if type == 'fly':
			fly_frame_1= pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_frame_1,fly_frame_2]
			y_pos = 210
		else:
			snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_frame_1,snail_frame_2]
			y_pos = 300

		
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom =  (randint(900,1100),y_pos))
		

	def animation_status(self):
		self.animation_index += 0.1
		if self.animation_index >= len(self.frames): 
			self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_status() 
		self.rect.x -= 6
		self.destroy()


	def destroy(self):
		if self.rect.x <= -100:
			self.kill()

def display_score():
	current_time = int(pygame.time.get_ticks()/1000) - start_time
	score_surf = test_font.render(f'{current_time}', False, (64,64,64)) 
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf , score_rect)	
	return current_time

def obstacle_moviment(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			obstacle_rect.x -= 5

			if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
			else: screen.blit(fly_surf, obstacle_rect)
		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

		return obstacle_list
	else: return []

def collisions(player, obstacles):
	if collisions:
		for obstacle_rect in obstacles:
			if player.colliderect(obstacle_rect): return False
	return True

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
		obstacle_group.empty()
		return False
	else: return True

def player_animation():
	global player_surf, player_index

	if player_rect.bottom < 300: #jump
		player_surf = player_jump
	else: #walk
		player_index += 0.1
		if player_index >= len(player_walk): player_index = 0
		player_surf = player_walk[int(player_index)]


pygame.init()

height = 800
weight = 400

screen = pygame.display.set_mode((height,weight))
pygame.display.set_caption("game")
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

bg_music = pygame.mixer.Sound('audio/music.wav')

#object
snail_speed = 6
snail_x_pos_factor = 1
active_game = False
start_time = 0

#screen
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
text_surface = test_font.render('My game', False, 'Pink').convert()

game_title = test_font.render('My game', False, 'Pink')
game_title_rect = game_title.get_rect(center = (400,80))

game_msg = test_font.render('press space to start', False, 'Pink')
game_msg_rect = game_msg.get_rect(center = (400,340))


#objs
snail_x_pos = 600
score = 0

player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]

player_rect = player_surf.get_rect(midbottom = (80,300))

player = pygame.sprite.GroupSingle()
player.add(Player())


obstacle_group = pygame.sprite.Group()
obstacle_group.update()

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))



#obstacle

obstacle_rect_list = []

#timer

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit() # to close properly and safely

		if active_game:
			if event.type == pygame.MOUSEBUTTONDOWN : 
				if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
					player_gravity = -20


			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
					player_gravity = -20
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				active_game = True
				start_time = int(pygame.time.get_ticks()/1000)

		if active_game:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))


			# if event.type == snail_animation_timer:
			# 	if snail_frame_index == 0: snail_frame_index = 1
			# 	else: snail_frame_index = 0
			# 	snail_surf = snail_frame[snail_frame_index]


			# if event.type == snail_animation_timer:
			# 	if fly_frame_index == 0: fly_frame_index = 1
			# 	else: fly_frame_index = 0
			# 	fly_surf = fly_frame[fly_frame_index]


	if active_game:

		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))
		score = display_score()
		bg_music.play(loops = -1)

		#player
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		#obstacle moviment
		# obstacle_rect_list =  obstacle_moviment(obstacle_rect_list)

		# colission
		active_game	 = collision_sprite()
		# active_game = collisions(player_rect, obstacle_rect_list)

	else:
		screen.fill('Gray')
		screen.blit(player_stand,player_stand_rect)
		screen.blit(game_title, game_title_rect)
		screen.blit(game_msg, game_msg_rect)
		# obstacle_rect_list.clear()
		# player_rect.midbottom = (80, 300)
		# player_gravity = 0

		score_msg = test_font.render(f'your score {score}', False,'Pink')
		score_msg_rect = score_msg.get_rect(center = (400, 310))
		
		if score == 0:
			screen.blit(game_msg, game_msg_rect)
		else:			
			screen.blit(score_msg, score_msg_rect)
			screen.blit(game_msg, game_msg_rect)


	pygame.display.update()	
	clock.tick(60) # not faster 60 times per second for while condition 



 