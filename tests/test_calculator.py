import pytest

from calculator.pkg.calculator import Calculator


@pytest.fixture
def calculator() -> Calculator:
    return Calculator()


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("3 + 5", 8),
        ("10 - 4", 6),
        ("3 * 4", 12),
        ("10 / 2", 5),
        ("3 * 4 + 5", 17),
        ("2 * 3 - 8 / 2 + 5", 7),
        ("( 3 + 7 ) * 2", 20),
        ("( 3 + ( 7 * 2 ) )", 17),
        ("(3 + 7) * 2", 20),
    ],
)
def test_evaluate_expression(
    calculator: Calculator, expression: str, expected: float
) -> None:
    assert calculator.evaluate(expression) == expected


def test_empty_expression_returns_none(calculator: Calculator) -> None:
    assert calculator.evaluate("") is None


@pytest.mark.parametrize("expression", ["( 3 + 7", "3 + 7 )"])
def test_unmatched_parentheses_raise_value_error(
    calculator: Calculator, expression: str
) -> None:
    with pytest.raises(ValueError):
        calculator.evaluate(expression)


@pytest.mark.parametrize("expression", ["$ 3 5", "+ 3"])
def test_invalid_expressions_raise_value_error(
    calculator: Calculator, expression: str
) -> None:
    with pytest.raises(ValueError):
        calculator.evaluate(expression)
