from Catch.start_window import StartWindow
import tkinter as tk



def main():
	master = tk.Tk()
	master.title('Догони!')	
	main_window = StartWindow(master = master)
	main_window.start()

if __name__ == '__main__':
	main()	 





