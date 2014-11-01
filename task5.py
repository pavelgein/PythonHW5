import tkinter
from tkinter import *
from random import choice

class Field():
    def __init__(self, x, y, text_id = None):
        self.x = x
        self.y = y
        self.text_id = None
n = 20

cur_start = Field(choice(range(0, n)), choice(range(0, n)))
cur_exit = Field(choice(range(0, n)), choice(range(0, n)))


arrows = ['\u2190', '\u2191', '\u2192', '\u2193'] # left, up, right, down

font = 'Arial 18'

s = str((n + 2) * 30) + 'x' + str((n + 2) * 30)

root = Tk()
root.geometry(s)
root.title("Догони!")
canv = Canvas(root, width = (n + 2) * 30, height = (n + 2) * 30)
canv.pack()


def get_fields(x, y):
    x %= n
    y %= n
    ans = [(x, y)]
    if x <= 1:
        ans.append((x + n, y))
    if y <= 1:
        ans.append((x, y + n))
    if x <= 1 and y <= 1:
        ans.append((x + n, y + n))
    return ans

def create_game():
    return [[choice([0, 1, 2, 3]) for i in range(n)] for j in range(n)]

def create_board():
    return [[None for i in range(n + 2)] for j in range(n + 2)]

def fx():
    if game[cur_start.x][cur_start.y] == 0:
        return -1
    if game[cur_start.x][cur_start.y] == 2:
        return 1
    return 0

def fy():
    if game[cur_start.x][cur_start.y] == 3:
        return 1
    if game[cur_start.x][cur_start.y] == 1:
        return -1
    return 0

# 38 up
# 37 left
# 40 down
# 39 right
    
def repaint(event):
    for text_id in cur_start.text_id:
        canv.delete(text_id)
    paint_arrow_field(cur_start.x, cur_start.y)    

    for text_id in cur_exit.text_id:
        canv.delete(text_id)

    if (event.keycode == 39):
        cur_start.x = (cur_start.x + 1) % n
    if (event.keycode == 37):
        cur_start.x = (cur_start.x - 1) % n
    if (event.keycode == 38):
        cur_start.y = (cur_start.y - 1) % n
    if (event.keycode == 40):
        cur_start.y = (cur_start.y + 1) % n
    if check_win():
        show_win_message()
        exit()
    if (37 <= event.keycode <=40):
        cur_exit.x = (cur_exit.x + fx()) % n
        cur_exit.y = (cur_exit.y + fy()) % n
        repaint_board()

    if check_win():
        show_win_message()
        exit()



def check_win():
    if cur_exit.x == cur_start.x and cur_exit.y == cur_start.y:
        print('Win')
    return cur_exit.x == cur_start.x and cur_exit.y == cur_start.y

def show_win_message():
    pass

def paint_arrow_field(x, y):
    fields = get_fields(x, y)
    for f_x, f_y in fields:
        board[f_x][f_y] = canv.create_text(30 * f_x + 15, 30 * f_y + 15, text = arrows[game[x][y]], font = font) 

def paint_start_field():
    fields = get_fields(cur_start.x, cur_start.y)
    cur_start.text_id = [canv.create_text(30 * f_x + 15, 30 * f_y + 15, text = "\u2655", font = font) for f_x, f_y in fields]

def paint_exit_field():   
    fields = get_fields(cur_exit.x, cur_exit.y)
    cur_exit.text_id = [canv.create_rectangle(30 * f_x, 30 * f_y, 30 + 30 * f_x, 30 + 30 * f_y, width = 5, outline ='red') 
                        for f_x, f_y in fields]

def paint():
    for i in range(n + 2):
        for j in range(n + 2):
            if (i == 0 or j == 0 or i == n+1 or j == n + 1):
                canv.create_rectangle(i * 30, j * 30, i * 30 + 30, j * 30 + 30, fill = '#C0C0C0')
            else:
                canv.create_rectangle(i * 30, j * 30, i * 30 + 30, j * 30 + 30, fill = '#90EE90')

    for i in range(n):
        for j in range(n):
            if cur_start.y != i or cur_start.x != j:
                paint_arrow_field(j, i)

    paint_start_field()
    paint_exit_field()
    canv.create_rectangle(30, 30, (n + 1) * 30, (n + 1) * 30, width = 3)

def repaint_board():
    fields = get_fields(cur_start.x, cur_start.y)
    for f_x, f_y in fields:
        canv.delete(board[f_x][f_y]) # удаляем стрелку на месте нашего положения

    paint_start_field()
    paint_exit_field()
   
  
board = create_board()
game = create_game()
paint()
root.bind("<KeyPress>", repaint)
root.mainloop()
