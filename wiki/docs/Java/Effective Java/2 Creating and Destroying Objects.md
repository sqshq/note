---
title: 2 Creating and Destroying Objects
---

THIS chapter concerns creating and destroying objects: 

* when and how to *create* them
* when and how to *avoid creating* them
* how to ensure they are *destroyed in a timely manner*
* how to manage any *cleanup* actions that must precede their destruction

### Item 1: Consider static factory methods instead of constructors

The traditional way to obtain an instance is to provide a public constructor. Also a public *static factory method*, which returns an instance of the class:

```Java
// translates a Boolean primitive value into a Boolean object reference
public static Boolean valueOf(boolean b) { 
    return b ? Boolean.TRUE : Boolean.FALSE; 
}
```

The static factory method has no direct equivalent in Design Patterns.

#### advantage

* have names: a static factory can describe the object being returned. 
    * e.g. `BigInteger(int, int, Random)`, which returns a `BigInteger` that is probably prime, would have been better expressed as `BigInteger.probablePrime`.
    * A class can have only a single constructor with a given signature. To get around this restriction, Programmers provide two constructors whose parameter lists differ only in the order of their parameter types. Easy to make mistake. 
    * In cases where a class seems to require multiple constructors with the same signature, replace the constructors with static factory methods and carefully chosen names to highlight their differences.
* NOT required to create a new object each time they’re invoked.
    * allow immutable classes to use preconstructed instances
    * or to cache instances as they’re constructed, and dispense them repeatedly to avoid creating unnecessary duplicate objects
    * e.g `:::Java Boolean.valueOf(boolean)` method *never* creates an object.
* return an object of any subtype of their return type.
* the class of the returned object can vary from call to call as a function of the input parameters.
* the class of the returned object need not exist when the class containing the method is written.

#### Distanvantage

* The main limitations that classes without public or protected constructors cannot be subclassed.
* They are hard for programmers to find. -> adhering to common naming conventions(from, of, valueOf, getInstance, newInstance)



### Item 2: Consider a builder when faced with many constructor parameters
### Item 3: Enforce the singleton property with a private constructor or an enum type
### Item 4: Enforce noninstantiability with a private constructor
### Item 5: Prefer dependency injection to hardwiring resources
### Item 6: Avoid creating unnecessary objects 
### Item 7: Eliminate obsolete object references
### Item 8: Avoid finalizers and cleaners 
### Item 9: Prefer try-with-resources to try-finally