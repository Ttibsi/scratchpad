# Last Algorithms Course You'll Ever Need
- ThePrimeagen + FrontEndMasters

Arrays are the most basic data structure.
This course uses typescript. My notes will use languages I'm more familiar with
as well as copying down some TS. Note the language being used

Recommended Books:
* Introduction to Algorithms (CSLR)
* Common-sense guide to Algorithms

### Big-O and the basics
Big-O categorises algorithms based on their time or memory input. It's helpful
to choose which data structure to use. 

Growth is respect to the size of the input.
One trick is to _look for the loops_ - it's the easiest way to work out 
your algorithm's speed - every time you go through the length of the data, it's
length `O(n)`

```go
// Running time: O(n)
for (int i := range n) {
    do_thing() 
}
```

Two loops consecutively is still O(n) because you drop the constants (which in
this case would be 2)

```go
// Running time: O(2n) because we're running through the length on the data
// twice, you drop the constants, so this becomes O(n)
for (int i := range n) {
    do_thing() 
}

for (int j := range n) {
    do_other_thing() 
}
```

On the other hand, if you have a nested loop, it would be O(n^2) because for
every element in the data, you're going through the whole data again

```go
// Running time: O(n^2)
for (int i := range n) {
    for (int j := range n) {
        do_thing() 
    }
}
```

Running times:
* O(1) - Constant time (the running time doesn't change based on the length of the data)
* O(logn)
* O(n) - linear time
* O(nlogn) - This is also a very common runtime
* O(n^2)

These both are so complex that they basically need a quantum computer to compute them
* O(2^n)
* O(n!)

This only ever comes up in one common algorithm.
* O(sqrt(n))

Array insertion and deletion are in constant time - O(n) - they take the 
start point, the array width in memory, the offset given for the index.
```
a + width + offset
```

This doesn't change no matter how big the array is, or how big the data is 
that you are inserting. 

Standard array data structures don't have an `insertAt()` method, they don't 
have pushing or popping. Doesn't mean you can't write algorithms for these
functions, and many languages have. 

Arrays will always have a set size that is defined at their point they're
created. (See the difference between a Go Array vs Slice) - this is also the 
point in C. 

### Searching
Linear search is the most basic searching algorithm. It's basically a for loop,
where you start at the beginning of the array and go through every element to 
check if it's the value you want. A linear search takes linear time

See file `1_linear_search.py`

Is your data sorted? If it is, this can give you many benefits that you can 
make use of for faster searching.

See file `2_binary_search.py`

Binary searching is in O(logn) because you are halving the size of your dataset
on each iteration.

`log` of a number is how many times you can half it. `log 4096` calculates like
this:

```
4096 -> 2048 -> 1024 -> 512 -> 256 -> 128 -> 64 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1
```

This is 12 steps, so `log 4096` == 12

If you halve your input, it's always O(log n) or O(n log n) depending on if you
still look at the rest of the data or not

### Two Crystal Balls
This is a common interview question:

```
// Given two crystal balls that will break if dropped from high enough
// distance, determine the exact spot in which it will break in the most
// optimized way.
```

This isn't just a binary search. The method for this is to jump halfway and if
the middle element is true (assuming we have a list of bools that tells us if
the ball smashes or not - we start on the middle floor) and from there, we 
go back to the start and jump sqrt(n) each time and test them.

See file `3_crystal_balls.py`

### Sorting
Bubble sort 
- this basically works by looking at each element, comparing it to the next 
element, and if it's bigger, swapping them.
- This means that any elem `i` is <= `i+1`. 
- After the first iteration, the last element will be the largest one in the array
which means, for each iteration, we only need to go as far as one less than 
the last iteration.

Big O drops insignificant values -> O(n^2 + n) just becomes O(n^2)
Bubble sort is O(n^2)

Binary search is harder than bubble sorting

See file `4_bubble_sort.py`

### Linked Lists
The big flaw in arrays is that they're a set length of memory, you can't easily
insert, delete, and it's ungrowable unless you reallocate memory.

Instead, we can use a Linked List, which instead uses nodes that point to 
the next element in the list, so they don't have to be contiguous in memory. 
A Singly Linked List only points to the next element, a double linked list also
points to the previous element as well.

Insertion and deletion are both in constant time because the position of the 
item in the list doesn't matter - you just need to update the next and prev
pointers on a few nodes. 

However, there's no easy way to find the `[x]` element, so you need to start from
the HEAD and look at every item until you find what you want, so searching is
in linear time.

### Queues
This is one implementation of a singly linked list using a FIFO approach.

Insertion is just adding a new node at the end of the queue and moving the TAIL
and is called `enqueue`
Deletion is popping from and moving the HEAD, and is called `deque`
Peeking is just looking at the value of what the HEAD is pointing to.

see file `5_queue.py`

### Stack
This is the opposite of a queue, a Last In First Out structure. 
It flips a queue around, with the HEAD at the end of the list and the TAIL at
the start.

see file `6_stack.py`

Linked lists use less memory than a static array but is always difficult or 
slow to search

### ArrayList
An array that we can grow by creating our own insert() and delete() methods.
This uses a separate capacity value as well as a length and you can work with
that to allow for insert and delete methods.

Python's Array and Go's Slice are examples of ArrayList data structures

Queues are better for node-based data structures such as a Linked List, as 
the methods on the data structure work from the start of the queue (as it's FIFO).
If you use an Array-based data structure, an enqueue() will involve moving 
every element along one just to insert at the start, which is an O(n) operation.

### Ring Buffers/ Array Buffers
These are a type of array that use index-based head and tails, meaning that
the length and capacity of the array are different values. Anything outside of
the head and tail are all set to null. If you need to deque(), for example, you
can just move the head forward and clear up the floating value. This makes for
a really elegant looping form of datastructure.

If your tail exceeds your capacity, you can move it back to the start of the 
array, and use modulo to work out where it should be in the actual array.

Example:

[  x   x]
0  H   TN

If you move the tail forward one element, it'll overflow the array. Instead,
you want to use `this.tail % len` (typescript) to move the tail to the start
and keep track of it's value

[x  x   ]
0T  H   N


### Recursion
A function that calls itself until a problem is solved, often using a base case
to detect if the problem is solved to break out of the recursion.

Always start with the base case, work out what you need first. 

Recursion is usually broken up into 3 stages, the pre, the recurse, and the post.
Often, you will use those for things like managing state.

see file `7_recursion.py`

### Quick Sort

This uses a method called Divide and Conquer - where you split the data in half
at each iteration of the algorithm and weakly sort each half, and then split it
again to check again etc. In this case, you're only making sure that the 
left-most element is the lowest on each iteration.
    - Merge sort is another example of this type of algorithm.

In Quick sort, we take a point anywhere in our array and make it our Pivot. We
take a pointer at the start of the array and go through until we reach the 
pivot, and if the element is lower than the pivot, it moves to the start of
the array. We then do the same at the upper half of the array. 

After the first iteration, every element to the left is lower, and every element
to the right is higher, but we haven't fully sorted the array yet. We want to 
repeat this process on each half.

Step 1:
[     p     ]
0           N

Step 2:
[  p  ][  p  ]
0            N

etc

In general, this is O(n log n), but if the array is fully reverse sorted already
(ex [10, 9, 8, ... 1]), then this can be O(n^2), so the running time of this
algorithm can vary.

see file `8_quick_sort.py`

