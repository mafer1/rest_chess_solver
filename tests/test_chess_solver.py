import pytest

from project.chess_solver import Pawn


@pytest.mark.parametrize(
    "figure_position, expected",
    (
        ("A1", "A2"),
        ("B5", "B6"),
    ),
)
def test_pawn_list_moves_(figure_position, expected):
    pawn_instance = Pawn(current_field=figure_position)
    assert pawn_instance.list_available_moves() == [expected]


@pytest.mark.parametrize(
    "figure_position, expected",
    (
        ("A9", pytest.raises(Exception)),
        ("A0", pytest.raises(Exception)),
        ("C14", pytest.raises(Exception)),
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
def test_pawn_list_moves_mlp_values(figure_position, expected):
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
