import tkinter as tk

class Message(tk.Frame):
	def __init__(self, message):
		tk.Frame.__init__(self, tk.Tk())
		self.pack()

		mes = tk.Label(self, text = message, fg = 'black', font = ("Arial", 16)).pack()
		self.begin_button = tk.Button(self, text = 'В начало', command = self.start_new, compound = 'left')
		self.begin_button.pack()
		self.mainloop()

if __name__ == '__main__':
	WinMessage('aaa')
