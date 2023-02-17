import string

from chess_solver import FigureBuilder
from flask import Flask

app = Flask(__name__)


@app.get("/api/v1/<string:chess_figure>/<string:current_field>")
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
