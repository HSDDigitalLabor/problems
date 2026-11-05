import random
import string
from pathlib import Path

import check50
import check50.py
from luhncheck import is_luhn

FILE_NAME = "hackers.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """hackers.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(exists)
def has_function():
    """function checkFile is defined"""
    module = check50.py.import_(FILE_NAME)
    if not hasattr(module, "checkFile"):
        msg = f"Function `checkFile` not found in {FILE_NAME}"
        raise check50.Failure(msg)


def run_submission(filepath: str, expected: int):
    module = check50.py.import_(FILE_NAME)

    try:
        result = module.checkFile(filepath)
    except Exception as e:
        raise check50.Failure(
            rationale="Your solution raised the following exception: "
            f"{type(e).__name__}"
        ) from e

    if type(result) is not int or result < 0:
        msg = "Your function must return a positive int"
        raise check50.Failure(msg)

    if result != expected:
        raise check50.Mismatch(str(expected), str(result))


@check50.check(has_function)
def testFile1():
    """check output of file with in file: small.txt"""
    filename = "small.txt"
    check50.include(f"files/{filename}")

    run_submission(filename, 2)


@check50.check(has_function)
def testFile2():
    """check output of file with in file: spaces.txt"""
    filename = "spaces.txt"

    check50.include(f"files/{filename}")

    run_submission(filename, 1)


@check50.check(has_function)
def testFile3():
    """check output of file with in file: medium.txt"""
    filename = "medium.txt"

    check50.include(f"files/{filename}")

    run_submission(filename, 46)


@check50.check(has_function)
def testFile4():
    """check output of file with in file: large.txt"""
    filename = "large.txt"

    check50.include(f"files/{filename}")

    run_submission(filename, 4776)


# ---------------------------------------------------------------------------
# Random file: generated fresh on every run, so answers can't be hard coded
# ---------------------------------------------------------------------------


def is_invalid(line: str) -> bool:
    """rule: invalid if not 12-19 digits (spaces ignored) or fails Luhn."""
    cc = line.replace(" ", "").strip()
    return not (12 <= len(cc) <= 19 and is_luhn(cc))


def random_digits(rng: random.Random, n: int) -> str:
    return "".join(rng.choice(string.digits) for _ in range(n))


def luhn_valid_number(rng: random.Random, length: int) -> str:
    """Random number of `length` digits that passes Luhn."""
    body = random_digits(rng, length - 1)
    for d in string.digits:
        if is_luhn(body + d):
            return body + d


def random_line(rng: random.Random) -> str:
    kind = rng.choices(
        ["valid", "bad_checksum", "too_short", "too_long", "boundary"],
        weights=[40, 30, 10, 10, 10],
    )[0]

    if kind == "valid":
        n = luhn_valid_number(rng, rng.randint(12, 19))
    elif kind == "bad_checksum":
        n = luhn_valid_number(rng, rng.randint(12, 19))
        n = n[:-1] + str((int(n[-1]) + rng.randint(1, 9)) % 10)
    elif kind == "too_short":
        # Luhn-valid on purpose: only the length check can catch it
        n = luhn_valid_number(rng, rng.randint(2, 11))
    elif kind == "too_long":
        n = luhn_valid_number(rng, rng.randint(20, 25))
    else:
        # right at the edges of the allowed range, all Luhn-valid
        n = luhn_valid_number(rng, rng.choice([11, 12, 19, 20]))

    # Sometimes write it in groups of four, like on a real card
    if rng.random() < 0.3:
        n = " ".join(n[i : i + 4] for i in range(0, len(n), 4))
    return n


@check50.check(has_function)
def testRandomFile():
    """check output of a randomly generated file"""
    seed = random.SystemRandom().randrange(10**9)
    rng = random.Random(seed)

    # Make sure the answer differs from every known list's answer
    while True:
        lines = [random_line(rng) for _ in range(rng.randint(150, 400))]
        expected = sum(is_invalid(line) for line in lines)
        if expected not in (0, 1, 2, 46, 4776):
            break

    # Random filename too, so solutions can't branch on the name
    filename = f"list_{seed}.txt"
    with Path.open(filename, "w") as f:
        f.write("\n".join(lines) + "\n")

    check50.log(f"generated {filename} with {len(lines)} lines (seed {seed})")
    run_submission(filename, expected)
