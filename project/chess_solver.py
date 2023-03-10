import string
from abc import ABCMeta, abstractmethod
from itertools import product


def location_translator(func):
    """
    Function translates coordinates from cartesian system to chess board
    :param func: creator/gathering function for tuples in structure similar to chess board coordinates ([A-H],[1-8])
    :return: list of translated values corresponding to chess board location system
    """

    def inner(*args, **kwargs) -> list:
        list_of_moves = func(*args, **kwargs)
        return sorted(set([f"{string.ascii_uppercase[h - 1]}{v}" for h, v in list_of_moves]))

    return inner


@location_translator
def create_list_of_moves(
    position_tuple: tuple,
    vectors: list,
) -> list:
    """
    Function of creating set of possible vectors for chess figures
    :param position_tuple: position described in cartesian coordinates
    :param vectors: move vectors described in cartesian coordinates
    :return: list of tuples with vectors available to do on chess boards
    """
    return [
        new_position
        for new_position in [
            (
                position_tuple[0] + move_vector[0],
                position_tuple[1] + move_vector[1],
            )
            for move_vector in vectors
        ]
        if 0 < new_position[0] <= 8 and 0 < new_position[1] <= 8
    ]


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

    def __init__(self, bare_position: str):
        self.bare_position = bare_position.lower()
        self.horizontal = self.bare_position[0]
        self.horizontal_index: int = dict(zip(string.ascii_lowercase[:8], range(1, 9)))[self.horizontal]
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
        elif value not in string.ascii_lowercase[:8]:
            raise ValueError("Uncorrected value. Please use value from range A-H")
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


class FigureBuilder:
    def __init__(self, figure_name):
        self.figure_name: str = figure_name
        self.figures = {
            "king": King,
            "queen": Queen,
            "bishop": Bishop,
            "knight": Knight,
            "rook": Rook,
            "pawn": Pawn,
        }

    def is_valid(self):
        return self.figure_name.lower() in self.figures

    def build(self) -> Figure:
        try:
            _figure_name = self.figure_name.lower()
        except KeyError:
            Exception("Incorrect figure.")
        else:
            return self.figures[_figure_name]


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
        return create_list_of_moves(
            self._position.position_tuple,
            self._available_move_vectors if self._position.position_tuple[1] == 2 else [(0, 1)],
        )

    def validate_move(self, dest_field: str) -> bool:
        """
        Move validator for Pawn figure. This figure moves only in one direction.
        If current position equals 2 - it is initial position
        Else: Pawn was already moved.
        :param dest_field:
        :return: bool
        """
        return dest_field in self.list_available_moves()


class Knight(Figure):
    """Knight figure - attacker with L-shape move"""

    def __init__(self, current_field):
        self.current_field = current_field
        self._position = FigurePosition(current_field)
        self._available_move_vectors = [
            vector for vector in list(product((-2, 2), (-1, 1))) + list(product((-1, 1), (-2, 2))) if vector != (0, 0)
        ]

    def list_available_moves(self) -> list:
        """
        Knights moves two squares in a horizontal or vertical direction,
        then move one square horizontally or vertically
        :return: list
        """
        return create_list_of_moves(position_tuple=self._position.position_tuple, vectors=self._available_move_vectors)

    def validate_move(self, dest_field: str) -> bool:
        """
        Move validator for Knight figure. The move of this figure can be divided into 2 parts:
            first: move two squares in a horizontal or vertical direction
            second: move one square horizontally or vertically
            (depends on first move if first move was horizontal -> second move has to be vertically
            and oppositely for first vertical move)

        :param dest_field:
        :return: bool
        """
        return dest_field in self.list_available_moves()


class Rook(Figure):
    """Rook figure - only vertically or horizontally"""

    def __init__(self, current_field):
        self.current_field = current_field
        self._position = FigurePosition(current_field)
        self._available_move_vectors = [
            vector for vector in list(product(range(-7, 8), [0])) + list(product([0], range(-7, 8))) if vector != (0, 0)
        ]

    def list_available_moves(self) -> list:
        return create_list_of_moves(position_tuple=self._position.position_tuple, vectors=self._available_move_vectors)

    def validate_move(self, dest_field: str) -> bool:
        return dest_field in self.list_available_moves()


class Queen(Figure):
    """Queen figure - diagonally or vertically or horizontally"""

    def __init__(self, current_field):
        self.current_field = current_field
        self._position = FigurePosition(current_field)
        self._available_move_vectors = [
            vector
            for vector in [(x, x) for x in range(-7, 8)]
            + [(x, -x) for x in range(-7, 8)]
            + list(product(range(-7, 8), [0]))
            + list(product([0], range(-7, 8)))
            if vector != (0, 0)
        ]

    def list_available_moves(self) -> list:
        return create_list_of_moves(position_tuple=self._position.position_tuple, vectors=self._available_move_vectors)

    def validate_move(self, dest_field: str) -> bool:
        return dest_field in self.list_available_moves()


class Bishop(Figure):
    """Bishop figure - only diagonally"""

    def __init__(self, current_field):
        self.current_field = current_field
        self._position = FigurePosition(current_field)
        self._available_move_vectors = [
            vector
            for vector in list([(x, x) for x in range(-7, 8)] + [(x, -x) for x in range(-7, 8)])
            if vector != (0, 0)
        ]

    def list_available_moves(self) -> list:
        return create_list_of_moves(position_tuple=self._position.position_tuple, vectors=self._available_move_vectors)

    def validate_move(self, dest_field: str) -> bool:
        return dest_field in self.list_available_moves()


class King(Figure):
    """King figure - only one square in any direction(vertically, horizontally and diagonally)"""

    def __init__(self, current_field):
        self.current_field = current_field
        self._position = FigurePosition(current_field)
        self._available_move_vectors = [vector for vector in list(product([-1, 0, 1], [-1, 0, 1])) if vector != (0, 0)]

    def list_available_moves(self) -> list:
        return create_list_of_moves(position_tuple=self._position.position_tuple, vectors=self._available_move_vectors)

    def validate_move(self, dest_field: str) -> bool:
        return dest_field in self.list_available_moves()
