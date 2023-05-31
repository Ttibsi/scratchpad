// Double linked list implemented in Golang
// For this example, I thought it was easier to implement in Go than in python
// This was previously implemented at another time in C++ at:
// scratchpad/c++/doubly_linked_list.cpp
package main

import "fmt"

type Node struct {
	value int
	prev *Node
	next *Node
}

type DoubleLinkedList struct {
	length int
	head *Node
	tail *Node
}

//constructor
func new() DoubleLinkedList {
	return DoubleLinkedList{length: 0}
}

func (d *DoubleLinkedList) prepend(item int) {
	node := Node{value: item}

	d.length += 1
	if d.head == nil {
		d.head = &node
		d.tail = &node
		return
	}

	node.next = d.head
	d.head.prev = &node
	d.head = &node
}

func (d *DoubleLinkedList) insertAt(item int, idx int) {
	if idx > d.length {
		// Raise error 
		fmt.Println("Error")
	} else if idx == d.length {
		d.append(item)
	} else if idx == 0 {
		d.prepend(item)
	}

	d.length += 1
	curr := d.getAt(idx)

	node := Node{value: item}
	node.next = curr
	node.prev = curr.prev
	curr.prev = &node

	if node.prev != nil {
		node.prev.next = curr
	}
	
}

func (d *DoubleLinkedList) append(item int) {
	d.length += 1
	node := Node{value: item}

	if d.tail == nil {
		d.head = &node
		d.tail = &node
		return
	}

	node.prev = d.tail
	d.tail.next = &node
	d.tail = &node
}

func (d *DoubleLinkedList) remove(item int) int {
	curr := d.head
	for i := 0; curr != nil && i < d.length; i++ {
		if curr.value == item {
			break
		}
		curr = curr.next
	}

	if curr == nil { return -1 }

	d.length =- 1

	if d.length == 0 {
		out := d.head.value
		d.head = nil
		d.tail = nil
		return out
	}

	if curr.prev != nil { curr.prev.next = curr.next }
	if curr.next != nil { curr.next.prev = curr.prev }
	if curr == d.head { d.head = curr.next }
	if curr == d.tail { d.tail = curr.prev }
	curr.prev = nil
	curr.next = nil
	return curr.value
}

func (d *DoubleLinkedList) get(idx int) int {
	return d.getAt(idx).value
}

func (d *DoubleLinkedList) removeAt(idx int) int {
	node := d.getAt(idx)
	if node == nil { return -1}
	return node.value
}

func (d *DoubleLinkedList) getAt(idx int) *Node {
	curr := d.head
	for i := 0; curr != nil && i < idx; i++ {
		curr = curr.next
	}

	return curr
}

