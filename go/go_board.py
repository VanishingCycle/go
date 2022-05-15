from go_player import GoPlayer
from typing import Tuple

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
            size: Tuple[int, int]=(19,19), 
            komi: float=6.5, 
            *argv):

        self._size = size
        self._komi = komi
        self._black = black
        self._white = white
        self._has_ended = False

    def update_move(move: str):
        pass

    def update_move(move: Tuple[int, int]):
        pass

    def check_history(numOfMoves: int) -> List[str]:
        pass
