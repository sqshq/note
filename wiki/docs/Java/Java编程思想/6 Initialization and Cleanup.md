---
title: 6 Initialization and Cleanup
toc: false
date: 2017-10-30
---


### Enumerated types

The <C>enum</C> keyword, makes much easier to group together and to use a set of *enumerated types*. Since instances of enumerate types are constants,  they are in all capital letters by convention.

In fact, <C>enum</C>s are classes and have their own methods. The compiler automatically adds useful methods(<C>toString()</C>, <C>ordinal</C>, <C>values()</C> when you create an <C>enum</C>. The <C>ordinal()</C> method indicates the declaration order of a particular  <C>enum</C> constant, and a static <C>values()</C> method that produces an array of values of the  <C>enum</C> constants in the order that they were declared.

An especially nice feature is the way that <C>enum</C>s can be used inside <C>switch</C> statements.

```Java
public enum Spiciness {
  NOT, MILD, MEDIUM, HOT, FLAMING
} 
public class Burrito {
  Spiciness degree;
  public Burrito(Spiciness degree) { this.degree = degree;}
  public void describe() {
    System.out.print("This burrito is ");
    switch(degree) {
      case NOT:    System.out.println("not spicy at all.");
                   break;
      case MILD:
      case MEDIUM: System.out.println("a little hot.");
                   break;
      case HOT:
      case FLAMING:
      default:     System.out.println("maybe too hot.");
    }
  }	
}
```