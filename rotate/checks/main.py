from re import match

import check50

FILE_NAME = "rotate.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)



