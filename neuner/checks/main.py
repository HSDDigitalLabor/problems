from pathlib import Path
import random
import check50
import check50.py

FILE_NAME = "neuner.py"


@check50.check()
def exists():
    """neuner.py is present"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """neuner.py imports without errors"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """function isValidProduct is defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "isValidProduct"):
        msg = f"Function `isValidProduct` not found in {FILE_NAME}"
        raise check50.Failure(msg)


@check50.check(has_function)
def test_valid_ints():
    """accepts a correct product (integers) via Neunerprobe"""
    module = check50.py.import_(FILE_NAME)
    # 247 * 71 = 17537 → Neunerprobe: gültig
    expected = True
    result = module.isValidProduct(247, 71, 17537)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_valid_strings():
    """accepts a correct product when inputs are strings"""
    module = check50.py.import_(FILE_NAME)
    # Gleiches Beispiel, aber als Strings
    expected = True
    result = module.isValidProduct("247", "71", "17537")
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_invalid_product_example():
    """rejects an incorrect product (Neunerprobe fails)"""
    module = check50.py.import_(FILE_NAME)
    # Beispiel aus der Beschreibung: Prüfsummen passen nicht
    expected = False
    result = module.isValidProduct(429, 357, 154153)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_invalid_product_small_change():
    """rejects a near-miss product differing by 1"""
    module = check50.py.import_(FILE_NAME)
    # 247 * 71 = 17537, aber hier 17538 → Neunerprobe falsch
    expected = False
    result = module.isValidProduct(247, 71, 17538)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_non_numeric_inputs():
    """returns False for non-numeric inputs"""
    module = check50.py.import_(FILE_NAME)
    expected = False
    result = module.isValidProduct("abc", "10", "20")
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))

    result = module.isValidProduct("12", "x3", "36")
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_empty_inputs():
    """returns False for empty or None inputs"""
    module = check50.py.import_(FILE_NAME)
    expected = False
    result = module.isValidProduct("", "10", "0")
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))

    result = module.isValidProduct(None, 10, 0)
    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_random_valid_products():
    """accepts random correct products"""
    module = check50.py.import_(FILE_NAME)

    random.seed(12345)  # deterministic tests

    for _ in range(10):  # 10 random valid tests
        a = random.randint(1, 99999)
        b = random.randint(1, 99999)
        c = a * b  # correct product → must be accepted

        expected = True
        result = module.isValidProduct(a, b, c)

        if result != expected:
            raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def test_random_invalid_products():
    """rejects random incorrect products"""
    module = check50.py.import_(FILE_NAME)

    a = random.randint(1, 99999)
    b = random.randint(1, 99999)
    c = a * b

    expected = True
    result = module.isValidProduct(a, b, c)

    msg = f"a={a}, b={b}, c={c} should be valid"
    if result != expected:
        msg += msg + f" but was {result}"
        raise check50.Failure(msg)
