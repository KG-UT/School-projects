"""Implementation of a generic game class, and a generic game state class.
 They are superclasses of all specific game classes and game state classes,
  such as the ones representing the game subtract square, or the one
  representing chopsticks.
"""


from typing import Any
class GenericGame:
    """Represents a generic two player, sequential move, zero-sum,
    perfect information game."""
    current_state: 'CurrentState'

    def __init__(self, player: bool) -> None:
        """Initialize the game, setting the starting player and current state"""
        if player:
            self.current_state = CurrentState('p1')
        else:
            self.current_state = CurrentState('p2')

    def get_instructions(self)-> None:
        """returns the instructions on how to play"""
        raise NotImplementedError("Instructions available in subclass.")

    def str_to_move(self, something: str) -> str:
        """Converts something into a move that can be done.
        >>> s = GenericGame(True)
        >>> s.str_to_move('move two steps forward')
        'move two steps forward'"""
        return something

    def is_over(self, state: "CurrentState") -> bool:
        """returns True if there are no possible moves left in the current
        state. False otherwise. Only available for subclasses of GenericGame."""
        return state.get_possible_moves() == []

    def is_winner(self, player: str) -> bool:
        """returns True if game is finished, and player is the winner.
        Only available for subclasses of GenericGame."""
        if self.current_state.get_possible_moves() == []:
            if player == 'p1':
                return 'p2' == self.current_state.get_current_player_name()
            return 'p1' == self.current_state.get_current_player_name()
        return False

    def __eq__(self, other: Any) -> bool:
        """compares if self and other are both the same game,
         and if they have the same current_state.
        >>> c = GenericGame(True)
        >>> s = GenericGame(True)
        >>> c == s
        True
        >>> k = GenericGame(False)
        >>> c == k
        False"""
        return (type(self) == type(other) and
                self.current_state == other.current_state)

    def __str__(self) -> str:
        """returns a string representation of the game in terms of its
        current state.
        >>> x = GenericGame(True)
        >>> print(x)
        A generic game. There is no current game state."""
        return str(self.current_state)

class CurrentState:
    """A generic current_state of a game."""
    player: str

    def __init__(self, player: str = 'p1'):
        """initializes the current_state, and sets the
         current player to player.
         >>> s = CurrentState()
         >>> s.player == 'p1'
         True"""
        self.player = player

    def get_possible_moves(self) -> None:
        """returns a list of the possible moves"""
        raise NotImplementedError("Possible moves available in subclass.")

    def make_move(self, move: str) -> None:
        """Makes the move given."""
        raise NotImplementedError("Available in subclass.")

    def is_valid_move(self, move: str) -> bool:
        """returns True iff move given is valid.
        Only available in subclasses of CurrentState."""
        return move in self.get_possible_moves()

    def get_current_player_name(self):
        """returns the current player
        >>> s = CurrentState()
        >>> s.get_current_player_name()
        'p1'"""
        return self.player

    def __str__(self) -> str:
        """A string representation of this class.
        >>> s = CurrentState()
        >>> print(s)
        A generic game. There is no current game state."""
        return "A generic game. There is no current game state."

    def __eq__(self, other: Any)-> None:
        """Compares if this is the same type as another object,
        and if they have the same player.
        >>> s = CurrentState()
        >>> q = CurrentState()
        >>> s == q
        True
        >>> t = CurrentState('p2')
        >>> s == t
        False"""
        return (type(self) == type(other) and
                self.player == other.player)

if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
