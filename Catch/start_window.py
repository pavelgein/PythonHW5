import tkinter as tk
from .tkgame import TkGame

font_big = 'Arial, 18'
font_small = 'Arial, 10'
class StartWindow(tk.Frame):
	def __init__(self, master=None, begin_window = None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.master = master
		self.master.title('Параметры игры "Догони!"')
		self.begin_window = begin_window
		# self.field = None
		# self.finish_report = None
		self.create_widgets()


	def create_widgets(self):
		tk.Label(self, justify='left', text="ИГРОКИ", font=font_small).grid(row=0,sticky='w',pady=5,padx=5)
		tk.Label(self, justify='left', text="количество\nигроков", font=font_small).grid(row=1,sticky='w',padx=5)
		tk.Label(self, justify='left', text="имена\nигроков", font=font_small).grid(row=1, column =1,sticky='w',padx=5)
		tk.Label(self, justify='left', text="символы игроков", font=font_small).grid(row=1,column =2,sticky='w', columnspan=4)

		self.number_players = tk.IntVar()
		self.ONE_PLAYER = tk.Radiobutton(self, text="один игрок", variable=self.number_players, value=1,
					   indicatoron=0, offrelief="groove", width=15, font=font_small, command=self.invisibleSecondPlayer)
		self.ONE_PLAYER.grid(padx=10, row=2,column =0,sticky='w')
		self.ONE_PLAYER.select()
		self.TWO_PLAYERS =tk.Radiobutton(self, text="двое игроков", variable=self.number_players, value=2,
										 indicatoron=0, offrelief="groove", command=self.visibleSecondPlayer, width=15, font=font_small)
		self.TWO_PLAYERS.grid(padx=10, row=3,column =0,sticky='w')

		self.name_first_player = tk.StringVar()
		self.name_first_player.set("Василий")
		self.FIRST_NAME = tk.Entry(self, textvariable=self.name_first_player, width=20, font=font_small)
		self.FIRST_NAME.grid(row=2, column = 1, sticky='w',padx=10)

		self.name_second_player = tk.StringVar()
		self.name_second_player.set("Иннокентий")
		self.SECOND_NAME = tk.Entry(self, textvariable=self.name_second_player, width=20, state='disabled', font=font_small)
		self.SECOND_NAME.grid(row=3, column = 1, sticky='w',padx=10)

		self.symbol_first_player = tk.StringVar()
		self.SYMBOL1_FIRST_PLAYER = tk.Radiobutton(self, text='\u2654', variable=self.symbol_first_player, value='\u2654',
					   indicatoron=0, offrelief="groove",width=3, font=font_big)
		self.SYMBOL1_FIRST_PLAYER.grid(row=2,column =2,sticky='w')
		self.SYMBOL1_FIRST_PLAYER.select()
		self.SYMBOL2_FIRST_PLAYER = tk.Radiobutton(self, text='\u2655', variable=self.symbol_first_player, value='\u2655',
					   indicatoron=0, offrelief="groove", width=3, font=font_big)
		self.SYMBOL2_FIRST_PLAYER.grid(row=2,column =3,sticky='w')
		self.SYMBOL3_FIRST_PLAYER = tk.Radiobutton(self, text='\u2656', variable=self.symbol_first_player, value='\u2656',
					   indicatoron=0, offrelief="groove", width=3, font=font_big)
		self.SYMBOL3_FIRST_PLAYER.grid(row=2,column =4,sticky='w')

		self.symbol_second_player = tk.StringVar()
		self.SYMBOL1_SECOND_PLAYER = tk.Radiobutton(self, text='\u265A', variable=self.symbol_second_player, value='\u265A',
					   indicatoron=0, offrelief="groove",width=3, font=font_big,state='disabled')
		self.SYMBOL1_SECOND_PLAYER.grid(row=3,column =2,sticky='w')
		self.SYMBOL1_SECOND_PLAYER.select()
		self.SYMBOL2_SECOND_PLAYER = tk.Radiobutton(self, text='\u265B', variable=self.symbol_second_player, value='\u265B',
					   indicatoron=0, offrelief="groove", width=3, font=font_big,state='disabled',)
		self.SYMBOL2_SECOND_PLAYER.grid(row=3,column =3,sticky='w')
		self.SYMBOL3_SECOND_PLAYER = tk.Radiobutton(self, text='\u265C', variable=self.symbol_second_player, value='\u265C',
					   indicatoron=0, offrelief="groove", width=3, font=font_big,state='disabled',)
		self.SYMBOL3_SECOND_PLAYER.grid(row=3,column =4,sticky='w')

		tk.Label(self, justify='left', text="ПАРАМЕТРЫ ПОЛЯ", font=font_small).grid(row=4,sticky='w',pady=5,padx=5)
		tk.Label(self, justify='left', text="ширина", font=font_small).grid(row=5,sticky='w',padx=5)
		tk.Label(self, justify='left', text="высота", font=font_small).grid(row=5, column =1,sticky='w',padx=5)
		tk.Label(self, justify='left', text="моря в начале игры", font=font_small).grid(row=5,column =2,sticky='w',padx=5,columnspan=4)

		self.width = tk.IntVar()
		self.width.set(30)
		self.WIDTH = tk.Entry(self, textvariable=self.width, width=5, font=font_small)
		self.WIDTH.grid(row=6, column = 0, sticky='w', padx=10)

		self.height = tk.IntVar()
		self.height.set(15)
		self.HEIGHT = tk.Entry(self, textvariable=self.height, width=5, font=font_small)
		self.HEIGHT.grid(row=6, column = 1, sticky='w', padx=10)

		self.sea = tk.IntVar()
		self.SEA = tk.Checkbutton(self, text="есть моря", width=10, font=font_small, variable=self.sea)
		self.SEA.grid(row=6, column = 2, sticky='n', padx=10, columnspan=4)

		self.image = tk.PhotoImage(file='Catch\catch.png')
		self.NEW = tk.Button(self, text=" Играть \n  в Догони   ", command=self.start_game, image = self.image, compound='left', font=font_small)
		self.NEW.grid(row=7,sticky='w',pady=10,padx=10)

		# self.QUIT = tk.Button(self, text="Играть в другую игру", command=self.main_window, font=font_small)
		# self.QUIT.grid(row=10, sticky='w',pady=10,padx=10)

	def visibleSecondPlayer(self):
			self.SECOND_NAME['state'] = 'normal'
			self.SYMBOL1_SECOND_PLAYER['state'] = 'normal'
			self.SYMBOL2_SECOND_PLAYER['state'] = 'normal'
			self.SYMBOL3_SECOND_PLAYER['state'] = 'normal'


	def invisibleSecondPlayer(self):
		self.SECOND_NAME['state'] = 'disable'
		self.SYMBOL1_SECOND_PLAYER['state'] = 'disable'
		self.SYMBOL2_SECOND_PLAYER['state'] = 'disable'
		self.SYMBOL3_SECOND_PLAYER['state'] = 'disable'

	def main_window(self):
		self.master.destroy()
		# self.begin_window()


	def start_game(self):
		number = int(self.number_players.get())

		names = [self.name_first_player.get(), self.name_second_player.get()]
		if names[0]=='':
			names[0]='1';
		if names[1]=='':
			names[1]='2';
		chars = [self.symbol_first_player.get(), self.symbol_second_player.get()]
		game = TkGame(height = min(30, int(self.HEIGHT.get())),
							width = min(40,int(self.WIDTH.get())),
								number_players = number, chars=chars, names = names, sea = int(self.sea.get()))
		self.master.destroy()

		game.start()
	def start(self):
		self.master.title = 'Догони!'
		self.mainloop()
# StartWindow(master=tk.Tk()).mainloop()

