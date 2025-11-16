from pathlib import Path

import check50
import check50.py

FILE_NAME = "intervals.py"


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
    """intervals.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """merge function defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "merge"):
        msg = f"Function `merge` not found in {FILE_NAME}"
        raise check50.Failure(msg)


@check50.check(has_function)
def example1():
    """merges touching intervals"""
    module = check50.py.import_(FILE_NAME)
    intervals = [[1, 4], [4, 5]]
    expected = [[1, 5]]
    result = module.merge(intervals)
    assert_list_equal(result, expected)


@check50.check(has_function)
def example2():
    """merges unsorted intervals correctly"""
    module = check50.py.import_(FILE_NAME)
    intervals = [[4, 7], [1, 4]]
    expected = [[1, 7]]
    result = module.merge(intervals)
    assert_list_equal(result, expected)


@check50.check(has_function)
def example3():
    """merges separated intervals"""
    module = check50.py.import_(FILE_NAME)
    intervals = [[1, 2], [3, 4], [5, 6]]
    expected = [[1, 2], [3, 4], [5, 6]]
    result = module.merge(intervals)
    assert_list_equal(result, expected)


@check50.check(has_function)
def overlapping():
    """merges multiple overlapping intervals"""
    module = check50.py.import_(FILE_NAME)
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    expected = [[1, 6], [8, 10], [15, 18]]
    result = module.merge(intervals)
    assert_list_equal(result, expected)


@check50.check(has_function)
def merges_multiple_overlaps():
    """merges multiple overlapping intervals"""
    module = check50.py.import_(FILE_NAME)
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    expected = [[1, 6], [8, 10], [15, 18]]
    result = module.merge(intervals)
    assert_list_equal(result, expected)


@check50.check(has_function)
def merges_nested_intervals():
    """handles intervals nested within others"""
    module = check50.py.import_(FILE_NAME)
    intervals = [[1, 10], [2, 5], [3, 4]]
    expected = [[1, 10]]
    result = module.merge(intervals)
    assert_list_equal(result, expected)


@check50.check(has_function)
def merges_single_interval():
    """returns same interval if only one provided"""
    module = check50.py.import_(FILE_NAME)
    intervals = [[5, 7]]
    expected = [[5, 7]]
    result = module.merge(intervals)
    assert_list_equal(result, expected)


@check50.check(has_function)
def handles_empty_input():
    """returns [] for empty input"""
    module = check50.py.import_(FILE_NAME)
    intervals = []
    expected = []
    result = module.merge(intervals)
    assert_list_equal(result, expected)


@check50.check(has_function)
def handles_non_overlapping():
    """returns intervals unchanged if none overlap"""
    module = check50.py.import_(FILE_NAME)
    intervals = [[1, 2], [3, 4], [5, 6]]
    expected = [[1, 2], [3, 4], [5, 6]]
    result = module.merge(intervals)
    assert_list_equal(result, expected)


@check50.check(has_function)
def merges_chain_overlaps():
    """merges chain overlaps where intervals connect indirectly"""
    module = check50.py.import_(FILE_NAME)
    intervals = [[1, 3], [2, 4], [4, 5], [6, 7]]
    expected = [[1, 5], [6, 7]]
    result = module.merge(intervals)
    assert_list_equal(result, expected)


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
