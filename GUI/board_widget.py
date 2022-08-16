import time # timing
import threading # do multiple loops at once
import numpy as np # numbers
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

import board
from .button import PicButton

class Board_Widget(QWidget): 
    def __init__(self, parent):        
    # basic initialize
        super(Board_Widget, self).__init__(parent) # initialize
        self.board = board.Board()
        self.turn = 1
        self.init_UI()
        self.window = parent
        self.run()
        
    def init_UI(self):
    # layout that could contain title text, etc., if I add it
        self.layout = QGridLayout(self)
    # the title
        # label = QLabel("Checkers")
        # self.layout.addWidget(label,0,0,alignment=Qt.AlignHCenter)
        # # print(label.height())
        # label.resize(label.width(), 25)
        # label.setFont(QFont('Arial', 15))
        # label.setStyleSheet('color : white')
    # the widget with the board
        self.board_widget = QWidget()
        self.layout.addWidget(self.board_widget,1,0)
        # size
        # self.board_widget.setFixedHeight(768)
        # self.board_widget.setFixedWidth(768)
        # layout
        self.blayout = QGridLayout(self)
        self.board_widget.setLayout(self.blayout)
        self.blayout.setSpacing(1)
        
        self.message_label= QLabel("")
        self.layout.addWidget(self.message_label,2,0,alignment=Qt.AlignHCenter)
        self.message_label.setFont(QFont('Arial', 15))
        self.message_label.setStyleSheet('color : white')
        self.message_label.resize(self.message_label.width(), 25)
        
        self.import_images()
        self.draw()
        self.update()
        
    def display(self, message):
        self.message_label.setText(message)


    def import_images(self):
        self.red_king_blue = QPixmap('GUI/Images/Red_King_Blue.jpg')
        self.red_king_black =  QPixmap('GUI/Images/Red_King_Black.jpg')
        self.red_king_green =  QPixmap('GUI/Images/Red_King_Green.jpg')
        self.white_king_blue = QPixmap('GUI/Images/White_King_Blue.jpg')
        self.white_king_black =  QPixmap('GUI/Images/White_King_Black.jpg')
        self.white_king_green =  QPixmap('GUI/Images/White_King_Green.jpg')
        self.red_regular_blue = QPixmap('GUI/Images/Red_Regular_Blue.jpg')
        self.red_regular_black =  QPixmap('GUI/Images/Red_Regular_Black.jpg')
        self.red_regular_green =  QPixmap('GUI/Images/Red_Regular_Green.jpg')
        self.white_regular_blue = QPixmap('GUI/Images/White_Regular_Blue.jpg')
        self.white_regular_black =  QPixmap('GUI/Images/White_Regular_Black.jpg')
        self.white_regular_green =  QPixmap('GUI/Images/White_Regular_Green.jpg')
        self.white_background = QPixmap('GUI/Images/White_Background.jpg')
        self.black_background = QPixmap('GUI/Images/Black_Background.jpg')
        self.blue_background = QPixmap('GUI/Images/Blue_Background.jpg')
        self.green_background = QPixmap('GUI/Images/Green_Background.jpg')
        self.lightblue_background = QPixmap('GUI/Images/Lightblue_Background.jpg')
        self.yellow_background = QPixmap('GUI/Images/Yellow_Background.jpg')


        self.image_key =\
                    {-1: [  self.white_background,      self.white_background], # white square
                    0 : [   self.black_background,      self.green_background], # empty black square
                    1 : [   self.white_regular_black,   self.white_regular_blue], # white piece
                    2 : [   self.red_regular_black,     self.red_regular_blue], # red piece
                    10: [   self.white_king_black,      self.white_king_blue],
                    20: [   self.red_king_black,        self.red_king_blue]}
                    
        self.selected_image_key =\
                    {0 :[   self.yellow_background,     self.green_background], # empty black square
                    1 : [   self.white_regular_blue,    self.white_regular_green], # white piece
                    2 : [   self.red_regular_blue,      self.red_regular_green], # red piece
                    10: [   self.white_king_blue,       self.white_king_green],
                    20: [   self.red_king_blue,         self.red_king_green]}
        
    def draw(self):
        self.buttons = [[None]*8]*8
        for r in range(8):
            for c in range(8):
                images = self.image_key[self.board.b[r][c]]
                button = PicButton(images)
                button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
                button.setCheckable(False)
                button.setEnabled(False)
                self.buttons[r][c]=button
                self.blayout.addWidget(self.buttons[r][c],r,c)
        # print(self.b.b)
        if (self.board.b!=1).all() and (self.board.b!=10).all():
            self.display("Red Wins!")
        elif (self.board.b!=2).all() and (self.board.b!=20).all():
            self.display("White Wins!")
        elif self.turn == 1:            
            self.display("White's Turn")
        else:
            self.display("Red's Turn")
    # def update(self):
    #     for row in range(8):
    #         for col in range(8):
    #             # print(r,c)
    #             self.blayout.addWidget(self.buttons[row][col],row,col)


    def run(self,enable=True):
        # pass
        self.board.show()
        if not enable:
            return
        for r in range(8):
            for c in range(8):
                piece_code = self.board.b[r][c]
                if (piece_code==self.turn or piece_code==self.turn*10) and len(self.board.valid_moves([r,c]))>0:
                    print(r,c)
                    images = self.selected_image_key[piece_code]
                    button = PicButton(images)
                    button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
                    button.setCheckable(True)
                    button.setEnabled(True)
                    button.clicked.connect(self.make_piece_clicker(r,c))
                    self.buttons[r][c]=button
                    self.blayout.addWidget(self.buttons[r][c],r,c)
        # self.update()

    def make_piece_clicker(self,row,col):
        def piece_clicker():
            self.draw()
            self.run()
            piece_code = self.board.b[row][col]
            images = self.selected_image_key[piece_code]
            button = PicButton(images)
            button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            button.setCheckable(True)
            button.setChecked(True)
            # button.setEnabled(False)
            button.clicked.connect(self.make_piece_clicker(row,col))
            self.buttons[row][col]=button
            self.blayout.addWidget(self.buttons[row][col],row,col)
            for move in self.board.valid_moves([row,col]):
                [r,c]=move
                # color = self.i
                images = self.selected_image_key[0]
                button = PicButton(images)
                button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
                button.setCheckable(True)
                if (np.abs(row-r)==1):
                    button.clicked.connect(self.make_step_clicker(row,col,r,c))
                else:
                    button.clicked.connect(self.make_skip_clicker(row,col,r,c))
                self.buttons[r][c]=button
                self.blayout.addWidget(self.buttons[r][c],r,c)
        return piece_clicker
    
    def make_step_clicker(self, prow, pcol, row, col):
        def blank_step_clicker():
            self.board.move([prow,pcol],[row,col],end_turn=True)
            self.turn = 3 - self.turn
            print("board.move("+str([prow,pcol])+","+str([row,col])+")")
            self.draw()
            self.run(enable=True)
            print([prow,pcol],[row,col])
        return blank_step_clicker

    def display(self, message):
        self.message_label.setText(message)
    
    def make_skip_clicker(self,prow,pcol,row,col):
        def blank_skip_clicker():
            next_skips = self.board.skip_moves([row,col],self.board.at([prow,pcol]))
            self.board.move([prow,pcol],[row,col],end_turn=(len(next_skips)==0))
            
            print("board.move("+str([prow,pcol])+","+str([row,col])+")")
            # self.turn = 3 - self.turn
            if len(next_skips)==0:
                self.turn = 3 - self.turn
                self.draw()
                self.run(enable=True)
            else:
                self.draw()
                self.run(enable=False)
                for move in next_skips:

                    [r,c]=move
                    # color = self.i
                    images = self.selected_image_key[0]
                    button = PicButton(images)
                    button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
                    button.setCheckable(True)
                    button.clicked.connect(self.make_skip_clicker(row,col,r,c))
                    self.buttons[r][c]=button
                    self.blayout.addWidget(self.buttons[r][c],r,c)
            
                def end_fun():
                    self.turn = 3 - self.turn
                    self.board.turn = self.turn
                    self.draw()
                    self.run(enable=True)
                    
                # color = self.i
                images = self.selected_image_key[self.board.at([row,col])]
                button = PicButton(images)
                button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
                button.setCheckable(True)
                button.clicked.connect(end_fun)
                self.buttons[row][col]=button
                self.blayout.addWidget(self.buttons[row][col],row,col)
            
        return blank_skip_clicker

    def comp_move(self,n):
        f = self.make_clicker(n)
        f()
        
    def delay_set(self,n):
        def f():
            time.sleep(0.5)
            self.buttons[n].setText("O")
            self.buttons[n].setEnabled(False)

        loop = threading.Thread(target=f)
        loop.start()    
        
    def message(self, m):
        self.message_spot.setText(m)