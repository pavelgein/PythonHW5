import tkinter
from tkinter import *
from random import choice, sample
from itertools import product
from .messages import Message


sea = 1

arrows = ['\u2190', '\u2191', '\u2192', '\u2193', '\u224b'] # left, up, right, down, sea
backgrounds = ['#90EE90', '#90EE90', '#90EE90', '#90EE90', 'blue'] # left, up, right, down, sea

class Field():
    def __init__(self, x, y, text_id = None):
        self.x = x
        self.y = y

class Player():
    def __init__(self, field, char = None, name = None, pl_id = None):
        self.x = field.x
        self.y = field.y
        self.char = char
        self.name = name
        self.id = pl_id


class Game():
    def __init__(self, number_players = 2, names = ['1', '2'], height = 3, width = 30):
        self.height = height
        self.width = width

        self.game = self.create_game()
        
        self.number_players = number_players
        self.players = []
        self.players = [Player(field = self.gen_good(), char = str(i + 1), name = names[i], pl_id = i) for i in range(number_players)]
        self.current_player = self.players[0]

        self.cur_exit = self.gen_good()



    def get_next_player(self):
        return (self.current_player.id + 1) % self.number_players

    def set_next_player(self):
        self.current_player = self.players[self.get_next_player()]

    def gen_good(self):
        while True:
            x = choice(range(self.width))
            y = choice(range(self.height))
            if self.game[y][x] != 4 and not Player(Field(x, y)) in self.players:
                return Field(x, y)
    

    def create_game(self):
        return [[choice(range(3)) for i in range(self.width)] for j in range(self.height)]


    def get_fields(self, x, y):
        x %= self.width
        y %= self.height
        ans = [(x, y)]
        if x <= 1:
            ans.append((x + self.width, y))
        if y <= 1:
            ans.append((x, y + self.height))
        if x <= 1 and y <= 1:
            ans.append((x + self.width, y + self.height))
        return ans

    def fx(self, field):
        if self.game[field.y][field.x] == 0:
            return -1
        if self.game[field.y][field.x] == 2:
            return 1
        return 0

    def fy(self, field):
        if self.game[field.y][field.x] == 3:
            return 1
        if self.game[field.y][field.x] == 1:
            return -1
        return 0

    def empty_cell(self, x, y):
        return all(x != player.x or y != player.y for player in self.players)

    def start(self):
        self.first_paint()
        self.window.bind("<KeyPress>", self.repaint)
        self.window.mainloop()

    def repaint_cell(self):
        cur_player = self.current_player
        for text_id in cur_player.text_id:
            self.canv.delete(text_id)
        fields = self.get_fields(cur_player.x + 1, cur_player.y + 1)
        for f_x, f_y in fields:
            if sea:
                self.paint_cell(f_x, f_y, 4)
                self.game[cur_player.y][cur_player.x] = 4
            else:
                self.paint_cell(f_x, f_y, self.game[(f_y - 1) % self.width][(f_x - 1) % self.height])

    def check_turn(self, code):
        if (code < 37 and code > 40):
            return False
        cur_player = self.current_player
        target_x = (cur_player.x + dx(code)) % self.width
        target_y = (cur_player.y + dy(code)) % self.height
        return self.empty_cell(target_x, target_y)

    def make_turn(self, code):
        if (code < 37 and code > 40):
            return False
        cur_player = self.current_player
        target_x = (cur_player.x + dx(code)) % self.width
        target_y = (cur_player.y + dy(code)) % self.height
        if self.empty_cell(target_x, target_y):
            cur_player.x = target_x
            cur_player.y = target_y
            return True
        return False

    def move_exit(self):
        cur_player = self.current_player
        self.cur_exit.x = (self.cur_exit.x + self.fx(cur_player)) % self.width
        self.cur_exit.y = (self.cur_exit.y + self.fy(cur_player)) % self.height

    

    def check_win(self):
        for player in self.players:
            if self.cur_exit.x == player.x and self.cur_exit.y == player.y:
                return True
        return False

    def check_lose(self):
        for player in self.players:
            if self.game[self.cur_exit.y][self.cur_exit.x] == 4 or self.game[player.y][player.x] == 4:
                return True
        return False
   
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

if __name__ == '__main__':
    game = Game()
    game.start()
  

# game = Game()
# game.start()


