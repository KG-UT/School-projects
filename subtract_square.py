"""Implementation of the game subtract square, and game state of
Subtract square. This is a subclass of GenericGame, and
CurrentState respectively.
"""
from typing import List, Any
from  generic_game import GenericGame, CurrentState

class SubtractSquare(GenericGame):
    """Represents the game subtract square."""
    current_state: 'SubtractSquareState'
    current_num: str

    def __init__(self, player: bool) -> None:

        """Initializes the game subtract square, by setting the
         starting player and number."""
        self.current_num = input("please select a number to begin with: ")
        while not self.current_num.isdigit():
            self.current_num = input("please select a number to begin with: ")
        if player:
            self.current_state = SubtractSquareState('p1',
                                                     int(self.current_num))
        else:
            self.current_state = SubtractSquareState('p2',
                                                     int(self.current_num))

    def get_instructions(self) -> str:
        """returns the instructions for the game. Examples ommited
        because __init__ of SubtractSquare requires input.
        """
        instructions = """Start from a number. Take turns inputting squares
of numbers to subtract from it. Make the number reach 0 to win."""
        return instructions




class SubtractSquareState(CurrentState):
    """represents the current state of the game subtract square."""
    number: int
    player: str

    def __init__(self, player: str = 'p1', number: int = '57'):
        """initializes the current state of the game subtract square.
        >>> s = SubtractSquareState(number=500)
        >>> s.player == 'p1'
        True
        >>> s.number == 500
        True"""
        self.number = number
        self.player = player

    def get_possible_moves(self) -> List[str]:
        """returns a list of all possible moves.
        >>> s = SubtractSquareState(number=20)
        >>> s.get_possible_moves()
        ['1', '4', '9', '16']"""
        natural = 1
        possible_moves = []
        while natural**2 <= self.number:
            possible_moves.append(str(natural**2))
            natural += 1
        return possible_moves

    def make_move(self, move: str) -> 'SubtractSquareState':
        """makes a move. Returns a new SubtractSquareState.
        >>> s = SubtractSquareState()
        >>> y = s.make_move('25')
        >>> print(y)
        p2 turn to move. Current number is 32"""
        if self.player == 'p1':
            return SubtractSquareState('p2', int(self.number) - int(move))
        return SubtractSquareState('p1', int(self.number) - int(move))

    def __str__(self) -> str:
        """A string represention of SubtractSquareState
        >>> s = SubtractSquareState()
        >>> print(s)
        p1 turn to move. Current number is 57
        """
        return ("{} turn to move. Current number is {}".format(self.player,
                                                               self.number))

    def __eq__(self, other: Any) -> bool:
        """Returns True iff both game states have the same type,
        current number, and current player.
        >>> s = SubtractSquareState()
        >>> t = SubtractSquareState()
        >>> s == t
        True
        >>> y = SubtractSquareState('p2')
        >>> s == y
        False
        """
        return (type(self) == type(other) and self.number == other.number
                and self.player == other.player)

if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config='a1_pyta.txt')
