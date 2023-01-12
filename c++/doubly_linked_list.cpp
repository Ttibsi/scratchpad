#include <iostream>

/*
 * Implementation of a doubly linked list to understand how pointers work with
 * practical experience. Implementation predominantly based off the ada code
 * on the wikipedia page here: https://en.wikipedia.org/wiki/Doubly_linked_list
*/

struct Node {
    int val;
    Node* prev;
    Node* next;
};

struct List {
    Node* head;
    Node* tail;
};

int get_next(Node* n) {
    return n->next->val;
}

int get_prev(Node* n) {
    return n->prev->val;
}

void print_forward(Node* head) {
    Node* player = head;
    while (player != nullptr) {
        std::cout << player->val;
        player = player->next;
    }
    std::cout << "\n";
}

void print_backward(Node* tail) {
    Node* player = tail;
    while (player != nullptr) {
        std::cout << player->val;
        player = player->prev;
    }
    std::cout << "\n";
}

void insert_before(Node* n, Node* head, int c) {
    Node* new_node = new Node();
    new_node->val = c; 
    new_node->next = n;

    if (n->prev == nullptr) {
        new_node->prev = nullptr;
        head = new_node;
    } else { 
        new_node->prev = n->prev;
        n->prev->next = new_node;
    }
    n->prev = new_node;
}

void insert_after(Node* n, Node* head, int c) {
    Node* new_node = new Node();
    new_node->val = c; 
    new_node->prev = n;

    if (n->next == nullptr) {
        new_node->next = nullptr;
        head = new_node;
    } else {
        new_node->next = n->next;
        n->next->prev = new_node;
    }
    n->next = new_node;
}

void remove(Node* n, Node* head, Node* tail) {
    if (n->prev == nullptr) {
        head = n-> next;
    } else {
        n->prev->next = n->next;
    }

    if (n->next == nullptr) {
        tail = n-> prev;
    } else {
        n->next->prev = n->prev;
    }
}

int main() {
    List* lst = new List();
    lst->head = nullptr;
    lst->tail = nullptr;

    for (int i = 1; i < 10; i++) {
        // Create node
        Node* n = new Node();
        n->val = i;
        n->next = nullptr;
        n->prev = lst->tail;

        if (i == 1) { lst->head = n; } else { lst->tail->next = n; }
        lst->tail = n;
    }

    std::cout << "All entries (forward, then backward)\n";
    print_forward(lst->head);
    print_backward(lst->tail);

    std::cout << "\nget next and previous\n";
    std::cout << get_next(lst->head) << "\n";
    std::cout << get_prev(lst->tail) << "\n";

    std::cout << "\nInsert before\n";
    insert_before(lst->head->next->next, lst->head, 0);
    print_forward(lst->head);

    std::cout << "\nInsert after\n";
    insert_before(lst->head->next->next, lst->head, 0);
    print_forward(lst->head);

    std::cout << "\nRemove node\n";
    // We only need one function because we can use `n->next` or `n->prev` to
    // specify
    remove(lst->tail->prev->prev, lst->head, lst->tail);
    print_forward(lst->head);
}

