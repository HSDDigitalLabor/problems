"""
use check50.hidden() to hide "running ./linkedListTest X..."
where X is the test_case while running check50
the docstring from the function will show regardless
"""

import re
from pathlib import Path

import check50
import check50.c

FILE_NAME = "queue.c"
TEST_FILE = "testing.c"

COMBINED_FILE_NAME = "queueTest.c"
COMPILED_PGRM = "./queueTest"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)
    check50.include(TEST_FILE)


@check50.hidden("")
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


def run_test_case(test_case: int):
    cmd = f"{COMPILED_PGRM} {test_case}"
    return check50.run(cmd).exit()


@check50.hidden("")
@check50.check(compiles)
def empty_queue():
    """Test case 0: Create an empty queue using createQueue()"""
    run_test_case(0)


@check50.hidden("")
@check50.check(compiles)
def create_node():
    """Test case 1: Create Node using create()"""
    run_test_case(1)


@check50.hidden("")
@check50.check(compiles)
def enqueue_one_element():
    """Test case 2: Enqueue one element"""
    run_test_case(2)


@check50.hidden("")
@check50.check(compiles)
def enqueue_multiple():
    """Test case 3: Enqueue multiple elements"""
    run_test_case(3)


@check50.hidden("")
@check50.check(compiles)
def peek_on_two():
    """Test case 4: Enqueue two elements, peek must return the value of the first"""
    run_test_case(4)


@check50.hidden("")
@check50.check(compiles)
def peek_is_idempotent():
    """Test case 5: Enqueue two elements, peek must not remove elements"""
    run_test_case(5)


@check50.hidden("")
@check50.check(compiles)
def dequeue_element():
    """Test case 6: Enqueue one, dequeue one, list should be empty"""
    run_test_case(6)


@check50.hidden("")
@check50.check(compiles)
def dequeue_multiple():
    """Test case 7: Enqueue multiple, dequeue multiple, check for FIFO order"""
    run_test_case(7)


@check50.hidden("")
@check50.check(compiles)
def dequeue_multiple_order():
    """Test case 8: Enqueue multiple and dequeue all,
    check correct order, head and tail pointer updated"""
    run_test_case(8)


@check50.hidden("")
@check50.check(compiles)
def dequeue_on_empty_queue():
    """Test case 9: Enqueue, dequeue and check if enqueue works after"""
    run_test_case(9)


@check50.hidden("")
@check50.check(compiles)
def length_of_empty_queue():
    """Test case 10: Check length of empty queue is zero"""
    run_test_case(10)


@check50.hidden("")
@check50.check(compiles)
def dequeue_on_empty_queue_2():
    """Test case 11: Attempt dequeue on empty queue"""
    run_test_case(11)


@check50.hidden("")
@check50.check(compiles)
def peek_on_empty_queue():
    """Test case 12: Peek on empty queue"""
    run_test_case(12)


@check50.hidden("")
@check50.check(compiles)
def null_arguments():
    """Test case 13: Call enqueue(), dequeue(), peek(), length() with NULL as arg"""
    run_test_case(13)


@check50.hidden("")
@check50.check(compiles)
def destory_empty_queue():
    """Test case 14: Call destroy() on empty queue"""
    run_test_case(14)


@check50.hidden("")
@check50.check(compiles)
def destroy_populated_queue():
    """Test case 15: Call destroy() on populated queue"""
    run_test_case(15)


@check50.hidden("")
@check50.check(compiles)
def free_memory():
    """Running every test case again and checking if memory gets freed"""

    # run valgrind manually here
    # using check50.c.valgrind causes an uncatchable error as check50 is unable to parse
    # the .xml file valgrind produces
    for i in range(0, 15):
        cmd = f"{COMPILED_PGRM} {i}"
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
