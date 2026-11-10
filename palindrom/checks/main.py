import ast
from pathlib import Path

import check50
import check50.py

FILE_NAME = "palindrom.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """palindrom.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """function defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "isPalindrome"):
        msg = "Function `isPalindrome` not found in palindrom.py"
        raise check50.Failure(msg)


def run_submission(eingabe: str, expected: bool):
    module = check50.py.import_(FILE_NAME)

    try:
        result = module.isPalindrome(eingabe)
    except IndexError:
        raise check50.Failure(
            rationale="Your solution raised an IndexError",
        ) from None

    except Exception as e:
        raise check50.Failure(
            rationale="Your solution raised the following exception: "
            f"{type(e).__name__}"
        ) from e

    if type(result) is not bool:
        msg = "Your function must return True or False."
        raise check50.Failure(msg)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example1():
    """test on example 1"""

    eingabe = "Hannah"
    expected = True

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_example2():
    """test on example 2"""

    eingabe = "Ein Esel lese nie."
    expected = True

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_example3():
    """test on example 3"""

    eingabe = "Max"
    expected = False

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_on_case_insensitive():
    """Your solution should ignore upper- and lowercase differences"""

    eingabe = "Aa"
    expected = True

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_empty_string():
    """an empty string should return True"""

    eingabe = ""
    expected = True

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_whitespace_string():
    """a string containing a single whitespace is considered a valid palindrom"""

    eingabe = " "
    expected = True

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_double_palindrom():
    """the same palindrome, separated by a empty space, should return True"""

    eingabe = "Anna Anna"
    expected = True

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_whitespaces_between_characters():
    """Test on spaces between characters"""

    eingabe = "a b a"
    expected = True

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_racecar():
    """a string containing a single whitespace is considered a vaklid palindrom"""

    eingabe = "racecar"
    expected = True

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_on_panama():
    """Test on a sentence"""

    eingabe = "A man, a plan, a canal: Panama"
    expected = True

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_on_numbers():
    """Your solution also checks numbers in a string"""

    eingabe = "12321"
    expected = True

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_on_numbers_invalid():
    """Your solution also checks numbers in a string"""

    eingabe = "12345"
    expected = False

    run_submission(eingabe, expected)


@check50.check(has_function)
def test_on_punctuation():
    """Your solution ignores punctuation"""

    eingabe = "!!!"
    expected = True

    run_submission(eingabe, expected)


@check50.check(compiles)
def no_slicing():
    """solution does not use slicing"""

    with Path.open(FILE_NAME, encoding="utf-8") as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Slice):
            msg = "String slicing is not allowed."
            raise check50.Failure(msg)


@check50.check(has_function)
def random_tests():
    """test randomly generated strings"""

    import random
    import string

    characters = string.ascii_letters + string.digits + " .,!?-"

    for _ in range(5):
        s = "".join(random.choice(characters) for _ in range(random.randint(0, 30)))

        cleaned = "".join(c.lower() for c in s if c.isalnum())

        expected = cleaned == cleaned[::-1]

        run_submission(s, expected)

    for _ in range(5):
        half = "".join(random.choice(characters) for _ in range(random.randint(1, 10)))

        middle = random.choice(characters) if random.choice([True, False]) else ""

        s = half + middle + half[::-1]

        run_submission(s, True)
