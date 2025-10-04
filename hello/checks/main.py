import random
import string

import check50


@check50.check()
def exists():
    """hello.py exists"""
    check50.exists("hello.py")


@check50.check(exists)
def testHelloEmma():
    """check output of hello.py"""

    expected = "Hallo, Emma"
    actual = check50.run("python3 hello.py").stdin("Emma").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testHelloTom():
    """check output of hello.py"""

    expected = "Hallo, Tom"
    actual = check50.run("python3 hello.py").stdin("Tom").stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)


@check50.check(exists)
def testHelloRandom():
    """check output of hello.py with a random name"""

    # generate a random name (5-8 letters)
    name = "".join(random.choices(string.ascii_letters, k=random.randint(5, 8)))
    expected = f"Hallo, {name}"
    actual = check50.run("python3 hello.py").stdin(name).stdout()
    if not actual.startswith(expected):
        help = None
        msg = f"{expected}\n"
        raise check50.Mismatch(msg, actual, help=help)
