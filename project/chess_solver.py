from abc import ABCMeta, abstractmethod
from itertools import product

chess_board = list(product("ABCDEFGH", range(1, 9)))


class Figure(metaclass=ABCMeta):
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


class FigurePosition:
    """
    Location class with validation methods for both dimensions.
    horizontal: str range(A-H)
    vertical: int range 1-9
    """

    def __init__(self, bare_position):
        self.bare_position = bare_position
        self.horizontal: str = self.bare_position[0]
        self.horizontal_index: int = dict(zip("ABCDEFGH", range(1, 9)))[self.horizontal]
        self.vertical = self.bare_position[1]
        self.position_tuple = (self.horizontal_index, self.vertical)

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

    def __add__(self, other):
        return self.horizontal_index + other.horizontal_index, self.vertical + other.vertical


class Pawn(Figure):
    """Pawn figure - solider of the first line"""

    def __init__(self, current_field):
        self.current_field = current_field
        self._position = FigurePosition(current_field)
        self._available_move_vectors = [(0, 1), (0, 2)]

    def list_available_moves(self) -> list:
        """
        Pawns move only vertically forward one square.
        ONE EXCEPTION - when pawn is not moved, it can move forward two squares.
        :return: list
        """
        import string

        cart_tuple = self._position.position_tuple
        figure_moves = []

        if (
            string.ascii_uppercase[self._position.position_tuple[0] - 1],
            self._position.position_tuple[1],
        ) not in chess_board:
            raise Exception("Field does not exist.")
        if self._position.position_tuple[1] == 2:
            for move_vector in self._available_move_vectors:
                figure_moves.append((cart_tuple[0] + move_vector[0], cart_tuple[1] + move_vector[1]))
            figure_moves2 = [
                f"{string.ascii_uppercase[h - 1]}{v}" for h, v in figure_moves if h in range(1, 9) and v in range(1, 9)
            ]

            return sorted(figure_moves2)
        else:
            figure_moves.append(
                (cart_tuple[0] + self._available_move_vectors[0][0], cart_tuple[1] + self._available_move_vectors[0][1])
            )
            return [
                f"{string.ascii_uppercase[h - 1]}{v}" for h, v in figure_moves if h in range(1, 9) and v in range(1, 9)
            ]

    def validate_move(self, dest_field: str) -> bool:
        """
        Move validator for Pawn figure. This figure moves only in one direction.
        If current position equals 2 - it is initial position
        Else: Pawn was already moved.
        :param dest_field:
        :return: bool
        """
        return dest_field in self.list_available_moves()
