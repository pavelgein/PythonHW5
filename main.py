from Catch.start_window import StartWindow
import tkinter as tk



class MainLauncher(tk.Frame):
	def __init__(self, master = tk.Tk()):
		tk.Frame.__init__(self, master)
		self.pack()
		self.master = master
		self.field = None
		self.finish_report = None
		self.create_widgets()
		self.mainloop()
		

	def create_widgets(self):
		self.labirinth = tk.Button(self, text="Лабиринт", command=self.run_labirinth)
		self.labirinth.pack(side="left")

		self.catch = tk.Button(self, text="Догони", command=self.run_catch)
		self.catch.pack(side="left")


	def run_catch(self):
		self.master.destroy()
		master = tk.Tk()
		master.title('Догони!')	
		main_window = StartWindow(master = master)

		main_window.start()



	def run_labirinth(self):
		self.master.destroy()
		import Labirinth.game

if __name__ == '__main__':
	MainLauncher()	 





