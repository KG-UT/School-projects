"""StoneHenge game. Subclass of game."""
from game import Game
from stonehenge_state_4 import StonehengeState

class Stonehenge(Game):
    """Implementation of the game Stonehenge."""

    current_state: StonehengeState

    def __init__(self, p1_starts: bool) -> None:
        """initializes the game Stonehenge."""
        side_length = int(input("What side length board do you want?: "))
        n = side_length + 1
        all_rows = []
        ascii_stuff = 64
        for row in range(side_length):
            new_row = []
            num_slots = 2
            while num_slots != row+4:
                ascii_stuff += 1
                new_row.append(chr(ascii_stuff))
                num_slots += 1
            all_rows.append(new_row)
        new_row = []
        num_slots = 0
        while num_slots != side_length:
            ascii_stuff += 1
            new_row.append(chr(ascii_stuff))
            num_slots += 1
        all_rows.append(new_row)
        for row in all_rows:
            row.insert(0, '@')
        all_rows.insert(0, ['@']*n)
        all_rows.append(['@']*n)
        self.current_state = StonehengeState(p1_starts, all_rows)

    def get_instructions(self) -> str:
        """returns the instruction to the game."""
        instructions = """Players take turns occupying cells. A player
gets a leyline when they occupy at least half of the cells
in a line associated with a leyline. There is a leyline
for each unique diagonal and horizontal line on the grid.
The player who gains half of the leylines first wins."""
        return instructions

    def is_over(self, state: StonehengeState) -> bool:
        """return if the game is over."""
        if state.get_possible_moves() == []:
            return True
        leylines = state.get_points()
        if leylines[True] >= leylines[2]/2:
            return True
        if leylines[False] >= leylines[2]/2:
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """return whether player is the winner of the game"""
        if self.is_over(self.current_state):
            leylines = self.current_state.get_points()
            if (player == 'p1' and
                    leylines[True] >= leylines[2]/2):
                return True
            elif (player == 'p2' and
                  leylines[False] >= leylines[2]/2):
                return True
        return False

    def str_to_move(self, string: str) -> str:
        """turns a string into a move that can
        be accepted by self.state"""
        return string

if __name__ == '__main__':
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
    x = Stonehenge(True)
    print(x.current_state)
