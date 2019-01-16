import pygame as pg
import random
import numpy as np
from pynput.keyboard import Key, Controller

keyboard = Controller()

pg.init()

display_width = 800
display_height = 600

# color defs

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 100)
white = (255, 255, 255)

gameDisplay = pg.display.set_mode((display_width, display_height))
clock = pg.time.Clock()
myfont = pg.font.SysFont("comicsansms", 25)



def car(x, y):
	pg.draw.rect(gameDisplay, red, (x, y, 50, 50))
def forward_movement_x(theta_degrees, movement_speed, currentx):
	# convert degrees to radians
	theta_radians = theta_degrees * (np.pi / 180)
	# find change in x and y
	delta_x = (movement_speed * np.cos(theta_radians))
	# find new x and y
	return delta_x
def forward_movement_y(theta_degrees, movement_speed, currenty):
	# convert degrees to radians
	theta_radians = theta_degrees * (np.pi / 180)
	# find change in x and y
	delta_y = (movement_speed * np.sin(theta_radians))
	# find new x and y
	return delta_y
def obstacles(num_obstacles):
	obs_array = []
	obs = []
	for i in range(num_obstacles):
			obstaclex = random.randrange(0, display_width)
			obstacley = random.randrange(0, display_height)
			obstacle_width = random.randrange(50, 75)
			obstacle_height = random.randrange(50, 75)

			object = pg.Rect(obstaclex, obstacley, obstacle_width, obstacle_height)

			obs.append((obstaclex, obstacley, obstacle_width, obstacle_height))
			obs_array.append(object)

	return (obs_array, obs)
def outbounds(x, y):
	if y < 0:
		y = display_height
	if y > display_height:
		y = 0
	if x > display_width:
		x = 0
	if x < 0:
		x = display_width
	return (x, y)
def collision():
	x = display_width/2
	y = display_height/2
	car_rotation = 0

	(obs_array, obs) = obstacles(3)

	return (obs, obs[0], obs[1], obs[2], x, y)
def calcThreat(sensL, sensC, sensR):
	j = 1
	threatL =  (j * sensL[6]) + ((j + 1) * sensL[5]) + ((j + 2) * sensL[4])+ ((j + 3) * sensL[3]) + ((j + 4) * sensL[2]) + ((j + 5) * sensL[1]) + ((j + 6) * sensL[0])
	threatC =  (j * sensC[6]) + ((j + 1) * sensC[5]) + ((j + 2) * sensC[4])+ ((j + 3) * sensC[3]) + ((j + 4) * sensC[2]) + ((j + 5) * sensC[1]) + ((j + 6) * sensC[0])
	threatR =  (j * sensR[6]) + ((j + 1) * sensR[5]) + ((j + 2) * sensR[4])+ ((j + 3) * sensR[3]) + ((j + 4) * sensR[2]) + ((j + 5) * sensR[1]) + ((j + 6) * sensR[0])

	return(threatL, threatC, threatR)
def displayThreat(threatL, threatC, threatR):
	threatText = "{}-{}-{}".format(threatL, threatC, threatR)
	threatGraphic = myfont.render(threatText, 1, yellow)
	gameDisplay.blit(threatGraphic, (0, display_height - threatGraphic.get_height()))
def displayTries(tries):
	triesText = "Deaths: {}".format(tries)
	triesGraphic = myfont.render(triesText, 1, yellow)
	gameDisplay.blit(triesGraphic, (0, 0))

"""q learning learns by choosing some action and looking at the new state that it is in
if this state is better, the reward will be higher. if state is worse, a punishment may happen
for this case, reward may be a function of how the sensors vals/threat levels changed 
(would have to make a better threat function). could be based upon distances of sensors
to center of obstacles"""
def game_loop():
	gameExit = False

	#sensor spacing
	spacing = 20
	num_sensors = 8
	sensL = []
	sensC = []
	sensR = []

	tries = 0

	x = (display_width * .5)
	y = (display_height * .5)
	car_rotation = 0
	rotate_speed = 0
	car_speed = 3
	car_direction = True

	#objects
	obs_array = []
	#rectangle drawing
	obs = []

	(obs_array, obs) = obstacles(3)
	

#	obs1 = pg.Rect(obs_array[0][0], obs_array[0][1], obs_array[0][2], obs_array[0][3])
#	obs2 = pg.Rect(obs_array[1][0], obs_array[1][1], obs_array[1][2], obs_array[1][3])
#	obs3 = pg.Rect(obs_array[2][0], obs_array[2][1], obs_array[2][2], obs_array[2][3])


	while not gameExit:

		sensL = []
		sensC = []
		sensR = []
		if car_rotation > 360 or car_rotation < -360:
			car_rotation = car_rotation%360

		#call func update sensors (check for collisions)
		#call func moves (NN)

		#if moves[0] == 1:
			#rotate_speed = -5
		#if moves[1] == 1:
			#rotate_speed = 0
		#if moves[2] == 1:
			#rotate_speed = 5

		for event in pg.event.get():
			if event.type == pg.QUIT:
				gameExit = True
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_LEFT:
					rotate_speed = -5
				if event.key == pg.K_RIGHT:
					rotate_speed = 5
			if event.type == pg.KEYUP:
				if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
					rotate_speed = 0

		car_rotation = car_rotation + rotate_speed

		y = y - forward_movement_y(car_rotation, car_speed, y)
		x = x - forward_movement_x(car_rotation, car_speed, x)
		gameDisplay.fill(pg.Color("black"))

		playerrect = pg.Rect(x - 25, y - 25, 50, 50)
		
		if playerrect.colliderect(obs[0]) or playerrect.colliderect(obs[1]) or playerrect.colliderect(obs[2]):
			(obs, obs[0], obs[1], obs[2], x, y) = collision()
			tries = tries + 1
			

		for i in obs:
			pg.draw.rect(gameDisplay, blue, i)


		(x, y) = outbounds(x, y)
		car(x - 25, y - 25)

		#draw sensors
		sensors = []
		car_rotation_radians = car_rotation * (np.pi / 180)

		#center line sensors
		for i in range(num_sensors):
			if i == 0:
				pass
			else:
				sx = x - ((i + 1) * spacing * np.cos(car_rotation_radians))
				sy = y - ((i + 1) * spacing * np.sin(car_rotation_radians))
				sx = int(sx)
				sy = int(sy)
														
				if (sx >= obs[0][0] and sx <= (obs[0][0] + obs[0][2]) and sy >= obs[0][1] and sy <= (obs[0][1] + obs[0][3]) or 
					sx >= obs[1][0] and sx <= (obs[1][0] + obs[1][2]) and sy >= obs[1][1] and sy <= (obs[1][1] + obs[1][3]) or 
					sx >= obs[2][0] and sx <= (obs[2][0] + obs[2][2]) and sy >= obs[2][1] and sy <= (obs[2][1] + obs[2][3])):

					pg.draw.circle(gameDisplay, white, (sx, sy), 5, 0)
					sensC.append(1)
				else:
					pg.draw.circle(gameDisplay, blue, (sx, sy), 5, 0)
					sensC.append(0)
		#right line sensors
		for i in range(num_sensors):
			if i == 0:
				pass
			else:
				sx = x - ((i + 1) * spacing * np.cos(car_rotation_radians + (np.pi / 10)))
				sy = y - ((i + 1) * spacing * np.sin(car_rotation_radians + (np.pi / 10)))
				sx = int(sx)
				sy = int(sy)
			
				if (sx >= obs[0][0] and sx <= (obs[0][0] + obs[0][2]) and sy >= obs[0][1] and sy <= (obs[0][1] + obs[0][3]) or 
					sx >= obs[1][0] and sx <= (obs[1][0] + obs[1][2]) and sy >= obs[1][1] and sy <= (obs[1][1] + obs[1][3]) or 
					sx >= obs[2][0] and sx <= (obs[2][0] + obs[2][2]) and sy >= obs[2][1] and sy <= (obs[2][1] + obs[2][3])):

					pg.draw.circle(gameDisplay, white, (sx, sy), 5, 0)
					sensR.append(1)
				else:
					pg.draw.circle(gameDisplay, blue, (sx, sy), 5, 0)
					sensR.append(0)
		#left line sensors
		for i in range(num_sensors):
			if i == 0:
				pass
			else:
				sx = x - ((i + 1) * spacing * np.cos(car_rotation_radians - (np.pi / 10)))
				sy = y - ((i + 1) * spacing * np.sin(car_rotation_radians - (np.pi / 10)))
				sx = int(sx)
				sy = int(sy)
											
				if (sx >= obs[0][0] and sx <= (obs[0][0] + obs[0][2]) and sy >= obs[0][1] and sy <= (obs[0][1] + obs[0][3]) or 
					sx >= obs[1][0] and sx <= (obs[1][0] + obs[1][2]) and sy >= obs[1][1] and sy <= (obs[1][1] + obs[1][3]) or 
					sx >= obs[2][0] and sx <= (obs[2][0] + obs[2][2]) and sy >= obs[2][1] and sy <= (obs[2][1] + obs[2][3])):

					pg.draw.circle(gameDisplay, white, (sx, sy), 5, 0)
					sensL.append(1)
				else:
					pg.draw.circle(gameDisplay, blue, (sx, sy), 5, 0)
					sensL.append(0)

		threatL, threatC, threatR = calcThreat(sensL, sensC, sensR)
		
		prev_state = [sensL, sensC, sensR]

		displayThreat(threatL, threatC, threatR)
		displayTries(tries)

		pg.display.update()
		clock.tick(60)

game_loop()
pg.quit()
quit()