from Catch.start_window import StartWindow
import tkinter as tk



class MainLauncher(tk.Frame):
		def __init__(self, master = tk.Tk()):
				tk.Frame.__init__(self, master, borderwidth = 5)
				self.master.title('Во что будем играть?')
				self.grid()
				self.master = master
				self.field = None
				self.finish_report = None
				self.create_widgets()
				self.mainloop()
				

		def create_widgets(self):
						self.imageCatch = tk.PhotoImage(file='Catch\catch.png')
						self.imageLabirinth = tk.PhotoImage(file='Labirinth\labirinth.png')

						self.LABEL_FOR_LABIRINTH = tk.Label(self, justify='left', 
															text="Лабиринт.\n\
Нужно дойти до выхода.\n\
Больше игра не имеет ничего общего с реальностью:\n\
стенки лабиринта то появляются, то исчезают,\nда и выход не стоит на месте!\n\
Игра рассчитана на одного человека.")
						self.LABEL_FOR_LABIRINTH.grid(row=0,sticky='w')
						
						self.LABIRINTH = tk.Button(self,  text=" Играть в Лабиринт", command=self.run_labirinth, image = self.imageLabirinth, compound='left')
						self.LABIRINTH.grid(row=1,sticky='w',pady=10)

						self.LABEL_FOR_CATCH = tk.Label(self, justify='left',
															text="Догони!\n\
Что делать, если земля уходит из-под ног?\n\
Скорее выбираться. Проблема в том, что \n\
каждый ход будет двигать точку выхода.\n\
Играть можно и одному и вдвоём.")
						self.LABEL_FOR_CATCH.grid(row=2,sticky='w')

						self.CATCH = tk.Button(self, text=" Играть в Догони", command=self.run_catch, image = self.imageCatch, compound='left')
						self.CATCH.grid(row=3,sticky='w',pady=10)

						self.QUIT = tk.Button(self, text="Не будем играть", command=self.master.destroy)
						self.QUIT.grid(row=4,sticky='w',pady=10)


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





