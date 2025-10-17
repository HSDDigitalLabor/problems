from pathlib import Path
import random as rand

import check50

FILE_NAME = "luhn.py"


def generate_Luhn(number):
    digits = [int(d) for d in number]
    # double every second digit starting from the rightmost
    for i in range(len(digits) - 1, -1, -2):
        doubled = digits[i] * 2
        digits[i] = doubled - 9 if doubled > 9 else doubled
    checksum = (10 - sum(digits) % 10) % 10
    return checksum


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def testUIC1():
    """check valid UIC: 31 81 665 0 286-0"""
    from re import match

    expected = "Die UIC-Wagennummer ist gültig."
    actual = check50.run(f"python3 {FILE_NAME}").stdin("31 81 665 0 286-0").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(exists)
def testUIC2():
    """check valid UIC: 93 81 4 011 090-0"""
    from re import match

    expected = "Die UIC-Wagennummer ist gültig.\n"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("93 81 4 011 090-0").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(exists)
def testUIC3():
    """check valid UIC: 93 81 4 011 091-8"""
    from re import match

    expected = "Die UIC-Wagennummer ist gültig.\n"
    actual = check50.run(f"python3 {FILE_NAME}").stdin("93 81 4 011 091-8").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(exists)
def testUICRand():
    """check random UIC-Wagennummer"""
    from re import match

    UIC_digits = [str(rand.randint(0, 9)) for _ in range(11)]
    prüfziffer = generate_Luhn("".join(UIC_digits))
    UIC_number = "".join(UIC_digits) + str(prüfziffer)
    expected = "Die UIC-Wagennummer ist gültig.\n"
    actual = check50.run(f"python3 {FILE_NAME}").stdin(UIC_number).stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(exists)
def testUIC4():
    """check invalid UIC: 93 81 4 011 090-6"""
    from re import escape, match

    expected = escape("Die UIC-Wagennummer ist ungültig [Prüfziffer: 0].\n")  # escape
    actual = check50.run(f"python3 {FILE_NAME}").stdin("93 81 4 011 090-6").stdout()
    if not match(expected, actual):
        help = None
        raise check50.Mismatch(expected, actual, help=help)


@check50.check(exists)
def hidden_valid_random_uic():
    """hidden test for Luhn validity"""
    import random
    from re import match

    random.seed("git2025")
    base_digits = [str(random.randint(0, 9)) for _ in range(11)]

    # build Luhn check digit
    digits = [int(d) for d in "".join(base_digits)]
    for i in range(len(digits) - 1, -1, -2):
        doubled = digits[i] * 2
        digits[i] = doubled - 9 if doubled > 9 else doubled
    checksum = (10 - sum(digits) % 10) % 10

    uic_number = "".join(base_digits) + str(checksum)

    # format
    formatted = (
        f"{uic_number[:2]} {uic_number[2:4]} {uic_number[4:5]} "
        f"{uic_number[5:8]} {uic_number[8:11]}-{uic_number[-1]}"
    )

    expected = "Die UIC-Wagennummer ist gültig.\n"
    actual = check50.run(f"python3 {FILE_NAME}").stdin(formatted).stdout()
    if not match(expected, actual):
        raise check50.Mismatch(expected, actual)
