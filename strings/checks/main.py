import check50


@check50.check()
def exists():
    """string.py exists"""
    check50.exists("string.py")


@check50.check(exists)
def testString():
    """check output of string.py"""
    from re import match

    expected = "equal"
    actual = check50.run("python3 string.py").stdin("HellO woRLd").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(f"{expected}\n", actual, help=help)


@check50.check(exists)
def testInvalidString():
    """check output of string.py"""
    from re import match

    expected = "unequal"
    actual = check50.run("python3 string.py").stdin("HellO woRLd!").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(f"{expected}\n", actual, help=help)
