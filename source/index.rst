.. Lesson Plan documentation master file, created by
   sphinx-quickstart on Sun Jan 28 19:33:27 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
Advanced Python Language Constructs
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


************
Introduction
************

This lesson covers several advanced Python language constructs and problem solving strategies, some of which are unique to Python.  At several points these techniques bridge the gap between object oriented programming and functional programming, albeit the specific methods might lean toward one side or the other.


Recommended Text
================

For the functional programming modules, this lesson included, we recommend Functional Python Programming by Steven Lott.

| Publisher: Packt Publishing
| Pub. Date: January 31, 2015
| Web ISBN-13: 978-1-78439-761-6
| Print ISBN-13: 978-1-78439-699-2
| http://bit.ly/2azI62S

Each lesson's optional readings will draw from this text.


Learning Objectives
===================

Upon successful completion of this lesson, you will be able to:

*
*


New Words or Concepts
=====================

* Decorator
* Context Manager
* Contextlib
* Multimethods
* Recursion


Required Reading
================

* Decorators

  | https://en.wikipedia.org/wiki/Python_syntax_and_semantics#Decorators

* Context Managers

  | `https://docs.python.org/3/library/stdtypes.html#typecontextmanager https://docs.python.org/3/library/stdtypes.html#typecontextmanager>`_
  | https://jeffknupp.com/blog/2016/03/07/python-with-context-managers/

* Multimethods

  | Five-minute Multimethods in Python by Guido van van Rossum
  | https://www.artima.com/weblogs/viewpost.jsp?thread=101605

* Recursion

  | `https://en.wikipedia.org/wiki/Recursion_(computer_science) <https://en.wikipedia.org/wiki/Recursion_(computer_science)>`_


Optional Reading
================

* Lott, S. (2015) Chapter 11. Decorator Design Techniques. In Functional Python Programming.

* Lott, S. (2015) Chapter 6. Recursions and Reductions. In Functional Python Programming.

* Decorators

  | https://wiki.python.org/moin/PythonDecorators
  | https://dbader.org/blog/python-decorators

* Context Managers

  | https://docs.python.org/3/library/contextlib.html


*******
Content
*******

Decorator
=========

Functions are things that generate values based on arguments.  In Python functions are first-class objects.  This means that you can bind names to them, pass them around, etc., just like other objects.  Thanks to this you can write functions that take functions as arguments or return functions as values.

.. code-block:: python

    def substitute(a_function):
        def new_function(*args, **kwargs):
            return "I'm not that other function"
        return new_function


A Definition
------------

There are many things you can do with a simple pattern like this, so many, that we give it a special name: a Decorator.

    "A decorator is a function that takes a function as an argument and
    returns a function as a return value."

That's nice, but why is it useful?

Imagine you are trying to debug a module with a number of functions like this one:

.. code-block:: python

    def add(a, b):
        return a + b

You want to see when each function is called, with what arguments and
with what result. So you rewrite each function as follows:

.. code-block:: python

    def add(a, b):
        print("Function 'add' called with args: {}, {}".format(a, b) )
        result = a + b
        print("\tResult --> {}".format(result))
        return result


That is not particularly nice, especially if you have lots of functions
in your module.  Now imagine we defined the following, more generic *decorator*:

.. code-block:: python

    def logged_func(func):
        def logged(*args, **kwargs):
            print("Function {} called".format(func.__name__))
            if args:
                print("\twith args: {}".format(args))
            if kwargs:
                print("\twith kwargs: {}".format(kwargs))
            result = func(*args, **kwargs)
            print("\t Result --> {}".format(result))
            return result
        return logged

We could then make logging versions of our module functions.

.. code-block:: python

    logging_add = logged_func(add)

Then, where we want to see the results, we can use the logged version:

.. code-block:: ipython

    In []: logging_add(3, 4)
    Function 'add' called
        with args: (3, 4)
         Result --> 7
    Out[]: 7


This is nice, but we must now call the new function wherever we originally called the old one.  It would be nicer if we could just call the old function and have it log.  Remembering that you can easily rebind symbols in Python using simple assignment statements leads to this form:

.. code-block:: python

    def logged_func(func):
        # implemented above

    def add(a, b):
        return a + b

    add = logged_func(add)

And now you can simply use the code you've already written and calls to ``add`` will be logged:

.. code-block:: ipython

    In []: add(3, 4)
    Function 'add' called
        with args: (3, 4)
         Result --> 7
    Out[]: 7


Syntax
------

Rebinding the name of a function to the result of calling a decorator on that function is called **decoration**.  Because this is so common and useful, Python provides a special operator to perform it more *declaratively*: the ``@`` operator.

.. code-block:: python

    def add(a, b):
        return a + b

    # add = logged_func(add)

    @logged_func
    def add(a, b):
        return a + b

The declarative form (called a decorator expression) is more common, but both forms have the identical result and can be used interchangeably.

.. code-block:: python

    In [1]: def my_decorator(func):
       ...:      def inner():
       ...:          print('running inner')
       ...:      return inner
       ...:


    In [2]: def other_func():
       ...:     print('running other_func')

    In [3]: other_func()
    running other_func

    In [4]: other_func = my_decorator(other_func)

    In [5]: other_func()
    In [5]: running inner

    In [6]: other_func
    Out[6]: <function __main__.my_decorator.<locals>.inner>

Which is the same as:

.. code-block:: python


    In [7]: @my_decorator
       ...: def other_func():
       ...:      print('running other_func')
       ...:

    In [8]: other_func()
    running inner

    In [9]: other_func
    Out[9]: <function __main__.my_decorator.<locals>.inner>


Context Manager
===============


Multimethods
============


Polymorphism
------------


Recursion
=========

Recursion is where a function or method calls itself, either directly or indirectly.  When directly, the function simply calls itself from within itself.  When indirectly, the more advanced scenario, it is called by some other function that it had already called; in other words, function a calls function b and then function b calls function a.  In this tutorial we will look at the first case, direct recursive calls.

Recursive algorithms naturally fit certain problems, particularly problems amenable to divide and conquer solutions.  The general form is when a solution can be divided into an operation on the first member of a collection combined with the same operation on the remaining members of the collection.

A key element to a recursive solution involves the specification of a termination condition.  The algorithm needs to know when to end, when to stop calling itself.  Typically this is when all of the members of the collection have been processed.

[Video: Recursion]


Recursion Limitations
---------------------

Python is not ideally suited to recursive programming for a few key reasons:

* mutable data structures
* stackframe limits
* lack of tail call optimization or elimination

Python's workhorse data structure is the list and recursive solutions on list-like sequences can be attractive.  However, Python lists are mutable and when mutable data structures are passed as arguments to functions they can be changed, affecting their value both inside and outside of the called function.  Clean and natural-looking recursive algorithms generally assume that values do not change between recursive calls and generally fail if they do.  Attempts to avoid this problem, say by making copies of the mutable data structure to pass at each successive recursive call, can be expensive both computationally and in terms of memory consumption.  Beware this scenario when designing and debugging recursive functions.

The Python interpreter by default limits the number of recursive calls --- the number of calls a function can make to itself --- to 1000.  This value can be changed at runtime, but if you find you have large data sets to process you may need to consider a non-recursive strategy.  To increase the number of stack frames available to a recursive algorithm, use sys.setrecursionlimit as follows:

.. code-block:: python3

    import sys
    sys.setrecursionlimit(5000)

Where Python sets a hard limit on the number of recursive calls a function can make, the interpreters or run-time engines of some other languages perform a technique called tail call optimization or tail call elimination.  Python's strategy in this context is to keep stack frames intact and unadulterated, which facilitates debugging: recursive stack traces still look like normal, Python stack traces.


Summary
-------

Recursion is generally considered a functional programming technique partly because it grew up in functional programming languages such as Lisp and Scheme, and also because it tends to satisfy the functional objective of avoiding state and thus the mapping of one set of inputs to a single, determinate output.

An astute observer might point out that by storing information on the stack, in successive stack frames, we are storing state.  Are we not?  Yes and no.  The data stored on the stack during the execution of most recursive algorithms become the return values from or the arguments to successive function calls.  This results in a natural composition of functions, but rather than the composition of different functions, for instance g(f(x)) which is the way we normally think about functional composition, recursive algorithms represent the composition of a function with itself: f(f(x)).


****
Quiz
****

1.

2.

3.

4. What conditions are necessary for a successful recursive algorithm?

   |
   | A termination condition.

5. When developing recursive solutions in Python it is important to be aware of what?

   | How many and which other functions will call your recursive function.
   | Your tail call elimination strategy.
   | The mutability of your function arguments and the depth of the call stack.


********
Activity
********

Recursion
=========

Write a recursive solution for the factorial function.

https://en.wikipedia.org/wiki/Factorial


**********
Assignment
**********



******************
Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
