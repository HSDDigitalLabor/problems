from pathlib import Path

import check50
import check50.py

FILE_NAME = "sudoku.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """file compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """isValid function defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "isValid"):
        msg = f"Function `isValid` not found in {FILE_NAME}"
        raise check50.Failure(msg)


@check50.check(has_function)
def test_valid_board():
    """valid board (rows and columns)"""
    module = check50.py.import_(FILE_NAME)
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    expected = True
    result = module.isValid(board)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_empty_board():
    """empty board (all '.')"""
    module = check50.py.import_(FILE_NAME)
    board = [["." for _ in range(9)] for _ in range(9)]
    expected = True
    result = module.isValid(board)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_full_valid_board():
    """fully filled valid board"""
    module = check50.py.import_(FILE_NAME)
    board = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]
    expected = True
    result = module.isValid(board)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_row_duplicate():
    """detect duplicate in row"""
    module = check50.py.import_(FILE_NAME)
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "5"],  # duplicate 5 in row
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    expected = False
    result = module.isValid(board)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_column_duplicate():
    """detect duplicate in column"""
    module = check50.py.import_(FILE_NAME)
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        ["5", "9", "8", ".", ".", ".", ".", "6", "."],  # duplicate 5 in col 0
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    expected = False
    result = module.isValid(board)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_multiple_row_column_duplicates():
    """board with multiple row and column duplicates"""
    module = check50.py.import_(FILE_NAME)
    board = [
        ["1", "1", "2", ".", "3", ".", ".", ".", "."],  # row duplicate
        ["2", ".", ".", ".", ".", ".", ".", ".", "."],
        ["3", ".", ".", ".", ".", ".", ".", ".", "."],
        ["4", ".", ".", ".", ".", ".", ".", ".", "."],
        ["5", ".", ".", ".", ".", ".", ".", ".", "."],
        ["6", ".", ".", ".", ".", ".", ".", ".", "."],
        ["7", ".", ".", ".", ".", ".", ".", ".", "."],
        ["8", ".", ".", ".", ".", ".", ".", ".", "."],
        ["1", ".", ".", ".", ".", ".", ".", ".", "."],  # column duplicate
    ]
    expected = False
    result = module.isValid(board)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check()
def no_forbidden_methods():
    """does not use forbidden built-ins or operators"""
    import tokenize

    forbidden_tokens = {".index(", ".count("}
    forbidden_ops = set()

    with Path(FILE_NAME).open() as f:
        tokens = tokenize.generate_tokens(f.readline)

        for tok_type, tok_string, *_ in tokens:
            # Skip comments and string literals
            if tok_type in (tokenize.COMMENT, tokenize.STRING):
                continue

            if tok_string in forbidden_tokens or tok_string in forbidden_ops:
                msg = f"Found forbidden token or operator '{tok_string}' in your code"
                raise check50.Failure(msg)
