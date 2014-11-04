import tkinter
from tkinter import *
from random import choice, sample
from itertools import product


sea = 1

arrows = ['\u2190', '\u2191', '\u2192', '\u2193', '\u224b'] # left, up, right, down, sea
backgrounds = ['#90EE90', '#90EE90', '#90EE90', '#90EE90', 'blue'] # left, up, right, down, sea

class Field():
    def __init__(self, x, y, text_id = None):
        self.x = x
        self.y = y
        self.text_id = text_id

class Player(Field):
    def __init__(self, field, char = None, name = None, pl_id = None):
        self.x = field.x
        self.y = field.y
        self.text_id = field.text_id
        self.char = char
        self.name = name
        self.id = pl_id


class Game():
    def __init__(self, number_players = 2, names = ['1', '2'], height = 10, width = 20, size_cell = 30):
        self.height = height
        self.width = width
        self.size_cell = 30

        self.game = self.create_game()
        self.board = self.create_board()
        
        self.number_players = number_players        
        self.players = []
        self.players = [Player(field = self.gen_good(), char = str(i + 1), name = names[i], pl_id = i + 1) for i in range(number_players)]
        self.current_player = [0]


        self.cur_exit = self.gen_good()

        self.font = 'Arial '+str(int(0.6 * size_cell)) 
        self.window, self.canv = self.init_graphics()


    def gen_good(self):
        while True:
            x = choice(range(self.width))
            y = choice(range(self.height))
            if self.game[x][y] != 4 and not Player(Field(x, y)) in self.players:
                return Field(x, y)
    def create_game(self):
        return [[choice(range(3)) for i in range(self.height)] for j in range(self.width)]

    def create_board(self):
        return [[None for i in range(self.height + 2)] for j in range(self.width + 2)]    

    def init_graphics(self):
        s = str((self.width + 2) * self.size_cell) + 'x' + str((self.height + 2) * self.size_cell)        

        root = Tk()
        root.geometry(s)
        root.title("Догони!")
        canv = Canvas(root, width = (self.width + 2) * self.size_cell, height = (self.height + 2) * self.size_cell)
        canv.pack()
        return root, canv

    def get_fields(self, x, y):
        x %= self.height
        y %= self.width
        ans = [(x, y)]
        if x <= 1:
            ans.append((x + self.width, y))
        if y <= 1:
            ans.append((x, y + self.height))
        if x <= 1 and y <= 1:
            ans.append((x + self.width, y + self.height))
        return ans

    def fx(self, field):
        if self.game[field.x][field.y] == 0:
            return -1
        if self.game[field.x][field.y] == 2:
            return 1
        return 0

    def fy(self, field):
        if self.game[field.x][field.y] == 3:
            return 1
        if self.game[field.x][field.y] == 1:
            return -1
        return 0

    def empty_cell(self, x,y):
        return all(x != player.x or y != player.y for player in self.players)

    def start(self):
        self.first_paint()
        self.window.bind("<KeyPress>", self.repaint)
        self.window.mainloop()

    def repaint_cell(self):
        cur_player = self.players[self.current_player[0]]
        for text_id in cur_player.text_id:
            self.canv.delete(text_id)
        fields = self.get_fields(cur_player.x + 1, cur_player.y + 1)
        for f_x, f_y in fields:
            if sea:
                self.paint_cell(f_x, f_y, 4)
                self.game[cur_player.x][cur_player.y] = 4
            else:
                self.paint_cell(f_x, f_y, self.game[(f_x - 1) % self.width][(f_y - 1) % self.height])


    def repaint(self, event):
        cur_player = self.players[self.current_player[0]]
        target_x = (cur_player.x + dx(event.keycode)) % self.height
        target_y = (cur_player.y + dy(event.keycode)) % self.width
        if (37 <= event.keycode <=40):        
            if self.empty_cell(target_x, target_y):
                self.repaint_cell()
                self.players[self.current_player[0]].x = target_x
                self.players[self.current_player[0]].y = target_y
            else:
                return
                
            self.paint_all_start_field()
           
            if self.check_lose():
                show_lose_message()
                exit()
            if self.check_win():
                show_win_message()
                exit()

            for text_id in self.cur_exit.text_id:
                self.canv.delete(text_id)

            
            self.cur_exit.x = (self.cur_exit.x + self.fx(cur_player)) % self.width
            self.cur_exit.y = (self.cur_exit.y + self.fy(cur_player)) % self.height       

            self.paint_exit_field()
            
            if self.check_lose():
                show_lose_message()
                exit()       
            if self.check_win():
                show_win_message()
                exit()

            self.current_player[0] = (self.current_player[0] + 1) % self.number_players
            fields = self.get_fields(self.players[self.current_player[0]].x + 1, self.players[self.current_player[0]].y + 1)
            self.players[self.current_player[0]].text_id.extend(self.canv.create_rectangle(self.size_cell * f_x + 2, self.size_cell * f_y + 2,
                                                                        self.size_cell + self.size_cell * f_x - 2, self.size_cell + self.size_cell * f_y - 2,
                                                                        width = self.size_cell / 6, outline ='black') for f_x, f_y in fields)

    def check_win(self):
        for player in self.players:
            if self.cur_exit.x == player.x and self.cur_exit.y == player.y:
                print('Win')
                print(player.name)
                return player.id
        return 0

    def check_lose(self):
        for player in self.players:
            if self.game[self.cur_exit.x][self.cur_exit.y] == 4 or self.game[player.x][player.y] == 4:
                print('Lose!'),
                print(player.name)
                return player.id
        return 0

    def paint_cell(self, x, y, z):
        if (x == 0 or y == 0 or x == self.width + 1 or y == self.height + 1): 
            if z == 4:
                 self.canv.create_rectangle(self.size_cell * x, self.size_cell * y, self.size_cell + self.size_cell * x, self.size_cell + self.size_cell * y, 
                                            fill = 'blue')
            else:
                 self.canv.create_rectangle(self.size_cell * x, self.size_cell * y, self.size_cell + self.size_cell * x, self.size_cell + self.size_cell * y, 
                                            fill = '#C0C0C0')
        else:
            self.canv.create_rectangle(self.size_cell * x, self.size_cell * y, self.size_cell + self.size_cell * x, self.size_cell + self.size_cell * y, 
                                       fill = backgrounds[z])
        self.board[x][y] = self.canv.create_text(self.size_cell * x + self.size_cell / 2, self.size_cell * y + self.size_cell / 2, text = arrows[z], font = self.font) 

    def paint_all_start_field(self):
        for player in self.players:
            self.paint_start_field(player)

    def paint_start_field(self, player):
        fields = self.get_fields(player.x + 1, player.y + 1)
        for f_x, f_y in fields:
            self.canv.delete(self.board[f_x][f_y]) # удаляем стрелку на месте нашего положения
        player.text_id = [self.canv.create_text(self.size_cell * f_x + self.size_cell / 2,
                                                self.size_cell * f_y + self.size_cell / 2, 
                                                text = player.char, font = self.font) for f_x, f_y in fields]

    def paint_exit_field(self):   
        fields = self.get_fields(self.cur_exit.x + 1, self.cur_exit.y + 1)
        self.cur_exit.text_id = [self.canv.create_rectangle(self.size_cell * f_x + 2, self.size_cell * f_y + 2, self.size_cell + self.size_cell * f_x - 2,
                                                            self.size_cell + self.size_cell * f_y - 2, width = self.size_cell / 6, outline ='red') 
                                for f_x, f_y in fields]


    def first_paint(self):
        for i in range(self.width + 2):
            for j in range(self.height + 2):
               self.paint_cell(i, j, self.game[(i - 1) % self.width][(j - 1) % self.height])
        self.paint_all_start_field()
        fields = self.get_fields(self.players[self.current_player[0]].x + 1, self.players[self.current_player[0]].y + 1)
        self.players[self.current_player[0]].text_id.extend(self.canv.create_rectangle(self.size_cell * f_x + 2, self.size_cell * f_y + 2,
                                                                                       self.size_cell + self.size_cell * f_x - 2, 
                                                                                       self.size_cell + self.size_cell * f_y - 2,
                                                                                       width = self.size_cell / 6, outline ='black') for f_x, f_y in fields)
        self.paint_exit_field()
        self.canv.create_rectangle(self.size_cell, self.size_cell, (self.width + 1) * self.size_cell, (self.height + 1) * self.size_cell, width = self.size_cell / 10)

   
def dx(key_code):
    if key_code == 39:
        return 1
    if key_code == 37:
        return -1
    return 0

def dy(key_code):
    if key_code == 38:
        return -1
    if key_code == 40:
        return 1
    return 0

def show_win_message():
    pass

def show_lose_message():
    pass     

if __name__ == '__main__':
    game = Game()
    game.start()
  

# game = Game()
# game.start()


