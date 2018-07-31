"""
A module for strategies.
"""
from typing import Any, Union, List, Dict
import copy
from simple_tree import Tree
from subtract_square_game import SubtractSquareGame
from stonehenge_game import Stonehenge
from stonehenge_state_4 import StonehengeState


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def recursive_minimax(game: Union[Stonehenge, SubtractSquareGame]) -> Any:
    """A recursive implementation of minimax.
    """
    scores = []
    moves = game.current_state.get_possible_moves()
    seen_states = {}
    for move in moves:
        if get_score(game, move, seen_states) == 1:
            return move
        else:
            scores.append(get_score(game, move, seen_states))
    highest_score = max(scores)
    index_of_score = scores.index(highest_score)
    move = game.current_state.get_possible_moves()[index_of_score]
    return move


def get_score(game: Union[Stonehenge,
                          SubtractSquareGame], move: Any,
              seen_states: Dict['GameState', int]) -> int:
    """Returns a score for move in the current state of game.
    move is assumed to be a valid move.
    Will return 1 if move guarantees at most a win.
    Will return 0 if move guarantees at most a tie.
    Will return -1 if move guarantees at most a loss."""

    # get old and new states
    new_state = game.current_state.make_move(move)
    old_state = game.current_state

    # get old and new player
    old_player = old_state.get_current_player_name()
    new_player = new_state.get_current_player_name()

    # base case: we can find the score instantly.
    # i.e. If it is in seen_states or game is over

    if new_state.__repr__() in seen_states:
        return seen_states[new_state.__repr__()]

    elif game.is_over(new_state):
        # get_current_player_name gets the other player's name
        # since players switch after making a move

        # Old player's move has made old player win
        if game.is_winner(old_player):
            seen_states[new_state.__repr__()] = 1
            return 1

        # The move has just made the other player win
        elif game.is_winner(new_player):
            seen_states[new_state.__repr__()] = -1
            return -1

        # Neither player has won, thus a tie
        seen_states[new_state.__repr__()] = 0
        return 0

    # else, do recursion.
    # opponent will take their best move.
    # Their best move negatively affects us.
    move_scores = []
    for x in new_state.get_possible_moves():
        # new game for recursion
        new_game = copy.deepcopy(game)
        new_game.current_state = new_state
        # want to stop early if opponent best move already found
        # new player of state after new_state, i.e. old_player
        if get_score(new_game, x, seen_states) == 1:
            seen_states[new_state.__repr__()] = 1
            return 1
        move_scores.append(get_score(new_game, x, seen_states))
    seen_states[new_state.__repr__()] = -1*max(move_scores)
    return -1*max(move_scores)


def iterative_minimax(game: Union[SubtractSquareGame,
                                  Stonehenge]) -> Any:
    """An iterative version of minimax"""

    new_game = copy.deepcopy(game)
    x = Tree(new_game, None)
    stack = [x]
    while stack != []:
        top_of_stack = stack[-1]
        new_game = top_of_stack.value
        new_state = new_game.current_state
        if top_of_stack.value.is_over(new_state):
            cur_player = new_state.get_current_player_name()
            if cur_player == 'p1':
                other_player = 'p2'
            else:
                other_player = 'p1'
            # points
            if new_game.is_winner(cur_player):
                top_of_stack.state_value = -1
            elif new_game.is_winner(other_player):
                top_of_stack.state_value = 1
            # Tie
            else:
                top_of_stack.state_value = 0
            stack.pop(-1)
        else:
            # We have not looked at this one yet
            if top_of_stack.children == []:
                not_looked_at_this_yet(stack)
            # We have looked at this before, and we have
            # evaluated value of all its future possible states
            else:
                values_list = [child.state_value for
                               child in top_of_stack.children]
                top_of_stack.state_value = -1*max(values_list)
                stack.pop(-1)
    set_of_values = [child.state_value for
                     child in x.children]
    moves = [child.move_made for child
             in x.children]
    index_of_it = set_of_values.index(max(set_of_values))
    return moves[index_of_it]


def not_looked_at_this_yet(stack: List[Tree]) -> None:
    """We find a Tree that we have not looked at yet in
    the stack. We identify this from the Tree having
    no children."""
    top_of_stack = stack[-1]
    new_game = top_of_stack.value
    for move in new_game.current_state.get_possible_moves():
        new_state = new_game.current_state.make_move(move)
        newest_game = copy.deepcopy(new_game)
        newest_game.current_state = new_state
        new_tree = Tree(newest_game, move)
        top_of_stack.children.append(new_tree)
        stack.append(new_tree)


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
