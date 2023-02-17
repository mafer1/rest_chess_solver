import string
from abc import ABCMeta, abstractmethod
from itertools import product


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
        elif value not in string.ascii_lowercase():
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

    def __add__(self, other):
        return self.horizontal_index + other.horizontal_index, self.vertical + other.vertical


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
        import string

        cart_tuple = self._position.position_tuple
        figure_moves = []

        if (
            string.ascii_uppercase[self._position.position_tuple[0] - 1],
            self._position.position_tuple[1],
        ) not in list(product("ABCDEFGH", range(1, 9))):
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


class Knight(Figure):
    """Knight figure - attacker with L-shape move"""

    def __init__(self, current_field):
        self.current_field = current_field
        self._position = FigurePosition(current_field)
        self._available_move_vectors = list(product((-2, 2), (-1, 1))) + list(product((-1, 1), (-2, 2)))

    def list_available_moves(self) -> list:
        """
        Knights moves two squares in a horizontal or vertical direction,
        then move one square horizontally or vertically
        :return: list
        """
        cart_tuple = self._position.position_tuple
        figure_moves = []
        for move_vector in self._available_move_vectors:
            figure_moves.append((cart_tuple[0] + move_vector[0], cart_tuple[1] + move_vector[1]))

        import string

        figure_moves2 = [
            f"{string.ascii_uppercase[h-1]}{v}" for h, v in figure_moves if h in range(1, 9) and v in range(1, 9)
        ]
        return sorted(set(figure_moves2))

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
        self._available_move_vectors = list(product(range(-7, 8), [0])) + list(product([0], range(-7, 8)))

    def list_available_moves(self) -> list:
        cart_tuple = self._position.position_tuple
        figure_moves = []
        for move_vector in self._available_move_vectors:
            figure_moves.append((cart_tuple[0] + move_vector[0], cart_tuple[1] + move_vector[1]))

        import string

        figure_moves2 = [
            f"{string.ascii_uppercase[h-1]}{v}" for h, v in figure_moves if h in range(1, 9) and v in range(1, 9)
        ]
        return sorted(set(figure_moves2))

    def validate_move(self, dest_field: str) -> bool:
        return dest_field in self.list_available_moves()


class Queen(Figure):
    """Queen figure - diagonally or vertically or horizontally"""

    def __init__(self, current_field):
        self.current_field = current_field
        self._position = FigurePosition(current_field)
        self._available_move_vectors = (
            list([(x, x) for x in range(-7, 8)] + [(x, -x) for x in range(-7, 8)])
            + list(product(range(-7, 8), [0]))
            + list(product([0], range(-7, 8)))
        )

    def list_available_moves(self) -> list:
        cart_tuple = self._position.position_tuple
        figure_moves = []
        for move_vector in self._available_move_vectors:
            figure_moves.append((cart_tuple[0] + move_vector[0], cart_tuple[1] + move_vector[1]))

        import string

        figure_moves2 = [
            f"{string.ascii_uppercase[h-1]}{v}" for h, v in figure_moves if h in range(1, 9) and v in range(1, 9)
        ]
        return sorted(set(figure_moves2))

    def validate_move(self, dest_field: str) -> bool:
        return dest_field in self.list_available_moves()


class Bishop(Figure):
    """Bishop figure - only diagonally"""

    def __init__(self, current_field):
        self.current_field = current_field
        self._position = FigurePosition(current_field)
        self._available_move_vectors = list([(x, x) for x in range(-7, 8)] + [(x, -x) for x in range(-7, 8)])

    def list_available_moves(self) -> list:
        cart_tuple = self._position.position_tuple
        figure_moves = []
        for move_vector in self._available_move_vectors:
            figure_moves.append((cart_tuple[0] + move_vector[0], cart_tuple[1] + move_vector[1]))

        import string

        figure_moves2 = [
            f"{string.ascii_uppercase[h-1]}{v}" for h, v in figure_moves if h in range(1, 9) and v in range(1, 9)
        ]
        return sorted(set(figure_moves2))

    def validate_move(self, dest_field: str) -> bool:
        return dest_field in self.list_available_moves()


class King(Figure):
    """King figure - only one square in any direction(vertically, horizontally and diagonally)"""

    def __init__(self, current_field):
        self.current_field = current_field
        self._position = FigurePosition(current_field)
        self._available_move_vectors = list(product([-1, 0, 1], [-1, 0, 1]))

    def list_available_moves(self) -> list:
        cart_tuple = self._position.position_tuple
        figure_moves = []
        for move_vector in self._available_move_vectors:
            figure_moves.append((cart_tuple[0] + move_vector[0], cart_tuple[1] + move_vector[1]))

        import string

        figure_moves2 = [
            f"{string.ascii_uppercase[h-1]}{v}" for h, v in figure_moves if h in range(1, 9) and v in range(1, 9)
        ]
        return sorted(set(figure_moves2))

    def validate_move(self, dest_field: str) -> bool:
        return dest_field in self.list_available_moves()
