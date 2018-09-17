# Text based games

Some simple textbased games. Can either play against another human player, or against a computer AI(Implemented using the minimax strategy).

## Prerequisites

Simply having python 3.6 is enough!

## Running

Run game_interface.py and follow the instructions given.

## On the implementation of the game AI

The code for the game AI can be in strategy.py, under either of the following functions: 
- recursive_minimax
- iterative_minimax

Both of these implement the decision ruling that is minimax. Minimax has the computer seek to minimize loss in the worst case scenario, where the opponent plays perfectly. We do this by assigning game states where we can guarantee at most a win, tie, or loss a score of 1, 0, and -1 respectively. To check if we can guarantee at most a win, tie, or loss from a certain game state, we treat game states like a tree, and check each possible 'child' game state, continually doing this until we reach game states where the game is already finished, at which point we can retroactively evaluate the score of game states based off the scores of their 'child' game states.
