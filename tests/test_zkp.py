from typer.testing import CliRunner

from .main import app

runner = CliRunner()


def test_hello_world():
    print("Hello World!")

def test_central_proof():
    result = runner.invoke(app ,['{"user1": [6, 7, 9, 10, 12], "user2": [1, 2, 3, 8, 7]}']) 
    assert result.exit_code == 0 
    assert len(result) == 5
    assert len(result[0]) == 5

def test_verification():
    result = runner.invoke(app ,['[6, 7, 9, 10, 12]', 1])
    assert result.exit_code == 0 
    assert result == [169, 137, 213, 11, 215]
