import check50
from re import escape


@check50.check()
def exists():
    """willkommen.py exists"""
    check50.exists("willkommen.py")


@check50.check(exists)
def testHello():
    """check output of Willkommen"""
    output = "Willkommen, Welt!"
    check50.run("python3 willkommen.py").stdout("Willkommen, Welt!").exit()
