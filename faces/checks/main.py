import check50


@check50.check()
def exists():
    """faces.py exists"""
    check50.exists("faces.py")


@check50.check(exists)
def testFaceUp():
    """check output of faces.py"""

    expected = "Hallo 🙂"
    actual = check50.run("python3 faces.py").stdin("Hallo :)").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testFaceDown():
    """check output of faces.py"""

    expected = "Hallo 🙁"
    actual = check50.run("python3 faces.py").stdin("Hallo :(").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testFaceTwo():
    """check output of faces.py"""

    expected = "Hallo 🙂, Tschüss 🙁"
    actual = check50.run("python3 faces.py").stdin("Hallo :), Tschüss :(").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)
