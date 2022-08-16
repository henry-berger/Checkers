import numpy as np

class Board():
    def __init__(self):
        self.b = np.zeros([8,8])
        self.place_pieces()
        self.key = {-1: "   ",0:" - ",1:" W ", 2:" B ",10: " Wk", 20: " Bk"}
        self.turn = 1
        
    # 1 for white, 2 for black, 0 for empty, -1 for inaccessible
    def place_pieces(self):
        for r in range(3):
            for c in range(8):
                if (r+c)%2==1:
                    self.b[r][c]=1
                    self.b[7-r][7-c]=2
        for r in range(8):
            for c in range(8):
                if (r+c)%2==0:
                    self.b[r][c]=-1             
                    
    def show(self):
        pass
        print("Board:")
        for row in self.b:
            print_line = "\t"
            for c in row:
                print_line = print_line + self.key[c]
            print(print_line)
        print()
            
    def valid_move(self,start, end,turn):
        valid_piece = self.at(start)==turn or self.at(start)==turn*10
        good_move = end in self.valid_moves(start)
        if not valid_piece:
            print("Invalid piece")
            print(self.at(start), turn)
        if not good_move:
            print("Invalid destination")
        return valid_piece and good_move
    
    def move(self, start, end, end_turn = True):
        if not self.valid_move(start, end, self.turn):
            print("Invalid move")
            print("Valid Moves: ")
            print(self.valid_moves(start))
            return
        
        if end[0]==0 or end[0]==7:
            self.setto(end,self.turn*10)
        else:
            self.setto(end,self.at(start))
        if np.abs(start[0]-end[0])>1:
           mid = [int((start[0]+end[0])/2),int((start[1]+end[1])/2)]          
           self.setto(mid,0)
        if end_turn:
            self.turn = 3 - self.turn            
        self.setto(start,0)
        self.show()


            
    # returns the value of board at point=[r,c]
    def at(self, point):
        return self.b[point[0]][point[1]]
    
    def setto(self, point, val):
        self.b[point[0]][point[1]] = val
        
    def find_valid_moves(self,piece,types,set_piece_code=-10):
        [R,C]=piece
        if set_piece_code == -10:
            piece_code = self.at(piece)
        else:
            piece_code = set_piece_code
        # Direction
        if piece_code==1: #white
            vdirs = [1]
        elif piece_code==2: #black
            vdirs = [-1]
        elif piece_code==10 or piece_code==20: # king
            vdirs = [-1,1]
            piece_code = piece_code / 10
        else:
            return [[]]
        hdirs = [-1,1]        
        on_board_moves = []
        on_board_skips = []
        single_moves = []
        skip_moves = []
        all_moves = []
        for vdir in vdirs:
            for hdir in hdirs:
                r, c = R+vdir, C+hdir
                r2,c2 = R+2*vdir, C+2*hdir
                if min(r,c)>=0 and max(r,c)<8:
                    if self.at([r,c])==0:
                        single_moves.append([r,c])
                        all_moves.append([r,c])
                    elif (
                            (self.at([r,c])==3-piece_code) or
                            (self.at([r,c])==10*(3-piece_code))
                        )\
                    and (min(r2,c2)>=0 and max(r2,c2)<8)\
                    and self.at([r2,c2])==0:
                        skip_moves.append([r2,c2])
                        all_moves.append([r2,c2])
        # print("All moves: ",all_moves)
        # print("All: ",all_moves, "Singles: ",single_moves, "Skip: ", skip_moves)
        if types == "All":
            return all_moves
        if types == "Singles":
            return single_moves
        if types == "Skips":
            return skip_moves
        return []
        return [all_moves, single_moves, skip_moves]
    
    def valid_moves(self, piece):
        return self.find_valid_moves(piece, types="All")
    
    def single_moves(self, piece):
         return self.find_valid_moves(piece, types="Singles")
    
    def skip_moves(self, piece,set_piece_code):
         return self.find_valid_moves(piece,"Skips",set_piece_code)

        # return skips