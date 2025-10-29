import random
from pathlib import Path

import check50
import check50.py

FILE_NAME = "linear.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """linear.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """linear_search function defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "linear_search"):
        msg = "Function `linear_search` not found in linear.py"
        raise check50.Failure(msg)


@check50.check(has_function)
def test_found_first():
    """finds first occurrence of key in list"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 2, 3]
    key = 1
    expected = lst.index(key)
    result = module.linear_search(lst, key)
    if result != expected:
        raise check50.Mismatch(expected, result, help=f"Expected index {expected}")


@check50.check(has_function)
def test_found_middle():
    """finds middle element on unsorted"""
    module = check50.py.import_(FILE_NAME)
    lst = [5, 4, 3, 2, 1]
    key = 3
    expected = lst.index(key)
    result = module.linear_search(lst, key)
    if result != expected:
        raise check50.Mismatch(expected, result, help=f"Expected index {expected}")


@check50.check(has_function)
def test_not_found():
    """returns -1 when key not found"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 2, 3]
    key = 10
    expected = -1
    result = module.linear_search(lst, key)
    if result != expected:
        raise check50.Mismatch(expected, result, help="Expected -1 when key not found")


@check50.check(has_function)
def test_empty_list():
    """returns -1 on empty list"""
    module = check50.py.import_(FILE_NAME)
    lst = []
    key = 10
    expected = -1
    result = module.linear_search(lst, key)
    if result != expected:
        raise


@check50.check(has_function)
def test_random():
    """works with random lists"""
    module = check50.py.import_(FILE_NAME)

    random.seed("git2025")
    lst = [random.randint(0, 9) for _ in range(random.randint(5, 13))]
    key = random.choice(lst)
    expected = lst.index(key)
    result = module.linear_search(lst, key)

    if result != expected:
        raise check50.Mismatch(
            expected,
            result,
            help=f"Expected index {expected} for key {key} in list {lst}",
        )


@check50.check(has_function)
def no_forbidden_methods():
    """does not use forbidden built-ins or operators"""
    import tokenize

    forbidden_tokens = {
        "index",
        "sort",
        "enumerate",
        "find",
        "count",
        "map",
        "filter",
        "any",
        "all",
        "next",
    }

    with Path(FILE_NAME).open() as f:
        tokens = list(tokenize.generate_tokens(f.readline))

        for i, (tok_type, tok_string, _, _, _) in enumerate(tokens):
            # Skip comments and string literals
            if tok_type in (tokenize.COMMENT, tokenize.STRING):
                continue

            # Disallow built-ins
            if tok_string in forbidden_tokens:
                msg = f"Found forbidden token '{tok_string}' in your code"
                raise check50.Failure(msg)

            # Check for forbidden membership tests: "if <expr> in <expr>"
            if tok_string == "in":
                # Look backwards a few tokens to see if we're inside a for loop
                lookback = [t[1] for t in tokens[max(0, i - 3) : i]]
                if "for" not in lookback:  # only flag if not inside a for statement
                    msg = "Found forbidden membership test using 'in'"
                    raise check50.Failure(msg)
