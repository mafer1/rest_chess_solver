from abc import ABC, abstractmethod
from itertools import product

chess_board = list(product("ABCDEFGH", range(1, 9)))


class Figure(metaclass=ABC):
    """Figure abstract base class"""

    @abstractmethod
    def __init__(self, current_field: str):
        self.current_field = current_field

    @abstractmethod
    def list_available_moves(self) -> list:
        """A function that returns list of possible chess moves for defined chess figure"""

    @abstractmethod
    def validate_move(self, dest_field: str) -> bool:
        """A function which validates correctness of move
        from current field to destination field for a defined chess figure"""
