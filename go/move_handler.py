from go_player import GlobalPlayer
from go_player import Move 
from typing import Tuple

class MoveHandler:
    r"""A class that oversees the match and handles moves. 
        
        Attributes
        ----------
        goban : list 
            the goban 
        turn : int
            number of turn of the current game
        groups : list 
            list of the different groups of stones
        history : list 
            history of the moves 
        size : Tuple[int,int] 
            size of the go board

        Methods
        -------

        opposite(str) -> str :
            return the opposite color 
        update_move() : 
            receive a move and update it if legit
        check_history() : 
            check the history
        make_move() : 
            add the move to the board 
        boundary_point() : 
            return the boundary points surrounding a given point 
        boundary_group() : 
            return the boundary points surrounding a given group 
        update_groups() : 
            update the list of groups 

    """

    def __init__(self, 
                rule: str = "",
                goban: list = [["void" for x in range(19)] for y in range(19)],
                turn : int = 0, 
                size : Tuple[int,int] = (19,19),
                groups:list = [],
                history: list = [],
                ):
        self.rule = rule 
        self.goban = goban 
        self.turn = turn 
        self.size = size
        self.groups = groups 
        self.history = history

    def opposite(self, s = str) : 
        if s == "black" : 
            return "white"
        elif s == "white" :
            return "black"
        else : 
            print("Error : argument is supposed to be a color")
            return "void"


    def legal_position(self, position) -> bool: 
        if position[0] in range(self.size[0]) and position[1] in range(self.size[1]): 
                return True 
        else : 
            return False 

    def boundary_point (self, position : Tuple[int,int]) : 
        boundary = []
        boundary.append((position[0]-1, position[1]))
        boundary.append((position[0]+1, position[1]))
        boundary.append((position[0], position[1]-1))
        boundary.append((position[0], position[1]+1))
    
        boundary = list(filter( self.legal_position, boundary))

        return boundary
    
    def boundary_group(self, group :list) :
        boundary = []
        for x in group :
            for y in self.boundary_point(x) : 
                if y not in group : 
                    boundary.append(y)
        boundary = list(set(boundary))
        return boundary 
    
    def check_ko(self, move:Move) -> bool: 
        potential_goban = self.goban
        potential_goban[move.position[0]][move.position[1]] = move.color 
        if potential_goban in self.history : 
            return True 
        else : 
            return False

    def check_capture(self, move:Move) -> list : 
        captured_groups = []
        for y in self.boundary_point(move.position) : 
            for g in self.groups :
                if y in g and self.goban[y[0]][y[1]] == self.opposite(move.color) :
                    captured_groups.append(g)
                    for u in self.boundary_group(g) : 
                        if u != move.position and self.goban[u[0]][u[1]] != move.color : 
                            captured_groups.remove(g)
                            break 
        return captured_groups

    def check_suicide(self, move:Move) -> bool: 
        b = self.boundary_point(move.position)
        if all (self.goban[u[0]][u[1]] == self.opposite(move.color) for u in b ):
            return True
        else : 
            return False
    
    def find_empty_group(self, position = Tuple[int,int]) -> list:
        a_group = []
        check_point = [[True for x in range(self.size[0])] for x in range(self.size[1])]
        current_boundary = [position]
        while current_boundary: 
            to_add = []
            for a in current_boundary: 
                a_group.append(a)
                current_boundary.remove(a)
                for b in self.boundary_point(a):
                    if check_point[b[0]][b[1]] and self.goban[b[0]][b[1]] == "void" :
                        to_add.append(b)
                        check_point[b[0]][b[1]] = False
            current_boundary = current_boundary + to_add            
        return a_group 

    #def boundary_group(self, group) -> list: 
    #    boundary_group = []
    #    for x in group: 
    #        for y in self.boundary_point(x): 
    #            if y not in group and y not in boundary_group: 
    #                boundary_group.append(y)
    #    return boundary_group 
    
    def color_group(self, group) -> str: 
        y = group[0]
        for x in group: 
            if self.goban[x[0]][x[1]] != self.goban[y[0]][y[1]]: 
                return "mixed"
        return self.goban[y[0]][y[1]]
