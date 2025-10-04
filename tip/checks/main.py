import ast
from pathlib import Path
from re import match

import check50

FILE_NAME = "tip.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def functions_exist():
    """check that required functions are defined"""
    with Path.open(FILE_NAME) as f:
        tree = ast.parse(f.read(), filename=FILE_NAME)

    # collect all function names in the file
    func_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    }

    required = {"main", "currency_to_float", "get_currency_symbol"}
    missing = required - func_names
    if missing:
        msg = f"Missing required function(s): {', '.join(missing)}"
        raise check50.Failure(msg)


@check50.check(functions_exist)
def test2870():
    """check output for input 28.70€"""
    expected = "Tip 5%: 1.44€\nTip 10%: 2.87€\nTip 15%: 4.30€"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("28.70€").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(functions_exist)
def test1000():
    """check output for input 10.00€"""
    expected = "Tip 5%: 0.50€\nTip 10%: 1.00€\nTip 15%: 1.50€"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("10.00€").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(functions_exist)
def test5432():
    """check output for input 54.32€"""
    expected = "Tip 5%: 2.72€\nTip 10%: 5.43€\nTip 15%: 8.15€"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("54.32€").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(functions_exist)
def testSmall():
    """check output for small input 1.00€"""
    expected = "Tip 5%: 0.05€\nTip 10%: 0.10€\nTip 15%: 0.15€"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("1.00€").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(functions_exist)
def testRandom():
    """check output for random input 99.99€"""
    expected = "Tip 5%: 5.00€\nTip 10%: 10.00€\nTip 15%: 15.00€"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("99.99€").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)
