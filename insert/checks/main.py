import check50
import check50.py

FILE_NAME = "insert.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """insert.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """function defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "searchInsert"):
        msg = "Function `searchInsert` not found in insert.py"
        raise check50.Failure(msg)


@check50.check(compiles)
def test_example1():
    """test on example 1"""
    module = check50.py.import_(FILE_NAME)

    nums = [1, 3, 5, 6]
    target = 5
    expected = 2

    result = module.searchInsert(nums, target)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(compiles)
def test_example2():
    """test on example 2"""
    module = check50.py.import_(FILE_NAME)

    nums = [1, 3, 5, 6]
    target = 2
    expected = 1

    result = module.searchInsert(nums, target)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(compiles)
def test_example3():
    """test on example 3"""
    module = check50.py.import_(FILE_NAME)

    nums = [1, 3, 5, 6]
    target = 7
    expected = 4

    result = module.searchInsert(nums, target)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(compiles)
def test_example4():
    """test on example 4"""
    module = check50.py.import_(FILE_NAME)

    nums = [1, 3, 5, 6]
    target = 0
    expected = 0

    result = module.searchInsert(nums, target)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(compiles)
def test_empty_list():
    """insert into empty list"""
    module = check50.py.import_(FILE_NAME)
    nums = []
    target = 10
    expected = 0
    result = module.searchInsert(nums, target)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(compiles)
def test_single_element_smaller():
    """single element, target smaller"""
    module = check50.py.import_(FILE_NAME)
    nums = [5]
    target = 2
    expected = 0
    result = module.searchInsert(nums, target)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(compiles)
def test_single_element_larger():
    """single element, target larger"""
    module = check50.py.import_(FILE_NAME)
    nums = [5]
    target = 9
    expected = 1
    result = module.searchInsert(nums, target)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(compiles)
def test_duplicates_before():
    """target matches first duplicate block"""
    module = check50.py.import_(FILE_NAME)
    nums = [1, 2, 5, 5, 5, 9]
    target = 5
    expected = 2
    result = module.searchInsert(nums, target)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(compiles)
def test_duplicates_insert_middle():
    """insert between duplicates"""
    module = check50.py.import_(FILE_NAME)
    nums = [1, 2, 5, 5, 9]
    target = 6
    expected = 4
    result = module.searchInsert(nums, target)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(compiles)
def test_negative_numbers():
    """list with negative numbers"""
    module = check50.py.import_(FILE_NAME)
    nums = [-10, -3, 0, 2, 9]
    target = -4
    expected = 1
    result = module.searchInsert(nums, target)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(compiles)
def test_middle_exact():
    """exact match in middle"""
    module = check50.py.import_(FILE_NAME)
    nums = [0, 4, 8, 12, 16, 20]
    target = 12
    expected = 3
    result = module.searchInsert(nums, target)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(compiles)
def test_between_middle():
    """target between two mid values"""
    module = check50.py.import_(FILE_NAME)
    nums = [0, 4, 8, 12, 16, 20]
    target = 10
    expected = 3
    result = module.searchInsert(nums, target)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


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

    module.searchInsert(lst, key)

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
