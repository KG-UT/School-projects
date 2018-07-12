# School-projects


For games:

These are just standard implementations of games that make use of inheritance and OOP.

For strategies:

On minimax and part of implementation: 

Minimax seeks to minimize the possible loss from a worst case scenario(That is, the opponent always takes their most optimal move).
To implement it, game states can be assigned values of 1,0,-1 for a win, tie, and loss respectively. Moves can then
be assigned values depending on the game state they lead to. Since minimax is typically used in zero sum games where
your win means your opponent's loss and vice-versa, then the score for any move we take can be taken as the negative of our 
opponent's best move (i.e. their highest scoring move). 

On how the strategies were implemented:

There were two equivalent implementations of minimax: One was just created recursively, and the other was created iteratively,
making use of a stack and tree.
