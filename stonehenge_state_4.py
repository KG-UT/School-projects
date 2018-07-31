"""Game state for Stonehenge."""
from typing import List, Union, Dict, Any
from game_state import GameState


class StonehengeState(GameState):
    """Game state for Stonehenge."""

    p1_turn: bool
    state: List[List[str]]
    rows: List[List[str]]

    def __init__(self, is_p1_turn: bool, state: List[List[str]]) -> None:
        """Initializes StonehengeState.
        The information regarding the status of the game
        will be kept track of via state, and is_p1_turn.

        state is formatted as such:
        [[top leylines]
        [row1],
        [row2],
        ...,
        [final row],
        [bottom leylines]]
        rows include the leyline associated with that row, and the leyline
        appears as the first element of the list.
        >>> r = [['@', '@', '@'], \
                ['@', 'A', 'B'], \
                ['@', 'C', 'D', 'E'], \
                ['@', 'F', 'D'], \
                ['@', '@', '@']]
        >>> e = StonehengeState(True, r)
        >>> e.rows
        [['A', 'B'], ['C', 'D', 'E'], ['F', 'D']]
        >>> e.p1_turn
        True
        >>> e.state
        [['@', '@', '@'], \
['@', 'A', 'B'], \
['@', 'C', 'D', 'E'], \
['@', 'F', 'D'], \
['@', '@', '@']]
        """
        self.p1_turn = is_p1_turn
        self.state = state
        self.rows = [row[1:] for row in self.state[1:-1]]

    def get_leylines(self, rows: List[List[str]]) -> List[List[str]]:
        """Using a new rows list, and self.state, create
        a list of new leylines. leylines will of the format:
        [[top leylines], [middle leylines], [bottom leylines]]
        >>> r = [['@', '@', '@'], \
                ['@', 'A', 'B'], \
                ['@', 'C', 'D', 'E'], \
                ['@', 'F', 'D'], \
                ['@', '@', '@']]
        >>> y = [['1', 'B'], \
                ['C', 'D', 'E'], \
                ['F', 'D']]
        >>> e = StonehengeState(True, r)
        >>> e.get_leylines(y)
        [['1', '@', '@'], ['1', '@', '@'], ['@', '@', '@']]"""

        leylines = []
        top_right_paral = self.make_parallelogram(rows, True)
        len_line = len(top_right_paral[0])
        top_leylines = []
        for i in range(len_line):
            single_line = []
            # this gets the line
            for line in top_right_paral:
                if line[i] != '.':
                    single_line.append(line[i])
            # this gets the leyline
            if ((self.state[0][i] == '@' and
                 single_line.count('1') >= len(single_line)/2)
                    or self.state[0][i] == '1'):
                top_leylines.append('1')
            elif ((self.state[0][i] == '@' and
                   single_line.count('2') >= len(single_line)/2)
                  or self.state[0][i] == '2'):
                top_leylines.append('2')
            else:
                top_leylines.append('@')
        middle_leylines = []
        for i in range(len_line):
            if ((self.state[i+1][0] == '@' and
                 rows[i].count('1') >= len(rows[i])/2)
                    or self.state[i+1][0] == '1'):
                middle_leylines.append('1')
            elif ((self.state[i+1][0] == '@' and
                   rows[i].count('2') >= len(rows[i])/2)
                  or self.state[i + 1][0] == '2'):
                middle_leylines.append('2')
            else:
                middle_leylines.append('@')
        top_left_paral = self.make_parallelogram(rows, False)
        bottom_leylines = []
        for i in range(len_line):
            single_line = []
            for line in top_left_paral:
                if line[i] != '.':
                    single_line.append(line[i])
            if ((self.state[-1][i] == '@' and
                 single_line.count('1') >= len(single_line)/2)
                    or self.state[-1][i] == '1'):
                bottom_leylines.append('1')
            elif ((self.state[-1][i] == '@' and
                   single_line.count('2') >= len(single_line)/2)
                  or self.state[-1][i] == '2'):
                bottom_leylines.append('2')
            else:
                bottom_leylines.append('@')
        leylines.append(top_leylines)
        leylines.append(middle_leylines)
        leylines.append(bottom_leylines)
        return leylines

    def _list_for_str(self) -> List[List[str]]:
        """Returns a nested list that is more friendly
        for creating the string method
        """

        num_leyline_2_diff = len(self.state[0]) - len(self.rows[0])
        # first make shallow copy of self.state
        new_list = [x[:] for x in self.state]
        for line_num in range(num_leyline_2_diff):
            l = new_list[0][2]
            new_list[1+line_num].append(l)
            new_list[0].pop(2)
        new_list[-2].append(new_list[-1][-1])
        new_list[-1].pop(-1)
        # now leylines and slots are in place
        return new_list

    def slash_list(self) -> List[List[str]]:
        """Creates a list of dashes for the
        __str__ method.
        # >>> st = [['@', '@', '@'], \
        #         ['@', 'A', 'B'], \
        #         ['@', 'C', 'D', 'E'], \
        #         ['@', 'F', 'D'], \
        #         ['@', '@', '@']]
        # >>> ex = StonehengeState(True, st)
        # >>> ex.slash_list()
        # [['/', '\\', '/', '\\', '/'], ['\\', '/', '\\', '/', '\\']]"""

        all_dashes = []
        for row_num in range(len(self.rows)-2):
            # slots of row is = 2+ row_num
            slots_of_row = 2 + row_num
            dashes = ['/', '\\']
            dash_row = dashes*slots_of_row + ['/']
            all_dashes.append(dash_row)
        last_dash_row = ['\\', '/']*(len(self.rows[-1])) + ['\\']
        all_dashes.append(last_dash_row)
        # top and bottom leyline dashes omitted
        # since they follow a diff space pattern
        return all_dashes

    def __str__(self) -> str:
        """Returns a str format of self.
        >>> st = [['@', '@', '@'], \
                ['@', 'A', 'B'], \
                ['@', 'C', 'D', 'E'], \
                ['@', 'F', 'D'], \
                ['@', '@', '@']]
        >>> ex = StonehengeState(True, st)
        >>> print(ex)
                @   @
               /   /
          @ - A - B   @
             / \\ / \\ /
        @ - C - D - E
             \\ / \\ / \\
          @ - F - D   @
               \\   \\
                @   @
        """

        return_string = ""
        str_list = self._list_for_str()
        dashes = self.slash_list()
        # length of longest row.
        total_length = len(str_list[-2]) * 4 #char + ' -
        # white space of first row + 6, since 6 will put it 2 after first letter
        # This puts dash at 1 after letter, and 1 before leyline
        leyline_white = (total_length - len(self.state[1]) * 4) // 2 + 6
        top_right_dash_white = leyline_white - 1
        # same here, but with white space of last row

        #we begin creating first leylines row, and dashes
        return_string += (leyline_white* ' '
                          + '   '.join(str_list[0]) + '\n')
        return_string += (top_right_dash_white*' '
                          + '/   /' + '\n')

        # we do this so we can check if first or last leyline
        for num in range(1, len(str_list)-2):
            row = str_list[num][:-1]
            # each character in row is followed by 3 characters, so total
            # space taken by row characters is 4*len(row)
            left_white = (total_length - len(self.state[num]) * 4) // 2
            return_string += left_white * ' '
            return_string += ' - '.join(row)
            if num != len(str_list) - 3:
                return_string += '   '
            else:
                return_string += ' - '
            return_string += str_list[num][-1]
            # go to next line
            return_string += '\n'
            # dashes now
            if num != len(str_list) -3:
                dash_white = left_white + 3
            else:
                dash_white = 5
            return_string += dash_white * ' '
            return_string += ' '.join(dashes[num - 1])
            return_string += '\n'
        # final row
        left_white = (total_length - len(self.state[-2]) * 4) // 2
        return_string += left_white * ' '
        return_string += ' - '.join(str_list[-2][:-1])
        return_string += '   '
        return_string += str_list[-2][-1]
        return_string += '\n'
        # final dashes
        # there are 5 white space for final dash row
        final_dash_white = 7
        return_string += ' '*final_dash_white
        return_string += '\\   '*(len(str_list[-1])-1) + '\\'
        return_string += '\n'
        # final leylines
        final_leyline_white = 8
        return_string += ' '*final_leyline_white
        return_string += '   '.join(str_list[-1])
        return return_string

    def __repr__(self):
        """return an easy to read format of self.
        >>> st = [['@', '@', '@'], \
                ['@', 'A', 'B'], \
                ['@', 'C', 'D', 'E'], \
                ['@', 'F', 'D'], \
                ['@', '@', '@']]
        >>> ex = StonehengeState(True, st)
        >>> ex
                @   @
               /   /
          @ - A - B   @
             / \\ / \\ /
        @ - C - D - E
             \\ / \\ / \\
          @ - F - D   @
               \\   \\
                @   @
        p1 to move.
        """
        x = str(self)
        x += '\n'
        if self.p1_turn:
            x += 'p1 to move.'
        else:
            x += 'p2 to move.'
        return x

    def get_possible_moves(self) -> list:
        """returns the available moves in a list.
        >>> st = [['@', '@', '@'], \
                ['@', 'A', 'B'], \
                ['@', 'C', 'D', 'E'], \
                ['@', 'F', 'D'], \
                ['@', '@', '@']]
        >>> ex = StonehengeState(True, st)
        >>> ex.get_possible_moves()
        ['A', 'B', 'C', 'D', 'E', 'F', 'D']
        """
        x = self.get_points()
        if x[True] >= x[2]/2 or x[False] >= x[2]/2:
            return []
        slots = sum(self.rows, [])
        moves = [x for x in slots if x != '1' and x != '2']
        return moves

    def make_parallelogram(self, new_rows: List[List[str]],
                           top_is_right: bool) -> List[List[str]]:
        """Makes The game board into a parallelogram to create new
        leylines easier.
        >>> r = [['@', '@', '@'], \
                ['@', 'A', 'B'], \
                ['@', 'C', 'D', 'E'], \
                ['@', 'F', 'D'], \
                ['@', '@', '@']]
        >>> e = StonehengeState(True, r)
        >>> e.make_parallelogram(e.rows, True)
        [['A', 'B', '.'], ['C', 'D', 'E'], ['.', 'F', 'D']]"""
        len_longest = len(new_rows[-2])
        parellelogram = [x[:] for x in new_rows]
        blank = ['.']
        for row_index in range(len(parellelogram)):
            row = parellelogram[row_index]
            row_deficit = len_longest - len(row)
            last_index = len(parellelogram) - 1
            if top_is_right:
                if row_index != last_index:
                    row += blank * row_deficit
                else:
                    row.insert(0, '.')
            else:
                if row_index != last_index:
                    temp = row[:]
                    row.clear()
                    row += blank * row_deficit
                    row += temp
                else:
                    row.append('.')
        return parellelogram

    def make_move(self, move: str) -> 'StonehengeState':
        """Makes a move which creates and returns a new instance
        of StonehengeState. This state remains unchanged.
        >>> r = [['@', '@', '@'], \
                ['@', 'A', 'B'], \
                ['@', 'C', 'D', 'E'], \
                ['@', 'F', 'D'], \
                ['@', '@', '@']]
        >>> e = StonehengeState(True, r)
        >>> e
                @   @
               /   /
          @ - A - B   @
             / \\ / \\ /
        @ - C - D - E
             \\ / \\ / \\
          @ - F - D   @
               \\   \\
                @   @
        p1 to move.
        >>> x = e.make_move('A')
        >>> x
                1   @
               /   /
          1 - 1 - B   @
             / \\ / \\ /
        @ - C - D - E
             \\ / \\ / \\
          @ - F - D   @
               \\   \\
                @   @
        p2 to move.
        """
        # get new rows
        new_row = [x[:] for x in self.rows]
        for row in new_row:
            for i in range(len(row)):
                if row[i] == move and self.p1_turn:
                    row[i] = '1'
                elif row[i] == move:
                    row[i] = '2'
        # get new leyline list
        new_leylines = self.get_leylines(new_row)
        for i in range(len(new_row)):
            new_row[i].insert(0, new_leylines[1][i])
        new_row.insert(0, new_leylines[0])
        new_row.append(new_leylines[2])
        if self.p1_turn:
            return StonehengeState(False, new_row)
        return StonehengeState(True, new_row)

    def get_points(self) -> Dict[Union[bool, int], int]:
        """returns number of leylines captured by each player
        and the total number of leylines available.
        The list returned is formatted as such:
        [p1 captured leylines, p2 captured leylines,
        total leylines in game]
        >>> r = [['@', '@', '@'], \
                ['@', 'A', 'B'], \
                ['@', 'C', 'D', 'E'], \
                ['@', 'F', 'D'], \
                ['1', '@', '@']]
        >>> e = StonehengeState(True, r)
        >>> print(e.get_points())
        {True: 1, False: 0, 2: 9}"""
        p1_leylines = 0
        p2_leylines = 0
        leylines = self.get_leylines(self.rows)
        for ll_type in leylines:
            for point in ll_type:
                if point == '1':
                    p1_leylines += 1
                elif point == '2':
                    p2_leylines += 1
        total_points = {True: p1_leylines, False: p2_leylines,
                        2: len(leylines[0])*3}
        return total_points

    def rough_outcome(self) -> float:
        """Returns a rough estimate of the game outcome.
        If the current player has a move that wins the game,
        return 1. If for all moves moves the current player makes,
        the other player still has a move that can make them win,
        return -1. Otherwise, return 0.
        >>> r = [['1', '@', '@'], \
                ['1', '1', 'B'], \
                ['@', 'C', 'D', 'E'], \
                ['@', 'F', 'G'], \
                ['@', '@', '@']]
        >>> e = StonehengeState(True, r)
        >>> e.rough_outcome()
        1"""
        for move in self.get_possible_moves():
            new_state = self.make_move(move)
            points = new_state.get_points()
            # check to see if current player wins with that move
            if points[self.p1_turn] > points[2]/2:
                return 1

        for move in self.get_possible_moves():
            # then check to see if other player cannot win
            new_state = self.make_move(move)
            points = new_state.get_points()
            other_player_moves = new_state.get_possible_moves()
            can_win = []
            for w in other_player_moves:
                possible_state = new_state.make_move(w)
                possible_points = possible_state.get_points()
                # if this move cannot win, add False
                if possible_points[not self.p1_turn] < points[2]/2:
                    can_win.append(False)
            # there does not exist a move the other player can make
            # that wins the game
            if not any(can_win):
                return 0
        # for each move the current player makes, it cannot win them the game,
        # and the other player has a move that makes them win.
        return -1

    def __eq__(self, obj: Any) -> bool:
        """ compares if another object obj is the same as self"""
        return type(obj) == type(self) and obj.__repr__() == self.__repr__()

if __name__ == '__main__':
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
