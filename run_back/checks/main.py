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
        msg = "Function `binary_recursive` not found in binary_recursive.py"
        raise check50.Failure(msg)


@check50.check(has_function)
def test_sample_1():
    """sample test: finds 8 in list"""
    module = check50.py.import_(FILE_NAME)
    list = [6, 7, 8, 9, 10]
    result = module.binary_recursive(list, 8, 0, len(list) - 1)
    if result != 2:
        raise check50.Mismatch(2, result)


@check50.check(has_function)
def test_sample_2():
    """sample test: finds 17 in list"""
    module = check50.py.import_(FILE_NAME)
    list = [11, 13, 15, 17, 18]
    result = module.binary_recursive(list, 17, 0, len(list) - 1)
    if result != 3:
        raise check50.Mismatch(3, result)


@check50.check(has_function)
def test_sample_3():
    """sample test: returns -1 for missing element"""
    module = check50.py.import_(FILE_NAME)
    list = [3, 4, 5, 6, 7]
    result = module.binary_recursive(list, 1, 0, len(list) - 1)
    if result != -1:
        raise check50.Mismatch(-1, result)


@check50.check(has_function)
def test_sample_4():
    """sample test: empty list returns -1"""
    module = check50.py.import_(FILE_NAME)
    list = []
    result = module.binary_recursive(list, 13, 0, len(list) - 1)
    if result != -1:
        raise check50.Mismatch(-1, result)


@check50.check(has_function)
def test_first():
    """finds first element"""
    module = check50.py.import_(FILE_NAME)
    list = [1, 2, 3]
    result = module.binary_recursive(list, 1, 0, len(list) - 1)
    if result != 0:
        raise check50.Mismatch(0, result)


@check50.check(has_function)
def test_last():
    """finds last element"""
    module = check50.py.import_(FILE_NAME)
    list = [10, 20, 30, 40, 50]
    result = module.binary_recursive(list, 50, 0, len(list) - 1)
    if result != 4:
        raise check50.Mismatch(4, result)


@check50.check(has_function)
def test_duplicates():
    """handles duplicates correctly (returns any valid index)"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 2, 2, 2, 3, 4]
    result = module.binary_recursive(lst, 2, 0, len(lst) - 1)
    if result not in (1, 2, 3):
        msg = f"Expected index 1, 2 or 3 but got {result}"
        raise check50.Failure(msg)


@check50.check(has_function)
def test_negative_numbers():
    """works with negative numbers"""
    module = check50.py.import_(FILE_NAME)
    list = [-10, -5, 0, 5, 10]
    result = module.binary_recursive(list, -5, 0, len(list) - 1)
    if result != 1:
        raise check50.Mismatch(1, result)


@check50.check(has_function)
def test_random():
    """works on a random sorted list"""
    import random

    module = check50.py.import_(FILE_NAME)
    random.seed("git2025")
    lst = sorted(random.sample(range(0, 500), 30))
    key = random.choice(lst)
    expected = lst.index(key)
    result = module.binary_recursive(lst, key, 0, len(lst) - 1)

    if result != expected:
        raise check50.Mismatch(expected, result)


@check50.check(has_function)
def test_efficiency():
    """algorithm accesses only logarithmic number of elements"""

    from collections import UserList

    class WatchList(UserList):
        def __getitem__(self, index):
            self.accesses += 1
            return super().__getitem__(index)

    module = check50.py.import_(FILE_NAME)

    lst = WatchList(range(100_000))
    lst.accesses = 0

    module.binary_recursive(lst, 99999, 0, len(lst) - 1)

    if lst.accesses > 1000:
        msg = "Too many list accesses; algorithm may not be binary search"
        raise check50.Failure(msg)


@check50.check(has_function)
def test_recursion():
    """binary_recursive uses recursion"""
    module = check50.py.import_(FILE_NAME)

    calls = 0
    original = module.binary_recursive

    def wrapper(*args, **kwargs):
        nonlocal calls
        calls += 1
        return original(*args, **kwargs)

    # Monkey-patch function so that calls are counted
    module.binary_recursive = wrapper

    # Perform a search that requires recursion
    list = [1, 2, 3, 4, 5, 6, 7]
    result = module.binary_recursive(list, 6, 0, len(list) - 1)

    # Restore original function (cleanliness, not required but good practice)
    module.binary_recursive = original

    if calls <= 1:
        msg = "Your function does not appear to be recursive (only 1 call detected)."
        raise check50.Failure(msg)


@check50.check(has_function)
def no_forbidden_methods():
    """does not use forbidden built-ins or membership tests"""
    import tokenize
    from pathlib import Path

    forbidden = {"index", "sort", "enumerate", "find", "count", "map", "filter"}

    with Path(FILE_NAME).open() as f:
        tokens = list(tokenize.generate_tokens(f.readline))

        for tok_type, tok_string, _, _, _ in tokens:
            # Skip comments and strings
            if tok_type in (tokenize.COMMENT, tokenize.STRING):
                continue

            if tok_string in forbidden:
                msg = f"Found forbidden function '{tok_string}'"
                raise check50.Failure(msg)
