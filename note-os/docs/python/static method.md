### **staticmethod/class method**

Though `classmethod` and `staticmethod` are quite similar, there's a slight difference in usage for both entities: `classmethod` must have a reference to a class object as the first parameter, whereas `staticmethod` can have no parameters at all.

Example

```python
class Date(object):

    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999

date2 = Date.from_string('11-09-2012')
is_date = Date.is_date_valid('11-09-2012')
```


Explanation

Let's assume an example of a class, dealing with date information (this will be our boilerplate):

```python
class Date(object):

    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year
```


This class obviously could be used to store information about certain dates (without timezone information; let's assume all dates are presented in UTC).

Here we have `__init__`, a typical initializer of Python class instances, which receives arguments as a typical `instancemethod`, having the first non-optional argument (self) that holds a reference to a newly created instance.

#### Class Method

We have some tasks that can be nicely done using `classmethods`.

Let's assume that we want to create a lot of Date class instances having date information coming from an outer source encoded as a string with format `'dd-mm-yyyy'`. Suppose we have to do this in different places in the source code of our project.

So what we must do here is:

Parse a string to receive day, month and year as three integer variables or a 3-item tuple consisting of that variable.
Instantiate Date by passing those values to the initialization call.
This will look like:

```python
day, month, year = map(int, string_date.split('-'))
date1 = Date(day, month, year)
```

For this purpose, C++ can implement such a feature with overloading, but Python lacks this overloading. Instead, we can use classmethod. Let's create another "constructor".

```python
    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

date2 = Date.from_string('11-09-2012')
```


Let's look more carefully at the above implementation, and review what advantages we have here:

We've implemented date string parsing in one place and it's reusable now.
Encapsulation works fine here (if you think that you could implement string parsing as a single function elsewhere, this solution fits the OOP paradigm far better).
`cls` is an object that holds the class itself, not an instance of the class. It's pretty cool because if we inherit our Date class, all children will have from_string defined also.


#### Static method

What about `staticmethod`? It's pretty similar to classmethod but doesn't take any obligatory parameters (like a class method or instance method does).

Let's look at the next use case.

We have a date string that we want to validate somehow. This task is also logically bound to the Date class we've used so far, but doesn't require instantiation of it.

Here is where staticmethod can be useful. Let's look at the next piece of code:

```python
    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999

    # usage:
    is_date = Date.is_date_valid('11-09-2012')
```

So, as we can see from usage of staticmethod, we don't have any access to what the class is---it's basically just a function, called syntactically like a method, but without access to the object and its internals (fields and another methods), while classmethod does.