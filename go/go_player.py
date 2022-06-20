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

    """
    def __init__(self,
                name : str,  
                rank : int=30, 
                ):
        self.name = name 
        self.rank = rank 

class Move:
    r"""A class that represents a go player, in a given game.

    Attributes
    ----------
    position = Tuple[int, int] 
        position of the move
    color = str
        its color 
    
    Methods
    -------

    """
    def __init__(self,
                position,
                color,
                ):
        self.position = position
        self.color = color 

