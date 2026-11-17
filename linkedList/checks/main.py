"""
use check50.hidden() to hide "running ./linkedListTest X..."
where X is the test_case while running check50
the docstring from the function will show regardless
"""

import re
from pathlib import Path

import check50
import check50.c

FILE_NAME = "linkedList.c"
TEST_FILE = "testing.c"

COMBINED_FILE_NAME = "linkedListTest.c"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)
    check50.include(TEST_FILE)


@check50.check(exists)
def compiles():
    """file compiles"""
    check50.c.compile(FILE_NAME)

    student_solution = re.sub(
        r"int\s+main\s*\(", "int distro_main(", Path(FILE_NAME).read_text()
    )

    testing = Path(TEST_FILE).read_text()

    with Path(COMBINED_FILE_NAME).open("w") as f:
        f.write(student_solution)
        f.write("\n")
        f.write(testing)

    check50.c.compile(COMBINED_FILE_NAME)


def run_test_case(test_case: int, valgrind: bool = False):
    cmd = f"./linkedListTest {test_case}"
    return check50.run(cmd).exit()


@check50.hidden("")
@check50.check(compiles)
def empty_list():
    """Empty list should initialize head to NULL"""
    run_test_case(0)


@check50.hidden("")
@check50.check(compiles)
def insert_one():
    """Insert one element"""
    run_test_case(1)


@check50.hidden("")
@check50.check(compiles)
def insert_multiple():
    """Insert multiple elements"""
    run_test_case(2)


@check50.hidden("")
@check50.check(compiles)
def search_existing():
    """Search should find an existing element"""
    run_test_case(3)


@check50.hidden("")
@check50.check(compiles)
def search_missing():
    """Search should return NULL for missing element"""
    run_test_case(4)


@check50.hidden("")
@check50.check(compiles)
def remove_head():
    """Remove the head element"""
    run_test_case(5)


@check50.hidden("")
@check50.check(compiles)
def remove_middle():
    """Remove a middle element"""
    run_test_case(6)


@check50.hidden("")
@check50.check(compiles)
def remove_last():
    """Remove the last element"""
    run_test_case(7)


@check50.hidden("")
@check50.check(compiles)
def get_valid():
    """Get element at valid index"""
    run_test_case(8)


@check50.hidden("")
@check50.check(compiles)
def get_invalid():
    """Get element at invalid index"""
    run_test_case(9)


@check50.hidden("")
@check50.check(compiles)
def remove_missing():
    """Removing nonexistent element should fail"""
    run_test_case(10)


@check50.hidden("")
@check50.check(compiles)
def destroy_empty():
    """Destroy empty list"""
    run_test_case(11)


@check50.hidden("")
@check50.check(compiles)
def destroy_populated():
    """Creating a list, inserting elements and calling destroy()"""
    run_test_case(12)


@check50.hidden("")
@check50.check(compiles)
def null_arguments():
    """Functions should handle NULL arguments"""
    run_test_case(13)


@check50.hidden("")
@check50.check(compiles)
def free_memory():
    """Running every test case again and checking if memory gets freed"""

    # run valgrind manually here
    # using check50.c.valgrind causes an uncatchable error as check50 is unable to parse
    # the .xml file valgrind produces
    for i in range(0, 13):
        cmd = f"./linkedListTest {i}"
        valgrind_cmd = (
            f"valgrind --leak-check=full "
            f"--show-leak-kinds=all "
            f"--errors-for-leak-kinds=definite "
            f"--error-exitcode=1 {cmd}"
        )
        result = check50.run(valgrind_cmd).exit()
        # result = check50.c.valgrind(cmd).exit()
        if result != 0:
            msg = f"Test case {i} failed"
            help = "Check you are freeing memory correctly"
            raise check50.Failure(msg, help)
