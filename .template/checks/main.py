from pathlib import Path

import check50

FILE_NAME = "willkommen.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def testFile():
    """check output of file"""
    from re import match

    expected = ""
    actual = check50.run(f"python3 {FILE_NAME}").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check()
def no_forbidden_methods():
    """solution does not use forbidden built-ins"""
    FORBIDDEN = ["str.lower(", "str.upper(", ".count("]
    with Path.open(FILE_NAME) as f:
        code = f.read()
    for method in FORBIDDEN:
        if method in code:
            msg = f"Forbidden method used: {method}"
            raise check50.Failure(msg)
