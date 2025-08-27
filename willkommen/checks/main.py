import check50


@check50.check()
def exists():
    """willkommen.py exists"""
    check50.exists("willkommen.py")


@check50.check(exists)
def testWillkommen():
    """check output of willkommen.py"""
    from re import match

    expected = "[Ww]illkommen, [Ww]elt!?$"
    actual = check50.run("python3 willkommen.py").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch("Willkommen, welt!\n", actual, help=help)
