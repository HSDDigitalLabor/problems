import check50

FILE_NAME = "strings.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def testString():
    """checking output on mixed-case"""

    expected = "equal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("HellO woRLd").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testStringLowercase():
    """checking output on lowercase"""

    expected = "equal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("hello world").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testStringUppercase():
    """checking output on uppercase"""

    expected = "equal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("HELLO WORLD").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testStringDifferentOrder():
    """asserting correctness with words in different order"""

    expected = "unequal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("World Hello").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testInvalidString():
    """checking output with exclamation mark"""

    expected = "unequal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("HellO woRLd!").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testInvalidString2():
    """checking output on invalid string"""

    expected = "unequal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("HellO woRLd Blabla").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testInvalidStringSameLengthNumbers():
    """checking output on string of same length"""

    expected = "unequal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("12345678901").stdout()
    if not actual.startswith(expected):
        help = "Checking the lengths of both string is not sufficient"
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testInvalidStringSameLengthString():
    """checking output on string of same length with chars"""

    expected = "unequal"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("abcdefghijk").stdout()
    if not actual.startswith(expected):
        help = "Checking the lengths of both string is not sufficient"
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)
