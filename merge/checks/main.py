from pathlib import Path

import check50
import check50.py

FILE_NAME = "merge.py"


# Helper for consistent error messages
def assert_list_equal(actual, expected, func_name="merge"):
    if actual != expected:
        msg = (
            f"{func_name} returned the wrong list.\n"
            f"Expected: {expected}\n"
            f"Got     : {actual}"
        )
        raise check50.Failure(msg)


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """merge.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """merge function defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "merge"):
        msg = "Function `merge` not found in merge.py"
        raise check50.Failure(msg)


@check50.check(has_function)
def merges_basic_case():
    """merges two small sorted lists correctly"""
    module = check50.py.import_(FILE_NAME)
    lst1 = [1, 3, 5]
    lst2 = [2, 4, 6]
    result = module.merge(lst1, lst2)
    expected = [1, 2, 3, 4, 5, 6]
    assert_list_equal(result, expected)


@check50.check(has_function)
def merges_with_duplicates():
    """handles duplicate numbers correctly"""
    module = check50.py.import_(FILE_NAME)
    lst1 = [1, 2, 2, 3]
    lst2 = [2, 3, 4]
    result = module.merge(lst1, lst2)
    expected = [1, 2, 2, 2, 3, 3, 4]
    assert_list_equal(result, expected)


@check50.check(has_function)
def merges_with_negatives():
    """merges lists containing negative numbers"""
    module = check50.py.import_(FILE_NAME)
    lst1 = [-3, -1, 2]
    lst2 = [-2, 0, 3]
    result = module.merge(lst1, lst2)
    expected = [-3, -2, -1, 0, 2, 3]
    assert_list_equal(result, expected)


@check50.check(has_function)
def merges_with_empty_lists():
    """handles empty lists correctly"""
    module = check50.py.import_(FILE_NAME)

    # first empty
    lst1 = []
    lst2 = [1, 2, 3]
    result = module.merge(lst1, lst2)
    expected = [1, 2, 3]
    assert_list_equal(result, expected)

    # second empty
    lst1 = [4, 5, 6]
    lst2 = []
    result = module.merge(lst1, lst2)
    expected = [4, 5, 6]
    assert_list_equal(result, expected)

    # both empty
    lst1 = []
    lst2 = []
    result = module.merge(lst1, lst2)
    expected = []
    assert_list_equal(result, expected)


@check50.check(has_function)
def sorts_random_lists():
    """merge correctly merges various random lists"""
    import random

    module = check50.py.import_(FILE_NAME)
    random.seed("git2025")
    for _ in range(5):
        lst1 = random.sample(range(10), 5)  # random list of 5 unique numbers
        lst2 = random.sample(range(10), 5)  # random list of 5 unique numbers
        lst1 = sorted(lst1)
        lst2 = sorted(lst2)
        merged_lst = module.merge(lst1.copy(), lst2.copy())

        expected = sorted(lst1 + lst2)

        assert_list_equal(merged_lst, expected)


@check50.check()
def no_forbidden_methods():
    """does not use forbidden built-ins or operators"""
    import tokenize

    forbidden_tokens = {"sorted", "sort", "min", "max", "heapq"}
    with Path(FILE_NAME).open() as f:
        tokens = tokenize.generate_tokens(f.readline)
        for tok_type, tok_string, *_ in tokens:
            if tok_type in (tokenize.COMMENT, tokenize.STRING):
                continue
            if tok_string in forbidden_tokens:
                msg = f"Found forbidden token '{tok_string}' in your code"
                raise check50.Failure(msg)
