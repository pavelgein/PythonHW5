from game import Game
from sys import argv
from start_window import StartWindow
import tkinter as tk



def main():
	# number_of_players = int(argv[1]) if len(argv) > 1 else 2
	# game = Game(number_players = number_of_players)
	main_window = StartWindow(master = tk.Tk())
	main_window.start()

if __name__ == '__main__':
	main()	 





