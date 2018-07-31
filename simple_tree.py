"""A simple tree."""
from typing import Any, List, Optional


class Tree:
    """Represents a tree"""
    value: Any
    children: List['Tree']
    state_value: Optional[int]
    move_made: Any

    def __init__(self, value: Any, move_made: Any,
                 state_value: Optional[int]=None,
                 children=None):
        """Creates a Tree with value value, and
        0 or more children"""
        self.value = value
        # copy children if not None
        self.children = children[:] if children is not None else []
        self.state_value = state_value
        self.move_made = move_made
