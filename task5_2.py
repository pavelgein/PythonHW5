import tkinter
from tkinter import *
from random import choice

class Field():
    def __init__(self, x, y, text_id = None):
        self.x = x
        self.y = y
        self.text_id = None

def create_game():
    return [[choice([0, 1, 2, 3]) for i in range(width)] for j in range(height)]

def create_board():
    return [[None for i in range(width + 2)] for j in range(height + 2)]        

height = 10	
width = 10
size_cell = 30
font = 'Arial '+str(int(0.6 * size_cell))
sea = 1
number_players = 2
current_player = [0]
players = []
player_char = []
for i in range(number_players):
    player_char.append(str(i+1))

board = create_board()
game = create_game()


def gen_good():
    while True:
        x = choice(range(width))
        y = choice(range(height))
        if game[x][y] != 4:
            return Field(x, y)

for i in range(number_players):
    players.append(gen_good())

cur_exit = gen_good()




arrows = ['\u2190', '\u2191', '\u2192', '\u2193', '\u224b'] # left, up, right, down, sea
backgrounds = ['#90EE90', '#90EE90', '#90EE90', '#90EE90', 'blue']



s = str((width + 2) * size_cell) + 'x' + str((height + 2) * size_cell)

root = Tk()
root.geometry(s)
root.title("Догони!")
canv = Canvas(root, width = (width + 2) * size_cell, height = (height + 2) * size_cell)
canv.pack()

def get_fields(x, y):
    x %= width
    y %= height
    ans = [(x, y)]
    if x <= 1:
        ans.append((x + width, y))
    if y <= 1:
        ans.append((x, y + height))
    if x <= 1 and y <= 1:
        ans.append((x + width, y + height))
    return ans


def fx():
    if game[players[current_player[0]].x][players[current_player[0]].y] == 0:
        return -1
    if game[players[current_player[0]].x][players[current_player[0]].y] == 2:
        return 1
    return 0

def fy():
    if game[players[current_player[0]].x][players[current_player[0]].y] == 3:
        return 1
    if game[players[current_player[0]].x][players[current_player[0]].y] == 1:
        return -1
    return 0
def empty_cell(x,y):
    return all([x != players[i].x or y != players[i].y for i in range(number_players)])

def repaint_cell():
    for text_id in players[current_player[0]].text_id:
        canv.delete(text_id)
    fields = get_fields(players[current_player[0]].x + 1, players[current_player[0]].y + 1)
    for f_x, f_y in fields:
        if (sea):
            paint_cell(f_x, f_y, 4)
            game[players[current_player[0]].x][players[current_player[0]].y] = 4
        else:
            paint_cell(f_x, f_y, game[(f_x-1)%width][(f_y-1)%height])
    
# 38 up
# 37 left
# 40 down
# 39 right
    
def repaint(event):
    if (37 <= event.keycode <=40):
        
        if (event.keycode == 39):
            if empty_cell((players[current_player[0]].x + 1) % width, players[current_player[0]].y):
                repaint_cell()
                players[current_player[0]].x = (players[current_player[0]].x + 1) % width
            else: return

        if (event.keycode == 37):
            if empty_cell((players[current_player[0]].x - 1) % width, players[current_player[0]].y):
                repaint_cell()
                players[current_player[0]].x = (players[current_player[0]].x - 1) % width
            else: return
        if (event.keycode == 38):
            if empty_cell((players[current_player[0]].x) % width, players[current_player[0]].y - 1):
                repaint_cell()
                players[current_player[0]].y = (players[current_player[0]].y - 1) % height
            else: return
        if (event.keycode == 40):
            if empty_cell((players[current_player[0]].x) % width, players[current_player[0]].y + 1):
                repaint_cell()
                players[current_player[0]].y = (players[current_player[0]].y + 1) % height
            else: return
            
        paint_all_start_field()
       
        if check_lose():
            show_lose_message()
            exit()
        if check_win():
            show_win_message()
            exit()

        for text_id in cur_exit.text_id:
            canv.delete(text_id)

        
        cur_exit.x = (cur_exit.x + fx()) % width
        cur_exit.y = (cur_exit.y + fy()) % height       

        paint_exit_field()
        
        if check_lose():
            show_lose_message()
            exit()       
        if check_win():
            show_win_message()
            exit()

        current_player[0] = (current_player[0]+1)%number_players
        fields = get_fields(players[current_player[0]].x + 1, players[current_player[0]].y + 1)
        players[current_player[0]].text_id.extend(canv.create_rectangle(size_cell * f_x + 2, size_cell * f_y + 2,
                                                                    size_cell + size_cell * f_x - 2, size_cell + size_cell * f_y - 2,
                                                                    width = size_cell/6, outline ='black') for f_x, f_y in fields)



def check_win():
    for i in range(number_players):
        if cur_exit.x == players[i].x and cur_exit.y == players[i].y:
            print('Win')
            return i+1
    return 0

def check_lose():
    for i in range(number_players):
        if game[cur_exit.x][cur_exit.y] == 4 or game[players[i].x][players[i].y] == 4:
            print('Lose!')
            return i+1
    return 0

def show_win_message():
    pass

def show_lose_message():
    pass

def paint_cell(x, y, z):
    if (x == 0 or y == 0 or x == width + 1 or y == height + 1): 
        if z == 4:
             canv.create_rectangle(size_cell * x, size_cell * y, size_cell + size_cell * x, size_cell + size_cell * y, fill = 'blue')
        else:
             canv.create_rectangle(size_cell * x, size_cell * y, size_cell + size_cell * x, size_cell + size_cell * y, fill = '#C0C0C0')
    else:
        canv.create_rectangle(size_cell * x, size_cell * y, size_cell + size_cell * x, size_cell + size_cell * y, fill = backgrounds[z])
    board[x][y] = canv.create_text(size_cell * x + size_cell/2, size_cell * y + size_cell/2, text = arrows[z], font = font) 

def paint_all_start_field():
    for i in range(number_players):
        paint_start_field(i)

def paint_start_field(i):
    fields = get_fields(players[i].x + 1, players[i].y + 1)
    for f_x, f_y in fields:
        canv.delete(board[f_x][f_y]) # удаляем стрелку на месте нашего положения
    players[i].text_id = [canv.create_text(size_cell * f_x + size_cell/2,
                                                       size_cell * f_y + size_cell/2, text = player_char[i], font = font) for f_x, f_y in fields]

def paint_exit_field():   
    fields = get_fields(cur_exit.x + 1, cur_exit.y + 1)
    cur_exit.text_id = [canv.create_rectangle(size_cell * f_x + 2, size_cell * f_y + 2, size_cell + size_cell * f_x - 2,
                                              size_cell + size_cell * f_y - 2, width = size_cell/6, outline ='red') 
                        for f_x, f_y in fields]


def first_paint():
    for i in range(width + 2):
        for j in range(height + 2):
           paint_cell(i, j, game[(i-1)%width][(j-1)%height])
    paint_all_start_field()
    fields = get_fields(players[current_player[0]].x + 1, players[current_player[0]].y + 1)
    players[current_player[0]].text_id.extend(canv.create_rectangle(size_cell * f_x + 2, size_cell * f_y + 2,
                                                                size_cell + size_cell * f_x - 2, size_cell + size_cell * f_y - 2,
                                                                width = size_cell/6, outline ='black') for f_x, f_y in fields)
    paint_exit_field()
    canv.create_rectangle(size_cell, size_cell, (width + 1) * size_cell, (height + 1) * size_cell, width = size_cell/10)
    

   
  

first_paint()
root.bind("<KeyPress>", repaint)
root.mainloop()
