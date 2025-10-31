import check50

import check50.py

FILE_NAME = "iban.py"


def calc_expected(a, b):
    return 98 - (a * int(1e16) + b * int(1e6) + 131400) % 97


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """iban.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """function defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "checkDigitsDE"):
        msg = "Function `checkDigitsDE` not found in iban.py"
        raise check50.Failure(msg)


@check50.check(has_function)
def test_example1():
    """test on example 1"""
    module = check50.py.import_(FILE_NAME)

    banking_code = 50010517
    account_number = 123456789

    expected = calc_expected(banking_code, account_number)

    result = module.checkDigitsDE(banking_code, account_number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example2():
    """test on example 2"""
    module = check50.py.import_(FILE_NAME)

    banking_code = 50010518
    account_number = 987654321

    expected = calc_expected(banking_code, account_number)

    result = module.checkDigitsDE(banking_code, account_number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example3():
    """test on example 3"""
    module = check50.py.import_(FILE_NAME)

    banking_code = 50010519
    account_number = 123123123

    expected = calc_expected(banking_code, account_number)

    result = module.checkDigitsDE(banking_code, account_number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example4():
    """test on example 4"""
    module = check50.py.import_(FILE_NAME)

    banking_code = 50010520
    account_number = 456456456

    expected = calc_expected(banking_code, account_number)

    result = module.checkDigitsDE(banking_code, account_number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example5():
    """test on example 5"""
    module = check50.py.import_(FILE_NAME)

    banking_code = 50010521
    account_number = 789789789

    expected = calc_expected(banking_code, account_number)

    result = module.checkDigitsDE(banking_code, account_number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example6():
    """test on example 6"""
    module = check50.py.import_(FILE_NAME)

    banking_code = 50010522
    account_number = 321321321

    expected = calc_expected(banking_code, account_number)

    result = module.checkDigitsDE(banking_code, account_number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example7():
    """test on example 7"""
    module = check50.py.import_(FILE_NAME)

    banking_code = 50010523
    account_number = 654654654

    expected = calc_expected(banking_code, account_number)

    result = module.checkDigitsDE(banking_code, account_number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example8():
    """test on example 8"""
    module = check50.py.import_(FILE_NAME)

    banking_code = 50010524
    account_number = 987987987

    expected = calc_expected(banking_code, account_number)

    result = module.checkDigitsDE(banking_code, account_number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))
