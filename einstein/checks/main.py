import check50

FILE_NAME = "einstein.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def testOnVideoExample():
    """testing using the example in the video"""

    expected = "4500000000000000000"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("50").stdout()
    if expected not in actual:
        raise check50.Mismatch(expected, actual)


@check50.check(exists)
def testExample1():
    """testing using the first example"""

    expected = "90000000000000000"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("1").stdout()
    if expected not in actual:
        raise check50.Mismatch(expected, actual)


@check50.check(exists)
def testExample2():
    """testing using the second example"""

    expected = "1260000000000000000"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("14").stdout()
    if expected not in actual:
        raise check50.Mismatch(expected, actual)
