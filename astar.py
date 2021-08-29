import pygame
# import math
import numpy as np
from queue import PriorityQueue, Queue

WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

RIGHT = 0
UP_RIGHT = 45 
UP = 90
UP_LEFT = 135
LEFT = 180
DOWN_LEFT = 225
DOWN = 270
DOWN_RIGHT = 315

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid, angle ):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier() and (abs(angle - RIGHT)<= 90 or abs(angle - RIGHT) >= 270): # RIGHT
			# print("RIGHT",abs(angle - RIGHT))
			self.neighbors.append((grid[self.row + 1][self.col],RIGHT))

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier() and abs(abs(angle - LEFT)<= 90 or abs(angle - LEFT) >= 270): # LEFT
			# print("LEFT",abs(angle - LEFT))
			self.neighbors.append((grid[self.row - 1][self.col],LEFT))


		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier()  and (abs(angle - DOWN)<= 90 or abs(angle - DOWN) >= 270): # DOWN
			# print("Down",abs(angle - DOWN))
			self.neighbors.append((grid[self.row][self.col + 1],DOWN))

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier()and (abs(angle - UP)<= 90 or abs(angle - UP) >= 270): # UP
			# print("UP",abs(angle - UP))
			self.neighbors.append((grid[self.row][self.col - 1],UP))

		if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col-1].is_barrier()  and (abs(angle - UP_RIGHT)<= 90 or abs(angle - UP_RIGHT) >= 270): # UP_RIGHT
			# print("UP RIGHT",abs(angle - UP_RIGHT))
			self.neighbors.append((grid[self.row + 1][self.col -1 ],UP_RIGHT))

		if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col+1].is_barrier()   and (abs(angle - DOWN_RIGHT)<= 90 or abs(angle - DOWN_RIGHT) >= 270): # DOWN RIGHT
			# print("Down RIGHT",abs(angle - DOWN_RIGHT))
			self.neighbors.append((grid[self.row + 1][self.col + 1 ],DOWN_RIGHT))

		if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col-1].is_barrier()  and (abs(angle - UP_LEFT)<= 90 or abs(angle - UP_LEFT) >= 270): # UP Left
			# print("UP_LEFT",abs(angle - UP_LEFT))
			self.neighbors.append((grid[self.row - 1][self.col  -1],UP_LEFT))


		if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col+1].is_barrier() and (abs(angle - DOWN_LEFT)<= 90 or abs(angle - DOWN_LEFT) >= 270): # DOWN_LEFT
			# print("DOWN lEFT",abs(angle - DOWN_LEFT))
			self.neighbors.append((grid[self.row - 1][self.col  +1],DOWN_LEFT))

		# print("neighbours added")
		# for neig in self.neighbors:
			# print(neig[0].get_pos())
		# print("------------------")



	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	# print (np.sqrt( np.square(abs(x1 - x2)) + np.square(abs(y1 - y2))))	
	return np.sqrt( np.square(abs(x1 - x2)) + np.square(abs(y1 - y2)))


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		
	draw()


def algorithm(draw, grid, start, end,start_angle,barriers):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, (start,start_angle)))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())
	i =0 
	for barrier in barriers:
		i +=1
		print(i)
		print (barrier.get_pos())

	open_set_hash = {(start,start_angle)}
	while not open_set.empty():
		current = open_set.get()[2]
		# print ("current is: ", current[0].get_pos())
		if (open_set_hash.__contains__(current)):
			open_set_hash.remove(current)


			if current[0] == end:
				reconstruct_path(came_from, end, draw)
				end.make_end()
				return True
			# print(current[1])
			current[0].update_neighbors(grid,current[1])
			for neighbor in current[0].neighbors:
				# scores should be tuned to get optimal results
				# distance score to be calibrated with actual distance
				steering_angle = abs(current[1] - neighbor[1])
				if (steering_angle > 180):
					steering_angle -= 180 
				steering_penalty = abs(current[1] - neighbor[1] )/90
				# print ("Steering penalty is : ",steering_penalty)
				distance_score = 0
				if (neighbor[1] % 90) == 0:
					# print (neighbor[1])
					# print (neighbor[1]%90)
					distance_score = 1 
				else : 
					# print (neighbor[1])
					# print (neighbor[1]%90)
					distance_score = np.sqrt(2)
				temp_g_score = g_score[current[0]] + distance_score + steering_penalty


				if temp_g_score < g_score[neighbor[0]]:
					came_from[neighbor[0]] = current[0]
					g_score[neighbor[0]] = temp_g_score
					f_score[neighbor[0]] = temp_g_score + h(neighbor[0].get_pos(), end.get_pos())
					if neighbor not in open_set_hash:
						# print ("adding neighbours")
						# print (neighbor[0].get_pos())
						count += 1
						open_set.put((f_score[neighbor[0]], count, neighbor))
						open_set_hash.add(neighbor)
						neighbor[0].make_open()
		else: 
			print ("duplicate")
			# draw()

		if current[0] != start:
			current[0].make_closed()
		# print ()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					barriers = []
					for row in grid:
						for spot in row:
							if spot.is_barrier():
								barriers.append(spot) 


					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end,0,barriers)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)