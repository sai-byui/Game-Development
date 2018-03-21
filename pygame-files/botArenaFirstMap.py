import os
import random
import pygame


class Player(object):
	"""Class for blue and red rectangles"""

	def __init__(self, x, y):
		self.rect = pygame.Rect(x, y, 16, 16)
		self.x = self.rect.x
		self.y = self.rect.y

	def move(self, dx, dy):

		# Move each axis separately. Note that this checks for collisions both times.
		if dx != 0:
			self.move_single_axis(dx, 0)
		if dy != 0:
			self.move_single_axis(0, dy)

	def move_single_axis(self, dx, dy):

		# Move the rect
		self.rect.x += dx
		self.rect.y += dy

		# If you collide with a wall, move out based on velocity
		for wall in walls:
			if self.rect.colliderect(wall.rect):
				if dx > 0:  # Moving right; Hit the left side of the wall
					self.rect.right = wall.rect.left
				elif dx < 0:  # Moving left; Hit the right side of the wall
					self.rect.left = wall.rect.right
				elif dy > 0:  # Moving down; Hit the top side of the wall
					self.rect.bottom = wall.rect.top
				elif dy < 0:  # Moving up; Hit the bottom side of the wall
					self.rect.top = wall.rect.bottom


# wall rect class
class Wall(object):

	def __init__(self, pos, length, width):
		walls.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], length, width)

# Initialize pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("RED VS. BLUE!")
screen = pygame.display.set_mode((1116, 444))

clock = pygame.time.Clock()
walls = []  # List to hold the walls
BluePlayer = Player(48, 32)  # Create the blue player, put him in coordinates 48 & 32
RedPlayer = Player(900, 222)


# Holds the arena layout using an array of strings.
# W = 12 X 12 brick
# S = spacing, moves map down by 24 pixels
# B = 84 X 12 wall
#

level = [
	"LWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWL",
	" SSS                                                                                         ",
	"                                                                                             ",
	"                                                                                             ",
	"                               WWWWWWWWWWWWWWWWWWWWWWWWWW                                    ",
	"                               W                        W                                    ",
	"                                                                                             ",
	"                                                                                             ",
	"                                            B                                                ",
	"                                                                                             ",
	"  SSS                                                                                        ",
	"                               W                        W                                    ",
	"                               WWWWWWWWWWWWWWWWWWWWWWWWWW                                    ",
	"  SSSSS                                                                                      ",
	" WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW ",
	]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
	for col in row:
		if col == "D":
			door = pygame.Rect(x, y, 12, 12)
		if col == "W":
			Wall((x, y), 12, 12)
		if col == "L":
			Wall((x, y), 12, 444)
		if col == "S":
			y += 24
			continue
		if col == "B":
			Wall((x, y), 12, 84)

		x += 12
	y += 12
	x = 0

running = True
while running:

	clock.tick(60)

	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			running = False
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			running = False

	# Blue Player Movement
	key = pygame.key.get_pressed()
	if key[pygame.K_LEFT]:
		BluePlayer.move(-2, 0)
	if key[pygame.K_RIGHT]:
		BluePlayer.move(2, 0)
	if key[pygame.K_UP]:
		BluePlayer.move(0, -2)
	if key[pygame.K_DOWN]:
		BluePlayer.move(0, 2)

	# Red Player Movement
	move = pygame.key.get_pressed()
	if move[pygame.K_a]:
		RedPlayer.move(-2, 0)
	if move[pygame.K_d]:
		RedPlayer.move(2, 0)
	if move[pygame.K_w]:
		RedPlayer.move(0, -2)
	if move[pygame.K_s]:
		RedPlayer.move(0, 2)

	# Draw the scene
	screen.fill((0, 0, 0))
	for wall in walls:
		pygame.draw.rect(screen, (255, 255, 255), wall.rect)

	pygame.draw.rect(screen, (255, 0, 0), RedPlayer.rect)
	pygame.draw.rect(screen, (0, 0, 255), BluePlayer.rect)
	pygame.display.flip()
