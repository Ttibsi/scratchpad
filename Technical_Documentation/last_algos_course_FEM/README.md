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

