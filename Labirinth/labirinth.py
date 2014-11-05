from random import choice


class Labirinth:
	def __init__(self, height=10, width=10):
		self.player = [choice(range(height)), choice(range(width))]
		self.exit = [choice(range(height)), choice(range(width))]
		self.height = height
		self.width = width
		self.generate_field()
	
	def generate_field(self):
		self.field = [[choice([False, True]) for j in range(self.width)] 
							for i in range(self.height << 1)]

	def wall_under(self, i, j):
		return self.field[((i + 1) % self.height) << 1][j]

	def wall_over(self, i, j):
		return self.field[i << 1][j]

	def wall_right_to(self, i, j):
		return self.field[(i << 1) + 1][(j + 1) % self.width]

	def wall_left_to(self, i, j):
		return self.field[(i << 1) + 1][j]
	
	def get_player_position(self):
		return self.player

	def get_exit_position(self):
		return self.exit
	
	def move_smth(self, smth_position, direction):
		i, j = smth_position
		if direction == "up" and not self.wall_over(i, j):
			move = (-1, 0)
		elif direction == "left" and not self.wall_left_to(i, j):
			move = (0, -1)
		elif direction == "right" and not self.wall_right_to(i, j):
			move = (0, 1)
		elif direction == "down" and not self.wall_under(i, j):
			move = (1, 0)
		else:
			return None
		
		return [(smth_position[0] + move[0]) % self.height, 
			(smth_position[1] + move[1]) % self.width]

	def move_player(self, direction):
		new_player = self.move_smth(self.player, direction)
		if new_player:
			self.player = new_player
		return new_player

	@staticmethod
	def count_difference(a1, a2, b):
		if a1 == a2:
			return 0

		diff1 = (a2 - a1) % b
		diff2 = (b - diff1) % b
		if diff1 > diff2:
			return -1
		elif diff1 < diff2:
			return 1
		else:
			return choice([-1, 1, 0])
	
	def move_exit(self):
		i0, j0 = self.player
		i1, j1 = self.exit
		move = (self.count_difference(i0, i1, self.height),
			self.count_difference(j0, j1, self.width))
		self.exit = [(self.exit[0] + move[0]) % self.height,
			     (self.exit[1] + move[1]) % self.width]
		return self.exit

		
		return self.exit

	def finish(self):
		return self.player == self.exit

