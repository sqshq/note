### **Lab 3: Unit Testing with JUnit, Debugging**

### 1 Introduction

JUnit is a Unit Testing Framework for Java.

Unit Testing is a great way to rigorously test each method of your code and ultimately ensure that you have a working project.

The “Unit” part of Unit Testing comes from the idea that you can break your program down into units, or the smallest testable part of an application. Therefore, Unit Testing enforces good code structure (each method should only do “One Thing”), and allows you to consider all of the edge cases for each method and test for them individually.


#### JUnit Syntax

<C>assertEquals</C> is a common method used in JUnit tests. It tests if a variable’s actual value is equivalent to its expected value.

```Java
@Test
public void testMethod() {
    assertEquals(<expected>, <actual>);
}
```

When you create JUnit test files, you should precede each test method with a <C>@Test</C> annotation, and can have one or more <C>assertEquals</C> or <C>assertTrue</C> methods (provided by the JUnit library). **All tests must be non-static.** 

#### Running JUnit Tests in IntelliJ

Even though methods includes many assert statements, only one failure is shown. This is because JUnit tests are short-circuiting – as soon as one of the asserts in a method fails, it will output the failure and move on to the next test.

* Write a test BEFORE we write a method.
* Don’t fill in the code for the actual method yet, just make it return null.
* Write a method, and rerun the tests until it passes.

Pro tip: If you want to have your tests timeout after a certain amount of time (to prevent inﬁnite loops), you can declare your test like this: `:::Java @Test(timeout = 1000)`

#### A Debugging Mystery

Another important skill to learn is how to exhaustively debug. When done properly, debugging should allow you to rapidly narrow down where a bug might be located, even when you are debugging code you don’t fully understand.

Using any combination of the following techniques, figure out whether the bug is in Horrible Steve’s code or in Flik enterprise’s library:

* Writing JUnit tests for the Flik library.
* Using the IntelliJ debugger, especially conditional breakpoints.
* Using print statements.
* Refactoring Horrible Steve’s code. Refactoring means changing the syntax without changing the functionality. This may be hard to do since HS’s code uses lots of weird stuff.

We do not expect you to ﬁx the bug or even understand why it’s happening once you have found it. Instead, your job is simply to find the bug.

Tip: JUnit provides methods <C>assertTrue(boolean)</C> and <C>assertTrue(String, boolean)</C> that you might find helpful.

### Running the 61B Style Checker

We will be using the CS 61B IntelliJ Plugin to check for style. [official 61B style guide](https://sp18.datastructur.es/materials/guides/style-guide)

My common mistake:

* ',' is followed by whitespace.
* Using trailing comments.