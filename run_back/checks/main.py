import check50
import check50.py

FILE_NAME = "run_back.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """run_back.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """binary_recursive function defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "binary_recursive"):
        msg = "Function `binary_recursive` not found in run_back.py"
        raise check50.Failure(msg)


@check50.check(has_function)
def test_found_first():
    """finds first element"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 2, 3]
    key = 1
    expected = lst.index(key)
    result = module.binary_recursive(lst, key)
    if result != expected:
        raise check50.Mismatch(expected, result, help=f"Expected index {expected}")


@check50.check(has_function)
def test_found_middle():
    """finds middle element"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 2, 3, 4, 5]
    key = 3
    expected = lst.index(key)
    result = module.binary_recursive(lst, key)
    if result != expected:
        raise check50.Mismatch(expected, result, help=f"Expected index {expected}")


@check50.check(has_function)
def test_found_last():
    """finds last element"""
    module = check50.py.import_(FILE_NAME)
    lst = [10, 20, 30, 40, 50]
    key = 50
    expected = lst.index(key)
    result = module.binary_recursive(lst, key)
    if result != expected:
        raise check50.Mismatch(expected, result, help=f"Expected index {expected}")


@check50.check(has_function)
def test_not_found():
    """returns -1 when key not in list"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 3, 5, 7, 9]
    key = 4
    result = module.binary_recursive(lst, key)
    if result != -1:
        raise check50.Mismatch(-1, result, help="Expected -1 when key not found")


@check50.check(has_function)
def test_empty_list():
    """returns -1 on empty list"""
    module = check50.py.import_(FILE_NAME)
    lst = []
    key = 10
    result = module.binary_recursive(lst, key)
    if result != -1:
        raise check50.Mismatch(-1, result, help="Expected -1 on empty list")


@check50.check(has_function)
def test_duplicates():
    """handles duplicates correctly (returns any valid index)"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 2, 2, 2, 3, 4]
    key = 2
    result = module.binary_recursive(lst, key)
    if result not in [1, 2, 3]:
        msg = f"Expected index 1, 2, or 3 but got {result}"
        raise check50.Failure(msg)


@check50.check(has_function)
def test_negative_numbers():
    """works with negative numbers"""
    module = check50.py.import_(FILE_NAME)
    lst = [-10, -5, 0, 5, 10]
    key = -5
    expected = lst.index(key)
    result = module.binary_recursive(lst, key)
    if result != expected:
        raise check50.Mismatch(expected, result)


@check50.check(has_function)
def test_random():
    """works on random sorted lists"""
    import random

    module = check50.py.import_(FILE_NAME)
    random.seed("cs50binary")
    lst = sorted(random.sample(range(0, 500), 30))
    key = random.choice(lst)
    expected = lst.index(key)
    result = module.binary_recursive(lst, key)
    if result != expected:
        raise check50.Mismatch(
            expected,
            result,
            help=f"Expected index {expected} for key {key} in list {lst}",
        )


@check50.check(has_function)
def test_efficiency():
    """performs well on large lists"""
    from collections import UserList

    class WatchList(UserList):
        def __getitem__(self, index):
            self.accesses += 1
            return super().__getitem__(index)

    module = check50.py.import_(FILE_NAME)

    lst = WatchList(range(100_000))
    lst.accesses = 0
    key = 99999

    module.binary_recursive(lst, key)

    if lst.accesses > 1000:  # binary search should only need ~17 accesses
        msg = "too many element accesses on large list"
        raise check50.Failure(msg)


@check50.check(has_function)
def no_forbidden_methods():
    """does not use forbidden built-ins or operators"""
    import tokenize
    from pathlib import Path

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
