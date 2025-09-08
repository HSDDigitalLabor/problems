import check50


@check50.check()
def exists():
    """hello.py exists"""
    check50.exists("hello.py")


@check50.check(exists)
def testHello():
    """check output of hello.py"""
    from re import match

    expected = "Hallo, Emma"
    actual = check50.run("python3 hello.py").stdin("Emma").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(f"{expected}\n", actual, help=help)
