# Python List - Array underhood

### Is a list truly dynamic? 
NO! It's an array that resizes by reallocating.

```Growth Formula of a list: new_capacity = old_capacity + (old_capacity >> 3) + 6```

```(old_capacity >> 3)``` means ```old_capacity/8``` which is ```12.5%```

### what is the default capacity of a list?

If you initialize an empty list:

```arr = []```

- The capacity allocated to your array is 0
- No backing array allocated yet
- When you first append an element, that then triggers allocation or rather I should say pre-allocation.

### what is lazy allocation?

Resource is allocated as late as possible. But why lazy?
- It decreases the statup time
- It eliminates the allocated if not used

But we can also pre-allocate a resource which might be needed in future to make execution efficient at the cost of startup speed, avoids the possibility of later allocation failure - in general about resources not only for lists memory.

### When you append 1 element -> CPython allocates space for 4 elements

**why 4 and not 6?**

- Pre-allocates exactly or slightly above needed size
- No growth formula used yet
    +6 constant is not yet used, 1st append is handled separately
    - hardcoded minimum growth floor
    - small enough to not waste memory + large enough to amortize first few appends
    why not 6?
    - overkill, unnecessary memory overhead



if lists are just arrays then how are lists able to store multiple data types?
they store pointers inside them not actual elements themselves. They are called referential arrays 

int array[50]

[1,2,3,4]

- these pointers point to PyObject structures
- CPython List:
    typedef struct {
        PyObject_Var_Head
        PyObject **ob_item;  # Pointer to array of pointers
        Py_ssize_t allocated;  # capacity
    } PyListObject;

list object ->ob_item -> [ptr][ptr][ptr][ptr]

    - now these pointers may have different types like one is int, other is string, another is bool,
    - so in array slots we actually store memory addresses not binary, unlike traditional arrays
    - so you must follow a pointer to reach to the real data, unlike traditional arrays that directly give you a value
    list -> pointer -> object -> value      # this is an extra indirection we have to go through
    - hence slower

what is memory footprint? = total RAM used

Memory footprint of normal 1 integer array = 4 bytes
and that of 1 integer python list = ~92 bytes

why?
when you have 1 element in python list, it actually is a pointer array
    which means -> 8 bytes (for each pointer) x 4(slots or capacity) (sometimes python pre-allocates memory for 4, this is pointer buffer)
    the object itself -> 56 bytes (overhead) why? => container metadata (capacity, ref count, etc) memory

    - the pointer points to a location where actual int is stored ->  28 bytes (which in actually a PyLongObject and is not addeed in calculation of sys.getsizeof() btw)

```
>>> import sys
>>> sys.getsizeof([]) # memory footprint 56, capacity =0
56
>>> sys.getsizeof([2]) # memory footprint 64, capacity=1 # if you append then only it'll change capacity to 4, in this one if you add the PyLongObject memory footprint then you'll get 92 bytes
64
>>> a=[]
>>> sys.getsizeof(a)  # memory footprint 56, capacity = 0
56
>>> a.append(7)
>>> sys.getsizeof(a) # memory footprint 56, capacity = 4 {88-56 = 32, 32/8(bytes req for one pointer) = 4, you get your capacity see} - this is bootstrap allocation
88
>>> a.append(7)
>>> sys.getsizeof(a) # capacity is unchanged since python will follow lazy allocation here, space is empty
88
>>> b = [2]
>>> sys.getsizeof(b) # initiated with c=1 and memory footprint 64 since -> this is a literal (a constant value directly given in code) # python knows its exact final size =1 so it allocates the same hence c = 1 hence pointer buffer also 1 x 8 bytes = 8 => 56 + 8 = 64
64
>>> b.append(7)
>>> sys.getsizeof(b) # capacity before append was 1 and for the 2nd element we use growth formula
120
# new capacity = old capacity + (old capacity//8) + 6 = 1 + 0 + 6 = 7

# 7 slots x 8 = 56 pointer buffer, hence -> 56 + 56 = 112 (list + pointer buffer)  

# since python's memory allocator (pymalloc) uses memory classes it rounded up 56 to 64 hence 56 + 64 = 120 instead of 112
```

BUT

- removing element does not decrement list capacity 
- python keeps allocated buffer to avoid frequent re-allocations

That does not mean it doesn't shrink

- It shrinks when :  new length of list < capacity/2

- Can be forced shrink by slice or clear+extend

- Python avoids aggressive shrinking because reallocating requires copying pointers, breaks cache locality, causes allocator churn
