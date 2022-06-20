from turtle import update
from go_player import GlobalPlayer
from go_player import Move 
from move_handler import MoveHandler
from typing import Tuple

class GoBoard:
    r"""An object that represents the go board.  

        Attributes
        ----------
        keep_playing: bool
            whether the game has ended
        turn : int
            number of turn of the current game
        komi : int 
            value of the komi 
        history : list
            history of the previous moves
        groups : list 
            list of the different groups of stones
        handicap : int 
            handicap given to black 
        one_pass : bool 
            if one player passed
        

        Methods
        -------

        update_move() : 
            receive a move and update it if legit
        check_history() : 
            check the history
        boundary_point() : 
            return the boundary points surrounding a given point  
        update_groups() : 
            update the list of groups 

    """

    def __init__(self, 
            black: GlobalPlayer, 
            white: GlobalPlayer, 
            move_handler: MoveHandler,
            keep_playing: bool = True, 
            komi: float=6.5, 
            turn: int=0,
            handicap: int=0,
            one_pass : bool = False, 
            prisonners_captured_by_black : int=0,
            prisonners_captured_by_white : int=0,
            ):

        self.white = white
        self.black = black
        self.move_handler = move_handler 
        self.komi = komi
        self.keep_playing = keep_playing 
        self.turn = turn 
        self.handicap = handicap 
        self.one_pass = one_pass 
        self.prisonners_captured_by_black = prisonners_captured_by_black
        self.prisonners_captured_by_white = prisonners_captured_by_white

    def checkMove(self, move:Move) -> bool :
        if self.move_handler.goban[move.position[0]][move.position[1]] != "void" : 
            print("You need to play on an empty intersection")
            return False
        elif not self.move_handler.check_capture(move) : 
            if not self.move_handler.check_suicide(move) : 
                return True 
            else : 
                print("Suicidal move!") 
                return False 
        else : 
            if self.move_handler.check_ko(move) : 
                print("Illegal move (ko)")
                return False 
            else : 
                return True 

    def update_groups(self, move=Move): 
        boundary = self.move_handler.boundary_point(move.position)
        old_groups = []
        new_group = []
        for u in boundary: 
            if self.move_handler.goban[u[0]][u[1]] == move.color : 
                for y in self.move_handler.groups:
                    if u in y : 
                        old_groups.append(y)
        if old_groups: 
            for g in old_groups: 
                for a in g : 
                    new_group.append(a)
                self.move_handler.groups.remove(g)
            new_group.append(move.position) 
            self.move_handler.groups.append(new_group)
        else: 
            self.move_handler.groups.append([move.position])

    def update_move(self, move:Move):
        self.move_handler.goban[move.position[0]][move.position[1]] = move.color
        captured_groups = self.move_handler.check_capture(move)
        for g in captured_groups: 
            for y in g :
                self.move_handler.goban[y[0]][y[1]] = "void"
                if move.color == "black" : 
                    self.prisonners_captured_by_black +=1 
                else : 
                    self.prisonners_captured_by_white +=1 
        for g1 in self.move_handler.groups : 
            if g1 in captured_groups : 
                self.move_handler.groups.remove(g1)
        self.move_handler.history.append(self.move_handler.goban)
        self.update_groups(move)

    def convert_position(self, s = str):
        a = ord(s[0]) - 64 
        b = int(s[1:]) 
        position = (a,b)
        return position 

    def count_points(self): #once no dead group remains 
        black_points = 0
        white_points = 0 
        for i in range(self.move_handler.size[0]) :
            for j in range(self.move_handler.size[1]):  
                if self.move_handler.goban[i][j] == "void":
                    g = self.move_handler.find_empty_group((i,j))
                    if self.move_handler.color_group(self.move_handler.boundary_group(g)) == "black":
                        black_points+= len(g)
                        for a in g: 
                            self.move_handler.goban[a[0]][a[1]] = "black"
                    elif self.move_handler.color_group(self.move_handler.boundary_group(g)) == "white": 
                        white_points+= len(g)
                    for a in g: 
                        self.move_handler.goban[a[0]][a[1]] = "white"
                else : 
                    for a in g: 
                        self.move_handler.goban[a[0]][a[1]] = "black"
        white_points += self.komi 
        white_points += self.prisonners_captured_by_white
        black_points += self.prisonners_captured_by_black
        x = [black_points,white_points]
        return x

    def input_move(self, color_player) -> str: 
            x = input("move?")
            if x == "pass": 
                self.turn+=1
                return "pass"
            else : 
                move = Move(color = color_player, position = self.convert_position(x))
                if self.checkMove(move): 
                    return x 
                else : 
                    return "invalid move"        

    def play_once(self, color_player):
        a = self.input_move(move, color_player)
        if a == "invalid move": 
            pass 
        elif a == "pass" : 
            if self.one_pass == True :
                self.keep_playing = False 
            elif self.one_pass == False :
                self.one_pass = True 
                self.turn +=1 
            else : 
                move = Move(color = color_player, position = self.convert_position(a))
                self.update_move(move) 

    def play(self) : 
        for a in range(self.handicap): 
            self.play_once(self.black)
        while self.keep_playing:
            if self.turn%2 ==0: 
                a = self.play_once(self.black)
                if a == "invalid move" : 
                    break
                elif a == "pass" : 
                    pass 
                else : 
                    self.update_move(self.black) 
            else : 
                a = self.play_once(self.white)
                if a == "invalid move": 
                    break
                elif a == "pass" : 
                    pass 
                else : 
                    self.update_move(self.white)
        dead_groups = []
        for g in self.move_handler.groups : 
            a = input("is the group dead? \"(Y/N)\"")
            if a == "Y" : 
                self.move_handler.groups.remove(g)
                dead_groups.append(g)
        for g in dead_groups:                           
            if self.move_handler.color_group(g) == "white":
                for p in g: 
                    self.move_handler.goban[p[0]][p[1]] = "void"
                self.black.prisonners += len(g)
            elif self.move_handler.color_group(g) == "black":
                for p in g: 
                    self.move_handler.goban[p[0]][p[1]] = "void"
                self.white.prisonners += len(g)
        x = self.count_points()
        if x[0] > x[1] : 
            print("Black wons by ", x[0] - x[1], " points. Black :", x[0], ". White : ", x[1])
        else : 
            print("White wons by ", x[1] - x[0], " points. Black :", x[0], ". White : ", x[1])

