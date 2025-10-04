from pathlib import Path

import check50

FILE_NAME = "emojize.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def uses_package():
    """solution must use emoji package"""
    with Path.open(FILE_NAME) as f:
        source = f.read()
        if "import emoji" not in source and "from emoji" not in source:
            msg = "The emoji package must be used."
            raise check50.Failure(msg)


@check50.check(uses_package)
def testOnVideoExample():
    """testing using the example in the video"""

    user_input = ":thumbs_up:"
    expected = "👍"
    actual = check50.run(f"python3 {FILE_NAME}").stdin(user_input).stdout()
    if expected not in actual:
        raise check50.Mismatch(expected, actual)


@check50.check(uses_package)
def testOnExample1():
    """testing using the first example"""

    user_input = "Der schnellste erhält die :1st_place_medal:"
    expected = "Der schnellste erhält die 🥇"
    actual = check50.run(f"python3 {FILE_NAME}").stdin(user_input).stdout()
    if expected not in actual:
        raise check50.Mismatch(expected, actual)


@check50.check(uses_package)
def testOnExample2():
    """testing using the second example"""

    user_input = ":money_bag:"
    expected = "💰"
    actual = check50.run(f"python3 {FILE_NAME}").stdin(user_input).stdout()
    if expected not in actual:
        raise check50.Mismatch(expected, actual)


@check50.check(uses_package)
def testOnExample3():
    """testing using the third example"""

    user_input = (
        "Miezel, eine schlaue :smile_cat:, Molly, ein begabter :dog_face:, "
        "Wohnhaft an demselben Platze, Haßten sich aus Herzensgrund."
    )
    expected = (
        "Miezel, eine schlaue 😸, Molly, ein begabter 🐶, "
        "Wohnhaft an demselben Platze, Haßten sich aus Herzensgrund."
    )
    actual = check50.run(f"python3 {FILE_NAME}").stdin(user_input).stdout()
    if expected not in actual:
        raise check50.Mismatch(expected, actual)
