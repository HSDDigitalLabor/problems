import check50

FILE_NAME = "playback.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def testFile():
    """checking output on first example"""
    from re import match

    input = "Grundlagen der Informatik II"
    expected = "Grundlagen...der...Informatik...II"
    actual = check50.run(f"python3 {FILE_NAME}").stdin(input).stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(exists)
def testFile2():
    """checking output on second example"""
    from re import match

    input = "Python ist einfach zu lernen und vielseitig einsetzbar."
    expected = "Python...ist...einfach...zu...lernen...und...vielseitig...einsetzbar."
    actual = check50.run(f"python3 {FILE_NAME}").stdin(input).stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(exists)
def testFile3():
    """checking output on test input"""
    from re import match

    input = "Test Test"
    expected = input.replace(" ", "...")
    actual = check50.run(f"python3 {FILE_NAME}").stdin(input).stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)
