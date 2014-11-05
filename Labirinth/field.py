import tkinter as tk


class Field:
	def __init__(self, parrent, labirinth, field_refresh_time, exit_refresh_time):
		self.cell_height, self.cell_width = 20, 20
		self.wall_width = 1
		self.figure_height, self.figure_width = 14, 14
		
		self.parrent = parrent

		field_height = (labirinth.height * self.cell_height + 
				(labirinth.height + 1) * self.wall_width)
		field_width = (labirinth.width * self.cell_width + 
				(labirinth.width + 1) * self.wall_width)
		self.field = tk.Canvas(height=field_height, width=field_width, bg="green")
		self.field.pack()
		self.field.focus_set()		

		self.labirinth = labirinth
		self.player_figure = self.print_player()
		self.exit_figure = self.print_exit()
		self.print_walls()
		
		self.destinations = {38: "up",
				     37: "left",
				     39: "right",
				     40: "down"}
		self.field.bind('<KeyPress>', self.key_handler)
		
		self.field_refresh_time = field_refresh_time
		self.exit_refresh_time = exit_refresh_time
		self.field.after(self.field_refresh_time, self.refresh_field)
		self.field.after(self.exit_refresh_time, self.move_exit)
	
	def get_wall_coordinate(self, i, j):
		return (j * (self.cell_width + self.wall_width) + 1, 
			i * (self.cell_height + self.wall_width) + 1) # <=> (x, y)		

	# FIXME make normal view of walls with width more then 1
	def print_upper_wall(self, i, j):
		x, y = self.get_wall_coordinate(i, j)
		self.field.create_line(x, y, 
				       x + self.cell_width + (self.wall_width << 1), y, 
				       width=self.wall_width)

	def print_left_wall(self, i, j):
		x, y = self.get_wall_coordinate(i, j)
		self.field.create_line(x, y,
				       x, y + self.cell_height + (self.wall_width << 1), 
				       width=self.wall_width)

	def print_walls(self):
		h, w = self.labirinth.height, self.labirinth.width
		for i in range(h + 1):
			for j in range(w + 1):
				if self.labirinth.wall_over(i % h, j % w):
					self.print_upper_wall(i, j)
				if self.labirinth.wall_left_to(i % h, j % w):
					self.print_left_wall(i, j)

	def get_figure_coordinate(self, i, j):
		x, y = self.get_wall_coordinate(i, j)
		return x + self.wall_width, y + self.wall_width

	def print_figure(self, i, j,  width, height, color='red'):
		x, y = self.get_figure_coordinate(i, j)		
		x += ((self.cell_width - width) >> 1)
		y += ((self.cell_height - height) >> 1)
		
		figure = self.field.create_rectangle(x, y, x + width, y + height, fill=color)
		return figure

	def print_player(self):
		return self.print_figure(self.labirinth.player[0],
					 self.labirinth.player[1],
					 self.figure_width,
					 self.figure_height,
					 color = "red")

	def print_exit(self):
		return self.print_figure(self.labirinth.exit[0],
					 self.labirinth.exit[1],
					 self.figure_width,
					 self.figure_height,
					 color = "blue")

	def move_figure(self, figure):
		pass

	def move_player(self, destination):
		new_player = self.labirinth.move_player(destination)
		if new_player:
			self.field.delete(self.player_figure)			
			self.player_figure = self.print_player()
			if self.labirinth.finish():
				self.parrent.end_game()				

	def move_exit(self):
		new_exit = self.labirinth.move_exit()
		if new_exit:
			self.field.delete(self.exit_figure)			
			self.exit_figure = self.print_exit()
		self.field.after(self.exit_refresh_time, self.move_exit)
			

	def key_handler(self, event):
		if event.keycode in self.destinations:
			self.move_player(self.destinations[event.keycode])
	
	def refresh_field(self):
		self.labirinth.generate_field()
		self.field.delete(tk.ALL)
		self.print_walls()
		self.player_figure = self.print_player()
		self.exit_figure = self.print_exit()
		self.field.after(self.field_refresh_time, self.refresh_field)

