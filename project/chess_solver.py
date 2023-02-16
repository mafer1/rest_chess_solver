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


class Location:
    """
    Location class with validation methods for both dimensions.
    horizontal: str range(A-H)
    vertical: int range 1-9
    """

    _HORIZONTAL_TRANSITION = dict(zip("ABCDEFGH", range(1, 9)))

    def __init__(self, horizontal, vertical):
        self.horizontal: str = horizontal
        self.vertical: int = vertical

    @property
    def horizontal(self):
        """Horizontal value for chess board"""
        return self._horizontal

    @property
    def vertical(self):
        """Vertical value for chess board"""
        return self._vertical

    @horizontal.setter
    def horizontal(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Inappropriate type of value. Please use string")
        elif value not in "ABCDEFGH":
            raise ValueError("Uncorrected value. Please use value from range A-H")
        elif len(value) != 1:
            raise ValueError(f"Uncorrected value. Field {value} does not exist. Please use value from range A-H")
        else:
            self._horizontal = value

    @vertical.setter
    def vertical(self, value: str):
        try:
            value = int(value)
        except ValueError:
            raise TypeError("Inappropriate type of value. Please use int")
        else:
            if value not in range(1, 9):
                raise ValueError("Uncorrected value. Please use value from range 1-8")
            else:
                self._vertical = value

    def __repr__(self):
        """Location representation"""
        return f"Location object for chess figure: ({self._horizontal}, {self._vertical})"

    def __add__(self, other):
        return self.horizontal + other.horizontal, self.vertical + other.vertical


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
