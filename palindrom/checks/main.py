import check50
import check50.py

FILE_NAME = "palindrom.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """palindrom.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """function defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "isPalindrome"):
        msg = "Function `isPalindrome` not found in palindrom.py"
        raise check50.Failure(msg)


@check50.check(has_function)
def test_example1():
    """test on example 1"""
    module = check50.py.import_(FILE_NAME)

    number = 12344321
    expected = True

    result = module.isPalindrome(number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example2():
    """test on example 2"""
    module = check50.py.import_(FILE_NAME)

    number = 12345
    expected = False

    result = module.isPalindrome(number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example3():
    """test on example 3"""
    module = check50.py.import_(FILE_NAME)

    number = 1221
    expected = True

    result = module.isPalindrome(number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example4():
    """test on example 4"""
    module = check50.py.import_(FILE_NAME)

    number = 1
    expected = True

    result = module.isPalindrome(number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example5():
    """test on example 5"""
    module = check50.py.import_(FILE_NAME)

    number = 9999
    expected = True

    result = module.isPalindrome(number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example6():
    """test on example 6"""
    module = check50.py.import_(FILE_NAME)

    number = 123454321
    expected = True

    result = module.isPalindrome(number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example7():
    """test on example 7"""
    module = check50.py.import_(FILE_NAME)

    number = 10
    expected = False

    result = module.isPalindrome(number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_example8():
    """test on example 8"""
    module = check50.py.import_(FILE_NAME)

    number = 1000021
    expected = False

    result = module.isPalindrome(number)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def random_tests():
    """randomized tests"""
    import random

    random.seed("git2025")
    module = check50.py.import_(FILE_NAME)

    for _ in range(10):
        n = random.randint(-(10**12), 10**12)

        s = str(n)
        expected = s == s[::-1] if n >= 0 else False
        result = module.isPalindrome(n)

        if result != expected:
            raise check50.Mismatch(str(expected), str(result))
