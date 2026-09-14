from pathlib import Path

import check50

FILE_NAME = "mitternacht.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


def get_solutions(stdout):
    """Takes the CMD output and returns the calculated solutions in a sorted list."""
    solutions = []

    for part in stdout.replace("\n", " ").split(","):
        if "=" in part:
            value = part.split("=")[1].strip()
            solutions.append(float(value))

    return sorted(solutions)


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
    """Check that the program returns the expected solutions."""
    actual = run_program(a, b, c)
    actual_solutions = get_solutions(actual)

    if actual_solutions != expected:
        raise check50.Mismatch(
            str(expected),
            actual,
        )


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
