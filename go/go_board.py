from turtle import update
from go_player import LocalPlayer
from go_player import GlobalPlayer
from move_handler import MoveHandler
from typing import Tuple

class GoBoard:
    r"""An object that represents the go board.  

        Attributes
        ----------
        black: LocalPlayer
            the black player
        white: LocalPlayer
            the white player
        size: Tuple[int,int]
            the size of the board.
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
            black_player: GlobalPlayer, 
            white_player: GlobalPlayer, 
            black : LocalPlayer, 
            white : LocalPlayer,
            move_handler: MoveHandler,
            size: Tuple[int, int]=(19,19), 
            keep_playing: bool = True, 
            komi: float=6.5, 
            turn: int=0,
            handicap: int=0,
            one_pass : bool = False, 
            ):

        self.black_player = black_player
        self.white_player = white_player
        self.white = white
        self.black = black
        self.move_handler = move_handler 
        self.size = size
        self.komi = komi
        self.keep_playing = keep_playing 
        self.turn = turn 
        self.white = white_player.get_local("white")
        self.black = black_player.get_local("black")
        self.handicap = handicap 
        self.one_pass = one_pass 

    def checkMove(self, player: LocalPlayer) -> bool :
        if self.move_handler.goban[player.move[0]][player.move[1]] != "void" : 
            print("You need to play on an empty intersection")
            return False
        elif not self.move_handler.check_capture(player) : 
            if not self.move_handler.check_suicide(player) : 
                return True 
            else : 
                print("Suicidal move!") 
                return False 
        else : 
            if self.move_handler.check_ko(player) : 
                print("Illegal move (ko)")
                return False 
            else : 
                return True 

    def update_groups(self, player = LocalPlayer): 
        boundary = self.move_handler.boundary_point(player.move)
        old_groups = []
        new_group = []
        for u in boundary: 
            if self.move_handler.goban[u[0]][u[1]] == player.color : 
                for y in self.move_handler.groups:
                    if u in y : 
                        old_groups.append(y)
        if old_groups: 
            for g in old_groups: 
                for a in g : 
                    new_group.append(a)
                self.move_handler.groups.remove(g)
                new_group.append(player.move)
                self.move_handler.groups.append(new_group)
                print("this is old group", old_groups, "at turn", self.turn)
        else: 
            self.move_handler.groups.append([player.move])

    def update_move(self, player : LocalPlayer):
        self.move_handler.goban[player.move[0]][player.move[1]] = player.color 
        captured_groups = self.move_handler.check_capture(player)
        for g in captured_groups: 
            for y in g :
                self.move_handler.goban[y[0]][y[1]] = "void"
                player.prisonners += 1
        for g1 in self.move_handler.groups : 
            if g1 in captured_groups : 
                self.move_handler.groups.remove(g1)
        self.move_handler.history.append(self.move_handler.goban)
        self.update_groups(player)

    def convert_position(self, s = str):
        a = ord(s[0]) - 64 
        b = int(s[1:]) 
        position = (a,b)
        return position 

    def count_point(self): #once no dead group remains 
        black_point = 0
        white_point = 0 
        for i,j in range(self.size) : 
            if self.move_handler.goban[i][j] == "void": 
                g = self.move_handler.find_empty_group((i,j))
                if self.move_handler.color_group.boundary_group(g) == "black": 
                    black_point+= len(g)
                    for a in g: 
                        self.goban[a[0]][a[1]] = "black"
                if self.move_handler.color_group.boundary_group(g) == "white": 
                    white_point+= len(g)
                    for a in g: 
                        self.goban[a[0]][a[1]] = "white"
        white_point += self.komi 
        white_point += self.white.prisonners
        black_point += self.black.prisonners
        x = [black_point,white_point]
        return x

    def input_move(self, player = LocalPlayer):
            x = input("move?")
            if x == "pass": 
                self.turn+=1
                return "pass"
            else : 
                position = self.convert_position(x)
                player.move = position 
                if self.checkMove(player): 
                    return x
                else : 
                    return "invalid move"        

    def play_once(self, player = LocalPlayer):
        a = self.input_move(player)
        if a == "invalid move": 
            pass 
        elif a == "pass" : 
            if self.one_pass == True :
                self.keep_playing = False 
            elif self.one_pass == False :
                self.one_pass = True 
                self.turn +=1 
            else : 
                self.update_move(self.black) 

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
        x = self.count_point()