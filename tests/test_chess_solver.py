import pytest

from project.chess_solver import (
    Bishop,
    FigureBuilder,
    FigurePosition,
    King,
    Knight,
    Pawn,
    Queen,
    Rook,
)


@pytest.mark.parametrize(
    "current_field, expected",
    (
        ("A1", "A2"),
        ("B5", "B6"),
    ),
)
def test_pawn_list_move_not_initial(current_field, expected):
    pawn_instance = Pawn(current_field=current_field)
    assert pawn_instance.list_available_moves() == [expected]


@pytest.mark.parametrize(
    "figure_position, expected",
    (
        ("A9", pytest.raises(Exception)),
        ("A0", pytest.raises(Exception)),
        ("Z1", pytest.raises(ValueError)),
        ("ZZ", pytest.raises(ValueError)),
    ),
)
def test_pawn_list_invalid_moves(figure_position, expected):
    with expected:
        pawn_instance = Pawn(current_field=figure_position)
        pawn_instance.list_available_moves()


@pytest.mark.parametrize(
    "figure_position, expected",
    (
        ("A2", ["A3", "A4"]),
        ("B2", ["B3", "B4"]),
    ),
)
def test_pawn_list_moves_initial(figure_position, expected):
    pawn_instance = Pawn(current_field=figure_position)
    assert pawn_instance.list_available_moves() == expected


@pytest.mark.parametrize(
    "field, dest_field",
    (
        ("A1", "A2"),
        ("A2", "A3"),
        ("A2", "A4"),
    ),
)
def test_pawn_valid_move(field, dest_field):
    assert Pawn(current_field=field).validate_move(dest_field=dest_field)


@pytest.mark.parametrize(
    "current_field, expected_field",
    (
        ("A1", "A1"),
        ("B2", "B2"),
        ("C3", "C3"),
    ),
)
def test_current_field(current_field, expected_field):
    figure = Pawn(current_field=current_field)
    assert figure.current_field == expected_field


@pytest.mark.parametrize(
    "current_field, expected_field",
    (
        ("B1", ["A3", "C3", "D2"]),
        ("G1", ["E2", "F3", "H3"]),
    ),
)
def test_knight_list_of_available(current_field, expected_field):
    knight_instance = Knight(current_field=current_field)
    assert knight_instance.list_available_moves() == expected_field


@pytest.mark.parametrize(
    "current_field, dest_field",
    (
        ("B1", "A3"),
        ("B1", "C3"),
        ("B1", "D2"),
    ),
)
def test_knight_validate_move(current_field, dest_field):
    knight_instance = Knight(current_field=current_field)
    assert knight_instance.validate_move(dest_field)


@pytest.mark.parametrize(
    "current_field, expected_field",
    (("B1", ["A1", "B1", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "C1", "D1", "E1", "F1", "G1", "H1"]),),
)
def test_rook_list_of_available(current_field, expected_field):
    rook_instance = Rook(current_field=current_field)
    assert rook_instance.list_available_moves() == expected_field


@pytest.mark.parametrize(
    "current_field, dest_field",
    (
        ("B1", "B2"),
        ("B1", "A1"),
        ("B1", "B7"),
    ),
)
def test_rook_validate_move(current_field, dest_field):
    rook_instance = Rook(current_field=current_field)
    assert rook_instance.validate_move(dest_field)


def test_figure_position_dunder_add():
    assert FigurePosition("A2") + FigurePosition("C4")


@pytest.mark.parametrize(
    "current_field, expected_field",
    (
        (
            "B1",
            [
                "A1",
                "A2",
                "B1",
                "B2",
                "B3",
                "B4",
                "B5",
                "B6",
                "B7",
                "B8",
                "C1",
                "C2",
                "D1",
                "D3",
                "E1",
                "E4",
                "F1",
                "F5",
                "G1",
                "G6",
                "H1",
                "H7",
            ],
        ),
    ),
)
def test_queen_list_of_available(current_field, expected_field):
    queen_instance = Queen(current_field=current_field)
    assert queen_instance.list_available_moves() == expected_field


@pytest.mark.parametrize(
    "current_field, dest_field",
    (
        (
            "B1",
            "A1",
        ),
    ),
)
def test_queen_validate_move_correct(current_field, dest_field):
    queen_instance = Queen(current_field=current_field)
    assert queen_instance.validate_move(dest_field)


@pytest.mark.parametrize(
    "current_field, expected_field",
    (
        (
            "B7",
            ["A6", "A7", "A8", "B6", "B7", "B8", "C6", "C7", "C8"],
        ),
    ),
)
def test_king_list_of_available(current_field, expected_field):
    king_instance = King(current_field=current_field)
    assert king_instance.list_available_moves() == expected_field


@pytest.mark.parametrize(
    "current_field, dest_field",
    (
        (
            "B7",
            "B6",
        ),
    ),
)
def test_king_validate_move_correct(current_field, dest_field):
    king_instance = King(current_field=current_field)
    assert king_instance.validate_move(dest_field)


@pytest.mark.parametrize(
    "current_field, expected_field",
    (
        (
            "B7",
            ["A6", "B7", "C8", "D7", "E6", "F5", "G4", "H3"],
        ),
    ),
)
def test_bishop_list_of_available(current_field, expected_field):
    bishop_instance = Bishop(current_field=current_field)
    assert bishop_instance.list_available_moves() == expected_field


@pytest.mark.parametrize(
    "current_field, dest_field",
    (
        (
            "C3",
            "H8",
        ),
    ),
)
def test_bishop_validate_move_correct(current_field, dest_field):
    bishop_instance = Bishop(current_field=current_field)
    assert bishop_instance.validate_move(dest_field)


@pytest.mark.parametrize(
    "figure, expected",
    (
        ("Pawn", Pawn),
        ("Rook", Rook),
        ("Knight", Knight),
        ("Bishop", Bishop),
        ("Queen", Queen),
        ("King", King),
    ),
)
def test_figure_builder_cls(figure, expected):
    figure_istance = FigureBuilder(figure).build()
    assert isinstance(figure_istance("A1"), expected)
