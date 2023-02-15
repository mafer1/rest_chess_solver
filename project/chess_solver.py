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


class Pawn(Figure):
    """Pawn figure - solider of the first line"""

    def __init__(self, current_field):
        self.current_field = current_field
        self._tuple_position = (str(current_field[0]), int(current_field[1]))

    def list_available_moves(self) -> list:
        """
        Pawns move only vertically forward one square.
        ONE EXCEPTION - when pawn is not moved, it can move forward two squares.
        :return: list
        """
        if self._tuple_position not in chess_board:
            raise Exception("Field does not exist.")
        elif self._tuple_position[1] == 2:
            return [
                f"{self._tuple_position[0]}{int(self._tuple_position[1]) + 1}",
                f"{self._tuple_position[0]}{int(self._tuple_position[1]) + 2}",
            ]
        else:
            return [f"{self._tuple_position[0]}{int(self._tuple_position[1]) + 1}"]

    def validate_move(self, dest_field: str) -> bool:
        """
        Move validator for Pawn figure. This figure moves only in one direction.
        If current position equals 2 - it is initial position
        Else: Pawn was already moved.
        :param dest_field:
        :return: bool
        """
        return True if dest_field in self.list_available_moves() else False
