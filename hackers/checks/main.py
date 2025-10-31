import check50
from re import match


FILE_NAME = "hackers.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def testFile1():
    """check output of file with in file: test.txt"""
    filename = "test"
    check50.include(f"files/{filename}.txt")

    expected = "Invalid count of IBANs: 1\n"
    actual = check50.run(f"python3 {FILE_NAME} {filename}.txt").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(exists)
def testFile2():
    """check output of file with in file: whistleblower.txt"""
    filename = "whistleblower"
    check50.include(f"files/{filename}.txt")

    expected = "Invalid count of IBANs: 14\n"
    actual = check50.run(f"python3 {FILE_NAME} {filename}.txt").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)

