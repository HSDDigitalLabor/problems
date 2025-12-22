import check50
import check50.py

FILE_NAME = "linkedMerge.py"


def to_list(ll):
    """LinkedList -> Python-Liste (mit Zyklus-Schutz)."""
    out = []
    if ll is None or ll.head is None:
        return out

    cur = ll.head
    seen = 0
    while cur is not None:
        out.append(cur.value)
        cur = cur.next
        seen += 1
        if seen > 10_000:
            msg = f"Linked list appears to have a cycle (more than {seen} nodes)"
            raise check50.Failure(msg)
    return out


def build_ll(module, values):
    """Erzeugt eine LinkedList über FromPythonlist (wie in der Aufgabe vorgegeben)."""
    ll = module.LinkedList()
    ll.FromPythonlist(values)
    return ll


@check50.check()
def exists():
    """linkedMerge.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """linkedMerge.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_classes_and_function():
    """ListNode, LinkedList and mergeTwoLists exist"""
    module = check50.py.import_(FILE_NAME)

    if not hasattr(module, "ListNode"):
        msg = f"Class `ListNode` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module, "LinkedList"):
        msg = f"Class `LinkedList` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module, "mergeTwoLists"):
        msg = f"Function `mergeTwoLists` not found in {FILE_NAME}"
        raise check50.Failure(msg)


@check50.check(has_classes_and_function)
def test_merge_two_sorted_lists():
    """mergeTwoLists merges two sorted lists correctly"""
    module = check50.py.import_(FILE_NAME)

    # List 1: 1 -> 2 -> 4 (Input [4, 2, 1] because FromPythonlist reverses)
    ll1 = build_ll(module, [4, 2, 1])
    # List 2: 1 -> 3 -> 4 (Input [4, 3, 1])
    ll2 = build_ll(module, [4, 3, 1])

    merged = module.mergeTwoLists(ll1, ll2)

    expected = [1, 1, 2, 3, 4, 4]
    actual = to_list(merged)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_function)
def test_merge_empty_lists():
    """mergeTwoLists handles two empty lists"""
    module = check50.py.import_(FILE_NAME)

    ll1 = module.LinkedList()
    ll2 = module.LinkedList()

    merged = module.mergeTwoLists(ll1, ll2)

    expected = []
    actual = to_list(merged)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_function)
def test_merge_one_empty_list():
    """mergeTwoLists handles one empty list"""
    module = check50.py.import_(FILE_NAME)

    ll1 = module.LinkedList()
    # List 2: 0 (Input [0])
    ll2 = build_ll(module, [0])

    merged = module.mergeTwoLists(ll1, ll2)

    expected = [0]
    actual = to_list(merged)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_function)
def test_merge_different_lengths():
    """mergeTwoLists merges lists of different lengths"""
    module = check50.py.import_(FILE_NAME)

    # List 1: 2 (Input [2])
    ll1 = build_ll(module, [2])
    # List 2: 1 -> 3 (Input [3, 1])
    ll2 = build_ll(module, [3, 1])

    merged = module.mergeTwoLists(ll1, ll2)

    expected = [1, 2, 3]
    actual = to_list(merged)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))
