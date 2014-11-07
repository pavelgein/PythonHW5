import tkinter as tk
from .labirinth import *
from .field import Field
import sys


DEBUG = False

if len(sys.argv) > 1 and sys.argv[1] == "true":
	DEBUG = True

lab_types = {
	'r': Labirinth,
	'v': VertLabirinth,
	'vh': VertHorLabirinth,
	'e': EmptyLabirinth
}

class MainFrame(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.master = master
		self.field = None
		self.finish_report = None
		self.create_widgets()
		
		# for testing
		if DEBUG:
			self.init_new_game()

	def create_widgets(self):
		self.HEIGHT, self.HEIGHT_WIDGET = self.create_entry_widget("25", "Height")
		self.WIDTH, self.WIDTH_WIDGET = self.create_entry_widget("45", "Width")
		self.FIELD_REFRESH, self.FIELD_REFRESH_WIDGET = self.create_entry_widget(
										"10", 
										"Field refresh time(in secs)")
		self.EXIT_REFRESH, self.EXIT_REFRESH_WIDGET = self.create_entry_widget(
										"3", 
										"Exit move time (in secs)")
		self.LABIRINTH_TYPE, self.LABIRINTH_TYPE_WIDGET = self.create_entry_widget(
										"vh", 
										"Labirinth type")
		self.NEW = tk.Button(self, text="New Game", command=self.init_new_game)
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


	def init_new_game(self):
		if self.field:
			self.field.field.destroy()

		if self.finish_report:
			self.finish_report.destroy()

		height, width = int(self.HEIGHT.get()), int(self.WIDTH.get())
		
		# FIXME meke lab_types as MainFrame attribute
		if self.LABIRINTH_TYPE.get() in lab_types:
			GameLabirinth = lab_types[self.LABIRINTH_TYPE.get()]
		else:
			GameLabirinth = Labirinth

		lab = GameLabirinth(height=height, width=width)		
		
		field_refresh_time = int(float(self.FIELD_REFRESH.get()) * 1000)
		exit_refresh_time = int(float(self.EXIT_REFRESH.get()) * 1000)
		self.field = Field(self,
				   labirinth=lab,
				   field_refresh_time=field_refresh_time,
				   exit_refresh_time=exit_refresh_time)

	def end_game(self):
		self.field.field.destroy()
		self.finish_report = tk.Label(self.master, text="Congratulations! You win!")
		self.finish_report.pack()
		# for testing
		if DEBUG:
			self.init_new_game()

MainFrame(master=tk.Tk()).mainloop()
