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
def testString1():
    """check output of strings.py"""

    expected = "equal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("hello world").stdout()
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


@check50.check(exists)
def testInvalidString2():
    """check output of strings.py"""

    expected = "unequal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("WORLD HELLO").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testInvalidString3():
    """check output of strings.py"""

    expected = "unequal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("12345 12345").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testInvalidString4():
    """check output of strings.py"""

    expected = "unequal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("hella warld").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)
