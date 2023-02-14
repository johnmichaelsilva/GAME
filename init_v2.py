import pygame
from sys import exit
from random import randint

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

#object
w = 100
h = 200 
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

snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frame = [snail_frame_1,snail_frame_2]
snail_frame_index  = 0
snail_surf = snail_frame[snail_frame_index]

fly_frame_1= pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frame = [fly_frame_1,fly_frame_2]
fly_frame_index  = 0
fly_surf = fly_frame[fly_frame_index]

player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]

player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

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
				if randint(0,2):
					obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
				else:
					obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))
				
			if event.type == snail_animation_timer:
				if snail_frame_index == 0: snail_frame_index = 1
				else: snail_frame_index = 0
				snail_surf = snail_frame[snail_frame_index]


			if event.type == snail_animation_timer:
				if fly_frame_index == 0: fly_frame_index = 1
				else: fly_frame_index = 0
				fly_surf = fly_frame[fly_frame_index]


	if active_game:

		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))
		score = display_score()

		#player
		player_gravity += 1
		player_rect.bottom += player_gravity
		if player_rect.bottom >= 300: player_rect.bottom = 300
		player_animation()
		screen.blit(player_surf,player_rect)

		#obstacle moviment
		obstacle_rect_list =  obstacle_moviment(obstacle_rect_list)

		# colission
		active_game = collisions(player_rect, obstacle_rect_list)
	else:
		screen.fill('Gray')
		screen.blit(player_stand,player_stand_rect)
		screen.blit(game_title, game_title_rect)
		screen.blit(game_msg, game_msg_rect)
		obstacle_rect_list.clear()
		player_rect.midbottom = (80, 300)
		player_gravity = 0

		score_msg = test_font.render(f'your score {score}', False,'Pink')
		score_msg_rect = score_msg.get_rect(center = (400, 310))
		
		if score == 0:
			screen.blit(game_msg, game_msg_rect)
		else:			
			screen.blit(score_msg, score_msg_rect)
			screen.blit(game_msg, game_msg_rect)


	pygame.display.update()	
	clock.tick(60) # not faster 60 times per second for while condition 



 
		#  if event.type == pygame.MOUSEBUTTONUP:
		# 	print('up')
		# 	player_gravity = -20

	# screen.blit(text_surface,(300, 50))
	# pygame.draw.line(screen,'#c0e8ec',(0,0), pygame.mouse.get_pos(),10)
	# pygame.draw.rect(screen,'Pink',score_rect, 10)


		# if event.type == pygame.KEYUP:
		# 	print('up')
		# if event.type == pygame.MOUSEBUTTONUP:
		# 	print('event.pos')

	# snail_surface_reverse = snail_surface.copy()
	# img_with_flip = pygame.transform.flip(snail_surface_reverse, True, False)


	# keys = (pygame.key.get_pressed())
	# if keys[pygame.K_SPACE]:
	# 	print('jump')


	# if player_rect.colliderect(snail_rect):
	# 	print('aa')

	# mouse_pos = pygame.mouse.get_pos()
	# if player_rect.collidepoint((mouse_pos)):
	# 	print(pygame.mouse.get_pressed())

	# if snail_rect.left < -72: 
	# 	snail_rect.right = 0
	# 	# snail_rect.left += snail_speed
	# 	# screen.blit(snail_surface, snail_rect)
	# 	print(snail_rect.left)
	# 	snail_x_pos_factor == -1
	# # 	snail_orientation = img_with_flip
		
	# elif snail_x_pos > height:
	# 	snail_x_pos_factor == 1
	# 	snail_orientation = snail_surface

	# else:
	# 	snail_x_pos += -snail_speed * snail_x_pos_factor 
	# 	screen.blit(snail_orientation,(snail_x_pos, 250))