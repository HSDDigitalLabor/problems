"""helper functions which prints list diff better than CS50 Mismatch"""

import check50


def assert_list_equal(actual, expected):
    if actual != expected:
        msg = f"Expected: {expected}\nGot     : {actual}"
        raise check50.Failure(msg)


def assert_list_equal2(actual, expected, func_name="function_name"):
    if actual != expected:
        msg = (
            f"{func_name} returned the wrong list.\n"
            f"Expected: {expected}\n"
            f"Got     : {actual}"
        )
        raise check50.Failure(msg)
