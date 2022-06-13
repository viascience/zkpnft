import random

from typer.testing import CliRunner

from ..main import prover
from ..verification_hash import verifier

random.seed(1)


def test_central_proof():
    runner = CliRunner()
    result = runner.invoke(
        prover, ['{"user1": [6, 7, 9, 10, 12], "user2": [1, 2, 3, 8, 7]}', "--noise", 1]
    )

    print(f"Result \n {result.stdout}")

    assert result.exit_code == 0

    expected_response = "\n{'user_0': '1', 'user_1': 4}\n"

    assert expected_response in result.stdout


def test_verification():
    runner = CliRunner()
    result = runner.invoke(verifier, ["[6, 7, 9, 10, 12]", "1"])
    print(f"Result \n {result.stdout}")
    assert result.exit_code == 0
    assert "\n[169, 137, 213, 11, 215]\n" in result.stdout
