import check50


@check50.check()
def exists():
    """faces.py exists"""
    check50.exists("faces.py")


@check50.check(exists)
def testFaces():
    """check output of faces.py"""
    from re import match

    expected = "Hallo 🙂"
    actual = check50.run("python3 faces.py").stdin("Hallo :)").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(f"{expected}\n", actual, help=help)
