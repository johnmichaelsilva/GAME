import pygame
from sys import exit

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
active_game = True

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
text_surface = test_font.render('My game', False, 'Gray').convert()

score_surface = test_font.render('aaahhh', False, (64,64,64))
score_rect = score_surface.get_rect(center = (400,50))

snail_x_pos = 600

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (snail_x_pos,300))


player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0


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
				snail_rect.left = 800
		

	if active_game:

		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))
		screen.blit(score_surface,score_rect)

		snail_rect.left -= snail_speed * snail_x_pos_factor
		if snail_rect.left  <=0: snail_rect.left = 800
		screen.blit(snail_surface, snail_rect)

		#player
		player_gravity += 1
		player_rect.bottom += player_gravity
		if player_rect.bottom >= 300: player_rect.bottom = 300
		screen.blit(player_surface,player_rect)


		# colission
		if snail_rect.colliderect(player_rect):
			active_game = False
			# pygame.quit()
			# exit()
	else:
		screen.fill('Gray')


	pygame.display.update()	
	clock.tick(60) # not faster 60 times per second for while condition 



 
		# if event.type == pygame.MOUSEBUTTONUP:
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