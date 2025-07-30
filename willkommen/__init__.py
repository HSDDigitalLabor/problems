import check50
from re import escape


@check50.check()
def exists():
    """bank.py exists"""
    check50.exists("bank.py")


@check50.check(exists)
def testHello():
    """input of \"Hello\" yields output of $0"""
    input = "Hello"
    output = "$0"
    check50.run("python3 bank.py").stdin(input, prompt=True).stdout(regex(output), output, regex=True).exit()
