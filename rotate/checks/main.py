import check50
import check50.py

FILE_NAME = "rotate.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """rotate.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """rotate_list function defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "rotate_list"):
        msg = f"Function `rotate_list` not found in {FILE_NAME}"
        raise check50.Failure(msg)


@check50.check(has_function)
def empty_list():
    """empty list is unchanged"""
    module = check50.py.import_(FILE_NAME)
    lst = []
    ret = module.rotate_list(lst, 0)
    expected = []
    if id(lst) != id(ret):
        msg = "got new list, address of list changes"
        raise check50.Failure(msg)

    if ret != expected:
        msg = f"expected {expected}, got {lst}"
        raise check50.Failure(msg)


@check50.check(has_function)
def zero_rotation():
    """Rotation by 0 keeps list unchanged"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 2, 3]
    ret = module.rotate_list(lst, 0)
    expected = [1, 2, 3]
    if id(lst) != id(ret):
        msg = "got new list, address of list changes"
        raise check50.Failure(msg)

    if ret != expected:
        msg = f"expected {expected}, got {lst}"
        raise check50.Failure(msg)


@check50.check(has_function)
def check_inplace():
    """check list is used in place"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 2, 3, 4, 5, 6, 7]
    ret = module.rotate_list(lst, 3)
    if id(lst) != id(ret):
        msg = "got new list, address of list changes"
        raise check50.Failure(msg)


@check50.check(check_inplace)
def rotation_equal_length():
    """Rotation by list length keeps list unchanged"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 2, 3, 4]
    module.rotate_list(lst, 4)
    expected = [1, 2, 3, 4]
    if lst != expected:
        msg = f"expected {expected}, got {lst}"
        raise check50.Failure(msg)


@check50.check(check_inplace)
def rotation_greater_than_length():
    """Rotation greater than list length works"""
    module = check50.py.import_(FILE_NAME)
    lst = [1, 2, 3]
    module.rotate_list(lst, 4)
    expected = [3, 1, 2]
    if lst != expected:
        msg = f"expected {expected}, got {lst}"
        raise check50.Failure(msg)


@check50.check(check_inplace)
def negatives():
    """Rotation with negative numbers works"""
    module = check50.py.import_(FILE_NAME)
    lst = [-1, -100, 3, 99]
    module.rotate_list(lst, 3)
    expected = [-100, 3, 99, -1]
    if lst != expected:
        msg = f"expected {expected}, got {lst}"
        raise check50.Failure(msg)
