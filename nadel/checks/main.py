import check50
import check50.py

FILE_NAME = "nadel.py"


@check50.check()
def exists():
    """nadel.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """nadel.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def test_basic_occurrence():
    """first occurrence of 'sad' in 'sadbutsad' is 0"""
    module = check50.py.import_(FILE_NAME)
    result = module.str_index("sadbutsad", "sad")
    if result != 0:
        msg = f"Expected 0 but got {result!r}"
        raise check50.Failure(msg)


@check50.check(compiles)
def test_not_found():
    """needle 'leeto' is not found in 'leetcode'"""
    module = check50.py.import_(FILE_NAME)
    result = module.str_index("leetcode", "leeto")
    if result != -1:
        msg = f"Expected -1 but got {result!r}"
        raise check50.Failure(msg)


@check50.check(compiles)
def test_needle_at_end():
    """first occurrence of 'sad' in 'butsadsad' is 3"""
    module = check50.py.import_(FILE_NAME)
    result = module.str_index("butsadsad", "sad")
    if result != 3:
        msg = f"Expected 3 but got {result!r}"
        raise check50.Failure(msg)


@check50.check(compiles)
def test_needle_equals_haystack():
    """needle equals haystack"""
    module = check50.py.import_(FILE_NAME)
    result = module.str_index("needle", "needle")
    if result != 0:
        msg = f"Expected 0 but got {result!r}"
        raise check50.Failure(msg)


@check50.check(compiles)
def test_needle_longer_than_haystack():
    """needle longer than haystack"""
    module = check50.py.import_(FILE_NAME)
    result = module.str_index("short", "longerneedle")
    if result != -1:
        msg = f"Expected -1 but got {result!r}"
        raise check50.Failure(msg)


@check50.check(compiles)
def test_multiple_occurrences():
    """first occurrence of 'abc' in 'abcabcabc' is 0"""
    module = check50.py.import_(FILE_NAME)
    result = module.str_index("abcabcabc", "abc")
    if result != 0:
        msg = f"Expected 0 but got {result!r}"
        raise check50.Failure(msg)
