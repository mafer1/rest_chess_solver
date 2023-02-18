import pytest

from project import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    yield app


def test_greeting(app):
    with app.test_client() as client:
        assert (client.get("/api/v1/")).json == {"message": "Welcome to REST Chess solver!"}


@pytest.mark.parametrize(
    "figure, field, expected",
    (
        ("pawn", "a1", ["A2"]),
        ("pawn", "a2", ["A3", "A4"]),
    ),
)
def test_get_moves_valid_availableMoves(app, figure, field, expected):
    with app.test_client() as client:
        with pytest.assume:
            assert client.get(f"/api/v1/{figure}/{field}").status_code == 200
            assert client.get(f"/api/v1/{figure}/{field}").json["availableMoves"] == expected


@pytest.mark.parametrize(
    "figure, field",
    (
        ("pawn1", "a1"),
        ("kingsman", "a2"),
    ),
)
def test_get_moves_invalid_chess_piece(app, figure, field):
    with app.test_client() as client:
        with pytest.assume:
            assert client.get(f"/api/v1/{figure}/{field}").status_code == 404
            assert client.get(f"/api/v1/{figure}/{field}").json["error"] == "Piece does not exist."


@pytest.mark.parametrize(
    "figure, field",
    (
        ("pawn", "9a"),
        ("king", "z2"),
        ("bishop", "a12"),
    ),
)
def test_get_moves_invalid_chess_current_field(app, figure, field):
    with app.test_client() as client:
        with pytest.assume:
            assert client.get(f"/api/v1/{figure}/{field}").status_code == 409
            assert client.get(f"/api/v1/{figure}/{field}").json["error"] == "Field does not exist."
