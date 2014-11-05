import tkinter as tk
from labirinth import Labirinth
from field import Field
import sys


DEBUG = True

if len(sys.argv) > 1 and sys.argv[1] == "true":
	DEBUG = True


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
		self.HEIGHT, self.HEIGHT_WIDGET = self.create_entry_widget("20", "height")
		self.WIDTH, self.WIDTH_WIDGET = self.create_entry_widget("30", "width")
		self.FIELD_REFRESH, self.FIELD_REFRESH_WIDGET = self.create_entry_widget(
										"10", 
										"field refresh time(in secs)")
		self.EXIT_REFRESH, self.EXIT_REFRESH_WIDGET = self.create_entry_widget(
										"3", 
										"exit move time (in secs)")

		self.NEW = tk.Button(self, text="New Game", command=self.init_new_game)
		self.NEW.pack(side="left")

		self.QUIT = tk.Button(self, text="Quit", command=self.master.destroy)
		self.QUIT.pack(side="left")

	def create_entry_widget(self, default="", label=""):
		label = tk.Label(self, text=label)
		label.pack()
		widget_text = tk.StringVar()
		widget = tk.Entry(self, textvariable=widget_text)
		widget_text.set(default)
		widget.pack()
		return widget_text, widget


	def init_new_game(self):
		if self.field:
			self.field.field.destroy()

		if self.finish_report:
			self.finish_report.destroy()

		height, width = int(self.HEIGHT.get()), int(self.WIDTH.get())
		lab = Labirinth(height=height, width=width)		
		
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
