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

This lesson covers advanced Python language constructs, some of which are unique to Python.  At several points these techniques bridge the gap between object oriented programming and functional programming, albiet the specific methods might lean toward one side or the other.


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

* Recurson

  | `https://en.wikipedia.org/wiki/Recursion_(computer_science) <https://en.wikipedia.org/wiki/Recursion_(computer_science)>`_


Optional Reading
================

* Lott, S. (2015) Chapter 11. Decorator Design Techniques. In Functional Python Programming.

* Lott, S. (2015) Chapter 6. Recursions and Reductions. In Functional Python Programming.

* Decorators

  | https://wiki.python.org/moin/PythonDecorators

* Context Managers

  | https://docs.python.org/3/library/contextlib.html


*******
Content
*******

Decorator
=========


Context Manager
===============


Multimethods
============


Polymorphism
------------


Recursion
=========

.. code-block:: python3

    def reverse_word(word):
        if word:
            return word[-1] + reverse_word(word[:-1])
        else:
            return ''

The Stack
---------

Tail Call Optimazation
----------------------



****
Quiz
****



********
Activity
********



**********
Assignment
**********



******************
Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
