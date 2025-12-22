import check50
import check50.py

FILE_NAME = "linkedInsert.py"


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
    """linkedInsert.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """linkedInsert.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_classes_and_method():
    """ListNode, LinkedList and insertAfterLast exist"""
    module = check50.py.import_(FILE_NAME)

    if not hasattr(module, "ListNode"):
        msg = f"Class `ListNode` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module, "LinkedList"):
        msg = f"Class `LinkedList` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module.LinkedList(), "insertAfterLast"):
        msg = "Method `insertAfterLast` not found in Class `LinkedList`"
        raise check50.Failure(msg)


@check50.check(has_classes_and_method)
def test_insert_empty_list():
    """insertAfterLast inserts into empty list (becomes head)"""
    module = check50.py.import_(FILE_NAME)
    ll = module.LinkedList()

    new_node = module.ListNode(10)
    ll.insertAfterLast(new_node)

    expected = [10]
    actual = to_list(ll)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_method)
def test_insert_non_empty_list():
    """insertAfterLast appends to non-empty list"""
    module = check50.py.import_(FILE_NAME)
    # List: 30 -> 20 -> 10
    ll = build_ll(module, [10, 20, 30])

    new_node = module.ListNode(5)
    ll.insertAfterLast(new_node)

    expected = [30, 20, 10, 5]
    actual = to_list(ll)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))


@check50.check(has_classes_and_method)
def test_insert_multiple():
    """insertAfterLast appends multiple elements correctly"""
    module = check50.py.import_(FILE_NAME)
    ll = module.LinkedList()

    ll.insertAfterLast(module.ListNode(1))
    ll.insertAfterLast(module.ListNode(2))
    ll.insertAfterLast(module.ListNode(3))

    expected = [1, 2, 3]
    actual = to_list(ll)

    if actual != expected:
        raise check50.Mismatch(str(expected), str(actual))
