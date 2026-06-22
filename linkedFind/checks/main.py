import check50
import check50.py

FILE_NAME = "linkedFind.py"


def build_ll(module, values):
    """Erzeugt eine LinkedList über FromPythonlist (wie in der Aufgabe vorgegeben)."""
    ll = module.LinkedList()
    ll.FromPythonlist(values)
    return ll


@check50.check()
def exists():
    """linkedFind.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """linkedFind.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_classes_and_method():
    """ListNode, LinkedList and searchValue exist"""
    module = check50.py.import_(FILE_NAME)

    if not hasattr(module, "ListNode"):
        msg = f"Class `ListNode` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module, "LinkedList"):
        msg = f"Class `LinkedList` not found in {FILE_NAME}"
        raise check50.Failure(msg)

    if not hasattr(module.LinkedList(), "searchValue"):
        msg = "Method `searchValue` not found in Class `LinkedList`"
        raise check50.Failure(msg)


@check50.check(has_classes_and_method)
def test_search_found_head():
    """searchValue finds the head element"""
    module = check50.py.import_(FILE_NAME)
    # List: 30 -> 20 -> 10 (FromPythonlist inserts at head)
    ll = build_ll(module, [10, 20, 30])

    found = ll.searchValue(30)

    if found is None:
        msg = "searchValue returned None for an existing value (head)"
        raise check50.Failure(msg)

    if not isinstance(found, module.ListNode):
        msg = "searchValue must return a ListNode object"
        raise check50.Failure(msg)

    if found.value != 30:
        msg = f"Node with value 30, Node with value {found.value}"
        raise check50.Mismatch(msg)


@check50.check(has_classes_and_method)
def test_search_found_middle():
    """searchValue finds a middle element"""
    module = check50.py.import_(FILE_NAME)
    # List: 30 -> 20 -> 10
    ll = build_ll(module, [10, 20, 30])

    found = ll.searchValue(20)

    if found is None:
        msg = "searchValue returned None for an existing value (middle)"
        raise check50.Failure(msg)

    if found.value != 20:
        msg = "Node with value 20", f"Node with value {found.value}"
        raise check50.Mismatch(msg)


@check50.check(has_classes_and_method)
def test_search_found_tail():
    """searchValue finds the tail element"""
    module = check50.py.import_(FILE_NAME)
    # List: 30 -> 20 -> 10
    ll = build_ll(module, [10, 20, 30])

    found = ll.searchValue(10)

    if found is None:
        msg = "searchValue returned None for an existing value (tail)"
        raise check50.Failure(msg)

    if found.value != 10:
        msg = "Node with value 10", f"Node with value {found.value}"
        raise check50.Mismatch(msg)


@check50.check(has_classes_and_method)
def test_search_not_found():
    """searchValue returns None for non-existing value"""
    module = check50.py.import_(FILE_NAME)
    # List: 30 -> 20 -> 10
    ll = build_ll(module, [10, 20, 30])

    found = ll.searchValue(99)

    if found is not None:
        msg = (
            f"searchValue should return None for non-existing value,"
            f"but returned Node with value {found.value}"
        )
        raise check50.Failure(msg)


@check50.check(has_classes_and_method)
def test_search_empty_list():
    """searchValue returns None on empty list"""
    module = check50.py.import_(FILE_NAME)
    ll = module.LinkedList()

    found = ll.searchValue(10)

    if found is not None:
        msg = (
            f"searchValue should return None on empty list, "
            f"but returned Node with value {found.value}"
        )
        raise check50.Failure(msg)
