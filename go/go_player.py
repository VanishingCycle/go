from typing import Tuple 

class GlobalPlayer: 

    r"""A class that represents a go player.

    Attributes
    ----------
    name = str 
        player's name 
    rank = int 
        player's rank
    
    Methods
    -------

    get_local = LocalPlayer
        create a class LocalPlayer

    """
    def __init__(self,
                name : str,  
                rank : int=30, 
                ):
        self.name = name 
        self.rank = rank 
    
    def get_local(self, game_color):
        return LocalPlayer(name = self.name, rank = self.rank, color = game_color) 

class LocalPlayer:
    r"""A class that represents a go player, in a given game.

    Attributes
    ----------
    name = str 
        player's name 
    rank = int 
        player's rank
    move = Tuple[int, int] 
        a move the player wants to make
    color = str
        its color 
    prisonners = int 
        number of prisonners 
    
    Methods
    -------

    """
    def __init__(self,
                color,
                name : str,  
                rank : int=30, 
                move : Tuple[int, int] = [-1,-1],
                prisonners : int = 0,
                ):
        self.color = color 
        self.name = name 
        self.rank = rank 
        self.move = move
        self.prisonners = prisonners 

