import check50

FILE_NAME = "strings.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def testString():
    """check output of strings.py"""

    expected = "equal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("HellO woRLd").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testInvalidString():
    """check output of strings.py"""

    expected = "unequal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("HellO woRLd!").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)
