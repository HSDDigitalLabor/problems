import check50


@check50.check()
def exists():
    """cs50_subscription.py exists"""
    check50.exists("cs50_subscription.py")


@check50.check(exists)
def testSubscription():
    """check output of cs50_subscription.py"""
    from re import match

    expected = r"e9c0f0fd-4be3-45b6-b1fe-18bde81c56f7"
    actual = check50.run("python3 cs50_subscription.py").stdout()
    if not match(expected, actual):
        help = None
        msg = "Something got wrong please try again\n"
        raise check50.Mismatch(msg, actual, help=help)
