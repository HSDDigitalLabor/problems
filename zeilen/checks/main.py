import check50
import check50.py

FILE_NAME = "zeilen.py"


def pretty_matrix_diff(expected, actual):
    """Return a pretty diff between two matrices as a string with aligned columns."""
    lines = ["expected values in ():"]

    num_cols = max(
        len(row) for row in expected + actual
    )  # calculate the number of columns

    # calculate the maximum width for each column
    col_widths = []
    for col in range(num_cols):
        max_width = 0
        for row in expected + actual:
            if col < len(row):
                max_width = max(max_width, len(str(row[col])))
        col_widths.append(max_width)

    # build diff lines
    for i, (exp_row, act_row) in enumerate(zip(expected, actual, strict=False)):
        row_diff = []
        for j in range(num_cols):
            e = exp_row[j] if j < len(exp_row) else ""
            a = act_row[j] if j < len(act_row) else ""
            cell = f"{a}" if a == e else f"{a} ({e})"
            row_diff.append(cell.ljust(col_widths[j] + 4))  # pad with spaces
        lines.append(f"Row {i}: " + " | ".join(row_diff))

    return "\n".join(lines)


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """zeilen.py compiles"""
    check50.py.compile(FILE_NAME)


# rowMult tests
@check50.check(compiles)
def has_rowMult_function():
    module = check50.py.import_(FILE_NAME)
    FUNCTION_NAME = "rowMult"

    if not hasattr(module, FUNCTION_NAME):
        msg = f"Function {FUNCTION_NAME} not found in {FILE_NAME}"
        raise check50.Failure(msg)


@check50.check(has_rowMult_function)
def rowMult_is_inplace():
    """rowMult(): operates in place"""
    module = check50.py.import_(FILE_NAME)

    input = [[1, 2, 3], [1, 2, 3]]
    output = module.rowMult(input, 1, 1)

    if not output:
        # nothing was returned, which is also valid
        return

    if id(input) != id(output):
        msg = "rowMult() should operate inplace, no new list should be returned"
        raise check50.Failure(msg)


@check50.check(rowMult_is_inplace)
def rowMult_ignore_k():
    """rowMult(): has no effect with k=0"""
    import copy

    module = check50.py.import_(FILE_NAME)

    input = [[1, 2, 3], [1, 2, 3]]
    expected = copy.deepcopy(input)
    module.rowMult(input, 1, 0)

    if expected != input:
        msg = pretty_matrix_diff(expected, input)
        raise check50.Failure(msg)


@check50.check(has_rowMult_function)
def test_rowMult_example_1():
    """rowMult(M, 1, 8): multiply 2nd row by 8 (example 1)"""
    module = check50.py.import_(FILE_NAME)

    M = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    module.rowMult(M, 1, 8)

    expected = [
        [1, 2, 3, 4],
        [40, 48, 56, 64],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    if expected != M:
        msg = pretty_matrix_diff(expected, M)
        raise check50.Failure(msg)


@check50.check(has_rowMult_function)
def rowMult_invalid_indices():
    """rowMult(): ignores invalid indices"""
    import copy

    module = check50.py.import_(FILE_NAME)

    expected = [
        [1, 2],
        [3, 4],
    ]
    output = copy.deepcopy(expected)

    try:
        module.rowMult(output, -1, 2)
        module.rowMult(output, 3, 2)
    except IndexError:
        msg = (
            "IndexError raised, check that only 0 to length of column / row is allowed"
        )
        raise check50.Failure(msg) from None


# rowAdd tests
@check50.check(compiles)
def has_rowAdd_function():
    module = check50.py.import_(FILE_NAME)
    FUNCTION_NAME = "rowAdd"

    if not hasattr(module, FUNCTION_NAME):
        msg = f"Function {FUNCTION_NAME} not found in {FILE_NAME}"
        raise check50.Failure(msg)


@check50.check(has_rowAdd_function)
def rowAdd_is_inplace():
    """rowAdd(): operates in place"""
    module = check50.py.import_(FILE_NAME)

    input = [[1, 2, 3], [1, 2, 3]]
    output = module.rowAdd(input, 1, 1, 1)

    if not output:
        # nothing was returned, which is also valid
        return

    if id(input) != id(output):
        msg = "rowAdd() should operate inplace, no new list should be returned"
        raise check50.Failure(msg)


@check50.check(has_rowAdd_function)
def rowAdd_ignore_k():
    """rowAdd(M, i, j, 0): has no effect with k=0"""
    import copy

    module = check50.py.import_(FILE_NAME)

    input = [[1, 2, 3], [1, 2, 3]]
    expected = copy.deepcopy(input)
    module.rowAdd(input, 1, 1, 0)

    if expected != input:
        msg = pretty_matrix_diff(expected, input)
        raise check50.Failure(msg)


@check50.check(has_rowAdd_function)
def rowAdd_test_example():
    """rowAdd(M, 0, 2, -3): -3 * row 0 + row 2 (example 2)"""
    module = check50.py.import_(FILE_NAME)

    M = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    module.rowAdd(M, 0, 2, -3)

    expected = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [6, 4, 2, 0],
        [13, 14, 15, 16],
    ]

    if expected != M:
        msg = pretty_matrix_diff(expected, M)
        raise check50.Failure(msg)


@check50.check(has_rowAdd_function)
def rowAdd_invalid_indices():
    """rowAdd(): ignores invalid indices"""
    import copy

    module = check50.py.import_(FILE_NAME)

    expected = [
        [1, 2],
        [3, 4],
    ]
    output = copy.deepcopy(expected)

    try:
        module.rowAdd(output, -1, 1, 2)
        module.rowAdd(output, 0, 10, 2)
    except IndexError:
        msg = (
            "IndexError raised, check that only 0 to length of column / row is allowed"
        )
        raise check50.Failure(msg) from None


@check50.check(compiles)
def no_forbidden_methods():
    """does not use libraries"""
    import tokenize
    from pathlib import Path

    # forbidden libraries / functions and common aliases AND the import keyword
    forbidden = {"rref", "numpy", "sympy", "np", "sp", "import"}

    path = Path(FILE_NAME)

    with path.open() as f:
        tokens = list(tokenize.generate_tokens(f.readline))

        for tok_type, tok_string, *_ in tokens:
            # Skip comments and string literals
            if tok_type in (tokenize.COMMENT, tokenize.STRING):
                continue

            # Normalize to lowercase for case-insensitive check
            tok_lower = tok_string.lower()
            if tok_lower in forbidden:
                msg = f"Found forbidden function or library '{tok_string}'"
                raise check50.Failure(msg)
