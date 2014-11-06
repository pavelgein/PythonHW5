import tkinter as tk
from game import Game


class StartWindow(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.master = master
		# self.field = None
		# self.finish_report = None
		self.create_widgets()
		
	def create_widgets(self):
		self.HEIGHT, self.HEIGHT_WIDGET = self.create_entry_widget("20", "Height")
		self.WIDTH, self.WIDTH_WIDGET = self.create_entry_widget("20", "Width")
		self.NUMBER, self.NUMBER_WIDGET = self.create_entry_widget(
										"2", 
										"Number of players")
		
		self.NEW = tk.Button(self, text="New Game", command=self.start_game)
		self.NEW.pack(side="left")

		self.QUIT = tk.Button(self, text="Quit", command=self.master.destroy)
		self.QUIT.pack(side="left")

	def create_entry_widget(self, default="", label=""):
		label = tk.Label(self, text=label)
		label.pack(side="left")
		widget_text = tk.StringVar()
		widget = tk.Entry(self, textvariable=widget_text, width=5)
		widget_text.set(default)
		widget.pack(side="left")
		return widget_text, widget

	def start_game(self):
		game = Game(height = int(self.HEIGHT.get()), 
			 	    width = int(self.WIDTH.get()), 
					number_players = int(self.NUMBER.get()))
		self.master.destroy()
		game.start()
	def start(self):
		self.mainloop()		
# StartWindow(master=tk.Tk()).mainloop()

