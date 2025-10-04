import check50


@check50.check()
def exists():
    """string.py exists"""
    check50.exists("string.py")


@check50.check(exists)
def testString():
    """check output of string.py"""

    expected = "equal"
    actual = check50.run("python3 string.py").stdin("HellO woRLd").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testInvalidString():
    """check output of string.py"""

    expected = "unequal"
    actual = check50.run("python3 string.py").stdin("HellO woRLd!").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)
