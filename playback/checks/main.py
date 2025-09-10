import check50

FILE_NAME = "playback.py"


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
