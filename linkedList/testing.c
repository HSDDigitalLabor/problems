#include <stdlib.h>

#ifndef LINKED_LIST_TYPES_DEFINED
#define LINKED_LIST_TYPES_DEFINED

typedef struct Node {
  int value;
  struct Node *next;
} Node;

typedef struct List {
  Node *head;
} List;

List *createList(void);
Node *create(int value);
List *insert(List *list, int value);
Node *search(List *list, int value);
int removeNode(List *list, Node *element);
int length(List *list);
Node *get(List *list, int index);
void destroy(List *list);

#endif

enum TestResult { TEST_PASS = 0, TEST_FAIL = 1 };

int main(int argc, char *argv[]) {
  if (argc != 2) {
    return TEST_FAIL;
  }

  int test_case = atoi(argv[1]);

  switch (test_case) {

  // 0: Empty list has head == NULL
  case 0: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    int result = (list->head == NULL) ? TEST_PASS : TEST_FAIL;

    destroy(list);
    return result;
  }

  // 1: Insert one element
  case 1: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    list = insert(list, 5);

    int result = (list != NULL && length(list) == 1 && list->head != NULL &&
                  list->head->value == 5 && list->head->next == NULL)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(list);
    return result;
  }

  // 2: Insert multiple elements
  case 2: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    list = insert(list, 5);
    list = insert(list, 10);
    list = insert(list, 15);

    int result = (list != NULL && length(list) == 3) ? TEST_PASS : TEST_FAIL;

    destroy(list);
    return result;
  }

  // 3: Search for an existing value
  case 3: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    list = insert(list, 5);
    list = insert(list, 10);

    Node *element = search(list, 10);

    int result =
        (element != NULL && element->value == 10) ? TEST_PASS : TEST_FAIL;

    destroy(list);
    return result;
  }

  // 4: Search for a nonexistent value
  case 4: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    list = insert(list, 5);

    int result = (search(list, 99) == NULL) ? TEST_PASS : TEST_FAIL;

    destroy(list);
    return result;
  }

  // 5: Remove the head
  case 5: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    list = insert(list, 5);
    list = insert(list, 10);

    Node *element = get(list, 0);
    int removed = removeNode(list, element);

    int result = (removed == 5 && length(list) == 1 && list->head->value == 10)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(list);
    return result;
  }

  // 6: Remove a middle element
  case 6: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    list = insert(list, 5);
    list = insert(list, 10);
    list = insert(list, 15);

    Node *element = get(list, 1);
    int removed = removeNode(list, element);

    int result = (removed == 10 && length(list) == 2 &&
                  get(list, 0)->value == 5 && get(list, 1)->value == 15)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(list);
    return result;
  }

  // 7: Remove the last element
  case 7: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    list = insert(list, 5);
    list = insert(list, 10);

    Node *element = get(list, 1);
    int removed = removeNode(list, element);

    int result =
        (removed == 10 && length(list) == 1 && list->head->next == NULL)
            ? TEST_PASS
            : TEST_FAIL;

    destroy(list);
    return result;
  }

  // 8: Get element at a valid index
  case 8: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    list = insert(list, 5);
    list = insert(list, 10);
    list = insert(list, 15);

    Node *element = get(list, 1);

    int result =
        (element != NULL && element->value == 10) ? TEST_PASS : TEST_FAIL;

    destroy(list);
    return result;
  }

  // 9: Get element at an invalid index
  case 9: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    list = insert(list, 5);

    int result =
        (get(list, 5) == NULL && get(list, -1) == NULL) ? TEST_PASS : TEST_FAIL;

    destroy(list);
    return result;
  }

  // 10: Remove nonexistent element
  case 10: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    list = insert(list, 5);

    Node *element = create(99);

    if (element == NULL) {
      destroy(list);
      return TEST_FAIL;
    }

    int removed = removeNode(list, element);

    int result = (removed == -1 && length(list) == 1) ? TEST_PASS : TEST_FAIL;

    free(element);
    destroy(list);
    return result;
  }

  // 11: Destroy an empty list
  case 11: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    destroy(list);
    return TEST_PASS;
  }

  // 12: Destroy a populated list
  case 12: {
    List *list = createList();

    if (list == NULL) {
      return TEST_FAIL;
    }

    list = insert(list, 5);
    list = insert(list, 10);
    list = insert(list, 15);

    destroy(list);
    return TEST_PASS;
  }

  // 13: Handle NULL list arguments
  case 13: {
    int result =
        (length(NULL) == 0 && search(NULL, 5) == NULL && get(NULL, 0) == NULL &&
         removeNode(NULL, NULL) == -1 && insert(NULL, 5) == NULL)
            ? TEST_PASS
            : TEST_FAIL;

    return result;
  }

  default:
    return TEST_FAIL;
  }
}