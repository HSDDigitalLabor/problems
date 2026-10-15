import math
import re
from pathlib import Path

import check50

FILE_NAME = "mitternacht.py"


FILE_NAME = "mitternacht.py"

NUMBER = r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"
ONE_SOLUTION = re.compile(rf"Eine Lösung:\s*x\s*=\s*({NUMBER})")
TWO_SOLUTIONS = re.compile(
    rf"Zwei Lösungen:\s*x1\s*=\s*({NUMBER})\s*,\s*x2\s*=\s*({NUMBER})"
)

FORMAT_HINT = (
    "Erwartetes Format:\n"
    "  Eine Lösung:   Eine Lösung: x = ...\n"
    "  Zwei Lösungen: Zwei Lösungen: x1 = ..., x2 = ...\n"
    "Achten Sie auf das Komma zwischen den beiden Lösungen und darauf, "
    "dass nach dem Doppelpunkt bzw. dem Gleichheitszeichen nur die Zahl folgt."
)


def parse_solutions(stdout):
    """Parse the program output strictly according to the task format.

    Returns a sorted list of floats or raises check50.Failure with a hint.
    """
    text = stdout.strip()

    if match := TWO_SOLUTIONS.match(text):
        return sorted(float(g) for g in match.groups())

    if match := ONE_SOLUTION.match(text):
        return [float(match.group(1))]

    hint = FORMAT_HINT
    if text.startswith("Zwei Lösungen") and "," not in text:
        hint = (
            "Die beiden Lösungen müssen durch ein Komma getrennt sein: "
            "`Zwei Lösungen: x1 = ..., x2 = ...`"
        )

    msg = f"Die Ausgabe entspricht nicht dem vorgegebenen Format. Ausgabe war: {text!r}"
    raise check50.Failure(
        msg,
        help=hint,
    )


def run_program(a, b, c):
    """Run the program with the given quadratic coefficients."""
    return (
        check50.run(f"python3 {FILE_NAME}")
        .stdin(str(a))
        .stdin(str(b))
        .stdin(str(c))
        .stdout()
    )


def check_solutions(a, b, c, expected):
    """Check that the program returns the expected solutions in the right format."""
    actual = run_program(a, b, c)
    actual_solutions = parse_solutions(actual)

    if len(actual_solutions) != len(expected):
        kind = "Eine Lösung" if len(expected) == 1 else "Zwei Lösungen"
        raise check50.Mismatch(
            kind,
            actual.strip(),
            help=f"Für a={a}, b={b}, c={c} werden {len(expected)} Lösung(en) erwartet.",
        )

    if not all(
        math.isclose(x, y, abs_tol=1e-9)
        for x, y in zip(
            actual_solutions,
            expected,
            strict=False,
        )
    ):
        raise check50.Mismatch(str(expected), str(actual_solutions))


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def test_example_1():
    """test using given example 1"""
    check_solutions(1, -5, 6, [2.0, 3.0])


@check50.check(exists)
def test_example_2():
    """test using given example 2"""
    check_solutions(1, -4, 4, [2.0])


@check50.check(exists)
def test_example_3():
    """test using given example 3"""
    expected = "Keine Lösung"

    actual = run_program(1, 2, 5)

    if not actual.startswith(expected):
        raise check50.Mismatch(expected, actual)


@check50.check(exists)
def test_two_negative_solutions():
    """test with two negative solutions"""
    check_solutions(1, 5, 6, [-3.0, -2.0])


@check50.check(exists)
def test_positive_and_negative_solution():
    """test with one positive and one negative solution"""
    check_solutions(1, 0, -9, [-3.0, 3.0])


@check50.check(exists)
def test_zero_as_solution():
    """test with zero as one of the solutions"""
    check_solutions(1, -3, 0, [0.0, 3.0])


@check50.check(exists)
def test_fractional_solutions():
    """test with fractional solutions"""
    check_solutions(4, -12, 5, [0.5, 2.5])


@check50.check(exists)
def test_single_negative_solution():
    """test with a negative double solution"""
    check_solutions(1, 6, 9, [-3.0])


@check50.check(exists)
def test_no_solution_negative_discriminant():
    """test another case with no real solutions"""
    expected = "Keine Lösung"

    actual = run_program(2, 3, 7)

    if not actual.startswith(expected):
        raise check50.Mismatch(expected, actual)


@check50.check()
def no_forbidden_methods():
    """does not use forbidden built-ins or operators"""
    import tokenize

    forbidden_tokens = {"index"}
    forbidden_ops = {"in"}

    with Path(FILE_NAME).open() as f:
        tokens = tokenize.generate_tokens(f.readline)

        for tok_type, tok_string, *_ in tokens:
            # Skip comments and string literals
            if tok_type in (tokenize.COMMENT, tokenize.STRING):
                continue

            if tok_string in forbidden_tokens or tok_string in forbidden_ops:
                msg = f"Found forbidden token or operator '{tok_string}' in your code"
                raise check50.Failure(msg)
