from __future__ import division
import random
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.graphics import BorderImage, Color
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivy.core.window import Window, Keyboard
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

spacing = 10

colors = (
    'eee4da', 'ede0c8', 'f2b179', 'f59563',
    'f67c5f', 'f65e3b', 'edcf72', 'edcc61',
    'edc850', 'edc53f', 'edc22e')

tile_colors = {2 ** i: color for i, color in
               enumerate(colors, start=1)}

def all_cells():
    for x in range(3):
        for y in range(3):
            yield (x, y)

class Tile(Widget):
    font_size = NumericProperty(24)
    text = StringProperty('')
    color = ListProperty(get_color_from_hex(tile_colors[2]))
    text_color = ListProperty(get_color_from_hex('776e65'))
    
    def __init__(self, text, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.font_size = 0.5 * self.width
        self.text = text
        if self.text == 'O':
            self.text_color = get_color_from_hex(colors[3])
        elif self.text == 'X':
            self.text_color == get_color_from_hex(colors[1])
        
    def resize(self, pos, size):
        self.pos = pos
        self.size = size
        self.font_size = 0.5 * self.width

           
class Board(Widget):
    b = None
    bstatus = None
    turndic = {'O':1, 'X':9}
    turn = 'O'
    tiles = []
    win = False
    winner = StringProperty('Tic Tac Toe')

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.resize()

    def reset(self):
        self.b = [[None for i in range(3)] for j in range(3)]
        self.bstatus = [[0 for i in range(3)] for j in range(3)]
        self.clear_widgets()
        self.win = False
        self.winner = 'Tic Tac Toe'

    def valid_cell(self, board_x, board_y, touch):
          if board_x >= 0 and board_x <= 2 and touch.x > self.pos[0] and \
                   board_y >= 0 and board_y <= 2 and touch.y > self.pos[1]:
              return True
          else:
              return False
              
    def can_move(self, board_x, board_y):
        self.b[board_x][board_y] == None

    def cell_pos(self, board_x, board_y):
        return (self.x + board_x * (self.cell_size[0] + spacing) + spacing,
                        self.y + board_y * (self.cell_size[1] + spacing) + spacing)

    def resize(self, *args):
        self.cell_size = (0.315* (self.width -  spacing), ) *2

        # redraw background
        self.canvas.before.clear()
        with self.canvas.before:
            BorderImage(pos=self.pos, size=self.size, source='board.png')
            Color(*get_color_from_hex('ccc0b4'))
            for board_x, board_y in all_cells():
                BorderImage(pos=self.cell_pos(board_x, board_y),
                            size=self.cell_size, source='cell.png')

        if not self.b:
            return
        for board_x, board_y in all_cells():
            tile = self.b[board_x][board_y]
            if tile:
                tile.resize(pos=self.cell_pos(board_x, board_y),
                            size=self.cell_size)

    on_pos = resize
    on_size = resize
   
    def coord(self, touch):
        x = int((touch.x - self.pos[0])/(self.size[0]/3))
        y = int((touch.y - self.pos[1])/(self.size[1]/3))
        
        if self.valid_cell(x, y, touch):
            return (x, y)
        else:
            return (None, None)
        
    def on_touch_up(self, touch):
        x_coord, y_coord = self.coord(touch)
        print(x_coord, y_coord)
        
        if self.win:
            return
        
        if x_coord != None and self.b[x_coord][y_coord] == None:
            tile = Tile(text=self.turn,pos=self.cell_pos(x_coord, y_coord),
                                  size=self.cell_size)
            self.b[x_coord][y_coord] = tile
            self.bstatus[x_coord][y_coord] = self.turndic[self.turn]
            self.add_widget(tile)
            self.check_win()
            self.toggle_player()
            print(self.bstatus)
          
    def toggle_player(self):
        if self.turn == 'O':
            self.turn = 'X'
        else:
            self.turn = 'O'

    def win_helper(self, score, message):
        for i in range(3):
            if sum(self.bstatus[i]) == score:
                print(message)
                self.win = True
                self.winner = self.turn + ' wins!'
            if sum([self.bstatus[0][i], self.bstatus[1][i], self.bstatus[2][i]]) == score:
                print(message)
                self.win = True
                self.winner = self.turn + ' wins!'
        if sum([self.bstatus[x][x] for x in range(3)]) == score:
            print(message)
            self.win = True
            self.winner = self.turn + ' wins!'
        if sum([self.bstatus[x][2-x] for x in range(3)]) == score:
            print(message)
            self.win = True
            self.winner = self.turn + ' wins!'

    def check_win(self):
        self.win_helper(3, 'Player 1 wins')
        self.win_helper(27, 'Player 2 wins')
                    
class TTTLayout(BoxLayout):
    pass

class tttApp(App):
    def on_start(self):
        board = self.root.ids.board
        board.reset()
    
if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('faf8ef')
    tttApp().run()