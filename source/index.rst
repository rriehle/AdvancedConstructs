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

* construct decorators
* use context managers
* design and code a recursive algorithm
* articulate the drawbacks of recursion in Python


New Words or Concepts
=====================

* Decorator
* Context Manager
* Contextlib
* Multiple Dispatch
* Multimethods
* Recursion


Required Reading
================

* Decorators

  | https://en.wikipedia.org/wiki/Python_syntax_and_semantics#Decorators

* Context Managers

  | `https://docs.python.org/3/library/stdtypes.html#typecontextmanager <https://docs.python.org/3/library/stdtypes.html#typecontextmanager>`_
  | https://jeffknupp.com/blog/2016/03/07/python-with-context-managers/

* Multiple Dispatch & Multimethods

  | Five-minute Multimethods in Python by Guido van van Rossum
  | https://www.artima.com/weblogs/viewpost.jsp?thread=101605
  | https://en.wikipedia.org/wiki/Multiple_dispatch

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
  | https://www.python.org/dev/peps/pep-0343/

* Recursion

  | https://pointlessprogramming.wordpress.com/tag/tail-call-optimization/


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


There are many things you can do with a simple pattern like this, so many, that we give it a special name: a Decorator.

    "A decorator is a function that takes a function as an argument and returns a function as a return value."

That's nice, but why is it useful?  Imagine you are trying to debug a module with a number of functions like this one:

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

We have seen the ``with`` statement --- probably used when working with files.  It is associated with resource management, but let's work our way there.

A large source of repetition in code deals with the handling of external
resources.  As an example, how many times do you think you might type something like the following:

.. code-block:: python

    file_handle = open('filename.txt', 'r')
    file_content = file_handle.read()
    file_handle.close()
    # do some stuff with the contents

Resource management is roughly half of that code and it is also prone to error.

* What happens if you forget to call ``.close()``?

* What happens if reading the file raises an exception?

Perhaps we should write it something like:

.. code-block:: python

    try:
        file_handle = open(...)
        file_content = file_handle.read()
    except IOError:
        print("The file couldn't be opened")
    finally:
        file_handle.close()

That is getting ugly, and hard to get right.  Should we do the read inside the try or only the open?  Should the read get its own try?  Leaving an open file handle laying around is bad enough.  What if the resource is a network connection, or a database cursor?

Starting in version 2.5, Python provides a structure called a *context manager* for reducing repetition and avoiding errors associated with handling resources.  They encapsulate the setup, error handling, and tear down of resources in a few steps.  The key is to use the ``with`` statement.

Since the introduction of the ``with`` statement in `PEP 343 <https://www.python.org/dev/peps/pep-0343/>`_, the above seven lines of defensive code have been replaced with this simple form:

.. code-block:: python

    with open('filename', 'r') as file_handle:
        file_content = file_handle.read()
    # do something with file_content

The ``open`` builtin is defined as a *context manager*.  The resource it returns (``file_handle``) is automatically and reliably closed when the code block ends.  At this point in Python's evolution, many functions you might expect to behave this way, in fact, do:

* file handling with ``open``
* network connections via ``socket``
* most implementations of database wrappers handle connections or cursors as context managers

But what if you are working with a library that doesn't support this, for instance ``urllib``?

contextlib
----------

If the resource in questions has a ``.close()`` method, then you can simply use the ``closing`` context manager from ``contextlib`` to handle the issue:

.. code-block:: python

    from urllib import request
    from contextlib import closing

    with closing(request.urlopen('http://google.com')) as web_connection:
        # do something with the open resource
    # and by here it will be closed automatically

But what if the thing doesn't have a ``close()`` method, or you're creating
the thing yourself and it shouldn't have a close() method?

(Full confession: urlib.request was not a context manager in py2 --- but it is in py3.  Nonetheless the issue still comes up with third-party packages and of course in your own code.)

Enter and exit
--------------

If you do need to support resource management of some sort, you can write a context manager of your own by implementing the context manager protocol.  The interface is simple.  It must be a class that implements two of the nifty python *special methods*

``__enter__(self)``:
  Called when the ``with`` statement is run, it should return something to work with in the created context.

``__exit__(self, e_type, e_val, e_traceback)``:
  Clean-up that needs to happen is implemented here.

Let's see this in action to get a sense of what happens.  Consider this code:

.. code-block:: python

    class Context(object):
        """from Doug Hellmann, PyMOTW
        https://pymotw.com/3/contextlib/#module-contextlib
        """
        def __init__(self, handle_error):
            print('__init__({})'.format(handle_error))
            self.handle_error = handle_error

        def __enter__(self):
            print('__enter__()')
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            print('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
            return self.handle_error

:download:`context_manager.py <../examples/context_managers/context_manager.py>`

This class doesn't do much of anything, but playing with it can help
clarify the order in which things happen:

.. code-block:: ipython

    In [2]: %paste
        In [46]: with Context(True) as foo:
           ....:     print('This is in the context')
           ....:     raise RuntimeError('this is the error message')

    ## -- End pasted text --
    __init__(True)
    __enter__()
    This is in the context
    __exit__(<class 'RuntimeError'>, this is the error message,
             <traceback object at 0x1047873c8>)

Because the ``__exit__`` method returns ``True``, the raised error is handled.  What if we try with ``False``?

.. code-block:: ipython

    In [3]: with Context(False) as foo:
       ...:     print("this is in the context")
       ...:     raise RuntimeError('this is the error message')
       ...:
    __init__(False)
    __enter__()
    this is in the context
    __exit__(<class 'RuntimeError'>, this is the error message, <traceback object at 0x10349e888>)
    ---------------------------------------------------------------------------
    RuntimeError                              Traceback (most recent call last)
    <ipython-input-3-8837b3d7f123> in <module>()
          1 with Context(False) as foo:
          2     print("this is in the context")
    ----> 3     raise RuntimeError('this is the error message')

    RuntimeError: this is the error message

This time the context manager did not catch the error --- so it was raised the in the usual way.  In real life a context manager could have pretty much any error raised in its context and the context manager will likely only be able to properly handle particular Exceptions, thus the ``__exit__`` method takes all the information about the exception as parameters.

``def __exit__(self, exc_type, exc_val, exc_tb)``

``exc_type``: the type of the Exception

``exc_val``: the value of the Exception

``exc_tb``: the Exception Traceback object

The lets you check if this is a type you know how to handle.

.. code-block:: python

    if exc_type is RuntimeError:

The value is the exception object itself.

And the traceback is a full traceback object.  Traceback objects hold all the information about the context in which and error occurred.  It's pretty advanced stuff, so you can mostly ignore it, but if you want to know more, there are tools for working with them in the ``traceback`` module.

https://docs.python.org/3/library/traceback.html

<<<<<<< HEAD
The contextmanager decorator
----------------------------

Similar to writing iterable classes, there's a fair bit of bookkeeping involved.  It turns out you can take advantage of generator functions to do that bookkeeping for you.  The ``contextlib.contextmanager`` decorator will turn a generator function into context manager.  Consider this code:

.. code-block:: python

    from contextlib import contextmanager

    @contextmanager
    def context(boolean):
        print("__init__ code here")
        try:
            print("__enter__ code goes here")
            yield object()
        except Exception as e:
            print("errors handled here")
            if not boolean:
                raise e
        finally:
            print("__exit__ cleanup goes here")

The code is similar to the class defined previously and using it has similar results.  We can handle errors.

.. code-block:: ipython

    In [96]: with context(True):
       ....:     print("in the context")
       ....:     raise RuntimeError("error raised")
       ....:
    __init__ code here
    __enter__ code goes here
    in the context
    errors handled here
    __exit__ cleanup goes here

Or, we can allow them to propagate:

.. code-block:: ipython

    In [51]: with context(False):
       ....: print("in the context")
       ....: raise RuntimeError("error raised")
    __init__ code here
    __enter__ code goes here
    in the context
    errors handled here
    __exit__ cleanup goes here
    ---------------------------------------------------------------------------
    RuntimeError                              Traceback (most recent call last)
    <ipython-input-51-641528ffa695> in <module>()
          1 with context(False):
          2     print "in the context"
    ----> 3     raise RuntimeError("error raised")
          4
    RuntimeError: error raised

=======
>>>>>>> rriehle
Mixing context_managers with generators
---------------------------------------

You can put a ``yield`` inside a context manager as well.  Here is a generator function that gives yields all the files in a directory.

.. code-block:: python

    import pathlib

    def file_yielder(dir=".", pattern="*"):
        """
        iterate over all the files that match the pattern

        pattern us a "glob" pattern, like: *.py
        """
        for filename in pathlib.Path(dir).glob(pattern):
            with open(filename) as file_obj:
                yield file_obj

:download:`file_yielder.py <../examples/context_managers/file_yielder.py>`

The ``yield`` is inside the file context manager, so that state will be preserved while the file object is in use.  This generator can be used as follows.

.. code-block:: ipython

    In [20]: for f in file_yielder(pattern="*.py"):
        ...:     print("The first line of: {} is:\n{}".format(f.name, f.readline()))

In each iteration through the loop the previous file gets closed and the new one opened.  If there is an exception raised inside the loop, the last file will get properly closed.


Multiple Dispatch & Multimethods
================================

.. https://canvas.uw.edu/courses/1212062/pages/lesson-02-dot-02-currying?module_item_id=8222029
.. https://www.artima.com/forums/flat.jsp?forum=106&thread=101605
.. https://stackoverflow.com/questions/14858192/force-a-function-parameter-type-in-python
.. https://gist.github.com/bcse/1443027
.. https://eli.thegreenplace.net/tag/multiple-dispatch
.. https://dzone.com/articles/a-polyglots-guide-to-multiple-dispatch-part-ii
.. https://pypi.python.org/pypi/multimethod/0.6
.. https://bitbucket.org/coady/multimethod



Recursion
=========

Recursion is where a function or method calls itself, either directly or indirectly.  When directly, the function simply calls itself from within itself.  When indirectly, the more advanced scenario, it is called by some other function that it had already called; in other words, function a calls function b and then function b calls function a.  In this tutorial we will look at the first case, direct recursive calls.

Recursive algorithms naturally fit certain problems, particularly problems amenable to divide and conquer solutions.  The general form is when a solution can be divided into an operation on the first member of a collection combined with the same operation on the remaining members of the collection.

A key element to a recursive solution involves the specification of a termination condition.  The algorithm needs to know when to end, when to stop calling itself.  Typically this is when all of the members of the collection have been processed.


Recursion Limitations
---------------------

Python is not ideally suited to recursive programming for a few key reasons.

Mutable Data Structures
^^^^^^^^^^^^^^^^^^^^^^^

Python's workhorse data structure is the list and recursive solutions on list-like sequences can be attractive.  However, Python lists are mutable and when mutable data structures are passed as arguments to functions they can be changed, affecting their value both inside and outside of the called function.  Clean and natural-looking recursive algorithms generally assume that values do not change between recursive calls and generally fail if they do.  Attempts to avoid this problem, say by making copies of the mutable data structure to pass at each successive recursive call, can be expensive both computationally and in terms of memory consumption.  Beware this scenario when designing and debugging recursive functions.

An astute observer might point out that by storing information on the stack, in successive stack frames, we are storing state, and that this is counter to functional programming's aversion to mutable state and its attraction to functional purity.  Are we or are we not?  The data stored on the stack during the execution of most recursive algorithms become the return values from and the arguments to successive function calls.  This results in a natural composition of functions, but rather than the composition of different functions, for instance ``g(f(x))`` which is the way we normally think about functional composition, recursive algorithms represent the composition of a function with itself: ``f(f(x))``.  Provided we are using immutable data structures in our calls, or provided we are careful not to mutate values between successive recursive calls, recursion should work.

Stackframe Limits
^^^^^^^^^^^^^^^^^

The Python interpreter by default has its stackframe limit set to 1000.  This value can be changed at runtime, but if you find you have large data sets to process you may need to consider a non-recursive strategy.  To increase the number of stack frames use sys.setrecursionlimit as follows:

.. code-block:: python3

    import sys
    sys.setrecursionlimit(5000)

Lack of Tail Call Optimization or Elimination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Where Python sets a hard limit on the number of recursive calls a function can make, the interpreters or run-time engines of some other languages perform a technique called tail call optimization or tail call elimination.  Python's strategy in this context is to keep stack frames intact and unadulterated, which facilitates debugging: recursive stack traces still look like normal Python stack traces.


Summary
-------

Recursion is generally considered a functional programming technique partly because it grew up in functional programming languages such as Lisp and Scheme, yet also because it tends to satisfy the functional objective of avoiding state and thus the mapping of one set of inputs to a single, determinate output.  It is a natural way to express many core algorithms having to do with sequences and tree structures, both of which pervade programming.  It has its limitations in Python, but is worth understanding and using nonetheless.


****
Quiz
****

1. Decorators rely on Python's ability to

   | Pass functions to other functions
   | Return functions from functions
   | Rebind function names to new or different functions


2. Context managers facilitate what types of problems?

   | Resource management
   | Opening and closing file handles and database cursors
   | Inheritance in the context of multiple parent classes
   | The opening and closing of closures
   | Determining the call sequence of nested decorators

3.

4. What condition is necessary for a successful recursive algorithm?

   | Pep8 compliance
   | A conditional condition
   | Mutable arguments
   | A termination condition

5. When developing recursive solutions in Python it is important to be aware of what?

   | How many and which other functions will call your recursive function.
   | Your tail call elimination strategy.
   | of what? of what? of what? of what? of what?
   | The mutability of your function arguments and the depth of the call stack.


*********************
Activity & Assignment
*********************

Context Managers
================

The `Ballard Lockes <https://en.wikipedia.org/wiki/Ballard_Locks>`_ in Seattle, Washington are a limited, controlled resource.  You have been hired by the Army Corps of Engineers to help build a software control system for the lockes.  There are two lockes at the locke complex, one small (30 x 150 feet, 8.5 x 45.7 meter) and one large (80 x 825 feet, 24.4 x 251.5 meter).  There are myriad ways in which different components of the lockees represent limited resources with specialized subsystems, and a missed or out-of-sequence step could mean disaster.  For instance, there are two sets of doors for each locke, one upstream and one down, that cannot both be open at the same time; boats need to clear the doors before they are closed, sealed and locked; pumps need to be shut down before locke doors are opened; observing tourists who can get very close to the action need to be safely managed; the lockes themselves can only handle a certain number of boats.  At every step of the way there is a limited resource that must be managed and in step with the others.  In effect it involves the tight management of resources all the way down.

For this first task you do not need to model every aspect of the locks, indeed you only need model its operation overall.  Early on you learn that there will be other software developers interacting with the system and that not everyone is going to remember all the details of using the resources of each component.  Your task is to make the use of the components as simple as possible, so that other developers don't need to remember all of the steps associated with each component's use.  You think to yourself that this is a good environment for context managers and so this is how you will model the overall functioning.

As an early design decision you have decided to avoid overloading the term lock, which in the context can be interpreted both as a verb and as a noun and thereby cause confusion.  For any instances of the verb you will use its usual spelling: lock.  For any instances of the noun you will use an alternative spelling: locke.

Write a context manager class ``Locke`` to simulate the overall functioning of the system.  When the locke is entered it stops the pumps, opens the doors, closes the doors, and restarts the pumps.  Likewise when the locke is exited it runs through the same steps: it stops the pumps, opens the doors, closes the doors, and restarts the pumps.  Don't worry for now that in the real world there are both upstream and downstream doors; perhaps you'll get to that later.  During initialization the context manger class accepts its capacity in number of boats.  If someone tries to move too many boats through the locke, anything over its established capacity, raise a suitable error.  Since this is a simulation you need do nothing more than print what is happening with the doors and pumps, like this:

.. code-block:: bash

    "Stopping the pumps."
    "Opening the doors."
    "Closing the doors."
    "Restarting the pumps."

This is how you might interact with your Locke class.

.. code-block:: python3

    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)

    # A lock with sufficient capacity can move boats without incident.
    with large_locke as locke:
        locke.move_boats_through(boats)


Recursion
=========

Write a recursive solution for the factorial function.

https://en.wikipedia.org/wiki/Factorial





******************
Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
