from pathlib import Path

import check50

FILE_NAME = "luhn.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def testUIC1():
    """check valid UIC: 31 81 665 0 286-0"""
    from re import match

    expected = "Die UIC-Wagennummer ist gültig."
    actual = check50.run(f"python3 {FILE_NAME}").stdin("31 81 665 0 286-0").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(exists)
def testUIC2():
    """check valid UIC: 93 81 4 011 090-0"""
    from re import match

    expected = "Die UIC-Wagennummer ist gültig.\n"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("93 81 4 011 090-0").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(exists)
def testUIC3():
    """check valid UIC: 93 81 4 011 091-8"""
    from re import match

    expected = "Die UIC-Wagennummer ist gültig.\n"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("93 81 4 011 091-8").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(exists)
def testUIC4():
    """check invalid UIC: 93 81 4 011 090-6"""
    from re import escape, match

    expected = escape("Die UIC-Wagennummer ist ungültig [Prüfziffer: 0].\n")  # escape
    actual = check50.run(f"python3 {FILE_NAME}").stdin("93 81 4 011 090-6").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)
