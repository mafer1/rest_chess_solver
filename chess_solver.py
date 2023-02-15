from abc import ABC, abstractmethod


class Figure(metaclass=ABC):
    """Figure abstract class"""

    @abstractmethod
    def __init__(self, current_field: str):
        self.position = current_field

    @abstractmethod
    def list_available_moves(self) -> list:
        """A function that returns list of possible chess moves for defined chess figure"""

    @abstractmethod
    def validate_move(self, dest_field: str) -> bool:
        """A function which validates correctness of move
        from current field to destination field for a defined chess figure"""
