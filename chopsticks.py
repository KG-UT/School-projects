"""Implementation of the game Chopsticks and its respective
game state. These are subclasses of GenericGame and
CurrentState respectively."""
from typing import List, Any, Tuple
from generic_game import GenericGame, CurrentState

class Chopsticks(GenericGame):
    """Represents the game Chopsticks."""
    current_state: 'ChopsticksState'
    INSTRUCTIONS = """Both players start with two hands each with one finger.
Suppose you are the current player. You choose one of your hands to hit theirs
with. Their hand that is hit, will now have a total of:
(your hitting hand's fingers + their hit hand's fingers) % 5. Current player then
switches to the opponent. Make the opponent reach 0 fingers on both
hands to win. Moves will be denoted as two characters, both of which are l or r,
representing left or right respectively. The first character represents current
player, and the other represents the opposing player."""

    def __init__(self, player: bool) -> None:
        """initializes the chopstick game. Setting the initial
        Chopsticks game state."""
        if player:
            self.current_state = ChopsticksState()
        else:
            self.current_state = ChopsticksState('p2')
    def get_instructions(self) -> str:
        """returns the instructions for the game.
        >>> s = Chopsticks(True)
        >>> Chopsticks.INSTRUCTIONS == s.get_instructions()
        True
        """
        return """Both players start with two hands each with one finger.
Suppose you are the current player. You choose one of your hands to hit theirs
with. Their hand that is hit, will now have a total of:
(your hitting hand's fingers + their hit hand's fingers) % 5. Current player then
switches to the opponent. Make the opponent reach 0 fingers on both
hands to win. Moves will be denoted as two characters, both of which are l or r,
representing left or right respectively. The first character represents current
player, and the other represents the opposing player."""

class ChopsticksState(CurrentState):
    """Represents the current game state of the game
    Chopsticks."""
    current_left: int
    current_right: int
    other_left: int
    other_right: int
    player: str

    def __init__(self, player: str = 'p1', current_hands:
                 Tuple[int]=(1, 1), other_hands: Tuple[int] = (1, 1)):
        """initializes the current state of the game chopsticks.
        The lists Current_hands and other_hands represents 
        player hands. The first element is the number 
        of fingers on the left hand, and second element
        is the fingers on the right hand."""
        self.current_left = current_hands[0]%5
        self.current_right = current_hands[1]%5
        self.other_left = other_hands[0]%5
        self.other_right = other_hands[1]%5
        self.player = player

    def get_possible_moves(self) -> List[str]:
        """returns a list of all possible moves.
        >>> c = ChopsticksState(True)
        >>> c.get_possible_moves()
        ['ll', 'lr', 'rl', 'rr']
        >>> k = ChopsticksState(current_hands=[0,1])
        >>> k.get_possible_moves()
        ['rl', 'rr']
        """
        moves_list = []
        if self.current_left != 0:
            if self.other_left != 0:
                moves_list.append('ll')
            if self.other_right != 0:
                moves_list.append('lr')
        if self.current_right != 0:
            if self.other_left != 0:
                moves_list.append('rl')
            if self.other_right != 0:
                moves_list.append('rr')
        return moves_list

    def make_move(self, move: str) -> 'ChopsticksState':
        """makes a move. Returns a new SubtractSquareState.
        >>> s = ChopsticksState()
        >>> x = s.make_move('ll')
        >>> print(x)
        p1: left 1-1 right ; p2: left 2-1 right"""
        new_left = self.other_left
        new_right = self.other_right
        if move == 'll':
            new_left = self.current_left + self.other_left
        elif move == 'rl':
            new_left = self.current_right + self.other_left
        elif move == 'lr':
            new_right = self.current_left + self.other_right
        elif move == 'rr':
            new_right = self.current_right + self.other_right
        current_hand = (int(new_left), int(new_right))
        opposing_hand = (int(self.current_left), int(self.current_right))
        if self.player == 'p1':
            return ChopsticksState('p2', current_hand, opposing_hand)
        return ChopsticksState('p1', current_hand, opposing_hand)

    def __str__(self) -> str:
        """A string represention of SubtractSquareState
        >>> s = ChopsticksState()
        >>> print(s)
        p1: left 1-1 right ; p2: left 1-1 right
        """
        if self.player == 'p1':
            return ("p1: left {}-{} right ; p2: left {}-{} right".format(
                self.current_left, self.current_right, self.other_left,
                self.other_right))
        return ("p1: left {}-{} right ; p2: left {}-{} right".format(
            self.other_left, self.other_right, self.current_left,
            self.current_right))

    def __eq__(self, other: Any) -> bool:
        """Returns True iff both self and other have the same type,
        current number, and current player.
        >>> s = ChopsticksState()
        >>> t = ChopsticksState()
        >>> s == t
        True
        >>> u = ChopsticksState('p2')
        >>> s == u
        False
        """
        return (type(self) == type(other) and str(self) == str(other)
                and self.player == other.player)

if __name__ == "__main__":
    x = Chopsticks(True)
    g1 = x.current_state.make_move('rr')
    g2 = g1.make_move('rr')
    g3 = g2.make_move('rr')
