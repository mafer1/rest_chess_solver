import string

from flask import Blueprint

from .chess_solver import FigureBuilder

api = Blueprint("api", __name__)


@api.get("/")
@api.get("/api/v1/")
def greeting():
    return {"message": "Welcome to REST Chess solver!"}, 200


@api.get("/api/v1/<string:chess_figure>/<string:current_field>")
def get_moves(chess_figure: str, current_field: str) -> tuple:
    if chess_figure.lower() not in ["king", "queen", "rook", "bishop", "knight", "pawn"]:
        return {
            "availableMoves": [],
            "error": "Piece does not exist.",
            "figure": chess_figure.title(),
            "currentField": current_field.upper(),
        }, 404

    if (
        len(current_field) != 2
        or current_field[0].lower() not in string.ascii_lowercase[:9]
        or int(current_field[1]) not in range(1, 9)
    ):
        return {
            "availableMoves": [],
            "error": "Field does not exist.",
            "figure": chess_figure.title(),
            "currentField": current_field.upper(),
        }, 409

    figure = FigureBuilder(chess_figure).build()
    return {
        "availableMoves": figure(current_field).list_available_moves(),
        "error": None,
        "figure": chess_figure,
        "currentField": current_field,
    }, 200


@api.get("/api/v1/<string:chess_figure>/<string:current_field>/<string:dest_field>")
def field_validation(chess_figure: str, current_field: str, dest_field: str) -> tuple:
    if chess_figure.lower() not in ["king", "queen", "rook", "bishop", "knight", "pawn"]:
        return {
            "availableMoves": [],
            "error": "Piece does not exist.",
            "figure": chess_figure.title(),
            "currentField": current_field.upper(),
        }, 404
    if (
        len(current_field) != 2
        or len(dest_field) != 2
        or current_field[0].lower() not in string.ascii_lowercase[:9]
        or int(current_field[1]) not in range(1, 9)
        or dest_field[0].lower() not in string.ascii_lowercase[:9]
        or int(dest_field[1]) not in range(1, 9)
    ):
        return {
            "availableMoves": [],
            "error": "Field does not exist.",
            "figure": chess_figure.title(),
            "currentField": current_field.upper(),
        }, 409
    figure = FigureBuilder(chess_figure).build()
    return {
        "move": "invalid" if not figure(current_field).validate_move(dest_field) else "valid",
        "error": None,
        "figure": chess_figure,
        "currentField": current_field,
        "destField": dest_field,
    }, 200
