import tkinter as tk
from . import game2 as game
from .messages import Message



arrows = ['\u2190', '\u2191', '\u2192', '\u2193', '\u224b'] # left, up, right, down, sea
backgrounds = ['#90EE90', '#90EE90', '#90EE90', '#90EE90', 'blue'] # left, up, right, down, sea

class TkField(game.Field):
	def __init__(self, x, y, text_id = None):
		self.x = x
		self.y = y
		self.text_id = text_id

class TkPlayer(game.Player):
	def __init__(self, field, char = None, name = None, pl_id = None, text_id = None, player = None):
		self.x = field.x
		self.y = field.y
		self.text_id = text_id
		self.char = char
		self.name = name


class TkGame(game.Game):
	def __init__(self, number_players = 2, names = ['\u2121', '2'], chars=['\u2121', '2'], height = 3, width = 30, size_cell = 30, sea = 1):
		super(TkGame, self).__init__(number_players, height, width,sea)
		self.size_cell = size_cell
		self.font = 'Arial '+ str(int(0.6 * size_cell))
		self.window, self.canv = self.init_graphics()
		self.board = self.create_board()
		for i in range(number_players):
			self.players[i].char = chars[i]
			self.players[i].name = names[i]


	def init_graphics(self):
		s = str((self.width + 2) * self.size_cell) + 'x' + str((self.height + 2) * self.size_cell)
		root = tk.Tk()
		root.geometry(s)
		root.title("Догони!")
		canv = tk.Canvas(root, width = (self.width + 2) * self.size_cell, height = (self.height + 2) * self.size_cell)
		canv.pack()
		return root, canv

	def create_board(self):
		return [[None for i in range(self.width + 2)] for j in range(self.height + 2)]

	def start(self):
		self.first_paint()
		self.window.bind("<KeyPress>", self.repaint)
		self.window.mainloop()

	def repaint_cell(self):
		cur_player = self.current_player
		for text_id in cur_player.text_id:
			self.canv.delete(text_id)
		fields = self.get_fields(cur_player.x + 1, cur_player.y + 1)
		for f_x, f_y in fields:
			self.paint_cell(f_x, f_y, 4)


	def get_fields(self, x, y):
		x %= self.width
		y %= self.height
		ans = [(x, y)]
		if x <= 1:
			ans.append((x + self.width, y))
		if y <= 1:
			ans.append((x, y + self.height))
		if x <= 1 and y <= 1:
			ans.append((x + self.width, y + self.height))
		return ans

	def repaint(self, event):
		cur_player = self.current_player
		if self.check_turn(event.keycode):
			self.repaint_cell()
			for text_id in self.cur_exit.text_id:
				self.canv.delete(text_id)
			self.make_turn(event.keycode)
			self.paint_all_start_field()
			self.paint_exit_field()

			if self.winner != None:
				self.window.destroy()
				if self.number_players == 1 and self.loser == True:
					show_lose_message(cur_player)
				else:
					show_win_message(self.players[self.winner])
				exit()

			self.set_next_player()
			fields = self.get_fields(self.current_player.x + 1, self.current_player.y + 1)
			self.players[self.current_player.id].text_id.extend(self.canv.create_rectangle(self.size_cell * f_x + 2, self.size_cell * f_y + 2,
																		self.size_cell + self.size_cell * f_x - 2, self.size_cell + self.size_cell * f_y - 2,
																		width = self.size_cell / 6, outline ='black') for f_x, f_y in fields)

	def paint_cell(self, x, y, z):
		if (x == 0 or y == 0 or x == self.width + 1 or y == self.height + 1):
			if z == 4:
				 self.canv.create_rectangle(self.size_cell * x, self.size_cell * y, self.size_cell + self.size_cell * x, self.size_cell + self.size_cell * y,
											fill = 'blue')
			else:
				 self.canv.create_rectangle(self.size_cell * x, self.size_cell * y, self.size_cell + self.size_cell * x, self.size_cell + self.size_cell * y,
											fill = '#C0C0C0')
		else:
			self.canv.create_rectangle(self.size_cell * x, self.size_cell * y, self.size_cell + self.size_cell * x, self.size_cell + self.size_cell * y,
									   fill = backgrounds[z])
		self.board[y][x] = self.canv.create_text(self.size_cell * x + self.size_cell / 2, self.size_cell * y + self.size_cell / 2, text = arrows[z], font = self.font)

	def paint_all_start_field(self):
		for player in self.players:
			self.paint_start_field(player)

	def paint_start_field(self, player):
		fields = self.get_fields(player.x + 1, player.y + 1)
		for f_x, f_y in fields:
			self.canv.delete(self.board[f_y][f_x]) # удаляем стрелку на месте нашего положения
		player.text_id = [self.canv.create_text(self.size_cell * f_x + self.size_cell / 2,
												self.size_cell * f_y + self.size_cell / 2,
												text = player.char, font = self.font) for f_x, f_y in fields]

	def paint_exit_field(self):
		fields = self.get_fields(self.cur_exit.x + 1, self.cur_exit.y + 1)
		self.cur_exit.text_id = [self.canv.create_rectangle(self.size_cell * f_x + 2, self.size_cell * f_y + 2, self.size_cell + self.size_cell * f_x - 2,
															self.size_cell + self.size_cell * f_y - 2, width = self.size_cell / 6, outline ='red')
								for f_x, f_y in fields]


	def first_paint(self):
		for i in range(self.width + 2):
			for j in range(self.height + 2):
			   self.paint_cell(i, j, self.game[(j - 1) % self.height][(i - 1) % self.width])
		self.paint_all_start_field()
		fields = self.get_fields(self.current_player.x + 1, self.current_player.y + 1)
		self.current_player.text_id.extend(self.canv.create_rectangle(self.size_cell * f_x + 2, self.size_cell * f_y + 2,
																					   self.size_cell + self.size_cell * f_x - 2,
																					   self.size_cell + self.size_cell * f_y - 2,
																					   width = self.size_cell / 6, outline ='black') for f_x, f_y in fields)
		self.paint_exit_field()
		self.canv.create_rectangle(self.size_cell, self.size_cell, (self.width + 1) * self.size_cell, (self.height + 1) * self.size_cell, width = self.size_cell / 10)


def show_win_message(player):
	Message('Выиграл ' + player.name)

def show_lose_message(plyer):
	Message('Вы проиграли')

