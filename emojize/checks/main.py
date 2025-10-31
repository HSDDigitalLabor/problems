import io
import re
import tokenize
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
def no_str_replace():
    """solution must not use str.replace()"""
    source = Path(FILE_NAME).read_text()
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    for token_type, token_string, *_ in tokens:
        # only check actual code (not comments, not strings)
        if token_type == tokenize.NAME and token_string == "replace":
            msg = "The use of str.replace() is not allowed."
            raise check50.Failure(msg)


@check50.check(uses_package)
def uses_emoji_emojize():
    """solution must call emoji.emojize()"""
    source = Path(FILE_NAME).read_text()

    # remove comments before checking
    io_obj = io.StringIO(source)
    tokens = tokenize.generate_tokens(io_obj.readline)
    code_no_comments = "".join(
        tokval for toktype, tokval, *_ in tokens if toktype != tokenize.COMMENT
    )

    if "emoji.emojize(" not in code_no_comments.replace(" ", ""):
        msg = "Your solution must call emoji.emojize()."
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
