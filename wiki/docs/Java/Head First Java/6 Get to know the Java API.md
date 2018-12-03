---
title: 6 Get to know the Java API
toc: false
date: 2017-10-30
---

#### ArrayList

`ArrayList` is a class in the core Java library (the API).

*  `:::Java boolean add(Object elem)`: Adds the objects parameter to the list(return `true`).
*  `:::Java boolean remove(int index)`: Removes the object at the index parameter. Returns `true` if the element was in the list.
*  `:::Java boolean remove(Object elem)`: Removes this object(if it's in the ArrayList).
*  `:::Java boolean contains(Object elem)`: Returns `true` if there's a match for the object parameter.
*  `:::Java boolean isEmpty()`: Returns `true` if the list has no elements
*  `:::Java int indexOf(Object elem)`: Returns either the index of the object parameter, or -1
*  `:::Java size()`: Return the number of elements currently in the list.
*  `:::Java Object get(int index)`: Return the object currently at the index parameter.


You have to know the full name of the class you want to use in your code. You have two options:

* Import: put an import statement at the top of your source code file:
    * `:::Java import java.util.ArrayList`
* Type: type the full name everywhere in your code. Each time you use it.
    * `:::Java java.util.ArrayList<Dog> list = new java.util.ArrayList<Dog>();`

#### Import

An `import` is not the same as `include` in C. So the `import` doesn't make a class bigger. **An `import` statement saves you from typing**. That's really it. It simply give Java the *full name of a class*.

You must tell Java the full name of every class you use, unless that class is in the ***java.lang*** package.