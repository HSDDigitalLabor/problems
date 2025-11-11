from pathlib import Path

import check50
import check50.py

FILE_NAME = "bubble.py"


# helper function for prettier list comparison
def assert_list_equal(actual, expected):
    if actual != expected:
        msg = f"Expected: {expected}\nGot     : {actual}"
        raise check50.Failure(msg)


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """bubble.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """bubble_sort function defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "bubble_sort"):
        msg = "Function `bubble_sort` not found in bubble.py"
        raise check50.Failure(msg)


@check50.check(has_function)
def sorts_small_list():
    """bubble_sort correctly sorts a small list"""
    module = check50.py.import_(FILE_NAME)
    lst = [3, 2, 1]
    sorted_lst = module.bubble_sort(lst.copy())
    expected = [1, 2, 3]
    assert_list_equal(sorted_lst, expected)


@check50.check(has_function)
def sorts_already_sorted():
    """bubble_sort leaves already sorted list unchanged"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 2, 3]
    sorted_lst = module.bubble_sort(lst.copy())
    expected = [1, 2, 3]
    assert_list_equal(sorted_lst, expected)


@check50.check(has_function)
def handles_duplicates():
    """bubble_sort handles duplicate numbers correctly"""
    module = check50.py.import_(FILE_NAME)
    lst = [3, 1, 3, 2]
    sorted_lst = module.bubble_sort(lst.copy())
    expected = [1, 2, 3, 3]
    assert_list_equal(sorted_lst, expected)


@check50.check(has_function)
def sorts_random_lists():
    """bubble_sort correctly sorts various random lists"""
    import random

    module = check50.py.import_(FILE_NAME)
    for _ in range(5):
        lst = random.sample(range(10), 5)  # random list of 5 unique numbers
        sorted_lst = module.bubble_sort(lst.copy())
        expected = sorted(lst)
        assert_list_equal(sorted_lst, expected)


@check50.check(has_function)
def sorts_edge_cases():
    """bubble_sort handles edge cases"""
    module = check50.py.import_(FILE_NAME)

    # empty list
    lst = []
    sorted_lst = module.bubble_sort(lst.copy())
    assert_list_equal(sorted_lst, [])

    # single element
    lst = [42]
    sorted_lst = module.bubble_sort(lst.copy())
    assert_list_equal(sorted_lst, lst)

    # all identical
    lst = [7, 7, 7, 7]
    sorted_lst = module.bubble_sort(lst.copy())
    assert_list_equal(sorted_lst, lst)


@check50.check()
def no_forbidden_methods():
    """does not use forbidden built-ins or operators"""
    import tokenize

    forbidden_tokens = {"sorted", "sort", "min", "max", "heapq"}
    forbidden_ops = {}

    with Path(FILE_NAME).open() as f:
        tokens = tokenize.generate_tokens(f.readline)

        for tok_type, tok_string, *_ in tokens:
            # Skip comments and string literals
            if tok_type in (tokenize.COMMENT, tokenize.STRING):
                continue

            if tok_string in forbidden_tokens or tok_string in forbidden_ops:
                msg = f"Found forbidden token or operator '{tok_string}' in your code"
                raise check50.Failure(msg)
