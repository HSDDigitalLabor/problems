import check50
import check50.py

FILE_NAME = "divide.py"


@check50.check()
def exists():
    """divide.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """divide.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def test_positive_division():
    """divide(10, 3) returns 3"""
    module = check50.py.import_(FILE_NAME)
    result = module.divide(10, 3)
    if result != 3:
        msg = f"Expected 3 but got {result!r}"
        raise check50.Failure(msg)


@check50.check(compiles)
def test_negative_division():
    """divide(7, -3) returns -2"""
    module = check50.py.import_(FILE_NAME)
    result = module.divide(7, -3)
    if result != -2:
        msg = f"Expected -2 but got {result!r}"
        raise check50.Failure(msg)


@check50.check(compiles)
def test_truncation_toward_zero():
    """divide(-7, 3) returns -2"""
    module = check50.py.import_(FILE_NAME)
    result = module.divide(-7, 3)
    if result != -2:
        msg = f"Expected -2 but got {result!r}"
        raise check50.Failure(msg)


@check50.check(compiles)
def test_divide_by_one():
    """divide(42, 1) returns 42"""
    module = check50.py.import_(FILE_NAME)
    result = module.divide(42, 1)
    if result != 42:
        msg = f"Expected 42 but got {result!r}"
        raise check50.Failure(msg)


@check50.check(compiles)
def test_divide_by_minus_one():
    """divide(-42, -1) returns 42"""
    module = check50.py.import_(FILE_NAME)
    result = module.divide(-42, -1)
    if result != 42:
        msg = f"Expected 42 but got {result!r}"
        raise check50.Failure(msg)
