import check50
import check50.py

FILE_NAME = "linkedRemove.py"


def to_list(ll):
    """LinkedList -> Python-Liste (mit Zyklus-Schutz)."""
    out = []
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
    """linkedRemove.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """linkedRemove.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_classes_and_method():
    """ListNode, LinkedList and removeElement exist"""
    module = check50.py.import_(FILE_NAME)

    if not hasattr(module, "ListNode"):
        msg = f"Class `ListNode` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module, "LinkedList"):
        msg = f"Class `LinkedList` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module.LinkedList(), "removeElement"):
        msg = "Method `removeElement` not found in Class `LinkedList`"
        raise check50.Failure(msg)


@check50.check(has_classes_and_method)
def test_remove_middle():
    """removeElement removes a middle node"""
    module = check50.py.import_(FILE_NAME)
    # List: 30 -> 20 -> 10
    ll = build_ll(module, [10, 20, 30])

    # Find node with value 20
    node_to_remove = ll.searchValue(20)
    if node_to_remove is None:
        msg = ("searchValue(20) returned None, but 20 should be in the list. "
               "Cannot test removeElement.")
        raise check50.Failure(msg)

    ll.removeElement(node_to_remove)

    expected = [30, 10]
    actual = to_list(ll)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_method)
def test_remove_head():
    """removeElement removes the head node"""
    module = check50.py.import_(FILE_NAME)
    # List: 30 -> 20 -> 10
    ll = build_ll(module, [10, 20, 30])

    # Find node with value 30 (head)
    node_to_remove = ll.searchValue(30)
    if node_to_remove is None:
        msg = ("searchValue(30) returned None, but 30 should be in the list. "
               "Cannot test removeElement.")
        raise check50.Failure(msg)

    ll.removeElement(node_to_remove)

    expected = [20, 10]
    actual = to_list(ll)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_method)
def test_remove_tail():
    """removeElement removes the tail node"""
    module = check50.py.import_(FILE_NAME)
    # List: 30 -> 20 -> 10
    ll = build_ll(module, [10, 20, 30])

    # Find node with value 10 (tail)
    node_to_remove = ll.searchValue(10)
    if node_to_remove is None:
        msg = ("searchValue(10) returned None, but 10 should be in the list. "
               "Cannot test removeElement.")
        raise check50.Failure(msg)

    ll.removeElement(node_to_remove)

    expected = [30, 20]
    actual = to_list(ll)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_method)
def test_remove_single_element():
    """removeElement removes the only element in the list"""
    module = check50.py.import_(FILE_NAME)
    # List: 10
    ll = build_ll(module, [10])

    node_to_remove = ll.searchValue(10)
    if node_to_remove is None:
        msg = (
            "searchValue(10) returned None, but 10 should be in the list. "
            "Cannot test removeElement."
        )
        raise check50.Failure(msg)

    ll.removeElement(node_to_remove)

    expected = []
    actual = to_list(ll)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))
