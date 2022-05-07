from go.go_player import GoPlayer

class GoBoard:
    r"""An object that represents the go board. 
        
        Attributes
        ----------
        black: GoPlayer
            the black player
        white: GoPlayer
            the white player
        size: Tuple[int,int]
            the size of the board.
        has_ended: bool
            whether the game has ended

        Methods
        -------

    """

    def __init__(self, 
            black: GoPlayer, 
            white: GoPlayer, 
            size:int=(19,19), 
            komi:int=6.5, 
            *argv):

        self.size = size
        self.komi = komi
        self.black = black
        self.white = white
        self.has_ended = False
